"""Climat simplifié : advection d'humidité par régimes de vents, pluie orographique, calibration."""
import numpy as np
from numba import njit
from scipy.ndimage import rotate, zoom, gaussian_filter, map_coordinates
from scipy.optimize import nnls

# régimes : (nom, direction vers laquelle souffle le vent en degrés [0 = est, 90 = nord], sources, recyclage)
REGIMES = [
    ("mousson_sud_ouest", 50, ("atl_s", "decoupe", "lacs"), 0.62),
    ("mousson_sud", 95, ("decoupe", "atl_s", "lacs"), 0.62),
    ("mousson_ouest", 15, ("decoupe", "atl_s", "lacs", "marais_sud"), 0.82),
    ("flux_ouest", 5, ("atl_n", "atl_s", "lacs_nord"), 0.35),
    ("hiver_nord_ouest", 305, ("med", "atl_n", "halakhel"), 0.25),
    ("vents_est", 185, ("est", "rouge"), 0.4),
    ("vents_nord", 265, ("med", "halakhel", "lacs_nord"), 0.25),
]


@njit(cache=True)
def _marche(h, src, terre, dx_m, p0, p1, recyc, seche):
    H, W = h.shape
    P = np.zeros((H, W), np.float64)
    for y in range(H):
        q = 0.0
        for x in range(W):
            s = src[y, x]
            if s > 0:
                q += (s - q) * 0.3
                P[y, x] = q * 0.02
                continue
            if not terre[y, x]:
                q *= 0.97
                continue
            up = 0.0
            dn = 0.0
            if x > 0:
                d = (h[y, x] - h[y, x - 1]) / dx_m
                if d > 0:
                    up = d
                else:
                    dn = -d
            pb = q * p0 * (1.0 + 0.5 * h[y, x] / 1000.0) * np.exp(-seche * dn * 1000.0)
            po = q * p1 * up * 1000.0
            if pb + po > 0.35 * q:
                f = 0.35 * q / (pb + po)
                pb *= f
                po *= f
            q -= pb * (1.0 - recyc) + po
            # capacité de l'air décroissante avec l'altitude : l'excès précipite au vent
            cap = np.exp(-h[y, x] / 3400.0)
            ex = 0.0
            if q > cap:
                ex = (q - cap) * 0.85
                q -= ex
            P[y, x] = pb + po + ex
    return P


