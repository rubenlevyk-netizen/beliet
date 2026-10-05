#!/usr/bin/env python3
"""Mesure la carte générée et écrit les valeurs à reporter dans le corpus.

Usage (après outils/generer_carte.py) :
    python3 outils/mesures_corpus.py

Sorties :
    carte/sig/beliet_mesures.json   — toutes les mesures, lisibles par un agent
    ALIGNEMENT_CORPUS.md            — la section entre les balises MESURES est régénérée
"""
import glob
import json
import os
import pickle
import sys

import numpy as np
import yaml
from pyproj import Geod
from scipy.ndimage import distance_transform_edt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from carto.sources import RACINE, CACHE           # noqa: E402
from generer_carte import empreinte, charger_cols # noqa: E402

GEOD = Geod(ellps="WGS84")
SIG = os.path.join(RACINE, "carte", "sig")


def r1(v, n=1):
    return round(float(v), n)


def longueur(c):
    c = np.asarray(c, float)
    return GEOD.line_length(c[:, 0], c[:, 1]) / 1000


def dist(a, b):
    return GEOD.inv(a[0], a[1], b[0], b[1])[2] / 1000


def main():
    p = yaml.safe_load(open(os.path.join(RACINE, "donnees", "parametres_carte.yaml"), encoding="utf-8"))
    p["cols"] = charger_cols()
    rel = pickle.load(open(os.path.join(CACHE, f"relief_{empreinte(p)}.pkl"), "rb"))
    g = rel.g
    km = g.km_px[:, None]
    A = g.aire_km2()
    LON, LAT = rel.LON, rel.LAT
    ll = lambda y, x: [r1(g.lons[x], 2), r1(g.lats[y], 2)]
    M = {"version": None, "halakhel": {}, "lacs": {}, "chaines": {}, "fleuves": {}, "distances": {}, "fondu_sud": {}}
    M["version"] = json.load(open(os.path.join(SIG, "beliet_statistiques.json"), encoding="utf-8"))["version"]

    # ---------------------------------------------------------------- Halakhel
    mer = rel.mer
    ys, xs = np.nonzero(mer)
    H = M["halakhel"]
    H["superficie_km2"] = round(float(A[mer].sum()))
    H["emprise"] = {"lon_min": r1(g.lons[xs.min()], 2), "lon_max": r1(g.lons[xs.max()], 2),
                    "lat_min": r1(g.lats[ys.max()], 2), "lat_max": r1(g.lats[ys.min()], 2)}
    lat_m = 0.5 * (H["emprise"]["lat_min"] + H["emprise"]["lat_max"])
    H["longueur_O_E_km"] = round(dist((H["emprise"]["lon_min"], lat_m), (H["emprise"]["lon_max"], lat_m)))
    H["profondeur_max_m"] = round(float(rel.L - rel.h[mer].min()))
    H["niveau_m"] = rel.L
    H["iles"] = int(rel.infos.get("halakhel_iles", 0))
    prof = []
    for lon in np.arange(np.ceil(H["emprise"]["lon_min"]), H["emprise"]["lon_max"], 2.0):
        x = int(g.px(lon, 0)[0])
        col = np.nonzero(mer[:, x])[0]
        if not len(col):
            continue
        n, s = g.lats[col.min()], g.lats[col.max()]
        prof.append({"lon": r1(lon, 0), "rive_nord_lat": r1(n, 2), "rive_sud_lat": r1(s, 2),
                     "largeur_km": round(dist((lon, s), (lon, n))),
                     "eau_km_sur_le_meridien": round(float(len(col) * km[col, 0].mean()))})
    H["profil_par_meridien"] = prof
    # distances aux océans
    oc = rel.ocean
    d_oc, (iy, ix) = distance_transform_edt(~oc, return_indices=True)
    for nom, zone in (("atlantique", oc & (LON < -5)), ("mediterranee", oc & (LAT > 30) & (LON > -5) & (LON < 33)),
                      ("mer_rouge", oc & (LON > 32) & (LON < 44) & (LAT > 12) & (LAT < 30))):
        d, (jy, jx) = distance_transform_edt(~zone, return_indices=True)
        dk = np.where(mer, d * km, np.inf)
        k = np.unravel_index(np.argmin(dk), dk.shape)
        H[f"distance_min_{nom}_km"] = round(float(dk[k]))
        H[f"point_mer_le_plus_proche_{nom}"] = ll(*k)
        H[f"point_cote_le_plus_proche_{nom}"] = ll(jy[k], jx[k])
    # largeur du Sumdan (rive nord → Méditerranée) par méridien
    sumdan = []
    for lon in range(0, 29, 2):
        x = int(g.px(lon, 0)[0])
        col = np.nonzero(mer[:, x])[0]
        cot = np.nonzero(oc[:, x] & (g.lats > 29.5))[0]
        if len(col) and len(cot):
            sumdan.append({"lon": lon, "rive_nord_lat": r1(g.lats[col.min()], 2), "cote_med_lat": r1(g.lats[cot.max()], 2),
                           "largeur_km": round(dist((lon, g.lats[col.min()]), (lon, g.lats[cot.max()])))})
    M["sumdan_largeur_par_meridien"] = sumdan

    # ---------------------------------------------------------------- lacs
    for k, L in enumerate(rel.lacs, start=1):
        m = rel.lac == k
        ys, xs = np.nonzero(m)
        c = L["cfg"]
        cy, cx = int(ys.mean()), int(xs.mean())
        M["lacs"][c["geo_id"]] = {
            "nom": c["nom"], "superficie_km2": round(float(A[m].sum())), "altitude_m": c["altitude_m"],
            "profondeur_max_m": round(float(c["altitude_m"] - rel.h[m].min())),
            "centre": ll(cy, cx),
            "emprise": {"lon_min": r1(g.lons[xs.min()], 2), "lon_max": r1(g.lons[xs.max()], 2),
                        "lat_min": r1(g.lats[ys.max()], 2), "lat_max": r1(g.lats[ys.min()], 2)},
            "longueur_O_E_km": round(dist((g.lons[xs.min()], g.lats[cy]), (g.lons[xs.max()], g.lats[cy]))),
            "largeur_N_S_km": round(dist((g.lons[cx], g.lats[ys.max()]), (g.lons[cx], g.lats[ys.min()]))),
        }

    # ---------------------------------------------------------------- chaînes
    for ax in rel.axes:
        ch = ax["cfg"]
        cle = ch["geo_id"] + ("" if ch.get("nom") else f" (segment {ch['points'][0][0]}, {ch['points'][0][1]})")
        e = {"nom": ch.get("nom"), "longueur_axe_km": round(longueur(ax["ligne"])),
             "extremites": [[r1(v, 2) for v in ax["ligne"][0]], [r1(v, 2) for v in ax["ligne"][-1]]],
             "points_parametres": ch["points"]}
        if ax["zone"] is not None:
            (y0, y1, x0, x1), pr, _ = ax["zone"]
            sub = rel.h[y0:y1, x0:x1]
            ok = (pr > 0.02) & rel.terre[y0:y1, x0:x1]
            if ok.any():
                i = np.argmax(np.where(ok, sub, -1e9))
                yy, xx = np.unravel_index(i, sub.shape)
                e["point_culminant"] = {"altitude_m": round(float(sub[yy, xx])), "position": ll(y0 + yy, x0 + xx)}
                cr = ok & (pr > 0.5)
                if cr.any():
                    e["altitude_mediane_crete_m"] = round(float(np.median(sub[cr])))
        M["chaines"][cle] = e

    # ---------------------------------------------------------------- fleuves dessinés
    for F in rel.fleuves:
        c = F["cfg"]
        tot = 0
        sources, bouches = [], []
        for L_ in F["lignes"]:
            tot += longueur(L_)
            sources.append([r1(L_[0][0], 2), r1(L_[0][1], 2)])
            bouches.append([r1(L_[-1][0], 2), r1(L_[-1][1], 2)])
        cle = c["geo_id"] or "affluent sans nom"
        e = M["fleuves"].setdefault(cle, {"noms": c["noms"], "longueur_dessinee_km": 0, "amont": [], "aval": []})
        e["longueur_dessinee_km"] += round(tot)
        e["amont"] += sources
        e["aval"] += bouches
        # source = extrémité amont la plus haute ; embouchure = extrémité aval la plus basse
        alt = lambda q: float(rel.h[int(np.clip(g.px(*q)[1], 0, g.H - 1)), int(np.clip(g.px(*q)[0], 0, g.W - 1))])
        e["source"] = max(e["amont"], key=alt)
        e["embouchure"] = min(e["aval"], key=alt)
        if "reel" in c:
            e["trace_reel"] = c["reel"]
        else:
            L0 = max(F["lignes"], key=len)
            pas = max(1, len(L0) // 40)
            e["trace_dessine"] = [[r1(a, 3), r1(b, 3)] for a, b in list(L0[::pas]) + [L0[-1]]]

    # ---------------------------------------------------------------- distances clés
    pos = {d["geo_id"]: d["pos"] for d in p.get("detroits_et_debouches", []) + p.get("deltas", [])}
    lac_c = {k: v["centre"] for k, v in M["lacs"].items()}
    D = M["distances"]
    D["Mopámà (centre) → delta du Mopámà"] = round(dist(lac_c["GEO_LAC_MOPAMA"], pos["GEO_DLT_MOPAMA"]))
    D["Tùmázì (centre) → Mopámà (centre)"] = round(dist(lac_c["GEO_LAC_TUMAZI"], lac_c["GEO_LAC_MOPAMA"]))
    D["Akhtir (centre) → Ḥawqil"] = round(dist(lac_c["GEO_LAC_AKHTIR"], pos["GEO_DET_HAWQIL"]))
    D["Abnīqa → Šafāqil (embouchures)"] = round(dist(pos["GEO_DET_ABNIQA"], pos["GEO_DET_SAFAQIL_PASSE"]))
    D["Hlom-khetal → Imekh-stom"] = round(dist(pos["GEO_DET_HLOMKHETAL"], pos["GEO_DET_IMEKHSTOM"]))
    D["Hlom-khetal → Abnīqa (extrémités O-E)"] = round(dist(pos["GEO_DET_HLOMKHETAL"], pos["GEO_DET_ABNIQA"]))
    D["Khreth-na-Serek → Hlom-khetal"] = round(dist(pos["GEO_DET_KHRETHNASEREK"], pos["GEO_DET_HLOMKHETAL"]))
    D["Imekh-stom → ria Tawālmaz (vol d'oiseau, RT_016)"] = round(dist(pos["GEO_DET_IMEKHSTOM"], pos["GEO_EST_TAWALMAZ"]))
    D["ria Tawālmaz → Abnīqa (vol d'oiseau, RT_023)"] = round(dist(pos["GEO_EST_TAWALMAZ"], pos["GEO_DET_ABNIQA"]))
    D["Hlom-khetal → Ḥawqil (vol d'oiseau)"] = round(dist(pos["GEO_DET_HLOMKHETAL"], pos["GEO_DET_HAWQIL"]))
    D["mer → Atlantique, plus court portage (RT_027)"] = M["halakhel"]["distance_min_atlantique_km"]
    D["mer → Méditerranée, plus court portage (§VI.1.2)"] = M["halakhel"]["distance_min_mediterranee_km"]
    D["mer → mer Rouge, plus courte caravane (§VI.1.2)"] = M["halakhel"]["distance_min_mer_rouge_km"]
    hk = next(c for c in p["chaines"] if c["geo_id"] == "GEO_ORO_URUMATI_HALEKH")["points"][0]
    D["Khlōr-Naw → extrémité O de halekh (RT_066)"] = round(dist(p["archipels"][0]["ile_principale"]["pos"], hk[:2]))
    D["Mopámà (centre) → nœud !Okheti (longueur du versant SO de lóngò)"] = round(dist(lac_c["GEO_LAC_MOPAMA"], (0.75, 23.75)))
    D["Tùmázì (centre) → |'Ara-Sukhì"] = round(dist(lac_c["GEO_LAC_TUMAZI"], (17.8, 20.3)))
    D["Tùmázì (centre) → plateaux de qoyra (38,0° E ; 9,5° N)"] = round(dist(lac_c["GEO_LAC_TUMAZI"], (38.0, 9.5)))
    # interfluve : de la côte E de la mer au Nil (bras d'Abnīqa)
    ab = next(f for f in p["fleuves"] if f["geo_id"] == "GEO_FLV_ABNUHIL_ABNIQA")["trace"]
    D["interfluve oriental (diffluence → côte E de la mer)"] = round(longueur(ab))
    sk = next(a for a in p["archipels"] if a["geo_id"] == "GEO_ARC_STAURKHLOR")
    kn = sk["ile_principale"]["pos"]
    d_at, (jy, jx) = distance_transform_edt(~(rel.terre & (LON > -18)), return_indices=True)
    x, y = (int(v) for v in g.px(*kn))
    D["Khlōr-Naw (Staur-Khlōr) → côte continentale la plus proche"] = round(float(d_at[y, x] * g.km_px[y]))

    # ---------------------------------------------------------------- fondu sud
    for lon in range(9, 46, 3):
        x = int(g.px(lon, 0)[0])
        col = rel.fondu[:, x]
        plein = np.nonzero(col >= 0.99)[0]
        moitie = np.nonzero(col >= 0.5)[0]
        M["fondu_sud"][str(lon)] = {"opaque_jusqu_a_lat": r1(g.lats[plein.max()], 2) if len(plein) else None,
                                    "moitie_a_lat": r1(g.lats[moitie.max()], 2) if len(moitie) else None}

    # ---------------------------------------------------------------- pluie aux points de calibration
    from carto.climat import Climat
    cl = Climat(rel, p, log=lambda m: None)
    M["pluie_calibration"] = cl.calibration
    M["climat"] = mesures_climat(rel, p, cl)
    M["statistiques"] = json.load(open(os.path.join(SIG, "beliet_statistiques.json"), encoding="utf-8"))

    # cols : altitude relevée sur la carte au point du col
    M["cols"] = []
    for c in p["cols"]:
        x, y = (int(v) for v in g.px(*c["pos"]))
        M["cols"].append(dict(c, altitude_carte_m=round(float(rel.h[y, x]))))
    M["positions"] = positions(p, M)
    json.dump(M, open(os.path.join(SIG, "beliet_mesures.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ecrire_md(M)
    print("mesures écrites")


def mesures_climat(rel, p, cl):
    """Hiver |'Arin : seuils par latitude, vérification des affirmations du §III, faciès par chaîne."""
    from carto.climat import FACIES, amplitude_annuelle, hiver, seuils_facies, temperature, temperature_hiver
    g = rel.g
    cfg = p.get("climat_hiver", {})
    E = p.get("etages", {})
    T_ann = temperature(rel)
    P = cl.pluie()
    hv = hiver(rel, T_ann, P, p, log=lambda m: None)
    sb, sg = seuils_facies(cfg)
    Tl = lambda lat, h: 27.5 - 0.45 * max(abs(lat) - 12, 0) - 6.0 * h / 1000
    Tw = lambda lat, h: float(temperature_hiver(Tl(lat, h), lat, cfg))
    ampl_j = lambda humide: cfg.get("amplitude_jour_humide", 8.0) if humide else cfg.get("amplitude_jour_aride", 12.0)
    alt_pour = lambda lat, T_cible, f: round(1000 * (f(lat, 0) - T_cible) / 6.0)
    lat_ref = E.get("latitude_reference", 22.5)
    A_ref = float(amplitude_annuelle(np.float32(lat_ref), cfg))
    Tgs = lambda lat, h: Tl(lat, h) + float(amplitude_annuelle(np.float32(lat), cfg)) / 3
    seuil_gs = lambda alt: Tgs(lat_ref, alt)
    C = {"modele": {
        "temperature_annuelle": "T = 27,5 − 0,45 × max(|lat| − 12, 0) − 6,0 × altitude (km)",
        "amplitude_ete_hiver": "A = 4 + 0,45 × (|lat| − 8), min. 2 °C",
        "temperature_hiver": "Tw = T − A/2 − 3 (refroidissement |'Arin, §III cause 3)",
        "minimum_nocturne": "Tn = Tw − 8 (humide) à − 12 (aride, < 100 mm)",
        "seuil_hiver_blanc_tw_c": round(sb, 2), "seuil_hiver_gris_tw_c": round(sg, 2),
        "etages": "température de saison de végétation T + A/3 ; seuils calés sur 800 / 2 400 / 3 600 m à 22,5° N",
        "glaciers": f"T ≤ {E.get('glacier_t_annuelle_c', -5.0)} °C (actifs) ; T ≤ {E.get('glacier_relictuel_t_annuelle_c', -2.5)} °C sur halekh (relictuels)"}}
    lignes = []
    for lat in (8, 10, 13, 15, 17, 20, 22.5, 25, 28, 30, 33):
        f_ = lambda la, h: Tw(la, h)
        lignes.append({"latitude": lat,
                       "hiver_gris_des_m": max(0, alt_pour(lat, sg, f_)), "hiver_blanc_des_m": max(0, alt_pour(lat, sb, f_)),
                       "foret_montagne_des_m": max(0, alt_pour(lat, seuil_gs(800), Tgs)),
                       "prairie_altitude_des_m": max(0, alt_pour(lat, seuil_gs(2400), Tgs)),
                       "periglaciaire_des_m": max(0, alt_pour(lat, seuil_gs(3600), Tgs)),
                       "glacier_actif_des_m": alt_pour(lat, E.get("glacier_t_annuelle_c", -5.0), Tl),
                       "glacier_relictuel_des_m": alt_pour(lat, E.get("glacier_relictuel_t_annuelle_c", -2.5), Tl)})
    C["limites_par_latitude"] = lignes
    # affirmations du §III et valeurs du modèle
    V = []
    def ajoute(texte, calcul, verdict):
        V.append({"affirmation": texte, "modele": calcul, "verdict": verdict})
    ajoute("§III |'Arin-sukhì : « −10/−15 °C (2 500 m) »",
           f"halekh (22,5° N) : Tw {Tw(22.5, 2500):.1f} °C, nuits {Tw(22.5, 2500) - ampl_j(True):.1f} à {Tw(22.5, 2500) - ampl_j(False):.1f} °C ; "
           f"k'ara orientale (13,3° N) : Tw {Tw(13.3, 2500):.1f} °C, nuits {Tw(13.3, 2500) - ampl_j(True):.1f} °C",
           "cohérent au nord (avec inversions) ; trop froid au sud")
    ajoute("§III |'Arin-sukhì : « gelées fréquentes < 1 500 m »",
           f"nuits à 1 500 m : {Tw(22.5, 1500) - ampl_j(True):.1f} °C (22,5° N) ; {Tw(13.3, 1500) - ampl_j(True):.1f} °C (13,3° N)",
           "cohérent au nord ; faux au sud de ~17° N")
    ajoute("§III |'Arin-sukhì : « neige permanente dès 1 000 m (versants exposés N) »",
           f"Tw à 1 000 m : {Tw(22.5, 1000):.1f} °C (22,5° N), {Tw(25, 1000):.1f} °C (25° N) ; manteau stable dès "
           f"{alt_pour(22.5, sb, Tw)} m (22,5° N), {alt_pour(17, sb, Tw)} m (17° N), {alt_pour(13, sb, Tw)} m (13° N)",
           "contradictoire avec la matrice (Gris 800-2 400 m) et physiquement faux : neige épisodique dès ~1 500 m (versants N du nord), manteau stable dès 2 400 m (22,5° N)")
    ajoute("§III matrice : « Hiver Gris 800-2 400 m », « Hiver Blanc > 2 400 m »",
           "exact à 22,5° N ; Blanc dès " + ", ".join(f"{l['hiver_blanc_des_m']} m ({l['latitude']}° N)" for l in lignes if l["latitude"] in (13, 17, 25, 30)),
           "cohérent comme valeur de référence ; à préciser : gradient avec la latitude")
    ajoute("§III économie : « Mer Halakhel gelée en bordures »",
           f"rive à 28° N : Tw {Tw(28, 0):.1f} °C, nuits {Tw(28, 0) - ampl_j(False):.1f} °C",
           "gel de la mer impossible (eau salée, Tw > 10 °C) ; seules des gelées nocturnes givrent les rives : remplacer par brouillards d'advection (Hiver de Vapeur, déjà au §III)")
    ajoute("§I halekh : « glaciers relictuels > 3 500 m »",
           f"T annuelle à 3 500 m (22,4° N) : {Tl(22.4, 3500):.1f} °C ; glace relictuelle possible dès {alt_pour(22.4, E.get('glacier_relictuel_t_annuelle_c', -2.5), Tl)} m",
           "relever à > 4 100 m (cirques sommitaux exposés N)")
    ajoute("§I k'ara : « dernier glacier équatorial (> 4 800 m) »",
           f"glacier actif dès {alt_pour(20.3, E.get('glacier_t_annuelle_c', -5.0), Tl)} m à 20,3° N (|'Ara-Sukhì, 5 350 m)",
           "cohérent")
    ajoute("§I qoyra : sommets > 4 600 m, aucun glacier mentionné",
           f"T annuelle au sommet (4 673 m, 13,2° N) : {Tl(13.2, 4673):.1f} °C ; Hiver Blanc dès {alt_pour(13.2, sb, Tw)} m",
           "cohérent : neige d'hiver sur les sommets, pas de glacier ; k'ara porte bien le « dernier glacier »")
    ajoute("§II Zone II : étages 800 / 2 400 / 3 600 m",
           "à 22,5° N : exact ; à 13° N : forêt dès " + str(next(l for l in lignes if l["latitude"] == 13)["foret_montagne_des_m"]) +
           " m, prairie dès " + str(next(l for l in lignes if l["latitude"] == 13)["prairie_altitude_des_m"]) + " m",
           "à préciser : étages de référence (nord de la cordillère), relevés vers le sud")
    C["verification_III"] = V
    # faciès par chaîne (emprise de la chaîne, profil > 0,25)
    A = g.aire_km2()
    par_chaine = {}
    for ax in rel.axes:
        ch = ax["cfg"]
        if ax["zone"] is None or not ch["geo_id"].startswith(("GEO_ORO_URUMATI", "GEO_ORO_OKHETI")):
            continue
        (y0, y1, x0, x1), pr, _ = ax["zone"]
        m = (pr > 0.25) & rel.terre[y0:y1, x0:x1]
        F = hv["facies"][y0:y1, x0:x1][m]
        a = A[y0:y1, x0:x1][m]
        tot = a.sum()
        cle = ch.get("nom") or f"{ch['geo_id']} (segment {ch['points'][0][0]}, {ch['points'][0][1]})"
        pts = np.array(ch["points"])
        e = {"latitudes": [round(float(pts[0][1]), 2), round(float(pts[-1][1]), 2)],
             "hiver_blanc_des_m": [alt_pour(float(pts[0][1]), sb, Tw), alt_pour(float(pts[-1][1]), sb, Tw)],
             "hiver_gris_des_m": [max(0, alt_pour(float(pts[0][1]), sg, Tw)), max(0, alt_pour(float(pts[-1][1]), sg, Tw))],
             "part_surface_pct": {FACIES[c][0]: round(float(100 * a[F == c].sum() / tot), 1) for c in FACIES if (F == c).any()}}
        if cle in par_chaine:
            continue
        par_chaine[cle] = e
    C["facies_par_chaine"] = par_chaine
    return C


def positions(p, M):
    """Positions paramétrées (toutes [PROPOSITION]) : ce qu'il faut reporter dans le corpus."""
    P = []
    def add(geo_id, nom, nature, coords, note=""):
        P.append({"geo_id": geo_id, "nom": nom, "nature": nature, "coordonnees": coords, "note": note})
    for d in p.get("detroits_et_debouches", []):
        add(d["geo_id"], d["nom"], "point (détroit / débouché)", d["pos"])
    for d in p.get("deltas", []):
        add(d["geo_id"], d["nom"], "point (delta / estuaire)", d["pos"])
    for d in p.get("eaux_exterieures", []):
        add(d["geo_id"], d["nom"], "point d'étiquette (mer, golfe)", d["pos"])
    for m in p.get("massifs", []):
        add(m["geo_id"], m["nom"], "point (massif, site)", m["centre"])
    for r in p.get("regions", []):
        add(r["geo_id"], r["nom"], "point d'étiquette (région)", r["pos"])
    for a in p.get("archipels", []):
        if "zone" in a:
            add(a["geo_id"], a["nom"], "zone (archipel)", a["zone"], "étiquette " + str(a.get("pos_etiquette")))
        if "ilots" in a:
            add(a["geo_id"], a["nom"], "îlots (archipel)", a["ilots"], "étiquette " + str(a.get("pos_etiquette")))
        if "ile_principale" in a:
            i = a["ile_principale"]
            add(i["geo_id"], i["nom"], "point (île principale)", i["pos"])
    for b in p["halakhel"]["bassins"]:
        add("GEO_MER_HALAKHEL", b["nom"], "contour-enveloppe (le rivage réel est découpé par le relief)", b["contour"])
    for c in p["halakhel"].get("chenaux", []):
        add(None, c["nom"], f"chenal {c['largeur_km']}→{c.get('largeur_fin_km', c['largeur_km'])} km", c["trace"])
    add("GEO_MER_HALAKHEL", "îles volcaniques et îles de passe", "points [lon, lat(, haut., rayon)]", p["halakhel"]["iles_volcaniques"])
    for z in p["halakhel"].get("rivages_escarpes", []):
        add(None, z["nom"], f"rivage escarpé (v0.5) : centre, rayon {z['rayon_km']} km, dénivelé {z['hauteur_m']} m", z["centre"])
    for d in p.get("plaines_deltaiques", []):
        add(None, d["nom"], "plaine deltaïque basse (v0.5) : contour", d["contour"])
    for c in p.get("canyons", []):
        add(c.get("geo_id"), c["nom"], f"canyon (v0.5.2) : thalweg amont → aval, profondeur ≤ {c['profondeur_m']} m", c["trace"])
    for L in p["lacs"]:
        add(L["geo_id"], L["nom"], "contour dessiné (ajusté à la superficie canonique)", L["contour"],
            "centre mesuré " + str(M["lacs"].get(L["geo_id"], {}).get("centre")))
    for ch in p["chaines"]:
        add(ch["geo_id"], ch.get("nom") or "segment / contrefort sans nom", "ligne de crête [lon, lat, crête m, demi-largeur km]",
            ch["points"], f"socle {ch['socle_m']} m / {ch.get('socle_km')} km" if ch.get("socle_m") else "")
    for f in p["fleuves"]:
        nom = " / ".join(n for n in f["noms"] if n) or "sans nom"
        if "trace" in f:
            if f.get("suivre_relief"):
                add(f["geo_id"], nom, "tracé indicatif (couloir) ; cours dessiné : clé fleuves.trace_dessine du JSON", f["trace"])
            else:
                add(f["geo_id"], nom, "tracé amont → aval", f["trace"])
        for k, br in enumerate(f.get("bras", [])):
            add(f["geo_id"], f"{nom} — bras {k + 1}", "bras ou chenal, amont → aval", br)
        if "reel" in f:
            add(f["geo_id"], nom, "tracé réel Natural Earth", f["reel"])
    for e in p.get("ecretements", []):
        add(None, e["nom"], f"écrêtement (seuil {e['seuil_m']} m, facteur {e['facteur']})", e["zone"])
    for i, e in enumerate(p.get("ergs", [])):
        add(None, f"erg n° {i + 1}", "zone de désert de sable", e)
    return P


def echapper_tableaux(txt):
    """Échappe les « | » des noms (||Urumati, |Na-madikh…) dans les lignes de tableau Markdown."""
    import re
    out = []
    for ligne in txt.split("\n"):
        if ligne.startswith("|") and not re.fullmatch(r"\|[-| :]+\|", ligne):
            car = list(ligne)
            for i, ch in enumerate(car):
                if ch != "|" or (i and car[i - 1] == "\\"):
                    continue
                g = i == 0 or ligne[i - 1] == " "
                d = i == len(ligne) - 1 or ligne[i + 1] == " "
                if not (g and d):
                    car[i] = "\\|"
            ligne = "".join(car)
        out.append(ligne)
    return "\n".join(out)


def ecrire_md(M):
    L = ["<!-- MESURES:DEBUT — section régénérée par outils/mesures_corpus.py ; ne pas éditer à la main -->", "",
         f"### Mesures de la carte v{M['version']}", "",
         "Toutes les valeurs sont mesurées sur la carte générée. Fichier complet : `carte/sig/beliet_mesures.json`.", ""]
    H = M["halakhel"]
    e = H["emprise"]
    L += ["#### Mer Halakhel", "",
          "| Grandeur | Valeur |", "|---|---|",
          f"| Superficie | {H['superficie_km2']:,} km² |".replace(",", " "),
          f"| Emprise | {e['lon_min']}° à {e['lon_max']}° E ; {e['lat_min']}° à {e['lat_max']}° N |",
          f"| Longueur O-E | {H['longueur_O_E_km']} km |",
          f"| Niveau / profondeur max | {H['niveau_m']} m / {H['profondeur_max_m']} m |",
          f"| Îles | {H['iles']} |",
          f"| Distance min. à l'Atlantique | {H['distance_min_atlantique_km']} km (mer {H['point_mer_le_plus_proche_atlantique']} → côte {H['point_cote_le_plus_proche_atlantique']}) |",
          f"| Distance min. à la Méditerranée | {H['distance_min_mediterranee_km']} km (mer {H['point_mer_le_plus_proche_mediterranee']} → côte {H['point_cote_le_plus_proche_mediterranee']}) |",
          f"| Distance min. à la mer Rouge | {H['distance_min_mer_rouge_km']} km |", "",
          "Profil par méridien :", "", "| Longitude | Rive nord | Rive sud | Largeur | Eau sur le méridien |", "|---|---|---|---|---|"]
    for r in H["profil_par_meridien"]:
        L.append(f"| {r['lon']}° | {r['rive_nord_lat']}° N | {r['rive_sud_lat']}° N | {r['largeur_km']} km | {r['eau_km_sur_le_meridien']} km |")
    L += ["", "Largeur du Sumdan (rive nord → Méditerranée) :", "", "| Longitude | Rive nord | Côte | Largeur |", "|---|---|---|---|"]
    for r in M["sumdan_largeur_par_meridien"]:
        L.append(f"| {r['lon']}° | {r['rive_nord_lat']}° N | {r['cote_med_lat']}° N | {r['largeur_km']} km |")
    L += ["", "#### Lacs", "", "| Lac | Superficie | Altitude | Prof. max | Centre | Emprise | O-E × N-S |", "|---|---|---|---|---|---|---|"]
    for k, v in M["lacs"].items():
        e = v["emprise"]
        L.append(f"| {v['nom']} (`{k}`) | {v['superficie_km2']:,} km² | {v['altitude_m']} m | {v['profondeur_max_m']} m | {v['centre']} | "
                 f"{e['lon_min']}-{e['lon_max']}° E, {e['lat_min']}-{e['lat_max']}° N | {v['longueur_O_E_km']} × {v['largeur_N_S_km']} km |".replace(",", " ", 1))
    L += ["", "#### Chaînes (lignes de crête)", "", "| Chaîne | Longueur d'axe | Point culminant | Médiane de crête | Extrémités |", "|---|---|---|---|---|"]
    for k, v in M["chaines"].items():
        pc = v.get("point_culminant", {})
        L.append(f"| {v['nom'] or k} | {v['longueur_axe_km']} km | {pc.get('altitude_m', '—')} m à {pc.get('position', '—')} | "
                 f"{v.get('altitude_mediane_crete_m', '—')} m | {v['extremites'][0]} → {v['extremites'][1]} |")
    L += ["", "#### Fleuves dessinés", "", "| Fleuve | Longueur dessinée | Amont | Aval |", "|---|---|---|---|"]
    for k, v in M["fleuves"].items():
        nom = " / ".join(n for n in v["noms"] if n) or k
        L.append(f"| {nom} (`{k}`) | {v['longueur_dessinee_km']} km | {v['source']} | {v['embouchure']} |")
    L += ["", "#### Distances", "", "| Trajet | Distance |", "|---|---|"]
    for k, v in M["distances"].items():
        L.append(f"| {k} | {v} km |")
    L += ["", "#### Limite sud estompée", "", "| Longitude | Opaque jusqu'à | Moitié estompée à |", "|---|---|---|"]
    for k, v in M["fondu_sud"].items():
        L.append(f"| {k}° E | {v['opaque_jusqu_a_lat']}° N | {v['moitie_a_lat']}° N |")
    L += ["", "#### Précipitations aux points de calibration", "", "| Lieu | Position | Cible | Modèle |", "|---|---|---|---|"]
    for r in M["pluie_calibration"]:
        L.append(f"| {r['lieu']} | {r['pos']} | {r['cible_mm']} mm | {r['modele_mm']} mm |")
    S = M["statistiques"]
    L += ["", "#### Surfaces", "", f"- Terres émergées (zone estompée pondérée) : {S['terres_emergees_beliet_km2']:,} km²".replace(",", " "),
          f"- Point culminant : {S['altitude_max_m']} m", "", "| Milieu | Surface |", "|---|---|"]
    for k, v in sorted(S["milieux_km2"].items(), key=lambda kv: -kv[1]):
        L.append(f"| `{k}` | {v:,} km² |".replace(",", " "))
    C = M["climat"]
    L += ["", "#### Climat : hivers du |'Arin et étages (modèle v0.4)", "",
          "Modèle :", ""] + [f"- {k} : {v}" for k, v in C["modele"].items()] + ["",
          "Limites par latitude (altitude du bas de chaque faciès ou étage) :", "",
          "| Latitude | Hiver Gris dès | Hiver Blanc dès | Forêt de montagne dès | Prairie dès | Périglaciaire dès | Glacier actif dès | Glacier relictuel dès |",
          "|---|---|---|---|---|---|---|---|"]
    for l in C["limites_par_latitude"]:
        L.append(f"| {l['latitude']}° N | {l['hiver_gris_des_m']} m | {l['hiver_blanc_des_m']} m | {l['foret_montagne_des_m']} m | "
                 f"{l['prairie_altitude_des_m']} m | {l['periglaciaire_des_m']} m | {l['glacier_actif_des_m']} m | {l['glacier_relictuel_des_m']} m |")
    L += ["", "Affirmations du Géosystème confrontées au modèle :", "", "| Affirmation | Modèle | Verdict |", "|---|---|---|"]
    for v in C["verification_III"]:
        L.append(f"| {v['affirmation']} | {v['modele']} | {v['verdict']} |")
    L += ["", "Faciès |'Arin par chaîne (part de la surface de la chaîne) :", "",
          "| Chaîne | Latitudes (extrémités) | Blanc dès | Gris dès | Blanc | Gris | Jaune | Hors |'Arin |", "|---|---|---|---|---|---|---|---|---|"]
    for k, v in C["facies_par_chaine"].items():
        f = v["part_surface_pct"]
        L.append(f"| {k} | {v['latitudes'][0]}° → {v['latitudes'][1]}° N | {v['hiver_blanc_des_m'][0]} → {v['hiver_blanc_des_m'][1]} m | "
                 f"{v['hiver_gris_des_m'][0]} → {v['hiver_gris_des_m'][1]} m | {f.get('hiver_blanc', 0)} % | {f.get('hiver_gris', 0)} % | "
                 f"{f.get('hiver_jaune', 0)} % | {f.get('hors_arin', 0)} % |")
    L += ["", "#### Les 48 cols", "",
          "Altitude canonique imposée au relief ; « crête d'origine » = altitude de la ligne de crête avant entaille ou selle.", "",
          "| geo_id | Nom | Groupe (interface) | Chaîne | Position [lon, lat] | Altitude | Crête d'origine | Statut | Routes |",
          "|---|---|---|---|---|---|---|---|---|"]
    for c in M["cols"]:
        L.append(f"| `{c['geo_id']}` | {c['nom']} | {c['groupe']} | {c['chaine']} | {c['pos']} | {c['altitude_m']} m "
                 f"(carte {c['altitude_carte_m']} m) | {c['altitude_crete_avant_entaille_m']} m | {c['statut_passage']} | "
                 f"{', '.join(c['routes']) or '—'} |")
    L += ["", "#### Positions paramétrées (toutes [PROPOSITION])", "",
          "Coordonnées [longitude, latitude] en degrés décimaux WGS84. Liste complète et lisible par machine : clé `positions` du JSON.", "",
          "| geo_id | Nom | Nature | Coordonnées | Note |", "|---|---|---|---|---|"]
    for e in M["positions"]:
        c = json.dumps(e["coordonnees"], ensure_ascii=False)
        if len(c) > 260:
            c = c[:257] + "…"
        L.append(f"| `{e['geo_id'] or '—'}` | {e['nom']} | {e['nature']} | {c} | {e['note']} |")
    L += ["", "<!-- MESURES:FIN -->"]
    bloc = "\n".join(L)
    chemin = os.path.join(RACINE, "ALIGNEMENT_CORPUS.md")
    txt = open(chemin, encoding="utf-8").read() if os.path.exists(chemin) else "<!-- MESURES:DEBUT -->\n<!-- MESURES:FIN -->\n"
    i = txt.index("<!-- MESURES:DEBUT")
    j = txt.index("<!-- MESURES:FIN -->") + len("<!-- MESURES:FIN -->")
    open(chemin, "w", encoding="utf-8").write(echapper_tableaux(txt[:i] + bloc + txt[j:]))


if __name__ == "__main__":
    main()
