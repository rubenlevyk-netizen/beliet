#!/usr/bin/env python3
"""Place les lieux du corpus sur la carte, calcule leurs caractéristiques physiques et trace les routes.

Usage (après outils/generer_carte.py) :
    python3 outils/lieux_routes.py

Entrées : donnees/lieux.yaml (placement raisonné), references/LIEUX_URBAINS.v2.json,
          references/RESEAU_ROUTES.v3.json, donnees/cols.yaml, état de la carte (cache).
Sorties : carte/sig/beliet_lieux.geojson, carte/sig/beliet_routes.geojson,
          carte/sig/beliet_lieux_routes.json, carte/beliet_carte_lieux.{png,svg},
          LIEUX_ET_ROUTES.md (section entre les balises GENERE).
"""
import json
import os
import pickle
import re
import sys

import numpy as np
import yaml
from pyproj import Geod
from scipy.ndimage import binary_dilation, distance_transform_edt, label, maximum_filter, minimum_filter
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from carto.etat import charger_etat                       # noqa: E402
from carto.milieux import MILIEUX, CODE                   # noqa: E402
from carto.sources import RACINE, CACHE                   # noqa: E402
from mesures_corpus import echapper_tableaux              # noqa: E402

GEOD = Geod(ellps="WGS84")
SIG = os.path.join(RACINE, "carte", "sig")
REF = os.path.join(RACINE, "references")
FACIES = {0: "hors |'Arin", 1: "Hiver Blanc", 2: "Hiver Gris", 3: "Hiver Jaune", 4: "Hiver de Vapeur",
          5: "hiver pluvieux tempéré"}
NOM_MIL = {i: m[0] for i, m in enumerate(MILIEUX)}
MOIS = ["jan", "fév", "mar", "avr", "mai", "juin", "juil", "août", "sep", "oct", "nov", "déc"]

# vitesses (km par jour de marche ou de navigation)
V = {"cabotage": 75.0, "hauturier": 150.0, "lacustre": 60.0, "fluvial_aval": 80.0, "fluvial_amont": 28.0,
     "fluvial_plat": 50.0, "terrestre_caravane": 30.0, "terrestre_portage": 22.0, "col_haute_altitude": 20.0}
TRANSBORD_J = 0.5          # rupture de charge eau ↔ terre
PENALITE = 8.0             # milieu non déclaré par la route : temps × 8 (le tracé l'évite si possible)
FREIN_MILIEU = {"foret_tropicale_humide": 0.6, "zone_humide_lacustre": 0.5, "foret_maree": 0.35, "glacier": 0.1,
                "zone_periglaciaire": 0.5, "desert_sableux": 0.75, "dunes_littorales": 0.7,
                "depression_saline": 0.8, "foret_montagne": 0.8, "foret_berge": 0.8}
F = 3                      # facteur de la grille de routage (≈ 5 km)
PENTE_NAVIGABLE = 1.5e-3   # pente maximale d'un bief navigable (1,5 m/km) ; au-delà : rapides, portage


def r1(v, n=1):
    return round(float(v), n)


def km(a, b):
    return GEOD.inv(a[0], a[1], b[0], b[1])[2] / 1000


# =============================================================================================== corpus

def lire_corpus():
    L = json.load(open(os.path.join(REF, "LIEUX_URBAINS.v2.json"), encoding="utf-8"))
    idx = {}
    for cle, typ in (("lieux", "LUR"), ("zones_secondaires", "ZRS")):
        for fac, liste in L[cle].items():
            for l in liste:
                lid = l.get("lieu_id") or l.get("zrs_id") or l.get("zone_id")
                a = l.get("ancrage_spatial", {})
                c = a.get("coordonnees_geo", {})
                arch = l.get("architecture") or {}
                idx[lid] = dict(
                    id=lid, nom=l.get("nom"), type=typ, facade=c.get("facade_principale"), famille=l.get("family_id"),
                    facades_sec=c.get("facade_secondaire") or [], biomes=c.get("biomes") or [],
                    ecosysteme=c.get("ecosysteme"),
                    categories=(l.get("classification") or {}).get("categories") or [],
                    expositions=[f"{e.get('type')}:{e.get('objet')}" for e in (l.get("expositions") or [])],
                    materiaux=[m.get("mise_en_oeuvre") for m in arch.get("materiaux", []) if m.get("mise_en_oeuvre")],
                    routes=(l.get("reseau") or {}).get("routes_traversantes") or [],
                    pop=(((l.get("composition_ethnique") or {}).get("demography") or {}).get("total") or {}).get("nombre_1570"),
                )
    R = json.load(open(os.path.join(REF, "RESEAU_ROUTES.v3.json"), encoding="utf-8"))["routes"]
    return idx, R


GLOSES = {"Kralekh-ner": "AUX_KRALEKH-NER", "Qūrāš-Ṣafīḥ": "AUX_QURASH-SAFIH",
          "Kù-kèdà yì Mù-Kíri": "AUX_KUKEDA-MUKIRI", "Foyers-Purs": "AUX_FOYERS-PURS",
          "Voie-Desnuées": "AUX_VOIE-DESNUEES", "Voie-Haute": "AUX_VOIE-HAUTE",
          "Voie-Comptable": "AUX_VOIE-COMPTABLE", "Cercle-Sans-Juron": "AUX_CERCLE-SANS-JURON",
          "Lisières Ba-lóngó": "AUX_LISIERES_BALONGO", "Ports T'nayel SE": "AUX_PORTS-TNAYEL",
          "Méditerranée NE": "AUX_MEDITERRANEE_NE"}
POINTS = {"GEO_ORO_MUDARHOBI": "AUX_PIEMONTS_MUDARHOBI", "GEO_DLT_MOPAMA": "AUX_DLT_MOPAMA",
          "INST_TRK_TAMA": "AUX_TAMA-ARA", "INST_SMQ_DIMLAS": "AUX_DIMLAS", "INST_SMQ_SIDQ": "AUX_VOIE-PURE",
          "INST_CIV_KISRALOM": "AUX_KISRALOM", "INST_MBR_MUKIRI": "AUX_FORGES-DES-COQUES",
          "INST_MBR_MUSUKU": "AUX_SANUBE-MUSUKU", "INST_SMQ_HAMUQAS": "AUX_HAMUQAS",
          "INST_QYR_KUMEL": "AUX_HAE-KUMEL", "EXT_REG_PORTS_NO": "AUX_PORTS-EXTERNES-NO"}


