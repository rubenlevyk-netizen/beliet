"""Hydrologie : remplissage des dépressions, écoulement, accumulation, érosion, réseau fluvial."""
import math
import numpy as np
from numba import njit

DX8 = np.array([-1, 0, 1, -1, 1, -1, 0, 1], np.int64)
DY8 = np.array([-1, -1, -1, 0, 0, 1, 1, 1], np.int64)


@njit(cache=True)
def _heap_push(hv, hi, size, v, i):
    k = size
    hv[k] = v
    hi[k] = i
    while k > 0:
        p = (k - 1) >> 1
        if hv[p] <= hv[k]:
            break
        hv[p], hv[k] = hv[k], hv[p]
        hi[p], hi[k] = hi[k], hi[p]
        k = p
    return size + 1


@njit(cache=True)
def _heap_pop(hv, hi, size):
    v = hv[0]
    i = hi[0]
    size -= 1
    hv[0] = hv[size]
    hi[0] = hi[size]
    k = 0
    while True:
        l = 2 * k + 1
        if l >= size:
            break
        r = l + 1
        m = l
        if r < size and hv[r] < hv[l]:
            m = r
        if hv[k] <= hv[m]:
            break
        hv[m], hv[k] = hv[k], hv[m]
        hi[m], hi[k] = hi[k], hi[m]
        k = m
    return v, i, size


@njit(cache=True)
def remplir(h, actif, eps):
    return _remplir(h, actif, np.full(h.shape, eps))


@njit(cache=True)
def _remplir(h, actif, eps):
    """Priority-flood + epsilon. `actif` = cellules à drainer ; les autres sont des exutoires.

    Renvoie l'altitude remplie et l'ordre de traitement (de l'aval vers l'amont).
    """
    H, W = h.shape
    N = H * W
    f = h.astype(np.float64).copy()
    ferme = np.zeros(N, np.bool_)
    hv = np.empty(N, np.float64)
    hi = np.empty(N, np.int64)
    size = 0
    ordre = np.empty(N, np.int64)
    no = 0
    ff = f.ravel()
    act = actif.ravel()
    ep = eps.ravel()
    for i in range(N):
        if not act[i]:
            ferme[i] = True
    # exutoires au contact d'une cellule active
    for i in range(N):
        if act[i]:
            continue
        y = i // W
        x = i - y * W
        bord = False
        for k in range(8):
            xx = x + DX8[k]
            yy = y + DY8[k]
            if 0 <= xx < W and 0 <= yy < H:
                if act[yy * W + xx]:
                    bord = True
                    break
        if bord:
            size = _heap_push(hv, hi, size, ff[i], i)
    # bords de la grille actifs = exutoires
    for i in range(N):
        if act[i]:
            y = i // W
            x = i - y * W
            if x == 0 or y == 0 or x == W - 1 or y == H - 1:
                ferme[i] = True
                size = _heap_push(hv, hi, size, ff[i], i)
    while size > 0:
        v, i, size = _heap_pop(hv, hi, size)
        if act[i]:
            ordre[no] = i
            no += 1
        y = i // W
        x = i - y * W
        for k in range(8):
            xx = x + DX8[k]
            yy = y + DY8[k]
            if 0 <= xx < W and 0 <= yy < H:
                j = yy * W + xx
                if not ferme[j]:
                    ferme[j] = True
                    if ff[j] <= v + ep[j]:
                        ff[j] = v + ep[j]
                    size = _heap_push(hv, hi, size, ff[j], j)
    return f, ordre[:no]


