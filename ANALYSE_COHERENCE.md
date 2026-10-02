# Analyse de cohérence — carte du Beliet v0.3.1

Sources croisées :
- `references/GEOSYSTEME_GLOBAL_DU_BELIET_v3.1.md` (GEO) et `GEOSYSTEME_REGISTRE.v1.json` ;
- `LIEUX_URBAINS.v2.json` (LIEUX) : façades, suffixes d'identifiants (`_NO`, `_N`, `_NE`, `_SO`, `_SC`…), milieux ;
- `RESEAU_ROUTES.v3.json` (ROUTES) : 74 routes, modes de transport, façades reliées ;
- `PORTFOLIO_RESSOURCES.v2.json` : aucune donnée de localisation ;
- `MAP_BELIET_ORIGIN.svg` : contour.

L'illustration `TEST_Beliet_MAP.png` n'est **pas** utilisée. Aucun fichier du corpus ne donne de coordonnées : toutes les positions sont des [PROPOSITION] déduites des relations de voisinage croisées ci-dessous.

## 0. Changements

### v0.3.1 (retours de l'auteur sur la v0.3)

| Point | v0.3 | v0.3.1 | Fondement |
|---|---|---|---|
| Tùmázì | Sudd, 26,4-32,1° E | 22,0-27,7° E, 6,5-8,9° N (décalé de 4,4° vers l'ouest) | « Sud-Centre » (§V.5) ; demande de l'auteur |
| Kù-kɨ́bò | 24,9-27,1° E | 20,5-22,7° E, 6,25-7,6° N, au sud-ouest du lac | suit le lac ; « S lac », FOR_S |
| lóngò | ligne droite posée sur un plat | tracé arqué par l'Adrar des Ifoghas ; bifurcation adoucie depuis !Okheti ; socle de piémonts (+550 m sur ~270 km) ; trois contreforts (O vers le Tilemsi, NE vers l'Aïr, SO au-dessus du Mopámà) | réalisme ; URU_SO « piémonts escarpés au-dessus du Mopámà » |
| halekh, extrémité ouest | crête de 2 100 m surgissant d'une plaine plate | descente progressive vers la côte (550 m puis 1 200 m), socle de piémonts (+450 m sur ~230 km) | une chaîne ne naît pas d'un plat sans contreforts ; versants atlantiques (§I) |
| Socles | aucun | !Okheti +450 m ; k'ara +250 m | raccord des chaînes au plat pays |
| Étage montagnard | forêt dès 800 m sur toute l'emprise des chaînes | limites bruitées ; forêt si ≥ 720 mm, bois clair (herbage arboré) de 480 à 720 mm, steppe en dessous | bandes forestières moins géométriques ; versants NE de lóngò semi-arides (§I) |
| Limite sud | décalage uniforme | décalage variable : abaissée de ~1,2° au sud du Tùmázì ; plonge vers le sud à l'est pour garder toute la Corne | demande de l'auteur |
| Cols | absents | les 48 cols du registre sont placés (`donnees/cols.yaml`) ; altitude canonique imposée au relief | demande de l'auteur ; méthode en `ALIGNEMENT_CORPUS.md` §5 |

Toutes les corrections, mesures et positions destinées au corpus sont consignées dans `ALIGNEMENT_CORPUS.md`.

### v0.3

La v0.3 repart de la v0.1 (géographie posée sur le relief réel). Elle corrige les points relevés par l'auteur, chacun justifié par le croisement GEO / LIEUX / ROUTES.

