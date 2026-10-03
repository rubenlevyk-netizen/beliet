"""Exports : cartes PNG, SVG à calques (Inkscape), GeoJSON, GeoTIFF, cartes d'altitude."""
import base64
import io
import json
import math
import os
import unicodedata

import numpy as np
from affine import Affine
from PIL import Image, ImageFont
from rasterio import features
from scipy.ndimage import gaussian_filter, zoom
from shapely.geometry import LineString, Polygon, mapping, shape
from shapely.ops import unary_union

from .grille import lisser_polyligne
from .milieux import CODE, DEHORS, HALAKHEL, MILIEUX, OCEAN
from .sources import RACINE, nom_registre

SORTIE = os.path.join(RACINE, "carte")
POLICE = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
POLICE_I = "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
POLICE_B = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
FAMILLE = "FreeSerif, 'DejaVu Serif', 'Liberation Serif', Georgia, serif"
VERSION = "0.4"

# --------------------------------------------------------------------------- couleurs

HYPSO = [(-500, (126, 160, 112)), (0, (118, 156, 104)), (150, (140, 172, 112)), (400, (180, 194, 132)),
         (700, (214, 210, 152)), (1000, (222, 200, 146)), (1500, (206, 172, 122)), (2000, (186, 146, 104)),
         (2600, (162, 124, 92)), (3200, (150, 120, 108)), (3800, (178, 170, 168)), (4400, (226, 224, 226)),
         (5200, (250, 250, 252))]
BATHY = [(-6000, (62, 104, 156)), (-3000, (86, 132, 182)), (-1000, (118, 164, 204)), (-200, (150, 190, 222)),
         (0, (176, 208, 230))]
BATHY_HAL = [(-1800, (70, 122, 150)), (-900, (96, 150, 172)), (-300, (130, 180, 196)), (0, (160, 202, 212))]
LAC = [(-800, (90, 140, 178)), (-200, (130, 178, 210)), (0, (160, 200, 226))]
# précipitations annuelles (mm) : désert ocre → steppe → savane → forêt → très humide
PLUIE = [(0, (236, 224, 196)), (100, (230, 212, 166)), (250, (220, 214, 150)), (500, (186, 206, 130)),
         (800, (140, 190, 118)), (1200, (92, 166, 122)), (1600, (62, 140, 140)), (2200, (48, 108, 160)),
         (3000, (40, 76, 140))]
ISOHYETES = [50, 100, 250, 500, 800, 1200, 1600, 2200]
MODES = {
    "milieux": "Carte physique — relief, hydrographie et milieux",
    "relief": "Carte physique — relief et hydrographie",
    "climat": "Carte du climat — précipitations annuelles et hivers du |’Arin",
}


def rampe(v, stops):
    xs = np.array([s[0] for s in stops], float)
    cs = np.array([s[1] for s in stops], float)
    out = np.empty(v.shape + (3,), np.float32)
    for k in range(3):
        out[..., k] = np.interp(v, xs, cs[:, k])
    return out


def ombrage(rel, z=3.0):
    g = rel.g
    h = gaussian_filter(rel.h.astype(np.float32), 0.6)
    dx = (g.km_px * 1000)[:, None]
    gy, gx = np.gradient(h)
    gx = gx / dx * z
    gy = gy / dx * z
    n = np.sqrt(gx * gx + gy * gy + 1)
    tot = np.zeros(h.shape, np.float32)
    for az, el, w in ((315, 40, 0.55), (270, 45, 0.2), (345, 55, 0.25)):
        a, e = math.radians(az), math.radians(el)
        L = (math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))
        tot += w * ((-gx * L[0] - gy * L[1] + L[2]) / n)
    return np.clip(tot, 0, 1)


def composer(couleur, om, rel, force_terre=0.75, force_eau=0.18):
    """Couleur × ombrage, avec un ombrage plus discret sous l'eau."""
    plat = 0.72  # valeur d'ombrage d'un terrain plat
    k = np.where(rel.eau, force_eau, force_terre)[..., None]
    f = 1 + k * (om[..., None] / plat - 1)
    return np.clip(couleur * f, 0, 255).astype(np.uint8)


def couleur_eaux(rel, base):
    L = rel.L
    c = base.copy()
    c[rel.ocean] = rampe(rel.h[rel.ocean], BATHY)
    c[rel.mer] = rampe(rel.h[rel.mer] - L, BATHY_HAL)
    for k, lac in enumerate(rel.lacs, start=1):
        m = rel.lac == k
        c[m] = rampe(rel.h[m] - lac["cfg"]["altitude_m"], LAC)
    gris = np.clip(200 + rel.h[rel.dehors] / 40, 185, 235)
    c[rel.dehors] = np.stack([gris, gris, gris * 0.99], -1)
    return c


def teintes_hypso(rel):
    c = rampe(rel.h, HYPSO)
    return couleur_eaux(rel, c)


def teintes_milieux(rel, mil):
    cl = mil["classes"]
    pal = np.zeros((256, 3), np.float32)
    for i, (_, _, hexa) in enumerate(MILIEUX):
        pal[i] = [int(hexa[j:j + 2], 16) for j in (1, 3, 5)]
    c = pal[cl]
    c = couleur_eaux(rel, c)
    r = cl == CODE["recif_corallien"]
    c[r] = 0.55 * c[r] + 0.45 * pal[CODE["recif_corallien"]]
    return c


def estomper(rgb, rel, om):
    """Dégradé vers un fond neutre au sud de la limite du Beliet (fondu)."""
    w = rel.fondu[..., None]
    if (w >= 1).all():
        return rgb
    gris = np.clip(214 + np.maximum(rel.h, 0) / 60, 205, 236)
    neutre = np.stack([gris, gris * 0.985, gris * 0.955], -1).astype(np.float32)
    neutre = neutre * (1 + 0.35 * (om[..., None] / 0.72 - 1))
    terre = (rel.terre | rel.dehors)[..., None]
    out = np.where(terre, rgb * w + neutre * (1 - w), rgb)
    return np.clip(out, 0, 255).astype(np.uint8)


def png_b64(arr, mode=None):
    buf = io.BytesIO()
    Image.fromarray(arr, mode).save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def jpg_b64(arr):
    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, "JPEG", quality=88, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


# --------------------------------------------------------------------------- géométrie

def chaikin(P, n=2):
    P = np.asarray(P, float)
    for _ in range(n):
        if len(P) < 3:
            break
        Q = 0.75 * P[:-1] + 0.25 * P[1:]
        R = 0.25 * P[:-1] + 0.75 * P[1:]
        mid = np.empty((2 * len(Q), 2))
        mid[0::2] = Q
        mid[1::2] = R
        P = np.vstack([P[:1], mid, P[-1:]])
    return P


def d_chemin(P, ferme=False, dec=1):
    if len(P) < 2:
        return ""
    s = "M" + " L".join(f"{x:.{dec}f},{y:.{dec}f}" for x, y in P)
    return s + ("Z" if ferme else "")


def contours_masque(masque, simpl=0.6, lisse=True, aire_min=4):
    """Polygones (en pixels) des zones True d'un masque."""
    out = []
    for geom, val in features.shapes(masque.astype(np.uint8), mask=masque, transform=Affine.identity()):
        poly = shape(geom).simplify(simpl, preserve_topology=True)
        if poly.area < aire_min:
            continue
        out.append(poly)
    return out


def anneaux_svg(poly, lisse=True):
    parts = []
    polys = [poly] if poly.geom_type == "Polygon" else list(poly.geoms)
    for pg in polys:
        for ring in [pg.exterior] + list(pg.interiors):
            P = np.array(ring.coords)
            if lisse and len(P) > 4:
                P = chaikin(P, 2)
            parts.append(d_chemin(P, ferme=True))
    return " ".join(parts)