class Climat:
    def __init__(self, rel, p, facteur=6, log=print):
        g = rel.g
        self.g, self.log = g, log
        f = facteur
        H, W = g.H // f, g.W // f
        sl = (slice(0, H * f), slice(0, W * f))
        def bloc(a, op=np.mean):
            return op(a[sl].reshape(H, f, W, f), axis=(1, 3))
        h = np.maximum(bloc(np.where(rel.eau, 0, rel.h).astype(np.float32)), 0)
        LON = bloc(rel.LON); LAT = bloc(rel.LAT)
        ocean = bloc(rel.ocean.astype(np.float32)) > 0.5
        mer = bloc(rel.mer.astype(np.float32)) > 0.5
        lacs = bloc((rel.lac > 0).astype(np.float32)) > 0.5
        decoupe = bloc(rel.decoupe.astype(np.float32)) > 0.5
        terre = bloc(rel.terre.astype(np.float32)) >= 0.5
        sources = {
            "atl_s": ocean & (LON < 14) & (LAT < 15),
            "atl_n": ocean & (LON < -5) & (LAT >= 15),
            "med": ocean & (LAT > 30) & (LON > -6) & (LON < 37),
            "rouge": ocean & (((LON > 32) & (LON < 44) & (LAT > 12) & (LAT <= 30)) | ((LON >= 42) & (LON < 51) & (LAT > 10.6) & (LAT <= 15))),
            "est": ocean & (LON >= 42) & ((LAT <= 10.6) | (LON >= 51)),
            "halakhel": mer,
            "lacs": lacs & (LAT < 15),
            "lacs_nord": lacs & (LAT >= 15),
            "decoupe": decoupe & (LAT < 6) & (LON < 36),
            # zones humides saisonnières au pied O de qoyra (§V.6) : plaines du Soudan du Sud
            "marais_sud": terre & (LON > 21) & (LON < 30) & (LAT > 5) & (LAT < 9.5) & (h < 700),
        }
        force = {"atl_s": 1.0, "atl_n": 0.55, "med": 0.7, "rouge": 0.12, "est": 0.6,
                 "halakhel": 0.3, "lacs": 0.3, "lacs_nord": 0.5, "decoupe": 0.95, "marais_sud": 0.6}
        dx_m = g.km_px_eq * f * 1000 * np.cos(np.radians(20))
        self.regimes = {}
        for nom, ang, srcs, recyc in REGIMES:
            S = np.zeros((H, W), np.float32)
            for k in srcs:
                S = np.maximum(S, sources[k] * force[k])
            # rotation pour que le vent souffle selon +x
            hr = rotate(h, -ang, reshape=True, order=1, cval=0)
            Sr = rotate(S, -ang, reshape=True, order=0, cval=0)
            Tr = rotate(terre.astype(np.float32), -ang, reshape=True, order=0, cval=0) > 0.5
            Pr = _marche(hr.astype(np.float64), Sr.astype(np.float64), Tr, dx_m, 0.028, 0.006, recyc, 0.05)
            Pb = rotate(Pr, ang, reshape=True, order=1, cval=0)
            # recadrage au centre
            oy = (Pb.shape[0] - H) // 2; ox = (Pb.shape[1] - W) // 2
            # diffusion latérale : l'humidité ne voyage pas en couloirs rectilignes
            self.regimes[nom] = gaussian_filter(np.clip(Pb[oy:oy + H, ox:ox + W], 0, None), 5.0)
        self.H, self.W, self.f = H, W, f
        self.LON, self.LAT, self.terre_c = LON, LAT, terre
        self._calibrer(p["calibration_pluies"])

    def _calibrer(self, points):
        g, f = self.g, self.f
        noms = list(self.regimes)
        A, b = [], []
        for pt in points:
            x, y = g.px(*pt["pos"])
            xc, yc = x / f - 0.5, y / f - 0.5
            ligne = [float(map_coordinates(gaussian_filter(self.regimes[n], 1.5), [[yc], [xc]], order=1)[0]) for n in noms]
            poids = 1.0 / np.sqrt(pt["mm"])
            A.append([v * poids for v in ligne])
            b.append(pt["mm"] * poids)
        c, res = nnls(np.array(A), np.array(b))
        self.coef = dict(zip(noms, c))
        P = sum(c_ * self.regimes[n] for n, c_ in zip(noms, c))
        P = gaussian_filter(P, 1.5) + 15
        # correction locale : les écarts résiduels aux points canoniques sont interpolés
        # (noyau gaussien ~500 km) et appliqués en facteur multiplicatif borné
        num = np.zeros_like(P); den = np.full_like(P, 1e-6)
        sig = 220 / (g.km_px_eq * f)
        yy, xx = np.mgrid[0:P.shape[0], 0:P.shape[1]]
        for pt in points:
            x, y = g.px(*pt["pos"])
            xc, yc = x / f - 0.5, y / f - 0.5
            v = float(map_coordinates(P, [[yc], [xc]], order=1)[0])
            r = np.log(pt["mm"] / max(v, 1.0))
            w = np.exp(-((xx - xc) ** 2 + (yy - yc) ** 2) / (2 * sig ** 2))
            num += w * r; den += w
        corr = np.exp(np.clip(num / (den + 0.02), np.log(0.3), np.log(6.0)))
        P = P * corr
        self.P_c = P
        self.log("  calibration des pluies :")
        self.calibration = []
        for pt in points:
            x, y = g.px(*pt["pos"])
            v = float(map_coordinates(P, [[y / f - 0.5], [x / f - 0.5]], order=1)[0])
            self.calibration.append(dict(lieu=pt["lieu"], pos=pt["pos"], cible_mm=pt["mm"], modele_mm=round(v)))
            self.log(f"    {pt['lieu']:<42} cible {pt['mm']:>5} mm  →  modèle {v:6.0f} mm")

    def pluie(self):
        """Pluie annuelle (mm) sur la grille complète."""
        g, f = self.g, self.f
        P = zoom(self.P_c, (g.H / self.H, g.W / self.W), order=1)
        return np.clip(P[:g.H, :g.W], 0, None).astype(np.float32)


def temperature(rel):
    """Température annuelle moyenne approximative (°C)."""
    h = np.maximum(np.where(rel.eau, 0, rel.h), 0)
    return (27.5 - 0.45 * np.clip(np.abs(rel.LAT) - 12, 0, None) - 6.0 * h / 1000).astype(np.float32)


