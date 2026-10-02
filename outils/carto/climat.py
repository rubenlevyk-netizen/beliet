"""Climat simplifié : advection d'humidité par régimes de vents, pluie orographique, calibration."""
import numpy as np
from numba import njit
from scipy.ndimage import rotate, zoom, gaussian_filter, map_coordinates
from scipy.optimize import nnls

# régimes : (nom, direction vers laquelle souffle le vent en degrés [0 = est, 90 = nord], sources, recyclage)
REGIMES = [
    ("mousson_sud_ouest", 50, ("atl_s", "decoupe", "lacs"), 0.62),
    ("mousson_sud", 95, ("decoupe", "atl_s", "lacs"), 0.62),
    ("mousson_ouest", 15, ("decoupe", "atl_s", "lacs"), 0.82),
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
        }
        force = {"atl_s": 1.0, "atl_n": 0.55, "med": 0.7, "rouge": 0.12, "est": 0.6,
                 "halakhel": 0.3, "lacs": 0.55, "lacs_nord": 0.75, "decoupe": 0.95}
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
            self.regimes[nom] = np.clip(Pb[oy:oy + H, ox:ox + W], 0, None)
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
        corr = np.exp(np.clip(num / (den + 0.04), np.log(0.35), np.log(4.0)))
        P = P * corr
        self.P_c = P
        self.log("  calibration des pluies :")
        for pt in points:
            x, y = g.px(*pt["pos"])
            v = float(map_coordinates(P, [[y / f - 0.5], [x / f - 0.5]], order=1)[0])
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
