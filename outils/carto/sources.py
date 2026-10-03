"""Chargement des sources : relief réel, contour fourni, registre, fleuves réels."""
import json
import os
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

from .grille import merc, imerc

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CACHE = os.path.join(RACINE, "outils", "cache")
URL_TUILE = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
URL_FLEUVES = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
               "geojson/ne_10m_rivers_lake_centerlines.geojson")


def _telecharger(url, chemin):
    if os.path.exists(chemin) and os.path.getsize(chemin) > 0:
        return
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    tmp = chemin + ".tmp"
    urllib.request.urlretrieve(url, tmp)
    os.replace(tmp, chemin)


def relief_reel(g, z=6):
    """Altitude réelle (m) rééchantillonnée sur la grille, depuis les tuiles « Terrarium » AWS."""
    n = 2 ** z
    tx0 = int(np.floor((g.lon0 + 180) / 360 * n)); tx1 = int(np.floor((g.lon1 + 180) / 360 * n))
    ty0 = int(np.floor((1 - merc(g.lat1) / np.pi) / 2 * n)); ty1 = int(np.floor((1 - merc(g.lat0) / np.pi) / 2 * n))
    taches = []
    for x in range(tx0, tx1 + 1):
        for y in range(ty0, ty1 + 1):
            taches.append((URL_TUILE.format(z=z, x=x, y=y), os.path.join(CACHE, "tuiles", f"{z}_{x}_{y}.png")))
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda t: _telecharger(*t), taches))
    M = np.zeros(((ty1 - ty0 + 1) * 256, (tx1 - tx0 + 1) * 256), np.float32)
    for x in range(tx0, tx1 + 1):
        for y in range(ty0, ty1 + 1):
            a = np.asarray(Image.open(os.path.join(CACHE, "tuiles", f"{z}_{x}_{y}.png")).convert("RGB")).astype(np.float32)
            M[(y - ty0) * 256:(y - ty0 + 1) * 256, (x - tx0) * 256:(x - tx0 + 1) * 256] = \
                a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
    Z = 256 * n
    X = (g.lons + 180) / 360 * Z - tx0 * 256
    Y = (1 - merc(g.lats) / np.pi) / 2 * Z - ty0 * 256
    XX, YY = np.meshgrid(X, Y)
    return map_coordinates(M, [YY - 0.5, XX - 0.5], order=1, mode="nearest").astype(np.float32)


def contour_beliet(p):
    """Polygone du contour fourni (lon/lat), à partir du SVG d'origine."""
    from svgpathtools import parse_path
    c = p["contour"]
    s = open(os.path.join(RACINE, c["fichier"]), encoding="utf-8").read()
    d = re.search(r' d="([^"]*)"', s).group(1)
    chemin = parse_path(d)
    pts = []
    for seg in chemin:
        for t in (0.0, 0.5):
            z = seg.point(t)
            pts.append((z.real, z.imag))
    pts = np.array(pts)
    K = c["largeur_svg"] / (c["lon_droite"] - c["lon_gauche"])
    R = K * 180 / np.pi
    lon = c["lon_gauche"] + pts[:, 0] / K
    lat = imerc(merc(c["lat_haut"]) - pts[:, 1] / R)
    return np.c_[lon, lat]


def registre():
    d = json.load(open(os.path.join(RACINE, "references", "GEOSYSTEME_REGISTRE.v1.json"), encoding="utf-8"))
    return {e["geo_id"]: e for e in d["entrees"]}


def nom_registre(reg, geo_id, rang=0):
    e = reg.get(geo_id)
    if not e:
        return None
    formes = [n["forme"] for n in e["noms"] if n["forme"] and not n["forme"].startswith("[")]
    if len(formes) > rang:
        return formes[rang]
    return None


def fleuves_reels():
    chemin = os.path.join(CACHE, "ne_10m_rivers_lake_centerlines.geojson")
    _telecharger(URL_FLEUVES, chemin)
    d = json.load(open(chemin, encoding="utf-8"))
    out = {}
    for f in d["features"]:
        nom = f["properties"].get("name")
        if not nom:
            continue
        geom = f["geometry"]
        lignes = [geom["coordinates"]] if geom["type"] == "LineString" else geom["coordinates"]
        out.setdefault(nom, []).extend(lignes)
    return out
