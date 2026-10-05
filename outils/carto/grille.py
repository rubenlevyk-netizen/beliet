"""Grille de travail en Web Mercator et outils géométriques de base."""
import math
import numpy as np
from numba import njit, prange
from affine import Affine
from rasterio import features
from shapely.geometry import Polygon, LineString, MultiPolygon, mapping

R_TERRE = 6371.0088


def merc(lat):
    return np.log(np.tan(np.pi / 4 + np.radians(lat) / 2))


def imerc(m):
    return np.degrees(2 * np.arctan(np.exp(m)) - np.pi / 2)


class Grille:
    """Grille raster alignée sur la projection Web Mercator du contour fourni.

    Pixel (x, y) couvre [x, x+1) × [y, y+1) ; son centre est en (x+0.5, y+0.5).
    """

    def __init__(self, cadre, facteur=1):
        self.K = cadre["pixels_par_degre"] / facteur
        self.lon0, self.lon1 = cadre["lon_min"], cadre["lon_max"]
        self.lat0, self.lat1 = cadre["lat_min"], cadre["lat_max"]
        self.R = self.K * 180 / np.pi
        self.mtop = merc(self.lat1)
        self.W = int(round((self.lon1 - self.lon0) * self.K))
        self.H = int(round((self.mtop - merc(self.lat0)) * self.R))
        self.lons = self.lon0 + (np.arange(self.W) + 0.5) / self.K
        self.lats = imerc(self.mtop - (np.arange(self.H) + 0.5) / self.R)
        self.km_px_eq = 2 * np.pi * R_TERRE / 360 / self.K
        self.km_px = self.km_px_eq * np.cos(np.radians(self.lats))  # par ligne
        self.shape = (self.H, self.W)

    # --- conversions -------------------------------------------------------
    def px(self, lon, lat):
        x = (np.asarray(lon, float) - self.lon0) * self.K
        y = (self.mtop - merc(np.asarray(lat, float))) * self.R
        return x, y

    def ll(self, x, y):
        return self.lon0 + np.asarray(x, float) / self.K, imerc(self.mtop - np.asarray(y, float) / self.R)

    def km_px_a(self, lat):
        return self.km_px_eq * np.cos(np.radians(lat))

    def aire_km2(self):
        return np.repeat((self.km_px ** 2)[:, None], self.W, axis=1)

    # --- géométries --------------------------------------------------------
    def poly_px(self, coords):
        x, y = self.px([c[0] for c in coords], [c[1] for c in coords])
        return Polygon(list(zip(x, y)))

    def ligne_px(self, coords):
        x, y = self.px([c[0] for c in coords], [c[1] for c in coords])
        return LineString(list(zip(x, y)))

    def rasteriser(self, geoms, valeur=1, dtype=np.uint8, all_touched=False):
        if not isinstance(geoms, (list, tuple)):
            geoms = [geoms]
        geoms = [g for g in geoms if g is not None and not g.is_empty]
        if not geoms:
            return np.zeros(self.shape, dtype)
        return features.rasterize(((mapping(g), valeur) for g in geoms), out_shape=self.shape,
                                  transform=Affine.identity(), dtype=dtype, all_touched=all_touched)

    def distance_km(self, masque):
        """Distance (km, approx.) de chaque pixel au masque (0 dans le masque)."""
        from scipy.ndimage import distance_transform_edt
        d = distance_transform_edt(~masque.astype(bool))
        return d * self.km_px[:, None]


# --- distance à une polyligne (km), avec position le long de la ligne ------------

