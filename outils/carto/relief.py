"""Construction du relief : relief réel (graine) + altérations du Beliet (jardin)."""
import numpy as np
from pyproj import Geod
from scipy.ndimage import distance_transform_edt, gaussian_filter, label, map_coordinates
from shapely.affinity import scale as sh_scale
from shapely.geometry import LineString, Polygon
from shapely.ops import linemerge, unary_union

from .grille import (bruit_bande, bruit_crete, distance_polyligne, lisser_polyligne, smax, smin)
from .sources import contour_beliet, fleuves_reels, relief_reel

GEOD = Geod(ellps="WGS84")


def aire_poly_ll(coords):
    lon = [c[0] for c in coords]
    lat = [c[1] for c in coords]
    a, _ = GEOD.polygon_area_perimeter(lon, lat)
    return abs(a) / 1e6


def ajuster_aire(coords, cible_km2, seulement_nord_sud=False):
    """Homothétie autour du centroïde pour atteindre la superficie cible."""
    a = aire_poly_ll(coords)
    f = np.sqrt(cible_km2 / a)
    P = Polygon(coords)
    if seulement_nord_sud:
        Q = sh_scale(P, xfact=1.0, yfact=cible_km2 / a, origin=P.centroid)
    else:
        Q = sh_scale(P, xfact=f, yfact=f, origin=P.centroid)
    return [list(c) for c in Q.exterior.coords], a


def _km(g):
    return g.km_px[:, None]


