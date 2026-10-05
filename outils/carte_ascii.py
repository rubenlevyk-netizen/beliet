#!/usr/bin/env python3
"""Carte ASCII du Beliet : version texte, légère et complète, de la carte générée.

Usage (après outils/generer_carte.py et outils/mesures_corpus.py) :
    python3 outils/carte_ascii.py
Sortie : carte/beliet_carte_ascii.md
"""
import json
import os
import pickle
import sys

import numpy as np
import rasterio
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from carto.sources import RACINE, CACHE                    # noqa: E402
from generer_carte import empreinte, charger_cols          # noqa: E402

PAS = 0.5                          # degrés par case, en longitude comme en latitude
LON0, LON1 = -18.0, 52.0
LAT1, LAT0 = 38.0, -2.0

RELIEF = [(-1e9, 0, "_"), (0, 300, "."), (300, 700, ":"), (700, 1200, "+"), (1200, 1800, "n"),
          (1800, 2600, "m"), (2600, 3600, "M"), (3600, 1e9, "A")]
MILIEUX = {
    "desert_pierreux": "d", "desert_sableux": "s", "dunes_littorales": "u", "oasis": "O", "steppe_piemont": "-",
    "fourre_cotier_sec": "f", "depression_saline": "x", "cote_desertique": "c", "recif_corallien": "r",
    "littoral_rocheux": "l", "plaine_alluviale": "a", "foret_montagne": "M", "prairie_altitude": "p",
    "zone_periglaciaire": "g", "glacier": "*", "foret_tropicale_humide": "T", "herbage_arbore": "h",
    "foret_berge": "b", "foret_maree": "v", "zone_humide_lacustre": "w", "eaux_lacustres": "o", "ile_aride": "i",
}


