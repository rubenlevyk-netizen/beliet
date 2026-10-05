"""Carte des lieux et des routes : fond physique adouci, lieux du corpus, routes calculées."""
import math
import os

import numpy as np
from scipy.ndimage import binary_dilation, gaussian_filter

from .export import (FAMILLE, POLICE, POLICE_B, POLICE_I, VERSION, Texte, anneaux_svg, composer, contours_masque,
                     d_chemin, echap, estomper, jpg_b64, ombrage, rendre_png, teintes_hypso, chaikin)

# familles linguistiques du corpus
FAMILLES = {
    "HLK": ("Halaktim", "#2f5f8a"), "SMQ": ("Šamqiriyyūn", "#a8642a"), "MBR": ("Ba-mbaro", "#3d7a3a"),
    "QYR": ("Qoyra-ña-ra", "#8a3a6a"), "TRK": ("Tɨrakh", "#6a4a2a"),
    "SMQ_TRK_MIXED": ("Šamqiriyyūn-Tɨrakh", "#8a5a3a"), "MBR_QYR_MIXED": ("Ba-mbaro-Qoyra", "#6a5a5a"),
}
MILIEU_ROUTE = {"mer": ("#1f5f9a", "10,6"), "lac": ("#2a8aa8", "6,4"), "fleuve": ("#1d8a7a", None),
                "terre": ("#7a3e1a", None)}


def fond(rel):
    """Relief ombré adouci (blanchi), eaux en clair."""
    om = ombrage(rel)
    rgb = estomper(composer(teintes_hypso(rel), om, rel, force_terre=0.55), rel, om).astype(np.float32)
    blanc = np.full_like(rgb, 250)
    rgb = rgb * 0.62 + blanc * 0.38
    return np.clip(rgb, 0, 255).astype(np.uint8)


class Placeur:
    """Placement glouton d'étiquettes sans chevauchement (boîtes en pixels)."""

    def __init__(self):
        self.boites = []
        self.T = Texte()

    def libre(self, b):
        x0, y0, x1, y1 = b
        for a in self.boites:
            if not (x1 < a[0] or x0 > a[2] or y1 < a[1] or y0 > a[3]):
                return False
        return True

    def reserver(self, b):
        self.boites.append(b)

    def largeur(self, t, taille, fichier=POLICE):
        w, _ = self.T.largeur(t, fichier, taille, 0)
        return sum(w)


