"""Classification des milieux selon le vocabulaire fermé du Géosystème v3.1 (§II, « Milieux »)."""
import numpy as np
from scipy.ndimage import (binary_dilation, distance_transform_edt, label, uniform_filter)

# Vocabulaire fermé du corpus — ordre = code numérique du raster
MILIEUX = [
    ("desert_pierreux", "Désert de pierre", "#c9b48f"),
    ("desert_sableux", "Désert de sable", "#ecd9a3"),
    ("dunes_littorales", "Cordons dunaires côtiers", "#f3e6bd"),
    ("oasis", "Oasis", "#3f8f4a"),
    ("steppe_piemont", "Steppe semi-aride de piémont", "#c6c58a"),
    ("fourre_cotier_sec", "Fourré côtier sec", "#9aa86a"),
    ("depression_saline", "Dépression saline", "#e8e2d6"),
    ("cote_desertique", "Côte désertique", "#d8c3a0"),
    ("recif_corallien", "Récif corallien", "#5fc9c4"),
    ("littoral_rocheux", "Littoral rocheux", "#8c8577"),
    ("plaine_alluviale", "Plaine alluviale irriguée", "#8cbf5a"),
    ("foret_montagne", "Forêt de montagne et de piémont", "#5f8466"),
    ("prairie_altitude", "Prairie d'altitude", "#a3b07f"),
    ("zone_periglaciaire", "Zone périglaciaire", "#a59e94"),
    ("glacier", "Glacier", "#f4f8fb"),
    ("foret_tropicale_humide", "Forêt tropicale humide", "#1f5a32"),
    ("herbage_arbore", "Herbage arboré", "#b4b85c"),
    ("foret_berge", "Forêt de berge", "#4c8a3c"),
    ("foret_maree", "Forêt de marée", "#2f7564"),
    ("zone_humide_lacustre", "Zone humide lacustre", "#6fa58e"),
    ("eaux_lacustres", "Eaux lacustres et hauts-fonds", "#7fb3d5"),
    ("ile_aride", "Île aride", "#bda57e"),
]
CODE = {c[0]: i for i, c in enumerate(MILIEUX)}
OCEAN, HALAKHEL, DEHORS, VIDE = 254, 253, 252, 255


def filtre_majoritaire(cl, masque, taille=5, codes=None):
    """Filtre de mode sur les classes de `codes`, limité à `masque`."""
    codes = codes if codes is not None else np.unique(cl[masque])
    meilleur = np.zeros(cl.shape, np.float32)
    sortie = cl.copy()
    for c in codes:
        f = uniform_filter((cl == c).astype(np.float32), taille)
        mieux = f > meilleur
        meilleur[mieux] = f[mieux]
        sortie[mieux & masque] = c
    return sortie


