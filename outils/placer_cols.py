#!/usr/bin/env python3
"""Place les 48 cols de la cordillère ||Urumati sur le relief calculé.

Méthode :
1. Chaque groupe du Géosystème (§I, « Inventaire opérationnel des cols ») correspond à une interface
   entre deux peuples ; on lui associe le tronçon de chaîne qui sépare leurs territoires.
2. Sur ce tronçon, on mesure le profil de la ligne de crête (point le plus haut de chaque transect).
3. Les ensellements (minima locaux du profil) sont les passages naturels. Chaque col reçoit, du plus
   haut au plus bas, l'ensellement libre dont l'altitude est la plus proche de son altitude canonique
   (sans descendre en dessous), en respectant un espacement minimal.
4. Les cols « désert → hauts plateaux » (Šamqiriyyūn ↔ Qoyra-ña-ra) n'ont pas de crête à franchir :
   ils sont placés au rebord de l'escarpement occidental de qoyra, là où il atteint leur altitude.
5. Le générateur entaille ensuite le relief pour que chaque col ait exactement son altitude canonique.

Usage : python3 outils/placer_cols.py   (relief en cache requis : lancer d'abord generer_carte.py)
Sortie : donnees/cols.yaml
"""
import json
import os
import pickle
import sys

import numpy as np
import yaml
from pyproj import Geod
from scipy.ndimage import map_coordinates

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from carto.sources import RACINE, CACHE           # noqa: E402
from generer_carte import empreinte               # noqa: E402

GEOD = Geod(ellps="WGS84")

# groupe → (chaînes et bornes du tronçon, espacement minimal km, interface)
GROUPES = [
    ("Šamqiriyyūn ↔ Tɨrakh", range(1, 10), [("||Urumati-k'ara", lambda lo, la: 15.0 <= lo <= 24.4),
                                             (None, lambda lo, la: lo < 29.0)], 90,
     "k'ara du Tibesti au Marra, puis monts Nouba : plaines NE (Abnuḥīl, interfluve) ↔ hautes terres centrales"),
    ("Qoyra-ña-ra ↔ Tɨrakh", range(10, 18), [(None, lambda lo, la: lo >= 29.0)], 70,
     "prolongement SE de k'ara jusqu'à la jonction avec qoyra (cirque de !Ayk-ma-‖Ixa)"),
    ("Ba-mbaro ↔ Halaktim", range(18, 24), [("||Urumati-halekh", lambda lo, la: lo <= -10.8)], 55,
     "extrémité ouest de halekh : versant atlantique humide ↔ cordons dunaires du NO"),
    ("Ba-mbaro ↔ Tɨrakh", range(24, 30), [("||Urumati-lóngò", lambda lo, la: la <= 20.2)], 140,
     "lóngò : forêts du SO (bassin Mopámà) ↔ hautes terres"),
    ("Halaktim ↔ Tɨrakh", range(30, 44), [("||Urumati-halekh", lambda lo, la: lo > -10.8),
                                          ("!Okheti", lambda lo, la: True),
                                          ("||Urumati-k'ara", lambda lo, la: lo <= 8.5)], 75,
     "halekh central et oriental, !Okheti, k'ara occidental : piémonts NO et rive S de l'Halakhel ↔ Centre"),
    ("Šamqiriyyūn ↔ Qoyra-ña-ra", range(44, 49), "escarpement", 95,
     "rebord occidental et septentrional de qoyra : déserts du NE ↔ hauts plateaux"),
]
PROCHE = {14: ((36.9, 9.1), 110),       # T'iqur-ɨlkh « bordé par le cirque de !Ayk-ma-‖Ixa »
          24: ((7.6, 11.6), 260)}       # Ku-Pámà-Tɨra-te : nom du Mopámà, au-dessus du lac
TERRITOIRE_KM = 420                     # cols d'un même territoire (registre, relation « territoire ») groupés


def km_entre(a, b):
    return GEOD.inv(a[0], a[1], b[0], b[1])[2] / 1000