# ------------------------------------------------------------------------- hiver |'Arin
# Faciès de la « matrice des hivers » (Géosystème §III)
FACIES = {
    0: ("hors_arin", "Hiver doux (hors |'Arin)", "#00000000"),
    1: ("hiver_blanc", "Hiver Blanc — manteau neigeux stable", "#f4f8ff"),
    2: ("hiver_gris", "Hiver Gris — pluies froides, gel humide, sols saturés", "#8a8f99"),
    3: ("hiver_jaune", "Hiver Jaune — gel nocturne, vents de poussière", "#d9b44a"),
    4: ("hiver_vapeur", "Hiver de Vapeur — brouillards de la mer Halakhel", "#4f86b5"),
    5: ("hiver_pluvieux_cotier", "Hiver pluvieux tempéré (hors matrice canonique)", "#7aa36a"),
}


def amplitude_annuelle(lat, cfg):
    """Écart été-hiver (°C) : faible sous les tropiques, croissant vers le nord."""
    return np.clip(cfg.get("amplitude_base", 4.0) + cfg.get("amplitude_par_degre", 0.45) * (np.abs(lat) - 8), 2.0, None)


def temperature_hiver(T_ann, lat, cfg):
    """Moyenne du cœur de l'hiver (|'Arin-sukhì) : annuelle − demi-amplitude − refroidissement |'Arin."""
    return T_ann - amplitude_annuelle(lat, cfg) / 2 - cfg.get("refroidissement_arin", 3.0)


def seuils_facies(cfg):
    """Seuils de température d'hiver calés pour que la matrice canonique (800 / 2 400 m) soit exacte
    à la latitude de référence (halekh, versant N)."""
    lat = cfg.get("latitude_reference", 22.5)
    T = lambda h: 27.5 - 0.45 * max(lat - 12, 0) - 6.0 * h / 1000
    blanc = float(temperature_hiver(T(cfg.get("altitude_blanc_m", 2400)), lat, cfg))
    gris = float(temperature_hiver(T(cfg.get("altitude_gris_m", 800)), lat, cfg))
    return blanc, gris


def hiver(rel, T_ann, P, p, log=print):
    """Température d'hiver, minimum nocturne et faciès |'Arin, cellule par cellule."""
    from scipy.ndimage import distance_transform_edt
    from .grille import distance_polyligne
    g = rel.g
    cfg = p.get("climat_hiver", {})
    Tw = temperature_hiver(T_ann, rel.LAT, cfg).astype(np.float32)
    aride = np.clip((400 - P) / 300, 0, 1)
    Tn = (Tw - cfg.get("amplitude_jour_humide", 8.0)
          - (cfg.get("amplitude_jour_aride", 12.0) - cfg.get("amplitude_jour_humide", 8.0)) * aride).astype(np.float32)
    s_blanc, s_gris = seuils_facies(cfg)
    # domaine de la cordillère ||Urumati : axes des chaînes + rayon d'influence (§III : 100-200 km)
    rayon = cfg.get("rayon_cordillere_km", 200)
    dom = np.zeros(g.shape, bool)
    for ax in rel.axes:
        if not ax["cfg"]["geo_id"].startswith(("GEO_ORO_URUMATI", "GEO_ORO_OKHETI")):
            continue
        d, _ = distance_polyligne(g, np.asarray(ax["ligne"]), rayon * 1.2)
        dom |= d < rayon
    terre = rel.terre
    F = np.zeros(g.shape, np.uint8)
    pluvieux = P >= cfg.get("pluie_min_gris_mm", 300)
    froid_humide = terre & (Tw <= s_gris) & pluvieux
    # régime méditerranéen (hors matrice) : façade nord, limite adoucie
    from .grille import bruit_bande
    nord = (rel.LAT + 0.8 * bruit_bande(g.shape, 917, 30 / g.km_px_eq, 500 / g.km_px_eq)) >= cfg.get("latitude_mediterraneenne", 29.5)
    F[terre & (Tn <= 0) & (P < 600)] = 3
    F[froid_humide & ~dom & nord] = 5
    # Hiver Gris : domaine de la cordillère, et partout ailleurs où l'hiver est aussi froid et pluvieux
    F[froid_humide & (dom | ~nord)] = 2
    F[terre & (Tw <= s_blanc)] = 1
    km = g.km_px[:, None]
    rive = distance_transform_edt(~rel.mer) * km < cfg.get("rive_vapeur_km", 25)
    F[rel.mer | (rive & terre)] = 4
    log(f"  hiver |'Arin : seuils Tw Blanc ≤ {s_blanc:.1f} °C, Gris ≤ {s_gris:.1f} °C (calés à {cfg.get('latitude_reference', 22.5)}° N)")
    return dict(Tw=Tw, Tn=Tn, facies=F, domaine=dom, seuil_blanc=s_blanc, seuil_gris=s_gris)