def point_route(o):
    pid = o.get("point_id")
    if pid and (pid.startswith("LUR_") or pid.startswith("ZRS_") or pid.startswith("GEO_COL_")):
        return pid
    if pid in POINTS:
        return POINTS[pid]
    return GLOSES.get(o.get("glose"))


# =============================================================================================== contexte

class Contexte:
    """Masques et distances sur la grille de la carte."""

    def __init__(self, E, log):
        self.E, self.g, self.rel = E, E.g, E.rel
        g, rel = self.g, self.rel
        f = os.path.join(CACHE, f"contexte_{id_etat(E)}.pkl")
        if os.path.exists(f):
            self.__dict__.update(pickle.load(open(f, "rb")))
            return
        log("  contexte : distances, fleuves nommés, îles…")
        d = {}
        self.fleuves = {}
        riv = np.zeros(g.shape, bool)
        for Fl in rel.fleuves:
            gid = Fl["cfg"].get("geo_id")
            m = np.zeros(g.shape, np.uint8)
            for c in Fl["lignes"]:
                ls = g.ligne_px(np.asarray(c))
                m |= g.rasteriser([ls.buffer(0.8)], all_touched=True)
            m = m.astype(bool) & ~rel.mer & ~rel.ocean
            self.fleuves[gid] = m
            riv |= m
        self.riv = riv
        for k, m in (("mer", rel.mer), ("ocean", rel.ocean), ("lac", rel.lac > 0), ("riv", riv | (E.Q >= 150)),
                     ("terre", rel.terre)):
            dd, (iy, ix) = distance_transform_edt(~m, return_indices=True)
            d[k] = ((dd * g.km_px[:, None]).astype(np.float32), iy.astype(np.int16), ix.astype(np.int16))
        self.d = d
        lab, n = label(rel.terre)
        tailles = np.bincount(lab.ravel())
        tailles[0] = 0
        self.continent = lab == np.argmax(tailles)
        gy, gx = np.gradient(rel.h.astype(np.float32))
        kmp = g.km_px[:, None] * 1000
        self.pente = (np.hypot(gx, gy) / kmp * 100).astype(np.float32)      # %
        pickle.dump({k: v for k, v in self.__dict__.items() if k not in ("E", "g", "rel")}, open(f, "wb"), protocol=4)


def id_etat(E):
    import hashlib
    return hashlib.sha1(np.ascontiguousarray(E.rel.h[::7, ::7]).tobytes()).hexdigest()[:10]


# =============================================================================================== placement

def placer(cfgs, C, cols, log):
    E, g, rel = C.E, C.g, C.rel
    pos = {}
    par_id = {c["id"]: c for c in cfgs}
    for c in cfgs:
        if "meme_que" in c:
            continue
        lon0, lat0 = c["cible"]
        R = c.get("rayon_km", 40)
        x0, y0 = g.px(lon0, lat0)
        kp = g.km_px_a(lat0)
        r = int(R / kp) + 2
        xa, xb = int(max(0, x0 - r)), int(min(g.W, x0 + r + 1))
        ya, yb = int(max(0, y0 - r)), int(min(g.H, y0 + r + 1))
        yy, xx = np.mgrid[ya:yb, xa:xb]
        dist = np.hypot(xx + 0.5 - x0, yy + 0.5 - y0) * kp
        sl = (slice(ya, yb), slice(xa, xb))
        terre = rel.terre[sl]
        eau = c.get("eau", "aucune")
        if eau in ("mer", "ocean", "lac"):
            ok = terre & (C.d[eau][0][sl] <= 2.5 * kp + 0.5)
        elif eau == "fleuve":
            m = C.fleuves.get(c.get("fleuve"), C.riv)
            dm = distance_transform_edt(~m[sl]) * kp
            ok = terre & (dm <= 3.0)
            if c.get("fleuve") in ("GEO_FLV_ABNUHIL_ABNIQA",) or eau == "fleuve":
                pass
        elif eau == "ile":
            ok = terre & ~C.continent[sl]
        elif eau == "dans_lac":
            ok = (rel.lac[sl] > 0) & (C.d["terre"][0][sl] <= 12)
        elif eau == "en_mer":
            ok = rel.ocean[sl] | rel.mer[sl]
        else:
            ok = terre.copy()
        ok &= dist <= R
        cl = E.classes[sl]
        h = rel.h[sl]
        score = dist / R
        mil = [CODE[m] for m in c.get("milieux", []) if m in CODE]
        if mil:
            rang = np.full(cl.shape, 2.0, np.float32)
            for i, m in enumerate(mil):
                rang = np.where((cl == m) & (rang > 1), 0.15 * i, rang)
            score = score + rang
        if "altitude" in c:
            a, b = c["altitude"]
            score = score + np.clip(np.maximum(a - h, h - b), 0, None) / 300.0
        score = np.where(ok, score, np.inf)
        if not np.isfinite(score).any():
            log(f"  ! {c['id']} : aucune cellule admissible dans {R} km — cible conservée")
            pos[c["id"]] = dict(lon=lon0, lat=lat0, admissible=False)
            continue
        j = np.unravel_index(np.argmin(score), score.shape)
        x, y = xa + j[1], ya + j[0]
        lon, lat = g.ll(x + 0.5, y + 0.5)
        pos[c["id"]] = dict(lon=float(lon), lat=float(lat), admissible=True,
                            ecart_cible_km=r1(dist[j], 0), milieu_prefere=bool(mil and cl[j] in mil))
    for c in cfgs:
        if "meme_que" in c:
            pos[c["id"]] = dict(pos[c["meme_que"]], meme_que=c["meme_que"])
    for col in cols:
        pos[col["geo_id"]] = dict(lon=col["pos"][0], lat=col["pos"][1], admissible=True, col=True)
    return pos


# =============================================================================================== caractéristiques