def classer_milieux(rel, p, P, T, hy, log=print):
    g = rel.g
    km = g.km_px[:, None]
    h = rel.h
    terre = rel.terre
    LON, LAT = rel.LON, rel.LAT
    cl = np.full(g.shape, VIDE, np.uint8)
    cl[rel.ocean] = OCEAN
    cl[rel.mer] = HALAKHEL
    cl[rel.dehors] = DEHORS
    cl[rel.lac > 0] = CODE["eaux_lacustres"]

    # ergs (désert de sable) — propositions dans les paramètres
    from .grille import bruit_bande
    erg0 = g.rasteriser([g.poly_px(e) for e in p.get("ergs", [])]).astype(bool)
    d_in = distance_transform_edt(erg0) * km
    d_out = distance_transform_edt(~erg0) * km
    nb = bruit_bande(g.shape, 909, 3, 160 / g.km_px_eq)
    erg = (d_in - d_out + 45 * nb) > 0
    # lisière d'écotone : ±12 % de bruit sur la pluie pour des limites naturelles
    P = P * (1 + 0.12 * bruit_bande(g.shape, 910, 3, 90 / g.km_px_eq))

    # --- base : pluie × altitude ------------------------------------------------------
    sec = P < 110
    desert = np.where(erg, CODE["desert_sableux"], CODE["desert_pierreux"])
    base = np.where(sec, desert, CODE["steppe_piemont"])
    base = np.where((P >= 250) & (P < 600), CODE["steppe_piemont"], base)
    base = np.where((P >= 110) & (P < 250) & (h < 350) & (rel.crete < 0.05), desert, base)
    base = np.where((P >= 600) & (P < 1450), CODE["herbage_arbore"], base)
    base = np.where((P >= 1450) & (T >= 19), CODE["foret_tropicale_humide"], base)
    # étages montagnards (Zone II) : 800 / 2 400 / 3 600 m [CANON] à la latitude de référence (halekh, ~22,5° N),
    # convertis en températures annuelles : les étages remontent vers le sud (~+800 m sous 12° N).
    # Limites irrégulières : seuils et emprise de la chaîne bruités, transition boisée.
    E = p.get("etages", {})
    lat_ref = E.get("latitude_reference", 22.5)
    # température de la saison de végétation (annuelle + 1/3 de l'amplitude) : la limite des arbres dépend
    # de l'été, d'où un étage plus bas au nord (étés chauds) qu'au sud
    from .climat import amplitude_annuelle
    ch = p.get("climat_hiver", {})
    T_ann = T
    T = T_ann + amplitude_annuelle(LAT, ch) / 3
    A_ref = float(amplitude_annuelle(np.float32(lat_ref), ch))
    T_alt = lambda alt: 27.5 - 0.45 * max(lat_ref - 12, 0) - 6.0 * alt / 1000 + A_ref / 3
    nm = bruit_bande(g.shape, 911, 3, 70 / g.km_px_eq)
    nm2 = bruit_bande(g.shape, 912, 3, 40 / g.km_px_eq)
    dT = 1.3 * nm                                      # ≈ ±220 m
    mont = (T <= T_alt(800) + dT) & (T > T_alt(2400) + dT) & ((rel.crete > 0.06 + 0.1 * nm2) | (T <= T_alt(1300) + 0.9 * nm2))
    base = np.where(mont & (P >= 720), CODE["foret_montagne"], base)
    base = np.where(mont & (P >= 480) & (P < 720), CODE["herbage_arbore"], base)
    base = np.where(mont & (P < 480) & (P >= 110), CODE["steppe_piemont"], base)
    base = np.where((T <= T_alt(2400) + dT) & (T > T_alt(3600) + dT) & terre, CODE["prairie_altitude"], base)
    base = np.where((T <= T_alt(3600) + dT) & terre, CODE["zone_periglaciaire"], base)
    # glaciers : actifs sous −5 °C de moyenne annuelle (k'ara, « dernier glacier » > 4 800 m) ;
    # relictuels sous −2,5 °C sur halekh (cirques) ; aucun sur qoyra (−1 °C au sommet)
    sl = 1.5 * bruit_bande(g.shape, 913, 40 / g.km_px_eq, 600 / g.km_px_eq)
    halekh = (LON + sl) < E.get("glaciers_relictuels_ouest_de_lon", 1.0)
    glace = (T_ann <= E.get("glacier_t_annuelle_c", -5.0)) | (halekh & (T_ann <= E.get("glacier_relictuel_t_annuelle_c", -2.5)))
    base = np.where(glace & terre, CODE["glacier"], base)
    cl[terre] = base[terre].astype(np.uint8)

    # --- façades ----------------------------------------------------------------------
    # limites géographiques adoucies : ±~0,7° de bruit à grande échelle (pas de coupure rectiligne)
    nl = 0.7 * bruit_bande(g.shape, 914, 30 / g.km_px_eq, 500 / g.km_px_eq)
    LONs, LATs = LON + nl, LAT + 0.8 * nl
    d_ocean = distance_transform_edt(~rel.ocean) * km
    d_mer = distance_transform_edt(~rel.mer) * km
    cote = terre & (d_ocean < 120) & (LATs >= 29.5) & (P >= 220) & (h < 900) & (LONs < 36)
    cl[cote & np.isin(cl, [CODE["steppe_piemont"], CODE["herbage_arbore"], CODE["desert_pierreux"]])] = CODE["fourre_cotier_sec"]
    dunes = terre & (d_ocean < 18) & (P < 450) & (LONs < -8) & (LATs > 15) & (LATs < 28.5) & (h < 90)
    cl[dunes] = CODE["dunes_littorales"]
    cdes = terre & (d_ocean < 16) & (P < 130) & (LONs > 30) & (h < 200)
    cl[cdes] = CODE["cote_desertique"]

    # --- dépressions salées -----------------------------------------------------------
    sal = terre & (hy.profondeur_cuvette > 8) & (P < 320)
    sal |= terre & (d_mer < 28) & (LONs > 25) & (P < 260) & (h < 60)       # remontées salines de l'interfluve
    for d in p.get("depressions_salees", []):
        m0 = g.rasteriser(g.poly_px(d["contour"])).astype(bool)
        din, dout = distance_transform_edt(m0) * km, distance_transform_edt(~m0) * km
        sal |= ((din - dout + 9 * bruit_bande(g.shape, 915, 3, 50 / g.km_px_eq)) > 0) & terre
    cl[sal] = CODE["depression_saline"]

    # --- zones humides et marées --------------------------------------------------------
    d_lac = distance_transform_edt(rel.lac == 0) * km
    niveau_lac = np.zeros(g.shape, np.float32)
    for k, L in enumerate(rel.lacs, start=1):
        dk = distance_transform_edt(rel.lac != k) * km
        niveau_lac = np.where(dk < 25, L["cfg"]["altitude_m"], niveau_lac)
    humide = terre & (d_lac < 18) & (h < niveau_lac + 30) & (P >= 500)
    cuv = terre & (hy.profondeur_cuvette > 3) & (hy.profondeur_cuvette < 40) & (P >= 750)
    lab_c, n_c = label(cuv)
    if n_c:
        taille = np.bincount(lab_c.ravel(), weights=g.aire_km2().ravel())
        cuv &= taille[lab_c] < 12000          # pas de marais géant non documenté
    humide |= cuv
    cl[humide] = CODE["zone_humide_lacustre"]
    maree = terre & (d_ocean < 12) & (h < 14) & (P >= 1000)
    cl[maree] = CODE["foret_maree"]

    # --- plaines alluviales des fleuves du nord --------------------------------------------
    lits = np.zeros(g.shape, bool)
    for F in rel.fleuves:
        for c in F["lignes"]:
            x, y = g.px(c[:, 0], c[:, 1])
            ix = np.clip(x.astype(int), 0, g.W - 1); iy = np.clip(y.astype(int), 0, g.H - 1)
            lits[iy, ix] = True
    d_lit = distance_transform_edt(~lits) * km
    alluv = terre & (d_lit < 9) & (P < 650) & (h < 1300)
    # delta Šafāqil : éventail entre les bras, borné par l'altitude (pas de cadre géographique)
    bras = np.zeros(g.shape, bool)
    for F in rel.fleuves:
        if F["cfg"]["geo_id"] == "GEO_FLV_ABNUHIL_SAFAQIL":
            for c in F["lignes"]:
                x, y = g.px(c[:, 0], c[:, 1])
                bras[np.clip(y.astype(int), 0, g.H - 1), np.clip(x.astype(int), 0, g.W - 1)] = True
    d_bras = distance_transform_edt(~bras) * km
    nd = bruit_bande(g.shape, 916, 3, 60 / g.km_px_eq)
    delta = terre & (d_bras < 70 + 18 * nd) & (h < 22 + 8 * nd) & (LATs > 29.9)
    alluv |= delta
    cl[alluv] = CODE["plaine_alluviale"]

    # --- forêts de berge : grands cours d'eau en savane / steppe ------------------------------
    berge = terre & (hy.Q > 120) & (P >= 300) & (P < 1450)
    berge = binary_dilation(berge, iterations=1) & terre & np.isin(cl, [CODE["steppe_piemont"], CODE["herbage_arbore"]])
    cl[berge] = CODE["foret_berge"]

    # --- oasis -------------------------------------------------------------------------
    rng = np.random.default_rng(p["cadre"]["graine_aleatoire"] + 77)
    cand = terre & (P < 160) & (hy.A > 400) & (hy.A < 60000) & (h < 1000) & np.isin(cl, [CODE["desert_pierreux"], CODE["desert_sableux"], CODE["depression_saline"], CODE["steppe_piemont"]])
    karst = terre & (d_mer < 8) & (LONs > 14) & (LONs < 28) & (LATs < 26.8) & (P < 300)   # oasis littorales (§IV.20)
    oasis = np.zeros(g.shape, bool)
    for masque, n_max, pas in ((cand, 140, 26), (karst, 40, 14)):
        ys, xs = np.nonzero(masque)
        if len(xs) == 0:
            continue
        ordre = rng.permutation(len(xs))
        pris = []
        for j in ordre:
            x, y = xs[j], ys[j]
            if all((x - a) ** 2 + (y - b) ** 2 > pas ** 2 for a, b in pris):
                pris.append((x, y))
                if len(pris) >= n_max:
                    break
        for x, y in pris:
            r = rng.uniform(1.2, 3.2)
            ri = int(np.ceil(r))
            yy, xx = np.mgrid[-ri:ri + 1, -ri:ri + 1]
            disque = (xx * xx + yy * yy) <= r * r
            y0, x0 = y - ri, x - ri
            if y0 >= 0 and x0 >= 0 and y0 + 2 * ri + 1 <= g.H and x0 + 2 * ri + 1 <= g.W:
                oasis[y0:y0 + 2 * ri + 1, x0:x0 + 2 * ri + 1] |= disque
    oasis &= terre
    cl[oasis] = CODE["oasis"]

    # --- littoral rocheux ------------------------------------------------------------------
    # pente à l'échelle réelle de la latitude ; hauteur mesurée au-dessus de l'eau voisine
    # (la mer Halakhel est à rel.L, sous le niveau de l'océan)
    gy, gx = np.gradient(h, g.km_px_eq * 1000)
    pente = np.hypot(gx, gy) / np.cos(np.radians(LAT))
    d_eau_sal = np.minimum(d_ocean, d_mer)
    h_eau = np.where(d_mer < d_ocean, h - rel.L, h)
    roche = terre & (d_eau_sal < 4) & ((pente > 0.035) | (h_eau > 120))
    cl[roche] = CODE["littoral_rocheux"]

    # --- îles arides -----------------------------------------------------------------------
    lab, n = label(terre)
    tailles = np.bincount(lab.ravel())
    continent = np.argmax(np.where(np.arange(len(tailles)) == 0, 0, tailles))
    ile = terre & (lab != continent)
    d_lac_ile = distance_transform_edt(rel.lac == 0) * km
    ile_ar = ile & (P < 900) & ~(d_lac_ile < 3)
    cl[ile_ar] = CODE["ile_aride"]

    # --- récifs coralliens (marins) --------------------------------------------------------
    d_cote = distance_transform_edt(~terre) * km
    recif = rel.ocean & (d_cote < 22) & (rel.h > -70) & (LON > 32) & (LON < 44) & (LAT > 12.3) & (LAT < 28.5)
    cl[recif] = CODE["recif_corallien"]

    # --- lissage ------------------------------------------------------------------------
    garde = np.isin(cl, [CODE["oasis"], CODE["glacier"], CODE["foret_berge"], CODE["eaux_lacustres"],
                         CODE["littoral_rocheux"]])   # liseré étroit : protégé du lissage (v0.5)
    cl = filtre_majoritaire(cl, terre & ~garde, 5, codes=[i for i in range(len(MILIEUX)) if i not in (CODE["oasis"], CODE["eaux_lacustres"])])
    A_f = g.aire_km2() * rel.fondu
    stats = {MILIEUX[c][0]: float((A_f[cl == c]).sum()) for c in range(len(MILIEUX))}
    log("  superficies (km²) : " + ", ".join(f"{k} {v:,.0f}" for k, v in sorted(stats.items(), key=lambda kv: -kv[1]) if v > 0))
    return dict(classes=cl, stats=stats)