# --------------------------------------------------------------------------- texte

class Texte:
    def __init__(self):
        self._polices = {}

    def police(self, fichier, taille):
        k = (fichier, round(taille, 1))
        if k not in self._polices:
            self._polices[k] = ImageFont.truetype(fichier, max(1, int(round(taille * 4))))
        return self._polices[k]

    @staticmethod
    def graphemes(t):
        out = []
        for ch in t:
            if out and unicodedata.combining(ch):
                out[-1] += ch
            else:
                out.append(ch)
        return out

    def largeur(self, t, fichier, taille, esp):
        f = self.police(fichier, taille)
        gs = self.graphemes(t)
        return [f.getlength(gr) / 4 + esp for gr in gs], gs


def echap(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


class Etiquettes:
    """Accumule les étiquettes en SVG (halo blanc + texte), lettre par lettre le long des courbes."""

    def __init__(self):
        self.halo, self.texte = [], []
        self.T = Texte()

    def _style(self, fichier, taille, couleur, ital):
        st = "italic" if fichier == POLICE_I else "normal"
        wt = "bold" if fichier == POLICE_B else "normal"
        return f'font-family="{FAMILLE}" font-size="{taille:.1f}" font-style="{st}" font-weight="{wt}"'

    def droit(self, x, y, t, taille, couleur, fichier=POLICE, esp=0.0, halo=3.0, ancre="middle", opac=1.0):
        st = self._style(fichier, taille, couleur, fichier == POLICE_I)
        ls = f' letter-spacing="{esp:.1f}"' if esp else ""
        if esp and ancre == "middle":
            # compense l'espacement final pour un centrage exact
            x += esp / 2
        if halo:
            self.halo.append(f'<text x="{x:.1f}" y="{y:.1f}" {st}{ls} text-anchor="{ancre}" fill="none" '
                             f'stroke="#ffffff" stroke-width="{halo:.1f}" stroke-linejoin="round" stroke-opacity="0.85">{echap(t)}</text>')
        self.texte.append(f'<text x="{x:.1f}" y="{y:.1f}" {st}{ls} text-anchor="{ancre}" fill="{couleur}" fill-opacity="{opac}">{echap(t)}</text>')

    def courbe(self, P, t, taille, couleur, fichier=POLICE, esp=0.0, halo=3.0, position=0.5, decalage=0.0):
        """Texte le long d'une polyligne P (pixels). Renvoie False si la courbe est trop courte."""
        P = np.asarray(P, float)
        if np.mean(np.diff(P[:, 0])) < 0:
            P = P[::-1]
        # rééchantillonnage régulier puis lissage fort : pas de virage serré sous les lettres
        from scipy.ndimage import gaussian_filter1d
        seg0 = np.hypot(*np.diff(P, axis=0).T)
        L0 = np.r_[0, np.cumsum(seg0)]
        if L0[-1] < 5:
            return False
        ss = np.linspace(0, L0[-1], max(4, int(L0[-1])))
        P = np.c_[np.interp(ss, L0, P[:, 0]), np.interp(ss, L0, P[:, 1])]
        sig = max(10.0, 1.6 * taille)
        P = np.c_[gaussian_filter1d(P[:, 0], sig, mode="nearest"), gaussian_filter1d(P[:, 1], sig, mode="nearest")]
        if decalage:
            d = np.gradient(P, axis=0)
            nrm = np.c_[-d[:, 1], d[:, 0]] / (np.hypot(d[:, 0], d[:, 1])[:, None] + 1e-9)
            P = P + nrm * decalage
        seg = np.hypot(*np.diff(P, axis=0).T)
        L = np.r_[0, np.cumsum(seg)]
        avances, gs = self.T.largeur(t, fichier, taille, esp)
        tot = sum(avances) - esp
        if tot > L[-1] * 0.98:
            return False
        s0 = (L[-1] - tot) * position
        st = self._style(fichier, taille, couleur, fichier == POLICE_I)
        s = s0
        h_parts, t_parts = [], []
        for a, gr in zip(avances, gs):
            w = a - esp
            c = s + w / 2
            x = np.interp(c, L, P[:, 0]); y = np.interp(c, L, P[:, 1])
            x1 = np.interp(c - max(w, taille * 0.6) / 2, L, P[:, 0]); y1 = np.interp(c - max(w, taille * 0.6) / 2, L, P[:, 1])
            x2 = np.interp(c + max(w, taille * 0.6) / 2, L, P[:, 0]); y2 = np.interp(c + max(w, taille * 0.6) / 2, L, P[:, 1])
            ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
            # ligne de base décalée pour centrer verticalement sur la courbe
            ox = -math.sin(math.radians(ang)) * -0.33 * taille
            oy = math.cos(math.radians(ang)) * 0.33 * taille
            X, Y = x + ox, y + oy
            if gr.strip():
                tr = f'transform="rotate({ang:.1f} {X:.1f} {Y:.1f})"'
                if halo:
                    h_parts.append(f'<text x="{X:.1f}" y="{Y:.1f}" {tr} text-anchor="middle">{echap(gr)}</text>')
                t_parts.append(f'<text x="{X:.1f}" y="{Y:.1f}" {tr} text-anchor="middle">{echap(gr)}</text>')
            s += a
        if halo:
            self.halo.append(f'<g {st} fill="none" stroke="#ffffff" stroke-width="{halo:.1f}" stroke-linejoin="round" '
                             f'stroke-opacity="0.85">' + "".join(h_parts) + "</g>")
        self.texte.append(f'<g {st} fill="{couleur}"><title>{echap(t)}</title>' + "".join(t_parts) + "</g>")
        return True


# --------------------------------------------------------------------------- principal

def tout(rel, p, reg, pluie, temp, hy, mil, hv, log=print):
    os.makedirs(os.path.join(SORTIE, "sig"), exist_ok=True)
    g = rel.g
    log("  ombrage et teintes…")
    om = ombrage(rel)
    rasters = {
        "relief": estomper(composer(teintes_hypso(rel), om, rel), rel, om),
        "milieux": estomper(composer(teintes_milieux(rel, mil), om, rel, force_terre=0.62), rel, om),
        "climat": estomper(composer(teintes_pluie(rel, pluie), om, rel, force_terre=0.45), rel, om),
    }

    log("  vecteurs…")
    vec = vecteurs(rel, p, reg, hy, mil, log)
    vec.update(vecteurs_climat(rel, pluie, hv))
    log("  étiquettes…")
    et = etiquettes(rel, p, reg, vec)

    # trois cartes : PNG pleine résolution + SVG à calques (rasters à demi-résolution pour rester légers)
    for mode in ("milieux", "relief", "climat"):
        rendre_png(assembler_svg(rel, p, rasters, om, vec, et, mil, mode, demi=False),
                   os.path.join(SORTIE, f"beliet_carte_{mode}.png"), log)
        chemin = os.path.join(SORTIE, f"beliet_carte_{mode}.svg")
        open(chemin, "w", encoding="utf-8").write(assembler_svg(rel, p, rasters, om, vec, et, mil, mode, demi=True))
        log(f"  {os.path.basename(chemin)} (calques) : {os.path.getsize(chemin) / 1e6:.1f} Mo")
    ancien = os.path.join(SORTIE, "beliet_carte.svg")
    if os.path.exists(ancien):
        os.remove(ancien)

    log("  données SIG…")
    exporter_sig(rel, p, reg, pluie, hy, mil, vec)
    exporter_climat(rel, pluie, hv, vec)
    log("  cartes d'altitude…")
    exporter_altitudes(rel)
    stats(rel, p, mil, pluie, hv, log)


FACIES_SVG = {
    1: ("Hiver Blanc", "#5a7fa8"), 2: ("Hiver Gris", "#5c6170"), 3: ("Hiver Jaune", "#a8801c"),
    4: ("Hiver de Vapeur", "#2f6b9c"), 5: ("Hiver pluvieux tempéré (hors matrice)", "#4d7a3c"),
}
DEFS_FACIES = (
    '<defs>'
    '<pattern id="motif_1" patternUnits="userSpaceOnUse" width="14" height="14">'
    '<rect width="14" height="14" fill="#ffffff" fill-opacity="0.62"/><circle cx="7" cy="7" r="1.6" fill="#5a7fa8"/></pattern>'
    '<pattern id="motif_2" patternUnits="userSpaceOnUse" width="12" height="12" patternTransform="rotate(45)">'
    '<rect width="12" height="12" fill="#6d7280" fill-opacity="0.16"/><line x1="0" y1="0" x2="0" y2="12" stroke="#5c6170" stroke-width="2.4" stroke-opacity="0.7"/></pattern>'
    '<pattern id="motif_3" patternUnits="userSpaceOnUse" width="18" height="18" patternTransform="rotate(-45)">'
    '<line x1="0" y1="0" x2="0" y2="18" stroke="#a8801c" stroke-width="2" stroke-opacity="0.55"/></pattern>'
    '<pattern id="motif_4" patternUnits="userSpaceOnUse" width="16" height="10">'
    '<line x1="0" y1="5" x2="16" y2="5" stroke="#e8f2fb" stroke-width="2" stroke-opacity="0.85"/></pattern>'
    '<pattern id="motif_5" patternUnits="userSpaceOnUse" width="16" height="16">'
    '<line x1="8" y1="0" x2="8" y2="16" stroke="#4d7a3c" stroke-width="1.8" stroke-opacity="0.55"/></pattern>'
    '</defs>')


def legende_climat(lx, g):
    """Légende de la carte du climat : précipitations et faciès |'Arin."""
    W, Hh = 1060, 560
    ly = g.H - Hh - 120
    o = [f'<g id="legende_climat"><rect x="{lx - 10:.0f}" y="{ly:.0f}" width="{W}" height="{Hh}" rx="6" fill="#ffffff" '
         f'fill-opacity="0.9" stroke="#6a5a48"/>']
    o.append(DEFS_FACIES)
    o.append(f'<text x="{lx + 10:.0f}" y="{ly + 42:.0f}" font-family="{FAMILLE}" font-size="28" font-weight="bold" fill="#3a2a1a">Précipitations annuelles</text>')
    seuils = [0, 100, 250, 500, 800, 1200, 1600, 2200, 3000]
    for i, mm in enumerate(seuils):
        r, v, b = rampe(np.array([mm + 1], float), PLUIE)[0]
        yy = ly + 62 + i * 40
        txt = f"< 100 mm" if mm == 0 else (f"> 3 000 mm" if mm == 3000 else f"{mm:,} mm".replace(",", " "))
        o.append(f'<rect x="{lx + 10:.0f}" y="{yy:.0f}" width="60" height="30" fill="rgb({int(r)},{int(v)},{int(b)})" stroke="#555" stroke-width="0.6"/>'
                 f'<text x="{lx + 84:.0f}" y="{yy + 23:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">{echap(txt)}</text>')
    for j, t in enumerate(("Isohyètes (mm/an) :", "50 · 100 · 250 · 500", "800 · 1 200 · 1 600 · 2 200")):
        o.append(f'<text x="{lx + 10:.0f}" y="{ly + 446 + j * 24:.0f}" font-family="{FAMILLE}" font-size="18" '
                 f'font-style="italic" fill="#24577a">{t}</text>')
    cx = lx + 400
    o.append(f'<text x="{cx:.0f}" y="{ly + 42:.0f}" font-family="{FAMILLE}" font-size="28" font-weight="bold" fill="#3a2a1a">Hivers du |’Arin (fin oct. → fin avr.)</text>')
    textes = {1: ["Hiver Blanc — manteau neigeux stable,", "cols fermés (§III)"],
              2: ["Hiver Gris — pluies froides, gel humide,", "sols saturés, glissements"],
              3: ["Hiver Jaune — gel nocturne, ciel clair,", "vents de poussière"],
              4: ["Hiver de Vapeur — brouillards", "d'advection sur la mer Halakhel"],
              5: ["Hiver pluvieux tempéré (Méditerranée,", "Atlas) — hors matrice canonique"]}
    for k, code in enumerate((1, 2, 3, 4, 5)):
        yy = ly + 66 + k * 68
        fond = "#4f86b5" if code == 4 else "#e9e3d3"
        o.append(f'<rect x="{cx:.0f}" y="{yy:.0f}" width="60" height="44" fill="{fond}"/>'
                 f'<rect x="{cx:.0f}" y="{yy:.0f}" width="60" height="44" fill="url(#motif_{code})" stroke="{FACIES_SVG[code][1]}" stroke-width="1.6"/>')
        for j, t in enumerate(textes[code]):
            o.append(f'<text x="{cx + 76:.0f}" y="{yy + 18 + j * 22:.0f}" font-family="{FAMILLE}" font-size="19" fill="#3a2a1a">{echap(t)}</text>')
    o.append(f'<text x="{cx:.0f}" y="{ly + 420:.0f}" font-family="{FAMILLE}" font-size="17" font-style="italic" fill="#3a2a1a">'
             f'Sans motif : hiver doux (tropiques, pas d\'|’Arin).</text>')
    o.append(f'<text x="{cx:.0f}" y="{ly + 446:.0f}" font-family="{FAMILLE}" font-size="17" font-style="italic" fill="#3a2a1a">'
             f'Matrice canonique exacte à 22,5° N (Gris dès 800 m, Blanc dès 2 400 m) ;</text>')
    o.append(f'<text x="{cx:.0f}" y="{ly + 470:.0f}" font-family="{FAMILLE}" font-size="17" font-style="italic" fill="#3a2a1a">'
             f'les limites remontent vers le sud (Blanc ≈ 3 500 m à 13° N).</text>')
    o.append("</g>")
    return "".join(o)


def teintes_pluie(rel, pluie):
    c = rampe(np.where(rel.terre, pluie, 0), PLUIE)
    return couleur_eaux(rel, c)


def vecteurs_climat(rel, pluie, hv):
    """Isohyètes et polygones des faciès |'Arin."""
    import contourpy
    g = rel.g
    v = {"isohyetes": [], "facies": []}
    Ps = gaussian_filter(np.where(rel.terre, pluie, np.nan_to_num(pluie)), 2.0)
    visible = rel.terre & (rel.fondu > 0.45)
    gen = contourpy.contour_generator(z=np.ma.masked_where(~visible, Ps), name="serial")
    for niv in ISOHYETES:
        for ligne in gen.lines(niv):
            if len(ligne) < 6:
                continue
            ls = LineString(ligne + 0.5).simplify(0.8)
            if ls.length > 40:
                v["isohyetes"].append((niv, np.array(ls.coords)))
    F = hv["facies"]
    for code in (3, 5, 2, 1, 4):
        m = (F == code) & ((rel.fondu > 0.45) | rel.mer)
        if m.any():
            for pg in contours_masque(m, simpl=1.0, aire_min=30):
                v["facies"].append((code, pg))
    return v


# --------------------------------------------------------------------------- vecteurs

def vecteurs(rel, p, reg, hy, mil, log):
    g = rel.g
    v = {}
    # côtes (continent + îles du Beliet), rivages Halakhel et lacs
    import contourpy
    from scipy.ndimage import binary_dilation
    oc = gaussian_filter(rel.ocean.astype(np.float32), 0.7)
    pres = binary_dilation(rel.terre, iterations=3) & (rel.fondu > 0.3)
    gen_c = contourpy.contour_generator(z=np.ma.masked_where(~pres, oc), name="serial")
    v["cotes"] = []
    for ligne in gen_c.lines(0.5):
        if len(ligne) < 4:
            continue
        ls = LineString(ligne + 0.5).simplify(0.5)
        if ls.length > 6:
            v["cotes"].append(np.array(ls.coords))
    v["halakhel"] = contours_masque(rel.mer, simpl=0.5)
    v["lacs"] = []
    for k, lac in enumerate(rel.lacs, start=1):
        v["lacs"].append((lac["cfg"], contours_masque(rel.lac == k, simpl=0.5)))
    v["dehors"] = contours_masque(rel.dehors & ~rel.decoupe, simpl=0.8, aire_min=30)
    # isohypses
    hs = gaussian_filter(rel.h, 1.6)
    hs = np.where(rel.terre & (rel.fondu > 0.5), hs, np.nan)
    gen = contourpy.contour_generator(z=hs, name="serial")
    iso = []
    for niv in (200, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000):
        for ligne in gen.lines(niv):
            if len(ligne) < 12:
                continue
            ls = LineString(ligne + 0.5).simplify(0.6)
            if ls.length < 18:
                continue
            iso.append((niv, np.array(ls.coords)))
    v["isohypses"] = iso
    log(f"    {len(iso)} isohypses")
    # réseau secondaire
    res = hy.reseau()
    sec = []
    for r in res:
        P0 = np.c_[r["x"], r["y"]]
        ok = rel.fondu[P0[:, 1].astype(int), P0[:, 0].astype(int)] > 0.6
        # morceaux continus dans la zone non estompée
        debut = None
        for i in range(len(P0) + 1):
            dedans = i < len(P0) and ok[i]
            if dedans and debut is None:
                debut = i
            if not dedans and debut is not None:
                P = P0[debut:i]
                debut = None
                if len(P) < 3 or (i < len(P0) and len(P) < 12):
                    continue
                ls = LineString(P).simplify(0.7)
                sec.append(dict(type=r["type"], P=chaikin(np.array(ls.coords), 2), Q=r["Q"], A=r["A"]))
    v["secondaires"] = sec
    log(f"    {len(sec)} tronçons de cours d'eau secondaires")
    # fleuves nommés (hors eau)
    nommes = []
    eau = rel.eau
    for F in rel.fleuves:
        for c in F["lignes"]:
            x, y = g.px(c[:, 0], c[:, 1])
            ix = np.clip(x.astype(int), 0, g.W - 1); iy = np.clip(y.astype(int), 0, g.H - 1)
            dedans = eau[iy, ix]
            # morceaux continus hors de l'eau
            debut = None
            for i in range(len(x) + 1):
                hors = i < len(x) and not dedans[i]
                if hors and debut is None:
                    debut = i
                if not hors and debut is not None:
                    fin = min(len(x), i + 1)
                    if fin - debut >= 3:
                        nommes.append(dict(cfg=F["cfg"], P=np.c_[x[debut:fin], y[debut:fin]]))
                    debut = None
    v["nommes"] = nommes
    # milieux vectorisés (demi-résolution)
    cl = mil["classes"][::2, ::2]
    polys = []
    terre2 = rel.terre[::2, ::2] & (rel.fondu[::2, ::2] > 0.5)
    for geom, val in features.shapes(cl, mask=terre2 | (cl == CODE["recif_corallien"]),
                                     transform=Affine.scale(2)):
        val = int(val)
        if val >= len(MILIEUX):
            continue
        pg = shape(geom).simplify(1.2, preserve_topology=True)
        if pg.area < 40:
            continue
        polys.append((val, pg))
    v["milieux"] = polys
    log(f"    {len(polys)} polygones de milieux")
    return v


# --------------------------------------------------------------------------- étiquettes

COUL_EAU = "#1f4f7a"
COUL_RELIEF = "#5a3a1c"
COUL_COL = "#3b2a1a"
COUL_REGION = "#4a4036"


def etiquettes(rel, p, reg, vec):
    g = rel.g
    E = Etiquettes()
    nom = lambda gid, k=0: nom_registre(reg, gid, k)

    # mers et océans
    for e in p.get("eaux_exterieures", []):
        x, y = g.px(*e["pos"])
        n = e["nom"]
        big = e["geo_id"].startswith("GEO_EXT")
        E.droit(x, y, n, 44 if big else 30, COUL_EAU, POLICE_I, esp=8 if big else 4, halo=0, opac=0.85)
    # Halakhel
    axe = p["halakhel"].get("axe_etiquette", [(8.0, 29.0), (12.0, 27.8), (16.0, 26.9), (20.0, 26.5), (24.0, 27.0)])
    P = np.array([g.px(lo, la) for lo, la in axe])
    P = lisser_polyligne(P, 10)
    E.courbe(P, nom("GEO_MER_HALAKHEL") and f"Mer {nom('GEO_MER_HALAKHEL')}", 60, COUL_EAU, POLICE_I, esp=22, halo=0)
    x, y = g.px(*p["halakhel"].get("pos_qibsan", (25.6, 27.9)))
    E.droit(x, y, nom("GEO_MER_HALAKHEL", 1), 30, COUL_EAU, POLICE_I, esp=4, halo=0, opac=0.85)
    # lacs
    for k, lac in enumerate(rel.lacs, start=1):
        m = rel.lac == k
        ys, xs = np.nonzero(m)
        cx, cy = xs.mean(), ys.mean()
        n = nom(lac["cfg"]["geo_id"])
        E.droit(cx, cy + 10, n, 34, COUL_EAU, POLICE_I, esp=3, halo=0)
        n2 = lac["cfg"].get("nom_secondaire")
        if n2:
            E.droit(cx, cy + 40, f"({n2})", 22, COUL_EAU, POLICE_I, halo=0)
    # chaînes
    for ax in rel.axes:
        ch = ax["cfg"]
        if not ch.get("nom"):
            continue
        n = nom(ch["geo_id"]) or ch["nom"]
        pts = np.array(ch["points"])[:, :2]
        P = np.array([g.px(lo, la) for lo, la in lisser_polyligne(pts, 10)])
        long_px = np.hypot(*np.diff(P, axis=0).T).sum()
        taille = 40 if "Urumati" in n else 28
        esp = max(4.0, min(40.0, (0.55 * long_px - len(n) * taille * 0.5) / max(1, len(n))))
        if not E.courbe(P, n, taille, COUL_RELIEF, POLICE_B if "Urumati" in n else POLICE, esp=esp, halo=4, decalage=0):
            x, y = P[len(P) // 2]
            E.droit(x, y, n, taille, COUL_RELIEF, POLICE_B, halo=4)
    # chaîne côtière : description (nom en lacune)
    pts = [c[:2] for c in next(c for c in p["chaines"] if c["geo_id"] == "GEO_ORO_COTIERE_N")["points"]][9:14]
    P = np.array([g.px(lo, la) for lo, la in lisser_polyligne(np.array(pts), 10)])
    E.courbe(P, "chaîne côtière septentrionale", 20, "#6b5a48", POLICE_I, esp=3, halo=3, decalage=-26)
    # massifs et sites
    for m in p.get("massifs", []):
        x, y = g.px(*m["centre"])
        n = nom(m["geo_id"]) or m["nom"]
        r = int(60)
        sub = rel.h[max(0, int(y) - r):int(y) + r, max(0, int(x) - r):int(x) + r]
        hmax = float(sub.max())
        yy, xx = np.unravel_index(np.argmax(sub), sub.shape)
        X, Y = max(0, int(x) - r) + xx + 0.5, max(0, int(y) - r) + yy + 0.5
        if m["geo_id"].startswith("GEO_SIT"):
            # site ponctuel : pas d'altitude calculée (le registre donne la sienne)
            X, Y = x, y
            E.texte.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="6" fill="none" stroke="{COUL_RELIEF}" stroke-width="2"/>')
            E.droit(X, Y - 14, n, 20, COUL_RELIEF, POLICE_I, halo=4)
            continue
        E.texte.append(f'<path d="M{X - 7:.1f},{Y + 6:.1f} L{X:.1f},{Y - 7:.1f} L{X + 7:.1f},{Y + 6:.1f}Z" fill="{COUL_RELIEF}"/>')
        E.droit(X, Y - 14, n, 24, COUL_RELIEF, POLICE_B, halo=4)
        E.droit(X, Y + 28, f"{hmax:,.0f} m".replace(",", " "), 18, COUL_RELIEF, POLICE, halo=3)
    # cols (positions calculées, altitudes canoniques) : symbole « )( » orienté selon la crête
    boites_cols = []
    for c in p.get("cols", []):
        x, y = g.px(*c["pos"])
        az = c.get("azimut_crete_px_deg", 0.0)
        if c.get("chaine", "").endswith("(escarpement)"):
            az = 90.0
        az = (az + 90) % 180 - 90
        E.texte.append(f'<text x="{x:.1f}" y="{y + 6:.1f}" transform="rotate({az:.1f} {x:.1f} {y:.1f})" '
                       f'font-family="{FAMILLE}" font-size="20" font-weight="bold" text-anchor="middle" '
                       f'fill="{COUL_COL}"><title>{echap(c["nom"])} — {c["altitude_m"]} m</title>)(</text>')
        n = nom(c["geo_id"]) or c["nom"]
        alt = f"{c['altitude_m']:,} m".replace(",", " ")
        # bloc nom + altitude ; huit positions essayées autour du symbole, sans chevaucher les autres cols
        lw = max(sum(E.T.largeur(n, POLICE_I, 15, 0)[0]), 8 * len(alt)) + 6
        lh = 34
        choix = [(0, -22), (0, 30), (lw / 2 + 14, 4), (-lw / 2 - 14, 4), (lw / 2 + 8, -20), (-lw / 2 - 8, -20),
                 (lw / 2 + 8, 28), (-lw / 2 - 8, 28)]
        for ox, oy in choix:
            bx0, by0 = x + ox - lw / 2, y + oy - lh / 2
            boite = (bx0, by0, bx0 + lw, by0 + lh)
            if not any(boite[0] < b[2] and b[0] < boite[2] and boite[1] < b[3] and b[1] < boite[3] for b in boites_cols):
                break
        boites_cols.append(boite)
        boites_cols.append((x - 12, y - 10, x + 12, y + 10))
        E.droit(x + ox, y + oy - 4, n, 15, COUL_COL, POLICE_I, halo=3)
        E.droit(x + ox, y + oy + 12, alt, 12, COUL_COL, POLICE, halo=2.5)
    # fleuves nommés
    for F in rel.fleuves:
        cfg = F["cfg"]
        noms = [nom(cfg["geo_id"], k) for k in range(len(cfg["noms"]))]
        noms = [n for n in noms if n]
        if not noms:
            continue
        lignes = [c for c in vec["nommes"] if c["cfg"] is cfg]
        if not lignes:
            continue
        Lg = max(lignes, key=lambda c: np.hypot(*np.diff(c["P"], axis=0).T).sum())
        P = chaikin(Lg["P"], 2)
        n = len(P)
        if len(noms) == 1:
            E.courbe(P[int(n * 0.25):int(n * 0.75)], noms[0], 24, COUL_EAU, POLICE_I, esp=2, halo=3, decalage=-14)
        else:
            E.courbe(P[int(n * 0.05):int(n * 0.45)], noms[0], 22, COUL_EAU, POLICE_I, esp=2, halo=3, decalage=-14)
            E.courbe(P[int(n * 0.55):int(n * 0.95)], noms[1], 24, COUL_EAU, POLICE_I, esp=2, halo=3, decalage=-14)
    # détroits, débouchés, deltas
    for d in p.get("detroits_et_debouches", []) + p.get("deltas", []):
        x, y = g.px(*d["pos"])
        n = nom(d["geo_id"]) or d["nom"]
        # un delta homonyme d'une passe (Šafāqil) porte « delta » : pas d'étiquette en double
        if d["geo_id"].startswith("GEO_DLT") and "delta" not in n.lower():
            n = "delta " + n
        E.droit(x, y - 10, n, 19, COUL_EAU, POLICE_I, halo=3)
    # régions
    for r in p.get("regions", []):
        x, y = g.px(*r["pos"])
        n = nom(r["geo_id"])
        txt = f"Désert du {n}" if r["geo_id"] == "GEO_DES_SUMDAN" else (reg[r["geo_id"]]["libelle"] if r["geo_id"] in reg else r["nom"])
        E.droit(x, y, txt, 34 * r.get("taille", 1), COUL_REGION, POLICE, esp=10 * r.get("taille", 1), halo=4)
    # archipels
    for a in p.get("archipels", []):
        x, y = g.px(*a["pos_etiquette"])
        E.droit(x, y, nom(a["geo_id"]) or a["nom"], 24, COUL_REGION, POLICE_I, esp=2, halo=3)
        if "ile_principale" in a:
            ip = a["ile_principale"]
            x, y = g.px(*ip["pos"])
            E.droit(x, y + 26, ip["nom"], 17, COUL_REGION, POLICE_I, halo=3)
    return E


# --------------------------------------------------------------------------- SVG

def graticule(g):
    out, lab = [], []
    for lon in range(-25, 55, 5):
        x, _ = g.px(lon, 0)
        out.append(f"M{x:.1f},0 L{x:.1f},{g.H}")
        lab.append((x + 6, 26, f"{abs(lon)}°{'O' if lon < 0 else ('E' if lon > 0 else '')}", "start"))
    for lat in range(0, 40, 5):
        _, y = g.px(0, lat)
        out.append(f"M0,{y:.1f} L{g.W},{y:.1f}")
        lab.append((g.W - 8, y - 6, f"{lat}°N" if lat else "0°", "end"))
    return " ".join(out), lab


def legende_svg(g, rel, mil, mode):
    """Cartouche : titre, légende, échelle, sources."""
    x0, y0 = 30, g.H - 30
    parts = []
    # titre (haut gauche)
    parts.append(f'<g id="titre"><rect x="24" y="24" width="760" height="150" rx="6" fill="#ffffff" fill-opacity="0.82" stroke="#6a5a48" stroke-width="1.5"/>'
                 f'<text x="44" y="86" font-family="{FAMILLE}" font-size="54" font-weight="bold" fill="#3a2a1a" letter-spacing="6">LE BELIET</text>'
                 f'<text x="46" y="124" font-family="{FAMILLE}" font-size="24" font-style="italic" fill="#4a3a2a">{echap(MODES[mode])}</text>'
                 f'<text x="46" y="156" font-family="{FAMILLE}" font-size="18" fill="#5a4a3a">Version {VERSION} · d\'après le Géosystème v3.1 et son registre · projection Web Mercator</text></g>')
    # échelle à 15° N
    kmpx = g.km_px_a(15)
    L = 1000 / kmpx
    sx, sy = 46, g.H - 60
    parts.append(f'<g id="echelle"><rect x="{sx - 16}" y="{sy - 52}" width="{L + 140}" height="84" rx="4" fill="#ffffff" fill-opacity="0.82"/>')
    for i in range(4):
        parts.append(f'<rect x="{sx + i * L / 4:.1f}" y="{sy - 12}" width="{L / 4:.1f}" height="10" fill="{"#3a2a1a" if i % 2 == 0 else "#ffffff"}" stroke="#3a2a1a" stroke-width="1"/>')
    for i, t in enumerate(("0", "250", "500", "750", "1 000 km")):
        parts.append(f'<text x="{sx + i * L / 4:.1f}" y="{sy + 16}" font-family="{FAMILLE}" font-size="16" text-anchor="{"start" if i == 4 else "middle"}" fill="#3a2a1a">{t}</text>')
    parts.append(f'<text x="{sx}" y="{sy - 24}" font-family="{FAMILLE}" font-size="16" font-style="italic" fill="#3a2a1a">Échelle valable à 15° N (Mercator : elle varie avec la latitude)</text></g>')
    # légende (bas, dans l'Atlantique sud)
    lx, ly = g.px(-26.2, 9.6)
    lx += 20
    if mode == "climat":
        parts.append(legende_climat(lx, g))
    elif mode == "relief":
        parts.append(f'<g id="legende_relief"><rect x="{lx - 10:.0f}" y="{ly:.0f}" width="560" height="560" rx="6" fill="#ffffff" fill-opacity="0.85" stroke="#6a5a48"/>')
        parts.append(f'<text x="{lx + 10:.0f}" y="{ly + 40:.0f}" font-family="{FAMILLE}" font-size="28" font-weight="bold" fill="#3a2a1a">Altitudes</text>')
        for i, (alt, col) in enumerate(reversed(HYPSO[1:])):
            yy = ly + 64 + i * 38
            alt_t = f"{alt:,} m".replace(",", " ")
            parts.append(f'<rect x="{lx + 10:.0f}" y="{yy:.0f}" width="60" height="30" fill="rgb({col[0]},{col[1]},{col[2]})" stroke="#555" stroke-width="0.6"/>'
                         f'<text x="{lx + 84:.0f}" y="{yy + 23:.0f}" font-family="{FAMILLE}" font-size="20" fill="#3a2a1a">{alt_t}</text>')
        parts.append("</g>")
    else:
        present = [i for i in range(len(MILIEUX)) if mil["stats"].get(MILIEUX[i][0], 0) > 0]
        n = len(present)
        cols = 2
        rows = math.ceil(n / cols)
        W = 1060
        Hh = 70 + rows * 36 + 14
        ly = g.H - Hh - 120
        parts.append(f'<g id="legende_milieux"><rect x="{lx - 10:.0f}" y="{ly:.0f}" width="{W}" height="{Hh}" rx="6" fill="#ffffff" fill-opacity="0.88" stroke="#6a5a48"/>')
        parts.append(f'<text x="{lx + 10:.0f}" y="{ly + 42:.0f}" font-family="{FAMILLE}" font-size="28" font-weight="bold" fill="#3a2a1a">Milieux (vocabulaire du Géosystème)</text>')
        for k, i in enumerate(present):
            cx = lx + 10 + (k // rows) * 520
            cy = ly + 62 + (k % rows) * 36
            code, lib, hexa = MILIEUX[i]
            parts.append(f'<rect x="{cx:.0f}" y="{cy:.0f}" width="44" height="26" fill="{hexa}" stroke="#555" stroke-width="0.6"/>'
                         f'<text x="{cx + 56:.0f}" y="{cy + 20:.0f}" font-family="{FAMILLE}" font-size="19" fill="#3a2a1a">{echap(lib)}</text>')
        parts.append("</g>")
    # sources (bas droite)
    parts.append(f'<text x="{g.W - 30}" y="{g.H - 24}" font-family="{FAMILLE}" font-size="16" text-anchor="end" fill="#555" fill-opacity="0.9">'
                 f'Relief de base : AWS Terrain Tiles (SRTM, ETOPO1, GMTED…) · cours d\'eau réels : Natural Earth · altérations : paramètres du Beliet</text>')
    return "".join(parts)


def assembler_svg(rel, p, rasters, om, vec, et, mil, mode, demi):
    g = rel.g
    W, H = g.W, g.H
    sl = (slice(None, None, 2), slice(None, None, 2)) if demi else (slice(None), slice(None))
    def img(arr, ident, label, visible=True, opac=1.0, extra=""):
        a = np.ascontiguousarray(arr[sl])
        b, typ = (jpg_b64(a), "jpeg") if demi else (png_b64(a), "png")
        vis = "" if visible else ' style="display:none"'
        return (f'<g inkscape:groupmode="layer" id="{ident}" inkscape:label="{label}"{vis}>'
                f'<image x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="none" opacity="{opac}" {extra} '
                f'xlink:href="data:image/{typ};base64,{b}"/></g>')
    o = []
    o.append(f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
             f'xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
             f'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" '
             f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    o.append(f'<title>Le Beliet — {MODES[mode].split(" — ")[0].lower()} v{VERSION}</title>')
    o.append(f'<desc>Grille Web Mercator : x = (longitude - {g.lon0}) × {g.K:.3f} ; '
             f'y = ({g.mtop:.6f} - ln(tan(π/4 + latitude/2))) × {g.R:.3f}. Paramètres : donnees/parametres_carte.yaml</desc>')
    o.append(f'<rect width="{W}" height="{H}" fill="#b0d0e6"/>')
    # un seul fond raster par fichier (léger) ; les autres versions sont dans leurs propres fichiers
    noms_fond = {"relief": "01 Relief — teintes d'altitude (ombrées)", "milieux": "02 Milieux — biomes (ombrés)",
                 "climat": "02 Climat — précipitations annuelles (ombrées)"}
    o.append(img(rasters[mode], f"calque_{mode}", noms_fond[mode]))
    # milieux vectoriels (masqués par défaut, éditables)
    if demi and mode == "milieux":
        o.append('<g inkscape:groupmode="layer" id="calque_milieux_vect" inkscape:label="03 Milieux — polygones éditables" style="display:none">')
        for code in range(len(MILIEUX)):
            ps = [pg for c, pg in vec["milieux"] if c == code]
            if not ps:
                continue
            d = " ".join(anneaux_svg(pg, lisse=False) for pg in ps)
            o.append(f'<path id="milieu_{MILIEUX[code][0]}" inkscape:label="{MILIEUX[code][1]}" d="{d}" '
                     f'fill="{MILIEUX[code][2]}" fill-rule="evenodd" stroke="none"/>')
        o.append("</g>")
    # climat : faciès |'Arin (motifs) et isohyètes
    vis = "" if mode == "climat" else ' style="display:none"'
    o.append(f'<g inkscape:groupmode="layer" id="calque_facies" inkscape:label="03b Hivers du |’Arin — faciès"{vis}>')
    o.append(DEFS_FACIES)
    for code, pg in vec.get("facies", []):
        o.append(f'<path inkscape:label="{FACIES_SVG[code][0]}" d="{anneaux_svg(pg, lisse=True)}" fill="url(#motif_{code})" '
                 f'fill-rule="evenodd" stroke="{FACIES_SVG[code][1]}" stroke-width="1.6" stroke-opacity="0.9"/>')
    o.append("</g>")
    o.append(f'<g inkscape:groupmode="layer" id="calque_isohyetes" inkscape:label="03c Isohyètes (mm/an)" fill="none" '
             f'stroke="#24577a" stroke-linejoin="round"{vis}>')
    for niv, P in vec.get("isohyetes", []):
        o.append(f'<path inkscape:label="{niv} mm" d="{d_chemin(chaikin(P, 2))}" stroke-width="{1.6 if niv in (250, 800, 1600) else 0.9}" '
                 f'stroke-opacity="0.75" stroke-dasharray="{"none" if niv in (250, 800, 1600) else "7 5"}"/>')
    for niv, P in vec.get("isohyetes", []):
        if len(P) > 60:
            x, y = P[len(P) // 2]
            o.append(f'<text x="{x:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="17" fill="#24577a" stroke="#ffffff" '
                     f'stroke-width="3" paint-order="stroke" text-anchor="middle">{niv}</text>'
                     f'<text x="{x:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="17" fill="#24577a" text-anchor="middle">{niv}</text>')
    o.append("</g>")
    # isohypses
    vis_iso = ' style="display:none"' if mode == "climat" else ""
    o.append('<g inkscape:groupmode="layer" id="calque_isohypses" inkscape:label="04 Courbes de niveau" '
             f'fill="none" stroke="#7a5532" stroke-linejoin="round"{vis_iso}>')
    for niv, P in vec["isohypses"]:
        maj = niv % 1000 == 0
        o.append(f'<path d="{d_chemin(P)}" stroke-width="{1.1 if maj else 0.55}" stroke-opacity="{0.55 if maj else 0.35}"/>')
    o.append("</g>")
    # hydrographie
    o.append('<g inkscape:groupmode="layer" id="calque_hydro" inkscape:label="05 Hydrographie" fill="none" '
             'stroke-linecap="round" stroke-linejoin="round">')
    for pg in vec["dehors"]:
        o.append(f'<path d="{anneaux_svg(pg)}" stroke="#8c8c8c" stroke-width="1.0"/>')
    o.append(f'<g id="cotes" stroke="#2f5f86" stroke-width="1.4">')
    for P in vec["cotes"]:
        o.append(f'<path d="{d_chemin(chaikin(P, 2))}"/>')
    o.append("</g>")
    o.append(f'<path id="GEO_MER_HALAKHEL" inkscape:label="Mer Halakhel (rivage)" d="{" ".join(anneaux_svg(pg) for pg in vec["halakhel"])}" stroke="#2f5f86" stroke-width="1.3"/>')
    for cfg, pgs in vec["lacs"]:
        o.append(f'<path id="{cfg["geo_id"]}" inkscape:label="{cfg["nom"]} (rivage)" d="{" ".join(anneaux_svg(pg) for pg in pgs)}" stroke="#2f5f86" stroke-width="1.2"/>')
    o.append('<g id="oueds" stroke="#7e98ad" stroke-width="0.9" stroke-dasharray="6 5" stroke-opacity="0.85">')
    for s in vec["secondaires"]:
        if s["type"] == "oued":
            o.append(f'<path d="{d_chemin(s["P"])}"/>')
    o.append("</g>")
    o.append('<g id="rivieres" stroke="#3d78ad">')
    for s in sorted(vec["secondaires"], key=lambda s: s["Q"]):
        if s["type"] != "perenne":
            continue
        w = 0.6 + 1.1 * math.log10(1 + s["Q"] / 40)
        o.append(f'<path d="{d_chemin(s["P"])}" stroke-width="{w:.2f}"/>')
    o.append("</g>")
    o.append('<g id="fleuves_nommes" stroke="#2f6aa3">')
    for f in vec["nommes"]:
        w = {1: 1.6, 2: 2.0, 3: 2.6, 4: 3.2}.get(f["cfg"].get("largeur", 2), 2.0)
        o.append(f'<path inkscape:label="{f["cfg"]["geo_id"]}" d="{d_chemin(chaikin(f["P"], 2))}" stroke-width="{w}"/>')
    o.append("</g></g>")
    # graticule
    d, lab = graticule(g)
    o.append('<g inkscape:groupmode="layer" id="calque_graticule" inkscape:label="06 Méridiens et parallèles">'
             f'<path d="{d}" fill="none" stroke="#33506b" stroke-width="0.8" stroke-opacity="0.3"/>')
    for x, y, t, a in lab:
        o.append(f'<text x="{x:.0f}" y="{y:.0f}" font-family="{FAMILLE}" font-size="18" fill="#33506b" fill-opacity="0.8" text-anchor="{a}">{t}</text>')
    o.append("</g>")
    # toponymie
    o.append('<g inkscape:groupmode="layer" id="calque_toponymie" inkscape:label="07 Toponymie">')
    o.append('<g id="halos">' + "".join(et.halo) + "</g>")
    o.append('<g id="noms">' + "".join(et.texte) + "</g></g>")
    # villes : calque vide prêt à l'emploi
    o.append('<g inkscape:groupmode="layer" id="calque_villes" inkscape:label="08 Villes et lieux (à compléter)"></g>')
    # habillage
    o.append('<g inkscape:groupmode="layer" id="calque_habillage" inkscape:label="09 Titre, légende, échelle">')
    o.append(legende_svg(g, rel, mil, mode))
    o.append("</g></svg>")
    return "\n".join(o)


def rendre_png(svg, chemin, log):
    import cairosvg
    try:
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=chemin)
    except Exception:
        open(chemin + ".echec.svg", "w", encoding="utf-8").write(svg)
        raise
    im = Image.open(chemin).convert("RGB")
    im.save(chemin, optimize=True)
    log(f"  {os.path.basename(chemin)} : {im.size[0]} × {im.size[1]} px, {os.path.getsize(chemin) / 1e6:.1f} Mo")


# --------------------------------------------------------------------------- SIG

def _ll(g, P):
    lon, lat = g.ll(P[:, 0], P[:, 1])
    return [[round(float(a), 4), round(float(b), 4)] for a, b in zip(lon, lat)]


def _poly_ll(g, pg):
    polys = [pg] if pg.geom_type == "Polygon" else list(pg.geoms)
    out = []
    for q in polys:
        out.append([_ll(g, np.array(q.exterior.coords))] + [_ll(g, np.array(r.coords)) for r in q.interiors])
    return {"type": "MultiPolygon", "coordinates": out}


def exporter_sig(rel, p, reg, pluie, hy, mil, vec):
    g = rel.g
    d = os.path.join(SORTIE, "sig")
    feats = []
    nom = lambda gid, k=0: nom_registre(reg, gid, k)
    def F(geom, **props):
        feats.append({"type": "Feature", "geometry": geom, "properties": props})
    F(_poly_ll(g, unary_union(vec["halakhel"])), geo_id="GEO_MER_HALAKHEL", nom=nom("GEO_MER_HALAKHEL"), type="MER",
      superficie_km2=round(float(rel.infos.get("halakhel_km2", 0))), statut="[PROPOSITION] placement")
    for cfg, pgs in vec["lacs"]:
        F(_poly_ll(g, unary_union(pgs)), geo_id=cfg["geo_id"], nom=nom(cfg["geo_id"]), type="LAC",
          altitude_m=cfg["altitude_m"], statut="[PROPOSITION] placement")
    for ax in rel.axes:
        ch = ax["cfg"]
        F({"type": "LineString", "coordinates": [[round(a, 4), round(b, 4)] for a, b in ax["ligne"]]},
          geo_id=ch["geo_id"], nom=nom(ch["geo_id"]), type="ORO", role="ligne de crête", statut="[PROPOSITION] placement")
    for F_ in rel.fleuves:
        cfg = F_["cfg"]
        for c in F_["lignes"]:
            F({"type": "LineString", "coordinates": [[round(a, 4), round(b, 4)] for a, b in c]},
              geo_id=cfg["geo_id"], nom=" / ".join(n for n in (nom(cfg["geo_id"], k) for k in range(len(cfg["noms"]))) if n),
              type="FLV", statut="[PROPOSITION] tracé")
    for m in p.get("massifs", []):
        F({"type": "Point", "coordinates": m["centre"]}, geo_id=m["geo_id"], nom=nom(m["geo_id"]), type="ORO")
    for c in p.get("cols", []):
        F({"type": "Point", "coordinates": c["pos"]}, geo_id=c["geo_id"], nom=nom(c["geo_id"]) or c["nom"], type="COL",
          altitude_m=c["altitude_m"], groupe=c["groupe"], chaine=c["chaine"], statut_passage=c.get("statut_passage"),
          cycle_hivernal=c.get("cycle_hivernal"), statut=c.get("statut"))
    for e in p.get("detroits_et_debouches", []) + p.get("deltas", []):
        F({"type": "Point", "coordinates": e["pos"]}, geo_id=e["geo_id"], nom=nom(e["geo_id"]), type=e["geo_id"].split("_")[1])
    for a in p.get("archipels", []):
        F({"type": "Point", "coordinates": a["pos_etiquette"]}, geo_id=a["geo_id"], nom=nom(a["geo_id"]), type="ARC")
    json.dump({"type": "FeatureCollection", "name": "beliet_geographie", "features": feats},
              open(os.path.join(d, "beliet_geographie.geojson"), "w", encoding="utf-8"), ensure_ascii=False)
    # cours d'eau secondaires
    feats = [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": _ll(g, s["P"])},
              "properties": {"type": s["type"], "debit_m3s": round(s["Q"], 1), "bassin_km2": round(s["A"])}}
             for s in vec["secondaires"]]
    json.dump({"type": "FeatureCollection", "name": "beliet_cours_eau", "features": feats},
              open(os.path.join(d, "beliet_cours_eau_secondaires.geojson"), "w", encoding="utf-8"))
    # milieux
    feats = [{"type": "Feature", "geometry": _poly_ll(g, pg),
              "properties": {"code": MILIEUX[c][0], "libelle": MILIEUX[c][1]}} for c, pg in vec["milieux"]]
    json.dump({"type": "FeatureCollection", "name": "beliet_milieux", "features": feats},
              open(os.path.join(d, "beliet_milieux.geojson"), "w", encoding="utf-8"), ensure_ascii=False)
    # GeoTIFF (EPSG:3857) — altitude et pluie à demi-résolution pour garder le dépôt léger
    import rasterio
    R = 6378137.0
    px = R * math.pi / 180 / g.K
    def profil(f):
        tr = Affine(px * f, 0, R * math.radians(g.lon0), 0, -px * f, R * g.mtop)
        return dict(driver="GTiff", width=g.W // f, height=g.H // f, count=1, crs="EPSG:3857", transform=tr,
                    compress="deflate", predictor=2)
    h2 = rel.h[: g.H // 2 * 2, : g.W // 2 * 2].reshape(g.H // 2, 2, g.W // 2, 2).mean(axis=(1, 3))
    with rasterio.open(os.path.join(d, "beliet_altitude.tif"), "w", dtype="int16", **profil(2)) as f:
        f.write(np.round(h2).astype(np.int16), 1)
    with rasterio.open(os.path.join(d, "beliet_milieux.tif"), "w", dtype="uint8", **{**profil(1), "predictor": 1}) as f:
        f.write(mil["classes"], 1)
        f.write_colormap(1, {i: tuple(int(MILIEUX[i][2][j:j + 2], 16) for j in (1, 3, 5)) + (255,) for i in range(len(MILIEUX))})
    p2 = np.where(rel.terre, pluie, 0)[: g.H // 4 * 4, : g.W // 4 * 4].reshape(g.H // 4, 4, g.W // 4, 4).mean(axis=(1, 3))
    with rasterio.open(os.path.join(d, "beliet_pluie_mm.tif"), "w", dtype="uint16", nodata=0, **profil(4)) as f:
        f.write(np.round(p2).astype(np.uint16), 1)
    json.dump({str(i): {"code": c, "libelle": l, "couleur": h} for i, (c, l, h) in enumerate(MILIEUX)} |
              {"252": "Dehors", "253": "Mer Halakhel", "254": "Océan"},
              open(os.path.join(d, "beliet_milieux_codes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def exporter_climat(rel, pluie, hv, vec):
    """Faciès |'Arin, températures d'hiver et isohyètes : GeoTIFF et GeoJSON."""
    import rasterio
    from .climat import FACIES
    g = rel.g
    d = os.path.join(SORTIE, "sig")
    R_ = 6378137.0
    px = R_ * math.pi / 180 / g.K
    def profil(f):
        tr = Affine(px * f, 0, R_ * math.radians(g.lon0), 0, -px * f, R_ * g.mtop)
        return dict(driver="GTiff", width=g.W // f, height=g.H // f, count=1, crs="EPSG:3857", transform=tr, compress="deflate")
    F = hv["facies"][: g.H // 2 * 2: 2, : g.W // 2 * 2: 2]
    with rasterio.open(os.path.join(d, "beliet_facies_arin.tif"), "w", dtype="uint8", **profil(2)) as f:
        f.write(F, 1)
    T = np.where(rel.terre, hv["Tw"], -99)[: g.H // 4 * 4: 4, : g.W // 4 * 4: 4]
    with rasterio.open(os.path.join(d, "beliet_temperature_hiver.tif"), "w", dtype="int16", nodata=-990, **profil(4)) as f:
        f.write(np.round(T * 10).astype(np.int16), 1)
    feats = [{"type": "Feature", "geometry": _poly_ll(g, pg),
              "properties": {"type": "FACIES_ARIN", "code": FACIES[c][0], "libelle": FACIES[c][1]}} for c, pg in vec["facies"]]
    feats += [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": _ll(g, P)},
               "properties": {"type": "ISOHYETE", "pluie_mm": niv}} for niv, P in vec["isohyetes"]]
    json.dump({"type": "FeatureCollection", "name": "beliet_climat", "features": feats},
              open(os.path.join(d, "beliet_climat.geojson"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"facies": {str(k): {"code": v[0], "libelle": v[1]} for k, v in FACIES.items()},
               "temperature_hiver": "°C × 10 (moyenne du cœur de l'hiver |'Arin-sukhì)", "seuil_blanc_c": hv["seuil_blanc"],
               "seuil_gris_c": hv["seuil_gris"]},
              open(os.path.join(d, "beliet_climat_codes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def exporter_altitudes(rel):
    d = os.path.join(SORTIE, "sig")
    h = rel.h
    # 16 bits : valeur = altitude + 10 000 (1 unité = 1 m)
    a16 = np.clip(np.round(h + 10000), 0, 65535).astype(np.uint16)[::2, ::2]
    Image.fromarray(a16).save(os.path.join(d, "beliet_altitude_16bits.png"))
    # Azgaar's Fantasy Map Generator : niveau 20 (sur 100) = rivage ; image en niveaux de gris
    terre = rel.terre | (rel.beliet & ~rel.eau) | rel.dehors
    hmax = float(h[terre].max())
    v = np.where(terre, 20 + 80 * np.clip(h, 0, None) / hmax, np.clip(19 + h / 300, 2, 19))
    Image.fromarray(np.round(v * 2.55).astype(np.uint8)[::2, ::2]).save(os.path.join(d, "beliet_altitude_azgaar.png"))


def stats(rel, p, mil, pluie, hv, log):
    g = rel.g
    A = g.aire_km2()
    s = {
        "version": VERSION,
        "terres_emergees_beliet_km2": round(float((A * rel.fondu)[rel.terre].sum())),
        "mer_halakhel_km2": round(float(A[rel.mer].sum())),
        "lacs_km2": {L["cfg"]["geo_id"]: round(float(A[rel.lac == k].sum())) for k, L in enumerate(rel.lacs, start=1)},
        "altitude_max_m": round(float(rel.h[rel.terre].max())),
        "milieux_km2": {k: round(v) for k, v in mil["stats"].items() if v > 0},
        "facies_arin_km2": {},
    }
    from .climat import FACIES
    for c, (code, _, _) in FACIES.items():
        s["facies_arin_km2"][code] = round(float((A * np.where(rel.mer, 1, rel.fondu))[(hv["facies"] == c) & (rel.terre | rel.mer)].sum()))
    json.dump(s, open(os.path.join(SORTIE, "sig", "beliet_statistiques.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log("  " + json.dumps({k: s[k] for k in ("terres_emergees_beliet_km2", "mer_halakhel_km2", "altitude_max_m")}))