def carte(rel, lieux, routes, cols, sortie, log, trouees=()):
    g = rel.g
    W, H = g.W, g.H
    parts = []
    img = fond(rel)
    # vecteurs physiques : rivage de la mer intérieure, lacs, côtes, fleuves nommés
    vec = []
    for pg in contours_masque(rel.mer, simpl=0.6, aire_min=6):
        vec.append(f'<path d="{anneaux_svg(pg)}" fill="none" stroke="#3d6f8f" stroke-width="1.6" stroke-opacity="0.8"/>')
    for k in range(1, len(rel.lacs) + 1):
        for pg in contours_masque(rel.lac == k, simpl=0.6):
            vec.append(f'<path d="{anneaux_svg(pg)}" fill="none" stroke="#3d6f8f" stroke-width="1.4"/>')
    oc = rel.ocean & (rel.h < -2)
    for pg in contours_masque(oc, simpl=0.8, aire_min=40):
        vec.append(f'<path d="{anneaux_svg(pg)}" fill="none" stroke="#4d7f9f" stroke-width="1.2" stroke-opacity="0.7"/>')
    for F in rel.fleuves:
        larg = 1.0 + 0.5 * F["cfg"].get("largeur", 2)
        for c in F["lignes"]:
            x, y = g.px(c[:, 0], c[:, 1])
            ok = ~(rel.mer | rel.ocean)[np.clip(y.astype(int), 0, H - 1), np.clip(x.astype(int), 0, W - 1)]
            P = np.c_[x, y][ok]
            if len(P) > 2:
                vec.append(f'<path d="{d_chemin(P[::2])}" fill="none" stroke="#4a86b0" stroke-width="{larg:.1f}" stroke-opacity="0.85" stroke-linejoin="round"/>')
    # routes : segments colorés par milieu de passage
    rts = []
    lab_rt = []
    for rid, r in sorted(routes.items()):
        if r.get("statut") != "tracé":
            continue
        segs = r.get("segments_milieu", [])
        for seg in segs:
            P = np.array([g.px(lo, la) for lo, la in seg["pts"]])
            if len(P) < 2:
                continue
            col, dash = MILIEU_ROUTE[seg["milieu"]]
            if seg.get("hors_modes"):
                col, dash = "#d0202a", "3,4"
            ds = f' stroke-dasharray="{dash}"' if dash else ""
            rts.append(f'<path d="{d_chemin(chaikin(P, 1))}" fill="none" stroke="#ffffff" stroke-width="5.5" stroke-opacity="0.55" stroke-linejoin="round"/>'
                       f'<path d="{d_chemin(chaikin(P, 1))}" fill="none" stroke="{col}" stroke-width="2.6"{ds} stroke-linejoin="round" stroke-linecap="round"/>')
        if r.get("correction"):
            P = np.array([g.px(lo, la) for lo, la in r["correction"]["trace"]])
            rts.append(f'<path d="{d_chemin(P)}" fill="none" stroke="#6a2a8a" stroke-width="2.4" stroke-dasharray="8,4,2,4" stroke-opacity="0.9"/>')
        if r.get("variante_corpus"):
            P = np.array([g.px(lo, la) for lo, la in r["variante_corpus"]["trace"]])
            rts.append(f'<path d="{d_chemin(P)}" fill="none" stroke="#7a3e1a" stroke-width="2" stroke-dasharray="2,5" stroke-opacity="0.9"/>')
        tr = np.array(r["trace"])
        m = tr[len(tr) // 2]
        lab_rt.append((rid, g.px(*m)))
    # cols
    sym = []
    pl = Placeur()
    cols_util = set()
    for r in routes.values():
        for c in r.get("cols_franchis", []) or []:
            cols_util.add(c.split("(")[1][:3])
    for c in cols:
        x, y = g.px(*c["pos"])
        utile = c["geo_id"][-3:] in cols_util
        s = 7 if utile else 5
        sym.append(f'<path d="M{x - s:.1f},{y + s * 0.8:.1f} L{x:.1f},{y - s:.1f} L{x + s:.1f},{y + s * 0.8:.1f} Z" '
                   f'fill="{"#3b2a1a" if utile else "#8a7a6a"}" stroke="#ffffff" stroke-width="1"/>')
        pl.reserver((x - s, y - s, x + s, y + s))
    # trouées basses
    txt_tr = []
    for t in trouees:
        x, y = g.px(*t["pos"])
        sym.append(f'<path d="M{x - 9:.1f},{y - 7:.1f} L{x - 3:.1f},{y:.1f} L{x - 9:.1f},{y + 7:.1f} M{x + 9:.1f},{y - 7:.1f} L{x + 3:.1f},{y:.1f} L{x + 9:.1f},{y + 7:.1f}" '
                   f'fill="none" stroke="#8a1a1a" stroke-width="2.6" stroke-linecap="round"/>')
        pl.reserver((x - 10, y - 8, x + 10, y + 8))
        txt_tr.append(f'<text x="{x + 12:.1f}" y="{y - 8:.1f}" font-family="{FAMILLE}" font-size="15" font-weight="bold" fill="#8a1a1a" '
                   f'stroke="#ffffff" stroke-width="3" paint-order="stroke">{t["id"].replace("TRO_", "T")}</text>')
    # lieux
    et = []
    ordre = sorted(lieux.values(), key=lambda l: (l["type"] != "LUR", -(l.get("pop_1570") or 0)))
    vus = {}
    for l in ordre:
        p = l["placement"]
        if l.get("placement", {}).get("meme_que"):
            continue
        x, y = g.px(p["lon"], p["lat"])
        cle = (round(x / 6), round(y / 6))
        if l["type"] == "LUR":
            pop = l.get("pop_1570") or 5000
            r = 4.5 + 3.2 * math.sqrt(pop / 20000)
            fam = l.get("famille") or ""
            col = FAMILLES.get(fam, ("?", "#555555"))[1]
            sym.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" stroke="#ffffff" stroke-width="1.6"/>')
            if l["constats_ecarts"]:
                sym.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 3.2:.1f}" fill="none" stroke="#d0202a" stroke-width="1.4" stroke-dasharray="3,2"/>')
            taille, fich, coul = 19, POLICE_B, "#1e1a16"
        elif l["type"] == "ZRS":
            r = 5.5
            sym.append(f'<path d="M{x:.1f},{y - r:.1f} L{x + r:.1f},{y:.1f} L{x:.1f},{y + r:.1f} L{x - r:.1f},{y:.1f} Z" fill="#f4f0e6" stroke="#3a2a1a" stroke-width="1.5"/>')
            taille, fich, coul = 15, POLICE_I, "#3a2a1a"
        else:
            r = 4.5
            sym.append(f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r:.1f}" height="{2 * r:.1f}" fill="#ffffff" stroke="#6a6a6a" stroke-width="1.4"/>')
            taille, fich, coul = 14, POLICE_I, "#5a5a5a"
        pl.reserver((x - r, y - r, x + r, y + r))
        et.append((l, x, y, r, taille, fich, coul))
    txt_halo, txt = [], list(txt_tr)
    for l, x, y, r, taille, fich, coul in et:
        t = l["nom"]
        w = pl.largeur(t, taille, fich)
        h = taille
        cands = [(x + r + 4, y + h * 0.35, "start"), (x - r - 4, y + h * 0.35, "end"), (x, y - r - 5, "middle"),
                 (x, y + r + h, "middle"), (x + r + 3, y - r - 2, "start"), (x - r - 3, y - r - 2, "end"),
                 (x + r + 3, y + r + h - 2, "start"), (x - r - 3, y + r + h - 2, "end")]
        for k in (1.0, 1.8, 2.6):
            ok = False
            for cx, cy, an in cands:
                dx = (cx - x) * (k - 1)
                dy = (cy - y) * (k - 1)
                cx2, cy2 = cx + dx, cy + dy
                x0 = cx2 if an == "start" else cx2 - w if an == "end" else cx2 - w / 2
                b = (x0 - 1, cy2 - h * 0.85, x0 + w + 1, cy2 + h * 0.25)
                if pl.libre(b):
                    pl.reserver(b)
                    ok = True
                    st = 'font-style="italic"' if fich == POLICE_I else ('font-weight="bold"' if fich == POLICE_B else "")
                    if k > 1:
                        txt.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{(x0 + w / 2):.1f}" y2="{cy2 - h * 0.3:.1f}" stroke="#6a6a6a" stroke-width="0.7"/>')
                    txt_halo.append(f'<text x="{cx2:.1f}" y="{cy2:.1f}" font-family="{FAMILLE}" font-size="{taille}" {st} text-anchor="{an}" fill="none" stroke="#ffffff" stroke-width="3.2" stroke-opacity="0.9" stroke-linejoin="round">{echap(t)}</text>')
                    txt.append(f'<text x="{cx2:.1f}" y="{cy2:.1f}" font-family="{FAMILLE}" font-size="{taille}" {st} text-anchor="{an}" fill="{coul}">{echap(t)}</text>')
                    break
            if ok:
                break
    # numéros de route
    for rid, (x, y) in lab_rt:
        t = rid.replace("RT_0", "").replace("RT_", "")
        w = pl.largeur(t, 13) + 6
        b = (x - w / 2, y - 9, x + w / 2, y + 7)
        if pl.libre(b):
            pl.reserver(b)
            txt.append(f'<rect x="{b[0]:.1f}" y="{b[1]:.1f}" width="{w:.1f}" height="16" rx="3" fill="#fffdf6" stroke="#7a3e1a" stroke-width="0.8"/>'
                       f'<text x="{x:.1f}" y="{y + 4:.1f}" font-family="{FAMILLE}" font-size="13" text-anchor="middle" fill="#5a2a0a">{t}</text>')
    leg = legende(g, lieux)
    for demi, chemin in ((False, sortie + ".png"), (True, sortie + ".svg")):
        k = 2 if demi else 1
        im = img[::k, ::k]
        fond_svg = (f'<image x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="none" '
                    f'href="data:image/jpeg;base64,{jpg_b64(im)}"/>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
               f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
               f'<g inkscape:groupmode="layer" id="fond" inkscape:label="Fond physique">{fond_svg}</g>'
               f'<g inkscape:groupmode="layer" id="hydro" inkscape:label="Rivages et fleuves">{"".join(vec)}</g>'
               f'<g inkscape:groupmode="layer" id="routes" inkscape:label="Routes calculées">{"".join(rts)}</g>'
               f'<g inkscape:groupmode="layer" id="lieux" inkscape:label="Lieux et cols">{"".join(sym)}</g>'
               f'<g inkscape:groupmode="layer" id="etiquettes" inkscape:label="Étiquettes">{"".join(txt_halo)}{"".join(txt)}</g>'
               f'<g inkscape:groupmode="layer" id="legende" inkscape:label="Légende">{leg}</g></svg>')
        if demi:
            open(chemin, "w", encoding="utf-8").write(svg)
            log(f"  {os.path.basename(chemin)} : {os.path.getsize(chemin) / 1e6:.1f} Mo")
        else:
            rendre_png(svg, chemin, log)