def caracteriser(lid, p, C, cols, Q_noms):
    E, g, rel = C.E, C.g, C.rel
    x, y = g.px(p["lon"], p["lat"])
    x, y = min(int(x), g.W - 1), min(int(y), g.H - 1)
    kp = g.km_px[y]
    out = dict(lon=r1(p["lon"], 3), lat=r1(p["lat"], 3))
    eau = "mer Halakhel" if rel.mer[y, x] else "océan" if rel.ocean[y, x] else ("lac" if rel.lac[y, x] else None)
    out["sur_l_eau"] = eau
    out["altitude_m"] = int(round(float(rel.h[y, x]))) if not eau else None
    r10 = max(1, int(10 / kp))
    bloc = rel.h[max(0, y - r10):y + r10 + 1, max(0, x - r10):x + r10 + 1]
    out["denivele_10km_m"] = int(bloc.max() - bloc.min())
    out["pente_pct"] = r1(C.pente[y, x], 1)
    for k, nom in (("mer", "d_halakhel_km"), ("ocean", "d_ocean_km"), ("lac", "d_lac_km"), ("riv", "d_cours_eau_km")):
        out[nom] = int(round(float(C.d[k][0][y, x])))
    # fleuve nommé le plus proche
    best = (1e9, None)
    for gid, m in C.fleuves.items():
        sl = (slice(max(0, y - 40), y + 41), slice(max(0, x - 40), x + 41))
        ys, xs = np.nonzero(m[sl])
        if len(ys):
            dd = np.hypot(ys + sl[0].start - y, xs + sl[1].start - x).min() * kp
            if dd < best[0]:
                best = (dd, gid)
    out["fleuve_nomme"] = Q_noms.get(best[1], best[1]) if best[0] < 30 else None
    rq = max(1, int(15 / kp))
    out["debit_proche_m3s"] = int(round(float(E.Q[max(0, y - rq):y + rq + 1, max(0, x - rq):x + rq + 1].max())))
    out["pluie_mm"] = int(round(float(E.P[y, x])))
    out["T_annuelle_C"] = r1(E.T[y, x])
    out["Tw_hiver_C"] = r1(E.Tw[y, x])
    out["Tn_nuit_hiver_C"] = r1(E.Tn[y, x])
    out["facies_arin"] = FACIES.get(int(E.facies[y, x]))
    c0 = int(E.classes[y, x])
    out["milieu_site"] = NOM_MIL.get(c0, {253: "mer Halakhel", 254: "océan", 252: "hors Beliet"}.get(c0, str(c0)))
    r25 = max(1, int(25 / kp))
    bl = E.classes[max(0, y - r25):y + r25 + 1, max(0, x - r25):x + r25 + 1].ravel()
    u, n = np.unique(bl, return_counts=True)
    o = np.argsort(-n)
    out["milieux_25km"] = {NOM_MIL.get(int(u[i]), {253: "mer Halakhel", 254: "océan", 252: "hors Beliet"}.get(int(u[i]), str(u[i]))):
                           int(round(100 * n[i] / len(bl))) for i in o[:4] if n[i] * 100 >= 5 * len(bl)}
    # col le plus proche
    dmin, cmin = 1e9, None
    for col in cols:
        dd = km((p["lon"], p["lat"]), col["pos"])
        if dd < dmin:
            dmin, cmin = dd, col
    out["col_proche"] = dict(geo_id=cmin["geo_id"], nom=cmin["nom"], altitude_m=cmin["altitude_m"],
                             distance_km=int(round(dmin)), ouverture=cmin.get("ouverture_mois"))
    # expositions physiques calculées
    ex = []
    dlit = C.d["riv"][0][y, x]
    if dlit < 8 and out["altitude_m"] is not None and out["debit_proche_m3s"] >= 50:
        ex.append("crues (lit majeur)")
    if (out["d_halakhel_km"] < 40 and int(E.facies[y, x]) in (3, 4)) or int(E.facies[y, x]) == 4:
        ex.append("brouillards d'évaporation (Hiver de Vapeur)")
    if any(k in out["milieux_25km"] for k in ("desert_sableux", "dunes_littorales")):
        ex.append("ensablement (sables à moins de 25 km)")
    if out["d_ocean_km"] < 15 or out["d_halakhel_km"] < 15:
        ex.append("tempêtes et houle de rivage")
    if out["altitude_m"] and out["altitude_m"] > 1800 and int(E.facies[y, x]) in (1, 2) and out["denivele_10km_m"] > 600:
        ex.append("avalanches / chutes de pierres (|'Arin)")
    if out["denivele_10km_m"] > 900:
        ex.append("éboulements, glissements (versants raides)")
    if out["altitude_m"] and out["altitude_m"] > 2500:
        ex.append("hypoxie légère (> 2 500 m)")
    if int(E.facies[y, x]) == 1:
        ex.append("Hiver Blanc : neige et gel durables")
    if out["pluie_mm"] < 150 and not eau:
        ex.append("aridité (< 150 mm)")
    out["expositions_calculees"] = ex
    return out


# =============================================================================================== vérifications