@njit(cache=True)
def recepteurs(f, ordre, km_ligne):
    """Récepteur D8 de plus forte pente sur l'altitude remplie ; -1 = exutoire."""
    H, W = f.shape
    ff = f.ravel()
    rec = np.full(H * W, -1, np.int64)
    dist = np.ones(H * W, np.float64)
    for n in range(ordre.shape[0]):
        i = ordre[n]
        y = i // W
        x = i - y * W
        best = 0.0
        bj = -1
        bd = 1.0
        dkm = km_ligne[y]
        for k in range(8):
            xx = x + DX8[k]
            yy = y + DY8[k]
            if 0 <= xx < W and 0 <= yy < H:
                j = yy * W + xx
                d = dkm * (1.41421356 if (DX8[k] != 0 and DY8[k] != 0) else 1.0)
                s = (ff[i] - ff[j]) / d
                if s > best:
                    best = s
                    bj = j
                    bd = d
        rec[i] = bj
        dist[i] = bd
    return rec, dist


@njit(cache=True)
def accumuler(poids, ordre, rec):
    a = poids.ravel().astype(np.float64).copy()
    for n in range(ordre.shape[0] - 1, -1, -1):
        i = ordre[n]
        r = rec[i]
        if r >= 0:
            a[r] += a[i]
    return a


@njit(cache=True)
def eroder(h, ordre, rec, dist, A, K, m, dt):
    """Puissance fluviale implicite (Braun & Willett 2013), n = 1."""
    hh = h.ravel()
    for n in range(ordre.shape[0]):
        i = ordre[n]
        r = rec[i]
        if r < 0:
            continue
        F = K[i] * dt * A[i] ** m / dist[i]
        nv = (hh[i] + F * hh[r]) / (1.0 + F)
        if nv < hh[i]:
            hh[i] = nv


def erosion(rel, iterations=10, K0=0.25, m=0.5, dt=1.0, log=print):
    """Creuse des vallées dendritiques, surtout dans les reliefs ajoutés."""
    from scipy.ndimage import gaussian_filter, maximum_filter, minimum_filter
    g = rel.g
    actif = rel.terre
    h_avant = rel.h.copy()
    Kc = (0.08 + 0.92 * np.clip(rel.crete * 1.6, 0, 1)) * K0
    Kc = np.where(actif, Kc, 0).ravel().astype(np.float64)
    aire = rel.g.aire_km2().ravel()
    km = g.km_px.astype(np.float64)
    for it in range(iterations):
        f, ordre = remplir(rel.h, actif, 1e-3)
        rec, dist = recepteurs(f, ordre, km)
        A = accumuler(aire, ordre, rec)
        h2 = f.copy()
        eroder(h2, ordre, rec, dist, A, Kc, m, dt)
        baisse = (f - h2).astype(np.float32)
        rel.h = np.where(actif, rel.h - baisse, rel.h).astype(np.float32)
        log(f"  érosion {it + 1}/{iterations} : incision max {baisse.max():.0f} m")
    # restauration des sommets : l'érosion creuse les vallées sans abaisser les crêtes
    r = max(3, int(round(14 / g.km_px_eq)))
    env_av = gaussian_filter(maximum_filter(h_avant, 2 * r + 1), r)
    env_ap = gaussian_filter(maximum_filter(rel.h, 2 * r + 1), r)
    pied = gaussian_filter(minimum_filter(h_avant, 8 * r + 1), 4 * r)
    s = np.clip((env_av - pied) / np.maximum(env_ap - pied, 1.0), 1.0, 1.8)
    w = np.clip(rel.crete * 2.0, 0, 1)
    restaure = pied + (rel.h - pied) * s
    rel.h = np.where(actif & (rel.h > pied), rel.h * (1 - w) + restaure * w, rel.h).astype(np.float32)
    # adoucissement des versants dans les reliefs ajoutés
    lisse = gaussian_filter(rel.h, 0.8)
    w = np.clip(rel.crete * 1.5, 0, 1) * 0.6
    rel.h = np.where(actif, rel.h * (1 - w) + lisse * w, rel.h).astype(np.float32)


