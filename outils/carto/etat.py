"""État complet de la carte (relief, climat, hydrologie, milieux, hivers), mis en cache.

Les outils d'analyse (lieux, routes) en ont besoin sans régénérer les exports.
"""
import os
import pickle
from types import SimpleNamespace

import numpy as np
import yaml

from .sources import RACINE, CACHE
from .climat import Climat, temperature, hiver
from .hydro import Hydro
from .milieux import classer_milieux


def charger_etat(log=print):
    import sys
    sys.path.insert(0, os.path.join(RACINE, "outils"))
    from generer_carte import empreinte, charger_cols
    p = yaml.safe_load(open(os.path.join(RACINE, "donnees", "parametres_carte.yaml"), encoding="utf-8"))
    p["cols"] = charger_cols()
    emp = empreinte(p)
    rel = pickle.load(open(os.path.join(CACHE, f"relief_{emp}.pkl"), "rb"))
    rel.log = None
    import hashlib
    # la clé suit aussi le relief lui-même : un changement de code à paramètres égaux invalide le cache
    cle = hashlib.sha1(np.ascontiguousarray(rel.h[::7, ::7]).tobytes()).hexdigest()[:8]
    f = os.path.join(CACHE, f"etat_{emp}_{cle}.pkl")
    if os.path.exists(f):
        e = pickle.load(open(f, "rb"))
    else:
        log("  état : climat, hydrologie, milieux (une fois, puis en cache)…")
        muet = lambda m: None
        cl = Climat(rel, p, log=muet)
        P = cl.pluie()
        T = temperature(rel)
        hy = Hydro(rel, P, log=muet)
        mil = classer_milieux(rel, p, P, T, hy, log=muet)
        hv = hiver(rel, T, P, p, log=muet)
        e = dict(P=P.astype(np.float32), T=T.astype(np.float32), Q=hy.Q, A=hy.A, rec=hy.rec,
                 classes=mil["classes"], Tw=hv["Tw"].astype(np.float32), Tn=hv["Tn"].astype(np.float32),
                 facies=hv["facies"], domaine=hv["domaine"], seuil_blanc=hv["seuil_blanc"],
                 seuil_gris=hv["seuil_gris"], calibration=cl.calibration)
        pickle.dump(e, open(f, "wb"), protocol=4)
    return SimpleNamespace(p=p, rel=rel, g=rel.g, **e)