MOTS_EXPO = [
    (r"brouillard|brume", lambda c: any("brouillard" in e for e in c["expositions_calculees"]) or c["d_lac_km"] < 15,
     "brouillards / brumes"),
    (r"crue|inond", lambda c: c["debit_proche_m3s"] >= 30 or c["d_lac_km"] < 10 or c["d_cours_eau_km"] < 15, "crues"),
    (r"ensabl", lambda c: any("ensablement" in e for e in c["expositions_calculees"]) or c["milieu_site"] in ("desert_pierreux", "steppe_piemont") and c["pluie_mm"] < 350,
     "ensablement"),
    (r"avalanche|névé", lambda c: c["altitude_m"] is not None and c["altitude_m"] > 1500 and c["denivele_10km_m"] > 500,
     "avalanches"),
    (r"éboul|glissement", lambda c: c["denivele_10km_m"] > 350, "éboulements / glissements"),
    (r"tempête|cyclon|houle", lambda c: c["d_ocean_km"] < 30 or c["d_halakhel_km"] < 30 or c["d_lac_km"] < 30, "tempêtes"),
    (r"sécheresse|famines sécheresse", lambda c: c["pluie_mm"] < 900, "sécheresses"),
    (r"hypoxie", lambda c: c["altitude_m"] is not None and c["altitude_m"] > 2400, "hypoxie"),
    (r"envasement|vase", lambda c: c["d_cours_eau_km"] < 30 or c["d_halakhel_km"] < 10, "envasement"),
]
COMPATIBLES = {
    "littoral_rocheux": {"littoral_rocheux"},
    "plaine_alluviale": {"plaine_alluviale", "foret_berge"},
    "oasis": {"oasis"},
    "desert_sableux": {"desert_sableux", "dunes_littorales"},
    "steppe_piemont": {"steppe_piemont", "herbage_arbore"},
    "depression_saline": {"depression_saline"},
    "foret_maree": {"foret_maree"},
    "zone_humide_lacustre": {"zone_humide_lacustre", "eaux_lacustres"},
    "eaux_lacustres": {"eaux_lacustres", "zone_humide_lacustre", "lac"},
    "foret_tropicale_humide": {"foret_tropicale_humide"},
    "foret_berge": {"foret_berge", "foret_tropicale_humide", "herbage_arbore"},
    "foret_montagne": {"foret_montagne"},
    "prairie_altitude": {"prairie_altitude"},
    "glacier": {"glacier", "zone_periglaciaire"},
    "ile_aride": {"ile_aride", "littoral_rocheux", "dunes_littorales", "desert_pierreux"},
}


def verifier(lid, info, c):
    """Confronte le corpus (biomes, expositions) au site calculé. Renvoie une liste de constats."""
    constats = []
    milieux_ici = set(c["milieux_25km"]) | {c["milieu_site"]}
    if c["sur_l_eau"] == "lac":
        milieux_ici |= {"lac", "eaux_lacustres"}
    for b in info.get("biomes", []):
        ok = bool(COMPATIBLES.get(b, {b}) & milieux_ici)
        constats.append(dict(objet=f"biome « {b} »", verdict="ok" if ok else "écart",
                             detail=None if ok else f"milieux calculés : {', '.join(sorted(milieux_ici))}"))
    for e in info.get("expositions", []):
        t, _, obj = e.partition(":")
        if t not in ("geophysique", "environnemental", "sanitaire"):
            continue
        for motif, test, lib in MOTS_EXPO:
            if re.search(motif, obj, re.I):
                ok = bool(test(c))
                constats.append(dict(objet=f"exposition « {obj} »", verdict="ok" if ok else "écart",
                                     detail=None if ok else f"non soutenue par le site ({lib})"))
                break
    return constats


# =============================================================================================== routage