def legende(g, lieux):
    p = []
    Wd, Hd = 820, 712
    lx, ly = g.W - Wd - 14, 24  # coin NE, sur les terres hors Beliet
    p.append(f'<rect x="24" y="24" width="900" height="150" rx="6" fill="#ffffff" fill-opacity="0.86" stroke="#6a5a48" stroke-width="1.5"/>'
             f'<text x="44" y="86" font-family="{FAMILLE}" font-size="54" font-weight="bold" fill="#3a2a1a" letter-spacing="6">LE BELIET</text>'
             f'<text x="46" y="124" font-family="{FAMILLE}" font-size="24" font-style="italic" fill="#4a3a2a">Lieux du corpus et routes calculées sur la géographie</text>'
             f'<text x="46" y="156" font-family="{FAMILLE}" font-size="18" fill="#5a4a3a">Version {VERSION} · LIEUX_URBAINS v2, RESEAU_ROUTES v3 · positions [PROPOSITION] · Web Mercator</text>')
    p.append(f'<rect x="{lx - 10:.0f}" y="{ly:.0f}" width="{Wd}" height="{Hd}" rx="6" fill="#ffffff" fill-opacity="0.9" stroke="#6a5a48"/>')
    y = ly + 40
    p.append(f'<text x="{lx + 10:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="28" font-weight="bold" fill="#3a2a1a">Lieux</text>')
    y += 34
    for code, (nom, col) in list(FAMILLES.items())[:5]:
        p.append(f'<circle cx="{lx + 30:.0f}" cy="{y - 7:.0f}" r="10" fill="{col}" stroke="#fff" stroke-width="1.5"/>'
                 f'<text x="{lx + 54:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">{echap(nom)} (cité, LUR ; taille selon la population 1570)</text>')
        y += 32
    p.append(f'<circle cx="{lx + 30:.0f}" cy="{y - 7:.0f}" r="10" fill="#888" stroke="#d0202a" stroke-width="1.4" stroke-dasharray="3,2"/>'
             f'<text x="{lx + 54:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">cité dont un biome ou une exposition du corpus diffère du site calculé</text>')
    y += 32
    p.append(f'<path d="M{lx + 30},{y - 15} L{lx + 38},{y - 7} L{lx + 30},{y + 1} L{lx + 22},{y - 7} Z" fill="#f4f0e6" stroke="#3a2a1a" stroke-width="1.5"/>'
             f'<text x="{lx + 54:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" font-style="italic" fill="#3a2a1a">zone secondaire (ZRS)</text>')
    y += 32
    p.append(f'<rect x="{lx + 22}" y="{y - 15}" width="16" height="16" fill="#fff" stroke="#6a6a6a" stroke-width="1.4"/>'
             f'<text x="{lx + 54:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" font-style="italic" fill="#3a2a1a">extrémité de route non documentée (position déduite)</text>')
    y += 32
    p.append(f'<path d="M{lx + 23},{y + 1} L{lx + 30},{y - 14} L{lx + 37},{y + 1} Z" fill="#3b2a1a" stroke="#fff"/>'
             f'<text x="{lx + 54:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">col emprunté par une route (gris : autre col)</text>')
    y += 46
    p.append(f'<text x="{lx + 10:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="28" font-weight="bold" fill="#3a2a1a">Routes (tracé le plus rapide dans les modes déclarés)</text>')
    y += 34
    for k, lib in (("mer", "navigation maritime (Halakhel, océans)"), ("lac", "navigation lacustre"),
                   ("fleuve", "navigation fluviale"), ("terre", "voie de terre (caravane, portage, col)")):
        col, dash = MILIEU_ROUTE[k]
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        p.append(f'<line x1="{lx + 14}" y1="{y - 7}" x2="{lx + 74}" y2="{y - 7}" stroke="{col}" stroke-width="3"{ds}/>'
                 f'<text x="{lx + 88:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">{lib}</text>')
        y += 30
    p.append(f'<line x1="{lx + 14}" y1="{y - 7}" x2="{lx + 74}" y2="{y - 7}" stroke="#d0202a" stroke-width="3" stroke-dasharray="3,4"/>'
             f'<text x="{lx + 88:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">tronçon imposé par la géographie, absent des modes déclarés</text>')
    y += 30
    p.append(f'<line x1="{lx + 14}" y1="{y - 7}" x2="{lx + 74}" y2="{y - 7}" stroke="#6a2a8a" stroke-width="2.4" stroke-dasharray="8,4,2,4"/>'
             f'<text x="{lx + 88:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">tracé corrigé proposé (extrémité ou modes)</text>')
    y += 30
    p.append(f'<path d="M{lx + 27},{y - 14} L{lx + 33},{y - 7} L{lx + 27},{y} M{lx + 45},{y - 14} L{lx + 39},{y - 7} L{lx + 45},{y}" fill="none" stroke="#8a1a1a" stroke-width="2.6"/>'
             f'<text x="{lx + 88:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">trouée basse de la cordillère (T1…, nom à forger)</text>')
    y += 30
    p.append(f'<line x1="{lx + 14}" y1="{y - 7}" x2="{lx + 74}" y2="{y - 7}" stroke="#7a3e1a" stroke-width="2" stroke-dasharray="2,5"/>'
             f'<text x="{lx + 88:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">variante par le col indiqué dans le corpus</text>')
    y += 30
    p.append(f'<rect x="{lx + 30}" y="{y - 20}" width="30" height="16" rx="3" fill="#fffdf6" stroke="#7a3e1a"/>'
             f'<text x="{lx + 45}" y="{y - 8}" font-family="{FAMILLE}" font-size="13" text-anchor="middle" fill="#5a2a0a">10</text>'
             f'<text x="{lx + 88:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">numéro de route (RT_010) ; mesures : LIEUX_ET_ROUTES.md</text>')
    return "".join(p)