class Hydro:
    """Écoulement final et réseau fluvial secondaire."""

    def __init__(self, rel, pluie_mm, log=print):
        g = rel.g
        self.g = g
        actif = rel.terre
        # sur les zones plates, l'ordre d'inondation suit un champ de bruit lisse : méandres naturels
        from .grille import bruit_bande
        nb = bruit_bande(g.shape, 4242, 6, 120 / g.km_px_eq)
        eps = (0.004 + 0.02 * (nb - nb.min()) / (nb.max() - nb.min()) ** 1.0).astype(np.float64)
        f, ordre = _remplir(rel.h, actif, eps)
        # grandes cuvettes fermées : exutoire terminal (bassins endoréiques réels, ex. Tchad)
        from scipy.ndimage import label as _label, minimum_position
        prof = np.where(actif, f - rel.h, 0)
        lab, n = _label(prof > 1.0)
        if n:
            aire_c = np.bincount(lab.ravel(), weights=g.aire_km2().ravel())
            pmax = np.zeros(n + 1)
            np.maximum.at(pmax, lab.ravel(), prof.ravel())
            grands = [k for k in range(1, n + 1) if aire_c[k] > 8000 and pmax[k] > 20]
            if grands:
                actif2 = actif.copy()
                for k in grands:
                    yx = minimum_position(rel.h, labels=lab, index=k)
                    actif2[int(yx[0]), int(yx[1])] = False
                f, ordre = _remplir(rel.h, actif2, eps)
                actif = actif2
                log(f"  {len(grands)} bassins endoréiques terminaux")
        self.rempli = f.astype(np.float32)
        self.profondeur_cuvette = np.where(actif, f - rel.h, 0).astype(np.float32)
        rec, dist = recepteurs(f, ordre, g.km_px.astype(np.float64))
        self.ordre, self.rec = ordre, rec
        aire = g.aire_km2()
        self.A = accumuler(aire, ordre, rec).reshape(g.shape).astype(np.float32)   # km²
        ruissel = np.clip((pluie_mm - 120) / 1400, 0, 0.55) * pluie_mm             # mm/an écoulés
        q = ruissel * aire * 1e3 / (365.25 * 86400)                                   # m³/s par cellule
        self.Q = accumuler(q.astype(np.float64), ordre, rec).reshape(g.shape).astype(np.float32)
        self.actif = actif
        log(f"  hydrologie : débit max {self.Q.max():,.0f} m³/s, bassin max {self.A.max():,.0f} km²")

    def reseau(self, seuil_Q=25.0, seuil_A_oued=6000.0, sec_Q=4.0):
        """Segments de cours d'eau (en pixels) : pérennes (Q ≥ seuil) et oueds (grand bassin, Q faible)."""
        g = self.g
        W = g.W
        Q = self.Q.ravel()
        A = self.A.ravel()
        act = self.actif.ravel()
        perenne = act & (Q >= seuil_Q)
        oued = act & ~perenne & (A >= seuil_A_oued) & (Q < sec_Q)
        rec = self.rec
        sortie = []
        for type_, masque in (("perenne", perenne), ("oued", oued)):
            idx = np.nonzero(masque)[0]
            if len(idx) == 0:
                continue
            nb_amont = np.zeros(len(Q), np.int32)
            r = rec[idx]
            ok = (r >= 0) & masque[np.clip(r, 0, None)]
            np.add.at(nb_amont, r[ok], 1)
            # têtes : cellules sans amont dans le masque ; confluences : ≥ 2 amonts
            departs = set(idx[nb_amont[idx] != 1].tolist())
            vu = np.zeros(len(Q), np.bool_)
            for d in departs:
                if vu[d] and nb_amont[d] == 1:
                    continue
                chemin = [d]
                i = d
                while True:
                    j = rec[i]
                    if j < 0:
                        break
                    chemin.append(j)
                    if not masque[j] or nb_amont[j] != 1:
                        break
                    if vu[j]:
                        break
                    vu[j] = True
                    i = j
                if len(chemin) >= 2:
                    ys = np.array(chemin) // W
                    xs = np.array(chemin) - ys * W
                    sortie.append(dict(type=type_, x=xs + 0.5, y=ys + 0.5, Q=float(Q[chemin[-2]]),
                                       A=float(A[chemin[-2]])))
        return sortie