class Relief:
    """Contient l'altitude et tous les masques produits pendant la construction."""

    def __init__(self, p, g, log=print):
        self.p, self.g, self.log = p, g, log
        self.graine = p["cadre"]["graine_aleatoire"]
        self.L = p["niveaux"]["halakhel_surface_m"]
        self.LON, self.LAT = np.meshgrid(g.lons.astype(np.float32), g.lats.astype(np.float32))
        self.infos = {}

    def __getstate__(self):
        d = self.__dict__.copy()
        for k in ("LON", "LAT", "n_lisse", "log"):
            d.pop(k, None)
        return d

    def __setstate__(self, d):
        self.__dict__.update(d)
        self.LON, self.LAT = np.meshgrid(self.g.lons.astype(np.float32), self.g.lats.astype(np.float32))
        self.log = print

    # ------------------------------------------------------------------ base
    def base(self):
        g, p = self.g, self.p
        self.log("  relief réel…")
        h = relief_reel(g)
        self.h_reel = h.copy()
        c = contour_beliet(p)
        self.contour_ll = c
        poly = g.poly_px(c).buffer(0)
        beliet = g.rasteriser(poly).astype(bool)
        d_px = distance_transform_edt(~beliet)
        decoupe = (self.LAT < 5.6) & (self.LON > 9.4) & (self.LON < 41.7)
        proche = (~beliet) & (d_px <= 5) & ~decoupe
        h[beliet & (h <= 0)] = 3.0
        h[proche & (h > 0)] = -8.0
        # archipels du Beliet hors contour (Staur-Khlōr)
        archi = np.zeros(g.shape, bool)
        for a in p.get("archipels", []):
            if "zone" in a:
                archi |= g.rasteriser(g.poly_px(a["zone"])).astype(bool)
        self.beliet = beliet | (archi & (h > 0))
        self.decoupe = decoupe & ~beliet & (h > 0)
        self.h = h
        self.n_lisse = bruit_bande(g.shape, self.graine + 7, 6, 400)

    # ------------------------------------------------------------ écrêtements
    def ecreter(self):
        g, h = self.g, self.h
        for e in self.p.get("ecretements", []):
            m = g.rasteriser(g.poly_px(e["zone"])).astype(bool) & self.beliet
            s, f = e["seuil_m"], e["facteur"]
            haut = m & (h > s)
            h[haut] = s + f * (h[haut] - s)
            self.log(f"  écrêtement « {e['nom']} » : max {h[m].max():.0f} m")

    # ------------------------------------------------------------------ lacs
    def preparer_lacs(self):
        g = self.g
        self.lacs = []
        for lac in self.p["lacs"]:
            coords, a0 = ajuster_aire(lac["contour"], lac["superficie_cible_km2"])
            m0 = g.rasteriser(g.poly_px(coords)).astype(bool)
            km = _km(g)
            din = distance_transform_edt(m0) * km
            dout = distance_transform_edt(~m0) * km
            graine = self.graine + sum(map(ord, lac["geo_id"]))
            n = bruit_bande(g.shape, graine, 3, 40 / g.km_px_eq)
            nG = bruit_bande(g.shape, graine + 1, 30 / g.km_px_eq, 250 / g.km_px_eq)
            m = (din - dout + 6.0 * n + 22.0 * nG) > 0
            lab, nl = label(m)
            core = lab[m0 & (din > 10)]
            garde = np.isin(lab, np.unique(core[core > 0]))
            self.lacs.append(dict(cfg=lac, masque=garde, coords=coords))
            self.log(f"  lac {lac['geo_id']} : contour dessiné {a0:,.0f} km² → ajusté {lac['superficie_cible_km2']:,} km²")

    def soulever_lacs(self):
        g, h = self.g, self.h
        for L in self.lacs:
            c = L["cfg"]
            d = distance_transform_edt(~L["masque"]) * _km(g)
            u = c["soulevement_regional_m"] * np.exp(-(d / c["rayon_soulevement_km"]) ** 2)
            h += np.where(self.beliet, u, 0).astype(np.float32)

    # --------------------------------------------------------------- chaînes
    def chaines(self):
        g, p = self.g, self.p
        km_eq = g.km_px_eq
        self.log("  bruit de crêtes…")
        R = bruit_crete(g.shape, self.graine + 11, 2.0, 70 / km_eq, octaves=6)
        warp = bruit_bande(g.shape, self.graine + 13, 40 / km_eq, 500 / km_eq)
        detail = bruit_bande(g.shape, self.graine + 17, 1.5, 25 / km_eq, pente=1.0)
        pied = gaussian_filter(self.h, 45 / km_eq)
        self.crete = np.zeros(g.shape, np.float32)   # intensité « montagne » (0-1), pour la suite
        self.axes = []
        for ch in p["chaines"]:
            pts = np.array(ch["points"], float)
            fin = lisser_polyligne(pts, sous=10)
            hw_max = pts[:, 3].max()
            d, s = distance_polyligne(g, fin[:, :2], hw_max * 1.6)
            i = np.clip(np.floor(s).astype(int), 0, len(fin) - 2)
            t = s - i
            crete = fin[i, 2] * (1 - t) + fin[i + 1, 2] * t
            hw = fin[i, 3] * (1 - t) + fin[i + 1, 3] * t
            u = (d + 0.28 * hw * warp) / hw
            prof = np.clip(1 - u, 0, 1) ** 1.6
            mod = 0.42 + 0.62 * R
            rug = ch.get("rugosite", 1.0)
            m = pied + (crete - pied) * prof * mod + rug * detail * 120 * prof
            zone = (prof > 0) & self.beliet
            if ch["mode"] == "plancher":
                m = pied + (crete - pied) * prof * (0.55 + 0.4 * R)
                self.h = np.where(zone, smax(self.h, m, 80), self.h).astype(np.float32)
            else:
                self.h = np.where(zone, smax(self.h, m, 160), self.h).astype(np.float32)
            self.crete = np.maximum(self.crete, np.where(zone, prof, 0)).astype(np.float32)
            ys, xs = np.nonzero(zone)
            bb = None
            if len(ys):
                bb = (ys.min(), ys.max() + 1, xs.min(), xs.max() + 1)
                bb = (bb, prof[bb[0]:bb[1], bb[2]:bb[3]].astype(np.float32), pied[bb[0]:bb[1], bb[2]:bb[3]].astype(np.float32))
            self.axes.append(dict(cfg=ch, ligne=fin[:, :2], zone=bb))
            zm = zone & (prof > 0.5)
            if zm.any():
                self.log(f"  chaîne {ch['geo_id']:<26} crête médiane {np.median(self.h[zm]):5.0f} m, max {self.h[zone].max():5.0f} m")

    # ------------------------------------------------------------- Halakhel
    def halakhel(self):
        g, p = self.g, self.p
        H = p["halakhel"]
        km = _km(g)
        a_bras = aire_poly_ll(H["bras_nord_ouest"])
        cible = H.get("superficie_cible_km2", 1350000) - a_bras
        princ, a0 = ajuster_aire(H["bassin_principal"], cible * 1.04, seulement_nord_sud=True)
        self.log(f"  Halakhel : bassin dessiné {a0:,.0f} km² → ajusté {cible * 1.06:,.0f} km² (+ bras {a_bras:,.0f})")
        geoms = [g.poly_px(princ), g.poly_px(H["bras_nord_ouest"])]
        for cle in ("detroit_khreth_na_serek", "ria_tawalmaz"):
            e = H[cle]
            ligne = g.ligne_px(e["trace"])
            lat = np.mean([c[1] for c in e["trace"]])
            geoms.append(ligne.buffer(e["largeur_km"] / 2 / g.km_px_a(lat), cap_style=2))
        m0 = g.rasteriser(unary_union(geoms)).astype(bool)
        din = distance_transform_edt(m0) * km
        dout = distance_transform_edt(~m0) * km
        n = bruit_bande(g.shape, self.graine + 21, 4, 120 / g.km_px_eq)
        nG = bruit_bande(g.shape, self.graine + 22, 80 / g.km_px_eq, 600 / g.km_px_eq)
        ouest = np.clip((12 - self.LON) / 5, 0, 1)
        rias = bruit_crete(g.shape, self.graine + 24, 2, 60 / g.km_px_eq, octaves=3)
        amp = 9 + 10 * ouest
        n = n + 2.2 * ouest * (rias - 0.5) * 2
        n = n + nG * (55 / amp)
        # le détroit et la ria gardent leur largeur
        etroit = g.rasteriser([geoms[2].buffer(10), geoms[3].buffer(10)]).astype(bool)
        amp = np.where(etroit, 1.5, amp)
        m = (din - dout + amp * n) > 0
        lab, _ = label(m)
        core = lab[m0 & (din > 25)]
        m = np.isin(lab, np.unique(core[core > 0]))
        m &= self.beliet
        # garder une bande de Sumdan entre la mer intérieure et la Méditerranée
        d_ocean = distance_transform_edt(self.beliet) * km
        m &= d_ocean > H.get("distance_min_ocean_km", 70)
        m &= ((H.get("longitude_max_est", 28.4) - self.LON) * 100 + 14 * n) > 0
        lab, _ = label(m)
        core = lab[m0 & (din > 25)]
        m = np.isin(lab, np.unique(core[core > 0]))
        d = distance_transform_edt(m) * km
        n2 = bruit_bande(g.shape, self.graine + 23, 8, 300 / g.km_px_eq)
        Dmax = p["niveaux"]["halakhel_profondeur_max_m"]
        fond = self.L - Dmax * (1 - np.exp(-d / 150)) ** 1.15 * np.clip(0.82 + 0.2 * n2, 0.5, 1.05)
        # îles volcaniques (proposition) + îlots côtiers
        rng = np.random.default_rng(self.graine + 29)
        iles = np.full(g.shape, -1e9, np.float32)
        def bosse(lon, lat, haut, rayon_km):
            x, y = g.px(lon, lat)
            r = rayon_km / g.km_px_a(lat)
            x0, x1 = int(max(0, x - 2 * r)), int(min(g.W, x + 2 * r + 1))
            y0, y1 = int(max(0, y - 2 * r)), int(min(g.H, y + 2 * r + 1))
            yy, xx = np.mgrid[y0:y1, x0:x1]
            rr = np.hypot(xx + 0.5 - x, yy + 0.5 - y) / r
            v = self.L + haut * np.clip(1 - rr, 0, None) ** 1.3 - 450 * rr * rr
            iles[y0:y1, x0:x1] = np.maximum(iles[y0:y1, x0:x1], v)
        for (lon, lat) in H["iles_volcaniques"]:
            bosse(lon, lat, rng.uniform(250, 900), rng.uniform(9, 22))
        ys, xs = np.nonzero(m & (d > 6) & (d < 45))
        k = 0
        essais = 0
        while k < H["ilots_cotiers_nombre"] and essais < 5000:
            essais += 1
            j = rng.integers(len(xs))
            lon, lat = g.ll(xs[j] + 0.5, ys[j] + 0.5)
            bosse(float(lon), float(lat), rng.uniform(15, 120), rng.uniform(3, 9))
            k += 1
        bruit_ile = bruit_bande(g.shape, self.graine + 31, 2, 20 / g.km_px_eq)
        iles = iles + 25 * bruit_ile
        fond = np.maximum(fond, iles)
        self.h = np.where(m, fond, self.h).astype(np.float32)
        self.mer = m & (self.h < self.L)
        # glacis : le terrain descend en pente douce vers la mer intérieure (§VI, HKL_S « glacis »)
        dout2 = distance_transform_edt(~self.mer) * km
        pente = H.get("pente_glacis_m_par_km", 5.5)
        glacis = self.L + 15 + pente * dout2
        zone_g = self.beliet & ~self.mer & (dout2 < 260)
        w = np.clip((260 - dout2) / 80, 0, 1)
        cible_g = smin(self.h, glacis, 120)
        self.h = np.where(zone_g, self.h + w * (cible_g - self.h), self.h).astype(np.float32)
        # rives : pas de terre sous le niveau de la mer intérieure au contact de celle-ci
        rive = self.beliet & ~self.mer & (dout2 < 45)
        w = np.clip((45 - dout2) / 25, 0, 1)
        cible = smax(self.h, self.L + 2 + 4 * np.minimum(dout2, 15), 40)
        self.h = np.where(rive, self.h + w * (cible - self.h), self.h).astype(np.float32)
        aire = (self.g.aire_km2()[self.mer]).sum()
        lab_i, n_i = label(m & ~self.mer)
        self.infos["halakhel_km2"] = aire
        self.infos["halakhel_iles"] = n_i
        self.log(f"  mer Halakhel : {aire:,.0f} km², {n_i} îles, fond min {self.h[self.mer].min():.0f} m")

    # ------------------------------------------------------- lacs : creusement
    def creuser_lacs(self):
        g = self.g
        km = _km(g)
        self.lac = np.zeros(g.shape, np.uint8)
        for k, L in enumerate(self.lacs, start=1):
            c, m = L["cfg"], L["masque"]
            d = distance_transform_edt(m) * km
            dout = distance_transform_edt(~m) * km
            n = bruit_bande(g.shape, self.graine + 41 + k, 3, 80 / g.km_px_eq)
            recifs = bruit_crete(g.shape, self.graine + 43 + k, 2, 30 / g.km_px_eq, octaves=3)
            fond = c["altitude_m"] - c["profondeur_max_m"] * (1 - np.exp(-d / 45)) ** 1.2 * np.clip(0.75 + 0.3 * n, 0.3, 1.0)
            fond = fond + np.where(recifs > 0.78, (recifs - 0.78) * 900, 0) * (d > 15)
            fond = np.minimum(fond, c["altitude_m"] - 2 + np.where(recifs > 0.93, 30, 0))
            self.h = np.where(m, fond, self.h).astype(np.float32)
            rive = self.beliet & ~m & (dout < 70)
            w = np.clip((70 - dout) / 40, 0, 1)
            cible = smax(self.h, c["altitude_m"] + 3 + 2.2 * np.minimum(dout, 25), 40)
            self.h = np.where(rive, self.h + w * (cible - self.h), self.h).astype(np.float32)
            self.lac[m & (self.h < c["altitude_m"])] = k
            L["masque_eau"] = self.lac == k
            aire = g.aire_km2()[L["masque_eau"]].sum()
            self.log(f"  lac {c['geo_id']:<16} {aire:9,.0f} km² à {c['altitude_m']} m")

    # ---------------------------------------------------------------- fleuves
    def preparer_fleuves(self):
        """Tracés des fleuves nommés (lon/lat), orientés de l'amont vers l'aval."""
        reels = None
        out = []
        for f in self.p["fleuves"]:
            lignes = []
            if "reel" in f:
                reels = reels or fleuves_reels()
                segs = []
                for nom in f["reel"]:
                    segs += [LineString(c) for c in reels.get(nom, []) if len(c) > 1]
                fus = linemerge(unary_union(segs))
                geoms = [fus] if fus.geom_type == "LineString" else list(fus.geoms)
                for gm in geoms:
                    c = np.array(gm.coords)
                    if "couper_au_nord_de" in f:
                        c = c[c[:, 1] <= f["couper_au_nord_de"] + 1e-6]
                    if "garder_au_nord_de" in f:
                        c = c[c[:, 1] >= f["garder_au_nord_de"] - 1e-6]
                    if len(c) > 2:
                        lignes.append(c)
            if "trace" in f:
                lignes.append(np.array(lisser_polyligne(np.array(f["trace"]), sous=6)))
            for b in f.get("bras", []):
                lignes.append(np.array(lisser_polyligne(np.array(b), sous=6)))
            # orientation : la source est l'extrémité la plus haute (relief réel)
            orient = []
            for c in lignes:
                x, y = self.g.px(c[:, 0], c[:, 1])
                z = map_coordinates(self.h_reel, [np.clip(y, 0, self.g.H - 1), np.clip(x, 0, self.g.W - 1)], order=1)
                if "trace" in f or z[0] >= z[-1]:
                    orient.append(c)
                else:
                    orient.append(c[::-1])
            # méandres pour les tracés dessinés à la main
            if "trace" in f:
                orient = [self._meandres(c, k) for k, c in enumerate(orient)]
            out.append(dict(cfg=f, lignes=orient))
        self.fleuves = out

    def _meandres(self, c, k):
        g = self.g
        x, y = g.px(c[:, 0], c[:, 1])
        P = np.c_[x, y]
        seg = np.hypot(*np.diff(P, axis=0).T)
        L = np.r_[0, np.cumsum(seg)]
        n = max(2, int(L[-1] / 0.7))
        s = np.linspace(0, L[-1], n)
        X = np.interp(s, L, P[:, 0]); Y = np.interp(s, L, P[:, 1])
        dx = np.gradient(X); dy = np.gradient(Y); nn = np.hypot(dx, dy) + 1e-9
        rng = np.random.default_rng(self.graine + 300 + k + int(abs(c[0, 0]) * 10))
        w = rng.standard_normal(n)
        from scipy.ndimage import gaussian_filter1d
        lam = 18 / g.km_px_eq
        off = gaussian_filter1d(w, lam) ; off /= off.std() + 1e-9
        off2 = gaussian_filter1d(rng.standard_normal(n), lam / 3); off2 /= off2.std() + 1e-9
        amp = (5 * off + 1.6 * off2) / g.km_px_eq
        taper = np.clip(np.minimum(s, L[-1] - s) / (25 / g.km_px_eq), 0, 1)
        X2 = X - dy / nn * amp * taper
        Y2 = Y + dx / nn * amp * taper
        lon, lat = g.ll(X2, Y2)
        return np.c_[lon, lat]

    def creuser_fleuves(self):
        g = self.g
        km = _km(g)
        eau = self.mer | (self.lac > 0) | (~self.beliet & (self.h <= 0))
        self.niveau = np.zeros(g.shape, np.float32)
        self.niveau[self.mer] = self.L
        for k, L in enumerate(self.lacs, start=1):
            self.niveau[self.lac == k] = L["cfg"]["altitude_m"]
        self.lit = np.zeros(g.shape, bool)
        for F in self.fleuves:
            larg = F["cfg"].get("largeur", 2)
            w_km = 7 + 4 * larg
            for c in F["lignes"]:
                x, y = g.px(c[:, 0], c[:, 1])
                P = np.c_[x, y]
                seg = np.hypot(*np.diff(P, axis=0).T)
                Ls = np.r_[0, np.cumsum(seg)]
                n = max(2, int(Ls[-1] / 0.4))
                s = np.linspace(0, Ls[-1], n)
                X = np.interp(s, Ls, P[:, 0]); Y = np.interp(s, Ls, P[:, 1])
                ix = np.clip(X.astype(int), 0, g.W - 1); iy = np.clip(Y.astype(int), 0, g.H - 1)
                dans_eau = eau[iy, ix]
                z = np.where(dans_eau, self.niveau[iy, ix], self.h[iy, ix]).astype(np.float64)
                z = np.minimum.accumulate(z)
                z = z - 4
                # ne pas creuser sous l'eau
                trace = np.zeros(g.shape, bool)
                zr = np.full(g.shape, np.nan, np.float32)
                ok = ~dans_eau
                trace[iy[ok], ix[ok]] = True
                zr[iy[ok], ix[ok]] = z[ok]
                if not trace.any():
                    continue
                x0, x1 = max(0, ix.min() - 60), min(g.W, ix.max() + 61)
                y0, y1 = max(0, iy.min() - 60), min(g.H, iy.max() + 61)
                sub = trace[y0:y1, x0:x1]
                dist, (iy2, ix2) = distance_transform_edt(~sub, return_indices=True)
                dk = dist * km[y0:y1]
                znear = zr[y0:y1, x0:x1][iy2, ix2]
                hs = self.h[y0:y1, x0:x1]
                f = np.clip(dk / w_km, 0, 1) ** 1.35
                nouv = znear + (hs - znear) * f
                app = (dk < w_km) & (hs > znear) & self.beliet[y0:y1, x0:x1] & ~eau[y0:y1, x0:x1]
                hs[app] = nouv[app]
                self.lit[y0:y1, x0:x1] |= sub

    def ilots(self):
        g = self.g
        rng = np.random.default_rng(self.graine + 51)
        for a in self.p.get("archipels", []):
            for lon, lat in a.get("ilots", []):
                x, y = g.px(lon, lat)
                r = rng.uniform(3, 6) / g.km_px_a(lat)
                x0, x1 = int(x - 2 * r), int(x + 2 * r + 1)
                y0, y1 = int(y - 2 * r), int(y + 2 * r + 1)
                yy, xx = np.mgrid[y0:y1, x0:x1]
                rr = np.hypot(xx + 0.5 - x, yy + 0.5 - y) / r
                v = rng.uniform(15, 70) * np.clip(1 - rr, 0, None) ** 1.2 - 30 * rr
                sub = self.h[y0:y1, x0:x1]
                np.maximum(sub, v, out=sub)
                self.beliet[y0:y1, x0:x1] |= v > 0

    def ajuster_sommets(self):
        """Cale le point culminant de chaque chaîne sur l'altitude canonique (après érosion)."""
        for ax in self.axes:
            cible = ax["cfg"].get("altitude_max_m")
            if not cible or ax["zone"] is None:
                continue
            (y0, y1, x0, x1), prof, pied = ax["zone"]
            sub = self.h[y0:y1, x0:x1]
            ok = (prof > 0.02) & self.terre[y0:y1, x0:x1] & (prof >= self.crete[y0:y1, x0:x1] - 1e-6)
            if not ok.any():
                continue
            i = np.argmax(np.where(ok, sub, -1e9))
            M, P0 = sub.ravel()[i], pied.ravel()[i]
            if M - P0 < 50:
                continue
            s = (cible - P0) / (M - P0)
            w = np.clip(prof * 1.5, 0, 1)
            fac = 1 + (s - 1) * w
            nouv = np.where(ok & (sub > pied), pied + (sub - pied) * fac, sub)
            self.h[y0:y1, x0:x1] = nouv.astype(np.float32)
            self.log(f"  sommet {ax['cfg']['geo_id']:<26} {M:5.0f} m → {cible} m")

    # ------------------------------------------------------------- ensemble
    def construire(self):
        self.base()
        self.ecreter()
        self.preparer_lacs()
        self.soulever_lacs()
        self.chaines()
        self.halakhel()
        self.ilots()
        self.creuser_lacs()
        self.preparer_fleuves()
        self.creuser_fleuves()
        # masques finaux
        self.ocean = ~self.beliet & ~self.decoupe & (self.h <= 0)
        self.dehors = ~self.beliet & ~self.ocean
        self.eau = self.ocean | self.mer | (self.lac > 0)
        self.terre = self.beliet & ~self.mer & (self.lac == 0)
        return self
