#!/usr/bin/env python3
"""Génère la carte du Beliet à partir de donnees/parametres_carte.yaml.

Usage :
    python3 outils/generer_carte.py              # tout recalculer
    python3 outils/generer_carte.py --reprendre  # réutiliser le relief en cache (si les paramètres
                                                 # de relief n'ont pas changé)
"""
import argparse
import hashlib
import json
import os
import pickle
import sys
import time

import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from carto.grille import Grille                      # noqa: E402
from carto.relief import Relief                      # noqa: E402
from carto.hydro import erosion, Hydro               # noqa: E402
from carto.climat import Climat, temperature         # noqa: E402
from carto.milieux import classer_milieux            # noqa: E402
from carto.sources import RACINE, CACHE, registre    # noqa: E402
from carto import export                             # noqa: E402


def journal(msg):
    print(msg, flush=True)


def empreinte(p):
    cles = ["cadre", "contour", "niveaux", "halakhel", "lacs", "chaines", "ecretements", "fleuves", "archipels",
            "fondu_sud", "zones_soulevement", "cols"]
    d = {k: p.get(k) for k in cles}
    if not d.get("cols"):
        d.pop("cols")          # sans cols : même empreinte qu'un relief de référence non entaillé
    return hashlib.sha1(json.dumps(d, sort_keys=True).encode()).hexdigest()[:12]


def charger_cols():
    """Cols placés par outils/placer_cols.py (donnees/cols.yaml), s'il existe."""
    f = os.path.join(RACINE, "donnees", "cols.yaml")
    return yaml.safe_load(open(f, encoding="utf-8"))["cols"] if os.path.exists(f) else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reprendre", action="store_true", help="réutiliser le relief en cache")
    ap.add_argument("--parametres", default=os.path.join(RACINE, "donnees", "parametres_carte.yaml"))
    args = ap.parse_args()
    t0 = time.time()
    p = yaml.safe_load(open(args.parametres, encoding="utf-8"))
    p["cols"] = charger_cols()
    g = Grille(p["cadre"])
    journal(f"Grille {g.W} × {g.H} px ({g.km_px_eq:.2f} km/px à l'équateur)")
    cache = os.path.join(CACHE, f"relief_{empreinte(p)}.pkl")
    if args.reprendre and os.path.exists(cache):
        journal("Relief : repris du cache")
        rel = pickle.load(open(cache, "rb"))
        rel.log = journal
    else:
        journal("Relief :")
        rel = Relief(p, g, journal).construire()
        journal("Érosion :")
        erosion(rel, log=journal)
        rel.ajuster_sommets()
        rel.entailler_cols(p["cols"])
        rel.log = None
        os.makedirs(CACHE, exist_ok=True)
        pickle.dump(rel, open(cache, "wb"), protocol=4)
        rel.log = journal
    journal("Climat :")
    cl = Climat(rel, p, log=journal)
    pluie = cl.pluie()
    temp = temperature(rel)
    journal("Hydrologie :")
    hy = Hydro(rel, pluie, log=journal)
    journal("Milieux :")
    mil = classer_milieux(rel, p, pluie, temp, hy, log=journal)
    journal("Exports :")
    reg = registre()
    export.tout(rel, p, reg, pluie, temp, hy, mil, log=journal)
    journal(f"Terminé en {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
