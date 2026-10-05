# Lieux et routes du Beliet — passe de cohérence (carte v0.5, révisée)

Ce document confronte les lieux (LIEUX_URBAINS v2 : 56 cités LUR, 18 zones ZRS) et les routes (RESEAU_ROUTES v3 : 74 routes) à la géographie de la carte. Il donne pour chaque lieu une position et ses caractéristiques physiques calculées, et pour chaque route un tracé, une longueur, une durée, des altitudes, des cols et des saisons. Il signale chaque écart et propose une solution. Il est écrit pour l'agent qui fait cascader les décisions dans le corpus. Les fiches de synthèse sont reprises dans `ALIGNEMENT_CORPUS.md` §9 (ALN-130 à ALN-181). La **révision** qui suit la relecture de l'auteur est décrite en §2.5 ; elle prime sur les passages antérieurs.

- **Statut** : toutes les positions sont des [PROPOSITION]. Les mesures sont des [MESURE] de la carte v0.5.
- **Sources de vérité** :
  1. `carte/sig/beliet_lieux_routes.json` : positions, caractéristiques, constats, tracés et mesures, lisibles par machine ;
  2. `donnees/lieux.yaml` : cible raisonnée et contraintes de chaque lieu, avec sa justification ; `donnees/routes.yaml` : réglages de tracé ;
  3. `carte/sig/beliet_lieux.geojson`, `carte/sig/beliet_routes.geojson` : géométries (QGIS) ;
  4. `carte/beliet_carte_lieux.png` et `.svg` (calques) : la carte ; `carte/beliet_carte_ascii.md` §7 : la version texte.
- **Régénération** : `python3 outils/lieux_routes.py` (après `generer_carte.py`).
- **Principe** : le corpus suit la géographie. La géographie n'a été modifiée que pour ajouter un contenu absent et physiquement fondé (§3). Tout le reste est consigné comme correction du corpus.

---

## 1. Méthode

### 1.1 Placement
1. **Cible raisonnée.** Chaque lieu reçoit une cible tirée du corpus : façade (ALIGNEMENT §4), rôle (port, estuaire, col, oasis…), pôle de rattachement, routes, composantes, ancres canoniques (détroits, estuaires, lacs, cols du registre). La justification figure dans `donnees/lieux.yaml`, champ `note`.
2. **Contraintes.** La cellule retenue doit respecter un type de site : rive de la mer Halakhel, de l'océan ou d'un lac ; berge d'un fleuve nommé ; île ; plate-forme sur un lac ; intérieur. Elle doit aussi rester dans un rayon donné. Elle respecte, si possible, les milieux déclarés par LIEUX et une plage d'altitude.
3. **Choix.** Parmi les cellules admissibles, le script retient la plus proche de la cible qui porte le milieu déclaré. L'écart à la cible est publié (table A).
4. **Extrémités non documentées** (Kralekh-ner, Qūrāš-Ṣafīḥ, Foyers-Purs, Voie-Haute…) : position déduite des gloses, avec un niveau de confiance. Les institutions prennent la position de leur siège.

### 1.2 Caractéristiques physiques calculées (par lieu)
Altitude ; dénivelé dans un rayon de 10 km ; pente ; milieu du site et milieux dans un rayon de 25 km ; pluie annuelle ; température annuelle ; température du cœur de l'hiver (Tw) et des nuits d'hiver (Tn) ; faciès du |'Arin ; distances à la mer Halakhel, à l'océan, à un lac, au cours d'eau pérenne le plus proche ; fleuve nommé à moins de 30 km ; débit modélisé maximal à 15 km ; col le plus proche (altitude, distance, mois d'ouverture). Le script en déduit des **expositions physiques** : crues, brouillards d'évaporation, ensablement, tempêtes de rivage, avalanches, éboulements, hypoxie, Hiver Blanc, aridité.

### 1.3 Vérifications
Chaque biome déclaré par LIEUX est comparé aux milieux du site et de son voisinage. Chaque exposition géophysique, environnementale ou sanitaire du corpus est comparée aux expositions calculées. Un écart signifie que le site calculé ne soutient pas la mention du corpus. La table C liste tous les écarts ; la §4 les interprète.

### 1.4 Routes
- **Grille** : cellules de ≈ 5 km. Milieux de passage : océan (mer réelle et liseré côtier), mer Halakhel, lac, fleuve navigable, terre. Les terres hors du Beliet sont infranchissables.
- **Modes** : seuls les modes déclarés par la route sont empruntés sans pénalité. Un milieu non déclaré n'est emprunté que s'il est inévitable. Son temps est alors multiplié par 8. La longueur ainsi parcourue est publiée (« hors modes déclarés ») : c'est le tronçon qui manque à la route.
- **Vitesses** (par jour) : cabotage 75 km ; haute mer 150 km ; lac 60 km ; fleuve 80 km à la descente, 28 km à la remontée ; caravane 30 km, portage 22 km, col 20 km, sur terrain plat. Sur terre, la vitesse suit la pente (loi de Tobler) et le milieu (forêt dense, marais, sable, glacier). Chaque 2 500 m de montée ajoute un jour. Au-dessus de 2 200 m, l'altitude ralentit la marche. Chaque rupture de charge entre l'eau et la terre coûte une demi-journée.
- **Navigabilité** : un bief n'est navigable que si sa pente reste sous 1,5 m/km. Au-delà, rapides et chutes imposent un portage.
- **Cols** : un col est « franchi » quand le tracé passe à moins de 15 km au-dessus de 1 200 m. Les mois praticables sont l'intersection des mois d'ouverture des cols franchis (`donnees/cols.yaml`).
- **Variantes** : quand le corpus impose une étape (un col, un relais), une variante est calculée en plus du tracé optimal (table F).
- **Limites** : les durées sont des ordres de grandeur, sans les haltes ni les attentes de saison. Le débit des fleuves est celui du modèle hydrologique (ruissellement sur la pluie calibrée) : il sert à comparer, pas à mesurer.

---

## 2. Décisions de placement

### 2.1 Synthèse par région