def profil(rel, ligne, demi_larg, pas_km=6):
    """Ligne de crête : pour chaque transect perpendiculaire à l'axe, le point le plus haut."""
    g = rel.g
    x, y = g.px(ligne[:, 0], ligne[:, 1])
    P = np.c_[x, y]
    kmpx = g.km_px_eq * np.cos(np.radians(ligne[:, 1]))
    seg = np.hypot(*np.diff(P, axis=0).T) * 0.5 * (kmpx[1:] + kmpx[:-1])
    S = np.r_[0, np.cumsum(seg)]
    s = np.arange(0, S[-1], pas_km)
    X = np.interp(s, S, P[:, 0]); Y = np.interp(s, S, P[:, 1])
    dx = np.gradient(X); dy = np.gradient(Y); n = np.hypot(dx, dy) + 1e-9
    nx, ny = -dy / n, dx / n
    out = []
    for i in range(len(s)):
        lat = g.ll(X[i], Y[i])[1]
        k = g.km_px_eq * np.cos(np.radians(lat))
        off = np.arange(-demi_larg, demi_larg + 1e-6, 2.0) / k
        tx, ty = X[i] + nx[i] * off, Y[i] + ny[i] * off
        z = map_coordinates(rel.h, [ty, tx], order=1)
        terre = map_coordinates(rel.terre.astype(np.float32), [ty, tx], order=0) > 0.5
        z = np.where(terre, z, -1e9)
        j = int(np.argmax(z))
        lo, la = g.ll(tx[j], ty[j])
        out.append((float(lo), float(la), float(z[j]), float(s[i]), float(np.degrees(np.arctan2(dy[i], dx[i])))))
    return np.array(out)


def minima(prof, k=3, prom=80):
    z = prof[:, 2]
    m = np.zeros(len(z), bool)
    for i in range(k, len(z) - k):
        if z[i] <= z[i - k:i + k + 1].min() + 1e-6:
            gauche = z[max(0, i - 12):i].max()
            droite = z[i + 1:i + 13].max()
            m[i] = min(gauche, droite) - z[i] >= prom
    return m


def main():
    p = yaml.safe_load(open(os.path.join(RACINE, "donnees", "parametres_carte.yaml"), encoding="utf-8"))
    # relief de référence, sans entaille : celui du cache sans cols, sinon la copie gardée avant entaille
    p["cols"] = []
    f = os.path.join(CACHE, f"relief_{empreinte(p)}.pkl")
    if not os.path.exists(f):
        from generer_carte import charger_cols
        p["cols"] = charger_cols()
        f = os.path.join(CACHE, f"relief_{empreinte(p)}.pkl")
    rel = pickle.load(open(f, "rb"))
    if getattr(rel, "h_sans_cols", None) is not None:
        rel.h = rel.h_sans_cols
    reg = json.load(open(os.path.join(RACINE, "references", "GEOSYSTEME_REGISTRE.v1.json"), encoding="utf-8"))
    cols = {e["geo_id"]: e for e in reg["entrees"] if e.get("type") == "COL"}
    axes = {}
    for ax in rel.axes:
        cle = ax["cfg"].get("nom") if ax["cfg"].get("nom") else (None if ax["cfg"]["geo_id"] == "GEO_ORO_URUMATI_KARA" else "autre")
        if cle in axes:
            continue
        hw = float(np.max(np.array(ax["cfg"]["points"])[:, 3]))
        axes[cle] = (ax["ligne"], hw)
    sortie = []
    for nom_g, numeros, troncons, espacement, interface in GROUPES:
        ids = [f"GEO_COL_{n:03d}" for n in numeros]
        if troncons == "escarpement":
            sortie += escarpement(rel, ids, cols, espacement, nom_g, interface)
            continue
        cand = []
        for nom_ch, garde in troncons:
            ligne, hw = axes[nom_ch]
            pr = profil(rel, np.asarray(ligne), hw * 0.9)
            mi = minima(pr)
            for (lo, la, z, s, az), est_min in zip(pr, mi):
                if garde(lo, la) and 20 < s < pr[-1, 3] - 20:
                    cand.append(dict(pos=(lo, la), z=z, az=az, minimum=bool(est_min), chaine=nom_ch or "||Urumati-k'ara (prolongement SE)"))
        pris = []
        terr = {i: {r["acteur_id"] for r in cols[i].get("renvois", []) if r.get("relation") == "territoire"} for i in ids}
        for gid in sorted(ids, key=lambda i: (int(i[-3:]) not in PROCHE, cols[i]["attributs"]["altitude_m"])):
            alt = cols[gid]["attributs"]["altitude_m"]
            n = int(gid[-3:])
            best, bc = None, 1e18
            for c in cand:
                if any(km_entre(c["pos"], q["pos"]) < espacement for q in pris):
                    continue
                if n in PROCHE and km_entre(c["pos"], PROCHE[n][0]) > PROCHE[n][1]:
                    continue
                voisins = [q for q in pris if terr[q["geo_id"]] & terr[gid]]
                if voisins and min(km_entre(c["pos"], q["pos"]) for q in voisins) > TERRITOIRE_KM:
                    continue
                d = c["z"] - alt
                cout = d if d >= 0 else 4 * (-d) + 600
                if c["minimum"]:
                    cout -= 250
                if cout < bc:
                    best, bc = c, cout
            if best is None:
                raise SystemExit(f"aucun emplacement pour {gid}")
            pris.append(dict(best, geo_id=gid))
        for c in pris:
            e = cols[c["geo_id"]]
            a = e["attributs"]
            sortie.append({
                "geo_id": c["geo_id"], "nom": e["noms"][0]["forme"], "groupe": nom_g, "interface": interface,
                "chaine": c["chaine"], "pos": [round(float(c["pos"][0]), 3), round(float(c["pos"][1]), 3)],
                "altitude_m": a["altitude_m"], "altitude_crete_avant_entaille_m": int(round(c["z"])),
                "ensellement_naturel": c["minimum"], "entaille": True, "azimut_crete_px_deg": round(float(c["az"]), 1),
                "statut_passage": a.get("statut_passage"), "cycle_hivernal": a.get("cycle_hivernal"),
                "ouverture_mois": [a.get("ouverture", {}).get("mois_debut"), a.get("ouverture", {}).get("mois_fin")],
                "routes": [r["route_id"] for r in e.get("renvois", []) if r.get("route_id")],
                "statut": "[PROPOSITION] position calculée ; altitude [CANON]",
            })
    sortie.sort(key=lambda c: c["geo_id"])
    entete = ("# Cols de la cordillère ||Urumati — positions calculées par outils/placer_cols.py\n"
              "# Altitudes et attributs : [CANON] (registre). Positions : [PROPOSITION].\n"
              "# Le générateur entaille le relief pour que chaque col ait son altitude canonique.\n")
    with open(os.path.join(RACINE, "donnees", "cols.yaml"), "w", encoding="utf-8") as f:
        f.write(entete)
        yaml.safe_dump({"cols": sortie}, f, allow_unicode=True, sort_keys=False, width=140)
    for c in sortie:
        print(f"{c['geo_id']} {c['nom']:<24} {c['altitude_m']:>5} m  crête {c['altitude_crete_avant_entaille_m']:>5} m  "
              f"{'ensellement' if c['ensellement_naturel'] else '           '}  {c['pos']}  {c['chaine']}")


