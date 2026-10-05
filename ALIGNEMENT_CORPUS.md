# Alignement du corpus — retours du chantier « carte du Beliet »

Ce document recense tout ce que le chantier de carte a **décidé, mesuré, ajouté, corrigé ou jugé impossible**, pour que ces éléments puissent être reportés dans le corpus (Géosystème, registre, LIEUX, ROUTES). Il est écrit pour être lu par un agent.

## Mode d'emploi

- **Coordonnées** : `[longitude, latitude]` en degrés décimaux WGS84 (longitude négative = ouest). Projection de la carte : Web Mercator (EPSG:3857).
- **Statuts** : `[CANON]` (déjà au corpus), `[PROPOSITION]` (choix de la carte, à canoniser ou rejeter), `[MESURE]` (valeur mesurée sur la carte générée), `[IMPOSSIBLE]` (contrainte du corpus qu'aucune géographie ne satisfait).
- **Fiches** : chaque fiche porte un identifiant `ALN-xxx`, un type et une action proposée pour le corpus.
  - Types : AJOUT, CORRECTION, PRÉCISION, CONFLIT TRANCHÉ, IMPOSSIBILITÉ.
  - Actions : « remplacer », « ajouter », « annoter », « trancher », « forger un nom » (skill `forge-ling`).
- **Sources de vérité, dans l'ordre** :
  1. `carte/sig/beliet_mesures.json` : mesures, positions et cols, lisibles par machine ; régénéré par `python3 outils/mesures_corpus.py`.
  2. `donnees/parametres_carte.yaml` et `donnees/cols.yaml` : décisions de placement.
  3. `carte/sig/beliet_geographie.geojson` : géométries (rivage réel de la mer, lacs, crêtes, fleuves, cols).
- **Version de référence** : carte v0.5. Les positions des versions antérieures (v0.1, v0.2) sont **caduques** ; voir §7.
- **Carte texte** : `carte/beliet_carte_ascii.md` (relief, eaux, milieux, répertoire des lieux, cols, lieux et routes du corpus ; une case = 0,5° × 0,5°).
- **Lieux et routes** (v0.5) : `LIEUX_ET_ROUTES.md` (méthode, constats, solutions, tables), `carte/sig/beliet_lieux_routes.json`, `carte/beliet_carte_lieux.png` ; synthèse en §9 (ALN-130 à ALN-181 ; révision après relecture de l'auteur : §9.6).

---

## 1. Positions à reporter (synthèse)

Le corpus ne donne aucune coordonnée. La carte fixe désormais les positions suivantes [PROPOSITION]. La liste exhaustive est générée en §8 et dans le JSON (`positions`, `cols`, `lacs`, `chaines`, `fleuves`).

| ID | geo_id | Élément | Position retenue | Action |
|---|---|---|---|---|
| ALN-001 | GEO_MER_HALAKHEL | Mer Halakhel | de -8,0° à 28,85° E ; de 23,0° à 31,2° N ; trois bassins (O, centre, E) d'un seul tenant | ajouter coordonnées et emprise |
| ALN-002 | GEO_LAC_TUMAZI | Tùmázì | 22,2-27,5° E ; 6,5-9,1° N ; centre 24,77° E 7,66° N ; 577 × 286 km | ajouter |
| ALN-003 | GEO_LAC_AKHTIR | Akhtir | 21,2-24,2° E ; 20,2-22,2° N, flanc N de k'ara ; à ~85 km du golfe de Koufra | ajouter |
| ALN-004 | GEO_LAC_MOPAMA | Mopámà | 5,0-7,3° E ; 9,1-11,0° N ; centre 6,08° E 10,10° N ; pied SO de l'extrémité de lóngò | ajouter |
| ALN-005 | GEO_ORO_URUMATI_* | Cordillère | axes de crête en §8 ; nœud !Okheti ≈ 0,75° E 23,75° N | ajouter |
| ALN-006 | GEO_COL_001 à 048 | 48 cols | §5 et §8 | ajouter positions ; altitudes inchangées |
| ALN-007 | GEO_DET_*, GEO_EST_*, GEO_DLT_* | Passes, goulets, estuaires, deltas | §8 | ajouter |
| ALN-008 | GEO_GLF_KUJALIMARIR, GEO_GLF_JALONDU, GEO_ARC_LISEKDI | Sud-ouest atlantique | golfe de Guinée, à l'ouest du delta du Mopámà ; golfe Ku-jálima-rir vers -5° E ; anse Jálondù sur la côte de l'actuel Ghana (-1,3° E) ; îlots au large (-2,4 à -0,45° E ; 4,5-4,95° N) ; étiquette du golfe Jálondù [-0,4 ; 4,6] (révision, ALN-146) | ajouter |
| ALN-009 | GEO_ARC_STAURKHLOR | Staur-Khlōr | archipel du Cap-Vert réel ; Khlōr-Naw = Fogo (-24,38° ; 14,95°) ; les dix îles : ALN-137 | ajouter |
| ALN-135 | LUR_*, ZRS_* | 56 cités, 18 zones secondaires, 21 extrémités de routes | `LIEUX_ET_ROUTES.md` table A ; `carte/sig/beliet_lieux_routes.json` (clé `lieux`) | ajouter coordonnées (v0.5) |

---

## 2. Ajouts : éléments créés par la carte (absents du corpus)

Les noms ci-dessous sont des **noms de travail** (géographie réelle ou description française). Ils ne doivent pas entrer tels quels dans le corpus : un endonyme est à forger pour chacun.

| ID | Élément | Description | Position | Action |
|---|---|---|---|---|
| ALN-010 | « golfe de Serek » | golfe nord de l'Halakhel, derrière la passe Khreth-na-Serek ; c'est la « connexion N » du §VI.1.3 | -2,6 à -0,95° E ; 29,95-31,2° N (vallée réelle de la Saoura) | forger un nom ; ajouter au registre (type golfe) |
| ALN-011 | Bassins de l'Halakhel | bassin occidental (Tindouf-Touat), central (Ghadamès-Fezzan), oriental (Syrte-Grande Mer de sable-Qattara) | voir §8 | forger trois noms (facultatif) |
| ALN-012 | Golfes de l'Halakhel | golfes de Ghadamès (N), du Tidikelt (S), du Fezzan (S, débouché de la ria Tawālmaz), de Syrte (N), de Koufra (S, vers l'Akhtir) | voir contour §8 | forger des noms ; rattacher aux façades (§4) |
| ALN-013 | Péninsules et caps | péninsule du Tademaït (étranglement occidental, ~250 km), cap de la hamada al-Hamra (étranglement central), péninsule du Haruj (volcanique, rive S du bassin oriental), falaises du Tassili (rive S, littoral rocheux) | voir §8 | forger des noms |
| ALN-014 | Îles de l'Halakhel | ~45 îles. Dont un groupe volcanique au large du Haruj (16,8-18,9° E ; 27,3-27,8° N), un îlot-récif dans la passe Khreth-na-Serek (-1,62° ; 29,72°) et des îlots côtiers (dunes stabilisées, rochers) | §8 | annoter (corpus : « ~40 îles ») |
| ALN-015 | Contreforts de lóngò | O vers le Tilemsi (2,6° 20,4° → 0,7° 18,9°, ≤ 2 300 m) ; NE vers l'Aïr (5,6° 16,6° → 8,4° 18,9°, ≤ 1 900 m) ; SO au-dessus du Mopámà (8,0° 12,9° → 5,6° 11,2°, ≤ 1 800 m) | §8 | ajouter comme parties de GEO_ORO_URUMATI_LONGO |
| ALN-016 | Socles de piémonts | bourrelets de piémont : halekh +450 m sur ~230 km, !Okheti +450 m sur ~200 km, k'ara +250 m sur ~260 km, lóngò +550 m sur ~270 km | — | annoter (piémonts « 800-1 600 m » du corpus) |
| ALN-017 | Prolongement SE de k'ara | « continuité montagnarde » k'ara → qoyra (§V.2) matérialisée : monts Nouba → escarpement éthiopien occidental, 24,4° 13,3° → 36,6° 8,7°, crêtes 2 100-2 800 m | §8 | ajouter (partie de k'ara ou chaîne à nommer) |
| ALN-018 | Delta du Mopámà | GEO_DLT_MOPAMA (déjà au registre, sans position) | ≈ 1,3° E ; 5,75° N | ajouter position |
| ALN-019 | Reliefs réels non documentés | Atlas (écrêté à ~2 100 m) et ligne du Cameroun (écrêtée à ~1 970 m) | zones en §8 | décider : documenter (piémonts NO ; hautes terres du SE de Mù-dárhòbì) ou laisser en relief anonyme |
| ALN-020 | Ergs | Grand Erg occidental, Grand Erg oriental, Calanscio, Erg Chech (pied N de halekh), Ténéré (versant NE de lóngò), cordons atlantiques, mer de sable de Selima, Bayouda | zones en §8 | forger des noms si utiles |
| ALN-021 | Dépressions salines | Ṣaraq (29,0-29,9° E ; 28,6-29,2° N) [CANON sans position] ; autres dépressions détectées sur le relief réel (chotts, Bodélé, Qattara) | §8 | ajouter position de Ṣaraq ; décider pour les autres |
| ALN-022 | Limite sud | le corpus dit « Sud : forêts tropicales » ; la carte estompe progressivement le sud. Elle est opaque jusqu'à ~4° N de 9 à 27° E, 5° N à 30° E, 2,7° N à 36° E et 1,5° N à 42° E. La Corne reste entière | table §8 | annoter (choix d'affichage, pas une frontière) |

---

## 3. Corrections de valeurs canoniques (remesurées)

Les valeurs « carte » sont mesurées sur la carte v0.3.2 (tables complètes en §8).

| ID | Objet | Corpus | Carte | Action proposée |
|---|---|---|---|---|
| ALN-030 | Halakhel, longueur × largeur | ~1 800 km × 600-900 km | 3 640 km ; largeur 110 km (goulet O) à 890 km (bassin E, golfe de Koufra), 200-450 km au centre (profil en §8) | remplacer |
| ALN-031 | Halakhel, superficie | 1 350 000 km² | 1 280 030 km² (-5 %) | conserver la valeur canonique, tolérance ±5 % |
| ALN-032 | Halakhel, profondeur max. | 1 700 m | 1 439 m (fond modélisé, bassin oriental) | conserver la valeur canonique |
| ALN-033 | Portage Halakhel O → Atlantique | « 3 jours » | 270 km au plus court, de la rive NO (-7,66° ; 28,08°) à la côte (-9,84° ; 29,55°) | remplacer par ~8-10 jours de caravane |
| ALN-034 | Portage Halakhel N → Méditerranée | « 5 jours » | 130 km au plus court (26,8° ; 30,2° → 27,5° ; 31,2°), 155-200 km au nord du bassin oriental | conserver ; préciser le lieu (bassin oriental) |
| ALN-035 | Caravanes Halakhel E → mer Rouge | « 8 jours » | 370 km au plus court | conserver (≈ 45 km/jour) |
| ALN-036 | Interfluve oriental | ~300 km | 245 km (bras d'Abnīqa) | conserver |
| ALN-037 | Région NO côtier atlantique | ~850 000 km² | estimation ~750 000 km² (Atlantique → mer, halekh → 35° N ; non mesurée : limites non tracées) | annoter |
| ALN-038 | Longueur de halekh | ~1 200 km | 1 797 km (côte mauritanienne → !Okheti) | remplacer |
| ALN-039 | Longueur de k'ara | ~2 100 km | 2 881 km, plus 1 444 km de prolongement SE | remplacer ou scinder (ALN-017) |
| ALN-040 | Longueur de lóngò | ~1 800 km | 1 736 km, plus trois contreforts (259, 392, 324 km) | conserver |
| ALN-041 | Longueur de qoyra | ~1 400 km | 2 020 km (plateaux réels) | remplacer |
| ALN-042 | Chaîne côtière septentrionale | ~1 200 km | 2 622 km (Tunisie → delta) | remplacer |
| ALN-043 | Ehukhtal | ~1 100 km | 918 km (cours calculé le long des vallées) | conserver |
| ALN-044 | Imikhrel | ~800 km | 536 km | remplacer, ou repousser ses sources sur l'Ahaggar |
| ALN-045 | \|Na-madikh / Madīlan | ~1 400 km | 808 km de fleuve + ~200 km de ria Tawālmaz | remplacer (~1 000 km) |
| ALN-046 | Émissaire du Mopámà | ~600 km | 653 km | conserver |
| ALN-047 | Tira-qoyra / Abnuḥīl | ~6 800 km ; bassin 3,2 M km² | ~3 600 km dans le Beliet | annoter : 6 800 km suppose des sources hors Beliet |
| ALN-048 | Superficie totale du Beliet | ~15 000 000 km² | 17,6 M km² de terres (zone estompée pondérée), plus 1,28 M km² de mer | remplacer |
| ALN-049 | Extension E-O / N-S | 6 800 km / 5 200 km | 7 380 km / 4 320 km (contour réel) | remplacer |
| ALN-050 | Staur-Khlōr | ~600 km de la façade SO | 737 km de Khlōr-Naw à la côte la plus proche ; 1 024 km jusqu'à l'extrémité O de halekh (RT_066) | annoter (~600-750 km) |
| ALN-051 | Points culminants | \|'Ara-Sukhì > 5 000 m ; halekh > 4 200 m ; qoyra > 4 600 m ; lóngò > 3 200 m | 5 350 m (17,81° ; 20,33°) ; 4 350 m (-6,54° ; 22,39°) ; 4 673 m (38,38° ; 13,22°) ; 3 454 m (nœud !Okheti) | conserver ; ajouter les positions |
| ALN-052 | Précipitations, écarts persistants du modèle | versant S humide de k'ara 1 000 mm ; piémonts NO 650 mm ; côte atlantique NO 450 mm ; Akhtir 750 mm ; piémonts SE 320 mm | 766 ; 474 ; 614 ; 630 ; 433 mm | annoter (modèle à vents dominants ; écarts locaux tolérés) |
| ALN-053 | Montagne et forêt | « forêts de montagne 800-2 400 m », prairies 2 400-3 600 m, périglaciaire > 3 600 m | v0.4 : étages exacts à 22,5° N, relevés vers le sud (forêt dès ~1 275 m, prairie dès ~2 875 m, périglaciaire dès ~4 075 m vers 10-13° N), abaissés au nord (prairie dès ~1 900 m vers 33° N) ; forêt si ≥ 720 mm/an, bois clair 480-720 mm, steppe en dessous ; glaciers actifs si T annuelle ≤ −5 °C (k'ara), relictuels ≤ −2,5 °C (halekh), aucun sur qoyra | remplacer par la table « Limites par latitude » (§8) ; voir ALN-119 |

---

## 4. Façades de la mer Halakhel (positions pour les villes à venir)

Segments de rivage recommandés pour placer les lieux de LIEUX, déduits des suffixes `_NO` / `_N` / `_NE` et des routes.

| Façade | Segment de rivage (carte v0.3.2) | Lieux du corpus | Remarques |
|---|---|---|---|
| HKL_O | goulet Hlom-khetal, extrémité ouest (-7,9 à -6,5° E ; 27,2-27,8° N) | Hlom-khetal | estuaire de l'Ehukhtal ; Akhidalet en amont (-8,2° ; 27,0°) |
| HKL_NO | rive nord du bassin occidental, de -6,5° à -2,0° E (28,3-29,7° N) ; rias | Akhidalet, Kralekh-Aktrik, Aktrik-khem | point de départ du portage RT_027 vers Khloreth-klam : rive NO la plus proche de l'Atlantique |
| HKL_N | passe Khreth-na-Serek (-1,9 à -1,6° E ; 29,6-30,2° N), golfe de Serek, puis rive nord jusqu'au golfe de Ghadamès (~9° E) | Khreth-na-Serek, Serékh-khem | Serékh-khem dans le golfe ou à l'entrée de la passe |
| HKL_SO | rive sud du bassin occidental, de -6,5° à 3,5° E ; goulet Imekh-stom (0,0-0,55° E ; 25,35-26,5° N) | Imekh-stom, Akhileth (relais) | Akhileth « forestier » : l'étage forestier le plus proche est !Okheti, à ~150 km |
| HKL_S | rive sud de 3,5° à ~26° E : Tidikelt, falaises du Tassili, golfe du Fezzan (ria Tawālmaz), péninsule du Haruj, golfe de Koufra | Cherbekh-khem (_NO : partie ouest, 2-5° E), Tawālmaz (_NE : ria, 12,8-14,6° E), Qabḍ-ār-Ǧanūb (_NE : partie est) | littoral rocheux (LIEUX) et glacis (index) combinés |
| HKL_NE | rive nord du bassin oriental, golfe de Syrte → Qattara (15-28° E) ; arrière-pays : bassin de l'Abnuḥīl | Qūrāš-Tanīqa, Qūrāš-Taniḥīl-Ramšūr, Ṣarīq, Ḥamaḍ-Rās, Qūrāš-Ṣafīḥ | v0.5.2 : la haute Tanāḥil est le canyon au nord du col Abnī-tɨra, affluent occidental de l'Abnuḥīl (ALN-136 révisé, ALN-182) ; Ṣarīq au marais de Ṣaraq ; Ḥamaḍ-Rās sur un cap (28,17° ; 29,31°) |
| HKL_E | côte orientale (26-28,5° E ; 25-29° N) : Abnīqa (28,35° ; 27,6°), Ḥawqil (26,85° ; 25,35°) | Abnaqil, Tanāqil, Abnīqa, Qabṣūr-Qibṣ, Ḥawqil ; Tanāḥil (à la confluence Tanāḥil-Abnuḥīl, 32,55° ; 15,61°) | v0.5 : cône deltaïque d'Abnīqa à deux chenaux (Abnīṣar NE, Tanīlḥa SE, ALN-132), Abnaqil à l'apex |

---

Positions retenues pour tous les lieux de ces façades : `LIEUX_ET_ROUTES.md` §2 et table A.

## 5. Les 48 cols

### 5.1 Méthode
1. **Interface → tronçon.** Chaque groupe de cols du §I correspond à une interface entre deux peuples. On lui associe le tronçon de chaîne qui sépare leurs territoires :
   - **Šamqiriyyūn ↔ Tɨrakh (001-009)** : k'ara du Tibesti au Marra, puis monts Nouba. Plaines NE (Abnuḥīl, interfluve) ↔ hautes terres centrales.
   - **Qoyra-ña-ra ↔ Tɨrakh (010-017)** : prolongement SE de k'ara, de 29° E à la jonction avec qoyra (cirque de !Ayk-ma-‖Ixa).
   - **Ba-mbaro ↔ Halaktim (018-023)** : extrémité ouest de halekh. Versant atlantique humide ↔ cordons dunaires du NO (« corridor tropical humide vers dunes »).
   - **Ba-mbaro ↔ Tɨrakh (024-029)** : lóngò. Forêts du SO ↔ hautes terres (« forêt vers Haute Montagne »).
   - **Halaktim ↔ Tɨrakh (030-043)** : halekh central et oriental, !Okheti, k'ara occidental jusqu'à 8,5° E. Piémonts NO et rive S de l'Halakhel ↔ Centre.
   - **Šamqiriyyūn ↔ Qoyra-ña-ra (044-048)** : rebord N et O de l'escarpement de qoyra. Déserts du NE ↔ hauts plateaux (« désert vers Hauts Plateaux »).
2. **Profil de crête.** Le long de chaque tronçon, on mesure tous les 6 km le point le plus haut du transect perpendiculaire. Les minima locaux, avec une remontée d'au moins 80 m de part et d'autre, sont les ensellements naturels.
3. **Attribution.** Les cols sont traités du plus bas au plus haut. Chacun reçoit l'emplacement libre dont l'altitude de crête est la plus proche de son altitude canonique, les ensellements étant préférés. Trois contraintes s'appliquent :
   - un espacement minimal par groupe (55 à 140 km) ;
   - les cols d'un même **territoire** du registre (ETH, SHQ, TSD, IXA, URM, KOL, TNQ) restent à moins de 420 km les uns des autres ;
   - deux indices de nom ou de texte sont respectés : T'iqur-ɨlkh « bordé par le cirque de !Ayk-ma-‖Ixa » et Ku-Pámà-Tɨra-te (« Pámà », Mopámà) au-dessus du lac.
4. **Altitude exacte.** Le relief est entaillé quand la crête est trop haute. Quand elle est trop basse, une selle est relevée. Chaque col a donc **exactement** son altitude canonique sur la carte. Les cols d'escarpement (044-048) sont placés au rebord, à la première cote égale à leur altitude en venant du désert.

### 5.2 Résultats
Table complète (position, altitude, crête d'origine, statut de passage, routes) : §8, « Les 48 cols », et `donnees/cols.yaml`.

### 5.3 Remarques pour le corpus
- **ALN-060 — Kurel-ahek** (« carrefour caravanier NE-Centre ») : placé sur le premier ensellement des monts Nouba, à 2 150 m, avec Šaqra-t'em à proximité. Le pidgin Kurr-Šaqra (EVT_LING_KURR_SAQRA_CRISTALLISATION_-200) naît donc dans ce secteur.
- **ALN-061 — Territoire ETH** (Abnī-tɨra, Maḥēl-!ara, Ṭubayl) : regroupé sur le Tibesti oriental et l'Ennedi. Abnī-tɨra est relié par RT_064 à Zagakh-TƗr, sur l'émissaire de l'Akhtir, au nord.
- **ALN-062 — Territoire KOL** (Kurahek, Hlenik-k'eso, Pēlakh-t'sira) : regroupé sur halekh occidental (-10 à -8,7° E).
- **ALN-063 — Cols relevés.** Neuf cols ont une altitude canonique supérieure à la crête naturelle de leur secteur : quatre sur le prolongement SE de k'ara (jusqu'à +440 m pour K'elis-‖ara), quatre sur lóngò (+80 à +190 m), un sur halekh occidental (+200 m). Une selle a été relevée. Le prolongement SE de k'ara et lóngò sont donc plus bas que plusieurs cols du registre ; relever leurs crêtes, ou abaisser ces altitudes, est à trancher.
- **ALN-064 — Ba-mbaro ↔ Halaktim.** Placés sur l'extrémité ouest de halekh, la seule interface directe entre le SO humide et le NO aride. Deux noms (Ku-Pámà-Rikh-te, Ku-Mázì-Klek-te) évoquent le Mopámà, à ~1 800 km. À trancher : soit l'interface passe ailleurs, soit ces noms viennent d'une diaspora.
- **ALN-065 — Interfaces absentes.** Le corpus ne prévoit aucun col Šamqiriyyūn ↔ Halaktim ni Ba-mbaro ↔ Qoyra-ña-ra. C'est cohérent : ces peuples ne sont pas séparés par la cordillère.
- **ALN-066 — 48 « carrossables » (1 600-2 800 m).** Le registre va jusqu'à 3 200 m (Ṭanīkhūr). La fourchette du §I est à élargir.

---

## 6. Impossibilités et conflits tranchés

| ID | Type | Objet | Constat | Décision de la carte | Action proposée |
|---|---|---|---|---|---|
| ALN-070 | IMPOSSIBILITÉ | Dimensions de l'Halakhel | « 1 800 × 600-900 km » est incompatible avec quatre autres contraintes : l'ancrage NO (§V.1, suffixes `_NO`), l'interfluve de 300 km, le portage de 3 jours et 1,35 M km² | ancrage NO + interfluve + superficie | remplacer les dimensions (ALN-030) |
| ALN-071 | IMPOSSIBILITÉ | RT_046 Imekh-stom ↔ Ku-jálima-rir en « maritime_cabotage » seul | mer fermée | — | ajouter un segment `terrestre_portage` (275 km, confirmé en v0.5 ; dix autres routes dans le même cas : ALN-172) |
| ALN-072 | IMPOSSIBILITÉ | Gel de l'Halakhel (§III) | mer à −20 m, 23-31° N ; Tw des rives > 10 °C (ALN-117) | non représenté ; Hiver de Vapeur sur la carte du climat | requalifier (brouillards, givre de rive) |
| ALN-073 | IMPOSSIBILITÉ | Buhlela « sources hors-Beliet E » | à l'est se trouve la mer Rouge | Atbara/Tekezé | requalifier (« sources aux confins NE de qoyra ») |
| ALN-074 | CONFLIT TRANCHÉ | \|'Ara-Sukhì : k'ara ou lóngò | §I contre sources de l'Imikhrel | k'ara (registre) | corriger la mention « (\|\|Urumati-lóngò) » des sources de l'Imikhrel |
| ALN-075 | CONFLIT TRANCHÉ | Kù-kɨ́bò au N ou au S du Tùmázì | §V.5 relief contre limites | au SO du lac, vers la forêt (FOR_S) | corriger « N : ... chaîne Kù-kɨ́bò » |
| ALN-076 | CONFLIT TRANCHÉ | HKL_S : glacis ou côte rocheuse | index contre LIEUX | les deux : falaises du Tassili, glacis ailleurs | annoter |
| ALN-077 | CONFLIT TRANCHÉ | Halekh ≠ Atlas | « versants sumdaniens arides (N) » | halekh de la côte mauritanienne à !Okheti ; Atlas écrêté | annoter |
| ALN-078 | CONFLIT TRANCHÉ | Tawālmaz « zone nord-centrale côtière » | la Madīlan vient du sud | ria sur la rive S (golfe du Fezzan) | corriger le libellé |
| ALN-079 | CONFLIT TRANCHÉ | HKL_NO « rias/goulets NO (Ehukhtal/Imikhrel) » | Imekh-stom est l'entrée SO | Imikhrel au SO | corriger l'index des façades |
| ALN-080 | CONFLIT TRANCHÉ | Limites des bassins Mopámà et Tùmázì | « E : k'ara (piémonts) » ; « E : piémonts qoyra » | Mopámà central, Tùmázì au Sud-Centre (22-27,7° E) | assouplir les deux limites E |
| ALN-081 | CONFLIT TRANCHÉ | Mangroves au bord du Mopámà | Ku-Bèláà, Mázì-Dúm en `foret_maree`, lac à 800 m | la façade MOP_SO inclut l'estuaire de l'émissaire, à ~650 km ; v0.5 : les deux cités sont dans les mangroves du delta (ALN-131) | annoter MOP_SO |
| ALN-082 | CONFLIT TRANCHÉ | RT_029, RT_047 Mù-dárhòbì / côte SO ↔ Tùmázì (fluvial + lacustre) | ~2 000 km entre les bassins | voie Bénoué + portage + affluent occidental du lac ; v0.5 : portage mesuré de ~440 km (RT_047) ; RT_029 : ALN-166 | annoter les routes (ajouter le portage) |
| ALN-083 | CONFLIT TRANCHÉ | Deux sens de « Tanāḥil » | affluent des plateaux SE (§VI) ou vallée des piémonts N de k'ara (§V.2, LIEUX) | **rouvert en v0.5.2 (ALN-136 révisé, ALN-182)** : deux objets distincts. Le fleuve Tanāḥil (Tira-ñara) descend des plateaux SE jusqu'au confluent de Tanāḥil ; la haute Tanāḥil est le canyon au nord du col Abnī-tɨra, autre affluent de l'Abnuḥīl | registre : rattacher GEO_VAL_HAUTE_TANAHIL à GEO_FLV_ABNUHIL ; forger un nom pour le cours d'eau du canyon, ou renommer la vallée |
| ALN-084 | CONFLIT TRANCHÉ | ATL_INS « ~40 îles : dunes stabilisées, volcans éteints... » | phrase des îles de l'Halakhel ; Staur-Khlōr = 10 îles | — | corriger l'index |
| ALN-085 | CONFLIT TRANCHÉ | Registre : GEO_EXT_ATLANTIQUE porte la forme « Jálondù » | doublon avec GEO_GLF_JALONDU | — | corriger le registre |
| ALN-086 | CONFLIT TRANCHÉ | Orientation de lóngò | « NO-SE » | conservée (nœud !Okheti → Jos) ; versants SO humides, NE semi-arides | conserver |
| ALN-087 | CONFLIT TRANCHÉ | Position du Tùmázì | « Sud-Centre » (§V.5) contre « E : piémonts qoyra » | Sud-Centre : 22,2-27,5° E (qoyra à ~1 470 km du centre du lac) | assouplir « E : piémonts qoyra » en « E : vers les piémonts de qoyra » |
| ALN-088 | IMPOSSIBILITÉ | Superficie des sous-régions | sous-régions détaillées ≈ 10 M km² + Halakhel, pour ~15 M km² au total ; la carte compte 17,6 M km² | — | recalculer les superficies régionales sur la carte (limites à tracer) |

---

## 6 bis. Audits externes vérifiés (v0.4)

Deux audits externes ont été soumis. Chaque point est vérifié par mesure sur la carte ou par le modèle physique (§8, « Climat »). Un point n'est retenu que s'il est fondé.

### Audit « cartes physique / milieux » (sur la v0.3.2)

| ID | Point de l'audit | Vérification | Verdict | Action |
|---|---|---|---|---|
| ALN-100 | « Forêt tropicale humide » dans le delta de Šafāqil (lu « Solaqi ») | classes mesurées sur 29,8-32,4° E × 30-31,7° N : plaine alluviale 74 %, fourré côtier sec 22 %, steppe 4 %, forêt tropicale 0 % | **non fondé** : confusion de teinte (vert vif de la plaine alluviale) | aucune sur le classement ; le canon (« terres alluviales fertiles ») est déjà conforme |
| ALN-101 | (relevé en vérifiant) formes géométriques dans le même secteur | delta dessiné par un rectangle de coordonnées ; Ṣaraq rectangulaire ; fourré côtier coupé net à 29,5° N ; autres limites rectilignes (cordons dunaires à −8°, côte désertique à 30° E, remontées salines à 25° E, oasis karstiques) | **fondé** (artefacts) | corrigé en v0.4 : delta en éventail le long des bras ; Ṣaraq irrégulier ; limites adoucies et bruitées |
| ALN-102 | (relevé en vérifiant) nom « Šafāqil » affiché deux fois (passe et delta) | deux étiquettes homonymes superposées : origine probable de la lecture « Solaqi » | **fondé** | delta étiqueté « delta Šafāqil » |
| ALN-103 | (relevé en vérifiant) zones confondables | forêt de montagne (#3e6b45) et forêt tropicale (#1f5a32) presque identiques ; aucune autre confusion de classe trouvée (glaciers : k'ara 1 516 km² et halekh relictuel, aucun ailleurs ; forêt tropicale : aucune au nord de 16° N hors versants atlantiques) | **fondé** (lisibilité) | forêt de montagne éclaircie (#5f8466) |
| ALN-104 | Confirmations (étagement, dissymétrie de qoyra, lóngò, endoréisme, glaciers du \|'Ara-Sukhì) | vérifiées | conservées | l'étagement est désormais modulé par la latitude, exact à 22,5° N (ALN-119) |

### Audit « cohérence physique du cycle \|'Arin » (antérieur aux cartes)

Méthode : un modèle d'hiver est ajouté au modèle climatique (§8, « Climat »). Il est calé pour que la matrice canonique (Gris dès 800 m, Blanc dès 2 400 m) soit **exacte** à 22,5° N (halekh). Ailleurs, la physique fixe les limites : l'hiver est plus doux vers le sud.

| ID | Point de l'audit | Mesure (modèle v0.4) | Verdict | Action proposée pour le corpus |
|---|---|---|---|---|
| ALN-110 | §2 : « neige permanente dès 1 000 m (versants N) » contre « Hiver Gris 800-2 400 m » | Tw à 1 000 m : +8,5 °C (22,5° N) ; manteau stable dès 2 400 m (22,5° N), 3 020 m (17° N), 3 470 m (13° N) | **fondé** ; la matrice est juste, la phrase est fausse | remplacer par « neige épisodique dès ~1 500 m sur les versants N du nord de la cordillère ; manteau stable au-dessus de 2 400 m (halekh), plus haut vers le sud » |
| ALN-111 | H1 : halekh, \|'Arin pleinement cohérent | Blanc dès 2 680 m (20° N) → 2 260 m (23,75° N) ; 18 % de la chaîne en Hiver Blanc, 18 % en Gris | **confirmé** | aucune |
| ALN-112 | H2 : lóngò, Hiver Gris dominant, Blanc réduit aux sommets | Blanc 3,5 % ; Gris 21,5 % ; hors \|'Arin 57 % ; Blanc dès 2 280 m (N) → 3 650 m (S) ; contreforts sud sans \|'Arin | **fondé** et plus marqué que prévu : le sud de lóngò n'a pas d'\|'Arin | §III : paragraphe lóngò — Gris au nord, Blanc limité aux crêtes > 2 300-2 800 m près de !Okheti, \|'Arin absent au sud de ~13° N (régime tropical) |
| ALN-113 | H3 : gradient interne de k'ara (chaîne unique) | Blanc dès 2 260 m (ouest, 23,75° N) → 3 435 m (Marra, 13,3° N) ; Gris dès 660 → 1 835 m ; prolongement SE : Blanc absent, 76 % hors \|'Arin | **fondé** | §III : formaliser un gradient continu ouest → est le long de k'ara, sans scission |
| ALN-114 | H4 : qoyra, \|'Arin secondaire, mousson dominante | Blanc 0,5 % (sommets) ; Gris 32 % ; hors \|'Arin 42 % ; T annuelle au sommet −1,1 °C : aucun glacier | **fondé** pour toute la chaîne | §V : étendre « \|'Arin secondaire » à tout qoyra ; confirmer l'absence de glacier |
| ALN-115 | (§III) « −10/−15 °C à 2 500 m » | nuits −8,5 à −12,5 °C à 22,5° N ; −2,3 °C à 13,3° N | valable au nord seulement | préciser « au nord de la cordillère (halekh, k'ara occidental) » |
| ALN-116 | (§III) « gelées fréquentes < 1 500 m » | nuits −2,5 °C à 1 500 m (22,5° N) ; +3,7 °C (13,3° N) | valable au nord seulement | idem |
| ALN-117 | (§III) « Mer Halakhel gelée en bordures » | rive à 28° N : Tw +10,8 °C ; nuits −1,2 °C | gel de la mer impossible ; gelée blanche possible sur les rives | remplacer par l'Hiver de Vapeur (brouillards) ; voir ALN-072 |
| ALN-118 | (§I) halekh « glaciers relictuels > 3 500 m » | T annuelle à 3 500 m : +1,8 °C ; glace relictuelle possible dès ~4 200 m | à corriger | « glaciers relictuels > 4 100 m (cirques sommitaux exposés N) » |
| ALN-119 | (§II) étages 800 / 2 400 / 3 600 m | exacts à 22,5° N ; relevés vers le sud, abaissés vers le nord (table « Limites par latitude », §8) | à préciser | présenter ces valeurs comme référence du nord de la cordillère, avec le gradient |
| ALN-120 | (nouveau) hiver de la façade méditerranéenne et de l'Atlas | froid et pluvieux, hors cordillère \|\|Urumati | hors matrice canonique | canoniser un faciès (ou le rattacher à l'Hiver Gris) ; carte : « hiver pluvieux tempéré » |
| ALN-121 | (nouveau) portée de l'Hiver Gris | conditions de l'Hiver Gris aussi au-delà de 100-200 km de la cordillère (plateaux du Fezzan, hauts plateaux) | à préciser | « zone d'impact » : rayon indicatif ; la physique (hiver froid et pluvieux) prime |
| ALN-122 | Carte du climat | `carte/beliet_carte_climat.png` et `.svg` ; SIG : `beliet_facies_arin.tif`, `beliet_temperature_hiver.tif`, `beliet_climat.geojson` ; carte texte §3 de `carte/beliet_carte_ascii.md` | ajout | référencer dans le Géosystème (§II-III) |

Effets sur la carte v0.4 : forêt de montagne de 840 000 à ~550 000 km² (étages relevés au sud) ; glaciers 1 516 km², sur k'ara (\|'Ara-Sukhì) et en relictuel sur halekh, aucun sur qoyra.

## 7. Historique des positions (versions caduques à ne pas reporter)

| Élément | v0.1 | v0.2 (abandonnée) | v0.3 | v0.3.1 à v0.5 (référence) |
|---|---|---|---|---|
| Halakhel | 6-28° E, 23,5-31,5° N, bras des chotts | -11,5-28° E, bande coupée en deux | -8-28,5° E, d'un seul tenant | idem v0.3 |
| Tùmázì | Sudd (26,4-32,1° E) | cuvette du Tchad | Sudd | 22,0-27,7° E |
| Mopámà | plateau de Jos | Fouta-Djalon | 4,9-7,4° E | idem |
| Ku-jálima-rir / Jálondù | baie du Bénin | Guinée-Bissau | golfe de Guinée O / côte du Ghana | idem |
| Cordillère | sur massifs réels | arc rectiligne 20-21° N | massifs réels, abaissée à l'ouest | + socles, lóngò arqué, contreforts |
| Cols | absents | absents | absents | 48 placés |
| Fleuves dessinés | tracés droits | tracés droits | tracés droits | v0.3.2 : cours calculés le long des vallées (même source, même embouchure) ; v0.5 : chenaux Abnīṣar et Tanīlḥa |
| Rivages de l'Halakhel | — | — | glacis continu | v0.5 : sept secteurs escarpés (ALN-130) |
| Delta du Mopámà | — | — | plateau de 20-40 m | v0.5 : plaine deltaïque à mangroves (ALN-131) |
| Haute Tanāḥil (vallée des villes) | — | — | piémonts N de k'ara, sans site (v0.3.2 §4) | v0.5 : gorge amont de l'Abay (caduc) ; v0.5.2 : canyon au nord du col Abnī-tɨra, 24,2-27,4° E, 15,9-17,5° N (ALN-182) |
| Qūrāš-Taniḥīl-Ramšūr ; Qūrāš-Tanīqa | — | — | — | v0.5 : 38,45° ; 10,95° et 38,35° ; 10,55° (caducs) ; v0.5.2 : tête et cours du canyon (ALN-183) |
| Lieux (LUR, ZRS) | — | — | aucune position | v0.5 : 74 lieux placés (ALN-135) |

---

## 8. Mesures et positions (section générée)

<!-- MESURES:DEBUT — section régénérée par outils/mesures_corpus.py ; ne pas éditer à la main -->

### Mesures de la carte v0.5

Toutes les valeurs sont mesurées sur la carte générée. Fichier complet : `carte/sig/beliet_mesures.json`.

#### Mer Halakhel

| Grandeur | Valeur |
|---|---|
| Superficie | 1 280 030 km² |
| Emprise | -7.99° à 28.85° E ; 23.01° à 31.17° N |
| Longueur O-E | 3640 km |
| Niveau / profondeur max | -20 m / 1439 m |
| Îles | 47 |
| Distance min. à l'Atlantique | 270 km (mer [-7.66, 28.08] → côte [-9.84, 29.55]) |
| Distance min. à la Méditerranée | 130 km (mer [26.77, 30.22] → côte [27.48, 31.21]) |
| Distance min. à la mer Rouge | 370 km |

Profil par méridien :

| Longitude | Rive nord | Rive sud | Largeur | Eau sur le méridien |
|---|---|---|---|---|
| -7.0° | 28.49° N | 27.49° N | 111 km | 70 km |
| -5.0° | 29.09° N | 27.18° N | 212 km | 189 km |
| -3.0° | 29.49° N | 26.48° N | 334 km | 319 km |
| -1.0° | 29.63° N | 26.31° N | 368 km | 352 km |
| 1.0° | 29.97° N | 25.92° N | 449 km | 289 km |
| 3.0° | 28.64° N | 25.88° N | 306 km | 226 km |
| 5.0° | 30.55° N | 27.18° N | 374 km | 76 km |
| 7.0° | 30.5° N | 26.64° N | 428 km | 431 km |
| 9.0° | 30.84° N | 27.2° N | 403 km | 398 km |
| 11.0° | 28.42° N | 26.68° N | 193 km | 173 km |
| 13.0° | 27.76° N | 24.74° N | 334 km | 207 km |
| 15.0° | 29.28° N | 25.3° N | 441 km | 422 km |
| 17.0° | 29.17° N | 27.22° N | 216 km | 212 km |
| 19.0° | 29.06° N | 25.19° N | 429 km | 404 km |
| 21.0° | 29.91° N | 23.99° N | 656 km | 617 km |
| 23.0° | 30.66° N | 23.08° N | 840 km | 713 km |
| 25.0° | 30.17° N | 24.42° N | 637 km | 622 km |
| 27.0° | 30.11° N | 25.22° N | 542 km | 546 km |

Largeur du Sumdan (rive nord → Méditerranée) :

| Longitude | Rive nord | Côte | Largeur |
|---|---|---|---|
| 0° | 29.43° N | 35.8° N | 706 km |
| 2° | 27.85° N | 36.52° N | 961 km |
| 4° | 27.94° N | 36.87° N | 990 km |
| 6° | 30.98° N | 36.81° N | 647 km |
| 8° | 30.53° N | 36.82° N | 698 km |
| 10° | 30.09° N | 37.26° N | 796 km |
| 12° | 28.51° N | 32.98° N | 495 km |
| 14° | 28.22° N | 32.72° N | 499 km |
| 16° | 29.71° N | 31.26° N | 172 km |
| 18° | 29.37° N | 30.8° N | 159 km |
| 20° | 29.23° N | 30.7° N | 164 km |
| 22° | 29.6° N | 32.87° N | 362 km |
| 24° | 29.91° N | 32.05° N | 238 km |
| 26° | 30.2° N | 31.59° N | 155 km |
| 28° | 29.24° N | 31.06° N | 202 km |

#### Lacs

| Lac | Superficie | Altitude | Prof. max | Centre | Emprise | O-E × N-S |
|---|---|---|---|---|---|---|
| Tùmázì (`GEO_LAC_TUMAZI`) | 92 194 km² | 620 m | 601 m | [24.77, 7.66] | 22.24-27.47° E, 6.51-9.1° N | 577 × 286 km |
| Akhtir (`GEO_LAC_AKHTIR`) | 44 753 km² | 1200 m | 592 m | [22.61, 21.31] | 21.2-24.17° E, 20.22-22.23° N | 308 × 222 km |
| Mopámà (`GEO_LAC_MOPAMA`) | 28 555 km² | 800 m | 255 m | [6.08, 10.1] | 4.97-7.26° E, 9.13-11.03° N | 252 × 210 km |

#### Chaînes (lignes de crête)

| Chaîne | Longueur d'axe | Point culminant | Médiane de crête | Extrémités |
|---|---|---|---|---|
| \|\|Urumati-halekh | 1797 km | 4350 m à [-6.54, 22.39] | 1940 m | [-16.3, 20.0] → [0.6, 23.75] |
| !Okheti | 190 km | 3454 m à [0.38, 23.39] | 1706 m | [0.0, 24.45] → [1.2, 23.15] |
| \|\|Urumati-k'ara | 2881 km | 5350 m à [17.81, 20.33] | 2326 m | [0.6, 23.75] → [24.4, 13.3] |
| GEO_ORO_URUMATI_KARA (segment 24.4, 13.3) | 1444 km | 3285 m à [23.34, 14.37] | 1700 m | [24.4, 13.3] → [36.6, 8.7] |
| \|\|Urumati-lóngò | 1736 km | 3454 m à [0.38, 23.39] | 1554 m | [0.9, 23.6] → [9.2, 10.2] |
| GEO_ORO_URUMATI_LONGO (segment 5.6, 16.6) | 392 km | 2056 m à [5.6, 16.59] | 1208 m | [5.6, 16.6] → [8.4, 18.9] |
| GEO_ORO_URUMATI_LONGO (segment 8.0, 12.9) | 324 km | 2228 m à [7.82, 13.19] | 1304 m | [8.0, 12.9] → [5.6, 11.2] |
| GEO_ORO_URUMATI_LONGO (segment 2.6, 20.4) | 259 km | 2689 m à [2.51, 19.55] | 1307 m | [2.6, 20.4] → [0.7, 18.9] |
| \|\|Urumati-qoyra | 2020 km | 4673 m à [38.38, 13.22] | 2181 m | [38.8, 15.4] → [48.5, 10.6] |
| GEO_ORO_COTIERE_N (segment 6.2, 36.2) | 2622 km | 1631 m à [8.33, 35.61] | 669 m | [6.2, 36.2] → [29.5, 30.6] |
| Mù-wúlè | 355 km | 1800 m à [3.79, 9.98] | 1032 m | [3.4, 11.7] → [4.2, 8.6] |
| Mù-dárhòbì | 289 km | 2100 m à [7.2, 7.71] | 1221 m | [5.5, 8.15] → [7.9, 8.2] |
| Kù-kɨ́bò | 287 km | 1400 m à [21.81, 6.62] | 1187 m | [20.5, 7.6] → [22.7, 6.25] |

#### Fleuves dessinés

| Fleuve | Longueur dessinée | Amont | Aval |
|---|---|---|---|
| Tira-ñara / Tanāḥil (`GEO_FLV_TANAHIL`) | 1755 km | [37.18, 11.04] | [32.49, 15.63] |
| Buhlela (`GEO_FLV_BUHLELA`) | 1135 km | [39.27, 11.97] | [33.98, 17.67] |
| Tira-qoyra / Abnuḥīl (`GEO_FLV_ABNUHIL`) | 2446 km | [32.49, 15.63] | [30.86, 27.6] |
| Šafāqil (`GEO_FLV_ABNUHIL_SAFAQIL`) | 768 km | [30.88, 27.63] | [30.4, 31.44] |
| Abnīqa (`GEO_FLV_ABNUHIL_ABNIQA`) | 386 km | [28.95, 27.62] | [28.52, 27.32] |
| \|Na-madikh / Madīlan (`GEO_FLV_MADIKH`) | 808 km | [5.7, 24.25] | [12.8, 24.75] |
| Imikhrel (`GEO_FLV_IMIKHREL`) | 536 km | [4.6, 24.0] | [0.49, 25.15] |
| Ehukhtal (`GEO_FLV_EHUKHTAL`) | 919 km | [-0.1, 24.5] | [-7.7, 27.22] |
| \|Na-khuwel / Ḥawqal (`GEO_FLV_HAWQAL`) | 1087 km | [19.9, 19.7] | [26.72, 25.2] |
| \|Na-khuwel-ra (`GEO_FLV_HAWQAL_RA`) | 635 km | [22.4, 17.7] | [23.3, 20.8] |
| \|Na-khuwel-ɨn (`GEO_FLV_HAWQAL_IN`) | 292 km | [27.0, 21.4] | [25.93, 23.62] |
| GEO_FLV_EMISSAIRE_MOPAMA (`GEO_FLV_EMISSAIRE_MOPAMA`) | 653 km | [5.0, 9.45] | [0.98, 5.93] |

#### Distances

| Trajet | Distance |
|---|---|
| Mopámà (centre) → delta du Mopámà | 714 km |
| Tùmázì (centre) → Mopámà (centre) | 2073 km |
| Akhtir (centre) → Ḥawqil | 623 km |
| Abnīqa → Šafāqil (embouchures) | 513 km |
| Hlom-khetal → Imekh-stom | 735 km |
| Hlom-khetal → Abnīqa (extrémités O-E) | 3467 km |
| Khreth-na-Serek → Hlom-khetal | 546 km |
| Imekh-stom → ria Tawālmaz (vol d'oiseau, RT_016) | 1357 km |
| ria Tawālmaz → Abnīqa (vol d'oiseau, RT_023) | 1513 km |
| Hlom-khetal → Ḥawqil (vol d'oiseau) | 3364 km |
| mer → Atlantique, plus court portage (RT_027) | 270 km |
| mer → Méditerranée, plus court portage (§VI.1.2) | 130 km |
| mer → mer Rouge, plus courte caravane (§VI.1.2) | 370 km |
| Khlōr-Naw → extrémité O de halekh (RT_066) | 1024 km |
| Mopámà (centre) → nœud !Okheti (longueur du versant SO de lóngò) | 1613 km |
| Tùmázì (centre) → \|'Ara-Sukhì | 1588 km |
| Tùmázì (centre) → plateaux de qoyra (38,0° E ; 9,5° N) | 1470 km |
| interfluve oriental (diffluence → côte E de la mer) | 245 km |
| Khlōr-Naw (Staur-Khlōr) → côte continentale la plus proche | 737 km |

#### Limite sud estompée

| Longitude | Opaque jusqu'à | Moitié estompée à |
|---|---|---|
| 9° E | 4.16° N | -3.49° N |
| 12° E | 4.06° N | 2.23° N |
| 15° E | 3.9° N | 2.84° N |
| 18° E | 3.97° N | 2.84° N |
| 21° E | 3.47° N | 2.6° N |
| 24° E | 4.24° N | 3.01° N |
| 27° E | 4.36° N | 3.46° N |
| 30° E | 5.08° N | 4.22° N |
| 33° E | 4.35° N | 2.97° N |
| 36° E | 2.73° N | 0.75° N |
| 39° E | 2.15° N | 0.94° N |
| 42° E | 1.45° N | 0.59° N |
| 45° E | 0.32° N | -3.49° N |

#### Précipitations aux points de calibration

| Lieu | Position | Cible | Modèle |
|---|---|---|---|
| côte atlantique SO (Ku-jálima-rir) | [1.5, 6.4] | 2200 mm | 2185 mm |
| bassin Mopámà | [6.2, 10.0] | 1900 mm | 1750 mm |
| bassin Tùmázì | [24.9, 7.6] | 1500 mm | 1078 mm |
| plateaux qoyra | [38.0, 9.5] | 1300 mm | 952 mm |
| désert du Sumdan | [11.0, 31.0] | 50 mm | 54 mm |
| façade méditerranéenne N (djebel Akhdar) | [21.8, 32.6] | 650 mm | 651 mm |
| côte atlantique NO | [-7.5, 33.5] | 450 mm | 601 mm |
| côte Mer Rouge | [37.5, 19.0] | 80 mm | 80 mm |
| Akhtir | [22.6, 21.3] | 750 mm | 506 mm |
| côte océan de l'Est | [47.0, 5.0] | 550 mm | 577 mm |
| versant sud de k'ara (humide) | [19.5, 17.6] | 1000 mm | 581 mm |
| versant sud de k'ara, Ennedi | [23.0, 14.5] | 900 mm | 900 mm |
| piémont nord de k'ara (200-600) | [11.0, 23.9] | 280 mm | 273 mm |
| rive nord de l'Halakhel (Sumdan) | [8.0, 30.3] | 90 mm | 84 mm |
| rive sud de l'Halakhel (désertique) | [20.5, 23.1] | 110 mm | 173 mm |
| versant atlantique de halekh | [-12.0, 20.6] | 750 mm | 745 mm |
| versant SO de lóngò (humide) | [2.6, 19.2] | 900 mm | 922 mm |
| versant NE de lóngò (semi-aride) | [7.4, 17.6] | 420 mm | 396 mm |
| façade méditerranéenne NE | [29.5, 30.95] | 400 mm | 401 mm |
| piémonts SE (semi-arides) | [43.5, 7.0] | 320 mm | 384 mm |
| piémonts NO (semi-aride froid) | [-6.5, 31.6] | 650 mm | 481 mm |
| déserts orientaux (NE) | [32.5, 22.5] | 30 mm | 32 mm |
| plaines du NE, aval du confluent | [29.0, 18.5] | 90 mm | 86 mm |
| sud somalien (côte océan de l'Est) | [42.5, 0.5] | 500 mm | 505 mm |
| plateau somalien (bras E-O de qoyra) | [45.0, 9.6] | 300 mm | 232 mm |
| versant humide O des plateaux SE (cols T'araq-ɨnkh, Q'usa-\|\|ema) | [35.0, 8.8] | 2200 mm | 2906 mm |
| rive S du Tùmázì (haute futaie, FOR_S) | [24.5, 6.0] | 1800 mm | 2491 mm |
| côte au sud du Mopámà (delta du Sud) | [6.3, 5.4] | 2400 mm | 2608 mm |

#### Surfaces

- Terres émergées (zone estompée pondérée) : 17 605 877 km²
- Point culminant : 5350 m

| Milieu | Surface |
|---|---|
| `steppe_piemont` | 5 913 744 km² |
| `herbage_arbore` | 3 600 095 km² |
| `foret_tropicale_humide` | 3 147 316 km² |
| `desert_pierreux` | 2 697 571 km² |
| `foret_montagne` | 534 367 km² |
| `fourre_cotier_sec` | 446 727 km² |
| `desert_sableux` | 284 190 km² |
| `prairie_altitude` | 226 138 km² |
| `depression_saline` | 199 047 km² |
| `foret_berge` | 189 740 km² |
| `eaux_lacustres` | 165 502 km² |
| `plaine_alluviale` | 164 198 km² |
| `zone_humide_lacustre` | 61 028 km² |
| `recif_corallien` | 39 332 km² |
| `foret_maree` | 38 430 km² |
| `ile_aride` | 25 241 km² |
| `cote_desertique` | 22 498 km² |
| `littoral_rocheux` | 21 035 km² |
| `zone_periglaciaire` | 20 740 km² |
| `oasis` | 6 913 km² |
| `dunes_littorales` | 5 072 km² |
| `glacier` | 1 516 km² |

#### Climat : hivers du |'Arin et étages (modèle v0.4)

Modèle :

- temperature_annuelle : T = 27,5 − 0,45 × max(|lat| − 12, 0) − 6,0 × altitude (km)
- amplitude_ete_hiver : A = 4 + 0,45 × (|lat| − 8), min. 2 °C
- temperature_hiver : Tw = T − A/2 − 3 (refroidissement |'Arin, §III cause 3)
- minimum_nocturne : Tn = Tw − 8 (humide) à − 12 (aride, < 100 mm)
- seuil_hiver_blanc_tw_c : 0.11
- seuil_hiver_gris_tw_c : 9.71
- etages : température de saison de végétation T + A/3 ; seuils calés sur 800 / 2 400 / 3 600 m à 22,5° N
- glaciers : T ≤ -5.0 °C (actifs) ; T ≤ -2.5 °C sur halekh (relictuels)

Limites par latitude (altitude du bas de chaque faciès ou étage) :

| Latitude | Hiver Gris dès | Hiver Blanc dès | Forêt de montagne dès | Prairie dès | Périglaciaire dès | Glacier actif dès | Glacier relictuel dès |
|---|---|---|---|---|---|---|---|
| 8° N | 2131 m | 3731 m | 1225 m | 2825 m | 4025 m | 5417 m | 5000 m |
| 10° N | 2056 m | 3656 m | 1275 m | 2875 m | 4075 m | 5417 m | 5000 m |
| 13° N | 1869 m | 3469 m | 1275 m | 2875 m | 4075 m | 5342 m | 4925 m |
| 15° N | 1644 m | 3244 m | 1175 m | 2775 m | 3975 m | 5192 m | 4775 m |
| 17° N | 1419 m | 3019 m | 1075 m | 2675 m | 3875 m | 5042 m | 4625 m |
| 20° N | 1081 m | 2681 m | 925 m | 2525 m | 3725 m | 4817 m | 4400 m |
| 22.5° N | 800 m | 2400 m | 800 m | 2400 m | 3600 m | 4629 m | 4212 m |
| 25° N | 519 m | 2119 m | 675 m | 2275 m | 3475 m | 4442 m | 4025 m |
| 28° N | 181 m | 1781 m | 525 m | 2125 m | 3325 m | 4217 m | 3800 m |
| 30° N | 0 m | 1556 m | 425 m | 2025 m | 3225 m | 4067 m | 3650 m |
| 33° N | 0 m | 1219 m | 275 m | 1875 m | 3075 m | 3842 m | 3425 m |

Affirmations du Géosystème confrontées au modèle :

| Affirmation | Modèle | Verdict |
|---|---|---|
| §III \|'Arin-sukhì : « −10/−15 °C (2 500 m) » | halekh (22,5° N) : Tw -0.5 °C, nuits -8.5 à -12.5 °C ; k'ara orientale (13,3° N) : Tw 5.7 °C, nuits -2.3 °C | cohérent au nord (avec inversions) ; trop froid au sud |
| §III \|'Arin-sukhì : « gelées fréquentes < 1 500 m » | nuits à 1 500 m : -2.5 °C (22,5° N) ; 3.7 °C (13,3° N) | cohérent au nord ; faux au sud de ~17° N |
| §III \|'Arin-sukhì : « neige permanente dès 1 000 m (versants exposés N) » | Tw à 1 000 m : 8.5 °C (22,5° N), 6.8 °C (25° N) ; manteau stable dès 2400 m (22,5° N), 3019 m (17° N), 3469 m (13° N) | contradictoire avec la matrice (Gris 800-2 400 m) et physiquement faux : neige épisodique dès ~1 500 m (versants N du nord), manteau stable dès 2 400 m (22,5° N) |
| §III matrice : « Hiver Gris 800-2 400 m », « Hiver Blanc > 2 400 m » | exact à 22,5° N ; Blanc dès 3469 m (13° N), 3019 m (17° N), 2119 m (25° N), 1556 m (30° N) | cohérent comme valeur de référence ; à préciser : gradient avec la latitude |
| §III économie : « Mer Halakhel gelée en bordures » | rive à 28° N : Tw 10.8 °C, nuits -1.2 °C | gel de la mer impossible (eau salée, Tw > 10 °C) ; seules des gelées nocturnes givrent les rives : remplacer par brouillards d'advection (Hiver de Vapeur, déjà au §III) |
| §I halekh : « glaciers relictuels > 3 500 m » | T annuelle à 3 500 m (22,4° N) : 1.8 °C ; glace relictuelle possible dès 4220 m | relever à > 4 100 m (cirques sommitaux exposés N) |
| §I k'ara : « dernier glacier équatorial (> 4 800 m) » | glacier actif dès 4794 m à 20,3° N (\|'Ara-Sukhì, 5 350 m) | cohérent |
| §I qoyra : sommets > 4 600 m, aucun glacier mentionné | T annuelle au sommet (4 673 m, 13,2° N) : -1.1 °C ; Hiver Blanc dès 3446 m | cohérent : neige d'hiver sur les sommets, pas de glacier ; k'ara porte bien le « dernier glacier » |
| §II Zone II : étages 800 / 2 400 / 3 600 m | à 22,5° N : exact ; à 13° N : forêt dès 1275 m, prairie dès 2875 m | à préciser : étages de référence (nord de la cordillère), relevés vers le sud |

Faciès |'Arin par chaîne (part de la surface de la chaîne) :

| Chaîne | Latitudes (extrémités) | Blanc dès | Gris dès | Blanc | Gris | Jaune | Hors \|'Arin |
|---|---|---|---|---|---|---|---|---|
| \|\|Urumati-halekh | 20.0° → 23.75° N | 2681 → 2259 m | 1081 → 659 m | 17.7 % | 18.4 % | 55.2 % | 8.7 % |
| !Okheti | 24.45° → 23.15° N | 2181 → 2327 m | 581 → 727 m | 24.4 % | 0 % | 60.7 % | 14.9 % |
| \|\|Urumati-k'ara | 23.75° → 13.3° N | 2259 → 3435 m | 659 → 1835 m | 24.2 % | 23.5 % | 46.2 % | 6.1 % |
| GEO_ORO_URUMATI_KARA (segment 24.4, 13.3) | 13.3° → 8.7° N | 3435 → 3705 m | 1835 → 2105 m | 0 % | 22.2 % | 1.9 % | 75.9 % |
| \|\|Urumati-lóngò | 23.6° → 10.2° N | 2276 → 3649 m | 676 → 2049 m | 3.5 % | 21.6 % | 17.4 % | 57.5 % |
| GEO_ORO_URUMATI_LONGO (segment 5.6, 16.6) | 16.6° → 18.9° N | 3064 → 2805 m | 1464 → 1205 m | 0 % | 19.3 % | 0 % | 80.7 % |
| GEO_ORO_URUMATI_LONGO (segment 8.0, 12.9) | 12.9° → 11.2° N | 3480 → 3611 m | 1880 → 2011 m | 0 % | 2.6 % | 0 % | 97.4 % |
| GEO_ORO_URUMATI_LONGO (segment 2.6, 20.4) | 20.4° → 18.9° N | 2636 → 2805 m | 1036 → 1205 m | 0 % | 63.1 % | 2.1 % | 34.8 % |
| \|\|Urumati-qoyra | 15.4° → 10.6° N | 3199 → 3634 m | 1599 → 2034 m | 0.5 % | 31.9 % | 26.1 % | 41.5 % |

#### Les 48 cols

Altitude canonique imposée au relief ; « crête d'origine » = altitude de la ligne de crête avant entaille ou selle.

| geo_id | Nom | Groupe (interface) | Chaîne | Position [lon, lat] | Altitude | Crête d'origine | Statut | Routes |
|---|---|---|---|---|---|---|---|---|
| `GEO_COL_001` | Abnī-tɨra | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | [23.96, 15.332] | 2800 m (carte 2800 m) | 2804 m | haute_route | RT_006, RT_064 |
| `GEO_COL_002` | Ṭanīkhūr | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | [21.319, 17.798] | 3200 m (carte 3200 m) | 3442 m | haute_route_extreme | — |
| `GEO_COL_003` | Ṣabūl-tɨkh | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | [15.678, 20.524] | 2900 m (carte 2900 m) | 3139 m | haute_route | — |
| `GEO_COL_004` | Ḥamīr-ɨlkh | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | [23.01, 15.768] | 3000 m (carte 3000 m) | 3164 m | haute_route | — |
| `GEO_COL_005` | Qaṣūl-tɨra | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | [20.26, 18.55] | 2700 m (carte 2700 m) | 2868 m | secondaire | — |
| `GEO_COL_006` | Maḥēl-!ara | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | [21.777, 16.057] | 2950 m (carte 2950 m) | 3161 m | haute_route | — |
| `GEO_COL_007` | Ṭubayl | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | [24.178, 13.441] | 2850 m (carte 2850 m) | 2851 m | haute_route | — |
| `GEO_COL_008` | Šaqra-t'em | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | [24.503, 12.481] | 2400 m (carte 2400 m) | 2649 m | haute_route | — |
| `GEO_COL_009` | Kurel-ahek | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | [25.553, 12.554] | 2150 m (carte 2150 m) | 2155 m | principal | — |
| `GEO_COL_010` | T'araq-ɨnkh | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | [34.758, 8.873] | 2400 m (carte 2400 m) | 2525 m | secondaire | RT_009, RT_053, RT_062 |
| `GEO_COL_011` | K'elis-‖ara | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | [32.099, 9.98] | 2500 m (carte 2500 m) | 2060 m | secondaire | RT_061 |
| `GEO_COL_012` | Q'ami-tɨra | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | [35.03, 7.796] | 2300 m (carte 2300 m) | 2314 m | secondaire | — |
| `GEO_COL_013` | P'etsul-!ama | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | [30.075, 10.977] | 2600 m (carte 2600 m) | 2197 m | haute_route | RT_065 |
| `GEO_COL_014` | T'iqur-ɨlkh | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | [36.183, 8.701] | 2700 m (carte 2700 m) | 2596 m | haute_route | — |
| `GEO_COL_015` | S'akum-\|ena | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | [35.665, 7.59] | 2200 m (carte 2200 m) | 2295 m | secondaire | RT_038 |
| `GEO_COL_016` | Q'usa-\|\|ema | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | [35.432, 8.586] | 2100 m (carte 2100 m) | 2170 m | principal | RT_019 |
| `GEO_COL_017` | T'amr-khɨna | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | [33.608, 9.527] | 2450 m (carte 2450 m) | 2131 m | secondaire | — |
| `GEO_COL_018` | Ku-Pámà-Rikh-te | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | [-12.952, 20.913] | 1600 m (carte 1600 m) | 1642 m | bas_col | — |
| `GEO_COL_019` | Ku-Mázì-Klek-te | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | [-14.336, 20.402] | 1900 m (carte 1900 m) | 1698 m | principal | — |
| `GEO_COL_020` | Kù-Lábà | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | [-12.405, 20.938] | 1700 m (carte 1700 m) | 2061 m | bas_col | — |
| `GEO_COL_021` | Ku-Sikal-Ktet-te | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | [-10.915, 21.194] | 1800 m (carte 1800 m) | 2628 m | bas_col | — |
| `GEO_COL_022` | Ku-Dúma-te | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | [-13.729, 20.559] | 1650 m (carte 1650 m) | 1690 m | bas_col | — |
| `GEO_COL_023` | Kù-Sepá | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | [-11.623, 21.139] | 1750 m (carte 1750 m) | 2548 m | bas_col | — |
| `GEO_COL_024` | Ku-Pámà-Tɨra-te | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | [7.88, 13.059] | 2000 m (carte 2000 m) | 1919 m | principal | — |
| `GEO_COL_025` | Lémakhɨ | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | [6.604, 14.407] | 2200 m (carte 2200 m) | 2022 m | secondaire | — |
| `GEO_COL_026` | Ku-Sogo-!Ara-te | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | [6.311, 15.863] | 2100 m (carte 2100 m) | 2112 m | secondaire | — |
| `GEO_COL_027` | Kù-Pété-‖Eni | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | [3.581, 19.229] | 1900 m (carte 1900 m) | 2060 m | bas_col | — |
| `GEO_COL_028` | Ku-Ténɨlkh-te | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | [4.886, 17.745] | 2300 m (carte 2300 m) | 2114 m | secondaire | — |
| `GEO_COL_029` | Ku-Darikámba-!Ari-te | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | [2.313, 19.76] | 2400 m (carte 2400 m) | 2280 m | secondaire | — |
| `GEO_COL_030` | Ktalep-tɨra | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | [1.194, 23.154] | 2600 m (carte 2600 m) | 2715 m | haute_route | — |
| `GEO_COL_031` | Tkrilan-ɨkh | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | [-5.028, 22.903] | 2800 m (carte 2800 m) | 2890 m | haute_route | — |
| `GEO_COL_032` | Hlelak-!uri | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | [-2.117, 22.914] | 2900 m (carte 2900 m) | 2941 m | haute_route | — |
| `GEO_COL_033` | Rekal-‖ene | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | [-3.648, 23.157] | 2500 m (carte 2500 m) | 2571 m | secondaire | — |
| `GEO_COL_034` | Ktamar-khɨ | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | [4.313, 23.601] | 3000 m (carte 3000 m) | 3009 m | haute_route | — |
| `GEO_COL_035` | Kraloth-!enu | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | [-1.477, 23.34] | 2700 m (carte 2700 m) | 2821 m | haute_route | — |
| `GEO_COL_036` | Narkh-ɨlkh | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | [7.442, 23.081] | 2550 m (carte 2550 m) | 2669 m | secondaire | — |
| `GEO_COL_037` | Kurahek | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | [-9.494, 21.843] | 2100 m (carte 2100 m) | 2209 m | principal | — |
| `GEO_COL_038` | Hlenik-k'eso | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | [-8.698, 22.642] | 2000 m (carte 2000 m) | 2437 m | principal | — |
| `GEO_COL_039` | Pēlakh-t'sira | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | [-9.927, 21.123] | 1750 m (carte 1750 m) | 1879 m | bas_col | — |
| `GEO_COL_040` | Namkural | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | [2.838, 23.089] | 1800 m (carte 1800 m) | 2041 m | bas_col | — |
| `GEO_COL_041` | Krathal-t'iq | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | [2.366, 21.929] | 2300 m (carte 2300 m) | 2372 m | secondaire | — |
| `GEO_COL_042` | Ktalor-p'es | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | [8.376, 22.98] | 2600 m (carte 2600 m) | 2799 m | haute_route | — |
| `GEO_COL_043` | Halek-t'ama | Halaktim ↔ Tɨrakh | !Okheti | [-0.344, 23.746] | 1900 m (carte 1900 m) | 2015 m | bas_col | — |
| `GEO_COL_044` | ʿUbayl-t'iq | Šamqiriyyūn ↔ Qoyra-ña-ra | \|\|Urumati-qoyra (escarpement) | [39.339, 14.45] | 2000 m (carte 2128 m) | 2128 m | secondaire | — |
| `GEO_COL_045` | Ḥazīr-k'ama | Šamqiriyyūn ↔ Qoyra-ña-ra | \|\|Urumati-qoyra (escarpement) | [38.749, 15.3] | 2100 m (carte 2195 m) | 2195 m | secondaire | — |
| `GEO_COL_046` | Ṣamar-q'ut | Šamqiriyyūn ↔ Qoyra-ña-ra | \|\|Urumati-qoyra (escarpement) | [38.462, 14.05] | 2200 m (carte 2268 m) | 2268 m | secondaire | — |
| `GEO_COL_047` | Rafīq-t'sal | Šamqiriyyūn ↔ Qoyra-ña-ra | \|\|Urumati-qoyra (escarpement) | [37.729, 13.0] | 2300 m (carte 2403 m) | 2403 m | secondaire | — |
| `GEO_COL_048` | Nrelat-q'urm | Šamqiriyyūn ↔ Qoyra-ña-ra | \|\|Urumati-qoyra (escarpement) | [37.777, 11.85] | 2200 m (carte 2225 m) | 2225 m | secondaire | — |

#### Positions paramétrées (toutes [PROPOSITION])

Coordonnées [longitude, latitude] en degrés décimaux WGS84. Liste complète et lisible par machine : clé `positions` du JSON.

| geo_id | Nom | Nature | Coordonnées | Note |
|---|---|---|---|---|
| `GEO_DET_KHRETHNASEREK` | Khreth-na-Serek | point (détroit / débouché) | [-1.85, 29.75] |  |
| `GEO_DET_HLOMKHETAL` | Hlom-khetal | point (détroit / débouché) | [-6.9, 27.65] |  |
| `GEO_DET_IMEKHSTOM` | Imekh-stom | point (détroit / débouché) | [0.2, 25.8] |  |
| `GEO_DET_ABNIQA` | Abnīqa | point (détroit / débouché) | [28.35, 27.6] |  |
| `GEO_DET_HAWQIL` | Ḥawqil | point (détroit / débouché) | [26.85, 25.35] |  |
| `GEO_DET_SAFAQIL_PASSE` | Šafāqil | point (détroit / débouché) | [31.2, 31.5] |  |
| `GEO_DLT_SAFAQIL` | Šafāqil | point (delta / estuaire) | [31.0, 30.9] |  |
| `GEO_EST_AKHIDALET` | Akhidalet | point (delta / estuaire) | [-8.2, 27.0] |  |
| `GEO_EST_TAWALMAZ` | Tawālmaz | point (delta / estuaire) | [13.6, 24.55] |  |
| `GEO_DLT_MOPAMA` | delta du Mopámà | point (delta / estuaire) | [1.3, 5.75] |  |
| `GEO_EXT_MEDITERRANEE` | Méditerranée | point d'étiquette (mer, golfe) | [18.0, 34.3] |  |
| `GEO_EXT_ATLANTIQUE` | Océan Atlantique | point d'étiquette (mer, golfe) | [-22.0, 25.0] |  |
| `GEO_EXT_MERROUGE` | Mer Rouge | point d'étiquette (mer, golfe) | [38.4, 19.2] |  |
| `GEO_EXT_OCEAN_EST` | Océan de l'Est | point d'étiquette (mer, golfe) | [50.0, 4.0] |  |
| `GEO_GLF_KUJALIMARIR` | Ku-jálima-rir | point d'étiquette (mer, golfe) | [-5.0, 3.3] |  |
| `GEO_GLF_JALONDU` | Golfe Jálondù | point d'étiquette (mer, golfe) | [-0.4, 4.6] |  |
| `GEO_ORO_ARASUKHI` | \|'Ara-Sukhì | point (massif, site) | [17.8, 20.3] |  |
| `GEO_SIT_AYKMAIXA` | !Ayk-ma-‖Ixa | point (massif, site) | [36.9, 9.1] |  |
| `GEO_DES_SUMDAN` | Désert du Sumdan | point d'étiquette (région) | [9.5, 31.4] |  |
| `GEO_ZON_INTERFLUVE_E` | Interfluve oriental | point d'étiquette (région) | [29.7, 25.6] |  |
| `GEO_ARC_STAURKHLOR` | Staur-Khlōr | zone (archipel) | [[-25.6, 14.6], [-22.4, 14.6], [-22.4, 17.4], [-25.6, 17.4]] | étiquette [-24.0, 18.0] |
| `GEO_ILE_KHLORNAW` | Khlōr-Naw | point (île principale) | [-24.38, 14.95] |  |
| `GEO_ARC_LISEKDI` | Li-sèk-dì | îlots (archipel) | [[-2.05, 4.55], [-1.65, 4.62], [-1.25, 4.72], [-0.85, 4.82], [-0.45, 4.95], [-2.4, 4.5]] | étiquette [-1.7, 4.1] |
| `GEO_MER_HALAKHEL` | Mer Halakhel | contour-enveloppe (le rivage réel est découpé par le relief) | [[-7.0, 27.75], [-6.5, 28.35], [-5.6, 28.85], [-4.6, 29.25], [-3.6, 29.5], [-2.7, 29.65], [-2.1, 29.7], [-1.55, 29.55], [-0.9, 29.35], [-0.2, 29.15], [0.6, 28.95], [1.4, 28.6], [2.2, 28.2], [3.0, 27.95], [3.8, 28.0], [4.5, 28.3], [5.1, 28.85], [5.6, 29.5], … |  |
| `GEO_MER_HALAKHEL` | golfe de Serek | contour-enveloppe (le rivage réel est découpé par le relief) | [[-1.8, 29.95], [-2.35, 30.15], [-2.6, 30.55], [-2.4, 31.0], [-1.9, 31.2], [-1.35, 31.15], [-0.95, 30.8], [-0.95, 30.35], [-1.25, 30.05]] |  |
| `—` | Khreth-na-Serek | chenal 12→12 km | [[-2.0, 29.3], [-1.95, 29.6], [-1.8, 29.85], [-1.7, 30.15]] |  |
| `—` | Hlom-khetal | chenal 35→18 km | [[-6.5, 27.7], [-7.0, 27.6], [-7.5, 27.45], [-7.9, 27.25]] |  |
| `—` | Imekh-stom | chenal 28→12 km | [[0.0, 26.5], [0.1, 26.0], [0.3, 25.6], [0.55, 25.35]] |  |
| `—` | Tawālmaz | chenal 24→8 km | [[14.6, 25.4], [14.0, 25.05], [13.4, 24.85], [12.8, 24.75]] |  |
| `GEO_MER_HALAKHEL` | îles volcaniques et îles de passe | points [lon, lat(, haut., rayon)] | [[17.3, 27.6], [17.9, 27.45], [18.5, 27.8], [16.8, 27.4], [18.9, 27.3], [19.8, 26.4], [21.6, 27.1], [24.0, 27.4], [22.7, 25.2], [13.0, 27.2], [9.3, 27.9], [7.3, 28.4], [1.2, 27.6], [-2.4, 28.0], [-4.9, 28.1], [-1.62, 29.72, 260, 6]] |  |
| `—` | falaises calcaires de la passe Khreth-na-Serek | rivage escarpé (v0.5) : centre, rayon 60 km, dénivelé 170 m | [-1.85, 29.8] |  |
| `—` | rives du goulet Hlom-khetal (calcaire blanc) | rivage escarpé (v0.5) : centre, rayon 75 km, dénivelé 110 m | [-7.2, 27.7] |  |
| `—` | goulet estuarien d'Imekh-stom | rivage escarpé (v0.5) : centre, rayon 55 km, dénivelé 120 m | [0.25, 25.9] |  |
| `—` | rias basaltiques de Cherbekh-khem | rivage escarpé (v0.5) : centre, rayon 70 km, dénivelé 150 m | [2.7, 25.95] |  |
| `—` | versants de la ria Tawālmaz (pierre claire) | rivage escarpé (v0.5) : centre, rayon 110 km, dénivelé 130 m | [13.8, 25.05] |  |
| `—` | cap de Qabḍ-ār-Ǧanūb (golfe de Koufra) | rivage escarpé (v0.5) : centre, rayon 50 km, dénivelé 110 m | [22.6, 23.75] |  |
| `—` | cap de Ḥamaḍ-Rās | rivage escarpé (v0.5) : centre, rayon 45 km, dénivelé 100 m | [28.15, 29.35] |  |
| `—` | delta du Mopámà | plaine deltaïque basse (v0.5) : contour | [[0.3, 5.68], [0.45, 6.1], [0.85, 6.5], [1.35, 6.75], [1.9, 6.62], [2.2, 6.38], [2.1, 6.15], [1.2, 5.9], [0.6, 5.6]] |  |
| `—` | delta du Sud Mopámà | plaine deltaïque basse (v0.5) : contour | [[4.95, 5.95], [5.7, 6.05], [6.55, 5.85], [7.1, 5.3], [7.7, 4.8], [7.8, 4.3], [6.5, 3.9], [5.4, 4.0], [4.8, 4.9]] |  |
| `GEO_LAC_TUMAZI` | Tùmázì | contour dessiné (ajusté à la superficie canonique) | [[22.0, 7.9], [22.8, 8.55], [24.0, 8.85], [25.2, 8.9], [26.4, 8.7], [27.4, 8.2], [27.7, 7.4], [27.1, 6.8], [25.9, 6.5], [24.6, 6.6], [23.4, 6.8], [22.4, 7.2]] | centre mesuré [24.77, 7.66] |
| `GEO_LAC_AKHTIR` | Akhtir | contour dessiné (ajusté à la superficie canonique) | [[21.2, 21.0], [21.7, 21.85], [22.6, 22.3], [23.6, 22.15], [24.0, 21.5], [23.6, 20.75], [22.6, 20.4], [21.7, 20.45]] | centre mesuré [22.61, 21.31] |
| `GEO_LAC_MOPAMA` | Mopámà | contour dessiné (ajusté à la superficie canonique) | [[4.9, 9.55], [5.4, 10.25], [6.3, 10.75], [7.2, 10.85], [7.4, 10.35], [6.8, 9.75], [5.9, 9.3], [5.2, 9.2]] | centre mesuré [6.08, 10.1] |
| `GEO_ORO_URUMATI_HALEKH` | \|\|Urumati-halekh | ligne de crête [lon, lat, crête m, demi-largeur km] | [[-16.3, 20.0, 550, 50], [-15.1, 20.2, 1200, 70], [-13.6, 20.55, 2100, 95], [-11.3, 21.35, 3000, 130], [-8.8, 22.05, 3700, 160], [-6.3, 22.6, 4350, 170], [-3.8, 23.05, 3900, 160], [-1.5, 23.4, 3300, 150], [0.6, 23.75, 3100, 140]] | socle 450 m / 230 km |
| `GEO_ORO_OKHETI` | !Okheti | ligne de crête [lon, lat, crête m, demi-largeur km] | [[0.0, 24.45, 2700, 80], [0.75, 23.75, 2900, 95], [1.2, 23.15, 2850, 100]] | socle 450 m / 200 km |
| `GEO_ORO_URUMATI_KARA` | \|\|Urumati-k'ara | ligne de crête [lon, lat, crête m, demi-largeur km] | [[0.6, 23.75, 3100, 140], [3.0, 23.55, 3300, 150], [5.5, 23.3, 3600, 175], [8.0, 23.0, 3450, 170], [10.4, 22.45, 3300, 160], [12.8, 21.8, 3500, 160], [15.2, 21.05, 3900, 175], [17.8, 20.3, 5350, 215], [20.0, 18.9, 4300, 190], [22.0, 16.9, 3700, 170], [23.5,… | socle 250 m / 260 km |
| `GEO_ORO_URUMATI_KARA` | segment / contrefort sans nom | ligne de crête [lon, lat, crête m, demi-largeur km] | [[24.4, 13.3, 3050, 140], [26.5, 12.0, 2400, 120], [28.5, 11.25, 2100, 115], [30.5, 10.8, 2300, 115], [32.5, 10.15, 2100, 110], [34.3, 9.2, 2300, 110], [35.6, 8.75, 2600, 110], [36.6, 8.7, 2800, 100]] |  |
| `GEO_ORO_URUMATI_LONGO` | \|\|Urumati-lóngò | ligne de crête [lon, lat, crête m, demi-largeur km] | [[0.9, 23.6, 2900, 110], [1.6, 22.4, 3200, 125], [2.2, 21.1, 3350, 135], [3.0, 19.7, 2900, 140], [4.1, 18.3, 2600, 140], [5.3, 16.9, 2400, 135], [6.5, 15.5, 2250, 130], [7.4, 14.0, 2100, 125], [8.1, 12.6, 2000, 120], [8.7, 11.3, 1900, 110], [9.2, 10.2, 1750… | socle 550 m / 270 km |
| `GEO_ORO_URUMATI_LONGO` | segment / contrefort sans nom | ligne de crête [lon, lat, crête m, demi-largeur km] | [[5.6, 16.6, 1900, 70], [6.6, 17.3, 1700, 65], [7.6, 18.1, 1600, 60], [8.4, 18.9, 1500, 55]] |  |
| `GEO_ORO_URUMATI_LONGO` | segment / contrefort sans nom | ligne de crête [lon, lat, crête m, demi-largeur km] | [[8.0, 12.9, 1800, 65], [7.2, 12.2, 1600, 60], [6.4, 11.6, 1450, 55], [5.6, 11.2, 1250, 50]] |  |
| `GEO_ORO_URUMATI_LONGO` | segment / contrefort sans nom | ligne de crête [lon, lat, crête m, demi-largeur km] | [[2.6, 20.4, 2300, 70], [1.6, 19.6, 1700, 60], [0.7, 18.9, 1300, 50]] |  |
| `GEO_ORO_URUMATI_QOYRA` | \|\|Urumati-qoyra | ligne de crête [lon, lat, crête m, demi-largeur km] | [[38.8, 15.4, 2300, 90], [38.3, 13.2, 2900, 120], [38.2, 11.0, 2900, 130], [38.6, 9.0, 2800, 140], [39.3, 7.3, 2700, 130], [40.5, 8.0, 2400, 110], [42.0, 9.0, 2100, 100], [44.0, 9.7, 1800, 90], [46.5, 10.2, 1700, 70], [48.5, 10.6, 1500, 50]] |  |
| `GEO_ORO_COTIERE_N` | segment / contrefort sans nom | ligne de crête [lon, lat, crête m, demi-largeur km] | [[6.2, 36.2, 1400, 45], [8.4, 35.7, 1600, 60], [9.7, 34.75, 1250, 45], [10.6, 33.3, 900, 35], [11.6, 32.15, 1050, 45], [13.0, 31.95, 1000, 45], [14.6, 31.55, 900, 40], [16.0, 30.75, 800, 35], [17.5, 30.25, 750, 30], [19.0, 30.0, 800, 30], [20.2, 31.2, 1000,… |  |
| `GEO_ORO_MUWULE` | Mù-wúlè | ligne de crête [lon, lat, crête m, demi-largeur km] | [[3.4, 11.7, 1400, 60], [3.7, 10.5, 1800, 75], [3.9, 9.4, 1700, 70], [4.2, 8.6, 1300, 55]] |  |
| `GEO_ORO_MUDARHOBI` | Mù-dárhòbì | ligne de crête [lon, lat, crête m, demi-largeur km] | [[5.5, 8.15, 1600, 55], [6.3, 7.75, 2100, 70], [7.2, 7.8, 1800, 60], [7.9, 8.2, 1400, 50]] |  |
| `GEO_ORO_KUKIBO` | Kù-kɨ́bò | ligne de crête [lon, lat, crête m, demi-largeur km] | [[20.5, 7.6, 1150, 60], [21.5, 6.85, 1400, 70], [22.7, 6.25, 1250, 60]] |  |
| `GEO_FLV_TANAHIL` | Tira-ñara / Tanāḥil | tracé réel Natural Earth | ["Abay", "El Bahr el Azraq"] |  |
| `GEO_FLV_BUHLELA` | Buhlela | tracé réel Natural Earth | ["Tekeze", "Setit", "Atbara"] |  |
| `GEO_FLV_ABNUHIL` | Tira-qoyra / Abnuḥīl | tracé réel Natural Earth | ["Nile"] |  |
| `GEO_FLV_ABNUHIL_SAFAQIL` | Šafāqil | tracé réel Natural Earth | ["Nile", "Rosetta Branch", "Damietta Branch"] |  |
| `GEO_FLV_ABNUHIL_ABNIQA` | Abnīqa | tracé amont → aval | [[30.78, 27.6], [30.2, 27.66], [29.6, 27.64], [29.0, 27.6], [28.55, 27.6], [28.3, 27.6]] |  |
| `GEO_FLV_ABNUHIL_ABNIQA` | Abnīqa — bras 1 | bras ou chenal, amont → aval | [[28.95, 27.62], [28.8, 27.74], [28.65, 27.88], [28.5, 28.0]] |  |
| `GEO_FLV_ABNUHIL_ABNIQA` | Abnīqa — bras 2 | bras ou chenal, amont → aval | [[28.95, 27.6], [28.8, 27.48], [28.65, 27.38], [28.52, 27.32]] |  |
| `GEO_FLV_MADIKH` | \|Na-madikh / Madīlan | tracé indicatif (couloir) ; cours dessiné : clé fleuves.trace_dessine du JSON | [[5.7, 24.25], [6.6, 24.55], [7.6, 24.6], [8.6, 24.5], [9.6, 24.35], [10.6, 24.3], [11.6, 24.45], [12.3, 24.65], [12.8, 24.75]] |  |
| `GEO_FLV_IMIKHREL` | Imikhrel | tracé indicatif (couloir) ; cours dessiné : clé fleuves.trace_dessine du JSON | [[4.6, 24.0], [3.9, 24.25], [3.1, 24.5], [2.3, 24.7], [1.6, 24.85], [0.9, 25.0], [0.4, 25.15]] |  |
| `GEO_FLV_EHUKHTAL` | Ehukhtal | tracé indicatif (couloir) ; cours dessiné : clé fleuves.trace_dessine du JSON | [[-0.1, 24.5], [-1.0, 24.7], [-2.1, 24.9], [-3.3, 25.15], [-4.5, 25.45], [-5.7, 25.8], [-6.8, 26.25], [-7.6, 26.75], [-8.0, 27.2], [-7.8, 27.3]] |  |
| `GEO_FLV_HAWQAL` | \|Na-khuwel / Ḥawqal | tracé indicatif (couloir) ; cours dessiné : clé fleuves.trace_dessine du JSON | [[19.9, 19.7], [20.6, 20.2], [21.3, 20.75], [23.6, 22.15], [24.5, 22.6], [25.3, 23.25], [25.9, 24.0], [26.4, 24.75], [26.8, 25.3]] |  |
| `GEO_FLV_HAWQAL_RA` | \|Na-khuwel-ra | tracé indicatif (couloir) ; cours dessiné : clé fleuves.trace_dessine du JSON | [[22.4, 17.7], [22.6, 18.7], [22.7, 19.6], [22.75, 20.45]] |  |
| `GEO_FLV_HAWQAL_RA` | \|Na-khuwel-ra — bras 1 | bras ou chenal, amont → aval | [[22.6, 18.7], [23.2, 19.4], [23.4, 20.2], [23.3, 20.8]] |  |
| `GEO_FLV_HAWQAL_IN` | \|Na-khuwel-ɨn | tracé indicatif (couloir) ; cours dessiné : clé fleuves.trace_dessine du JSON | [[27.0, 21.4], [26.7, 22.2], [26.2, 23.0], [25.8, 23.7]] |  |
| `GEO_FLV_EMISSAIRE_MOPAMA` | sans nom | tracé indicatif (couloir) ; cours dessiné : clé fleuves.trace_dessine du JSON | [[5.0, 9.45], [4.4, 9.0], [3.8, 8.4], [3.0, 7.8], [2.3, 7.25], [1.7, 6.7], [1.25, 6.2], [0.95, 5.85]] |  |
| `—` | Atlas (relief réel non documenté au corpus) | écrêtement (seuil 1200 m, facteur 0.35) | [[-10.5, 29.0], [10.0, 29.0], [10.0, 37.5], [-10.5, 37.5]] |  |
| `—` | Ligne du Cameroun (relief réel non documenté au corpus) | écrêtement (seuil 1500 m, facteur 0.22) | [[8.5, 3.6], [15.0, 3.6], [15.0, 8.2], [8.5, 8.2]] |  |
| `—` | erg n° 1 | zone de désert de sable | [[-1.5, 30.2], [1.8, 30.2], [2.2, 31.4], [-1.0, 31.5]] |  |
| `—` | erg n° 2 | zone de désert de sable | [[6.6, 31.1], [9.6, 30.8], [9.8, 32.2], [7.0, 32.3]] |  |
| `—` | erg n° 3 | zone de désert de sable | [[20.5, 29.6], [24.5, 29.7], [24.5, 30.6], [21.0, 30.5]] |  |
| `—` | erg n° 4 | zone de désert de sable | [[-6.5, 23.6], [-2.5, 24.0], [-2.0, 24.6], [-6.0, 24.6]] |  |
| `—` | erg n° 5 | zone de désert de sable | [[9.6, 17.6], [12.4, 17.9], [13.2, 20.0], [10.6, 20.4]] |  |
| `—` | erg n° 6 | zone de désert de sable | [[-16.2, 21.5], [-13.8, 21.2], [-11.8, 23.4], [-12.5, 25.0], [-15.0, 24.0]] |  |
| `—` | erg n° 7 | zone de désert de sable | [[27.0, 20.0], [31.0, 20.0], [31.5, 23.0], [28.5, 24.0], [27.0, 22.5]] |  |
| `—` | erg n° 8 | zone de désert de sable | [[33.0, 16.5], [35.0, 17.5], [34.5, 19.0], [32.5, 18.5]] |  |

<!-- MESURES:FIN -->

---

## 9. Lieux et routes (v0.5)

Passe de cohérence des lieux (LIEUX_URBAINS v2) et des routes (RESEAU_ROUTES v3) avec la géographie. Le détail est dans `LIEUX_ET_ROUTES.md` : méthode, constats LR-xx (lieux) et LT-xx (routes), tables A à F. Les données lisibles par machine sont dans `carte/sig/beliet_lieux_routes.json` (clés `lieux` et `routes`). La carte est `carte/beliet_carte_lieux.png` (ou `.svg` à calques).

### 9.1 Géographie modifiée (contenu ajouté, physiquement fondé)

| ID | Type | Objet | Décision | Action pour le corpus |
|---|---|---|---|---|
| ALN-130 | AJOUT | Rivages escarpés de l'Halakhel | 7 secteurs de falaises, caps et rias (100-170 m) : passe Khreth-na-Serek, goulets Hlom-khetal et Imekh-stom, rias de Cherbekh-khem et de Tawālmaz, caps de Qabḍ-ār-Ǧanūb et de Ḥamaḍ-Rās ; glacis ailleurs. Positions : §8, « Positions paramétrées » | §VI.1 et index des façades : « rivage de glacis, coupé de falaises aux passes, goulets, rias et caps » ; forger des noms pour les caps |
| ALN-131 | AJOUT | Plaine deltaïque du Mopámà | plaine basse à mangroves (~180 km de côte, 0,3-2,2° E) | §V.4 : le « delta de Jáli-Fè » est cette plaine ; Kù-Bèláà et Mázì-Dúm y sont |
| ALN-132 | AJOUT | Chenaux Abnīṣar (NE) et Tanīlḥa (SE) | tracés depuis l'apex (28,95° ; 27,6°) jusqu'à la mer | §VI.1.3 : ajouter les positions des deux chenaux |
| ALN-133 | PRÉCISION | Classement du littoral rocheux | hauteur mesurée au-dessus de l'eau voisine (mer Halakhel à −20 m) | aucune (méthode) |
| ALN-134 | CORRECTION | Pluies maximales du modèle | deux points de calage : versant O des plateaux SE 2 200 mm, rive S du Tùmázì 1 800 mm (modèle : 2 880 et 2 460 mm au lieu de 9 500 et 3 800) | aucune ; les valeurs restent dans les plages du §V |

### 9.2 Positions

| ID | Type | Objet | Décision | Action pour le corpus |
|---|---|---|---|---|
| ALN-135 | AJOUT | Positions des 74 lieux et de 21 extrémités de routes | table A de `LIEUX_ET_ROUTES.md` ; JSON `lieux.<id>.caracteristiques.lon/lat` | ajouter `coordonnees_geo.position` à chaque lieu de LIEUX ; statut [PROPOSITION] |
| ALN-136 | CONFLIT TRANCHÉ (révisé en v0.5.2 : ALN-182) | Haute Tanāḥil (GEO_VAL_HAUTE_TANAHIL) | ~~gorge amont de l'Abay (38,1-38,5° E ; 10,1-11,0° N)~~ : caduc. Canyon au nord du col Abnī-tɨra (§9.6, ALN-182). Tanāḥil reste à la confluence du Tanāḥil et de l'Abnuḥīl (32,55° ; 15,61°) | voir ALN-182 et ALN-183 |
| ALN-137 | PROPOSITION | Les dix îles de Staur-Khlōr | Fogo = Khlōr-Naw ; Boa Vista = Strakh-Kot ; Santiago = Staur-Om ; Santo Antão = Threl-Hal ; São Vicente = Skral-Kot ; Sal = Hleka-Kōr ; São Nicolau = Strakh-Khlōr ; Brava = Aktir-Kot ; îlots Branco et Raso = Skel-Ti ; Santa Luzia = Hal-Kot | §V.7 : ajouter positions ; Kot-Skral sur Skral-Kot, Threskōl-Strakh sur Strakh-Kot |
| ALN-138 | PROPOSITION | Extrémités non documentées | Kralekh-ner, Qūrāš-Ṣafīḥ, Kù-kèdà yì Mù-Kíri, Foyers-Purs, Voie-Desnuées, Voie-Haute, Voie-Comptable, Hae K'umel, Sa-nùbè yì Mù-Sùkú, Cercle-Sans-Juron, Lisières Ba-lóngó : `LIEUX_ET_ROUTES.md` §2.4 | documenter ces lieux (Qūrāš-Ṣafīḥ en priorité : trois routes) |

### 9.3 Lieux : corrections proposées

| ID | Type | Lieu | Constat | Action pour le corpus |
|---|---|---|---|---|
| ALN-140 | CORRECTION | Stakhr-Durek | steppe de piémont (546 mm), pas de désert de sable | biome → `steppe_piemont` ; « cordons sableux, ensablement des pistes en saison sèche » |
| ALN-141 | CORRECTION | Hloran-rir, Oase-Skren | steppe (480-700 mm) | « oasis de résurgence en steppe de piémont » |
| ALN-142 | CORRECTION | Li-sèk-dì | 2 900 mm/an : climat de golfe équatorial | « îlots sans nappe ni source : la pluie ne se garde pas » ; garder la fonction (bannissement) |
| ALN-143 | CORRECTION | Imekh-stom, Akhileth | l'Imikhrel est un oued (débit modélisé ~0) | « crues d'oued, rares et brutales » |
| ALN-144 | CORRECTION | Akhileth | forêt de montagne à ~150 km du goulet | scinder : comptoir au goulet, coupes sur le piémont de !Okheti ; RT_035 : + portage de 70 km |
| ALN-145 | CORRECTION | Kù-téka, Jáli-Fè, Šafāq-Mirq, Cherbekh-khem, Abnīqa | aucun sable à 25 km | « ensablement » → « envasement, colmatage alluvial » |
| ALN-150 | DÉCIDÉ (révision) : hauts plateaux de qoyra (37,86° ; 10,65°, 3 440 m, prairie) ; façade URU_C → URU_SE ; voir §9.6 | \|'Ukh-‖Sék | crête à ~2 250 m, prairie à ~2 900 m à 9,5° N | biome → forêt de montagne claire, refuges à 2 200-2 400 m ; ou déplacer le sanctuaire sur les plateaux de qoyra et revoir RT_009 |
| ALN-151 | DÉCIDÉ (révision) : reste à \|'Ara-Sukhì ; territoire URM réattribué (ALN-156) | \|'Urum-!Samel | seuls glaciers : \|'Ara-Sukhì (k'ara) ; cols URM sur lóngò, à 1 300 km | garder à \|'Ara-Sukhì (pèlerinage) ; ou retirer `glacier` |
| ALN-152 | CONFLIT TRANCHÉ | Ts'idar-‖Sek ; RT_061 | interface Költ / HKL_S-SO à l'ouest (retenu, crête de halekh oriental, 2 840 m) ; RT_061 vers K'elis-‖ara : 4 200 km, 216 jours | RT_061 : remplacer K'elis-‖ara par Hlelak-!uri (GEO_COL_032) ou Kraloth-!enu (GEO_COL_035) ; noter une colonie Ts'idari à l'ouest |
| ALN-153 | CORRECTION | Tanāḥil | « avalanches sur l'accès au col Abnī-tɨra » : col à 920 km | viser T'iqur-ɨlkh (GEO_COL_014) ou Rafīq-t'sal (GEO_COL_047) |
| ALN-154 | PRÉCISION | Hae Ts'i-K'uré | monastère à 1 890 m, hors \|'Arin ; le col P'etsul-!ama (2 600 m) est en Hiver Gris | rattacher « hypoxie/froid » à la montée du col (RT_065) |
| ALN-155 | CORRECTION | Q'irel-Ts'idar | 1 370 mm/an | « saison sèche marquée » au lieu de « sécheresses prolongées » ; ou déplacer vers le plateau sec du nord-est |

### 9.4 Routes : corrections proposées

| ID | Type | Routes | Constat | Action pour le corpus |
|---|---|---|---|---|
| ALN-160 | AJOUT (décidé : nommer les principales, ALN-180) | cordillère | brèches plus basses que les cols : prolongement SE de k'ara 1 180 m (27,0° E ; 11,9° N), 1 240 m (32,9° E), 1 580 m (31,5° E) ; lóngò 1 200-1 670 m | registre : ajouter des « trouées » (voies basses, longues ou exposées) ; les cols restent les voies courtes et gardées |
| ALN-161 | PRÉCISION | RT_010 | optimal : 1 260 km, 39 j, par la trouée (1 690 m) ; par T'iqur-ɨlkh (2 700 m, juin-oct.) : 2 610 km, 69 j | préciser le col (GEO_COL_014) et la raison de le préférer, ou retirer l'hypoxie |
| ALN-162 | PRÉCISION | RT_062, RT_051 | « toute l'année » par des cols fermés en hiver (T'araq-ɨnkh nov.-avr. ; Hlenik-k'eso déc.-mars) | préciser le dépôt d'hiver (Silos de Trêve) et le service d'hiver du corridor d'État |
| ALN-163 | CORRECTION (décidée) | RT_020 | Mù-Kíri (Atlantique) → Ts'idar-ré : 5 080 km, 189 j | origine → Kù-békà (cité-mère du Tùmázì) ; modes : lacustre + caravane + col ; 1 370 km, 50 j, point haut 2 310 m (`LIEUX_ET_ROUTES.md` table G) |
| ALN-165 | PRÉCISION | RT_001 | Kù-békà ↔ Kù-téka : 2 440 km, 84 j | annoter « grande caravane trans-forestière (~3 mois) » |
| ALN-166 | CORRECTION | RT_029 ; Ku-Bángá | Mù-dárhòbì à ~1 900 km du Tùmázì ; « canaux inter-lacs » impossibles | Mù-dárhòbì → collines Kù-kɨ́bò (basalte de Ku-Bángá) ; supprimer les canaux inter-lacs |
| ALN-167 | CORRECTION | RT_070 ; Sa-kúmadì, Ku-pèpanà | pôles et lisières au Sud Mopámà pour des lieux du Sud Tùmázì | lisières → rive S du Tùmázì ; pôle → Kù-békà |
| ALN-170 | AJOUT | RT_003, RT_059, RT_031, RT_071 | rapides : émissaire du Mopámà (140-160 km de portage) ; gorge de la haute Tanāḥil (110-220 km de piste) | ajouter `terrestre_portage` ou `terrestre_caravane` |
| ALN-171 | CORRECTION | portage NO (RT_027 ; §VI.1.2 « 3 jours ») | 291 km, 14 jours, point haut ~1 230 m | « 12 à 15 jours » ; ALN-033 (8-10 jours) est remplacé |
| ALN-172 | IMPOSSIBILITÉ | RT_046, 056, 033, 049, 074, 072, 047, 007, 036, 032, 035 | mer Halakhel et Tùmázì fermés ; isthme entre Méditerranée et mer Rouge | ajouter le segment terrestre mesuré (`LIEUX_ET_ROUTES.md` §5.1, LT-01 à LT-11) |
| ALN-173 | PRÉCISION | caravanes Halakhel E → mer Rouge (« 8 jours ») | 370 km au plus court | 8 jours suppose ~45 km/j (méharée) ; 12-13 jours en caravane chargée |
| ALN-175 | PRÉCISION | fenêtres saisonnières | mois communs des cols franchis : table D (RT_009 mai-oct. ; RT_043 juin-sept. ; RT_068 mai-oct. au lieu d'avr.-nov.) | aligner les fenêtres des routes sur `ouverture_mois` des cols |

### 9.5 Caractéristiques à reporter dans LIEUX

| ID | Type | Objet | Contenu | Action |
|---|---|---|---|---|
| ALN-174 | PRÉCISION | Façades | §4 mis à jour (HKL_NE, HKL_E) ; toutes les façades : table A | reporter |
| ALN-176 | AJOUT | Caractéristiques physiques des lieux | altitude, pluie, températures, faciès du \|'Arin, distances à l'eau, débit, col proche, expositions calculées : tables A à C ; JSON `lieux.<id>.caracteristiques` | ajouter un bloc `physique` à chaque lieu de LIEUX |
| ALN-177 | AJOUT | Métriques des routes | longueur, durée, km par milieu, ruptures de charge, altitude max, dénivelé, cols, mois : table D ; JSON `routes.<id>` | remplir `trajet.metrique` (actuellement « [LACUNE] » partout) |
| ALN-178 | CLOS | Points ouverts | ALN-150, 151, 160, 163 tranchés par l'auteur (§9.6) | — |

### 9.6 Révision après relecture de l'auteur

Signalements vérifiés dans le corpus avant tout déplacement ; détail et mesures : `LIEUX_ET_ROUTES.md` §2.5 (RV-01 à RV-07).

| ID | Type | Objet | Décision et mesures | Action pour le corpus |
|---|---|---|---|---|
| ALN-139 | AJOUT (géographie) | Delta du Sud Mopámà | plaine deltaïque basse à mangroves sur la côte au sud du lac (contour : §8, « Positions paramétrées ») ; point de calage des pluies 2 400 mm (le modèle donnait 5 000-6 500 mm) | §V.4 : ajouter un delta côtier au sud du bassin (nom à forger) ; forêt de marée 30 440 → 38 430 km² |
| ALN-146 | CORRECTION (avérée) | Ku-jálima-rir, Jáli-Fè, Anses-Jálondù | déplacés vers l'ouest : Ku-jálima-rir (-4,95° ; 5,21°, estuaire du golfe Ku-jálima-rir) ; Jáli-Fè (-3,70° ; 5,22°, delta à lagunes) ; Anses-Jálondù (-1,28° ; 5,10°, face à Li-sèk-dì) | §V.4 : le « delta de Jáli-Fè » est un delta côtier distinct de celui de l'émissaire ; ses bassins sont alimentés par les fleuves atlantiques du SO (et non du bassin-versant du Mopámà) |
| ALN-147 | CORRECTION (avérée) | Kù-Bèláà, Mázì-Dúm ; RT_060 | « mangrove Sud » : delta côtier au sud du lac, à ~500 km (Kù-Bèláà 6,27° ; 4,35° — Mázì-Dúm 6,85° ; 4,62°) ; RT_060 : 1 530 km, 53 j, dont 885 km de côte | LIEUX : préciser « mangrove du delta au sud du Mopámà » ; ALN-081 est remplacé ; RT_060 : « fluvial et lagunaire » |
| ALN-148 | CORRECTION (avérée) | Šālim (ZRS) ; RT_071 | seuil de diffluence de l'Abnuḥīl, tête du bras d'Abnīqa (30,72° ; 27,64°) : digues de la « valve », reflux en crue ; RT_071 : 264 km, 5,5 j | LIEUX : secteur intérieur → « seuil de diffluence (interfluve oriental) » au lieu de la haute Tanāḥil ; biome → `plaine_alluviale` |
| ALN-156 | CORRECTION (décidée) | Territoire URM (registre, relation « territoire ») | URM ← Ṣabūl-tɨkh (GEO_COL_003), Qaṣūl-tɨra (GEO_COL_005), Ṭanīkhūr (GEO_COL_002), autour de \|'Ara-Sukhì ; retirer URM de GEO_COL_024, 025, 028 (lóngò). Positions des cols inchangées | modifier les `renvois` des six cols au registre |
| ALN-180 | AJOUT (décidé) | Trouées principales | TRO_01 (27,0° ; 11,94°, 1 180 m, 360 km), TRO_02 (31,47° ; 10,29°, 1 580 m, 114 km ; 5 routes), TRO_07 (7,25° ; 11,48°, 1 200 m, extrémité S de lóngò) ; TRO_03 à 06 restent anonymes. Positions : `donnees/routes.yaml` ; table H | forger trois noms (`forge-ling`) dans la langue de leurs usagers ; créer un type « trouée » au registre |
| ALN-181 | PRÉCISION | « Delta du Mopámà » du corpus | trois deltas distincts : celui de l'émissaire (Gálu-kánda, ALN-131), celui de Jáli-Fè (ALN-146), celui de la mangrove Sud (ALN-139) | §V.4 : distinguer les trois |