| Région | Lieux | Ancrage retenu |
|---|---|---|
| ATL_NO | Khloreth-klam, Stalomar-Kot, Stakhr-Durek, Hloran-rir, Oase-Skren | Khloreth-klam au terminus atlantique du portage le plus court vers l'Halakhel (baie basse, Agadir réel). Stalomar-Kot sur les falaises granitiques du rebord de l'Anti-Atlas, à 75 km. Stakhr-Durek à mi-portage. Hloran-rir et Oase-Skren sur le corridor, au pied du rebord montagneux. |
| ATL_SO | Ku-jálima-rir, Jáli-Fè, Anses-Jálondù, Jáli-lòngò, Gálu-kánda, Li-sèk-dì | (révisé, §2.5) D'ouest en est : Ku-jálima-rir (estuaire du golfe Ku-jálima-rir, -4,95°), Jáli-Fè (delta à lagunes d'eau douce, -3,70°), Anses-Jálondù (anse face à Li-sèk-dì, -1,28°), puis, à 300 km plus à l'est, Gálu-kánda (cales à la tête du delta du Mopámà) et Jáli-lòngò (côte relevée). |
| ATL_INS | Kot-Skral, Threskōl-Strakh | Îles du Cap-Vert réel : Skral-Kot = São Vicente ; Strakh-Kot = Boa Vista (§2.3). |
| HKL_N | Khreth-na-Serek, Serékh-khem, Kralekh-ner | Khreth-na-Serek sur la rive ouest de la passe ; Serékh-khem au fond du golfe de Serek ; Kralekh-ner = sortie nord de la passe. |
| HKL_NO / HKL_O | Akhidalet, Kralekh-Aktrik, Aktrik-khem, Hlom-khetal | Akhidalet à l'embouchure réelle de l'Ehukhtal (-7,72° ; 27,19°), au fond du goulet. Kralekh-Aktrik sur la rive nord du goulet, point de l'Halakhel le plus proche de l'Atlantique. Aktrik-khem à 150 km à l'est. Hlom-khetal sur la rive sud du goulet. |
| HKL_SO / HKL_S | Imekh-stom, Akhileth, Cherbekh-khem, Tawālmaz, Qabḍ-ār-Ǧanūb | Imekh-stom au goulet de l'Imikhrel ; Cherbekh-khem à 230 km à l'est ; Tawālmaz sur la ria de la Madīlan ; Qabḍ-ār-Ǧanūb au cap du golfe de Koufra, extrémité sud de la mer. |
| HKL_E (delta d'Abnīqa) | Abnaqil, Abnīqa, Tanāqil, Qabṣūr-Qibṣ, Ḥawqil, Qūrāš-Ṣafīḥ, Ḥamaḍ-Rās | Abnaqil à l'apex du cône deltaïque, où divergent les chenaux Abnīṣar (NE) et Tanīlḥa (SE). Abnīqa au débouché ouest ; Qūrāš-Ṣafīḥ sur l'Abnīṣar ; Tanāqil sur la Tanīlḥa ; Qabṣūr-Qibṣ sur les salines de la côte, au sud ; Ḥamaḍ-Rās sur un cap au nord ; Ḥawqil à l'embouchure du Ḥawqal. |
| HKL_NE (haute Tanāḥil, seuil de diffluence) | Qūrāš-Tanīqa, Qūrāš-Taniḥīl-Ramšūr, Šālim, Ṣarīq, Tanāḥil | (révisé, §2.2) Haute Tanāḥil = canyon au nord du col Abnī-tɨra (k'ara), affluent occidental de l'Abnuḥīl : Qūrāš-Taniḥīl-Ramšūr ferme la tête du canyon, Qūrāš-Tanīqa est ~110 km en aval. Tanāḥil à la confluence avec l'Abnuḥīl (Khartoum réel). (révisé, §2.5) Šālim au seuil de diffluence de l'Abnuḥīl, tête du bras d'Abnīqa. Ṣarīq en bordure du marais de Ṣaraq. |
| MED_NE | Šafāq-Mirq, Ṭanquish | Šafāq-Mirq aux bouches du delta Šafāqil ; Ṭanquish sur la côte à l'ouest du delta, bordée de lagunes. |
| ROU_SE / IND_SE | T'naya-Ḥaem, K'uré-K'ésun, K'uré-tawa | K'uré-tawa : port corallien (Massawa réel). K'uré-K'ésun : côte basaltique au pied de l'escarpement. T'naya-Ḥaem : golfe de Tadjoura, jonction mer Rouge / océan de l'Est. |
| MOP_SO | Kù-téka, Ku-Ngúmi, Kù-Bèláà, Mázì-Dúm, Ku-sáladì | Kù-téka à la sortie de l'émissaire ; Ku-Ngúmi juste en aval ; Ku-sáladì sur la rive sud du lac ; (révisé, §2.5) Kù-Bèláà et Mázì-Dúm dans la « mangrove Sud », au sud du lac : delta côtier des rivières qui drainent le sud du bassin, à ~500 km du lac. |
| TUM_SC / FOR_S | Kù-békà, Ku-Pɨla-Mù-Sùkú, Q'eša-Kɨ́bò et 10 ZRS | Kù-békà sur pilotis près de la rive nord ; Ku-Pɨla-Mù-Sùkú sur la rive sud-ouest, au pied des collines Kù-kɨ́bò où se tient Q'eša-Kɨ́bò ; bancs et récifs dans le lac ; bourgs de rive au nord et au nord-est ; Sa-kúmadì et Ku-pèpanà dans la haute futaie de la rive sud. |
| URU_NO / URU_SO | Bannaktì, !Tamar-‖Khu | Bannaktì au cœur du territoire KOL (halekh occidental, 1 770 m). !Tamar-‖Khu dans les vallées sud de lóngò. |
| URU_C | Zagakh-TƗr, \|'Urum-!Samel, \|'Ukh-‖Sék, ‖Ethak-Kél-Ts'idar, Ts'idar-‖Sek | Zagakh-TƗr sur l'émissaire de l'Akhtir. \|'Urum-!Samel sous les glaciers de \|'Ara-Sukhì (3 710 m). (révisé, §2.5) \|'Ukh-‖Sék sur les hauts plateaux de qoyra, au-dessus de la gorge du Tanāḥil (3 440 m). ‖Ethak-Kél-Ts'idar au col T'araq-ɨnkh. Ts'idar-‖Sek sur la crête de halekh oriental (§4, LR-12). |
| URU_SE / PLT_SE | Gîtes-Ts'idar, Ts'idar-ré, Q'irel-Ts'idar, K'umal-Naqra, Hae Ts'i-K'uré, P'i-K'uré-Neša, Hae-P'ešu | Groupe Ts'idar autour des cols T'araq-ɨnkh et Q'usa-‖ema : Gîtes au pied de l'escarpement ; Ts'idar-ré au col Q'usa-‖ema ; Q'irel-Ts'idar sur le plateau, en citadelle au-dessus du col T'araq-ɨnkh. K'umal-Naqra sur le rebord oriental, au-dessus de la mer Rouge. Hae Ts'i-K'uré au pied du col P'etsul-!ama. P'i-K'uré-Neša et Hae-P'ešu sur le plateau au-dessus de K'uré-tawa. |

### 2.2 La haute Tanāḥil est le canyon nord du col Abnī-tɨra (révision RV-08 ; ALN-136 révisé, ALN-182)

**Lecture v0.5 abandonnée.** La v0.5 plaçait la haute Tanāḥil dans la gorge amont de l'Abay (38,1-38,5° E ; 10,1-11,0° N). Les deux cités TNQ y tombaient au sud-est, à 2 300 m, à 45 km l'une de l'autre, hors du bassin qu'elles déclarent. L'auteur l'a signalé ; le corpus lui donne raison.

**Indices du corpus (vérifiés).**
- Géosystème : « segment amont du cours du Tanāḥil, **en aval des piémonts septentrionaux de \|\|Urumati-k'ara** » ; « secteur intérieur amont de HKL_NE » ; canyon gréseux/marno-calcaire, semi-aride, crues brutales, « bassins-versants courts, forte pente », résurgences de piémont.
- LIEUX : les deux cités déclarent `bassin_versant_id` GEO_FLV_ABNUHIL, biome `steppe_piemont`, façade HKL_NE. Qūrāš-Taniḥīl-Ramšūr « ferme le fond de canyon » et vit de « la rupture de charge au débouché des cols » ; raids désertiques. Qūrāš-Tanīqa : citadelle-coffre, siège, citernes.
- ROUTES : RT_006 relie le col **Abnī-tɨra** (GEO_COL_001, 2 800 m, k'ara) à Tanāḥil par « cols, vallée, vallée (vertical) ». Les routes proximales de Qūrāš-Taniḥīl-Ramšūr (RT_006, 007, 010, 030, 031) sont celles du « corridor de la haute Tanāḥil ».

**Physique.** Au nord du col Abnī-tɨra, le versant de k'ara débouche à ~800 m sur un piémont de steppe (130-180 mm). Le thalweg calculé file au NE, collecte aussi le débouché du col Ḥamīr-ɨlkh (004), traverse 1 000 km de désert et rejoint l'Abnuḥīl vers 30,6° E ; 18,4° N (analogues réels : Ennedi, wadi Howar). Le relief local n'y dépassait pas 40-110 m : pas de canyon.

**Géographie ajoutée : le canyon de la haute Tanāḥil** (`donnees/parametres_carte.yaml`, clé `canyons`). Il suit ce thalweg sur 465 km, du débouché du col (24,18° E ; 15,92° N) au piémont (27,4° E ; 17,5° N). Tête fermée : le fond plonge de ~190 m sur 15 km (cirque, cascade de crue). Profondeur 170-210 m sur les 120 premiers kilomètres, puis décroissante jusqu'à zéro. Fond large de ~1,5 km, parois raides sur ~3 km. Le fond descend partout vers l'aval (≥ 0,4 m/km) : aucune cuvette fermée. Le canyon est creusé après l'érosion ; le terrain n'est qu'abaissé.

**Placements.**
- **Qūrāš-Taniḥīl-Ramšūr** ferme la tête du canyon, au débouché nord du col Abnī-tɨra : caravansérail-forteresse au pied de la seule montée vers le col, rupture de charge entre la piste du col et celle du canyon.
- **Qūrāš-Tanīqa** est dans le canyon, ~110 km en aval : citadelle-coffre sur un fond encaissé, ravitaillée par citernes, facile à bloquer.

**Écarts consignés, non appliqués** (hors du périmètre demandé) :
- Le registre rattache GEO_VAL_HAUTE_TANAHIL au fleuve Tanāḥil (`partie_de` GEO_FLV_TANAHIL). Le Tanāḥil (Tira-ñara) descend des hauts plateaux SE ; le canyon draine k'ara. Ce sont deux cours distincts du bassin de l'Abnuḥīl. Le rattachement devient `partie_de` GEO_FLV_ABNUHIL (affluent occidental, à nommer) (ALN-182).
- **Tanāḥil** reste à la confluence du Tanāḥil et de l'Abnuḥīl (32,55° ; 15,61°). Le canyon rejoint l'Abnuḥīl ~450 km plus en aval. « En amont du pôle Tanāḥil » reste vrai le long de la route RT_006 (le col, puis le canyon, puis la vallée), pas le long du fleuve. Option pour le corpus : placer Tanāḥil à la confluence du canyon (30,6° ; 18,4°) ; RT_006 deviendrait une descente continue du canyon. Cette option casse le « confluent Tira-ñara/Tanāḥil » du Géosystème ; elle n'est pas retenue (ALN-183).
- **ALN-083** (deux sens de « Tanāḥil ») est rouvert : le fleuve Tanāḥil (SE) et la vallée des villes (N de k'ara) sont deux objets. C'était la lecture de la v0.3.2.

### 2.3 Archipel de Staur-Khlōr : correspondance proposée des dix îles (ALN-137)
Le Cap-Vert réel compte dix îles principales, comme le Géosystème. Proposition [PROPOSITION] : Khlōr-Naw = Fogo (point culminant, ALN-009) ; Strakh-Kot = Boa Vista (la plus grande du sous-groupe aride, tabulaire) ; Staur-Om = Santiago (plaines de lave) ; Threl-Hal = Santo Antão (la plus exposée à l'ouest) ; Skral-Kot = São Vicente (promontoire et baie profonde) ; Hleka-Kōr = Sal (détachée au nord-est, récifs) ; Strakh-Khlōr = São Nicolau (piton nu) ; Aktir-Kot = Brava (aiguille méridionale isolée) ; Skel-Ti = îlots Branco et Raso (« les Jumelles ») ; Hal-Kot = Santa Luzia (banc sableux). Maio reste sans nom. Kot-Skral est placé sur Skral-Kot ; Threskōl-Strakh sur Strakh-Kot.

### 2.4 Extrémités non documentées (ALN-138)
| Extrémité (routes) | Position | Confiance | Raison |
|---|---|---|---|
| Kralekh-ner (RT_002, 005, 039) | sortie N de la passe Khreth-na-Serek | moyenne | « approches nord du détroit » |
| Qūrāš-Ṣafīḥ (RT_022, 039, 041) | chenal NE du delta d'Abnīqa | moyenne | « NE » d'Abnaqil (LIEUX) |
| Kù-kèdà yì Mù-Kíri, Forges-des-Coques (RT_020, 033, 037) | Ku-jálima-rir | moyenne | chantiers Mù-Kíri du quartier Kù-kíri-jálima |
| Foyers-Purs (RT_032, 034, 045) | plateau au-dessus de K'uré-tawa | faible | « hauts plateaux SE », amont de K'uré-tawa |
| Voie-Desnuées (RT_034) | hautes terres de qoyra | faible | aucune indication spatiale |
| Voie-Haute (RT_048) | crête voisine du col P'etsul-!ama | faible | pèlerinage d'altitude vers Hae Ts'i-K'uré |
| Voie-Comptable (RT_049) | P'i-K'uré-Neša | moyenne | même mouvance |
| Hae K'umel (RT_074) | vallées de K'umal-Naqra | faible | « Foyer-Origine » des K'umal |
| Sa-nùbè yì Mù-Sùkú (RT_072) | banc Ku-Sùkú-nà | moyenne | pesée rituelle au temple |
| Cercle-Sans-Juron (RT_033) | Kralekh-Aktrik | faible | « chez les Kisrali » |
| Ports T'nayel SE (RT_007) | T'naya-Ḥaem | moyenne | façade T'nayel |
| Lisières Ba-lóngó (RT_070) | lisière S du Mopámà | faible | glose |
| Méditerranée NE, Ports externes NO | points de mer | faible | façades |

### 2.5 Révision après relecture de l'auteur

L'auteur a tranché quatre points et signalé quatre placements. Chaque signalement a été vérifié dans le corpus. La physique a été vérifiée avant tout déplacement.

| ID | Objet | Indices du corpus vérifiés | Décision | Mesures au nouveau site |
|---|---|---|---|---|
| RV-01 | \|'Ukh-‖Sék (décision) | `prairie_altitude`, refuges à 3 200 m, « sanctuaire-col », routes vers la vallée (RT_021, RT_073) | Hauts plateaux de qoyra, massif qui domine la gorge du Tanāḥil (Choke réel au-dessus de l'Abay) : 37,86° E, 10,65° N | 3 440 m, prairie d'altitude, 710 mm, T 6,8 °C, Hiver Gris (Tw 1,2 °C). RT_009 : 456 km et 25 jours par le col T'araq-ɨnkh (mai-oct.). RT_021 et RT_073 : ~2 300 km, point haut 3 220 m. Plus aucun écart |
| RV-02 | \|'Urum-!Samel (décision) | biome `glacier` ; territoire URM | Reste sous les glaciers de \|'Ara-Sukhì. Le territoire URM est réattribué : Ṣabūl-tɨkh (003, 2 900 m, à 223 km), Qaṣūl-tɨra (005, 2 700 m, 323 km), Ṭanīkhūr (002, 3 200 m, 462 km). Ces trois cols n'avaient pas de territoire au registre. Ku-Pámà-Tɨra-te (024), Lémakhɨ (025) et Ku-Ténɨlkh-te (028) perdent le rattachement URM. Positions des cols inchangées | 3 710 m, Hiver Blanc (Tw −6,1 °C) |
| RV-03 | Trouées basses (décision : nommer les principales) | — | 7 trouées mesurées (table H). 3 trouées « principales » : routes calculées ou liaison entre grands bassins. Nom à forger (§5.3) | table H |
| RV-04 | RT_020 (décision : origine la plus plausible) | Ts'idar-ré est « interface obligatoire… flux trans-cordillère (TRK + MBR) » ; bois et cloches ; « Kù- » est un préfixe ba-mbaro | Origine : Kù-békà, cité-mère du Tùmázì. Traversée lacustre, caravane vers l'escarpement, montée au col (table G) | 1 370 km, 50 jours, point haut 2 310 m, au lieu de 5 080 km et 189 jours depuis l'Atlantique |
| RV-05 | Kù-Bèláà, Mázì-Dúm (signalement : au sud du Mopámà, pas au delta de l'émissaire) | **avéré** : « ceinture de sécurité de la mangrove Sud » ; « pirogues lourdes venant de l'Atlantique » ; « invisible depuis le fleuve » | Une forêt de marée exige la marée : elle n'existe pas au bord d'un lac d'eau douce à 800 m. Au sud du lac, la seule mangrove possible est la côte, à ~500 km, dans le delta des rivières qui drainent le sud du bassin (delta réel du Niger). Carte : plaine deltaïque ajoutée, pluie bornée (ALN-139) | Kù-Bèláà 6,27° E, 4,35° N ; Mázì-Dúm 6,85° E, 4,62° N ; mangrove, 2 000-2 200 mm, hors \|'Arin. Plus aucun écart |
| RV-06 | Jáli-Fè, Ku-jálima-rir, Anses-Jálondù (signalement : plus à l'ouest, pas au delta du Mopámà) | **avéré** : golfe Ku-jálima-rir à l'ouest ; Ku-jálima-rir « port linéaire en pointe d'estuaire » ; Jáli-Fè « delta (golfe Jálondù / arrière-mangrove de Ku-jálima-rir) » à bassins d'eau douce ; Li-sèk-dì « au large de l'anse Jálondù » | Ku-jálima-rir à l'estuaire du golfe Ku-jálima-rir (Bandama réel) ; Jáli-Fè sur le delta à lagunes voisin (Comoé et lagune Aby réels) ; Anses-Jálondù face aux îlots Li-sèk-dì. L'étiquette du golfe Jálondù est déplacée. Écart restant : « bassins alimentés par les fleuves du bassin-versant du Mopámà » ; ces fleuves côtiers ne drainent pas le Mopámà | Ku-jálima-rir -4,95° ; 5,21° (débit 3 200 m³/s à 15 km) ; Jáli-Fè -3,70° ; 5,22° ; Anses-Jálondù -1,28° ; 5,10°. RT_054 : 150 km ; RT_055 : 320 km ; RT_003 : 1 480 km, émissaire puis 860 km de cabotage |
| RV-07 | Šālim (signalement : au NE, plus au nord) | **avéré** : HKL_NE ; « restes cyclopéens de digues » ; « fleuve coulant à l'envers la nuit » ; RT_071 « fluvial après crues, chenaux mobiles » vers Abnīqa ; Ṭanquish a recueilli les scribes de sa chancellerie | Seuil de diffluence de l'Abnuḥīl, tête du bras d'Abnīqa. C'est la « valve » de l'interfluve : en crue, l'eau y repart vers la mer intérieure. Les digues sont celles de la valve | 30,72° E, 27,64° N ; 30 m, plaine alluviale, 140 mm, Hiver Jaune. RT_071 : 264 km et 5,5 jours au lieu de 3 830 km. Écart restant : `steppe_piemont` (vallée irriguée en désert) |

**Conséquence sur les deltas.** Le delta de l'émissaire (ALN-131) reste celui de Gálu-kánda (cales). Le « delta de Jáli-Fè » est un autre delta côtier, plus à l'ouest. La « mangrove Sud » est un troisième delta, au sud du lac. Le corpus réunissait les trois sous le seul nom de « delta du Mopámà ».

---

## 3. Modifications de la géographie (v0.5)

Quatre changements apportent un contenu absent jusqu'ici. Chacun est physiquement fondé. Aucun ne déplace un lieu canonique, un lac, une chaîne ou un col.

| ID | Changement | Pourquoi | Physique | Effet mesuré |
|---|---|---|---|---|
| ALN-130 | **Rivages escarpés de l'Halakhel** : 7 secteurs de falaises, caps et rias (100 à 170 m de commandement) : passe Khreth-na-Serek, goulet Hlom-khetal, goulet d'Imekh-stom, rias de Cherbekh-khem, ria Tawālmaz, cap de Qabḍ-ār-Ǧanūb, cap de Ḥamaḍ-Rās | La v0.4 imposait un glacis à tout le pourtour (5,5 m/km) : aucun littoral rocheux, alors que LIEUX en déclare 9 et que le Géosystème décrit passe, promontoire, goulets et rias | Rebords de plateaux (hamadas calcaires, coulées basaltiques, grès) tranchés par la mer ; vallées noyées pour les rias. Le glacis reste la règle ailleurs (« HKL_S glacis ») | Littoral rocheux : 12 750 → 20 990 km² ; 8 lieux sur 9 dans leur milieu (Akhileth excepté, LR-05) |
| ALN-131 | **Plaine deltaïque du Mopámà** : terrain abaissé à 1 m + 0,16 m/km de la mer, sur ~180 km de côte | Le delta (GEO_DLT_MOPAMA, « delta de Jáli-Fè », « mangroves ») était un plateau de 20 à 40 m sans mangrove | Delta tropical à sédiments abondants (lac de 28 000 km², émissaire de 650 km) : plaine basse, marées, mangroves | Forêt de marée : 29 350 → 30 440 km² ; mangroves au delta de l'émissaire (Gálu-kánda, estuaire du Mopámà) |
| ALN-132 | **Chenaux du cône d'Abnīqa** : Abnīṣar (NE) et Tanīlḥa (SE) tracés depuis l'apex (28,95° ; 27,6°) | Canon (GEO §VI.1.3) jamais dessiné | Cône de déjection à chenaux instables (Géosystème, interfluve) | Abnaqil, Qūrāš-Ṣafīḥ et Tanāqil reçoivent un site |
| ALN-133 | **Règle du littoral rocheux** : hauteur mesurée au-dessus de l'eau voisine (la mer Halakhel est à −20 m) ; pente à l'échelle de la latitude ; liseré protégé du lissage | La règle mesurait la hauteur au-dessus de l'océan et le lissage effaçait les liserés étroits | Correction de calcul | Inclus dans ALN-130 |
| ALN-134 | **Deux points de calibration des pluies** : versant humide ouest des plateaux SE (2 200 mm) ; rive sud du Tùmázì (1 800 mm) | Le modèle donnait jusqu'à 9 500 mm à l'escarpement des cols T'araq-ɨnkh et Q'usa-‖ema, et 3 800 mm au sud du Tùmázì, hors de toute plage du corpus | Maxima orographiques ramenés à des valeurs plausibles (2 900 et 2 450 mm au point) | Gîtes-Ts'idar 9 530 → 3 800 mm ; ‖Ethak-Kél 7 500 → 3 080 mm |
| ALN-139 | **Delta du Sud Mopámà** (révision) : plaine deltaïque basse à mangroves sur la côte au sud du lac (4,8-7,8° E) ; troisième point de calage des pluies (2 400 mm) | « mangrove Sud » de Kù-Bèláà et Mázì-Dúm (RV-05) | Delta réel du Niger : grand fleuve tropical, marées, mangroves. Le modèle y donnait 5 000-6 500 mm | Forêt de marée : 30 440 → 38 430 km² ; pluie au point 2 610 mm |

**Non modifié, consigné :**
- **Brèches des chaînes** (ALN-160) : le prolongement SE de k'ara et lóngò ont des brèches plus basses que leurs cols. Relever les crêtes reviendrait à plier la géographie au corpus.
- **Distance Mopámà-Tùmázì** (~2 000 km, ALN-165) : le Tùmázì reste au Sud-Centre (choix v0.3.1).
- **Sables du portage NO** (ALN-140) : le corridor reçoit 300 à 550 mm/an (calage du corpus lui-même) ; c'est une steppe, pas un erg.

---

## 4. Lieux : constats et solutions

Biomes et expositions de 74 lieux (106 mentions) confrontés au site : 54 lieux sans écart, 25 mentions en écart (après révision). Les écarts restants et leur traitement :

| ID | Lieu | Constat (mesure) | Solution proposée | Fiche |
|---|---|---|---|---|
| LR-01 | Stakhr-Durek | Corpus : `desert_sableux`, « ensablement des pistes », « tempêtes de sable ». Site : steppe de piémont, 546 mm/an, Hiver Gris. Aucun erg à moins de 25 km | Requalifier en « steppe de piémont à cordons sableux ». Le portage traverse des sables mobiles, pas un désert de sable. Garder l'ensablement comme aléa des pistes en saison sèche | ALN-140 |
| LR-02 | Hloran-rir, Oase-Skren | Corpus : `oasis`. Site : steppe (480 à 700 mm). L'oasis est une résurgence irriguée dans une steppe, pas un îlot dans un désert | Requalifier « oasis de résurgence en steppe de piémont » ; garder la dépendance aux « pluies d'altitude » (le rebord voisin reçoit ~700 mm) | ALN-141 |
| LR-03 | Li-sèk-dì | Corpus : îlots secs, `ile_aride`, sans eau douce. Site : 2 900 mm/an, mangrove | Impossible sous ce climat de golfe équatorial. Requalifier « îlots rocheux sans nappe » : la pluie tombe mais ne se garde pas (substrat corallien et rocheux, pas de nappe). L'aridité devient hydrique, pas climatique | ALN-142 |
| LR-04 | Imekh-stom | « crues subites de l'Imikhrel » : débit modélisé ~0 m³/s ; l'Imikhrel est un oued (179 mm au goulet) | Requalifier en « crues d'oued, rares et brutales » ; la remarque vaut aussi pour la « vase estuarienne » d'Akhileth | ALN-143 |
| LR-05 | Akhileth | `littoral_rocheux` + `foret_montagne` : le premier étage boisé (!Okheti) est à ~150 km du goulet ; site retenu : steppe de piémont, 443 m | Scinder : comptoir côtier au goulet + coupes sur le piémont de !Okheti (RT_035 devient fluvial + portage de 70 km) | ALN-144 |
| LR-06 | Kù-téka, Jáli-Fè, Šafāq-Mirq, Cherbekh-khem, Abnīqa | « ensablement » non soutenu par le voisinage : aucun sable à 25 km | Lire « envasement » ou « colmatage par les alluvions » : ce sont des embouchures et des chenaux deltaïques | ALN-145 |
| LR-07 | Ṭanquish | `depression_saline` absent du site (plaine alluviale) | Les lagunes salées de bordure (Maqbaṣ côtiers) sont sous la résolution de la carte ; garder | — |
| LR-08 | Ku-Ngúmi, Ku-Nómà | `zone_humide_lacustre`, `plaine_alluviale` : site en forêt tropicale de berge | Garder ; milieux de bordure plus étroits que la maille de la carte | — |
| LR-09 | Mázì-Dúm, Kù-Bèláà | Résolu par la révision (RV-05) : mangrove Sud | — | ALN-147 |
| LR-10 | \|'Ukh-‖Sék (résolu : RV-01) | `prairie_altitude`, refuges à 3 200 m. La crête du prolongement SE de k'ara culmine à ~2 450 m vers 9,5° N ; la prairie commence à ~2 900 m à cette latitude | (a) le corpus garde le site et remplace « prairie » par « forêt de montagne claire » et « refuges à 2 200-2 400 m » ; ou (b) le sanctuaire va sur les hauts plateaux de qoyra (> 3 000 m), à l'est de T'araq-ɨnkh, ce qui oblige à revoir RT_009 | ALN-150 |
| LR-11 | \|'Urum-!Samel (résolu : RV-02) | Seul lieu à biome `glacier` : seuls les flancs de \|'Ara-Sukhì (k'ara) en portent. Site : 3 710 m, prairie et zone périglaciaire sous les glaciers, Hiver Blanc. Or les cols du territoire URM (024, 025, 028) sont sur lóngò, à 1 300 km | Garder le sanctuaire à \|'Ara-Sukhì : les URM y montent en pèlerinage depuis leurs vallées de lóngò ; ou retirer `glacier` et placer le bourg sur lóngò | ALN-151 |
| LR-12 | Ts'idar-‖Sek | Deux ancrages incompatibles : « interface Költ (Bannaktì) / façade HKL_S/SO (Cherbekh-khem) » à l'ouest ; ethnie Ts'idari et RT_061 vers K'elis-‖ara à l'est, à 3 900 km | Retenu : crête de halekh oriental (2 840 m, Hiver Blanc, « Mur de l'Hiver »). Corriger RT_061 (LT-21) | ALN-152 |
| LR-13 | Tanāḥil | « Avalanches de redoux sur l'accès au col Abnī-tɨra » : le col est à 920 km | Viser le col de la haute Tanāḥil : T'iqur-ɨlkh (2 700 m) ou Rafīq-t'sal (2 300 m) | ALN-153 |
| LR-14 | Hae Ts'i-K'uré | « Hypoxie/froid » : le monastère est à 1 890 m, hors \|'Arin ; c'est le col P'etsul-!ama (2 600 m, Hiver Gris) qui l'expose | Rattacher l'exposition à la montée du col (RT_065) | ALN-154 |
| LR-15 | Gîtes-Ts'idar | « blocages par avalanches en amont » : site à 1 380 m hors \|'Arin ; les cols voisins sont en Hiver Gris | Garder : l'aléa vient des cols (amont) ; préciser « en amont, aux cols T'araq-ɨnkh et Q'usa-‖ema » | — |
| LR-16 | Q'irel-Ts'idar | « Sécheresses prolongées » : 1 370 mm/an sur le plateau à l'est des cols | Lire « saison sèche marquée » ; ou situer Q'irel-Ts'idar plus au nord-est, sur le plateau sec qui borde la haute Tanāḥil (500 à 700 mm vers 38,3° E, 10,5-11° N), au prix d'un RT_009 plus long | ALN-155 |
| LR-17 | K'umal-Naqra | « glissements de terrain » : versants modérés au site retenu ; « canaux, conflits pour l'eau » : 94 mm/an | Garder : vallées encaissées irriguées du rebord oriental, arides. Les glissements relèvent des corniches de RT_067 | — |
| LR-22 | Šālim | `steppe_piemont` au seuil de diffluence (plaine irriguée, 140 mm) ; « canyon gréseux » : vallée entaillée dans les plateaux calcaires | Biome → `plaine_alluviale` ; écosystème → « vallée entaillée dans les plateaux marno-calcaires, au seuil de diffluence » | ALN-148 |
| LR-23 | Jáli-Fè | « bassins alimentés par les fleuves atlantiques pérennes du bassin-versant Mopámà » : les fleuves côtiers de son delta ne drainent pas le Mopámà | « fleuves atlantiques pérennes du SO » | ALN-146 |
| LR-18 | Ku-Bángá | « piémonts basaltiques du Mù-dárhòbì (Sud Mopámà) » sur la rive du Tùmázì : le Mù-dárhòbì est à ~1 900 km | Remplacer par « piémonts des collines Kù-kɨ́bò » ; le basalte vient de ces collines | ALN-166 |
| LR-19 | Sa-kúmadì, Ku-pèpanà | Façade FOR_S (rive S du Tùmázì) mais pôle Kù-téka (Mopámà, ~1 900 km) ; Ku-pèpanà « ouvrant sur le Sud Mopámà » | Pôle de rattachement → Kù-békà ; ou déplacer Ku-pèpanà en FOR_SO | ALN-167 |
| LR-20 | Bannaktì | Hiver Jaune au site (234 mm) ; « fermeture \|'Arin 3 mois » | Cohérent : la fermeture est celle des cols KOL (Hiver Gris ou mixte, fermés de décembre à mars) | — |
| LR-21 | Qabṣūr-Qibṣ | « cécité des neiges (réverbération) » | Cohérent si l'on lit la réverbération du sel ; aucune neige sur la côte (Hiver de Vapeur) | — |

**Caractéristiques à reporter (extraits ; tout est dans les tables A à C) :**
- **Brouillards d'évaporation.** Tous les ports de l'Halakhel sont en Hiver de Vapeur : Akhidalet, Serékh-khem, Tanāqil, Khreth-na-Serek. Les brumes du corpus sont confirmées.
- **Climat des ports.** Les ports atlantiques NO sont humides et doux : Khloreth-klam 1 410 mm, Tw 9 °C. Le portage NO est en Hiver Gris.
- **Le Sud tropical** est hors \|'Arin : lacs, delta, Corne côtière.
- **Hauts lieux.** Ts'idar-‖Sek (2 840 m) et \|'Urum-!Samel (3 710 m) sont en Hiver Blanc : Tw −2,8 et −6,1 °C.
- **Débits.** Abnaqil est à l'apex du delta : ~4 400 m³/s modélisés. Tanāḥil, à la confluence : ~4 100 m³/s. Jáli-Fè, au delta du Mopámà : ~2 500 m³/s.

---

## 5. Routes : constats et solutions

74 routes tracées. 22 empruntent un milieu absent de leurs modes déclarés, dont 15 de plus de 50 km. 21 dépassent 2 500 km ; une dizaine sont de simples traversées de la mer Halakhel ou de l'océan.

### 5.1 Mer fermée et isthmes : portages manquants (ALN-172)
La mer Halakhel est fermée (§VI.1.2). Aucune voie d'eau ne relie la mer Rouge à la Méditerranée ou à l'Abnuḥīl. Les routes suivantes déclarent un trajet maritime ou fluvial seul et ne peuvent pas s'en passer. Le tronçon terrestre manquant a été mesuré.

| ID | Route | Modes déclarés | Tronçon terrestre imposé | Solution |
|---|---|---|---|---|
| LT-01 | RT_046 Imekh-stom ↔ Ku-jálima-rir | cabotage | 275 km (portage NO Kralekh-Aktrik → Khloreth-klam) | ajouter `terrestre_portage` (ALN-071 confirmé) |
| LT-02 | RT_056 Talom-ak ↔ Kisralom | cabotage | 280 km (même portage) | ajouter `terrestre_portage` |
| LT-03 | RT_033 Forges-des-Coques ↔ Cercle-Sans-Juron | cabotage | 280 km | idem |
| LT-04 | RT_049 Voie-Comptable ↔ Kisralom | cabotage | 300 km (isthme de Suez, puis portage NO) | ajouter deux portages ; ou faire partir la route d'un port méditerranéen |
| LT-05 | RT_074 Hae K'umel ↔ Talom-ak | cabotage « SE→NO » | 350 km (descente du plateau, isthme, portage) | idem ; 7 150 km, 104 jours |
| LT-06 | RT_072 Sa-nùbè yì Mù-Sùkú ↔ Talom-ak | fluvial + cabotage | 170 km (bassin fermé du Tùmázì → réseau atlantique ou nilotique) | ajouter un portage ; 9 400 km, 156 jours : la plus longue route du réseau |
| LT-07 | RT_047 Kù-békà ↔ Ku-jálima-rir | fluvial + lacustre + cabotage | 440 km : le Tùmázì est fermé ; la ligne de partage avec les rivières atlantiques passe à ~250-450 km du lac | ajouter `terrestre_portage` (voie Bénoué : ALN-082 précisé) |
| LT-08 | RT_007 Tanāḥil ↔ Ports T'nayel | fluvial + cabotage | 140 km (isthme de Suez ; ou Nil → mer Rouge, ~200 km) | ajouter `terrestre_caravane` (corpus : « caravanes Halakhel E → mer Rouge, 8 jours ») |
| LT-09 | RT_036 K'uré-tawa ↔ Abnaqil | cabotage + fluvial | 110 km (mer Rouge → vallée de l'Abnuḥīl) | idem |
| LT-10 | RT_032 Foyers-Purs ↔ Voie-Pure-des-Vallées | cabotage + fluvial | 230 km (descente du plateau + isthme) | idem |
| LT-11 | RT_035 Akhileth ↔ Imekh-stom | fluvial + côtier | 70 km (aucun cours pérenne) | `terrestre_portage` (LR-05) |

Écarts mineurs, sans action : Abnaqil est à 20 km de la mer, sur le bras d'Abnīqa (RT_002, 012, 015, 017, 023 : accès fluvial au port). Qabṣūr-Qibṣ est sur le rivage (RT_030 : 50 km de mer au départ).

**RT_060 Kù-Bèláà → Ku-jálima-rir** (« fluvial discret », révisé) : 1 530 km et 53 jours entre la mangrove Sud et l'estuaire de Ku-jálima-rir, dont 885 km le long de la côte. La voie « fluviale » discrète est la chaîne de lagunes côtières qui longe ce littoral (lagunes réelles de Lagos à Abidjan, sous la résolution de la carte). **Action** : préciser « lagunaire et côtier » (ALN-147).

### 5.2 Rapides : émissaire du Mopámà et haute Tanāḥil
- **Émissaire du Mopámà.** Il descend de 800 m sur 650 km (1,2 m/km en moyenne). Plusieurs biefs dépassent 1,5 m/km. RT_003 (Kù-téka → Ku-jálima-rir) et RT_059 (Ku-Ngúmi → estuaire) comptent 140 à 170 km de portage autour des rapides. Le corpus le dit déjà : aléa « barres/rapides » de RT_003. **Action** : ajouter un segment `terrestre_portage` aux deux routes, ou préciser « navigable par biefs » (GEO §VI.3 : « navigable, ~600 km ») (ALN-170).
- **Haute Tanāḥil.** La gorge n'est pas navigable. RT_031 (Gîtes-Ts'idar → Tanāḥil) commence par ~220 km de descente de l'escarpement avant le premier bief navigable. **Action** : ajouter `terrestre_caravane` en tête de la route (ALN-170).

### 5.3 Cols et brèches de la cordillère
- **Brèches** (ALN-160). Le profil de crête mesuré montre des passages plus bas que les cols canoniques :
  - prolongement SE de k'ara : 1 180 m vers 27,0° E, 11,9° N (sur ~360 km) ; 1 240 m vers 32,9° E ; 1 580 m vers 31,5° E. Les cols canoniques de ce tronçon sont à 2 100-2 800 m.
  - lóngò : 1 200 à 1 670 m en six points. Ses cols sont à 1 900-2 400 m.
  Ces brèches sont du relief réel (monts Nouba, cuvette du Sudd, plateau de Jos) que les chaînes n'ont pas recouvert. Un convoi qui veut seulement passer les emprunte.
  **Solutions** : (a) ajouter au registre des « trouées » à nommer, voies basses chaudes et sans neige mais longues ou exposées (marais, raids) ; les cols restent les voies courtes, gardées, à péage ; (b) relever les crêtes de la carte, solution écartée car elle plierait la géographie au corpus.
- **Trouées à nommer** (révision, décision de l'auteur ; table H). Sept trouées sont mesurées. Trois sont principales :
  - **TRO_02** (1 580 m, 31,5° E). Cinq routes calculées l'empruntent : RT_020, 025, 048, 061, 068. C'est la voie basse entre les monastères du col P'etsul-!ama et la jonction de qoyra.
  - **TRO_01** (1 180 m, 27,0° E, 360 km de large). C'est la grande dépression entre le Marra et le prolongement SE (monts Nouba réels). Elle relie les plaines de l'Abnuḥīl au bassin du Tùmázì. C'est la plus basse et la plus large.
  - **TRO_07** (1 200 m, extrémité S de lóngò). Elle relie le bassin du Mopámà aux plaines du nord-est de lóngò.

  Les autres (TRO_03, 04, 05, 06) restent anonymes : elles sont étroites, ou seulement traversées par des routes qui ont un col à proximité.

  **Le nom n'est pas forgé ici.** Le pipeline `forge-ling` exige le fichier LING de la langue et la base sémantique (`ARCHIVES HISTORIQUES ET ETYMOLGIES.md`), absents de ce dépôt. Le champ reste vide, sans forme provisoire.

  **Langue du nommeur** : celle de ceux qui empruntent la trouée et la perçoivent.
  - TRO_01 : caravaniers šamqiriyyūn des plaines du nord, ou riverains ba-mbaro du Tùmázì.
  - TRO_02 : Tɨrakh des monastères et Ts'idari.
  - TRO_07 : Ba-mbaro du Mopámà, Tɨrakh de lóngò.
- **RT_010 Tanāḥil → Kù-békà** (ALN-161). Le corpus annonce un col à 2 700-2 800 m, ouvert de juin à octobre.
  - Tracé optimal : 1 260 km, 39 jours, par la trouée basse (1 690 m), sans col.
  - Variante par T'iqur-ɨlkh (2 700 m, juin-octobre, seul col de ce profil sur la remontée de la Tanāḥil) : 2 610 km, 69 jours.
  **Solution** : garder le col si la route est contrôlée ou rituelle ; sinon la route commerciale passe la trouée.
- **Fenêtres saisonnières** (ALN-175 ; mois d'ouverture des cols franchis) :
  - RT_009 : mai → octobre (corpus : « été, 4 mois ») ;
  - RT_019 : avril → novembre ;
  - RT_043 : juin → septembre (corpus : « fin \|'Arin → été ») ;
  - RT_051 : avril → novembre ; le corpus annonce aussi « toute l'année (corridor d'État) », qui exige un service d'hiver au col Hlenik-k'eso ;
  - RT_053 : mai → octobre ;
  - RT_064 : juin → octobre ;
  - RT_065 : mai → octobre (identique) ;
  - RT_068 : mai → octobre (corpus : avril-novembre ; écart d'un mois de part et d'autre).
- **RT_062** Gîtes-Ts'idar ↔ ‖Ethak-Kél « toute l'année » passe par le col T'araq-ɨnkh, fermé de novembre à avril. Il faut un dépôt d'hiver, que le corpus mentionne déjà : les « Silos de Trêve » (ALN-162).

### 5.4 Routes hors d'échelle
Ces routes relient des lieux que la géographie sépare de plusieurs milliers de kilomètres.

| ID | Route | Tracé | Problème | Solution |
|---|---|---|---|---|
| LT-21 | RT_061 Ts'idar-‖Sek ↔ K'elis-‖ara | 4 200 km, 216 jours, par terre | route « pastorale » d'été | remplacer K'elis-‖ara par un col de halekh oriental : Hlelak-!uri (2 900 m) ou Kraloth-!enu (2 700 m) (ALN-152) |
| LT-22 | RT_020 Kù-kèdà yì Mù-Kíri ↔ Ts'idar-ré | 5 080 km, 189 jours, depuis l'Atlantique | « cabotage + cols » | origine → Kù-békà (Tùmázì) : 1 370 km, 50 jours (RV-04, table G, ALN-163) |
| LT-23 | RT_001 Kù-békà ↔ Kù-téka | 2 440 km, 84 jours | caravane P3 entre les deux lacs | garder : grande caravane trans-forestière (sel, poisson, bois) ; annoter la durée (ALN-165) |
| LT-24 | RT_029 Piémonts du Mù-dárhòbì ↔ Kù-békà | 2 330 km, 81 jours ; « canaux inter-lacs » | aucun canal possible entre deux bassins distants de 2 000 km | origine → piémonts des collines Kù-kɨ́bò (basalte de Ku-Bángá) : quelques dizaines de km de portage, puis le lac (ALN-166) |
| LT-25 | RT_070 Lisières Ba-lóngó ↔ Q'eša-Kɨ́bò | 1 850 km, 65 jours | « pistes de contrebandiers (nuit) » | origine → lisières de la rive S du Tùmázì (FOR_S) (ALN-167) |
| LT-26 | RT_053 Ṣarīq ↔ ‖Ethak-Kél | 2 500 km, 87 jours | caravane lourde annuelle | garder (axe trans-sumdanien du §VII.5) ; annoter |
| LT-27 | RT_024 !Tama-\|'Ara ↔ Dimlāš | 3 070 km, 105 jours | voie rituelle | garder comme pèlerinage au long cours ; annoter |
| LT-28 | RT_021, RT_073 \|'Urum-‖Sek ↔ Abnaqil / Abnīqa | 2 190-2 220 km, ~75 jours | col + vallée | cohérent : crête → vallée de l'Abnuḥīl → delta |
| LT-29 | RT_071 Šālim ↔ Abnīqa | révisé : 264 km, 5,5 jours de descente du bras d'Abnīqa (RV-07) | « drainage administratif après crues » | cohérent |
| LT-30 | RT_030 Qabṣūr-Qibṣ ↔ Tanāḥil | 2 750 km de remontée, 58 jours | « remontée saisonnière » | cohérent avec §2.2 |

### 5.5 Durées canoniques
- **Portage NO** : 291 km et 14 jours de Khloreth-klam à Kralekh-Aktrik (RT_027), contre « 3 jours » au Géosystème. La valeur de 8 à 10 jours d'ALN-033 est trop courte d'un tiers : le tracé franchit les contreforts côtiers (point haut ~1 230 m). **Action** : « portage NO : 12 à 15 jours » (ALN-171).
- **Caravanes Halakhel E → mer Rouge** (ALN-173) : « 8 jours » au Géosystème. La carte mesure 370 km au plus court, soit 12 à 13 jours à 30 km par jour. Les 8 jours supposent ~45 km par jour (méhari) : cohérent pour une caravane légère.
- **Navigation intérieure** : traverser l'Halakhel d'ouest en est prend 44 à 52 jours de cabotage (RT_002, 017, 039, 041 ; 3 300 à 3 800 km).

### 5.6 Routes cohérentes
Les autres routes ne présentent pas d'écart : trafic de la mer Halakhel, réseau du delta d'Abnīqa, routes atlantiques, réseau des cols du SE, façade de la mer Rouge, routes de halekh. Leurs mesures sont dans les tables D et E.

---

## 6. Décisions de l'auteur

Les quatre points ouverts sont tranchés (§2.5, RV-01 à RV-04). Il reste deux points :
- la forge des noms des trois trouées principales (agent du corpus, `forge-ling`) ;
- la correction des fiches LIEUX et ROUTES selon `ALIGNEMENT_CORPUS.md` §9.

---

## 7. Tables générées

Les tables suivantes sont produites par `outils/lieux_routes.py`. Elles ne doivent pas être éditées à la main.

<!-- GENERE:DEBUT (outils/lieux_routes.py — ne pas éditer à la main) -->

### A. Lieux : position et site

Positions [PROPOSITION] en [longitude, latitude]. « Écart » = distance entre la cible raisonnée et la cellule retenue.

| ID | Nom | Type | Façade | Position | Altitude (m) | Dénivelé 10 km (m) | Milieu du site | Milieux à 25 km (%) |
|---|---|---|---|---|---|---|---|---|
| `LUR_KHLORETH-KLAM_NO` | Khloreth-klam | LUR | ATL_NO | [-9.568, 30.099] | 60 | 160 | fourre_cotier_sec | fourre_cotier_sec 55, océan 40, hors Beliet 5 |
| `LUR_STALOMAR-KOT_NO` | Stalomar-Kot | LUR | ATL_NO | [-10.03, 29.296] | 366 | 816 | littoral_rocheux | océan 32, fourre_cotier_sec 24, herbage_arbore 16, hors Beliet 15 |
| `LUR_STAKHR-DUREK_NO` | Stakhr-Durek | LUR | ATL_NO | [-8.548, 29.004] | 539 | 449 | steppe_piemont | steppe_piemont 90, herbage_arbore 6 |
| `LUR_HLORAN-RIR_NO` | Hloran-rir | LUR | ATL_NO | [-8.054, 29.601] | 529 | 481 | steppe_piemont | steppe_piemont 99 |
| `ZRS_FALAMI_SKREN_PERIPH_NO` | Oase-Skren | ZRS | ATL_NO | [-8.596, 29.393] | 802 | 485 | steppe_piemont | steppe_piemont 49, herbage_arbore 43, foret_montagne 9 |
| `LUR_KU-JALIMA-RIR_SO` | Ku-jálima-rir | LUR | ATL_SO | [-4.947, 5.206] | 9 | 69 | foret_maree | foret_tropicale_humide 48, océan 39, foret_maree 13 |
| `LUR_JALI-FE_SO` | Jáli-Fè | LUR | ATL_SO | [-3.704, 5.222] | -8 | 66 | foret_maree | océan 48, foret_tropicale_humide 37, foret_maree 15 |
| `LUR_ANSES-JALONDU_SO` | Anses-Jálondù | LUR | ATL_SO | [-1.282, 5.095] | 9 | 85 | foret_maree | foret_tropicale_humide 43, océan 42, foret_maree 15 |
| `LUR_JALI-LONGO_SO` | Jáli-lòngò | LUR | ATL_SO | [2.447, 6.364] | -5 | 99 | foret_tropicale_humide | foret_tropicale_humide 56, océan 44 |
| `LUR_GALU-KANDA_SO` | Gálu-kánda | LUR | ATL_SO | [1.443, 6.443] | 6 | 3 | foret_tropicale_humide | foret_tropicale_humide 93, foret_maree 7 |
| `ZRS_LISEKDI_SO` | Li-sèk-dì | ZRS | ATL_SO | [-1.25, 4.714] | 18 | 71 | foret_maree | océan 100 |
| `LUR_KOT-SKRAL_LARGE` | Kot-Skral | LUR | ATL_INS | [-24.994, 16.884] | 2 | 430 | ile_aride | océan 71, ile_aride 29 |
| `LUR_THRESKOL-STRAKH_LARGE` | Threskōl-Strakh | LUR | ATL_INS | [-22.906, 16.166] | 1 | 178 | ile_aride | océan 72, ile_aride 28 |
| `LUR_KRETH-NA-SEREK_N` | Khreth-na-Serek | LUR | HKL_N | [-1.983, 29.671] | 107 | 215 | littoral_rocheux | mer Halakhel 64, desert_pierreux 19, steppe_piemont 12 |
| `LUR_SEREKH-KHEM_N` | Serékh-khem | LUR | HKL_N | [-1.632, 30.772] | -27 | 133 | desert_pierreux | desert_pierreux 66, mer Halakhel 23, desert_sableux 9 |
| `AUX_KRALEKH-NER` | Kralekh-ner | AUX | — | [-1.728, 30.25] | sur l'eau (mer Halakhel) | 112 | mer Halakhel | mer Halakhel 100 |
| `LUR_AKHIDALET_NO` | Akhidalet | LUR | HKL_NO | [-7.72, 27.19] | 10 | 135 | plaine_alluviale | steppe_piemont 42, mer Halakhel 35, plaine_alluviale 21 |
| `LUR_KRALEKH-AKTRIK_NO` | Kralekh-Aktrik | LUR | HKL_NO | [-7.497, 28.206] | 32 | 139 | desert_pierreux | mer Halakhel 37, steppe_piemont 33, desert_pierreux 30 |
| `LUR_AKTRIK-KHEM_NO` | Aktrik-khem | LUR | HKL_NO | [-5.983, 28.262] | -2 | 116 | desert_pierreux | desert_pierreux 86, mer Halakhel 10 |
| `LUR_HLOM-KHETAL_NO` | Hlom-khetal | LUR | HKL_O | [-6.891, 27.488] | 64 | 211 | littoral_rocheux | mer Halakhel 56, steppe_piemont 41 |
| `LUR_IMEKH-STOM_NO` | Imekh-stom | LUR | HKL_SO | [0.344, 25.707] | 59 | 203 | littoral_rocheux | desert_pierreux 52, mer Halakhel 41 |
| `ZRS_AKHILETH_NO` | Akhileth | ZRS | HKL_SO | [0.599, 24.596] | 443 | 203 | steppe_piemont | steppe_piemont 98 |
| `LUR_CHERBEKH-KHEM_NO` | Cherbekh-khem | LUR | HKL_S | [2.623, 25.85] | 55 | 209 | littoral_rocheux | mer Halakhel 62, desert_pierreux 24, littoral_rocheux 7, steppe_piemont 5 |
| `LUR_TAWALMAZ_NE` | Tawālmaz | LUR | HKL_S | [14.064, 25.203] | 62 | 245 | littoral_rocheux | mer Halakhel 58, herbage_arbore 31, steppe_piemont 9 |
| `LUR_QABD-AR-GANUB_NE` | Qabḍ-ār-Ǧanūb | LUR | HKL_S | [22.574, 23.709] | 32 | 164 | littoral_rocheux | desert_pierreux 39, mer Halakhel 34, steppe_piemont 20, littoral_rocheux 6 |
| `LUR_QURASH-TANIQA_NE` | Qūrāš-Tanīqa | LUR | HKL_NE | [38.351, 10.555] | 1384 | 1097 | herbage_arbore | herbage_arbore 62, steppe_piemont 21, plaine_alluviale 13 |
| `LUR_QURASH-TANIHIL_NE` | Qūrāš-Taniḥīl-Ramšūr | LUR | HKL_NE | [38.446, 10.947] | 1413 | 828 | steppe_piemont | steppe_piemont 67, herbage_arbore 32 |
| `ZRS_SHALIM_NE` | Šālim | ZRS | HKL_NE | [30.717, 27.643] | 30 | 88 | plaine_alluviale | plaine_alluviale 63, desert_pierreux 37 |
| `LUR_SARIQ_NE` | Ṣarīq | LUR | HKL_NE | [29.395, 29.268] | 241 | 38 | depression_saline | desert_pierreux 49, depression_saline 35, steppe_piemont 16 |
| `ZRS_HAMAD-RAS_NE` | Ḥamaḍ-Rās | ZRS | HKL_NE | [28.168, 29.31] | 43 | 185 | littoral_rocheux | desert_pierreux 43, mer Halakhel 32, depression_saline 23 |
| `AUX_QURASH-SAFIH` | Qūrāš-Ṣafīḥ | AUX | — | [28.407, 28.445] | 2 | 131 | depression_saline | mer Halakhel 48, depression_saline 29, desert_pierreux 18 |
| `LUR_ABNAQIL_NE` | Abnaqil | LUR | HKL_E | [28.901, 27.615] | 27 | 62 | plaine_alluviale | plaine_alluviale 73, desert_pierreux 15, depression_saline 10 |
| `LUR_ABNIQA_NE` | Abnīqa | LUR | HKL_E | [28.359, 27.657] | 12 | 72 | plaine_alluviale | mer Halakhel 47, plaine_alluviale 30, depression_saline 20 |
| `LUR_TANAQIL_NE` | Tanāqil | LUR | HKL_E | [28.423, 27.375] | -5 | 110 | depression_saline | mer Halakhel 55, plaine_alluviale 23, depression_saline 22 |
| `LUR_QABSUR-QIBS_E` | Qabṣūr-Qibṣ | LUR | HKL_E | [28.343, 26.75] | 0 | 118 | depression_saline | mer Halakhel 61, depression_saline 31 |
| `LUR_HAWQIL_NE` | Ḥawqil | LUR | HKL_E | [26.893, 25.333] | 6 | 141 | depression_saline | mer Halakhel 53, depression_saline 22, plaine_alluviale 11, steppe_piemont 9 |
| `LUR_TANAHIL_NE` | Tanāḥil | LUR | HKL_E | [32.55, 15.614] | 378 | 29 | plaine_alluviale | desert_pierreux 54, plaine_alluviale 46 |
| `LUR_SHAFAQ-MIRQ_NE` | Šafāq-Mirq | LUR | MED_NE | [31.291, 31.481] | 0 | 12 | plaine_alluviale | plaine_alluviale 54, océan 45 |
| `LUR_TANQUISH_NE` | Ṭanquish | LUR | MED_NE | [29.809, 31.073] | 0 | 49 | plaine_alluviale | océan 42, plaine_alluviale 32, fourre_cotier_sec 26 |
| `AUX_MEDITERRANEE_NE` | Méditerranée NE (façade) | AUX | — | [31.004, 32.293] | sur l'eau (océan) | 540 | océan | océan 100 |
| `LUR_TNAYA-HAEM_SE` | T'naya-Ḥaem | LUR | ROU_SE | [42.892, 11.744] | -15 | 994 | littoral_rocheux | steppe_piemont 55, océan 37, littoral_rocheux 7 |
| `LUR_KURE-KESUN_SE` | K'uré-K’ésun | LUR | ROU_SE | [40.135, 15.014] | 62 | 199 | littoral_rocheux | cote_desertique 31, desert_pierreux 29, recif_corallien 27, hors Beliet 9 |
| `LUR_KURE-TAWA_SE` | K'uré-tawa | LUR | ROU_SE | [39.45, 15.598] | 368 | 666 | littoral_rocheux | steppe_piemont 38, recif_corallien 30, océan 15, littoral_rocheux 10 |
| `LUR_KUTEKA_SO` | Kù-téka | LUR | MOP_SO | [5.045, 9.504] | 804 | 60 | zone_humide_lacustre | eaux_lacustres 43, zone_humide_lacustre 39, herbage_arbore 14 |
| `LUR_KUNGUMI_SO` | Ku-Ngúmi | LUR | MOP_SO | [4.583, 9.048] | 671 | 67 | foret_tropicale_humide | foret_tropicale_humide 83, herbage_arbore 17 |
| `LUR_KUBELAA_SO` | Kù-Bèláà | LUR | MOP_SO | [6.272, 4.349] | -6 | 10 | foret_maree | foret_tropicale_humide 46, foret_maree 34, océan 19 |
| `LUR_MAZI-DUM_SO` | Mázì-Dúm | LUR | MOP_SO | [6.846, 4.619] | 1 | 11 | foret_maree | foret_tropicale_humide 53, foret_maree 42 |
| `ZRS_KUSALADI_SO` | Ku-sáladì | ZRS | MOP_SO | [6.113, 9.394] | 807 | 75 | zone_humide_lacustre | eaux_lacustres 47, zone_humide_lacustre 31, foret_tropicale_humide 21 |
| `AUX_LISIERES_BALONGO` | Lisières Ba-lóngó | AUX | — | [6.288, 8.828] | 512 | 281 | foret_tropicale_humide | herbage_arbore 78, foret_tropicale_humide 19 |
| `AUX_PIEMONTS_MUDARHOBI` | Piémonts du Mù-dárhòbì | AUX | — | [6.607, 8.497] | 394 | 199 | foret_berge | herbage_arbore 49, foret_tropicale_humide 35, foret_berge 8, zone_humide_lacustre 8 |
| `AUX_DLT_MOPAMA` | Estuaire Mopámà | AUX | — | [1.22, 6.047] | -3 | 56 | foret_maree | océan 46, foret_maree 27, foret_tropicale_humide 27 |
| `ZRS_KUUMANA_SO` | Ku-ùmanà | ZRS | FOR_SO | [2.702, 7.408] | 320 | 122 | foret_tropicale_humide | foret_tropicale_humide 97 |
| `ZRS_SAKUMADI_FORS` | Sa-kúmadì | ZRS | FOR_S | [24.805, 6.205] | 976 | 67 | foret_tropicale_humide | foret_tropicale_humide 98 |
| `ZRS_KUPEPANA_FORS` | Ku-pèpanà | ZRS | FOR_S | [23.992, 5.904] | 939 | 78 | foret_tropicale_humide | foret_tropicale_humide 100 |
| `LUR_KUBEKA_SC` | Kù-békà | LUR | TUM_SC | [24.773, 8.717] | sur l'eau (lac) | 622 | eaux_lacustres | foret_tropicale_humide 52, eaux_lacustres 47 |
| `LUR_KUPILA-MUSUKU_SC` | Ku-Pɨla-Mù-Sùkú | LUR | TUM_SC | [23.196, 6.839] | 951 | 498 | herbage_arbore | herbage_arbore 67, eaux_lacustres 30 |
| `LUR_KUKIBO_QESHA_SC` | Q'eša-Kɨ́bò | LUR | TUM_SC | [21.905, 6.902] | 1219 | 166 | herbage_arbore | herbage_arbore 51, foret_montagne 46 |
| `ZRS_KU-PILA-DI_SC` | Ku-Pɨla-dì | ZRS | TUM_SC | [23.403, 7.202] | sur l'eau (lac) | 524 | eaux_lacustres | eaux_lacustres 74, herbage_arbore 26 |
| `ZRS_KU-SUKU-NA_SC` | Ku-Sùkú-nà | ZRS | TUM_SC | [24.088, 6.949] | sur l'eau (lac) | 502 | eaux_lacustres | eaux_lacustres 76, herbage_arbore 14, foret_tropicale_humide 10 |
| `ZRS_KU-LEMBE_SC` | Ku-Lémbè | ZRS | TUM_SC | [26.255, 8.308] | sur l'eau (lac) | 406 | eaux_lacustres | foret_tropicale_humide 51, eaux_lacustres 49 |
| `ZRS_KU-ZABA_SC` | Kù-Zàbà | ZRS | TUM_SC | [25.331, 8.371] | sur l'eau (lac) | 168 | eaux_lacustres | eaux_lacustres 85, foret_tropicale_humide 15 |
| `ZRS_MI-TONO_SC` | Mi-Tónò | ZRS | TUM_SC | [25.65, 7.013] | sur l'eau (lac) | 197 | eaux_lacustres | eaux_lacustres 90, foret_tropicale_humide 6 |
| `ZRS_KU-PELE-SO_SC` | Ku-Pélé-sò | ZRS | TUM_SC | [23.801, 8.843] | 1071 | 656 | herbage_arbore | herbage_arbore 50, eaux_lacustres 29, foret_tropicale_humide 19 |
| `ZRS_KU-BANGA_SC` | Ku-Bángá | ZRS | TUM_SC | [22.463, 7.329] | 1028 | 461 | herbage_arbore | herbage_arbore 77, eaux_lacustres 17 |
| `ZRS_KU-NOMA_SC` | Ku-Nómà | ZRS | TUM_SC | [26.701, 8.292] | 897 | 354 | foret_tropicale_humide | foret_tropicale_humide 70, eaux_lacustres 30 |
| `ZRS_KUKANADI_SC` | Ku-kànadì | ZRS | TUM_SC | [22.686, 7.992] | 1011 | 590 | herbage_arbore | herbage_arbore 52, eaux_lacustres 47 |
| `LUR_BANNAKTI_NO` | Bannaktì | LUR | URU_NO | [-9.106, 22.301] | 1766 | 1459 | steppe_piemont | steppe_piemont 89, prairie_altitude 6 |
| `LUR_TAMAR-KHU_CENTRE` | !Tamar-\|\|Khu | LUR | URU_SO | [4.407, 17.796] | 1596 | 676 | foret_montagne | foret_montagne 98 |
| `LUR_ZAGAKH-TIR_NE` | Zagakh-TƗr | LUR | URU_C | [23.658, 22.242] | 1198 | 39 | zone_humide_lacustre | zone_humide_lacustre 35, herbage_arbore 30, eaux_lacustres 20, plaine_alluviale 14 |
| `LUR_URUM-SAMEL_CENTRE` | \|'Urum-!Samel | LUR | URU_C | [17.905, 20.102] | 3708 | 2443 | prairie_altitude | zone_periglaciaire 53, prairie_altitude 40, glacier 5 |
| `LUR_UKH-SEK_CENTRE` | \|'Ukh-\|\|Sék | LUR | URU_C | [37.857, 10.649] | 3442 | 1555 | prairie_altitude | foret_montagne 39, prairie_altitude 33, herbage_arbore 27 |
| `LUR_ETHAK-KEL_CENTRE` | \|\|Ethak-Kél-Ts'idar | LUR | URU_C | [34.845, 8.906] | 2453 | 825 | foret_montagne | foret_montagne 100 |
| `LUR_TSIDAR-SEK_CENTRE` | Ts'idar-‖Sek | LUR | URU_C | [-2.094, 22.933] | 2842 | 803 | prairie_altitude | prairie_altitude 68, desert_pierreux 29 |
| `LUR_GITES-TSIDAR_SE` | Gîtes-Ts'idar | LUR | URU_SE | [34.351, 8.623] | 1382 | 588 | foret_montagne | foret_tropicale_humide 55, foret_montagne 45 |
| `LUR_TSIDAR-RE_SE` | Ts'idar-ré | LUR | URU_SE | [35.307, 8.717] | 2272 | 633 | foret_montagne | foret_montagne 100 |
| `LUR_KUMAL-NAQRA_SE` | K'umal-Naqra | LUR | URU_SE | [39.004, 13.594] | 2223 | 302 | steppe_piemont | steppe_piemont 59, desert_pierreux 41 |
| `LUR_HAE-TSI-KURE_SE` | Hae Ts'i-K'uré | LUR | URU_SE | [30.351, 10.743] | 1886 | 615 | foret_montagne | foret_montagne 60, herbage_arbore 38 |
| `LUR_PI-KURE-NESHA_SE` | P'i-K'uré-Neša | LUR | URU_SE | [38.956, 15.245] | 2299 | 728 | desert_pierreux | steppe_piemont 57, desert_pierreux 43 |
| `LUR_HAE-PESHU_SE` | Hae-P'ešu | LUR | URU_SE | [39.052, 14.845] | 1662 | 228 | depression_saline | steppe_piemont 47, desert_pierreux 29, depression_saline 24 |
| `LUR_QIREL-TSIDAR_SE` | Q'irel-Ts'idar | LUR | PLT_SE | [35.052, 9.001] | 2395 | 438 | foret_montagne | foret_montagne 100 |
| `AUX_FOYERS-PURS` | Foyers-Purs | AUX | — | [38.701, 14.598] | 2008 | 463 | desert_pierreux | desert_pierreux 97 |
| `AUX_VOIE-DESNUEES` | Voie-Desnuées | AUX | — | [38.303, 12.398] | 2580 | 675 | steppe_piemont | steppe_piemont 96 |
| `AUX_VOIE-HAUTE` | Voie-Haute | AUX | — | [31.004, 10.602] | 1873 | 798 | foret_montagne | foret_montagne 87, herbage_arbore 9 |
| `AUX_HAE-KUMEL` | Hae K'umel | AUX | — | [38.797, 13.299] | 2516 | 688 | steppe_piemont | steppe_piemont 71, desert_pierreux 23 |
| `AUX_KUKEDA-MUKIRI` | Kù-kèdà yì Mù-Kíri | AUX | — | [-4.947, 5.206] | 9 | 69 | foret_maree | foret_tropicale_humide 48, océan 39, foret_maree 13 |
| `AUX_FORGES-DES-COQUES` | Forges-des-Coques (Mù-Kíri) | AUX | — | [-4.947, 5.206] | 9 | 69 | foret_maree | foret_tropicale_humide 48, océan 39, foret_maree 13 |
| `AUX_KISRALOM` | Kisralom | AUX | — | [-7.497, 28.206] | 32 | 139 | desert_pierreux | mer Halakhel 37, steppe_piemont 33, desert_pierreux 30 |
| `AUX_CERCLE-SANS-JURON` | Cercle-Sans-Juron | AUX | — | [-7.497, 28.206] | 32 | 139 | desert_pierreux | mer Halakhel 37, steppe_piemont 33, desert_pierreux 30 |
| `AUX_DIMLAS` | Dimlāš | AUX | — | [28.901, 27.615] | 27 | 62 | plaine_alluviale | plaine_alluviale 73, desert_pierreux 15, depression_saline 10 |
| `AUX_VOIE-PURE` | Voie-Pure-des-Vallées | AUX | — | [28.359, 27.657] | 12 | 72 | plaine_alluviale | mer Halakhel 47, plaine_alluviale 30, depression_saline 20 |
| `AUX_HAMUQAS` | Ḥamūqaš | AUX | — | [28.359, 27.657] | 12 | 72 | plaine_alluviale | mer Halakhel 47, plaine_alluviale 30, depression_saline 20 |
| `AUX_TAMA-ARA` | !Tama-\|'Ara | AUX | — | [4.407, 17.796] | 1596 | 676 | foret_montagne | foret_montagne 98 |
| `AUX_VOIE-COMPTABLE` | Voie-Comptable | AUX | — | [38.956, 15.245] | 2299 | 728 | desert_pierreux | steppe_piemont 57, desert_pierreux 43 |
| `AUX_PORTS-TNAYEL` | Ports T'nayel SE | AUX | — | [42.892, 11.744] | -15 | 994 | littoral_rocheux | steppe_piemont 55, océan 37, littoral_rocheux 7 |
| `AUX_SANUBE-MUSUKU` | Sa-nùbè yì Mù-Sùkú | AUX | — | [24.088, 6.949] | sur l'eau (lac) | 502 | eaux_lacustres | eaux_lacustres 76, herbage_arbore 14, foret_tropicale_humide 10 |
| `AUX_PORTS-EXTERNES-NO` | Ports externes NO | AUX | — | [-21.998, 34.502] | sur l'eau (océan) | 441 | océan | océan 100 |

### B. Lieux : climat, eaux, cols

| ID | Pluie (mm/an) | T annuelle (°C) | Hiver Tw / nuit Tn (°C) | Faciès \|'Arin | Distance mer Halakhel / océan / lac / cours d'eau (km) | Fleuve nommé à < 30 km ; débit max à 15 km (m³/s) | Col le plus proche |
|---|---|---|---|---|---|---|---|
| `LUR_KHLORETH-KLAM_NO` | 1108 | 19.0 | 9.0 / 1.0 | hiver pluvieux tempéré | 283 / 2 / 2490 / 26 | — ; 22 | Hlenik-k'eso (2000 m) à 831 km |
| `LUR_STALOMAR-KOT_NO` | 1046 | 17.5 | 7.7 / -0.3 | hiver pluvieux tempéré | 267 / 2 / 2463 / 102 | — ; 5 | Hlenik-k'eso (2000 m) à 749 km |
| `LUR_STAKHR-DUREK_NO` | 435 | 16.6 | 6.9 / -1.1 | Hiver Gris | 131 / 138 / 2360 / 88 | — ; 29 | Hlenik-k'eso (2000 m) à 705 km |
| `LUR_HLORAN-RIR_NO` | 336 | 16.4 | 6.5 / -2.3 | Hiver Gris | 153 / 154 / 2373 / 147 | — ; 9 | Hlenik-k'eso (2000 m) à 774 km |
| `ZRS_FALAMI_SKREN_PERIPH_NO` | 569 | 14.9 | 5.0 / -3.0 | hiver pluvieux tempéré | 163 / 113 / 2389 / 115 | — ; 5 | Hlenik-k'eso (2000 m) à 748 km |
| `LUR_KU-JALIMA-RIR_SO` | 2630 | 27.4 | 23.1 / 15.1 | hors \|'Arin | 2397 / 2 / 1194 / 2 | — ; 3190 | Lémakhɨ (2200 m) à 1624 km |
| `LUR_JALI-FE_SO` | 2790 | 27.5 | 23.1 / 15.1 | hors \|'Arin | 2364 / 4 / 1068 / 0 | — ; 2325 | Lémakhɨ (2200 m) à 1519 km |
| `LUR_ANSES-JALONDU_SO` | 2778 | 27.4 | 23.1 / 15.1 | hors \|'Arin | 2340 / 4 / 841 / 35 | — ; 39 | Ku-Pámà-Tɨra-te (2000 m) à 1337 km |
| `LUR_JALI-LONGO_SO` | 2447 | 27.5 | 22.9 / 14.9 | hors \|'Arin | 2195 / 2 / 431 / 46 | — ; 86 | Ku-Pámà-Tɨra-te (2000 m) à 950 km |
| `LUR_GALU-KANDA_SO` | 2143 | 27.5 | 22.8 / 14.8 | hors \|'Arin | 2178 / 33 / 507 / 0 | GEO_FLV_EMISSAIRE_MOPAMA ; 83 | Ku-Pámà-Tɨra-te (2000 m) à 1017 km |
| `ZRS_LISEKDI_SO` | 2563 | 27.4 | 23.1 / 15.1 | hors \|'Arin | 2383 / 2 / 862 / 48 | — ; 0 | Ku-Pámà-Tɨra-te (2000 m) à 1363 km |
| `LUR_KOT-SKRAL_LARGE` | 361 | 25.3 | 18.3 / 9.8 | hors \|'Arin | 2164 / 2 / 3285 / 906 | — ; 0 | Ku-Mázì-Klek-te (1900 m) à 1190 km |
| `LUR_THRESKOL-STRAKH_LARGE` | 356 | 25.6 | 18.8 / 10.2 | hors \|'Arin | 2038 / 2 / 3062 / 674 | — ; 0 | Ku-Mázì-Klek-te (1900 m) à 1020 km |
| `LUR_KRETH-NA-SEREK_N` | 236 | 18.9 | 9.0 / -1.2 | Hiver de Vapeur | 2 / 613 / 2094 / 472 | — ; 0 | Halek-t'ama (1900 m) à 676 km |
| `LUR_SEREKH-KHEM_N` | 124 | 19.1 | 8.9 / -2.8 | Hiver de Vapeur | 3 / 486 / 2172 / 449 | — ; 0 | Halek-t'ama (1900 m) à 789 km |
| `AUX_KRALEKH-NER` | 204 | 19.3 | 9.3 / -1.3 | Hiver de Vapeur | 0 / 546 / 2133 / 505 | — ; 0 | Halek-t'ama (1900 m) à 734 km |
| `LUR_AKHIDALET_NO` | 287 | 20.6 | 11.3 / 1.8 | Hiver de Vapeur | 4 / 325 / 2186 / 2 | Ehukhtal ; 1 | Hlenik-k'eso (2000 m) à 513 km |
| `LUR_KRALEKH-AKTRIK_NO` | 251 | 20.0 | 10.5 / 0.5 | Hiver de Vapeur | 2 / 274 / 2246 / 109 | — ; 3 | Hlenik-k'eso (2000 m) à 628 km |
| `LUR_AKTRIK-KHEM_NO` | 197 | 20.2 | 10.6 / -0.1 | Hiver de Vapeur | 3 / 399 / 2166 / 184 | — ; 0 | Tkrilan-ɨkh (2800 m) à 601 km |
| `LUR_HLOM-KHETAL_NO` | 317 | 20.1 | 10.8 / 1.6 | Hiver de Vapeur | 2 / 371 / 2161 / 62 | — ; 1 | Tkrilan-ɨkh (2800 m) à 541 km |
| `LUR_IMEKH-STOM_NO` | 201 | 21.0 | 12.0 / 1.3 | Hiver de Vapeur | 2 / 1104 / 1669 / 62 | — ; 0 | Halek-t'ama (1900 m) à 228 km |
| `ZRS_AKHILETH_NO` | 231 | 19.2 | 10.4 / 0.2 | hors \|'Arin | 77 / 1194 / 1559 / 60 | — ; 1 | Halek-t'ama (1900 m) à 134 km |
| `LUR_CHERBEKH-KHEM_NO` | 226 | 20.9 | 11.9 / 1.6 | Hiver de Vapeur | 2 / 1160 / 1616 / 120 | — ; 0 | Ktamar-khɨ (3000 m) à 302 km |
| `LUR_TAWALMAZ_NE` | 651 | 21.2 | 12.3 / 4.3 | Hiver de Vapeur | 2 / 719 / 832 / 141 | — ; 1 | Ṣabūl-tɨkh (2900 m) à 544 km |
| `LUR_QABD-AR-GANUB_NE` | 247 | 22.0 | 13.5 / 3.5 | Hiver de Vapeur | 2 / 817 / 167 / 187 | — ; 0 | Qaṣūl-tɨra (2700 m) à 620 km |
| `LUR_QURASH-TANIQA_NE` | 573 | 19.2 | 13.6 / 5.6 | hors \|'Arin | 2056 / 471 / 1236 / 12 | Tira-ñara / Tanāḥil ; 46 | Nrelat-q'urm (2200 m) à 156 km |
| `LUR_QURASH-TANIHIL_NE` | 445 | 19.0 | 13.4 / 5.4 | hors \|'Arin | 2024 / 453 / 1257 / 3 | Tira-ñara / Tanāḥil ; 27 | Nrelat-q'urm (2200 m) à 124 km |
| `ZRS_SHALIM_NE` | 138 | 20.3 | 10.9 / -0.6 | Hiver Jaune | 185 / 237 / 907 / 2 | Abnīqa ; 4560 | Ṭanīkhūr (3200 m) à 1455 km |
| `LUR_SARIQ_NE` | 222 | 18.3 | 8.5 / -1.9 | Hiver Jaune | 79 / 173 / 944 / 153 | — ; 0 | Qaṣūl-tɨra (2700 m) à 1507 km |
| `ZRS_HAMAD-RAS_NE` | 175 | 19.5 | 9.7 / -1.3 | Hiver de Vapeur | 2 / 187 / 886 / 147 | — ; 0 | Qaṣūl-tɨra (2700 m) à 1437 km |
| `AUX_QURASH-SAFIH` | 151 | 20.1 | 10.5 / -0.8 | Hiver de Vapeur | 2 / 272 / 822 / 49 | — ; 0 | Qaṣūl-tɨra (2700 m) à 1375 km |
| `LUR_ABNAQIL_NE` | 162 | 20.3 | 10.9 / -0.3 | Hiver de Vapeur | 23 / 360 / 781 / 2 | Abnīqa ; 4564 | Ṭanīkhūr (3200 m) à 1337 km |
| `LUR_ABNIQA_NE` | 146 | 20.4 | 11.0 / -0.4 | Hiver de Vapeur | 4 / 361 / 752 / 2 | Abnīqa ; 0 | Qaṣūl-tɨra (2700 m) à 1305 km |
| `LUR_TANAQIL_NE` | 151 | 20.6 | 11.2 / -0.1 | Hiver de Vapeur | 2 / 392 / 733 / 16 | Abnīqa ; 0 | Qaṣūl-tɨra (2700 m) à 1286 km |
| `LUR_QABSUR-QIBS_E` | 158 | 20.9 | 11.6 / 0.4 | Hiver de Vapeur | 2 / 464 / 678 / 70 | — ; 0 | Ṭanīkhūr (3200 m) à 1227 km |
| `LUR_HAWQIL_NE` | 234 | 21.5 | 12.6 / 2.4 | Hiver de Vapeur | 2 / 660 / 471 / 22 | \|Na-khuwel / Ḥawqal ; 5 | Ṭanīkhūr (3200 m) à 1014 km |
| `LUR_TANAHIL_NE` | 86 | 23.6 | 16.9 / 4.9 | hors \|'Arin | 1224 / 632 / 1019 / 0 | Tira-ñara / Tanāḥil ; 4138 | P'etsul-!ama (2600 m) à 579 km |
| `LUR_SHAFAQ-MIRQ_NE` | 306 | 18.7 | 8.4 / -0.8 | hiver pluvieux tempéré | 362 / 4 / 1225 / 36 | — ; 1 | Qaṣūl-tɨra (2700 m) à 1812 km |
| `LUR_TANQUISH_NE` | 374 | 18.9 | 8.7 / 0.4 | hiver pluvieux tempéré | 239 / 4 / 1116 / 66 | — ; 2 | Qaṣūl-tɨra (2700 m) à 1688 km |
| `AUX_MEDITERRANEE_NE` | 272 | 18.4 | 7.9 / -1.8 | hors \|'Arin | 410 / 0 / 1275 / 110 | — ; 0 | Qaṣūl-tɨra (2700 m) à 1864 km |
| `LUR_TNAYA-HAEM_SE` | 365 | 27.5 | 21.7 / 13.2 | hors \|'Arin | 2266 / 3 / 1743 / 36 | — ; 1 | ʿUbayl-t'iq (2000 m) à 488 km |
| `LUR_KURE-KESUN_SE` | 118 | 25.8 | 19.2 / 7.4 | hors \|'Arin | 1773 / 2 / 1589 / 222 | — ; 0 | ʿUbayl-t'iq (2000 m) à 106 km |
| `LUR_KURE-TAWA_SE` | 117 | 23.7 | 17.0 / 5.2 | hors \|'Arin | 1670 / 2 / 1558 / 229 | — ; 0 | Ḥazīr-k'ama (2100 m) à 82 km |
| `LUR_KUTEKA_SO` | 1372 | 22.7 | 17.3 / 9.3 | hors \|'Arin | 1884 / 362 / 2 / 6 | GEO_FLV_EMISSAIRE_MOPAMA ; 17 | Ku-Pámà-Tɨra-te (2000 m) à 500 km |
| `LUR_KUNGUMI_SO` | 1613 | 23.5 | 18.2 / 10.2 | hors \|'Arin | 1925 / 297 / 56 / 2 | GEO_FLV_EMISSAIRE_MOPAMA ; 51 | Ku-Pámà-Tɨra-te (2000 m) à 571 km |
| `LUR_KUBELAA_SO` | 1995 | 27.5 | 23.3 / 15.3 | hors \|'Arin | 2455 / 4 / 542 / 11 | — ; 82 | Ku-Pámà-Tɨra-te (2000 m) à 979 km |
| `LUR_MAZI-DUM_SO` | 2200 | 27.5 | 23.3 / 15.3 | hors \|'Arin | 2407 / 6 / 525 / 9 | — ; 353 | Ku-Pámà-Tɨra-te (2000 m) à 940 km |
| `ZRS_KUSALADI_SO` | 1596 | 22.7 | 17.3 / 9.3 | hors \|'Arin | 1909 / 395 / 4 / 89 | — ; 7 | Ku-Pámà-Tɨra-te (2000 m) à 449 km |
| `AUX_LISIERES_BALONGO` | 1417 | 24.4 | 19.2 / 11.2 | hors \|'Arin | 1964 / 352 / 60 / 26 | — ; 17 | Ku-Pámà-Tɨra-te (2000 m) à 499 km |
| `AUX_PIEMONTS_MUDARHOBI` | 1379 | 25.1 | 20.0 / 12.0 | hors \|'Arin | 1987 / 342 / 110 / 2 | — ; 318 | Ku-Pámà-Tɨra-te (2000 m) à 523 km |
| `AUX_DLT_MOPAMA` | 2217 | 27.5 | 22.9 / 14.9 | hors \|'Arin | 2223 / 2 / 554 / 13 | GEO_FLV_EMISSAIRE_MOPAMA ; 76 | Ku-Pámà-Tɨra-te (2000 m) à 1066 km |
| `ZRS_KUUMANA_SO` | 1840 | 25.6 | 20.7 / 12.7 | hors \|'Arin | 2078 / 118 / 330 / 16 | GEO_FLV_EMISSAIRE_MOPAMA ; 12 | Ku-Pámà-Tɨra-te (2000 m) à 844 km |
| `ZRS_SAKUMADI_FORS` | 2187 | 21.6 | 17.0 / 9.0 | hors \|'Arin | 1934 / 1679 / 46 / 34 | — ; 39 | Šaqra-t'em (2400 m) à 695 km |
| `ZRS_KUPEPANA_FORS` | 2442 | 21.9 | 17.3 / 9.3 | hors \|'Arin | 1963 / 1586 / 80 / 30 | — ; 68 | Šaqra-t'em (2400 m) à 730 km |
| `LUR_KUBEKA_SC` | 1730 | 27.5 | 22.3 / 14.3 | hors \|'Arin | 1646 / 1745 / 0 / 105 | — ; 7 | Šaqra-t'em (2400 m) à 417 km |
| `LUR_KUPILA-MUSUKU_SC` | 1192 | 21.8 | 17.1 / 9.1 | hors \|'Arin | 1854 / 1522 / 2 / 134 | — ; 81 | Šaqra-t'em (2400 m) à 640 km |
| `LUR_KUKIBO_QESHA_SC` | 1349 | 20.2 | 15.4 / 7.4 | hors \|'Arin | 1852 / 1387 / 82 / 57 | — ; 36 | Šaqra-t'em (2400 m) à 680 km |
| `ZRS_KU-PILA-DI_SC` | 1136 | 27.5 | 22.7 / 14.7 | hors \|'Arin | 1813 / 1554 / 0 / 134 | — ; 4 | Šaqra-t'em (2400 m) à 596 km |
| `ZRS_KU-SUKU-NA_SC` | 1292 | 27.5 | 22.7 / 14.7 | hors \|'Arin | 1844 / 1619 / 0 / 128 | — ; 3 | Šaqra-t'em (2400 m) à 614 km |
| `ZRS_KU-LEMBE_SC` | 2205 | 27.5 | 22.4 / 14.4 | hors \|'Arin | 1715 / 1666 / 0 / 58 | — ; 9 | Kurel-ahek (2150 m) à 476 km |
| `ZRS_KU-ZABA_SC` | 1993 | 27.5 | 22.4 / 14.4 | hors \|'Arin | 1692 / 1752 / 0 / 88 | — ; 3 | Kurel-ahek (2150 m) à 463 km |
| `ZRS_MI-TONO_SC` | 1449 | 27.5 | 22.7 / 14.7 | hors \|'Arin | 1852 / 1788 / 0 / 108 | — ; 1 | Kurel-ahek (2150 m) à 613 km |
| `ZRS_KU-PELE-SO_SC` | 1461 | 21.1 | 15.9 / 7.9 | hors \|'Arin | 1624 / 1649 / 4 / 136 | — ; 20 | Šaqra-t'em (2400 m) à 410 km |
| `ZRS_KU-BANGA_SC` | 1009 | 21.3 | 16.5 / 8.5 | hors \|'Arin | 1799 / 1459 / 4 / 39 | — ; 6 | Šaqra-t'em (2400 m) à 612 km |
| `ZRS_KU-NOMA_SC` | 2253 | 22.1 | 17.1 / 9.1 | hors \|'Arin | 1726 / 1624 / 4 / 76 | — ; 9 | P'etsul-!ama (2600 m) à 475 km |
| `ZRS_KUKANADI_SC` | 977 | 21.4 | 16.4 / 8.4 | hors \|'Arin | 1722 / 1505 / 4 / 61 | — ; 4 | Šaqra-t'em (2400 m) à 535 km |
| `LUR_BANNAKTI_NO` | 217 | 12.3 | 4.1 / -6.4 | Hiver Jaune | 558 / 633 / 1957 / 365 | — ; 0 | Hlenik-k'eso (2000 m) à 56 km |
| `LUR_TAMAR-KHU_CENTRE` | 1014 | 15.3 | 8.1 / 0.1 | Hiver Gris | 918 / 1227 / 772 / 100 | — ; 17 | Ku-Ténɨlkh-te (2300 m) à 51 km |
| `LUR_ZAGAKH-TIR_NE` | 708 | 15.7 | 7.5 / -0.5 | Hiver Gris | 90 / 1021 / 11 / 2 | \|Na-khuwel / Ḥawqal ; 6 | Qaṣūl-tɨra (2700 m) à 541 km |
| `LUR_URUM-SAMEL_CENTRE` | 123 | 1.6 | -6.1 / -17.8 | Hiver Blanc | 517 / 1176 / 369 / 211 | — ; 0 | Ṣabūl-tɨkh (2900 m) à 237 km |
| `LUR_UKH-SEK_CENTRE` | 711 | 6.8 | 1.2 / -6.8 | Hiver Gris | 2017 / 522 / 1187 / 60 | — ; 3 | Nrelat-q'urm (2200 m) à 133 km |
| `LUR_ETHAK-KEL_CENTRE` | 3095 | 12.8 | 7.6 / -0.4 | Hiver Gris | 2006 / 879 / 825 / 58 | — ; 19 | T'araq-ɨnkh (2400 m) à 10 km |
| `LUR_TSIDAR-SEK_CENTRE` | 76 | 5.5 | -2.8 / -14.8 | Hiver Blanc | 376 / 1087 / 1540 / 234 | — ; 0 | Hlelak-!uri (2900 m) à 3 km |
| `LUR_GITES-TSIDAR_SE` | 3841 | 19.2 | 14.1 / 6.1 | hors \|'Arin | 2004 / 939 / 767 / 49 | — ; 91 | T'araq-ɨnkh (2400 m) à 53 km |
| `LUR_TSIDAR-RE_SE` | 2526 | 13.9 | 8.7 / 0.7 | Hiver Gris | 2054 / 854 / 872 / 31 | — ; 16 | Q'usa-\|\|ema (2100 m) à 20 km |
| `LUR_KUMAL-NAQRA_SE` | 119 | 13.4 | 7.2 / -4.6 | Hiver Jaune | 1810 / 185 / 1415 / 35 | — ; 1 | Ṣamar-q'ut (2200 m) à 77 km |
| `LUR_HAE-TSI-KURE_SE` | 755 | 16.2 | 10.6 / 2.6 | hors \|'Arin | 1574 / 1132 / 475 / 84 | — ; 11 | P'etsul-!ama (2600 m) à 40 km |
| `LUR_PI-KURE-NESHA_SE` | 110 | 12.2 | 5.6 / -6.3 | Hiver Jaune | 1661 / 63 / 1495 / 170 | — ; 0 | Ḥazīr-k'ama (2100 m) à 23 km |
| `LUR_HAE-PESHU_SE` | 110 | 16.2 | 9.7 / -2.2 | Hiver Jaune | 1703 / 80 / 1482 / 135 | — ; 0 | ʿUbayl-t'iq (2000 m) à 54 km |
| `LUR_QIREL-TSIDAR_SE` | 2564 | 13.1 | 7.9 / -0.1 | Hiver Gris | 2010 / 857 / 849 / 43 | — ; 11 | T'araq-ɨnkh (2400 m) à 35 km |
| `AUX_FOYERS-PURS` | 86 | 14.3 | 7.8 / -4.2 | Hiver Jaune | 1698 / 126 / 1437 / 94 | — ; 0 | Ṣamar-q'ut (2200 m) à 66 km |
| `AUX_VOIE-DESNUEES` | 256 | 11.8 | 5.8 / -4.1 | Hiver Jaune | 1874 / 339 / 1294 / 11 | Buhlela ; 9 | Nrelat-q'urm (2200 m) à 83 km |
| `AUX_VOIE-HAUTE` | 1127 | 16.3 | 10.7 / 2.7 | hors \|'Arin | 1619 / 1078 / 516 / 75 | — ; 13 | P'etsul-!ama (2600 m) à 110 km |
| `AUX_HAE-KUMEL` | 124 | 11.8 | 5.6 / -6.1 | Hiver Jaune | 1823 / 224 / 1381 / 5 | Buhlela ; 10 | Ṣamar-q'ut (2200 m) à 91 km |
| `AUX_KUKEDA-MUKIRI` | 2630 | 27.4 | 23.1 / 15.1 | hors \|'Arin | 2397 / 2 / 1194 / 2 | — ; 3190 | Lémakhɨ (2200 m) à 1624 km |
| `AUX_FORGES-DES-COQUES` | 2630 | 27.4 | 23.1 / 15.1 | hors \|'Arin | 2397 / 2 / 1194 / 2 | — ; 3190 | Lémakhɨ (2200 m) à 1624 km |
| `AUX_KISRALOM` | 251 | 20.0 | 10.5 / 0.5 | Hiver de Vapeur | 2 / 274 / 2246 / 109 | — ; 3 | Hlenik-k'eso (2000 m) à 628 km |
| `AUX_CERCLE-SANS-JURON` | 251 | 20.0 | 10.5 / 0.5 | Hiver de Vapeur | 2 / 274 / 2246 / 109 | — ; 3 | Hlenik-k'eso (2000 m) à 628 km |
| `AUX_DIMLAS` | 162 | 20.3 | 10.9 / -0.3 | Hiver de Vapeur | 23 / 360 / 781 / 2 | Abnīqa ; 4564 | Ṭanīkhūr (3200 m) à 1337 km |
| `AUX_VOIE-PURE` | 146 | 20.4 | 11.0 / -0.4 | Hiver de Vapeur | 4 / 361 / 752 / 2 | Abnīqa ; 0 | Qaṣūl-tɨra (2700 m) à 1305 km |
| `AUX_HAMUQAS` | 146 | 20.4 | 11.0 / -0.4 | Hiver de Vapeur | 4 / 361 / 752 / 2 | Abnīqa ; 0 | Qaṣūl-tɨra (2700 m) à 1305 km |
| `AUX_TAMA-ARA` | 1014 | 15.3 | 8.1 / 0.1 | Hiver Gris | 918 / 1227 / 772 / 100 | — ; 17 | Ku-Ténɨlkh-te (2300 m) à 51 km |
| `AUX_VOIE-COMPTABLE` | 110 | 12.2 | 5.6 / -6.3 | Hiver Jaune | 1661 / 63 / 1495 / 170 | — ; 0 | Ḥazīr-k'ama (2100 m) à 23 km |
| `AUX_PORTS-TNAYEL` | 365 | 27.5 | 21.7 / 13.2 | hors \|'Arin | 2266 / 3 / 1743 / 36 | — ; 1 | ʿUbayl-t'iq (2000 m) à 488 km |
| `AUX_SANUBE-MUSUKU` | 1292 | 27.5 | 22.7 / 14.7 | hors \|'Arin | 1844 / 1619 / 0 / 128 | — ; 3 | Šaqra-t'em (2400 m) à 614 km |
| `AUX_PORTS-EXTERNES-NO` | 291 | 17.4 | 6.4 / -3.0 | hors \|'Arin | 1484 / 0 / 3477 / 1110 | — ; 0 | Ku-Mázì-Klek-te (1900 m) à 1735 km |

### C. Lieux : expositions calculées et écarts avec le corpus

| ID | Nom | Expositions physiques calculées | Écarts (biomes et expositions du corpus non soutenus par le site) |
|---|---|---|---|
| `LUR_KHLORETH-KLAM_NO` | Khloreth-klam | tempêtes et houle de rivage | aucun |
| `LUR_STALOMAR-KOT_NO` | Stalomar-Kot | tempêtes et houle de rivage | aucun |
| `LUR_STAKHR-DUREK_NO` | Stakhr-Durek | — | biome « desert_sableux » — milieux calculés : herbage_arbore, steppe_piemont<br>exposition « Ensablement des pistes » — non soutenue par le site (ensablement)<br>exposition « tempêtes de sable » — non soutenue par le site (tempêtes) |
| `LUR_HLORAN-RIR_NO` | Hloran-rir | — | biome « oasis » — milieux calculés : steppe_piemont |
| `ZRS_FALAMI_SKREN_PERIPH_NO` | Oase-Skren | — | biome « oasis » — milieux calculés : foret_montagne, herbage_arbore, steppe_piemont |
| `LUR_KU-JALIMA-RIR_SO` | Ku-jálima-rir | crues (lit majeur); tempêtes et houle de rivage | aucun |
| `LUR_JALI-FE_SO` | Jáli-Fè | crues (lit majeur); tempêtes et houle de rivage | exposition « Ensablement » — non soutenue par le site (ensablement) |
| `LUR_ANSES-JALONDU_SO` | Anses-Jálondù | tempêtes et houle de rivage | aucun |
| `LUR_JALI-LONGO_SO` | Jáli-lòngò | tempêtes et houle de rivage | aucun |
| `LUR_GALU-KANDA_SO` | Gálu-kánda | crues (lit majeur) | aucun |
| `ZRS_LISEKDI_SO` | Li-sèk-dì | tempêtes et houle de rivage | biome « ile_aride » — milieux calculés : foret_maree, océan |
| `LUR_KOT-SKRAL_LARGE` | Kot-Skral | tempêtes et houle de rivage | aucun |
| `LUR_THRESKOL-STRAKH_LARGE` | Threskōl-Strakh | tempêtes et houle de rivage | aucun |
| `LUR_KRETH-NA-SEREK_N` | Khreth-na-Serek | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_SEREKH-KHEM_N` | Serékh-khem | brouillards d'évaporation (Hiver de Vapeur); ensablement (sables à moins de 25 km); tempêtes et houle de rivage; aridité (< 150 mm) | aucun |
| `LUR_AKHIDALET_NO` | Akhidalet | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_KRALEKH-AKTRIK_NO` | Kralekh-Aktrik | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_AKTRIK-KHEM_NO` | Aktrik-khem | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_HLOM-KHETAL_NO` | Hlom-khetal | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_IMEKH-STOM_NO` | Imekh-stom | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | exposition « crues subites de l'Imikhrel » — non soutenue par le site (crues)<br>exposition « tempêtes O (saison après crues) » — non soutenue par le site (crues) |
| `ZRS_AKHILETH_NO` | Akhileth | — | biome « littoral_rocheux » — milieux calculés : steppe_piemont<br>biome « foret_montagne » — milieux calculés : steppe_piemont<br>exposition « Vase estuarienne et marnage » — non soutenue par le site (envasement) |
| `LUR_CHERBEKH-KHEM_NO` | Cherbekh-khem | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | exposition « ensablement des chenaux » — non soutenue par le site (ensablement) |
| `LUR_TAWALMAZ_NE` | Tawālmaz | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_QABD-AR-GANUB_NE` | Qabḍ-ār-Ǧanūb | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_QURASH-TANIQA_NE` | Qūrāš-Tanīqa | éboulements, glissements (versants raides) | aucun |
| `LUR_QURASH-TANIHIL_NE` | Qūrāš-Taniḥīl-Ramšūr | — | aucun |
| `ZRS_SHALIM_NE` | Šālim | crues (lit majeur); aridité (< 150 mm) | biome « steppe_piemont » — milieux calculés : desert_pierreux, plaine_alluviale |
| `LUR_SARIQ_NE` | Ṣarīq | — | aucun |
| `ZRS_HAMAD-RAS_NE` | Ḥamaḍ-Rās | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_ABNAQIL_NE` | Abnaqil | crues (lit majeur); brouillards d'évaporation (Hiver de Vapeur) | aucun |
| `LUR_ABNIQA_NE` | Abnīqa | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage; aridité (< 150 mm) | exposition « Ensablement bras secondaires » — non soutenue par le site (ensablement) |
| `LUR_TANAQIL_NE` | Tanāqil | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_QABSUR-QIBS_E` | Qabṣūr-Qibṣ | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_HAWQIL_NE` | Ḥawqil | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_TANAHIL_NE` | Tanāḥil | crues (lit majeur); aridité (< 150 mm) | exposition « Avalanches de redoux sur l'accès au col Abnī-tɨra » — non soutenue par le site (avalanches) |
| `LUR_SHAFAQ-MIRQ_NE` | Šafāq-Mirq | tempêtes et houle de rivage | exposition « ensablement des bouches » — non soutenue par le site (ensablement) |
| `LUR_TANQUISH_NE` | Ṭanquish | tempêtes et houle de rivage | biome « depression_saline » — milieux calculés : fourre_cotier_sec, océan, plaine_alluviale |
| `LUR_TNAYA-HAEM_SE` | T'naya-Ḥaem | tempêtes et houle de rivage; éboulements, glissements (versants raides) | aucun |
| `LUR_KURE-KESUN_SE` | K'uré-K’ésun | tempêtes et houle de rivage; aridité (< 150 mm) | aucun |
| `LUR_KURE-TAWA_SE` | K'uré-tawa | tempêtes et houle de rivage; aridité (< 150 mm) | aucun |
| `LUR_KUTEKA_SO` | Kù-téka | — | exposition « Ensablement saisonnier de l'émissaire » — non soutenue par le site (ensablement) |
| `LUR_KUNGUMI_SO` | Ku-Ngúmi | crues (lit majeur) | biome « zone_humide_lacustre » — milieux calculés : foret_tropicale_humide, herbage_arbore |
| `LUR_KUBELAA_SO` | Kù-Bèláà | tempêtes et houle de rivage | aucun |
| `LUR_MAZI-DUM_SO` | Mázì-Dúm | tempêtes et houle de rivage | aucun |
| `ZRS_KUSALADI_SO` | Ku-sáladì | — | aucun |
| `ZRS_KUUMANA_SO` | Ku-ùmanà | — | aucun |
| `ZRS_SAKUMADI_FORS` | Sa-kúmadì | — | aucun |
| `ZRS_KUPEPANA_FORS` | Ku-pèpanà | — | aucun |
| `LUR_KUBEKA_SC` | Kù-békà | — | aucun |
| `LUR_KUPILA-MUSUKU_SC` | Ku-Pɨla-Mù-Sùkú | — | aucun |
| `LUR_KUKIBO_QESHA_SC` | Q'eša-Kɨ́bò | — | aucun |
| `ZRS_KU-PILA-DI_SC` | Ku-Pɨla-dì | — | aucun |
| `ZRS_KU-SUKU-NA_SC` | Ku-Sùkú-nà | — | aucun |
| `ZRS_KU-LEMBE_SC` | Ku-Lémbè | — | aucun |
| `ZRS_KU-ZABA_SC` | Kù-Zàbà | — | aucun |
| `ZRS_MI-TONO_SC` | Mi-Tónò | — | aucun |
| `ZRS_KU-PELE-SO_SC` | Ku-Pélé-sò | — | aucun |
| `ZRS_KU-BANGA_SC` | Ku-Bángá | — | aucun |
| `ZRS_KU-NOMA_SC` | Ku-Nómà | — | biome « plaine_alluviale » — milieux calculés : eaux_lacustres, foret_tropicale_humide |
| `ZRS_KUKANADI_SC` | Ku-kànadì | — | aucun |
| `LUR_BANNAKTI_NO` | Bannaktì | éboulements, glissements (versants raides) | aucun |
| `LUR_TAMAR-KHU_CENTRE` | !Tamar-\|\|Khu | — | aucun |
| `LUR_ZAGAKH-TIR_NE` | Zagakh-TƗr | — | aucun |
| `LUR_URUM-SAMEL_CENTRE` | \|'Urum-!Samel | avalanches / chutes de pierres (\|'Arin); éboulements, glissements (versants raides); hypoxie légère (> 2 500 m); Hiver Blanc : neige et gel durables; aridité (< 150 mm) | aucun |
| `LUR_UKH-SEK_CENTRE` | \|'Ukh-\|\|Sék | avalanches / chutes de pierres (\|'Arin); éboulements, glissements (versants raides); hypoxie légère (> 2 500 m) | aucun |
| `LUR_ETHAK-KEL_CENTRE` | \|\|Ethak-Kél-Ts'idar | avalanches / chutes de pierres (\|'Arin) | aucun |
| `LUR_TSIDAR-SEK_CENTRE` | Ts'idar-‖Sek | avalanches / chutes de pierres (\|'Arin); hypoxie légère (> 2 500 m); Hiver Blanc : neige et gel durables; aridité (< 150 mm) | aucun |
| `LUR_GITES-TSIDAR_SE` | Gîtes-Ts'idar | — | exposition « blocages par avalanches en amont » — non soutenue par le site (avalanches) |
| `LUR_TSIDAR-RE_SE` | Ts'idar-ré | avalanches / chutes de pierres (\|'Arin) | aucun |
| `LUR_KUMAL-NAQRA_SE` | K'umal-Naqra | aridité (< 150 mm) | exposition « glissements de terrain » — non soutenue par le site (éboulements / glissements) |
| `LUR_HAE-TSI-KURE_SE` | Hae Ts'i-K'uré | — | exposition « Hypoxie/froid (saison \|'Arin-sukhì) » — non soutenue par le site (hypoxie) |
| `LUR_PI-KURE-NESHA_SE` | P'i-K'uré-Neša | aridité (< 150 mm) | aucun |
| `LUR_HAE-PESHU_SE` | Hae-P'ešu | aridité (< 150 mm) | aucun |
| `LUR_QIREL-TSIDAR_SE` | Q'irel-Ts'idar | — | exposition « Sécheresses prolongées » — non soutenue par le site (sécheresses) |

### D. Routes : tracé calculé

Tracé le plus rapide sur la carte (grille ≈ 5 km), dans les modes déclarés par la route. Un milieu absent des modes déclarés n'est emprunté que s'il est inévitable (colonne « hors modes »).

| ID | Route | Modes déclarés | Longueur (vol d'oiseau) km | Durée (j) | km par milieu | Hors modes déclarés (km) | Ruptures de charge | Altitude max / D+ (m) | Cols franchis ; mois ouverts |
|---|---|---|---|---|---|---|---|---|---|
| `RT_001` | Kù-békà ↔ Kù-téka | terrestre_caravane | 2296 (2170) | 83.0 | terre 2293 | — | 1 | 1266 / 3793 | — |
| `RT_002` | Abnaqil ↔ Kralekh-ner | maritime_cabotage | 3430 (2992) | 47.0 | mer Halakhel 3405, terre 22 | terre 19 | 1 | 29 / 2 | — |
| `RT_003` | Kù-téka ↔ Ku-jálima-rir | fluvial, maritime_cabotage | 1483 (1201) | 29.0 | océan 859, lac 5, fleuve (aval) 320, fleuve (amont) 110, terre 179 | terre 168 | 3 | 799 / 140 | — |
| `RT_004` | Tawālmaz ↔ Khloreth-klam | maritime_cabotage, terrestre_portage | 2706 (2390) | 47.0 | mer Halakhel 2416, terre 286 | — | 1 | 1232 / 1461 | — |
| `RT_005` | Serékh-khem ↔ Kralekh-ner | maritime_cabotage | 59 (59) | 1.3 | mer Halakhel 49, terre 7 | — | 1 | -20 / 7 | — |
| `RT_006` | Abnī-tɨra ↔ Tanāḥil | col_haute_altitude, terrestre_caravane | 936 (922) | 32.0 | terre 936 | — | 0 | 2515 / 1377 | Abnī-tɨra (001, 2800 m) ; juin → oct |
| `RT_007` | Tanāḥil ↔ Ports T'nayel SE | fluvial, maritime_cabotage | 4348 (1198) | 74.0 | océan 2118, fleuve (aval) 2071, fleuve (amont) 7, terre 145 | terre 138 | 2 | 623 / 596 | — |
| `RT_008` | Ṭanquish ↔ Méditerranée NE | maritime_cabotage | 185 (177) | 2.9 | océan 181, terre 2 | — | 1 | -1 / 0 | — |
| `RT_009` | \|'Ukh-\|\|Sék ↔ Q'irel-Ts'idar | terrestre_portage | 456 (358) | 25.0 | terre 456 | — | 0 | 2961 / 3582 | T'araq-ɨnkh (010, 2400 m) ; mai → oct |
| `RT_010` | Tanāḥil ↔ Kù-békà | col_haute_altitude, fluvial, lacustre, terrestre_caravane, terrestre_portage | 1260 (1139) | 39.0 | lac 70, fleuve (aval) 5, fleuve (amont) 276, terre 906 | — | 1 | 1581 / 2423 | — |
| `RT_011` | Talom-ak ↔ Kot-Skral | maritime_hauturier | 2109 (2055) | 16.0 | océan 2099, terre 5 | — | 2 | 365 / 0 | — |
| `RT_012` | Abnīqa ↔ Abnaqil | fluvial, maritime_cabotage | 58 (54) | 1.4 | fleuve (aval) 30, fleuve (amont) 21, terre 7 | terre 7 | 0 | 30 / 45 | — |
| `RT_013` | Ḥawqil ↔ Abnaqil | fluvial, maritime_cabotage | 370 (323) | 6.5 | mer Halakhel 298, fleuve (aval) 30, fleuve (amont) 27, terre 9 | — | 2 | 30 / 28 | — |
| `RT_014` | Abnīqa ↔ Tanāqil | fluvial, maritime_cabotage | 77 (32) | 1.5 | mer Halakhel 72, terre 2 | — | 1 | -10 / 0 | — |
| `RT_015` | Tanāqil ↔ Abnaqil | maritime_cabotage | 163 (54) | 3.0 | mer Halakhel 138, terre 22 | terre 19 | 1 | 29 / 26 | — |
| `RT_016` | Imekh-stom ↔ Tawālmaz | maritime_cabotage | 1700 (1380) | 23.0 | mer Halakhel 1700 | — | 0 | None / 0 | — |
| `RT_017` | Aktrik-khem ↔ Dimlāš | fluvial, maritime_cabotage | 3776 (3422) | 52.0 | mer Halakhel 3730, fleuve (aval) 13, terre 26 | terre 21 | 2 | 30 / 59 | — |
| `RT_018` | Imekh-stom ↔ Khloreth-klam | maritime_cabotage, terrestre_portage | 1209 (1090) | 27.0 | mer Halakhel 920, terre 286 | — | 1 | 1232 / 1461 | — |
| `RT_019` | Q'usa-\|\|ema ↔ Ts'idar-ré | col_haute_altitude | 20 (20) | 1.3 | terre 20 | — | 0 | 2192 / 115 | Q'usa-\|\|ema (016, 2100 m) ; avr → nov |
| `RT_020` | Kù-kèdà yì Mù-Kíri ↔ Ts'idar-ré | col_haute_altitude, maritime_cabotage | 5078 (4463) | 189.0 | océan 1811, lac 505, terre 2753 | — | 3 | 2309 / 8654 | P'etsul-!ama (013, 2600 m) ; mai → oct |
| `RT_021` | \|'Urum-‖Sek ↔ Dimlāš | col_haute_altitude, terrestre_caravane | 2269 (2099) | 76.0 | terre 2269 | — | 0 | 3216 / 1626 | — |
| `RT_022` | Qūrāš-Ṣafīḥ ↔ Ḥamaḍ-Rās | maritime_cabotage | 107 (99) | 1.9 | mer Halakhel 102, terre 2 | — | 1 | 26 / 0 | — |
| `RT_023` | Tawālmaz ↔ Abnaqil | maritime_cabotage | 1769 (1503) | 24.0 | mer Halakhel 1744, terre 22 | terre 19 | 1 | 29 / 26 | — |
| `RT_024` | !Tama-\|'Ara ↔ Dimlāš | col_haute_altitude, terrestre_caravane | 3071 (2734) | 105.0 | terre 3071 | — | 0 | 1743 / 6214 | — |
| `RT_025` | Hae Ts'i-K'uré ↔ \|'Urum-‖Sek | col_haute_altitude | 846 (821) | 47.0 | terre 846 | — | 0 | 2961 / 4846 | — |
| `RT_026` | Gîtes-Ts'idar ↔ Ts'idar-ré | col_haute_altitude | 110 (106) | 8.1 | terre 110 | — | 0 | 2192 / 1915 | — |
| `RT_027` | Khloreth-klam ↔ Kralekh-Aktrik | terrestre_portage | 291 (291) | 14.0 | terre 291 | — | 0 | 1232 / 1407 | — |
| `RT_028` | Qabṣūr-Qibṣ ↔ Abnaqil | terrestre_caravane | 123 (111) | 4.8 | terre 120 | — | 1 | 57 / 232 | — |
| `RT_029` | Piémonts du Mù-dárhòbì ↔ Kù-békà | fluvial, lacustre, terrestre_portage | 2318 (2000) | 78.0 | lac 322, fleuve (aval) 282, fleuve (amont) 796, terre 915 | — | 1 | 1069 / 2360 | — |
| `RT_030` | Qabṣūr-Qibṣ ↔ Tanāḥil | fluvial | 2748 (1308) | 58.0 | mer Halakhel 48, fleuve (aval) 11, fleuve (amont) 2658, terre 15 | mer 48 | 5 | 378 / 408 | — |
| `RT_031` | Gîtes-Ts'idar ↔ Tanāḥil | fluvial | 994 (798) | 23.0 | fleuve (aval) 765, fleuve (amont) 5, terre 223 | terre 223 | 0 | 1977 / 1684 | — |
| `RT_032` | Foyers-Purs ↔ Voie-Pure-des-Vallées | fluvial, maritime_cabotage | 2726 (1799) | 46.0 | mer Halakhel 93, océan 1861, fleuve (aval) 291, fleuve (amont) 223, terre 246 | terre 233 | 4 | 2068 / 842 | — |
| `RT_033` | Forges-des-Coques ↔ Cercle-Sans-Juron | maritime_cabotage | 4418 (2560) | 66.0 | mer Halakhel 18, océan 4103, terre 289 | terre 280 | 3 | 646 / 532 | — |
| `RT_034` | Voie-Desnuées ↔ Foyers-Purs | col_haute_altitude, maritime_cabotage | 259 (247) | 14.0 | terre 259 | — | 0 | 2517 / 2316 | — |
| `RT_035` | Akhileth ↔ Imekh-stom | fluvial, maritime_cabotage | 135 (126) | 3.7 | mer Halakhel 53, fleuve (amont) 5, terre 74 | terre 72 | 1 | 397 / 1 | — |
| `RT_036` | K'uré-tawa ↔ Abnaqil | fluvial, maritime_cabotage | 2436 (1719) | 39.0 | océan 1843, fleuve (aval) 260, fleuve (amont) 213, terre 114 | terre 109 | 2 | 441 / 538 | — |
| `RT_037` | Kù-kèdà yì Mù-Kíri ↔ Aktrik-khem | maritime_cabotage, terrestre_caravane | 4584 (2554) | 68.0 | mer Halakhel 167, océan 4103, terre 304 | — | 3 | 646 / 555 | — |
| `RT_038` | S'akum-\|ena ↔ K'uré-tawa | col_haute_altitude, maritime_cabotage | 1055 (977) | 57.0 | terre 1055 | — | 0 | 2177 / 5552 | S'akum-\|ena (015, 2200 m); Ṣamar-q'ut (046, 2200 m) ; avr → nov |
| `RT_039` | Kralekh-ner ↔ Qūrāš-Ṣafīḥ | maritime_cabotage | 3308 (2925) | 44.0 | mer Halakhel 3308 | — | 0 | None / 0 | — |
| `RT_040` | Qabḍ-ār-Ǧanūb ↔ Khloreth-klam | maritime_cabotage, terrestre_portage | 3707 (3259) | 61.0 | mer Halakhel 3408, terre 293 | — | 2 | 1232 / 1476 | — |
| `RT_041` | Serékh-khem ↔ Qūrāš-Ṣafīḥ | maritime_cabotage | 3366 (2912) | 45.0 | mer Halakhel 3357, terre 7 | — | 1 | -20 / 7 | — |
| `RT_042` | Ku-jálima-rir ↔ Ports externes NO | maritime_hauturier | 4495 (3689) | 30.0 | océan 4495 | — | 0 | None / 0 | — |
| `RT_043` | Bannaktì ↔ Ts'idar-‖Sek | col_haute_altitude, terrestre_caravane | 819 (724) | 31.0 | terre 819 | — | 0 | 2842 / 7834 | Hlelak-!uri (032, 2900 m) ; juin → sep |
| `RT_044` | Ts'idar-‖Sek ↔ Cherbekh-khem | col_haute_altitude, terrestre_caravane | 618 (577) | 22.0 | terre 615 | — | 1 | 2842 / 1799 | Hlelak-!uri (032, 2900 m); Kraloth-!enu (035, 2700 m) ; juin → sep |
| `RT_045` | Foyers-Purs ↔ K'uré-tawa | col_haute_altitude, maritime_cabotage | 147 (137) | 7.1 | terre 147 | — | 0 | 2068 / 189 | — |
| `RT_046` | Imekh-stom ↔ Ku-jálima-rir | maritime_cabotage | 5347 (2338) | 78.0 | mer Halakhel 933, océan 4126, terre 281 | terre 275 | 2 | 763 / 1082 | — |
| `RT_047` | Kù-békà ↔ Ku-jálima-rir | fluvial, lacustre, maritime_cabotage | 4484 (3306) | 78.0 | océan 1704, lac 200, fleuve (aval) 1813, fleuve (amont) 318, terre 441 | terre 435 | 2 | 1220 / 521 | — |
| `RT_048` | Voie-Haute ↔ Hae Ts'i-K'uré | col_haute_altitude | 74 (73) | 4.6 | terre 74 | — | 0 | 1839 / 1042 | — |
| `RT_049` | Voie-Comptable ↔ Kisralom | maritime_cabotage | 6363 (4983) | 93.0 | mer Halakhel 3618, océan 2410, terre 317 | terre 300 | 6 | 2031 / 325 | — |
| `RT_050` | Cherbekh-khem ↔ Imekh-stom | maritime_cabotage, terrestre_caravane | 379 (229) | 5.0 | mer Halakhel 379 | — | 0 | None / 0 | — |
| `RT_051` | Bannaktì ↔ Cherbekh-khem | terrestre_caravane | 1357 (1255) | 47.0 | terre 1353 | — | 1 | 2016 / 4388 | Hlenik-k'eso (038, 2000 m) ; avr → nov |
| `RT_052` | T'naya-Ḥaem ↔ Q'irel-Ts'idar | terrestre_caravane, terrestre_portage | 985 (911) | 38.0 | terre 985 | — | 0 | 2514 / 7699 | — |
| `RT_053` | Ṣarīq ↔ \|\|Ethak-Kél-Ts'idar | terrestre_caravane | 2492 (2325) | 87.0 | terre 2492 | — | 0 | 2386 / 4255 | T'araq-ɨnkh (010, 2400 m) ; mai → oct |
| `RT_054` | Ku-jálima-rir ↔ Jáli-Fè | maritime_cabotage | 149 (138) | 2.4 | océan 141, terre 4 | — | 1 | -8 / 0 | — |
| `RT_055` | Jáli-Fè ↔ Anses-Jálondù | maritime_cabotage | 319 (269) | 5.1 | océan 306, terre 6 | — | 2 | -3 / 0 | — |
| `RT_056` | Talom-ak ↔ Kisralom | maritime_cabotage | 333 (275) | 12.0 | mer Halakhel 18, océan 11, terre 292 | terre 280 | 4 | 646 / 532 | — |
| `RT_057` | Talom-ak ↔ Ku-jálima-rir | maritime_hauturier | 4189 (2720) | 29.0 | océan 4184, terre 2 | — | 1 | 365 / 0 | — |
| `RT_058` | Kisralom ↔ Serékh-khem | maritime_cabotage | 765 (636) | 11.0 | mer Halakhel 752, terre 9 | — | 2 | 26 / 0 | — |
| `RT_059` | Ku-Ngúmi ↔ Estuaire Mopámà | fluvial | 728 (498) | 21.0 | océan 23, fleuve (aval) 374, fleuve (amont) 148, terre 163 | mer 23, terre 142 | 6 | 693 / 154 | — |
| `RT_060` | Kù-Bèláà ↔ Ku-jálima-rir | fluvial | 1529 (1248) | 53.0 | océan 885, fleuve (aval) 75, fleuve (amont) 69, terre 250 | mer 885 | 77 | 16 / 22 | — |
| `RT_061` | Ts'idar-‖Sek ↔ K'elis-‖ara | col_haute_altitude | 4200 (3909) | 216.0 | terre 4200 | — | 0 | 2842 / 10602 | K'elis-‖ara (011, 2500 m); Hlelak-!uri (032, 2900 m); Krathal-t'iq (041, 2300 m) ; juin → sep |
| `RT_062` | Gîtes-Ts'idar ↔ \|\|Ethak-Kél-Ts'idar | terrestre_caravane | 71 (63) | 3.8 | terre 71 | — | 0 | 2386 / 1286 | T'araq-ɨnkh (010, 2400 m) ; mai → oct |
| `RT_063` | Qūrāš-Tanīqa ↔ K'umal-Naqra | terrestre_caravane | 366 (344) | 14.0 | terre 366 | — | 0 | 2792 / 2192 | — |
| `RT_064` | Abnī-tɨra ↔ Zagakh-TƗr | col_haute_altitude | 817 (766) | 43.0 | terre 817 | — | 0 | 2515 / 1462 | Abnī-tɨra (001, 2800 m) ; juin → oct |
| `RT_065` | Hae Ts'i-K'uré ↔ P'etsul-!ama | terrestre_caravane | 42 (40) | 1.9 | terre 42 | — | 0 | 2397 / 736 | P'etsul-!ama (013, 2600 m) ; mai → oct |
| `RT_066` | Kot-Skral ↔ Bannaktì | maritime_hauturier, terrestre_caravane | 2106 (1770) | 34.0 | océan 1422, terre 677 | — | 2 | 1262 / 1493 | — |
| `RT_067` | K'umal-Naqra ↔ K'uré-K'ésun | col_haute_altitude | 208 (199) | 11.0 | terre 208 | — | 0 | 2472 / 906 | — |
| `RT_068` | Gîtes-Ts'idar ↔ Q'eša-Kɨ́bò | terrestre_caravane | 1722 (1386) | 63.0 | terre 1722 | — | 0 | 1912 / 6043 | T'amr-khɨna (017, 2450 m) ; mai → oct |
| `RT_069` | Ku-Pɨla-Mù-Sùkú ↔ Q'eša-Kɨ́bò | lacustre, terrestre_portage | 220 (143) | 6.6 | lac 126, terre 90 | — | 1 | 1178 / 238 | — |
| `RT_070` | Lisières Ba-lóngó ↔ Q'eša-Kɨ́bò | terrestre_caravane | 1815 (1735) | 62.0 | terre 1815 | — | 0 | 1178 / 3665 | — |
| `RT_071` | Šālim ↔ Abnīqa | fluvial | 264 (233) | 5.5 | fleuve (aval) 221, fleuve (amont) 30, terre 13 | terre 13 | 0 | 30 / 64 | — |
| `RT_072` | Sa-nùbè yì Mù-Sùkú ↔ Talom-ak | fluvial, maritime_cabotage | 9368 (4347) | 156.0 | océan 4580, lac 387, fleuve (aval) 4079, fleuve (amont) 122, terre 184 | terre 167 | 5 | 1529 / 1315 | — |
| `RT_073` | \|'Urum-‖Sek ↔ Ḥamūqaš | col_haute_altitude, terrestre_caravane | 2297 (2129) | 78.0 | terre 2297 | — | 0 | 3216 / 1762 | — |
| `RT_074` | Hae K'umel ↔ Talom-ak | maritime_cabotage | 7149 (5324) | 104.0 | océan 6774, terre 363 | terre 352 | 4 | 2369 / 1110 | ʿUbayl-t'iq (044, 2000 m) ; avr → nov |

### E. Routes : milieux et hivers traversés (voies de terre)

| ID | Milieux traversés (km) | Faciès \|'Arin traversés (km) |
|---|---|---|
| `RT_001` | steppe_piemont 1109, herbage_arbore 1004, foret_tropicale_humide 90, zone_humide_lacustre 71, foret_berge 23 | hors \|'Arin 2296 |
| `RT_002` | — | — |
| `RT_003` | foret_tropicale_humide 501, herbage_arbore 71, zone_humide_lacustre 20 | hors \|'Arin 605 |
| `RT_004` | steppe_piemont 145, fourre_cotier_sec 57, foret_montagne 48 | hiver pluvieux tempéré 125, Hiver Gris 85, Hiver Jaune 59 |
| `RT_005` | — | — |
| `RT_006` | steppe_piemont 602, desert_pierreux 313, plaine_alluviale 21 | hors \|'Arin 913 |
| `RT_007` | plaine_alluviale 2063, desert_pierreux 133, desert_sableux 20 | hors \|'Arin 2034, Hiver Jaune 190 |
| `RT_008` | — | — |
| `RT_009` | herbage_arbore 217, foret_montagne 203, steppe_piemont 22 | hors \|'Arin 318, Hiver Gris 138 |
| `RT_010` | desert_pierreux 490, herbage_arbore 364, steppe_piemont 192, foret_berge 102, foret_tropicale_humide 22 | hors \|'Arin 1183 |
| `RT_011` | — | — |
| `RT_012` | plaine_alluviale 58 | Hiver de Vapeur 53 |
| `RT_013` | plaine_alluviale 67 | Hiver de Vapeur 62 |
| `RT_014` | — | — |
| `RT_015` | plaine_alluviale 25 | Hiver de Vapeur 25 |
| `RT_016` | — | — |
| `RT_017` | plaine_alluviale 27 | Hiver de Vapeur 41 |
| `RT_018` | steppe_piemont 145, fourre_cotier_sec 57, foret_montagne 48 | hiver pluvieux tempéré 125, Hiver Gris 85, Hiver Jaune 59 |
| `RT_019` | foret_montagne 20 | Hiver Gris 20 |
| `RT_020` | herbage_arbore 1796, steppe_piemont 405, foret_tropicale_humide 335, foret_montagne 201, foret_berge 21 | hors \|'Arin 2680, Hiver Gris 78 |
| `RT_021` | desert_pierreux 1539, steppe_piemont 335, plaine_alluviale 249, herbage_arbore 118, prairie_altitude 28 | hors \|'Arin 1639, Hiver Jaune 552, Hiver Gris 72 |
| `RT_022` | — | — |
| `RT_023` | plaine_alluviale 25 | Hiver de Vapeur 25 |
| `RT_024` | steppe_piemont 2086, desert_pierreux 743, herbage_arbore 94, plaine_alluviale 64, foret_montagne 39, depression_saline 25 | hors \|'Arin 1522, Hiver Jaune 1056, Hiver de Vapeur 419, Hiver Gris 74 |
| `RT_025` | herbage_arbore 509, steppe_piemont 178, foret_montagne 124 | hors \|'Arin 728, Hiver Gris 118 |
| `RT_026` | foret_montagne 97 | hors \|'Arin 83, Hiver Gris 26 |
| `RT_027` | steppe_piemont 158, foret_montagne 50, fourre_cotier_sec 50 | hiver pluvieux tempéré 114, Hiver Gris 99, Hiver Jaune 46, Hiver de Vapeur 33 |
| `RT_028` | depression_saline 43, desert_pierreux 43, plaine_alluviale 38 | Hiver de Vapeur 105 |
| `RT_029` | foret_berge 767, herbage_arbore 694, steppe_piemont 474, zone_humide_lacustre 20 | hors \|'Arin 1989 |
| `RT_030` | plaine_alluviale 2654, desert_sableux 22 | hors \|'Arin 2075, Hiver Jaune 572, Hiver de Vapeur 43 |
| `RT_031` | plaine_alluviale 633, foret_montagne 147, foret_berge 130, herbage_arbore 69 | hors \|'Arin 994 |
| `RT_032` | plaine_alluviale 532, fourre_cotier_sec 81, steppe_piemont 79, desert_pierreux 59 | Hiver Jaune 508, Hiver Gris 126, hors \|'Arin 91, Hiver de Vapeur 32 |
| `RT_033` | steppe_piemont 134, herbage_arbore 126, desert_pierreux 31 | Hiver Gris 161, hiver pluvieux tempéré 69, Hiver Jaune 36, Hiver de Vapeur 25 |
| `RT_034` | desert_pierreux 130, steppe_piemont 129 | Hiver Jaune 247 |
| `RT_035` | steppe_piemont 38 | hors \|'Arin 53, Hiver de Vapeur 24 |
| `RT_036` | plaine_alluviale 493, fourre_cotier_sec 81 | Hiver Jaune 410, Hiver Gris 126, hors \|'Arin 41 |
| `RT_037` | steppe_piemont 134, herbage_arbore 126, desert_pierreux 47 | Hiver Gris 161, hiver pluvieux tempéré 69, Hiver de Vapeur 40, Hiver Jaune 36 |
| `RT_038` | steppe_piemont 364, herbage_arbore 287, foret_montagne 210, desert_pierreux 181 | hors \|'Arin 678, Hiver Jaune 320, Hiver Gris 57 |
| `RT_039` | — | — |
| `RT_040` | steppe_piemont 145, fourre_cotier_sec 57, foret_montagne 48, desert_pierreux 25 | hiver pluvieux tempéré 125, Hiver Gris 85, Hiver Jaune 59, Hiver de Vapeur 25 |
| `RT_041` | — | — |
| `RT_042` | — | — |
| `RT_043` | steppe_piemont 543, desert_pierreux 234, prairie_altitude 35 | Hiver Jaune 609, hors \|'Arin 177, Hiver Blanc 33 |
| `RT_044` | steppe_piemont 309, plaine_alluviale 97, desert_pierreux 96, prairie_altitude 75, littoral_rocheux 21 | Hiver Jaune 198, hors \|'Arin 175, Hiver de Vapeur 123, Hiver Blanc 116 |
| `RT_045` | steppe_piemont 73, desert_pierreux 66 | Hiver Jaune 98, hors \|'Arin 49 |
| `RT_046` | steppe_piemont 127, herbage_arbore 75, fourre_cotier_sec 44, desert_pierreux 26 | hiver pluvieux tempéré 126, Hiver Gris 98, Hiver Jaune 38 |
| `RT_047` | foret_berge 1177, foret_tropicale_humide 590, steppe_piemont 514, herbage_arbore 245, zone_humide_lacustre 35 | hors \|'Arin 2574 |
| `RT_048` | herbage_arbore 41, foret_montagne 34 | hors \|'Arin 74 |
| `RT_049` | fourre_cotier_sec 231, steppe_piemont 57 | hiver pluvieux tempéré 128, Hiver Gris 64, Hiver Jaune 52, hors \|'Arin 42, Hiver de Vapeur 29 |
| `RT_050` | — | — |
| `RT_051` | steppe_piemont 710, desert_pierreux 509, plaine_alluviale 98, littoral_rocheux 21 | Hiver Jaune 1007, hors \|'Arin 201, Hiver de Vapeur 142 |
| `RT_052` | steppe_piemont 491, herbage_arbore 300, foret_montagne 161 | hors \|'Arin 806, Hiver Gris 179 |
| `RT_053` | desert_pierreux 1224, plaine_alluviale 586, steppe_piemont 337, foret_montagne 151, herbage_arbore 124, depression_saline 55 | hors \|'Arin 1891, Hiver Jaune 564, Hiver Gris 37 |
| `RT_054` | — | — |
| `RT_055` | — | — |
| `RT_056` | steppe_piemont 134, herbage_arbore 126, desert_pierreux 31 | Hiver Gris 161, hiver pluvieux tempéré 69, Hiver Jaune 36, Hiver de Vapeur 25 |
| `RT_057` | — | — |
| `RT_058` | — | — |
| `RT_059` | foret_tropicale_humide 594, foret_maree 53, herbage_arbore 38 | hors \|'Arin 685 |
| `RT_060` | foret_maree 252, foret_tropicale_humide 124 | hors \|'Arin 376 |
| `RT_061` | steppe_piemont 3157, desert_pierreux 684, herbage_arbore 236, foret_montagne 92, prairie_altitude 24 | hors \|'Arin 3050, Hiver Jaune 885, Hiver Gris 241, Hiver Blanc 24 |
| `RT_062` | foret_montagne 63 | hors \|'Arin 45, Hiver Gris 25 |
| `RT_063` | steppe_piemont 331, herbage_arbore 23 | Hiver Jaune 201, hors \|'Arin 84, Hiver Gris 81 |
| `RT_064` | steppe_piemont 554, herbage_arbore 129, foret_montagne 106 | Hiver Gris 305, Hiver Jaune 268, hors \|'Arin 245 |
| `RT_065` | herbage_arbore 22 | Hiver Gris 22 |
| `RT_066` | steppe_piemont 603, desert_pierreux 69 | hors \|'Arin 606, Hiver Jaune 70 |
| `RT_067` | steppe_piemont 160, desert_pierreux 34 | Hiver Jaune 133, hors \|'Arin 76 |
| `RT_068` | herbage_arbore 1346, foret_montagne 222, steppe_piemont 96, foret_tropicale_humide 40 | hors \|'Arin 1722 |
| `RT_069` | herbage_arbore 93 | hors \|'Arin 93 |
| `RT_070` | herbage_arbore 1012, steppe_piemont 780 | hors \|'Arin 1815 |
| `RT_071` | plaine_alluviale 264 | Hiver Jaune 202, Hiver de Vapeur 62 |
| `RT_072` | plaine_alluviale 2834, foret_tropicale_humide 789, steppe_piemont 278, desert_pierreux 270, foret_berge 89, foret_montagne 67, herbage_arbore 35, desert_sableux 20 | hors \|'Arin 3605, Hiver Jaune 523, hiver pluvieux tempéré 192, Hiver Gris 66 |
| `RT_073` | desert_pierreux 1507, steppe_piemont 335, plaine_alluviale 283, herbage_arbore 118, prairie_altitude 28, depression_saline 25 | hors \|'Arin 1662, Hiver Jaune 473, Hiver de Vapeur 89, Hiver Gris 72 |
| `RT_074` | steppe_piemont 206, fourre_cotier_sec 119, desert_pierreux 27 | Hiver Jaune 205, Hiver Gris 64, hiver pluvieux tempéré 59, hors \|'Arin 33 |

### F. Variantes imposées par une indication du corpus

| ID | Étapes imposées | Longueur km | Durée (j) | Altitude max (m) | Cols franchis ; mois ouverts | Écart avec le tracé optimal |
|---|---|---|---|---|---|---|
| `RT_010` | GEO_COL_014 | 2614 | 69.0 | 2624 | T'iqur-ɨlkh (014, 2700 m) ; juin → oct | +1354 km, +30.0 j |
| `RT_027` | LUR_STAKHR-DUREK_NO | 300 | 15.0 | 1232 | — ; — | +9 km, +1.0 j |
| `RT_066` | LUR_STALOMAR-KOT_NO | 2924 | 44.0 | 1347 | — ; — | +818 km, +10.0 j |

### G. Corrections proposées (extrémités ou modes modifiés)

| ID | Origine → destination proposées | Modes | Étapes | Longueur km | Durée (j) | km par milieu | Altitude max (m) | Cols franchis ; mois ouverts |
|---|---|---|---|---|---|---|---|---|
| `RT_020` | LUR_KUBEKA_SC → LUR_TSIDAR-RE_SE | col_haute_altitude, lacustre, terrestre_caravane | — | 1371 | 50.0 | lac 70, terre 1297 | 2309 | — ; — |

### H. Trouées basses de la cordillère

Passages plus bas que les cols canoniques du tronçon (profil de crête mesuré tous les 6 km). Nom : à forger (`forge-ling`).

| ID | Chaîne | Position | Crête minimale (m) | Largeur (km) | Cols canoniques du tronçon | Routes calculées qui l'empruntent | Statut |
|---|---|---|---|---|---|---|---|
| `TRO_01` | \|\|Urumati-k'ara (prolongement SE) | [27.0, 11.94] | 1178 | 360 | Kurel-ahek 2 150 m — P'etsul-!ama 2 600 m | — | principale — à nommer |
| `TRO_02` | \|\|Urumati-k'ara (prolongement SE) | [31.47, 10.29] | 1578 | 114 | P'etsul-!ama 2 600 m — K'elis-‖ara 2 500 m | RT_020, RT_025, RT_048, RT_061, RT_068 | principale — à nommer |
| `TRO_03` | \|\|Urumati-k'ara (prolongement SE) | [32.93, 9.88] | 1239 | 108 | K'elis-‖ara 2 500 m — T'amr-khɨna 2 450 m | RT_068, RT_072 | secondaire |
| `TRO_04` | \|\|Urumati-k'ara (prolongement SE) | [34.22, 9.4] | 1790 | 60 | T'amr-khɨna 2 450 m — T'araq-ɨnkh 2 400 m | RT_020, RT_068 | secondaire |
| `TRO_05` | \|\|Urumati-lóngò | [3.93, 18.74] | 1387 | 60 | Kù-Pété-‖Eni 1 900 m — Ku-Ténɨlkh-te 2 300 m | — | secondaire |
| `TRO_06` | \|\|Urumati-lóngò | [7.52, 13.67] | 1473 | 48 | Lémakhɨ 2 200 m — Ku-Pámà-Tɨra-te 2 000 m | — | secondaire |
| `TRO_07` | \|\|Urumati-lóngò (extrémité S) | [7.25, 11.48] | 1201 | 234 | Ku-Pámà-Tɨra-te 2 000 m — fin de chaîne | — | principale — à nommer |

<!-- GENERE:FIN -->