| Point | v0.1 | v0.2 (abandonnée) | v0.3 | Fondement |
|---|---|---|---|---|
| Mer Halakhel | 23,5-31,5° N, 6-28° E, bras des chotts | bande rectiligne de -11,5 à 28° E, coupée en deux par un détroit | **une seule mer continue**, de -8 à 28,5° E, 23-31° N ; trois bassins reliés par des étranglements de 200-300 km | §V.1 « E : Mer Halakhel occidentale » ; suffixes `_NO` des façades HKL_NO, HKL_O, HKL_SO (§2) |
| Rivages | contour dessiné | contour dessiné, quasi rectiligne | contour enveloppe + relief réel : la mer envahit les bas-pays réels (Touat, Tidikelt, Ghadamès, Fezzan, Syrte, Qattara) et bute sur les plateaux (Tademaït, hamada al-Hamra, Tassili, Haruj) | rivages naturels, golfes et péninsules |
| Khreth-na-Serek | détroit vers le bras des chotts | détroit entre les deux bassins | passe de 12 km entre la côte NO et un promontoire nord, à l'entrée du golfe de Serek (vallée de la Saoura) | GEO §VI.1.3 « entre côtes NO Halakhel et promontoire N » |
| Cordillère | sur les massifs réels | arc rectiligne vers 20-21° N | tracé v0.1 sur les massifs réels (Adrar, Ahnet, Ahaggar, Djado, Tibesti, Ennedi, Marra ; lóngò à l'ouest de l'Aïr jusqu'à Jos), abaissé d'~1° dans l'ouest | demande de l'auteur ; « Y couché » de GEO §I |
| Mopámà | piémont du plateau de Jos | Fouta-Djalon | piémont sud-ouest de l'extrémité de lóngò (centre du Nigeria) | GEO §V.4 « N : lóngò » ; URU_SO « piémonts escarpés au-dessus du Mopámà » ; demande de l'auteur |
| Émissaire du Mopámà | Niger inférieur | vers le Geba | ~600 km vers le sud-ouest : gorges de Mù-wúlè, bas-pays du Mono, delta à mangroves | GEO §VI.3 (600 km, navigable) ; LIEUX : Kù-Bèláà, Mázì-Dúm en `foret_maree` |
| Ku-jálima-rir, golfe Jálondù, Li-sèk-dì | baie du Bénin | côte de Guinée-Bissau | golfe de Guinée à l'ouest du delta : anse Jálondù sur la côte de l'actuel Ghana, Li-sèk-dì au large, Ku-jálima-rir plus à l'ouest | demande de l'auteur (plus à l'ouest) ; lien avec l'émissaire (RT_003, RT_047, RT_060) |
| Tùmázì | Sudd | cuvette du Tchad | Sudd (v0.1) ; décalé vers l'ouest en v0.3.1 | GEO §V.5 « N : piémonts S de k'ara », « E : piémonts qoyra » ; RT_068 vers les Gîtes-Ts'idar (qoyra) |
| Kù-kɨ́bò | nord-ouest du lac | monts Mandara | au sud-ouest du lac, vers la forêt | GEO §V.5 relief « S lac » ; Q'eša-Kɨ́bò en TUM_SC + FOR_S |
| Mù-wúlè / Mù-dárhòbì | Borgou / Ouest camerounais | Fouta / monts Loma | ouest et sud du lac | GEO §I « bordure O », « massif S » |
| Ehukhtal | vers le bras des chotts | ~650 km | ~950 km : pied nord de halekh, débouché par le goulet Hlom-khetal | GEO : sources !Okheti, ~1 100 km, estuaire Akhidalet « côtes NO » |
| Madīlan | ~900 km | ~650 km | ~1 000 km avec la ria Tawālmaz | GEO : ~1 400 km, ria « plusieurs centaines de km » |
| Limite sud | frontières réelles | estompée | estompée (inchangé) | demande de l'auteur |

---

## 1. Le contour

Le contour est l'Afrique réelle en projection Web Mercator, géoréférencée sur quatre points (cap Vert, Ras ben Sakka, Ras Hafun, frontière Somalie–Kenya). Chaque point a une longitude et une latitude réelles. Le relief réel sert de graine ; les altérations du Beliet s'y ajoutent.

Réserves :
1. **Mesures.** Surface réelle 18,5 M km² pour ~15 M km² au corpus. Largeur 7 380 km (6 800 au corpus). Hauteur 4 320 km (5 200 au corpus).
2. **Limite sud.** Elle suivait des frontières politiques. Elle est remplacée par une limite lissée et estompée sur ~300 km.
3. **Îles.** Staur-Khlōr (Cap-Vert) est hors du contour ; le cadre est élargi vers l'ouest.

---

## 2. Croisement GEO / LIEUX / ROUTES pour la mer Halakhel

### 2.1 Façades

| Façade | GEO | LIEUX (suffixe d'identifiant, milieu) | ROUTES | Placement v0.3 |
|---|---|---|---|---|
| HKL_NO | rias et goulets NO ; estuaire Akhidalet « côtes NO » | Akhidalet, Kralekh-Aktrik, Aktrik-khem : `_NO` | RT_027 portage vers Khloreth-klam (ATL_NO) ; RT_002, RT_039 cabotage vers l'E | rive nord du bassin occidental, découpée en rias |
| HKL_O | goulets O intérieurs ; Hlom-khetal « entrée O », 35 km | Hlom-khetal : `_NO`, `littoral_rocheux` | RT_004, RT_018, RT_040 : cabotage S → O → NO puis portage | goulet à l'extrémité ouest, estuaire de l'Ehukhtal |
| HKL_SO | rias SO ; Imekh-stom « entrée SO » | Imekh-stom : `_NO` ; Akhileth (relais forestier) : `_NO` | RT_016, RT_035, RT_050 | goulet estuarien de l'Imikhrel, sud du bassin occidental |
| HKL_N | passes et détroits | Khreth-na-Serek, Serékh-khem : `_N`, `littoral_rocheux` | RT_005, RT_058 vers HKL_NO ; RT_041 vers HKL_NE | promontoire nord et golfe de Serek |
| HKL_S | rive S désertique, glacis | Cherbekh-khem : `_NO` ; Tawālmaz, Qabḍ-ār-Ǧanūb : `_NE` ; tous `littoral_rocheux` | RT_051 Bannaktì (halekh) → Cherbekh-khem ; RT_023 Tawālmaz → Abnaqil | rive sud de l'O à l'E : pied du Tassili, golfe du Fezzan, golfe de Koufra |
| HKL_NE | delta Abnuḥīl, levées irriguées | Qūrāš-Tanīqa, Ṣarīq : `_NE` | RT_006, RT_021, RT_024 : cols de k'ara vers HKL_NE | côte NE, vers Qattara |
| HKL_E | deltas Abnuḥīl / Ḥawqal, Maqbaṣ | Abnīqa, Ḥawqil, Abnaqil… : `_NE` | RT_012 à RT_015 | côte orientale |

Conclusion : la mer s'étend sur deux macro-régions. Sa moitié ouest (O, NO, SO, et la rive S jusqu'à Cherbekh-khem) relève du Nord-Ouest ; sa moitié est (Tawālmaz, deltas) relève du Nord-Est. La v0.1 la plaçait entièrement à l'est de 6° E et trop au nord. La v0.2 l'étirait en bande et la coupait en deux. La v0.3 en fait une seule mer, ancrée dans le NO et abaissée.

### 2.2 Les rivages suivent le relief réel
Le contour paramétré n'est qu'une enveloppe. Le rivage avance dans les bas-pays réels situés sous ~450 m et recule devant les plateaux. Il en résulte :
- **bassin occidental** sur Tindouf, le Touat et le Tidikelt ; rias au nord-ouest ;
- **étranglement du Tademaït** (~250 km), plateau réel en péninsule ;
- **bassin central** et **golfe de Ghadamès** au nord ; falaises du Tassili au sud ;
- **étranglement de la hamada al-Hamra** ; **golfe du Fezzan** au sud, où débouche la ria Tawālmaz ;
- **bassin oriental** sur Syrte, la Grande Mer de sable et Qattara, avec la **péninsule du Haruj** (volcans réels) et le **golfe de Koufra** vers l'Akhtir.

---

## 3. Incohérences du corpus et choix retenus

Chaque choix est réversible dans `donnees/parametres_carte.yaml`.

### 3.1 Dimensions de la mer
Quatre contraintes ne tiennent pas ensemble :
- « ~1 800 km × 600-900 km » (§VI.1) ;
- bordure orientale de la région NO (§V.1) et portage vers l'Atlantique (RT_027, « 3 jours ») ;
- interfluve de ~300 km jusqu'à l'Abnuḥīl (§V.2) ;
- 1 350 000 km².

**Choix v0.3 :** la superficie, l'ancrage NO et l'interfluve priment. La mer mesure ~3 500 km d'ouest en est. Sa largeur varie : ~350 km à l'ouest, 250 km aux étranglements, 450 km au centre, 650 km à l'est. Superficie obtenue : **1,28 M km²** (v0.3.1).

Conséquences :
- **Portage vers l'Atlantique** : l'extrémité ouest est à ~350 km de la côte (Tan-Tan, Sidi Ifni). « 3 jours » reste trop court ; un portage d'une à deux semaines par le Sas terrestre (Stakhr-Durek, oasis de Hloran-rir) est cohérent.
- **Portage vers la Méditerranée (5 jours)** : possible au nord du bassin oriental, où le Sumdan ne mesure que 130 à 250 km (golfe de Syrte).
- **Région NO** : de l'Atlantique à la mer, ~750 000 km² (850 000 au corpus).

### 3.2 Longueurs de la cordillère

| Chaîne | Corpus | Carte |
|---|---|---|
| halekh | 1 200 km | ~1 500 km |
| k'ara | 2 100 km | ~2 900 km, plus ~1 450 km de « continuité montagnarde » vers qoyra |
| lóngò | 1 800 km | ~1 650 km |
| qoyra | 1 400 km | ~2 000 km (plateaux réels) |

Le contour réel est plus large que le continent du corpus (§1). Les chaînes s'allongent d'autant.

### 3.3 Longueurs des fleuves

| Fleuve | Corpus | Carte (avec méandres) |
|---|---|---|
| Ehukhtal | ~1 100 km | ~950 km |
| Imikhrel | ~800 km | ~500 km |
| \|Na-madikh / Madīlan | ~1 400 km | ~1 000 km avec la ria |
| Émissaire du Mopámà | ~600 km | ~650 km |
| \|Na-khuwel / Ḥawqal | — | ~1 050 km |

L'Imikhrel reste court : ses « piémonts O » sont pris entre !Okheti et la rive sud. Pour l'allonger, il faudrait faire naître le fleuve plus à l'est, sur l'Ahaggar.

### 3.4 Halekh ne peut pas être l'Atlas
Halekh a des « versants sumdaniens arides (N) » : un désert s'étend au nord de la chaîne. Halekh va donc de la côte mauritanienne (face à Staur-Khlōr, RT_066) au nœud !Okheti (Ahnet). L'Atlas réel, absent du corpus, est **écrêté** à ~2 100 m ; il forme les « piémonts ondulés » de la région NO.

### 3.5 |'Ara-Sukhì attribué à deux chaînes
§I le place dans k'ara ; les sources de l'Imikhrel disent « |'Ara-Sukhì (||Urumati-lóngò) ». Le registre tranche : `partie_de GEO_ORO_URUMATI_KARA`. **Choix :** k'ara (Tibesti).

### 3.6 Kù-kɨ́bò au nord ou au sud du Tùmázì
§V.5 le place au sud du lac (« Relief ») et au nord (« Limites »). LIEUX tranche : Q'eša-Kɨ́bò est en TUM_SC **et FOR_S**. **Choix :** au sud-ouest du lac, vers la forêt.

### 3.6 bis Position du Tùmázì
« Sud-Centre » (§V.5) place le lac au centre de la moitié sud. Le Sudd (v0.3) était trop à l'est. **Choix v0.3.1 :** 22,0-27,7° E. Deux limites du corpus s'en trouvent plus lâches : « E : piémonts qoyra » (qoyra est à ~1 400 km) et les affluents venus des « plateaux SE ».

### 3.7 Sud-ouest

| Élément | GEO | ROUTES | LIEUX | Placement v0.3 |
|---|---|---|---|---|
| Mopámà | 800 m ; N : lóngò ; O : Mù-wúlè ; S : Mù-dárhòbì | RT_001 caravane vers Kù-békà (Tùmázì) ; RT_003, RT_060 fluvial vers Ku-jálima-rir | Kù-téka en MOP_SO + URU_SO | pied SO de l'extrémité de lóngò |
| Ku-jálima-rir | golfe occidental, mangroves, estuaires Mopámà | RT_042, RT_057 hauturier vers le NO ; RT_054 vers Jáli-Fè | port atlantique majeur, Gálu-kánda (chantiers navals) | golfe de Guinée, à l'ouest du delta |
| Anse Jálondù, Jáli-Fè | bassins d'eau douce du delta, arrière-mangrove | RT_055 Jáli-Fè ↔ Anses-Jálondù | Anses-Jálondù, Jáli-Fè | côte de l'actuel Ghana, de part et d'autre du delta |
| Li-sèk-dì | îlots secs au large de l'anse Jálondù | — | ZRS rattachée à l'ATL_SO | chapelet d'îlots au large |

Tensions restantes :
- **« E : ||Urumati-k'ara (piémonts) »** pour le bassin Mopámà (§V.4) : k'ara est loin au nord-est.
- **RT_029 et RT_047** (Mù-dárhòbì ↔ Tùmázì, fluvial et lacustre) : le Tùmázì est à ~2 000 km du Mopámà. La voie suppose le Bénoué, un portage, puis un affluent occidental du lac.
- **RT_046 Imekh-stom ↔ Ku-jálima-rir** en « maritime_cabotage » seul : impossible depuis une mer fermée ; un portage est nécessaire.

### 3.8 Longueur de l'Abnuḥīl
Le corpus annonce 6 800 km et 3,2 M km² de bassin. Ce sont les valeurs du Nil réel. Sur la carte, le système mesure ~3 600 km, car le confluent est dans le Beliet.

### 3.9 Autres points
- **Buhlela, « sources hors-Beliet E »** : à l'est se trouve la mer Rouge. Placé sur l'Atbara/Tekezé. **Non résolu.**
- **Akhileth** (HKL_SO) : « relais forestier » d'Imekh-stom. La forêt la plus proche est l'étage montagnard de !Okheti, à ~150 km.
- **HKL_S : glacis ou côte rocheuse.** L'index dit « glacis », LIEUX dit `littoral_rocheux`. La carte combine glacis et falaises (Tassili).
- **Gel de l'Halakhel** (§III) : à −20 m et 23-31° N, physiquement extrême ; non représenté.
- **Chaîne côtière septentrionale** : « ~1 200 km » au corpus ; la côte qu'elle borde mesure ~2 600 km.
- **Deux sens pour « Tanāḥil »** : affluent des plateaux SE (§VI.5) ou vallée des piémonts N de k'ara (§V.2, LIEUX). La carte suit le premier.
- **Registre** : `GEO_EXT_ATLANTIQUE` et `GEO_GLF_JALONDU` portent la même forme, « Jálondù ».

### 3.10 Surfaces
- Terres émergées : **~17,6 M km²** (zone estompée pondérée, v0.3.1).
- Mer Halakhel : **1,28 M km²** (1,35 au corpus).

---

## 4. Ce qui est [PROPOSITION]
- **Tracés et positions** : chaînes, mer Halakhel et golfe de Serek, lacs, fleuves dessinés, archipel de Li-sèk-dì.
- **Écrêtements** : Atlas, ligne du Cameroun.
- **Îles** : ~45 îles de l'Halakhel (Haruj volcanique, îles de passe, îlots côtiers).
- **Milieux** : issus d'un modèle climatique calibré sur 25 points de précipitations du corpus.

## 5. Absent de la v0.3
- **Les 48 cols** : le registre donne altitudes et interfaces, pas de positions.
- **Les 24 phénomènes** : zones décrites, non cartographiées.
- **Les villes** : le calque existe et il est vide. LIEUX ne donne aucune coordonnée ; les façades de la §2 indiquent où les placer.