class Reseau:
    """Grille de routage (facteur F) : milieux de passage, altitudes, rivières."""

    def __init__(self, C, log):
        E, g, rel = C.E, C.g, C.rel
        self.C, self.g = C, g
        H, W = g.H // F, g.W // F
        self.H, self.W = H, W

        def blocs(a, op):
            a = a[:H * F, :W * F].reshape(H, F, W, F)
            return op(op(a, axis=3), axis=1)
        frac = lambda m: blocs(m.astype(np.float32), np.mean)
        # océan navigable : eaux réellement marines reliées entre elles (exclut les liserés du contour et
        # les dépressions intérieures sous le niveau de la mer, mer Morte, lac Assal)
        from scipy.ndimage import binary_opening
        # mer réelle (relief réel ≤ 0, grandes étendues) + liseré côtier de 25 km : le contour du Beliet laisse
        # par endroits une bande « hors Beliet » (jusqu'à ~20 km) entre la côte dessinée et la mer réelle
        vrai = binary_opening(~rel.beliet & (rel.h_reel <= 0), iterations=1)
        lab, n = label(vrai)
        tailles = np.bincount(lab.ravel())
        tailles[0] = 0
        vrai = np.isin(lab, np.nonzero(tailles > 20000)[0])
        d_vrai = distance_transform_edt(~vrai) * g.km_px[:, None]
        vrai |= (rel.ocean | rel.dehors) & (d_vrai < 25)
        oc, me, la = frac(vrai), frac(rel.mer), frac(rel.lac > 0)
        te = frac(rel.terre & (rel.fondu > 0.25))
        med = np.full((H, W), 4, np.int8)                  # 4 = infranchissable
        med[te > 0.34] = 0
        med[la >= 0.5] = 3
        med[me >= 0.4] = 2
        med[oc >= 0.5] = 1
        self.med = med
        hh = np.where(rel.terre, rel.h, 9000).astype(np.float32)
        self.hmin = blocs(hh, np.min)
        self.hmin = np.where(self.hmin > 8000, 0, self.hmin)
        self.riv = blocs(C.riv.astype(np.uint8), np.max).astype(bool) | (blocs(E.Q, np.max) >= 150)
        self.riv &= med == 0
        c = E.classes[F // 2::F, F // 2::F][:H, :W]
        self.frein = np.ones((H, W), np.float32)
        for nom, v in FREIN_MILIEU.items():
            self.frein[c == CODE[nom]] = v
        self.classes = c
        self.facies = E.facies[F // 2::F, F // 2::F][:H, :W]
        self.cote = (blocs((C.d["terre"][0] <= 40).astype(np.uint8), np.max) > 0)
        self.kmc = (g.km_px[F // 2::F][:H] * F).astype(np.float32)        # km par cellule (ligne)
        self.cache = {}

    def idx(self, lon, lat):
        x, y = self.g.px(lon, lat)
        return int(min(self.H - 1, y // F)), int(min(self.W - 1, x // F))

    def graphe(self, modes):
        cle = tuple(sorted(modes))
        if cle in self.cache:
            return self.cache[cle]
        H, W = self.H, self.W
        med, hmin, riv = self.med, self.hmin, self.riv
        mer_ok = bool({"maritime_cabotage", "maritime_hauturier"} & modes)
        haut = "maritime_hauturier" in modes
        lac_ok = bool({"lacustre", "fluvial", "maritime_cabotage"} & modes)
        flu_ok = "fluvial" in modes
        terres = [m for m in modes if m in ("terrestre_caravane", "terrestre_portage", "col_haute_altitude")]
        v_terre = max([V[m] for m in terres]) if terres else V["terrestre_caravane"]
        terre_ok = bool(terres)
        N = H * W
        ids = np.arange(N).reshape(H, W)
        lignes, cols, temps, interdit = [], [], [], []
        for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)):
            ya, yb = max(0, -dy), H - max(0, dy)
            xa, xb = max(0, -dx), W - max(0, dx)
            u = ids[ya:yb, xa:xb].ravel()
            v = ids[ya + dy:yb + dy, xa + dx:xb + dx].ravel()
            mu = med[ya:yb, xa:xb].ravel()
            mv = med[ya + dy:yb + dy, xa + dx:xb + dx].ravel()
            d = self.kmc[ya:yb][:, None].repeat(xb - xa, 1).ravel() * (1.4142 if dx and dy else 1.0)
            hu = hmin[ya:yb, xa:xb].ravel()
            hv = hmin[ya + dy:yb + dy, xa + dx:xb + dx].ravel()
            ru = riv[ya:yb, xa:xb].ravel()
            rv = riv[ya + dy:yb + dy, xa + dx:xb + dx].ravel()
            fr = self.frein[ya + dy:yb + dy, xa + dx:xb + dx].ravel()
            cote = self.cote[ya + dy:yb + dy, xa + dx:xb + dx].ravel()
            t = np.full(len(u), np.inf, np.float64)
            pen = np.zeros(len(u), bool)
            # mer / océan
            sea = (mu == mv) & ((mu == 1) | (mu == 2))
            vs = np.where(cote, V["cabotage"], V["hauturier"] if haut else V["cabotage"] / 1.5)
            t = np.where(sea, d / vs, t)
            pen |= sea & (not mer_ok)
            # lac
            lk = (mu == 3) & (mv == 3)
            t = np.where(lk, d / V["lacustre"], t)
            pen |= lk & (not lac_ok)
            # transbordement eau ↔ terre
            tr = ((mu == 0) & np.isin(mv, (1, 2, 3))) | ((mv == 0) & np.isin(mu, (1, 2, 3)))
            t = np.where(tr, TRANSBORD_J + d / 2 / v_terre, t)
            # terre
            ld = (mu == 0) & (mv == 0)
            dh = hv - hu
            s = dh / (d * 1000)
            tob = np.exp(-3.5 * np.abs(s + 0.05)) / np.exp(-0.175)
            alt = 1 + np.clip((np.maximum(hu, hv) - 2200) / 1000, 0, None) ** 2 * 0.6
            t_terre = d / (v_terre * tob * fr) * alt + np.clip(dh, 0, None) / 2500
            fl = ld & ru & rv & flu_ok & (np.abs(dh) <= PENTE_NAVIGABLE * d * 1000)
            v_fl = np.where(dh < -2, V["fluvial_aval"], np.where(dh > 2, V["fluvial_amont"], V["fluvial_plat"]))
            t = np.where(ld, np.where(fl, d / v_fl, t_terre), t)
            pen |= ld & ~fl & (not terre_ok)
            t = np.where(pen, t * PENALITE, t)
            ok = np.isfinite(t)
            lignes.append(u[ok]); cols.append(v[ok]); temps.append(t[ok]); interdit.append(pen[ok])
        M = csr_matrix((np.concatenate(temps), (np.concatenate(lignes), np.concatenate(cols))), shape=(N, N))
        self.cache[cle] = M
        return M

    def chemin(self, modes, a, b):
        M = self.graphe(modes)
        ia = a[0] * self.W + a[1]
        ib = b[0] * self.W + b[1]
        dist, pred = dijkstra(M, directed=True, indices=ia, return_predecessors=True)
        if not np.isfinite(dist[ib]):
            return None
        p = [ib]
        while p[-1] != ia:
            p.append(pred[p[-1]])
        p = np.array(p[::-1])
        return np.c_[p // self.W, p % self.W]


def mesurer_route(R, cells, modes, cols):
    """Décompose le tracé en milieux et calcule longueur, durée, altitudes, cols, saisons."""
    g = R.g
    med = R.med[cells[:, 0], cells[:, 1]]
    hm = R.hmin[cells[:, 0], cells[:, 1]]
    rv = R.riv[cells[:, 0], cells[:, 1]]
    xs = (cells[:, 1] * F + F / 2)
    ys = (cells[:, 0] * F + F / 2)
    lon, lat = g.ll(xs, ys)
    pts = np.c_[lon, lat]
    seg = GEOD.inv(lon[:-1], lat[:-1], lon[1:], lat[1:])[2] / 1000
    mer_ok = bool({"maritime_cabotage", "maritime_hauturier"} & modes)
    lac_ok = bool({"lacustre", "fluvial", "maritime_cabotage"} & modes)
    flu_ok = "fluvial" in modes
    terres = [m for m in modes if m in ("terrestre_caravane", "terrestre_portage", "col_haute_altitude")]
    v_terre = max([V[m] for m in terres]) if terres else V["terrestre_caravane"]
    km_ = {"mer Halakhel": 0.0, "océan": 0.0, "lac": 0.0, "fleuve (aval)": 0.0, "fleuve (amont)": 0.0, "terre": 0.0}
    hors = {"mer": 0.0, "lac": 0.0, "terre": 0.0}
    jours = 0.0
    transb = 0
    for i, d in enumerate(seg):
        a, b = med[i], med[i + 1]
        if a in (1, 2) and b == a:
            k = "océan" if a == 1 else "mer Halakhel"
            km_[k] += d
            cote = R.cote[cells[i + 1, 0], cells[i + 1, 1]]
            jours += d / (V["cabotage"] if cote or "maritime_hauturier" not in modes else V["hauturier"])
            if not mer_ok:
                hors["mer"] += d
        elif a == 3 and b == 3:
            km_["lac"] += d
            jours += d / V["lacustre"]
            if not lac_ok:
                hors["lac"] += d
        elif a == 0 and b == 0:
            dh = hm[i + 1] - hm[i]
            if flu_ok and rv[i] and rv[i + 1] and abs(dh) <= PENTE_NAVIGABLE * d * 1000:
                k = "fleuve (aval)" if dh <= 0 else "fleuve (amont)"
                km_[k] += d
                jours += d / (V["fluvial_aval"] if dh < -2 else V["fluvial_amont"] if dh > 2 else V["fluvial_plat"])
            else:
                km_["terre"] += d
                s = dh / max(d * 1000, 1)
                tob = np.exp(-3.5 * abs(s + 0.05)) / np.exp(-0.175)
                fr = R.frein[cells[i + 1, 0], cells[i + 1, 1]]
                alt = 1 + max(0.0, (max(hm[i], hm[i + 1]) - 2200) / 1000) ** 2 * 0.6
                jours += d / (v_terre * tob * fr) * alt + max(0.0, dh) / 2500
                if not terres:
                    hors["terre"] += d
        else:
            transb += 1
            jours += TRANSBORD_J
            km_["terre"] += d / 2
    terre = med == 0
    h_land = np.where(terre, hm, np.nan)
    alt_max = float(np.nanmax(h_land)) if terre.any() else None
    asc = float(np.nansum(np.clip(np.diff(np.where(terre, hm, np.nan)), 0, None)))
    # cols franchis : col à moins de 15 km d'un point du tracé situé à plus de 1 200 m
    franchis = []
    for col in cols:
        cl_lon, cl_lat = col["pos"]
        dd = GEOD.inv(np.full(len(lon), cl_lon), np.full(len(lat), cl_lat), lon, lat)[2] / 1000
        j = int(np.argmin(dd))
        if dd[j] < 15 and terre[j] and hm[j] > 1200:
            franchis.append(col)
    mil = {}
    for i, d in enumerate(seg):
        if med[i + 1] == 0:
            c = NOM_MIL.get(int(R.classes[cells[i + 1, 0], cells[i + 1, 1]]), "?")
            mil[c] = mil.get(c, 0) + d
    fac = {}
    for i, d in enumerate(seg):
        if med[i + 1] == 0:
            f_ = FACIES.get(int(R.facies[cells[i + 1, 0], cells[i + 1, 1]]))
            fac[f_] = fac.get(f_, 0) + d
    # tronçons par milieu (pour la carte)
    nav = np.zeros(len(med), bool)
    for i, d in enumerate(seg):
        if rv[i] and rv[i + 1] and abs(hm[i + 1] - hm[i]) <= PENTE_NAVIGABLE * d * 1000:
            nav[i] = nav[i + 1] = True
    cat = np.where((med == 1) | (med == 2), 0, np.where(med == 3, 1, np.where((med == 0) & nav & flu_ok, 2, 3)))
    noms_cat = ["mer", "lac", "fleuve", "terre"]
    hors_cat = [not mer_ok, not lac_ok, False, not terres]
    segs_m = []
    debut = 0
    for i in range(1, len(cat) + 1):
        if i == len(cat) or cat[i] != cat[debut]:
            k = int(cat[debut])
            j1 = min(i, len(cat) - 1)
            segs_m.append(dict(milieu=noms_cat[k], hors_modes=bool(hors_cat[k]),
                               pts=[[r1(lon[q], 3), r1(lat[q], 3)] for q in range(max(0, debut - 1), j1 + 1)]))
            debut = i
    ouverts = set(range(1, 13))
    for col in franchis:
        a, b = col.get("ouverture_mois") or [1, 12]
        ouverts &= set(range(a, b + 1))
    return dict(
        longueur_km=int(round(seg.sum())),
        km_par_milieu={k: int(round(v)) for k, v in km_.items() if v >= 1},
        km_hors_modes_declares={k: int(round(v)) for k, v in hors.items() if v >= 5},
        ruptures_de_charge=transb,
        duree_jours=r1(jours, 0) if jours >= 10 else r1(jours, 1),
        altitude_max_m=None if alt_max is None else int(round(alt_max)),
        denivele_positif_m=int(round(asc)),
        cols_franchis=[f"{c['nom']} ({c['geo_id'][-3:]}, {c['altitude_m']} m)" for c in franchis],
        mois_ouverts=None if not franchis else (f"{MOIS[min(ouverts) - 1]} → {MOIS[max(ouverts) - 1]}" if ouverts else "aucun mois commun"),
        milieux_km={k: int(round(v)) for k, v in sorted(mil.items(), key=lambda t: -t[1]) if v >= 20},
        facies_km={k: int(round(v)) for k, v in sorted(fac.items(), key=lambda t: -t[1]) if v >= 20},
        trace=[[r1(a, 3), r1(b, 3)] for a, b in pts[::max(1, len(pts) // 400)]] + [[r1(pts[-1][0], 3), r1(pts[-1][1], 3)]],
        segments_milieu=segs_m,
    )


def tracer_routes(ROUTES, pos, R, cols, routes_cfg, log):
    cols_par_id = {c["geo_id"]: c for c in cols}
    res = {}
    for rt in ROUTES:
        rid = rt["route_id"]
        e = rt["extremites"]
        a, b = point_route(e["origine"]), point_route(e["destination"])
        modes = {s["mode"] for s in rt["trajet"]["segments"]}
        cfg = routes_cfg.get(rid, {})
        via = [p["geo_id"] for p in rt["trajet"]["passages"] if p.get("geo_id", "").startswith("GEO_COL_")]
        via = cfg.get("via", via)
        out = dict(route_id=rid, nom=rt["nom"], origine=a, destination=b, modes_declares=sorted(modes))
        if a not in pos or b not in pos:
            out["statut"] = "extrémité non localisable"
            res[rid] = out
            continue
        etapes = [a] + via + [b]
        cells = []
        echec = False
        for u, w in zip(etapes[:-1], etapes[1:]):
            pu, pw = pos[u], pos[w]
            c = R.chemin(modes, R.idx(pu["lon"], pu["lat"]), R.idx(pw["lon"], pw["lat"]))
            if c is None:
                echec = True
                break
            cells.append(c if not cells else c[1:])
        if echec:
            out["statut"] = "aucun tracé"
            res[rid] = out
            continue
        cells = np.concatenate(cells)
        out.update(mesurer_route(R, cells, modes, cols))
        if cfg.get("via_corpus"):
            et2 = [a] + list(cfg["via_corpus"]) + [b]
            c2 = []
            for u, w in zip(et2[:-1], et2[1:]):
                pu, pw = pos[u], pos[w]
                c = R.chemin(modes, R.idx(pu["lon"], pu["lat"]), R.idx(pw["lon"], pw["lat"]))
                c2.append(c if not c2 else c[1:])
            v = mesurer_route(R, np.concatenate(c2), modes, cols)
            v["via"] = cfg["via_corpus"]
            out["variante_corpus"] = v
        if cfg.get("note"):
            out["note_reglage"] = cfg["note"]
        out["via"] = via
        out["vol_oiseau_km"] = int(round(km((pos[a]["lon"], pos[a]["lat"]), (pos[b]["lon"], pos[b]["lat"]))))
        out["statut"] = "tracé"
        res[rid] = out
    log(f"  {sum(1 for r in res.values() if r['statut'] == 'tracé')} routes tracées sur {len(res)}")
    return res


# =============================================================================================== sorties

def exporter_sig(lieux, routes):
    feats = []
    for l in lieux.values():
        c = l["caracteristiques"]
        props = {k: v for k, v in c.items() if k not in ("lon", "lat")}
        props.update(id=l["id"], nom=l["nom"], type=l["type"], facade=l["facade"], confiance=l["confiance"],
                     note=l["note"], ecarts_corpus=l["constats_ecarts"], statut="[PROPOSITION]")
        props["col_proche"] = json.dumps(props["col_proche"], ensure_ascii=False)
        props["milieux_25km"] = json.dumps(props["milieux_25km"], ensure_ascii=False)
        props["expositions_calculees"] = "; ".join(props["expositions_calculees"])
        feats.append(dict(type="Feature", geometry=dict(type="Point", coordinates=[c["lon"], c["lat"]]), properties=props))
    json.dump(dict(type="FeatureCollection", features=feats), open(os.path.join(SIG, "beliet_lieux.geojson"), "w", encoding="utf-8"),
              ensure_ascii=False)
    feats = []
    for r in routes.values():
        if r.get("statut") != "tracé":
            continue
        props = {k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
                 for k, v in r.items() if k not in ("trace", "segments_milieu", "variante_corpus")}
        feats.append(dict(type="Feature", geometry=dict(type="LineString", coordinates=r["trace"]), properties=props))
        if r.get("variante_corpus"):
            v = r["variante_corpus"]
            feats.append(dict(type="Feature", geometry=dict(type="LineString", coordinates=v["trace"]),
                              properties=dict(route_id=r["route_id"] + "_variante", nom=r["nom"] + " (variante du corpus)",
                                              longueur_km=v["longueur_km"], duree_jours=v["duree_jours"],
                                              altitude_max_m=v["altitude_max_m"], cols_franchis=json.dumps(v["cols_franchis"], ensure_ascii=False))))
    json.dump(dict(type="FeatureCollection", features=feats), open(os.path.join(SIG, "beliet_routes.geojson"), "w", encoding="utf-8"),
              ensure_ascii=False)


def _kv(d, unite=""):
    return ", ".join(f"{k} {v}{unite}" for k, v in d.items()) if d else "—"


def documenter(lieux, routes, log):
    L = []
    L.append("### A. Lieux : position et site\n")
    L.append("Positions [PROPOSITION] en [longitude, latitude]. « Écart » = distance entre la cible raisonnée et la cellule retenue.\n")
    L.append("| ID | Nom | Type | Façade | Position | Altitude (m) | Dénivelé 10 km (m) | Milieu du site | Milieux à 25 km (%) |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for l in lieux.values():
        c = l["caracteristiques"]
        alt = c["altitude_m"] if c["altitude_m"] is not None else f"sur l'eau ({c['sur_l_eau']})"
        L.append(f"| `{l['id']}` | {l['nom']} | {l['type']} | {l['facade'] or '—'} | [{c['lon']}, {c['lat']}] | {alt} | "
                 f"{c['denivele_10km_m']} | {c['milieu_site']} | {_kv(c['milieux_25km'])} |")
    L.append("\n### B. Lieux : climat, eaux, cols\n")
    L.append("| ID | Pluie (mm/an) | T annuelle (°C) | Hiver Tw / nuit Tn (°C) | Faciès \\|'Arin | Distance mer Halakhel / océan / lac / cours d'eau (km) | Fleuve nommé à < 30 km ; débit max à 15 km (m³/s) | Col le plus proche |")
    L.append("|---|---|---|---|---|---|---|---|")
    for l in lieux.values():
        c = l["caracteristiques"]
        cp = c["col_proche"]
        L.append(f"| `{l['id']}` | {c['pluie_mm']} | {c['T_annuelle_C']} | {c['Tw_hiver_C']} / {c['Tn_nuit_hiver_C']} | {c['facies_arin']} | "
                 f"{c['d_halakhel_km']} / {c['d_ocean_km']} / {c['d_lac_km']} / {c['d_cours_eau_km']} | {c['fleuve_nomme'] or '—'} ; {c['debit_proche_m3s']} | "
                 f"{cp['nom']} ({cp['altitude_m']} m) à {cp['distance_km']} km |")
    L.append("\n### C. Lieux : expositions calculées et écarts avec le corpus\n")
    L.append("| ID | Nom | Expositions physiques calculées | Écarts (biomes et expositions du corpus non soutenus par le site) |")
    L.append("|---|---|---|---|")
    for l in lieux.values():
        if l["type"] == "AUX":
            continue
        c = l["caracteristiques"]
        ec = [f"{k['objet']} — {k['detail']}" for k in l["constats"] if k["verdict"] != "ok"]
        L.append(f"| `{l['id']}` | {l['nom']} | {'; '.join(c['expositions_calculees']) or '—'} | {'<br>'.join(ec) or 'aucun'} |")
    L.append("\n### D. Routes : tracé calculé\n")
    L.append("Tracé le plus rapide sur la carte (grille ≈ 5 km), dans les modes déclarés par la route. Un milieu absent des modes déclarés n'est emprunté que s'il est inévitable (colonne « hors modes »).\n")
    L.append("| ID | Route | Modes déclarés | Longueur (vol d'oiseau) km | Durée (j) | km par milieu | Hors modes déclarés (km) | Ruptures de charge | Altitude max / D+ (m) | Cols franchis ; mois ouverts |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in routes.values():
        if r.get("statut") != "tracé":
            L.append(f"| `{r['route_id']}` | {r['nom']} | {', '.join(r['modes_declares'])} | — | — | — | — | — | — | {r.get('statut')} |")
            continue
        cols_t = "; ".join(r["cols_franchis"]) or "—"
        if r.get("mois_ouverts"):
            cols_t += f" ; {r['mois_ouverts']}"
        L.append(f"| `{r['route_id']}` | {r['nom']} | {', '.join(r['modes_declares'])} | {r['longueur_km']} ({r['vol_oiseau_km']}) | {r['duree_jours']} | "
                 f"{_kv(r['km_par_milieu'])} | {_kv(r['km_hors_modes_declares']) } | {r['ruptures_de_charge']} | {r['altitude_max_m']} / {r['denivele_positif_m']} | {cols_t} |")
    L.append("\n### E. Routes : milieux et hivers traversés (voies de terre)\n")
    L.append("| ID | Milieux traversés (km) | Faciès \\|'Arin traversés (km) |")
    L.append("|---|---|---|")
    for r in routes.values():
        if r.get("statut") == "tracé":
            L.append(f"| `{r['route_id']}` | {_kv(r['milieux_km'])} | {_kv(r['facies_km'])} |")
    var = [r for r in routes.values() if r.get("variante_corpus")]
    if var:
        L.append("\n### F. Variantes imposées par une indication du corpus\n")
        L.append("| ID | Étapes imposées | Longueur km | Durée (j) | Altitude max (m) | Cols franchis ; mois ouverts | Écart avec le tracé optimal |")
        L.append("|---|---|---|---|---|---|---|")
        for r in var:
            v = r["variante_corpus"]
            L.append(f"| `{r['route_id']}` | {', '.join(v['via'])} | {v['longueur_km']} | {v['duree_jours']} | {v['altitude_max_m']} | "
                     f"{'; '.join(v['cols_franchis']) or '—'} ; {v.get('mois_ouverts') or '—'} | +{v['longueur_km'] - r['longueur_km']} km, +{r1(v['duree_jours'] - r['duree_jours'], 0)} j |")
    bloc = echapper_tableaux("\n".join(L))
    f = os.path.join(RACINE, "LIEUX_ET_ROUTES.md")
    deb, fin = "<!-- GENERE:DEBUT (outils/lieux_routes.py — ne pas éditer à la main) -->", "<!-- GENERE:FIN -->"
    txt = open(f, encoding="utf-8").read() if os.path.exists(f) else f"# Lieux et routes du Beliet\n\n{deb}\n{fin}\n"
    i, j = txt.find(deb), txt.find(fin)
    txt = txt[:i + len(deb)] + "\n\n" + bloc + "\n\n" + txt[j:]
    open(f, "w", encoding="utf-8").write(txt)
    log("  LIEUX_ET_ROUTES.md : section générée mise à jour")


# =============================================================================================== principal

def main():
    log = lambda m: print(m, flush=True)
    log("Lieux et routes :")
    E = charger_etat(log)
    C = Contexte(E, log)
    cfg = yaml.safe_load(open(os.path.join(RACINE, "donnees", "lieux.yaml"), encoding="utf-8"))
    cfgs = cfg["lieux"]
    routes_cfg = (yaml.safe_load(open(os.path.join(RACINE, "donnees", "routes.yaml"), encoding="utf-8")) or {}).get("routes", {}) \
        if os.path.exists(os.path.join(RACINE, "donnees", "routes.yaml")) else {}
    cols = yaml.safe_load(open(os.path.join(RACINE, "donnees", "cols.yaml"), encoding="utf-8"))["cols"]
    idx, ROUTES = lire_corpus()
    Q_noms = {}
    for Fl in C.rel.fleuves:
        n = [x for x in (Fl["cfg"].get("noms") or []) if x] or [str(Fl["cfg"].get("geo_id"))]
        Q_noms[Fl["cfg"].get("geo_id")] = " / ".join(n)
    log("  placement…")
    pos = placer(cfgs, C, cols, log)
    lieux = {}
    for c in cfgs:
        lid = c["id"]
        info = idx.get(lid, dict(nom=c.get("nom"), type=c.get("type", "AUX")))
        car = caracteriser(lid, pos[lid], C, cols, Q_noms)
        lieux[lid] = dict(id=lid, nom=info.get("nom") or c.get("nom"), type=info.get("type", "AUX"),
                          facade=info.get("facade"), facades_sec=info.get("facades_sec", []),
                          cible=c.get("cible"), confiance=c.get("confiance", "haute" if lid[:3] in ("LUR", "ZRS") else "moyenne"),
                          note=c.get("note"), placement=pos[lid], caracteristiques=car,
                          biomes_corpus=info.get("biomes", []), expositions_corpus=info.get("expositions", []),
                          materiaux_corpus=info.get("materiaux", []), routes_corpus=info.get("routes", []),
                          pop_1570=info.get("pop"), famille=info.get("famille"),
                          constats=verifier(lid, info, car) if lid[:3] in ("LUR", "ZRS") else [])
        lieux[lid]["constats_ecarts"] = sum(1 for k in lieux[lid]["constats"] if k["verdict"] != "ok")
    log("  routes (grille ≈ 5 km)…")
    R = Reseau(C, log)
    routes = tracer_routes(ROUTES, pos, R, cols, routes_cfg, log)
    os.makedirs(SIG, exist_ok=True)
    json.dump(dict(lieux=lieux, routes=routes), open(os.path.join(SIG, "beliet_lieux_routes.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    log("  écrit carte/sig/beliet_lieux_routes.json")
    exporter_sig(lieux, routes)
    from carto.carte_lieux import carte
    log("  carte des lieux et des routes…")
    carte(C.rel, lieux, routes, cols, os.path.join(RACINE, "carte", "beliet_carte_lieux"), log)
    documenter(lieux, routes, log)


if __name__ == "__main__":
    main()