def main():
    p = yaml.safe_load(open(os.path.join(RACINE, "donnees", "parametres_carte.yaml"), encoding="utf-8"))
    p["cols"] = charger_cols()
    rel = pickle.load(open(os.path.join(CACHE, f"relief_{empreinte(p)}.pkl"), "rb"))
    g = rel.g
    codes = {k: v for k, v in json.load(open(os.path.join(RACINE, "carte", "sig", "beliet_milieux_codes.json"),
                                            encoding="utf-8")).items() if isinstance(v, dict)}
    mil = rasterio.open(os.path.join(RACINE, "carte", "sig", "beliet_milieux.tif")).read(1)
    M = json.load(open(os.path.join(RACINE, "carte", "sig", "beliet_mesures.json"), encoding="utf-8"))
    reg = {e["geo_id"]: e for e in json.load(open(os.path.join(RACINE, "references", "GEOSYSTEME_REGISTRE.v1.json"),
                                                   encoding="utf-8"))["entrees"]}

    nx = int(round((LON1 - LON0) / PAS))
    ny = int(round((LAT1 - LAT0) / PAS))
    lon_c = LON0 + PAS * (np.arange(nx) + 0.5)
    lat_c = LAT1 - PAS * (np.arange(ny) + 0.5)
    xb = [int(np.clip(g.px(LON0 + PAS * i, 0)[0], 0, g.W)) for i in range(nx + 1)]
    yb = [int(np.clip(g.px(0, LAT1 - PAS * j)[1], 0, g.H)) for j in range(ny + 1)]

    from carto.climat import Climat, hiver, temperature
    cl = Climat(rel, p, log=lambda m: None)
    pluie = cl.pluie()
    hv = hiver(rel, temperature(rel), pluie, p, log=lambda m: None)
    relief = np.full((ny, nx), " ", object)
    c_pluie = np.full((ny, nx), " ", object)
    c_hiver = np.full((ny, nx), " ", object)
    milieu = np.full((ny, nx), " ", object)
    terre_case = np.zeros((ny, nx), bool)
    inv = {int(k): v["code"] for k, v in codes.items()}
    for j in range(ny):
        for i in range(nx):
            sl = (slice(yb[j], max(yb[j] + 1, yb[j + 1])), slice(xb[i], max(xb[i] + 1, xb[i + 1])))
            n = rel.h[sl].size
            if n == 0:
                continue
            visible = rel.fondu[sl] >= 0.5
            oc = (rel.ocean[sl]).mean()
            hk = (rel.mer[sl]).mean()
            lc = (rel.lac[sl] > 0).mean()
            te = (rel.terre[sl] & visible).mean()
            if hk >= 0.4:
                c = "="
            elif lc >= 0.3:
                c = "o"
            elif te >= 0.4:
                h = np.percentile(rel.h[sl][rel.terre[sl]], 90)
                c = next(s for a, b, s in RELIEF if a <= h < b)
                terre_case[j, i] = True
            elif oc >= 0.5:
                c = "~"
            else:
                c = " "
            relief[j, i] = c
            if c in "=~o ":
                milieu[j, i] = c
            else:
                v = mil[sl][rel.terre[sl]]
                v = v[v < 250]
                milieu[j, i] = MILIEUX.get(inv.get(int(np.bincount(v).argmax()), ""), "?") if v.size else "?"
            if c in "~o ":
                c_pluie[j, i] = c_hiver[j, i] = c
            elif c == "=":
                c_pluie[j, i] = "="
                c_hiver[j, i] = "V"
            else:
                pm = float(np.median(pluie[sl][rel.terre[sl]]))
                c_pluie[j, i] = str(sum(pm >= b for b in (50, 100, 250, 500, 800, 1200, 1600, 2200, 3000)))
                fv = hv["facies"][sl][rel.terre[sl]]
                c_hiver[j, i] = ".BGJVP"[int(np.bincount(fv, minlength=6).argmax())]

    def case(lon, lat):
        i = int((lon - LON0) // PAS)
        j = int((LAT1 - lat) // PAS)
        return (j, i) if 0 <= i < nx and 0 <= j < ny else None

    # surimpressions de la carte physique : fleuves nommés, cols, détroits et deltas, sommets
    phys = relief.copy()
    for F in rel.fleuves:
        for c in F["lignes"]:
            for lo, la in c:
                k = case(lo, la)
                if k and phys[k] not in "=~o ":
                    phys[k] = "w"
    for c in p["cols"]:
        k = case(*c["pos"])
        if k:
            phys[k] = "X"
    for d in p.get("detroits_et_debouches", []) + p.get("deltas", []):
        k = case(*d["pos"])
        if k:
            phys[k] = "#"
    for cle, ch in M["chaines"].items():
        pc = ch.get("point_culminant")
        if pc and ch.get("nom"):
            k = case(*pc["position"])
            if k:
                phys[k] = "^"

    def grille(arr, titre):
        L = [titre, "", "```"]
        t1 = [" "] * nx
        t2 = [" "] * nx
        for i in range(nx):
            lo = LON0 + PAS * i
            if abs(lo / 10 - round(lo / 10)) < 1e-9:
                s = f"{int(lo)}"
                for k_, ch in enumerate(s):
                    if i + k_ < nx:
                        t1[i + k_] = ch
                t2[i] = "|"
            elif abs(lo / 5 - round(lo / 5)) < 1e-9:
                t2[i] = "'"
        L.append("        " + "".join(t1))
        L.append("        " + "".join(t2))
        for j in range(ny):
            la = LAT1 - PAS * j
            tag = f"{la:6.1f}" if abs(la - round(la)) < 1e-9 and int(round(la)) % 2 == 0 else "      "
            L.append(f"{tag} |" + "".join(arr[j]) + "|")
        L.append("        " + "".join(t2))
        L.append("        " + "".join(t1))
        L.append("```")
        return L

    nom_reg = lambda gid, d="": (reg.get(gid, {}).get("noms") or [{}])[0].get("forme") or d
    out = ["# Carte ASCII du Beliet (v" + M["version"] + ")", "",
           "Version texte de la carte générée, pour un usage sans image : corpus, agents, recherche de positions.",
           "Elle complète la carte visuelle et ne la remplace pas. Elle est régénérée par `python3 outils/carte_ascii.py`.", "",
           "## Lecture", "",
           f"- **Grille** : projection équirectangulaire, une case = {PAS}° de longitude × {PAS}° de latitude "
           f"(≈ 55 km × 55 km à l'équateur, ≈ 45 km × 55 km à 35° N).",
           f"- **Emprise** : {LON0}° à {LON1}° de longitude ; {LAT1}° N à {LAT0}° de latitude. {nx} colonnes × {ny} lignes.",
           "- **Contenu** : 1. relief et eaux ; 2. milieux ; 3. climat (précipitations, hivers du |'Arin) ; 4. répertoire des lieux ; 5. cols ; 6. façades ; 7. lieux et routes du corpus.",
           "- **Repères** : en haut et en bas, la longitude (`|` tous les 10°, `'` tous les 5°) ; à gauche, la latitude du "
           "bord supérieur de la ligne (toutes les 2°).",
           "- **Retrouver une case** : colonne = (longitude + 18) ÷ 0,5 ; ligne = (38 − latitude) ÷ 0,5, en comptant à partir de 0.",
           "- **Case** : altitude = 90e centile des terres de la case ; milieu = milieu majoritaire ; eau quand elle couvre "
           "≥ 40 % (mer Halakhel), ≥ 30 % (lac) ou ≥ 50 % (océan).",
           "- Le Sud estompé (au-delà de la limite du Beliet) et les terres hors Beliet restent en blanc.", ""]
    out += ["## 1. Relief et eaux", "",
            "| Signe | Sens | Signe | Sens |", "|---|---|---|---|",
            "| `~` | océan, mers extérieures | `=` | mer Halakhel |",
            "| `o` | lac (Tùmázì, Akhtir, Mopámà) | `w` | fleuve nommé |",
            "| `_` | terre sous le niveau de la mer | `.` | 0-300 m |",
            "| `:` | 300-700 m | `+` | 700-1 200 m |",
            "| `n` | 1 200-1 800 m | `m` | 1 800-2 600 m |",
            "| `M` | 2 600-3 600 m | `A` | > 3 600 m |",
            "| `^` | point culminant d'une chaîne nommée | `X` | col (48, voir §4) |",
            "| `#` | détroit, goulet, débouché, delta, estuaire | | |", ""]
    out += grille(phys, "")
    out += ["", "## 2. Milieux (vocabulaire du Géosystème)", "",
            "| Signe | Milieu | Signe | Milieu |", "|---|---|---|---|"]
    items = [(v, codes[k]["libelle"], codes[k]["code"]) for k, v in
             ((k, MILIEUX[c["code"]]) for k, c in codes.items() if c["code"] in MILIEUX)]
    for a, b in zip(items[0::2], items[1::2] + [("", "", "")] * (len(items) % 2)):
        out.append(f"| `{a[0]}` | {a[1]} (`{a[2]}`) | " + (f"`{b[0]}` | {b[1]} (`{b[2]}`) |" if b[0] else " | |"))
    out += ["", "`~` océan, `=` mer Halakhel, `o` lac, blanc : hors Beliet ou estompé.", ""]
    out += grille(milieu, "")
    out += ["", "## 3. Climat", "", "### 3a. Précipitations annuelles (médiane de la case)", "",
            "| Chiffre | mm/an | Chiffre | mm/an |", "|---|---|---|---|",
            "| `0` | < 50 | `5` | 800-1 200 |", "| `1` | 50-100 | `6` | 1 200-1 600 |", "| `2` | 100-250 | `7` | 1 600-2 200 |",
            "| `3` | 250-500 | `8` | 2 200-3 000 |", "| `4` | 500-800 | `9` | > 3 000 |", "",
            "`~` océan, `=` mer Halakhel, `o` lac.", ""]
    out += grille(c_pluie, "")
    out += ["", "### 3b. Hivers du |'Arin (faciès majoritaire de la case)", "",
            "| Signe | Faciès |", "|---|---|",
            "| `B` | Hiver Blanc : manteau neigeux stable, cols fermés |",
            "| `G` | Hiver Gris : pluies froides, gel humide, sols saturés |",
            "| `J` | Hiver Jaune : gel nocturne, ciel clair, vents de poussière |",
            "| `V` | Hiver de Vapeur : brouillards de la mer Halakhel et de ses rives |",
            "| `P` | Hiver pluvieux tempéré (Méditerranée, Atlas ; hors matrice canonique) |",
            "| `.` | hiver doux (tropiques) : pas d'|'Arin |", "",
            f"Seuils (température moyenne du cœur de l'hiver) : Blanc ≤ {hv['seuil_blanc']:.1f} °C, Gris ≤ {hv['seuil_gris']:.1f} °C ; "
            "exactement 2 400 m et 800 m à 22,5° N (matrice du §III), plus haut vers le sud. Voir `ALIGNEMENT_CORPUS.md` §8.", ""]
    out += grille(c_hiver, "")

    # ------------------------------------------------------------------ répertoire
    def ref(lon, lat):
        k = case(lon, lat)
        return f"c{k[1]}·l{k[0]}" if k else "—"

    out += ["", "## 4. Répertoire des lieux", "",
            "Coordonnées [longitude, latitude] en degrés décimaux ; « case » = colonne·ligne de la grille ci-dessus.", ""]
    H = M["halakhel"]
    e = H["emprise"]
    out += ["### Mers et golfes", "", "| Élément | geo_id | Position | Case | Données |", "|---|---|---|---|---|",
            f"| Mer Halakhel (Qibṣān) | `GEO_MER_HALAKHEL` | {e['lon_min']}° à {e['lon_max']}° E ; {e['lat_min']}° à {e['lat_max']}° N | — | "
            f"{H['superficie_km2']:,} km² ; {H['longueur_O_E_km']} km O-E ; niveau {H['niveau_m']} m ; prof. max {H['profondeur_max_m']} m ; {H['iles']} îles |".replace(",", " ")]
    for b in p["halakhel"]["bassins"][1:]:
        c = np.mean(np.array(b["contour"]), axis=0)
        out.append(f"| {b['nom']} (nom de travail) | — | [{c[0]:.2f}, {c[1]:.2f}] | {ref(*c)} | golfe nord derrière la passe Khreth-na-Serek |")
    for d in p.get("eaux_exterieures", []):
        out.append(f"| {d['nom']} | `{d['geo_id']}` | {d['pos']} | {ref(*d['pos'])} | étiquette |")
    out += ["", "### Lacs", "", "| Lac | geo_id | Centre | Case | Données |", "|---|---|---|---|---|"]
    for k, v in M["lacs"].items():
        e = v["emprise"]
        out.append(f"| {v['nom']} | `{k}` | {v['centre']} | {ref(*v['centre'])} | {v['superficie_km2']:,} km² ; {v['altitude_m']} m ; "
                   f"prof. {v['profondeur_max_m']} m ; {e['lon_min']}-{e['lon_max']}° E, {e['lat_min']}-{e['lat_max']}° N |".replace(",", " ", 1))
    out += ["", "### Chaînes", "", "| Chaîne | Longueur | Point culminant | Case | Extrémités |", "|---|---|---|---|---|"]
    for k, v in M["chaines"].items():
        pc = v.get("point_culminant", {})
        pos = pc.get("position")
        out.append(f"| {v['nom'] or k} | {v['longueur_axe_km']} km | {pc.get('altitude_m', '—')} m à {pos} | "
                   f"{ref(*pos) if pos else '—'} | {v['extremites'][0]} → {v['extremites'][1]} |")
    for m in p.get("massifs", []):
        out.append(f"| {m['nom']} (`{m['geo_id']}`) | — | {m['centre']} | {ref(*m['centre'])} | massif ou site |")
    out += ["", "### Fleuves nommés", "", "| Fleuve | geo_id | Longueur dessinée | Amont | Aval | Cases amont → aval |", "|---|---|---|---|---|---|"]
    for k, v in M["fleuves"].items():
        n = " / ".join(x for x in v["noms"] if x) or "émissaire du Mopámà (nom en lacune)"
        out.append(f"| {n} | `{k}` | {v['longueur_dessinee_km']} km | {v['source']} | {v['embouchure']} | "
                   f"{ref(*v['source'])} → {ref(*v['embouchure'])} |")
    out += ["", "### Détroits, goulets, débouchés, deltas, estuaires", "", "| Nom | geo_id | Position | Case |", "|---|---|---|---|"]
    for d in p.get("detroits_et_debouches", []) + p.get("deltas", []):
        out.append(f"| {d['nom']} | `{d['geo_id']}` | {d['pos']} | {ref(*d['pos'])} |")
    out += ["", "### Régions et archipels", "", "| Nom | geo_id | Position | Case |", "|---|---|---|---|"]
    for r in p.get("regions", []):
        out.append(f"| {r['nom']} | `{r['geo_id']}` | {r['pos']} | {ref(*r['pos'])} |")
    for a in p.get("archipels", []):
        out.append(f"| {a['nom']} | `{a['geo_id']}` | {a['pos_etiquette']} | {ref(*a['pos_etiquette'])} |")
        if "ile_principale" in a:
            ip = a["ile_principale"]
            out.append(f"| {ip['nom']} | `{ip['geo_id']}` | {ip['pos']} | {ref(*ip['pos'])} |")
    out += ["", "## 5. Les 48 cols", "",
            "| geo_id | Nom | Altitude | Position | Case | Groupe | Chaîne | Passage | Hiver | Ouverture (mois) |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for c in p["cols"]:
        out.append(f"| `{c['geo_id']}` | {c['nom']} | {c['altitude_m']} m | {c['pos']} | {ref(*c['pos'])} | {c['groupe']} | "
                   f"{c['chaine']} | {c.get('statut_passage')} | {c.get('cycle_hivernal')} | {c['ouverture_mois'][0]}-{c['ouverture_mois'][1]} |")
    out += ["", "## 6. Façades de la mer Halakhel", "",
            "Voir `ALIGNEMENT_CORPUS.md` §4 pour les segments de rivage et les lieux de LIEUX qui s'y rattachent.", ""]
    # ------------------------------------------------------------------ lieux et routes
    f_lr = os.path.join(RACINE, "carte", "sig", "beliet_lieux_routes.json")
    if os.path.exists(f_lr):
        LR = json.load(open(f_lr, encoding="utf-8"))
        lr = relief.copy()
        for r in LR["routes"].values():
            for seg in r.get("segments_milieu", []):
                for lo, la in seg["pts"]:
                    k = case(lo, la)
                    if k:
                        lr[k] = ":" if seg["milieu"] in ("mer", "lac") else "+"
        for l in LR["lieux"].values():
            c = l["caracteristiques"]
            k = case(c["lon"], c["lat"])
            if k:
                lr[k] = {"LUR": "@", "ZRS": "%"}.get(l["type"], "&")
        out += ["## 7. Lieux et routes", "",
                "Positions et tracés calculés par `outils/lieux_routes.py` (détail : `LIEUX_ET_ROUTES.md`).", "",
                "| Signe | Sens |", "|---|---|",
                "| `@` | cité (LUR) |", "| `%` | zone secondaire (ZRS) |", "| `&` | extrémité de route non documentée |",
                "| `+` | route par voie de terre ou fluviale |", "| `:` | route maritime ou lacustre |",
                "| autres | relief et eaux (section 1) |", ""]
        out += grille(lr, "### 7a. Carte des lieux et des routes")
        out += ["", "### 7b. Lieux par case", "", "| ID | Nom | Type | Façade | Position | Case |", "|---|---|---|---|---|---|"]
        for l in LR["lieux"].values():
            c = l["caracteristiques"]
            out.append(f"| `{l['id']}` | {l['nom']} | {l['type']} | {l['facade'] or '—'} | [{c['lon']}, {c['lat']}] | {ref(c['lon'], c['lat'])} |")
        out.append("")
    from mesures_corpus import echapper_tableaux
    txt = echapper_tableaux("\n".join(out) + "\n")
    chemin = os.path.join(RACINE, "carte", "beliet_carte_ascii.md")
    open(chemin, "w", encoding="utf-8").write(txt)
    print(f"{chemin} : {nx} × {ny} cases, {len(txt) // 1024} Ko")


if __name__ == "__main__":
    main()