@njit(parallel=True, cache=True)
def _dist_polyligne(lons, lats, plon, plat, x0, x1, y0, y1, out_d, out_s):
    n = plon.shape[0]
    for y in prange(y0, y1):
        la = lats[y]
        c = math.cos(la * math.pi / 180.0) * 111.32
        for x in range(x0, x1):
            lo = lons[x]
            best = 1e30
            bs = 0.0
            for k in range(n - 1):
                ax = (plon[k] - lo) * c
                ay = (plat[k] - la) * 110.57
                bx = (plon[k + 1] - lo) * c
                by = (plat[k + 1] - la) * 110.57
                dx = bx - ax
                dy = by - ay
                L2 = dx * dx + dy * dy
                t = 0.0
                if L2 > 0:
                    t = -(ax * dx + ay * dy) / L2
                    if t < 0:
                        t = 0.0
                    elif t > 1:
                        t = 1.0
                qx = ax + t * dx
                qy = ay + t * dy
                d2 = qx * qx + qy * qy
                if d2 < best:
                    best = d2
                    bs = k + t
            out_d[y, x] = math.sqrt(best)
            out_s[y, x] = bs


def lisser_polyligne(pts, sous=8):
    """Spline de Catmull-Rom passant par les sommets ; renvoie (N, k) avec attributs interpolés."""
    P = np.asarray(pts, float)
    if len(P) < 3:
        t = np.linspace(0, 1, sous * (len(P) - 1) + 1)[:, None]
        return P[0] + t * (P[-1] - P[0])
    Q = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        for t in np.linspace(0, 1, sous, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
                              (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-1])
    return np.array(out)


def distance_polyligne(g, pts_ll, marge_km):
    """Distance (km) et abscisse (indice de segment + t) à une polyligne lon/lat, limitées à une boîte."""
    pts_ll = np.asarray(pts_ll, float)
    x, y = g.px(pts_ll[:, 0], pts_ll[:, 1])
    marge_px = marge_km / g.km_px_eq / np.cos(np.radians(min(80, np.abs(pts_ll[:, 1]).max())))
    x0 = int(max(0, x.min() - marge_px)); x1 = int(min(g.W, x.max() + marge_px + 1))
    y0 = int(max(0, y.min() - marge_px)); y1 = int(min(g.H, y.max() + marge_px + 1))
    d = np.full(g.shape, 1e9, np.float32)
    s = np.zeros(g.shape, np.float32)
    if x1 > x0 and y1 > y0:
        _dist_polyligne(g.lons, g.lats, pts_ll[:, 0].copy(), pts_ll[:, 1].copy(), x0, x1, y0, y1, d, s)
    return d, s


# --- bruit ---------------------------------------------------------------------

def bruit_bande(shape, graine, l_min_px, l_max_px, pente=2.0):
    """Bruit gaussien filtré dans une bande de longueurs d'onde (px), écart-type 1."""
    H, W = shape
    rng = np.random.default_rng(graine)
    w = rng.standard_normal(shape).astype(np.float32)
    F = np.fft.rfft2(w)
    ky = np.fft.fftfreq(H)[:, None]
    kx = np.fft.rfftfreq(W)[None, :]
    k = np.sqrt(kx * kx + ky * ky)
    k[0, 0] = 1e-9
    f = k ** (-pente / 2)
    f *= np.exp(-(k * l_min_px) ** 2)          # coupe les petites longueurs d'onde
    f *= 1 - np.exp(-(k * l_max_px) ** 2)      # coupe les grandes
    n = np.fft.irfft2(F * f, s=shape).astype(np.float32)
    n -= n.mean()
    n /= n.std() + 1e-9
    return n


def bruit_crete(shape, graine, l_min_px, l_max_px, octaves=5):
    """Bruit « de crête » (ridged multifractal simplifié), valeurs ~[0, 1]."""
    tot = np.zeros(shape, np.float32)
    poids = 0.0
    lmax = l_max_px
    for o in range(octaves):
        lmin = max(l_min_px, lmax / 2.2)
        b = bruit_bande(shape, graine + 101 * o, lmin, lmax, pente=0.5)
        r = (1 - np.abs(np.tanh(b * 0.9))) ** 2
        a = 0.55 ** o
        tot += a * r
        poids += a
        lmax /= 2.0
        if lmax < l_min_px:
            break
    return tot / poids


def smax(a, b, k):
    """Maximum lissé."""
    return 0.5 * (a + b + np.sqrt((a - b) ** 2 + k * k))


def smin(a, b, k):
    return 0.5 * (a + b - np.sqrt((a - b) ** 2 + k * k))