def escarpement(rel, ids, cols, espacement, nom_g, interface):
    """Rebord de qoyra : en venant de l'ouest, premier point où le relief atteint l'altitude du col."""
    g = rel.g
    cand = []
    for la in np.arange(11.6, 15.3, 0.05):
        x1, y = g.px(39.6, la)
        x0, _ = g.px(34.5, la)
        xs = np.arange(int(x0), int(x1))
        z = rel.h[int(y), xs]
        cand.append((la, xs, z))
    pris = []
    for gid in sorted(ids, key=lambda i: (int(i[-3:]) not in PROCHE, cols[i]["attributs"]["altitude_m"])):
        alt = cols[gid]["attributs"]["altitude_m"]
        best, bl = None, -1e9
        for la, xs, z in cand:
            ok = np.nonzero(z >= alt)[0]
            if not len(ok):
                continue
            x = xs[ok[0]]
            lo = float(g.ll(x + 0.5, 0)[0])
            pos = (lo, float(la))
            if any(km_entre(pos, q["pos"]) < espacement for q in pris):
                continue
            # rentrant de l'escarpement (vallée qui pénètre le plateau) : rebord le plus à l'est
            if lo > bl:
                best, bl = dict(pos=pos, z=float(z[ok[0]])), lo
        pris.append(dict(best, geo_id=gid))
    out = []
    for c in pris:
        e = cols[c["geo_id"]]
        a = e["attributs"]
        out.append({
            "geo_id": c["geo_id"], "nom": e["noms"][0]["forme"], "groupe": nom_g, "interface": interface,
            "chaine": "||Urumati-qoyra (escarpement)", "pos": [round(float(c["pos"][0]), 3), round(float(c["pos"][1]), 3)],
            "altitude_m": a["altitude_m"], "altitude_crete_avant_entaille_m": int(round(c["z"])),
            "ensellement_naturel": False, "entaille": False,
            "statut_passage": a.get("statut_passage"), "cycle_hivernal": a.get("cycle_hivernal"),
            "ouverture_mois": [a.get("ouverture", {}).get("mois_debut"), a.get("ouverture", {}).get("mois_fin")],
            "routes": [r["route_id"] for r in e.get("renvois", []) if r.get("route_id")],
            "statut": "[PROPOSITION] position calculée ; altitude [CANON]",
        })
    return out


if __name__ == "__main__":
    main()
