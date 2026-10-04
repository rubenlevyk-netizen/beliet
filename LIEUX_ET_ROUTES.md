# Lieux et routes du Beliet — passe de cohérence (carte v0.5)

Ce document confronte les lieux (LIEUX_URBAINS v2 : 56 cités LUR, 18 zones ZRS) et les routes (RESEAU_ROUTES v3 : 74 routes) à la géographie de la carte. Il donne pour chaque lieu une position et ses caractéristiques physiques calculées, et pour chaque route un tracé, une longueur, une durée, des altitudes, des cols et des saisons. Il signale chaque écart et propose une solution. Il est écrit pour l'agent qui fait cascader les décisions dans le corpus. Les fiches de synthèse sont reprises dans `ALIGNEMENT_CORPUS.md` §9 (ALN-130 à ALN-178).

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
| ATL_SO | Ku-jálima-rir, Jáli-Fè, Anses-Jálondù, Jáli-lòngò, Gálu-kánda, Li-sèk-dì | D'ouest en est : Anses-Jálondù (anse, face à Li-sèk-dì), Ku-jálima-rir (mangroves), Jáli-Fè (delta du Mopámà), Gálu-kánda (cales à la tête du delta, sur l'émissaire), Jáli-lòngò (côte relevée à l'est du delta). |
| ATL_INS | Kot-Skral, Threskōl-Strakh | Îles du Cap-Vert réel : Skral-Kot = São Vicente ; Strakh-Kot = Boa Vista (§2.3). |
| HKL_N | Khreth-na-Serek, Serékh-khem, Kralekh-ner | Khreth-na-Serek sur la rive ouest de la passe ; Serékh-khem au fond du golfe de Serek ; Kralekh-ner = sortie nord de la passe. |
| HKL_NO / HKL_O | Akhidalet, Kralekh-Aktrik, Aktrik-khem, Hlom-khetal | Akhidalet à l'embouchure réelle de l'Ehukhtal (-7,72° ; 27,19°), au fond du goulet. Kralekh-Aktrik sur la rive nord du goulet, point de l'Halakhel le plus proche de l'Atlantique. Aktrik-khem à 150 km à l'est. Hlom-khetal sur la rive sud du goulet. |
| HKL_SO / HKL_S | Imekh-stom, Akhileth, Cherbekh-khem, Tawālmaz, Qabḍ-ār-Ǧanūb | Imekh-stom au goulet de l'Imikhrel ; Cherbekh-khem à 230 km à l'est ; Tawālmaz sur la ria de la Madīlan ; Qabḍ-ār-Ǧanūb au cap du golfe de Koufra, extrémité sud de la mer. |
| HKL_E (delta d'Abnīqa) | Abnaqil, Abnīqa, Tanāqil, Qabṣūr-Qibṣ, Ḥawqil, Qūrāš-Ṣafīḥ, Ḥamaḍ-Rās | Abnaqil à l'apex du cône deltaïque, où divergent les chenaux Abnīṣar (NE) et Tanīlḥa (SE). Abnīqa au débouché ouest ; Qūrāš-Ṣafīḥ sur l'Abnīṣar ; Tanāqil sur la Tanīlḥa ; Qabṣūr-Qibṣ sur les salines de la côte, au sud ; Ḥamaḍ-Rās sur un cap au nord ; Ḥawqil à l'embouchure du Ḥawqal. |
| HKL_NE (haute Tanāḥil) | Qūrāš-Tanīqa, Qūrāš-Taniḥīl-Ramšūr, Šālim, Ṣarīq, Tanāḥil | Haute Tanāḥil = gorge amont du Tira-ñara/Tanāḥil (Abay réel). Tanāḥil à la confluence avec l'Abnuḥīl (Khartoum réel). Ṣarīq en bordure du marais de Ṣaraq (§2.2). |
| MED_NE | Šafāq-Mirq, Ṭanquish | Šafāq-Mirq aux bouches du delta Šafāqil ; Ṭanquish sur la côte à l'ouest du delta, bordée de lagunes. |
| ROU_SE / IND_SE | T'naya-Ḥaem, K'uré-K'ésun, K'uré-tawa | K'uré-tawa : port corallien (Massawa réel). K'uré-K'ésun : côte basaltique au pied de l'escarpement. T'naya-Ḥaem : golfe de Tadjoura, jonction mer Rouge / océan de l'Est. |
| MOP_SO | Kù-téka, Ku-Ngúmi, Kù-Bèláà, Mázì-Dúm, Ku-sáladì | Kù-téka à la sortie de l'émissaire ; Ku-Ngúmi juste en aval ; Kù-Bèláà et Mázì-Dúm dans les mangroves du delta du Mopámà (ALN-081) ; Ku-sáladì sur la rive sud du lac. |
| TUM_SC / FOR_S | Kù-békà, Ku-Pɨla-Mù-Sùkú, Q'eša-Kɨ́bò et 10 ZRS | Kù-békà sur pilotis près de la rive nord ; Ku-Pɨla-Mù-Sùkú sur la rive sud-ouest, au pied des collines Kù-kɨ́bò où se tient Q'eša-Kɨ́bò ; bancs et récifs dans le lac ; bourgs de rive au nord et au nord-est ; Sa-kúmadì et Ku-pèpanà dans la haute futaie de la rive sud. |
| URU_NO / URU_SO | Bannaktì, !Tamar-‖Khu | Bannaktì au cœur du territoire KOL (halekh occidental, 1 770 m). !Tamar-‖Khu dans les vallées sud de lóngò. |
| URU_C | Zagakh-TƗr, \|'Urum-!Samel, \|'Ukh-‖Sék, ‖Ethak-Kél-Ts'idar, Ts'idar-‖Sek | Zagakh-TƗr sur l'émissaire de l'Akhtir. \|'Urum-!Samel sous les glaciers de \|'Ara-Sukhì (3 710 m). \|'Ukh-‖Sék sur la crête du prolongement SE de k'ara, à l'ouest du col T'araq-ɨnkh. ‖Ethak-Kél-Ts'idar au col T'araq-ɨnkh. Ts'idar-‖Sek sur la crête de halekh oriental (§4, LR-12). |
| URU_SE / PLT_SE | Gîtes-Ts'idar, Ts'idar-ré, Q'irel-Ts'idar, K'umal-Naqra, Hae Ts'i-K'uré, P'i-K'uré-Neša, Hae-P'ešu | Groupe Ts'idar autour des cols T'araq-ɨnkh et Q'usa-‖ema : Gîtes au pied de l'escarpement ; Ts'idar-ré au col Q'usa-‖ema ; Q'irel-Ts'idar sur le plateau, à l'est. K'umal-Naqra sur le rebord oriental, au-dessus de la mer Rouge. Hae Ts'i-K'uré au pied du col P'etsul-!ama. P'i-K'uré-Neša et Hae-P'ešu sur le plateau au-dessus de K'uré-tawa. |

### 2.2 La haute Tanāḥil est la gorge amont de l'Abay (ALN-136, résout ALN-083)
Le corpus donnait deux sens à « Tanāḥil » : l'affluent des plateaux SE (§VI.5) et une « vallée des piémonts nord de k'ara » où LIEUX place trois lieux (§V.2). Le prolongement SE de k'ara borde précisément la gorge amont du Tira-ñara/Tanāḥil (Abay réel), au nord de la chaîne. La définition du Géosystème correspond trait pour trait à cette gorge :
- canyon en grès et marno-calcaires (formations réelles d'Adigrat et d'Antalo) ;
- fond semi-aride : steppe de piémont, 430 à 570 mm/an sur la carte ;
- crues saisonnières ;
- bassin de l'Abnuḥīl, sans lien de drainage avec la Méditerranée.

Les deux sens se rejoignent : la vallée des villes est celle du fleuve. Conséquences :
- **Tanāḥil** (« tête de vallée fluviale, confluence de transition montagne-delta ») se place à la confluence avec l'Abnuḥīl (Khartoum réel). Il s'y trouve en tête de la vallée de l'Abnuḥīl, au débouché de la haute Tanāḥil.
- **Qūrāš-Tanīqa et Qūrāš-Taniḥīl-Ramšūr** (ethnie TNQ) sont à ~300 km des cols du territoire TNQ (044, 046, 047), ce qui satisfait le regroupement territorial.
- **RT_063** Qūrāš-Tanīqa ↔ K'umal-Naqra passe de « trans-Beliet » à 360 km (13 jours), cohérent avec une contrebande muletière de nuit.
- **RT_031** Gîtes-Ts'idar ↔ Tanāḥil (« fluvial amont ») et **RT_010** (« remontée Tanāḥil » puis col) deviennent lisibles.
- **Coût** : la « chaîne urbaine Abnīqa-Tanāḥil-Ṭanquish » s'étire sur 2 700 km de vallée ; RT_030 (Qabṣūr-Qibṣ → Tanāḥil, remontée) dure ~58 jours.

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

---

## 3. Modifications de la géographie (v0.5)

Quatre changements apportent un contenu absent jusqu'ici. Chacun est physiquement fondé. Aucun ne déplace un lieu canonique, un lac, une chaîne ou un col.

| ID | Changement | Pourquoi | Physique | Effet mesuré |
|---|---|---|---|---|
| ALN-130 | **Rivages escarpés de l'Halakhel** : 7 secteurs de falaises, caps et rias (100 à 170 m de commandement) : passe Khreth-na-Serek, goulet Hlom-khetal, goulet d'Imekh-stom, rias de Cherbekh-khem, ria Tawālmaz, cap de Qabḍ-ār-Ǧanūb, cap de Ḥamaḍ-Rās | La v0.4 imposait un glacis à tout le pourtour (5,5 m/km) : aucun littoral rocheux, alors que LIEUX en déclare 9 et que le Géosystème décrit passe, promontoire, goulets et rias | Rebords de plateaux (hamadas calcaires, coulées basaltiques, grès) tranchés par la mer ; vallées noyées pour les rias. Le glacis reste la règle ailleurs (« HKL_S glacis ») | Littoral rocheux : 12 750 → 20 990 km² ; 8 lieux sur 9 dans leur milieu (Akhileth excepté, LR-05) |
| ALN-131 | **Plaine deltaïque du Mopámà** : terrain abaissé à 1 m + 0,16 m/km de la mer, sur ~180 km de côte | Le delta (GEO_DLT_MOPAMA, « delta de Jáli-Fè », « mangroves ») était un plateau de 20 à 40 m sans mangrove | Delta tropical à sédiments abondants (lac de 28 000 km², émissaire de 650 km) : plaine basse, marées, mangroves | Forêt de marée : 29 350 → 30 440 km² ; Kù-Bèláà en mangrove, Mázì-Dúm à 15 km |
| ALN-132 | **Chenaux du cône d'Abnīqa** : Abnīṣar (NE) et Tanīlḥa (SE) tracés depuis l'apex (28,95° ; 27,6°) | Canon (GEO §VI.1.3) jamais dessiné | Cône de déjection à chenaux instables (Géosystème, interfluve) | Abnaqil, Qūrāš-Ṣafīḥ et Tanāqil reçoivent un site |
| ALN-133 | **Règle du littoral rocheux** : hauteur mesurée au-dessus de l'eau voisine (la mer Halakhel est à −20 m) ; pente à l'échelle de la latitude ; liseré protégé du lissage | La règle mesurait la hauteur au-dessus de l'océan et le lissage effaçait les liserés étroits | Correction de calcul | Inclus dans ALN-130 |
| ALN-134 | **Deux points de calibration des pluies** : versant humide ouest des plateaux SE (2 200 mm) ; rive sud du Tùmázì (1 800 mm) | Le modèle donnait jusqu'à 9 500 mm à l'escarpement des cols T'araq-ɨnkh et Q'usa-‖ema, et 3 800 mm au sud du Tùmázì, hors de toute plage du corpus | Maxima orographiques ramenés à des valeurs plausibles (2 900 et 2 450 mm au point) | Gîtes-Ts'idar 9 530 → 3 800 mm ; ‖Ethak-Kél 7 500 → 3 080 mm |

**Non modifié, consigné :**
- **Brèches des chaînes** (ALN-160) : le prolongement SE de k'ara et lóngò ont des brèches plus basses que leurs cols. Relever les crêtes reviendrait à plier la géographie au corpus.
- **Distance Mopámà-Tùmázì** (~2 000 km, ALN-165) : le Tùmázì reste au Sud-Centre (choix v0.3.1).
- **Sables du portage NO** (ALN-140) : le corridor reçoit 300 à 550 mm/an (calage du corpus lui-même) ; c'est une steppe, pas un erg.

---

## 4. Lieux : constats et solutions

Biomes et expositions de 74 lieux (106 mentions) confrontés au site : 54 lieux sans écart, 26 mentions en écart. Les écarts restants et leur traitement :

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
| LR-09 | Mázì-Dúm | `foret_maree` : site à 30 m, à la lisière de la mangrove | Garder ; la mangrove est à 15 km | — |
| LR-10 | \|'Ukh-‖Sék | `prairie_altitude`, refuges à 3 200 m. La crête du prolongement SE de k'ara culmine à ~2 450 m vers 9,5° N ; la prairie commence à ~2 900 m à cette latitude | (a) le corpus garde le site et remplace « prairie » par « forêt de montagne claire » et « refuges à 2 200-2 400 m » ; ou (b) le sanctuaire va sur les hauts plateaux de qoyra (> 3 000 m), à l'est de T'araq-ɨnkh, ce qui oblige à revoir RT_009 | ALN-150 |
| LR-11 | \|'Urum-!Samel | Seul lieu à biome `glacier` : seuls les flancs de \|'Ara-Sukhì (k'ara) en portent. Site : 3 710 m, prairie et zone périglaciaire sous les glaciers, Hiver Blanc. Or les cols du territoire URM (024, 025, 028) sont sur lóngò, à 1 300 km | Garder le sanctuaire à \|'Ara-Sukhì : les URM y montent en pèlerinage depuis leurs vallées de lóngò ; ou retirer `glacier` et placer le bourg sur lóngò | ALN-151 |
| LR-12 | Ts'idar-‖Sek | Deux ancrages incompatibles : « interface Költ (Bannaktì) / façade HKL_S/SO (Cherbekh-khem) » à l'ouest ; ethnie Ts'idari et RT_061 vers K'elis-‖ara à l'est, à 3 900 km | Retenu : crête de halekh oriental (2 840 m, Hiver Blanc, « Mur de l'Hiver »). Corriger RT_061 (LT-21) | ALN-152 |
| LR-13 | Tanāḥil | « Avalanches de redoux sur l'accès au col Abnī-tɨra » : le col est à 920 km | Viser le col de la haute Tanāḥil : T'iqur-ɨlkh (2 700 m) ou Rafīq-t'sal (2 300 m) | ALN-153 |
| LR-14 | Hae Ts'i-K'uré | « Hypoxie/froid » : le monastère est à 1 890 m, hors \|'Arin ; c'est le col P'etsul-!ama (2 600 m, Hiver Gris) qui l'expose | Rattacher l'exposition à la montée du col (RT_065) | ALN-154 |
| LR-15 | Gîtes-Ts'idar | « blocages par avalanches en amont » : site à 1 380 m hors \|'Arin ; les cols voisins sont en Hiver Gris | Garder : l'aléa vient des cols (amont) ; préciser « en amont, aux cols T'araq-ɨnkh et Q'usa-‖ema » | — |
| LR-16 | Q'irel-Ts'idar | « Sécheresses prolongées » : 1 370 mm/an sur le plateau à l'est des cols | Lire « saison sèche marquée » ; ou situer Q'irel-Ts'idar plus au nord-est, sur le plateau sec qui borde la haute Tanāḥil (500 à 700 mm vers 38,3° E, 10,5-11° N), au prix d'un RT_009 plus long | ALN-155 |
| LR-17 | K'umal-Naqra | « glissements de terrain » : versants modérés au site retenu ; « canaux, conflits pour l'eau » : 94 mm/an | Garder : vallées encaissées irriguées du rebord oriental, arides. Les glissements relèvent des corniches de RT_067 | — |
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

74 routes tracées. 22 empruntent un milieu absent de leurs modes déclarés, dont 15 de plus de 50 km. 23 dépassent 2 500 km ; dix d'entre elles sont de simples traversées de la mer Halakhel ou de l'océan.

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

Écarts mineurs, sans action : Abnaqil est à 20 km de la mer, sur le bras d'Abnīqa (RT_002, 012, 015, 017, 023 : accès fluvial au port). Qabṣūr-Qibṣ et Kù-Bèláà sont sur le rivage (RT_030, 060 : 50 à 60 km de mer au départ).

### 5.2 Rapides : émissaire du Mopámà et haute Tanāḥil
- **Émissaire du Mopámà.** Il descend de 800 m sur 650 km (1,2 m/km en moyenne). Plusieurs biefs dépassent 1,5 m/km. RT_003 (Kù-téka → Ku-jálima-rir) et RT_059 (Ku-Ngúmi → estuaire) comptent 140 à 160 km de portage autour des rapides. Le corpus le dit déjà : aléa « barres/rapides » de RT_003. **Action** : ajouter un segment `terrestre_portage` aux deux routes, ou préciser « navigable par biefs » (GEO §VI.3 : « navigable, ~600 km ») (ALN-170).
- **Haute Tanāḥil.** La gorge n'est pas navigable. RT_071 (Šālim → Abnīqa) commence par ~110 km de piste. RT_031 (Gîtes-Ts'idar → Tanāḥil) commence par ~220 km de descente de l'escarpement avant le premier bief navigable. **Action** : ajouter `terrestre_caravane` en tête des deux routes (ALN-170).

### 5.3 Cols et brèches de la cordillère
- **Brèches** (ALN-160). Le profil de crête mesuré montre des passages plus bas que les cols canoniques :
  - prolongement SE de k'ara : 1 180 m vers 27,0° E, 11,9° N (sur ~360 km) ; 1 240 m vers 32,9° E ; 1 580 m vers 31,5° E. Les cols canoniques de ce tronçon sont à 2 100-2 800 m.
  - lóngò : 1 200 à 1 670 m en six points. Ses cols sont à 1 900-2 400 m.
  Ces brèches sont du relief réel (monts Nouba, cuvette du Sudd, plateau de Jos) que les chaînes n'ont pas recouvert. Un convoi qui veut seulement passer les emprunte.
  **Solutions** : (a) ajouter au registre des « trouées » à nommer, voies basses chaudes et sans neige mais longues ou exposées (marais, raids) ; les cols restent les voies courtes, gardées, à péage ; (b) relever les crêtes de la carte, solution écartée car elle plierait la géographie au corpus.
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
| LT-22 | RT_020 Kù-kèdà yì Mù-Kíri ↔ Ts'idar-ré | 4 470 km, 184 jours | « cabotage + cols » | origine fausse : un port de la mer Rouge, K'uré-tawa ou T'naya-Ḥaem (ALN-163) |
| LT-23 | RT_001 Kù-békà ↔ Kù-téka | 2 440 km, 84 jours | caravane P3 entre les deux lacs | garder : grande caravane trans-forestière (sel, poisson, bois) ; annoter la durée (ALN-165) |
| LT-24 | RT_029 Piémonts du Mù-dárhòbì ↔ Kù-békà | 2 330 km, 81 jours ; « canaux inter-lacs » | aucun canal possible entre deux bassins distants de 2 000 km | origine → piémonts des collines Kù-kɨ́bò (basalte de Ku-Bángá) : quelques dizaines de km de portage, puis le lac (ALN-166) |
| LT-25 | RT_070 Lisières Ba-lóngó ↔ Q'eša-Kɨ́bò | 1 850 km, 65 jours | « pistes de contrebandiers (nuit) » | origine → lisières de la rive S du Tùmázì (FOR_S) (ALN-167) |
| LT-26 | RT_053 Ṣarīq ↔ ‖Ethak-Kél | 2 500 km, 87 jours | caravane lourde annuelle | garder (axe trans-sumdanien du §VII.5) ; annoter |
| LT-27 | RT_024 !Tama-\|'Ara ↔ Dimlāš | 3 070 km, 105 jours | voie rituelle | garder comme pèlerinage au long cours ; annoter |
| LT-28 | RT_021, RT_073 \|'Urum-‖Sek ↔ Abnaqil / Abnīqa | 2 190-2 220 km, ~75 jours | col + vallée | cohérent : crête → vallée de l'Abnuḥīl → delta |
| LT-29 | RT_071 Šālim ↔ Abnīqa | 3 830 km, 73 jours de fleuve (haute Tanāḥil → Abnuḥīl → bras d'Abnīqa) | « drainage administratif » | cohérent avec §2.2 ; annoter la durée |
| LT-30 | RT_030 Qabṣūr-Qibṣ ↔ Tanāḥil | 2 750 km de remontée, 58 jours | « remontée saisonnière » | cohérent avec §2.2 |

### 5.5 Durées canoniques
- **Portage NO** : 291 km et 14 jours de Khloreth-klam à Kralekh-Aktrik (RT_027), contre « 3 jours » au Géosystème. La valeur de 8 à 10 jours d'ALN-033 est trop courte d'un tiers : le tracé franchit les contreforts côtiers (point haut ~1 230 m). **Action** : « portage NO : 12 à 15 jours » (ALN-171).
- **Caravanes Halakhel E → mer Rouge** (ALN-173) : « 8 jours » au Géosystème. La carte mesure 370 km au plus court, soit 12 à 13 jours à 30 km par jour. Les 8 jours supposent ~45 km par jour (méhari) : cohérent pour une caravane légère.
- **Navigation intérieure** : traverser l'Halakhel d'ouest en est prend 44 à 52 jours de cabotage (RT_002, 017, 039, 041 ; 3 300 à 3 800 km).

### 5.6 Routes cohérentes
Les autres routes ne présentent pas d'écart : trafic de la mer Halakhel, réseau du delta d'Abnīqa, routes atlantiques, réseau des cols du SE, façade de la mer Rouge, routes de halekh. Leurs mesures sont dans les tables D et E.

---

## 6. Points à trancher par l'auteur

1. **LR-10 / ALN-150** : \|'Ukh-‖Sék sur la crête (le biome change) ou sur les hauts plateaux de qoyra (la route RT_009 change).
2. **LR-11 / ALN-151** : \|'Urum-!Samel à \|'Ara-Sukhì (pèlerinage lointain) ou sur lóngò (sans glacier).
3. **ALN-160** : nommer les trouées basses du prolongement SE de k'ara et de lóngò, ou les laisser anonymes.
4. **LT-22 / ALN-163** : origine maritime de RT_020.

---

## 7. Tables générées

Les tables suivantes sont produites par `outils/lieux_routes.py`. Elles ne doivent pas être éditées à la main.

<!-- GENERE:DEBUT (outils/lieux_routes.py — ne pas éditer à la main) -->

### A. Lieux : position et site

Positions [PROPOSITION] en [longitude, latitude]. « Écart » = distance entre la cible raisonnée et la cellule retenue.

| ID | Nom | Type | Façade | Position | Altitude (m) | Dénivelé 10 km (m) | Milieu du site | Milieux à 25 km (%) |
|---|---|---|---|---|---|---|---|---|
| `LUR_KHLORETH-KLAM_NO` | Khloreth-klam | LUR | ATL_NO | [-9.568, 30.099] | 60 | 160 | fourre_cotier_sec | fourre_cotier_sec 54, océan 40, hors Beliet 5 |
| `LUR_STALOMAR-KOT_NO` | Stalomar-Kot | LUR | ATL_NO | [-10.03, 29.296] | 366 | 816 | littoral_rocheux | océan 32, fourre_cotier_sec 24, hors Beliet 15, herbage_arbore 12 |
| `LUR_STAKHR-DUREK_NO` | Stakhr-Durek | LUR | ATL_NO | [-8.532, 28.976] | 364 | 456 | steppe_piemont | steppe_piemont 59, herbage_arbore 36 |
| `LUR_HLORAN-RIR_NO` | Hloran-rir | LUR | ATL_NO | [-8.054, 29.601] | 529 | 481 | steppe_piemont | steppe_piemont 85, herbage_arbore 14 |
| `ZRS_FALAMI_SKREN_PERIPH_NO` | Oase-Skren | ZRS | ATL_NO | [-8.58, 29.352] | 855 | 525 | steppe_piemont | herbage_arbore 55, foret_montagne 27, steppe_piemont 18 |
| `LUR_KU-JALIMA-RIR_SO` | Ku-jálima-rir | LUR | ATL_SO | [0.057, 5.619] | 7 | 114 | foret_maree | océan 47, foret_tropicale_humide 43, foret_maree 11 |
| `LUR_JALI-FE_SO` | Jáli-Fè | LUR | ATL_SO | [1.013, 5.92] | 17 | 61 | foret_tropicale_humide | foret_tropicale_humide 51, océan 37, foret_maree 11 |
| `LUR_ANSES-JALONDU_SO` | Anses-Jálondù | LUR | ATL_SO | [-0.756, 5.206] | 2 | 86 | foret_maree | océan 51, foret_tropicale_humide 34, foret_maree 16 |
| `LUR_JALI-LONGO_SO` | Jáli-lòngò | LUR | ATL_SO | [2.447, 6.364] | -5 | 99 | foret_tropicale_humide | foret_tropicale_humide 56, océan 44 |
| `LUR_GALU-KANDA_SO` | Gálu-kánda | LUR | ATL_SO | [1.443, 6.443] | 6 | 3 | foret_tropicale_humide | foret_tropicale_humide 100 |
| `ZRS_LISEKDI_SO` | Li-sèk-dì | ZRS | ATL_SO | [-1.25, 4.714] | 18 | 71 | foret_maree | océan 100 |
| `LUR_KOT-SKRAL_LARGE` | Kot-Skral | LUR | ATL_INS | [-24.994, 16.884] | 2 | 430 | ile_aride | océan 71, ile_aride 29 |
| `LUR_THRESKOL-STRAKH_LARGE` | Threskōl-Strakh | LUR | ATL_INS | [-22.906, 16.166] | 1 | 178 | ile_aride | océan 72, ile_aride 28 |
| `LUR_KRETH-NA-SEREK_N` | Khreth-na-Serek | LUR | HKL_N | [-1.983, 29.671] | 107 | 215 | littoral_rocheux | mer Halakhel 64, desert_pierreux 30 |
| `LUR_SEREKH-KHEM_N` | Serékh-khem | LUR | HKL_N | [-1.632, 30.772] | -27 | 133 | desert_pierreux | desert_pierreux 68, mer Halakhel 23, desert_sableux 9 |
| `AUX_KRALEKH-NER` | Kralekh-ner | AUX | — | [-1.728, 30.25] | sur l'eau (mer Halakhel) | 112 | mer Halakhel | mer Halakhel 100 |
| `LUR_AKHIDALET_NO` | Akhidalet | LUR | HKL_NO | [-7.72, 27.19] | 10 | 135 | plaine_alluviale | steppe_piemont 44, mer Halakhel 35, plaine_alluviale 21 |
| `LUR_KRALEKH-AKTRIK_NO` | Kralekh-Aktrik | LUR | HKL_NO | [-7.497, 28.206] | 32 | 139 | desert_pierreux | steppe_piemont 58, mer Halakhel 37, desert_pierreux 5 |
| `LUR_AKTRIK-KHEM_NO` | Aktrik-khem | LUR | HKL_NO | [-5.983, 28.262] | -2 | 116 | desert_pierreux | desert_pierreux 89, mer Halakhel 10 |
| `LUR_HLOM-KHETAL_NO` | Hlom-khetal | LUR | HKL_O | [-6.891, 27.488] | 64 | 211 | littoral_rocheux | mer Halakhel 56, steppe_piemont 38 |
| `LUR_IMEKH-STOM_NO` | Imekh-stom | LUR | HKL_SO | [0.344, 25.707] | 59 | 203 | littoral_rocheux | desert_pierreux 56, mer Halakhel 41 |
| `ZRS_AKHILETH_NO` | Akhileth | ZRS | HKL_SO | [0.599, 24.596] | 443 | 203 | steppe_piemont | steppe_piemont 98 |
| `LUR_CHERBEKH-KHEM_NO` | Cherbekh-khem | LUR | HKL_S | [2.623, 25.85] | 55 | 209 | littoral_rocheux | mer Halakhel 62, desert_pierreux 30, littoral_rocheux 7 |
| `LUR_TAWALMAZ_NE` | Tawālmaz | LUR | HKL_S | [14.064, 25.203] | 62 | 245 | littoral_rocheux | mer Halakhel 58, steppe_piemont 27, herbage_arbore 14 |
| `LUR_QABD-AR-GANUB_NE` | Qabḍ-ār-Ǧanūb | LUR | HKL_S | [22.574, 23.709] | 32 | 164 | littoral_rocheux | desert_pierreux 58, mer Halakhel 34, littoral_rocheux 5 |
| `LUR_QURASH-TANIQA_NE` | Qūrāš-Tanīqa | LUR | HKL_NE | [38.351, 10.555] | 1384 | 1097 | herbage_arbore | herbage_arbore 59, steppe_piemont 24, plaine_alluviale 13 |
| `LUR_QURASH-TANIHIL_NE` | Qūrāš-Taniḥīl-Ramšūr | LUR | HKL_NE | [38.446, 10.947] | 1413 | 828 | steppe_piemont | steppe_piemont 73, herbage_arbore 27 |
| `ZRS_SHALIM_NE` | Šālim | ZRS | HKL_NE | [38.096, 10.101] | 1146 | 773 | herbage_arbore | foret_montagne 58, herbage_arbore 33, foret_berge 9 |
| `LUR_SARIQ_NE` | Ṣarīq | LUR | HKL_NE | [29.395, 29.365] | 231 | 53 | desert_pierreux | desert_pierreux 61, steppe_piemont 25, depression_saline 14 |
| `ZRS_HAMAD-RAS_NE` | Ḥamaḍ-Rās | ZRS | HKL_NE | [28.168, 29.31] | 43 | 185 | littoral_rocheux | desert_pierreux 43, mer Halakhel 32, depression_saline 23 |
| `AUX_QURASH-SAFIH` | Qūrāš-Ṣafīḥ | AUX | — | [28.407, 28.445] | 2 | 131 | depression_saline | mer Halakhel 48, depression_saline 29, desert_pierreux 18 |
| `LUR_ABNAQIL_NE` | Abnaqil | LUR | HKL_E | [28.901, 27.615] | 27 | 62 | plaine_alluviale | plaine_alluviale 73, desert_pierreux 15, depression_saline 10 |
| `LUR_ABNIQA_NE` | Abnīqa | LUR | HKL_E | [28.359, 27.657] | 12 | 72 | plaine_alluviale | mer Halakhel 47, plaine_alluviale 30, depression_saline 20 |
| `LUR_TANAQIL_NE` | Tanāqil | LUR | HKL_E | [28.423, 27.375] | -5 | 110 | depression_saline | mer Halakhel 55, plaine_alluviale 23, depression_saline 22 |
| `LUR_QABSUR-QIBS_E` | Qabṣūr-Qibṣ | LUR | HKL_E | [28.343, 26.75] | 0 | 118 | depression_saline | mer Halakhel 61, depression_saline 30 |
| `LUR_HAWQIL_NE` | Ḥawqil | LUR | HKL_E | [26.893, 25.333] | 6 | 141 | depression_saline | mer Halakhel 53, depression_saline 25, plaine_alluviale 11, desert_pierreux 8 |
| `LUR_TANAHIL_NE` | Tanāḥil | LUR | HKL_E | [32.55, 15.614] | 378 | 29 | plaine_alluviale | desert_pierreux 51, plaine_alluviale 46 |
| `LUR_SHAFAQ-MIRQ_NE` | Šafāq-Mirq | LUR | MED_NE | [31.291, 31.481] | 0 | 12 | plaine_alluviale | plaine_alluviale 54, océan 45 |
| `LUR_TANQUISH_NE` | Ṭanquish | LUR | MED_NE | [29.809, 31.073] | 0 | 49 | plaine_alluviale | océan 42, plaine_alluviale 32, fourre_cotier_sec 26 |
| `AUX_MEDITERRANEE_NE` | Méditerranée NE (façade) | AUX | — | [31.004, 32.293] | sur l'eau (océan) | 540 | océan | océan 100 |
| `LUR_TNAYA-HAEM_SE` | T'naya-Ḥaem | LUR | ROU_SE | [42.892, 11.744] | -15 | 994 | littoral_rocheux | steppe_piemont 46, océan 37, desert_pierreux 8, littoral_rocheux 8 |
| `LUR_KURE-KESUN_SE` | K'uré-K’ésun | LUR | ROU_SE | [40.135, 15.014] | 62 | 199 | littoral_rocheux | cote_desertique 41, recif_corallien 26, desert_pierreux 19, hors Beliet 9 |
| `LUR_KURE-TAWA_SE` | K'uré-tawa | LUR | ROU_SE | [39.45, 15.598] | 368 | 666 | littoral_rocheux | steppe_piemont 31, recif_corallien 30, océan 15, desert_pierreux 14 |
| `LUR_KUTEKA_SO` | Kù-téka | LUR | MOP_SO | [5.045, 9.504] | 804 | 60 | zone_humide_lacustre | eaux_lacustres 43, zone_humide_lacustre 39, herbage_arbore 17 |
| `LUR_KUNGUMI_SO` | Ku-Ngúmi | LUR | MOP_SO | [4.583, 9.048] | 671 | 67 | foret_tropicale_humide | foret_tropicale_humide 83, herbage_arbore 17 |
| `LUR_KUBELAA_SO` | Kù-Bèláà | LUR | MOP_SO | [0.79, 5.73] | 17 | 65 | foret_maree | océan 49, foret_tropicale_humide 34, foret_maree 17 |
| `LUR_MAZI-DUM_SO` | Mázì-Dúm | LUR | MOP_SO | [1.571, 6.174] | 30 | 74 | foret_tropicale_humide | foret_tropicale_humide 51, océan 49 |
| `ZRS_KUSALADI_SO` | Ku-sáladì | ZRS | MOP_SO | [6.113, 9.394] | 807 | 75 | zone_humide_lacustre | eaux_lacustres 47, zone_humide_lacustre 31, foret_tropicale_humide 21 |
| `AUX_LISIERES_BALONGO` | Lisières Ba-lóngó | AUX | — | [6.288, 8.906] | 607 | 250 | foret_tropicale_humide | foret_tropicale_humide 59, herbage_arbore 40 |
| `AUX_PIEMONTS_MUDARHOBI` | Piémonts du Mù-dárhòbì | AUX | — | [6.607, 8.497] | 394 | 199 | foret_tropicale_humide | foret_tropicale_humide 92, zone_humide_lacustre 6 |
| `AUX_DLT_MOPAMA` | Estuaire Mopámà | AUX | — | [1.22, 6.047] | 21 | 80 | foret_tropicale_humide | foret_tropicale_humide 50, océan 46 |
| `ZRS_KUUMANA_SO` | Ku-ùmanà | ZRS | FOR_SO | [2.702, 7.408] | 320 | 122 | foret_tropicale_humide | foret_tropicale_humide 96 |
| `ZRS_SAKUMADI_FORS` | Sa-kúmadì | ZRS | FOR_S | [24.805, 6.205] | 976 | 67 | foret_tropicale_humide | foret_tropicale_humide 98 |
| `ZRS_KUPEPANA_FORS` | Ku-pèpanà | ZRS | FOR_S | [23.992, 5.904] | 939 | 78 | foret_tropicale_humide | foret_tropicale_humide 100 |
| `LUR_KUBEKA_SC` | Kù-békà | LUR | TUM_SC | [24.773, 8.717] | sur l'eau (lac) | 622 | eaux_lacustres | foret_tropicale_humide 52, eaux_lacustres 47 |
| `LUR_KUPILA-MUSUKU_SC` | Ku-Pɨla-Mù-Sùkú | LUR | TUM_SC | [23.196, 6.839] | 951 | 498 | herbage_arbore | herbage_arbore 68, eaux_lacustres 30 |
| `LUR_KUKIBO_QESHA_SC` | Q'eša-Kɨ́bò | LUR | TUM_SC | [21.905, 6.902] | 1219 | 166 | herbage_arbore | herbage_arbore 54, foret_montagne 45 |
| `ZRS_KU-PILA-DI_SC` | Ku-Pɨla-dì | ZRS | TUM_SC | [23.403, 7.202] | sur l'eau (lac) | 524 | eaux_lacustres | eaux_lacustres 74, herbage_arbore 25 |
| `ZRS_KU-SUKU-NA_SC` | Ku-Sùkú-nà | ZRS | TUM_SC | [24.088, 6.949] | sur l'eau (lac) | 502 | eaux_lacustres | eaux_lacustres 76, herbage_arbore 15, foret_tropicale_humide 10 |
| `ZRS_KU-LEMBE_SC` | Ku-Lémbè | ZRS | TUM_SC | [26.255, 8.308] | sur l'eau (lac) | 406 | eaux_lacustres | foret_tropicale_humide 51, eaux_lacustres 49 |
| `ZRS_KU-ZABA_SC` | Kù-Zàbà | ZRS | TUM_SC | [25.331, 8.371] | sur l'eau (lac) | 168 | eaux_lacustres | eaux_lacustres 85, foret_tropicale_humide 15 |
| `ZRS_MI-TONO_SC` | Mi-Tónò | ZRS | TUM_SC | [25.65, 7.013] | sur l'eau (lac) | 197 | eaux_lacustres | eaux_lacustres 90, foret_tropicale_humide 6 |
| `ZRS_KU-PELE-SO_SC` | Ku-Pélé-sò | ZRS | TUM_SC | [23.801, 8.843] | 1071 | 656 | herbage_arbore | herbage_arbore 63, eaux_lacustres 29, foret_tropicale_humide 7 |
| `ZRS_KU-BANGA_SC` | Ku-Bángá | ZRS | TUM_SC | [22.463, 7.329] | 1028 | 461 | herbage_arbore | herbage_arbore 78, eaux_lacustres 17 |
| `ZRS_KU-NOMA_SC` | Ku-Nómà | ZRS | TUM_SC | [26.701, 8.292] | 897 | 354 | foret_tropicale_humide | foret_tropicale_humide 70, eaux_lacustres 30 |
| `ZRS_KUKANADI_SC` | Ku-kànadì | ZRS | TUM_SC | [22.686, 7.992] | 1011 | 590 | herbage_arbore | herbage_arbore 52, eaux_lacustres 47 |
| `LUR_BANNAKTI_NO` | Bannaktì | LUR | URU_NO | [-9.106, 22.301] | 1766 | 1459 | steppe_piemont | steppe_piemont 89, prairie_altitude 6 |
| `LUR_TAMAR-KHU_CENTRE` | !Tamar-\|\|Khu | LUR | URU_SO | [4.407, 17.796] | 1596 | 676 | foret_montagne | foret_montagne 98 |
| `LUR_ZAGAKH-TIR_NE` | Zagakh-TƗr | LUR | URU_C | [23.658, 22.242] | 1198 | 39 | zone_humide_lacustre | zone_humide_lacustre 31, plaine_alluviale 28, eaux_lacustres 20, herbage_arbore 13 |
| `LUR_URUM-SAMEL_CENTRE` | \|'Urum-!Samel | LUR | URU_C | [17.905, 20.102] | 3708 | 2443 | prairie_altitude | zone_periglaciaire 53, prairie_altitude 40, glacier 5 |
| `LUR_UKH-SEK_CENTRE` | \|'Ukh-\|\|Sék | LUR | URU_C | [33.41, 9.598] | 2251 | 1640 | foret_montagne | foret_montagne 88, foret_tropicale_humide 12 |
| `LUR_ETHAK-KEL_CENTRE` | \|\|Ethak-Kél-Ts'idar | LUR | URU_C | [34.845, 8.906] | 2453 | 825 | foret_montagne | foret_montagne 100 |
| `LUR_TSIDAR-SEK_CENTRE` | Ts'idar-‖Sek | LUR | URU_C | [-2.094, 22.933] | 2842 | 803 | prairie_altitude | prairie_altitude 68, desert_pierreux 29 |
| `LUR_GITES-TSIDAR_SE` | Gîtes-Ts'idar | LUR | URU_SE | [34.351, 8.623] | 1382 | 588 | foret_montagne | foret_tropicale_humide 55, foret_montagne 45 |
| `LUR_TSIDAR-RE_SE` | Ts'idar-ré | LUR | URU_SE | [35.307, 8.717] | 2272 | 633 | foret_montagne | foret_montagne 100 |
| `LUR_KUMAL-NAQRA_SE` | K'umal-Naqra | LUR | URU_SE | [39.227, 13.423] | 1981 | 378 | steppe_piemont | desert_pierreux 69, depression_saline 17, steppe_piemont 14 |
| `LUR_HAE-TSI-KURE_SE` | Hae Ts'i-K'uré | LUR | URU_SE | [30.351, 10.743] | 1886 | 615 | herbage_arbore | herbage_arbore 55, foret_montagne 41 |
| `LUR_PI-KURE-NESHA_SE` | P'i-K'uré-Neša | LUR | URU_SE | [38.956, 15.245] | 2299 | 728 | desert_pierreux | desert_pierreux 54, steppe_piemont 46 |
| `LUR_HAE-PESHU_SE` | Hae-P'ešu | LUR | URU_SE | [39.052, 14.845] | 1662 | 228 | depression_saline | desert_pierreux 61, depression_saline 23, steppe_piemont 16 |
| `LUR_QIREL-TSIDAR_SE` | Q'irel-Ts'idar | LUR | PLT_SE | [35.896, 9.3] | 1845 | 823 | foret_montagne | foret_montagne 69, herbage_arbore 22, steppe_piemont 6 |
| `AUX_FOYERS-PURS` | Foyers-Purs | AUX | — | [38.701, 14.598] | 2008 | 463 | desert_pierreux | desert_pierreux 100 |
| `AUX_VOIE-DESNUEES` | Voie-Desnuées | AUX | — | [38.303, 12.398] | 2580 | 675 | steppe_piemont | steppe_piemont 96 |
| `AUX_VOIE-HAUTE` | Voie-Haute | AUX | — | [31.004, 10.602] | 1873 | 798 | foret_montagne | foret_montagne 81, herbage_arbore 17 |
| `AUX_HAE-KUMEL` | Hae K'umel | AUX | — | [38.797, 13.299] | 2516 | 688 | desert_pierreux | desert_pierreux 87, steppe_piemont 7 |
| `AUX_KUKEDA-MUKIRI` | Kù-kèdà yì Mù-Kíri | AUX | — | [0.057, 5.619] | 7 | 114 | foret_maree | océan 47, foret_tropicale_humide 43, foret_maree 11 |
| `AUX_FORGES-DES-COQUES` | Forges-des-Coques (Mù-Kíri) | AUX | — | [0.057, 5.619] | 7 | 114 | foret_maree | océan 47, foret_tropicale_humide 43, foret_maree 11 |
| `AUX_KISRALOM` | Kisralom | AUX | — | [-7.497, 28.206] | 32 | 139 | desert_pierreux | steppe_piemont 58, mer Halakhel 37, desert_pierreux 5 |
| `AUX_CERCLE-SANS-JURON` | Cercle-Sans-Juron | AUX | — | [-7.497, 28.206] | 32 | 139 | desert_pierreux | steppe_piemont 58, mer Halakhel 37, desert_pierreux 5 |
| `AUX_DIMLAS` | Dimlāš | AUX | — | [28.901, 27.615] | 27 | 62 | plaine_alluviale | plaine_alluviale 73, desert_pierreux 15, depression_saline 10 |
| `AUX_VOIE-PURE` | Voie-Pure-des-Vallées | AUX | — | [28.359, 27.657] | 12 | 72 | plaine_alluviale | mer Halakhel 47, plaine_alluviale 30, depression_saline 20 |
| `AUX_HAMUQAS` | Ḥamūqaš | AUX | — | [28.359, 27.657] | 12 | 72 | plaine_alluviale | mer Halakhel 47, plaine_alluviale 30, depression_saline 20 |
| `AUX_TAMA-ARA` | !Tama-\|'Ara | AUX | — | [4.407, 17.796] | 1596 | 676 | foret_montagne | foret_montagne 98 |
| `AUX_VOIE-COMPTABLE` | Voie-Comptable | AUX | — | [38.956, 15.245] | 2299 | 728 | desert_pierreux | desert_pierreux 54, steppe_piemont 46 |
| `AUX_PORTS-TNAYEL` | Ports T'nayel SE | AUX | — | [42.892, 11.744] | -15 | 994 | littoral_rocheux | steppe_piemont 46, océan 37, desert_pierreux 8, littoral_rocheux 8 |
| `AUX_SANUBE-MUSUKU` | Sa-nùbè yì Mù-Sùkú | AUX | — | [24.088, 6.949] | sur l'eau (lac) | 502 | eaux_lacustres | eaux_lacustres 76, herbage_arbore 15, foret_tropicale_humide 10 |
| `AUX_PORTS-EXTERNES-NO` | Ports externes NO | AUX | — | [-21.998, 34.502] | sur l'eau (océan) | 441 | océan | océan 100 |

### B. Lieux : climat, eaux, cols

| ID | Pluie (mm/an) | T annuelle (°C) | Hiver Tw / nuit Tn (°C) | Faciès \|'Arin | Distance mer Halakhel / océan / lac / cours d'eau (km) | Fleuve nommé à < 30 km ; débit max à 15 km (m³/s) | Col le plus proche |
|---|---|---|---|---|---|---|---|
| `LUR_KHLORETH-KLAM_NO` | 1411 | 19.0 | 9.0 / 1.0 | hiver pluvieux tempéré | 283 / 2 / 2490 / 26 | — ; 28 | Hlenik-k'eso (2000 m) à 831 km |
| `LUR_STALOMAR-KOT_NO` | 1245 | 17.5 | 7.7 / -0.3 | hiver pluvieux tempéré | 267 / 2 / 2463 / 102 | — ; 6 | Hlenik-k'eso (2000 m) à 749 km |
| `LUR_STAKHR-DUREK_NO` | 546 | 17.7 | 8.0 / -0.0 | Hiver Gris | 128 / 141 / 2357 / 32 | — ; 66 | Hlenik-k'eso (2000 m) à 702 km |
| `LUR_HLORAN-RIR_NO` | 479 | 16.4 | 6.5 / -1.5 | Hiver Gris | 153 / 154 / 2373 / 115 | — ; 18 | Hlenik-k'eso (2000 m) à 774 km |
| `ZRS_FALAMI_SKREN_PERIPH_NO` | 701 | 14.6 | 4.8 / -3.2 | hiver pluvieux tempéré | 158 / 116 / 2385 / 70 | — ; 11 | Hlenik-k'eso (2000 m) à 743 km |
| `LUR_KU-JALIMA-RIR_SO` | 2656 | 27.5 | 23.0 / 15.0 | hors \|'Arin | 2272 / 2 / 685 / 32 | — ; 40 | Ku-Pámà-Tɨra-te (2000 m) à 1189 km |
| `LUR_JALI-FE_SO` | 2375 | 27.4 | 22.9 / 14.9 | hors \|'Arin | 2237 / 4 / 581 / 2 | GEO_FLV_EMISSAIRE_MOPAMA ; 2550 | Ku-Pámà-Tɨra-te (2000 m) à 1091 km |
| `LUR_ANSES-JALONDU_SO` | 2923 | 27.5 | 23.1 / 15.1 | hors \|'Arin | 2323 / 2 / 785 / 25 | — ; 71 | Ku-Pámà-Tɨra-te (2000 m) à 1286 km |
| `LUR_JALI-LONGO_SO` | 2646 | 27.5 | 22.9 / 14.9 | hors \|'Arin | 2195 / 2 / 431 / 46 | — ; 88 | Ku-Pámà-Tɨra-te (2000 m) à 950 km |
| `LUR_GALU-KANDA_SO` | 2155 | 27.5 | 22.8 / 14.8 | hors \|'Arin | 2178 / 33 / 507 / 0 | GEO_FLV_EMISSAIRE_MOPAMA ; 80 | Ku-Pámà-Tɨra-te (2000 m) à 1017 km |
| `ZRS_LISEKDI_SO` | 2930 | 27.4 | 23.1 / 15.1 | hors \|'Arin | 2383 / 2 / 862 / 48 | — ; 0 | Ku-Pámà-Tɨra-te (2000 m) à 1363 km |
| `LUR_KOT-SKRAL_LARGE` | 543 | 25.3 | 18.3 / 10.3 | hors \|'Arin | 2164 / 2 / 3285 / 906 | — ; 1 | Ku-Mázì-Klek-te (1900 m) à 1190 km |
| `LUR_THRESKOL-STRAKH_LARGE` | 519 | 25.6 | 18.8 / 10.8 | hors \|'Arin | 2038 / 2 / 3062 / 674 | — ; 1 | Ku-Mázì-Klek-te (1900 m) à 1020 km |
| `LUR_KRETH-NA-SEREK_N` | 194 | 18.9 | 9.0 / -1.7 | Hiver de Vapeur | 2 / 613 / 2094 / 472 | — ; 0 | Halek-t'ama (1900 m) à 676 km |
| `LUR_SEREKH-KHEM_N` | 116 | 19.1 | 8.9 / -2.9 | Hiver de Vapeur | 3 / 486 / 2172 / 449 | — ; 0 | Halek-t'ama (1900 m) à 789 km |
| `AUX_KRALEKH-NER` | 168 | 19.3 | 9.3 / -1.8 | Hiver de Vapeur | 0 / 546 / 2133 / 505 | — ; 0 | Halek-t'ama (1900 m) à 734 km |
| `LUR_AKHIDALET_NO` | 292 | 20.6 | 11.3 / 1.8 | Hiver de Vapeur | 4 / 325 / 2186 / 2 | Ehukhtal ; 2 | Hlenik-k'eso (2000 m) à 513 km |
| `LUR_KRALEKH-AKTRIK_NO` | 283 | 20.0 | 10.5 / 0.9 | Hiver de Vapeur | 2 / 274 / 2246 / 109 | — ; 7 | Hlenik-k'eso (2000 m) à 628 km |
| `LUR_AKTRIK-KHEM_NO` | 201 | 20.2 | 10.6 / -0.0 | Hiver de Vapeur | 3 / 399 / 2166 / 184 | — ; 0 | Tkrilan-ɨkh (2800 m) à 601 km |
| `LUR_HLOM-KHETAL_NO` | 277 | 20.1 | 10.8 / 1.1 | Hiver de Vapeur | 2 / 371 / 2161 / 62 | — ; 1 | Tkrilan-ɨkh (2800 m) à 541 km |
| `LUR_IMEKH-STOM_NO` | 179 | 21.0 | 12.0 / 1.1 | Hiver de Vapeur | 2 / 1104 / 1669 / 62 | — ; 0 | Halek-t'ama (1900 m) à 228 km |
| `ZRS_AKHILETH_NO` | 193 | 19.2 | 10.4 / -0.3 | Hiver Jaune | 77 / 1194 / 1559 / 60 | — ; 1 | Halek-t'ama (1900 m) à 134 km |
| `LUR_CHERBEKH-KHEM_NO` | 191 | 20.9 | 11.9 / 1.1 | Hiver de Vapeur | 2 / 1160 / 1616 / 120 | — ; 0 | Ktamar-khɨ (3000 m) à 302 km |
| `LUR_TAWALMAZ_NE` | 569 | 21.2 | 12.3 / 4.3 | Hiver de Vapeur | 2 / 719 / 832 / 141 | — ; 1 | Ṣabūl-tɨkh (2900 m) à 544 km |
| `LUR_QABD-AR-GANUB_NE` | 151 | 22.0 | 13.5 / 2.2 | Hiver de Vapeur | 2 / 817 / 167 / 187 | — ; 0 | Qaṣūl-tɨra (2700 m) à 620 km |
| `LUR_QURASH-TANIQA_NE` | 565 | 19.2 | 13.6 / 5.6 | hors \|'Arin | 2056 / 471 / 1236 / 12 | Tira-ñara / Tanāḥil ; 43 | Nrelat-q'urm (2200 m) à 156 km |
| `LUR_QURASH-TANIHIL_NE` | 434 | 19.0 | 13.4 / 5.4 | hors \|'Arin | 2024 / 453 / 1257 / 3 | Tira-ñara / Tanāḥil ; 25 | Nrelat-q'urm (2200 m) à 124 km |
| `ZRS_SHALIM_NE` | 817 | 20.6 | 15.2 / 7.2 | hors \|'Arin | 2086 / 511 / 1198 / 6 | Tira-ñara / Tanāḥil ; 185 | Nrelat-q'urm (2200 m) à 197 km |
| `LUR_SARIQ_NE` | 236 | 18.3 | 8.5 / -1.7 | Hiver Jaune | 83 / 162 / 952 / 157 | — ; 0 | Qaṣūl-tɨra (2700 m) à 1515 km |
| `ZRS_HAMAD-RAS_NE` | 179 | 19.5 | 9.7 / -1.3 | Hiver de Vapeur | 2 / 187 / 886 / 147 | — ; 0 | Qaṣūl-tɨra (2700 m) à 1437 km |
| `AUX_QURASH-SAFIH` | 148 | 20.1 | 10.5 / -0.9 | Hiver de Vapeur | 2 / 272 / 822 / 49 | — ; 0 | Qaṣūl-tɨra (2700 m) à 1375 km |
| `LUR_ABNAQIL_NE` | 151 | 20.3 | 10.9 / -0.4 | Hiver de Vapeur | 23 / 360 / 781 / 2 | Abnīqa ; 4406 | Ṭanīkhūr (3200 m) à 1337 km |
| `LUR_ABNIQA_NE` | 139 | 20.4 | 11.0 / -0.5 | Hiver de Vapeur | 4 / 361 / 752 / 2 | Abnīqa ; 0 | Qaṣūl-tɨra (2700 m) à 1305 km |
| `LUR_TANAQIL_NE` | 141 | 20.6 | 11.2 / -0.2 | Hiver de Vapeur | 2 / 392 / 733 / 16 | Abnīqa ; 0 | Qaṣūl-tɨra (2700 m) à 1286 km |
| `LUR_QABSUR-QIBS_E` | 139 | 20.9 | 11.6 / 0.2 | Hiver de Vapeur | 2 / 464 / 678 / 70 | — ; 0 | Ṭanīkhūr (3200 m) à 1227 km |
| `LUR_HAWQIL_NE` | 165 | 21.5 | 12.6 / 1.4 | Hiver de Vapeur | 2 / 660 / 471 / 22 | \|Na-khuwel / Ḥawqal ; 1 | Ṭanīkhūr (3200 m) à 1014 km |
| `LUR_TANAHIL_NE` | 84 | 23.6 | 16.9 / 4.9 | hors \|'Arin | 1224 / 632 / 1019 / 0 | Tira-ñara / Tanāḥil ; 4064 | P'etsul-!ama (2600 m) à 579 km |
| `LUR_SHAFAQ-MIRQ_NE` | 301 | 18.7 | 8.4 / -0.9 | hiver pluvieux tempéré | 362 / 4 / 1225 / 36 | — ; 1 | Qaṣūl-tɨra (2700 m) à 1812 km |
| `LUR_TANQUISH_NE` | 372 | 18.9 | 8.7 / 0.4 | hiver pluvieux tempéré | 239 / 4 / 1116 / 66 | — ; 2 | Qaṣūl-tɨra (2700 m) à 1688 km |
| `AUX_MEDITERRANEE_NE` | 267 | 18.4 | 7.9 / -1.9 | hors \|'Arin | 410 / 0 / 1275 / 110 | — ; 0 | Qaṣūl-tɨra (2700 m) à 1864 km |
| `LUR_TNAYA-HAEM_SE` | 298 | 27.5 | 21.7 / 12.3 | hors \|'Arin | 2266 / 3 / 1743 / 36 | — ; 0 | ʿUbayl-t'iq (2000 m) à 488 km |
| `LUR_KURE-KESUN_SE` | 94 | 25.8 | 19.2 / 7.2 | hors \|'Arin | 1773 / 2 / 1589 / 222 | — ; 0 | ʿUbayl-t'iq (2000 m) à 106 km |
| `LUR_KURE-TAWA_SE` | 106 | 23.7 | 17.0 / 5.0 | hors \|'Arin | 1670 / 2 / 1558 / 229 | — ; 0 | Ḥazīr-k'ama (2100 m) à 82 km |
| `LUR_KUTEKA_SO` | 1344 | 22.7 | 17.3 / 9.3 | hors \|'Arin | 1884 / 362 / 2 / 6 | GEO_FLV_EMISSAIRE_MOPAMA ; 17 | Ku-Pámà-Tɨra-te (2000 m) à 500 km |
| `LUR_KUNGUMI_SO` | 1586 | 23.5 | 18.2 / 10.2 | hors \|'Arin | 1925 / 297 / 56 / 2 | GEO_FLV_EMISSAIRE_MOPAMA ; 49 | Ku-Pámà-Tɨra-te (2000 m) à 571 km |
| `LUR_KUBELAA_SO` | 2457 | 27.4 | 22.9 / 14.9 | hors \|'Arin | 2259 / 4 / 613 / 11 | GEO_FLV_EMISSAIRE_MOPAMA ; 2580 | Ku-Pámà-Tɨra-te (2000 m) à 1124 km |
| `LUR_MAZI-DUM_SO` | 2357 | 27.3 | 22.7 / 14.7 | hors \|'Arin | 2210 / 2 / 515 / 13 | GEO_FLV_EMISSAIRE_MOPAMA ; 2134 | Ku-Pámà-Tɨra-te (2000 m) à 1029 km |
| `ZRS_KUSALADI_SO` | 1732 | 22.7 | 17.3 / 9.3 | hors \|'Arin | 1909 / 395 / 4 / 89 | — ; 8 | Ku-Pámà-Tɨra-te (2000 m) à 449 km |
| `AUX_LISIERES_BALONGO` | 1565 | 23.9 | 18.7 / 10.7 | hors \|'Arin | 1955 / 359 / 53 / 35 | — ; 18 | Ku-Pámà-Tɨra-te (2000 m) à 491 km |
| `AUX_PIEMONTS_MUDARHOBI` | 1633 | 25.1 | 20.0 / 12.0 | hors \|'Arin | 1987 / 342 / 110 / 2 | — ; 375 | Ku-Pámà-Tɨra-te (2000 m) à 523 km |
| `AUX_DLT_MOPAMA` | 2334 | 27.4 | 22.8 / 14.8 | hors \|'Arin | 2223 / 2 / 554 / 13 | GEO_FLV_EMISSAIRE_MOPAMA ; 2363 | Ku-Pámà-Tɨra-te (2000 m) à 1066 km |
| `ZRS_KUUMANA_SO` | 1764 | 25.6 | 20.7 / 12.7 | hors \|'Arin | 2078 / 118 / 330 / 16 | GEO_FLV_EMISSAIRE_MOPAMA ; 12 | Ku-Pámà-Tɨra-te (2000 m) à 844 km |
| `ZRS_SAKUMADI_FORS` | 2154 | 21.6 | 17.0 / 9.0 | hors \|'Arin | 1934 / 1679 / 46 / 34 | — ; 38 | Šaqra-t'em (2400 m) à 695 km |
| `ZRS_KUPEPANA_FORS` | 2410 | 21.9 | 17.3 / 9.3 | hors \|'Arin | 1963 / 1586 / 80 / 28 | — ; 66 | Šaqra-t'em (2400 m) à 730 km |
| `LUR_KUBEKA_SC` | 1706 | 27.5 | 22.3 / 14.3 | hors \|'Arin | 1646 / 1745 / 0 / 90 | — ; 7 | Šaqra-t'em (2400 m) à 417 km |
| `LUR_KUPILA-MUSUKU_SC` | 1135 | 21.8 | 17.1 / 9.1 | hors \|'Arin | 1854 / 1522 / 2 / 53 | — ; 73 | Šaqra-t'em (2400 m) à 640 km |
| `LUR_KUKIBO_QESHA_SC` | 1162 | 20.2 | 15.4 / 7.4 | hors \|'Arin | 1852 / 1387 / 82 / 49 | — ; 31 | Šaqra-t'em (2400 m) à 680 km |
| `ZRS_KU-PILA-DI_SC` | 1122 | 27.5 | 22.7 / 14.7 | hors \|'Arin | 1813 / 1554 / 0 / 65 | — ; 3 | Šaqra-t'em (2400 m) à 596 km |
| `ZRS_KU-SUKU-NA_SC` | 1283 | 27.5 | 22.7 / 14.7 | hors \|'Arin | 1844 / 1619 / 0 / 59 | — ; 3 | Šaqra-t'em (2400 m) à 614 km |
| `ZRS_KU-LEMBE_SC` | 2250 | 27.5 | 22.4 / 14.4 | hors \|'Arin | 1715 / 1666 / 0 / 58 | — ; 10 | Kurel-ahek (2150 m) à 476 km |
| `ZRS_KU-ZABA_SC` | 2009 | 27.5 | 22.4 / 14.4 | hors \|'Arin | 1692 / 1752 / 0 / 88 | — ; 3 | Kurel-ahek (2150 m) à 463 km |
| `ZRS_MI-TONO_SC` | 1481 | 27.5 | 22.7 / 14.7 | hors \|'Arin | 1852 / 1788 / 0 / 103 | — ; 1 | Kurel-ahek (2150 m) à 613 km |
| `ZRS_KU-PELE-SO_SC` | 1383 | 21.1 | 15.9 / 7.9 | hors \|'Arin | 1624 / 1649 / 4 / 103 | — ; 19 | Šaqra-t'em (2400 m) à 410 km |
| `ZRS_KU-BANGA_SC` | 886 | 21.3 | 16.5 / 8.5 | hors \|'Arin | 1799 / 1459 / 4 / 31 | — ; 5 | Šaqra-t'em (2400 m) à 612 km |
| `ZRS_KU-NOMA_SC` | 2316 | 22.1 | 17.1 / 9.1 | hors \|'Arin | 1726 / 1624 / 4 / 64 | — ; 9 | P'etsul-!ama (2600 m) à 475 km |
| `ZRS_KUKANADI_SC` | 852 | 21.4 | 16.4 / 8.4 | hors \|'Arin | 1722 / 1505 / 4 / 61 | — ; 3 | Šaqra-t'em (2400 m) à 535 km |
| `LUR_BANNAKTI_NO` | 234 | 12.3 | 4.1 / -6.2 | Hiver Jaune | 558 / 633 / 1957 / 368 | — ; 0 | Hlenik-k'eso (2000 m) à 56 km |
| `LUR_TAMAR-KHU_CENTRE` | 1046 | 15.3 | 8.1 / 0.1 | Hiver Gris | 918 / 1227 / 772 / 100 | — ; 17 | Ku-Ténɨlkh-te (2300 m) à 51 km |
| `LUR_ZAGAKH-TIR_NE` | 676 | 15.7 | 7.5 / -0.5 | Hiver Gris | 90 / 1021 / 11 / 2 | \|Na-khuwel / Ḥawqal ; 5 | Qaṣūl-tɨra (2700 m) à 541 km |
| `LUR_URUM-SAMEL_CENTRE` | 103 | 1.6 | -6.1 / -18.1 | Hiver Blanc | 517 / 1176 / 369 / 211 | — ; 0 | Ṣabūl-tɨkh (2900 m) à 237 km |
| `LUR_UKH-SEK_CENTRE` | 3278 | 14.0 | 8.6 / 0.6 | Hiver Gris | 1851 / 929 / 691 / 38 | — ; 35 | T'amr-khɨna (2450 m) à 23 km |
| `LUR_ETHAK-KEL_CENTRE` | 3079 | 12.8 | 7.6 / -0.4 | Hiver Gris | 2006 / 879 / 825 / 31 | — ; 18 | T'araq-ɨnkh (2400 m) à 10 km |
| `LUR_TSIDAR-SEK_CENTRE` | 64 | 5.5 | -2.8 / -14.8 | Hiver Blanc | 376 / 1087 / 1540 / 234 | — ; 0 | Hlelak-!uri (2900 m) à 3 km |
| `LUR_GITES-TSIDAR_SE` | 3805 | 19.2 | 14.1 / 6.1 | hors \|'Arin | 2004 / 939 / 767 / 14 | — ; 90 | T'araq-ɨnkh (2400 m) à 53 km |
| `LUR_TSIDAR-RE_SE` | 2500 | 13.9 | 8.7 / 0.7 | Hiver Gris | 2054 / 854 / 872 / 21 | — ; 16 | Q'usa-\|\|ema (2100 m) à 20 km |
| `LUR_KUMAL-NAQRA_SE` | 94 | 15.0 | 8.8 / -3.2 | Hiver Jaune | 1842 / 194 / 1428 / 54 | — ; 0 | Ṣamar-q'ut (2200 m) à 108 km |
| `LUR_HAE-TSI-KURE_SE` | 703 | 16.2 | 10.6 / 2.6 | hors \|'Arin | 1574 / 1132 / 475 / 84 | — ; 10 | P'etsul-!ama (2600 m) à 40 km |
| `LUR_PI-KURE-NESHA_SE` | 106 | 12.2 | 5.6 / -6.3 | Hiver Jaune | 1661 / 63 / 1495 / 170 | — ; 0 | Ḥazīr-k'ama (2100 m) à 23 km |
| `LUR_HAE-PESHU_SE` | 98 | 16.2 | 9.7 / -2.3 | Hiver Jaune | 1703 / 80 / 1482 / 135 | — ; 0 | ʿUbayl-t'iq (2000 m) à 54 km |
| `LUR_QIREL-TSIDAR_SE` | 1368 | 16.4 | 11.1 / 3.1 | hors \|'Arin | 2037 / 770 / 946 / 14 | — ; 82 | T'iqur-ɨlkh (2700 m) à 73 km |
| `AUX_FOYERS-PURS` | 83 | 14.3 | 7.8 / -4.2 | Hiver Jaune | 1698 / 126 / 1437 / 94 | — ; 0 | Ṣamar-q'ut (2200 m) à 66 km |
| `AUX_VOIE-DESNUEES` | 227 | 11.8 | 5.8 / -4.5 | Hiver Jaune | 1874 / 339 / 1294 / 11 | Buhlela ; 7 | Nrelat-q'urm (2200 m) à 83 km |
| `AUX_VOIE-HAUTE` | 1078 | 16.3 | 10.7 / 2.7 | hors \|'Arin | 1619 / 1078 / 516 / 70 | — ; 11 | P'etsul-!ama (2600 m) à 110 km |
| `AUX_HAE-KUMEL` | 88 | 11.8 | 5.6 / -6.4 | Hiver Jaune | 1823 / 224 / 1381 / 5 | Buhlela ; 7 | Ṣamar-q'ut (2200 m) à 91 km |
| `AUX_KUKEDA-MUKIRI` | 2656 | 27.5 | 23.0 / 15.0 | hors \|'Arin | 2272 / 2 / 685 / 32 | — ; 40 | Ku-Pámà-Tɨra-te (2000 m) à 1189 km |
| `AUX_FORGES-DES-COQUES` | 2656 | 27.5 | 23.0 / 15.0 | hors \|'Arin | 2272 / 2 / 685 / 32 | — ; 40 | Ku-Pámà-Tɨra-te (2000 m) à 1189 km |
| `AUX_KISRALOM` | 283 | 20.0 | 10.5 / 0.9 | Hiver de Vapeur | 2 / 274 / 2246 / 109 | — ; 7 | Hlenik-k'eso (2000 m) à 628 km |
| `AUX_CERCLE-SANS-JURON` | 283 | 20.0 | 10.5 / 0.9 | Hiver de Vapeur | 2 / 274 / 2246 / 109 | — ; 7 | Hlenik-k'eso (2000 m) à 628 km |
| `AUX_DIMLAS` | 151 | 20.3 | 10.9 / -0.4 | Hiver de Vapeur | 23 / 360 / 781 / 2 | Abnīqa ; 4406 | Ṭanīkhūr (3200 m) à 1337 km |
| `AUX_VOIE-PURE` | 139 | 20.4 | 11.0 / -0.5 | Hiver de Vapeur | 4 / 361 / 752 / 2 | Abnīqa ; 0 | Qaṣūl-tɨra (2700 m) à 1305 km |
| `AUX_HAMUQAS` | 139 | 20.4 | 11.0 / -0.5 | Hiver de Vapeur | 4 / 361 / 752 / 2 | Abnīqa ; 0 | Qaṣūl-tɨra (2700 m) à 1305 km |
| `AUX_TAMA-ARA` | 1046 | 15.3 | 8.1 / 0.1 | Hiver Gris | 918 / 1227 / 772 / 100 | — ; 17 | Ku-Ténɨlkh-te (2300 m) à 51 km |
| `AUX_VOIE-COMPTABLE` | 106 | 12.2 | 5.6 / -6.3 | Hiver Jaune | 1661 / 63 / 1495 / 170 | — ; 0 | Ḥazīr-k'ama (2100 m) à 23 km |
| `AUX_PORTS-TNAYEL` | 298 | 27.5 | 21.7 / 12.3 | hors \|'Arin | 2266 / 3 / 1743 / 36 | — ; 0 | ʿUbayl-t'iq (2000 m) à 488 km |
| `AUX_SANUBE-MUSUKU` | 1283 | 27.5 | 22.7 / 14.7 | hors \|'Arin | 1844 / 1619 / 0 / 59 | — ; 3 | Šaqra-t'em (2400 m) à 614 km |
| `AUX_PORTS-EXTERNES-NO` | 447 | 17.4 | 6.4 / -1.6 | hors \|'Arin | 1484 / 0 / 3477 / 1110 | — ; 0 | Ku-Mázì-Klek-te (1900 m) à 1735 km |

### C. Lieux : expositions calculées et écarts avec le corpus

| ID | Nom | Expositions physiques calculées | Écarts (biomes et expositions du corpus non soutenus par le site) |
|---|---|---|---|
| `LUR_KHLORETH-KLAM_NO` | Khloreth-klam | tempêtes et houle de rivage | aucun |
| `LUR_STALOMAR-KOT_NO` | Stalomar-Kot | tempêtes et houle de rivage | aucun |
| `LUR_STAKHR-DUREK_NO` | Stakhr-Durek | — | biome « desert_sableux » — milieux calculés : herbage_arbore, steppe_piemont<br>exposition « Ensablement des pistes » — non soutenue par le site (ensablement)<br>exposition « tempêtes de sable » — non soutenue par le site (tempêtes) |
| `LUR_HLORAN-RIR_NO` | Hloran-rir | — | biome « oasis » — milieux calculés : herbage_arbore, steppe_piemont<br>exposition « Ensablement progressif de la résurgence principale en cas de sécheresse prolongée (>40 jours consécutifs sans rosée nocturne) » — non soutenue par le site (ensablement) |
| `ZRS_FALAMI_SKREN_PERIPH_NO` | Oase-Skren | — | biome « oasis » — milieux calculés : foret_montagne, herbage_arbore, steppe_piemont |
| `LUR_KU-JALIMA-RIR_SO` | Ku-jálima-rir | tempêtes et houle de rivage | aucun |
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
| `ZRS_SHALIM_NE` | Šālim | crues (lit majeur) | aucun |
| `LUR_SARIQ_NE` | Ṣarīq | — | aucun |
| `ZRS_HAMAD-RAS_NE` | Ḥamaḍ-Rās | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_ABNAQIL_NE` | Abnaqil | crues (lit majeur); brouillards d'évaporation (Hiver de Vapeur) | aucun |
| `LUR_ABNIQA_NE` | Abnīqa | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage; aridité (< 150 mm) | exposition « Ensablement bras secondaires » — non soutenue par le site (ensablement) |
| `LUR_TANAQIL_NE` | Tanāqil | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage; aridité (< 150 mm) | aucun |
| `LUR_QABSUR-QIBS_E` | Qabṣūr-Qibṣ | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage; aridité (< 150 mm) | aucun |
| `LUR_HAWQIL_NE` | Ḥawqil | brouillards d'évaporation (Hiver de Vapeur); tempêtes et houle de rivage | aucun |
| `LUR_TANAHIL_NE` | Tanāḥil | crues (lit majeur); aridité (< 150 mm) | exposition « Avalanches de redoux sur l'accès au col Abnī-tɨra » — non soutenue par le site (avalanches) |
| `LUR_SHAFAQ-MIRQ_NE` | Šafāq-Mirq | tempêtes et houle de rivage | exposition « ensablement des bouches » — non soutenue par le site (ensablement) |
| `LUR_TANQUISH_NE` | Ṭanquish | tempêtes et houle de rivage | biome « depression_saline » — milieux calculés : fourre_cotier_sec, océan, plaine_alluviale |
| `LUR_TNAYA-HAEM_SE` | T'naya-Ḥaem | tempêtes et houle de rivage; éboulements, glissements (versants raides) | aucun |
| `LUR_KURE-KESUN_SE` | K'uré-K’ésun | tempêtes et houle de rivage; aridité (< 150 mm) | aucun |
| `LUR_KURE-TAWA_SE` | K'uré-tawa | tempêtes et houle de rivage; aridité (< 150 mm) | aucun |
| `LUR_KUTEKA_SO` | Kù-téka | — | exposition « Ensablement saisonnier de l'émissaire » — non soutenue par le site (ensablement) |
| `LUR_KUNGUMI_SO` | Ku-Ngúmi | — | biome « zone_humide_lacustre » — milieux calculés : foret_tropicale_humide, herbage_arbore |
| `LUR_KUBELAA_SO` | Kù-Bèláà | tempêtes et houle de rivage | aucun |
| `LUR_MAZI-DUM_SO` | Mázì-Dúm | tempêtes et houle de rivage | biome « foret_maree » — milieux calculés : foret_tropicale_humide, océan |
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
| `LUR_UKH-SEK_CENTRE` | \|'Ukh-\|\|Sék | avalanches / chutes de pierres (\|'Arin); éboulements, glissements (versants raides) | biome « prairie_altitude » — milieux calculés : foret_montagne, foret_tropicale_humide |
| `LUR_ETHAK-KEL_CENTRE` | \|\|Ethak-Kél-Ts'idar | avalanches / chutes de pierres (\|'Arin) | aucun |
| `LUR_TSIDAR-SEK_CENTRE` | Ts'idar-‖Sek | avalanches / chutes de pierres (\|'Arin); hypoxie légère (> 2 500 m); Hiver Blanc : neige et gel durables; aridité (< 150 mm) | aucun |
| `LUR_GITES-TSIDAR_SE` | Gîtes-Ts'idar | — | exposition « blocages par avalanches en amont » — non soutenue par le site (avalanches) |
| `LUR_TSIDAR-RE_SE` | Ts'idar-ré | avalanches / chutes de pierres (\|'Arin) | aucun |
| `LUR_KUMAL-NAQRA_SE` | K'umal-Naqra | aridité (< 150 mm) | aucun |
| `LUR_HAE-TSI-KURE_SE` | Hae Ts'i-K'uré | — | exposition « Hypoxie/froid (saison \|'Arin-sukhì) » — non soutenue par le site (hypoxie) |
| `LUR_PI-KURE-NESHA_SE` | P'i-K'uré-Neša | aridité (< 150 mm) | aucun |
| `LUR_HAE-PESHU_SE` | Hae-P'ešu | aridité (< 150 mm) | aucun |
| `LUR_QIREL-TSIDAR_SE` | Q'irel-Ts'idar | — | exposition « Sécheresses prolongées » — non soutenue par le site (sécheresses) |

### D. Routes : tracé calculé

Tracé le plus rapide sur la carte (grille ≈ 5 km), dans les modes déclarés par la route. Un milieu absent des modes déclarés n'est emprunté que s'il est inévitable (colonne « hors modes »).

| ID | Route | Modes déclarés | Longueur (vol d'oiseau) km | Durée (j) | km par milieu | Hors modes déclarés (km) | Ruptures de charge | Altitude max / D+ (m) | Cols franchis ; mois ouverts |
|---|---|---|---|---|---|---|---|---|---|
| `RT_001` | Kù-békà ↔ Kù-téka | terrestre_caravane | 2439 (2170) | 84.0 | terre 2435 | — | 1 | 1266 / 2460 | — |
| `RT_002` | Abnaqil ↔ Kralekh-ner | maritime_cabotage | 3430 (2992) | 47.0 | mer Halakhel 3405, terre 22 | terre 19 | 1 | 29 / 2 | — |
| `RT_003` | Kù-téka ↔ Ku-jálima-rir | fluvial, maritime_cabotage | 847 (698) | 22.0 | océan 23, lac 5, fleuve (aval) 485, fleuve (amont) 144, terre 176 | terre 162 | 4 | 799 / 142 | — |
| `RT_004` | Tawālmaz ↔ Khloreth-klam | maritime_cabotage, terrestre_portage | 2706 (2390) | 47.0 | mer Halakhel 2416, terre 286 | — | 1 | 1232 / 1406 | — |
| `RT_005` | Serékh-khem ↔ Kralekh-ner | maritime_cabotage | 59 (59) | 1.3 | mer Halakhel 49, terre 7 | — | 1 | -20 / 7 | — |
| `RT_006` | Abnī-tɨra ↔ Tanāḥil | col_haute_altitude, terrestre_caravane | 936 (922) | 32.0 | terre 936 | — | 0 | 2515 / 1377 | Abnī-tɨra (001, 2800 m) ; juin → oct |
| `RT_007` | Tanāḥil ↔ Ports T'nayel SE | fluvial, maritime_cabotage | 4348 (1198) | 74.0 | océan 2118, fleuve (aval) 2071, fleuve (amont) 7, terre 145 | terre 138 | 2 | 623 / 596 | — |
| `RT_008` | Ṭanquish ↔ Méditerranée NE | maritime_cabotage | 185 (177) | 2.9 | océan 181, terre 2 | — | 1 | -1 / 0 | — |
| `RT_009` | \|'Ukh-\|\|Sék ↔ Q'irel-Ts'idar | terrestre_portage | 325 (275) | 19.0 | terre 325 | — | 0 | 2370 / 1829 | T'araq-ɨnkh (010, 2400 m); T'amr-khɨna (017, 2450 m) ; mai → oct |
| `RT_010` | Tanāḥil ↔ Kù-békà | col_haute_altitude, fluvial, lacustre, terrestre_caravane, terrestre_portage | 1257 (1139) | 39.0 | lac 70, fleuve (aval) 5, fleuve (amont) 276, terre 903 | — | 1 | 1693 / 2571 | — |
| `RT_011` | Talom-ak ↔ Kot-Skral | maritime_hauturier | 2109 (2055) | 16.0 | océan 2099, terre 5 | — | 2 | 365 / 0 | — |
| `RT_012` | Abnīqa ↔ Abnaqil | fluvial, maritime_cabotage | 58 (54) | 1.4 | fleuve (aval) 30, fleuve (amont) 21, terre 7 | terre 7 | 0 | 30 / 45 | — |
| `RT_013` | Ḥawqil ↔ Abnaqil | fluvial, maritime_cabotage | 370 (323) | 6.5 | mer Halakhel 298, fleuve (aval) 30, fleuve (amont) 27, terre 9 | — | 2 | 30 / 28 | — |
| `RT_014` | Abnīqa ↔ Tanāqil | fluvial, maritime_cabotage | 77 (32) | 1.5 | mer Halakhel 72, terre 2 | — | 1 | -10 / 0 | — |
| `RT_015` | Tanāqil ↔ Abnaqil | maritime_cabotage | 163 (54) | 3.0 | mer Halakhel 138, terre 22 | terre 19 | 1 | 29 / 26 | — |
| `RT_016` | Imekh-stom ↔ Tawālmaz | maritime_cabotage | 1700 (1380) | 23.0 | mer Halakhel 1700 | — | 0 | None / 0 | — |
| `RT_017` | Aktrik-khem ↔ Dimlāš | fluvial, maritime_cabotage | 3776 (3422) | 52.0 | mer Halakhel 3730, fleuve (aval) 13, terre 26 | terre 21 | 2 | 30 / 59 | — |
| `RT_018` | Imekh-stom ↔ Khloreth-klam | maritime_cabotage, terrestre_portage | 1209 (1090) | 27.0 | mer Halakhel 920, terre 286 | — | 1 | 1232 / 1406 | — |
| `RT_019` | Q'usa-\|\|ema ↔ Ts'idar-ré | col_haute_altitude | 20 (20) | 1.3 | terre 20 | — | 0 | 2192 / 115 | Q'usa-\|\|ema (016, 2100 m) ; avr → nov |
| `RT_020` | Kù-kèdà yì Mù-Kíri ↔ Ts'idar-ré | col_haute_altitude, maritime_cabotage | 4473 (3907) | 184.0 | océan 1181, lac 507, terre 2771 | — | 4 | 2305 / 8588 | — |
| `RT_021` | \|'Urum-‖Sek ↔ Dimlāš | col_haute_altitude, terrestre_caravane | 2189 (2050) | 75.0 | terre 2189 | — | 0 | 2243 / 2003 | — |
| `RT_022` | Qūrāš-Ṣafīḥ ↔ Ḥamaḍ-Rās | maritime_cabotage | 107 (99) | 1.9 | mer Halakhel 102, terre 2 | — | 1 | 26 / 0 | — |
| `RT_023` | Tawālmaz ↔ Abnaqil | maritime_cabotage | 1769 (1503) | 24.0 | mer Halakhel 1744, terre 22 | terre 19 | 1 | 29 / 26 | — |
| `RT_024` | !Tama-\|'Ara ↔ Dimlāš | col_haute_altitude, terrestre_caravane | 3071 (2734) | 105.0 | terre 3071 | — | 0 | 1743 / 6263 | — |
| `RT_025` | Hae Ts'i-K'uré ↔ \|'Urum-‖Sek | col_haute_altitude | 421 (358) | 24.0 | terre 421 | — | 0 | 2243 / 3304 | — |
| `RT_026` | Gîtes-Ts'idar ↔ Ts'idar-ré | col_haute_altitude | 110 (106) | 8.1 | terre 110 | — | 0 | 2192 / 1915 | — |
| `RT_027` | Khloreth-klam ↔ Kralekh-Aktrik | terrestre_portage | 291 (291) | 14.0 | terre 291 | — | 0 | 1232 / 1373 | — |
| `RT_028` | Qabṣūr-Qibṣ ↔ Abnaqil | terrestre_caravane | 123 (111) | 4.8 | terre 120 | — | 1 | 57 / 232 | — |
| `RT_029` | Piémonts du Mù-dárhòbì ↔ Kù-békà | fluvial, lacustre, terrestre_portage | 2326 (2000) | 81.0 | lac 322, fleuve (aval) 276, fleuve (amont) 705, terre 1018 | — | 1 | 1076 / 2529 | — |
| `RT_030` | Qabṣūr-Qibṣ ↔ Tanāḥil | fluvial | 2748 (1308) | 58.0 | mer Halakhel 48, fleuve (aval) 11, fleuve (amont) 2658, terre 15 | mer 48 | 5 | 378 / 408 | — |
| `RT_031` | Gîtes-Ts'idar ↔ Tanāḥil | fluvial | 994 (798) | 23.0 | fleuve (aval) 765, fleuve (amont) 5, terre 223 | terre 223 | 0 | 1977 / 1684 | — |
| `RT_032` | Foyers-Purs ↔ Voie-Pure-des-Vallées | fluvial, maritime_cabotage | 2726 (1799) | 46.0 | mer Halakhel 93, océan 1861, fleuve (aval) 291, fleuve (amont) 223, terre 246 | terre 233 | 4 | 2068 / 842 | — |
| `RT_033` | Forges-des-Coques ↔ Cercle-Sans-Juron | maritime_cabotage | 5012 (2624) | 74.0 | mer Halakhel 18, océan 4689, terre 292 | terre 280 | 4 | 650 / 487 | — |
| `RT_034` | Voie-Desnuées ↔ Foyers-Purs | col_haute_altitude, maritime_cabotage | 259 (247) | 14.0 | terre 259 | — | 0 | 2517 / 2316 | — |
| `RT_035` | Akhileth ↔ Imekh-stom | fluvial, maritime_cabotage | 135 (126) | 3.7 | mer Halakhel 53, fleuve (amont) 5, terre 74 | terre 72 | 1 | 397 / 1 | — |
| `RT_036` | K'uré-tawa ↔ Abnaqil | fluvial, maritime_cabotage | 2436 (1719) | 39.0 | océan 1843, fleuve (aval) 260, fleuve (amont) 213, terre 114 | terre 109 | 2 | 441 / 538 | — |
| `RT_037` | Kù-kèdà yì Mù-Kíri ↔ Aktrik-khem | maritime_cabotage, terrestre_caravane | 5159 (2586) | 77.0 | mer Halakhel 167, océan 4661, terre 317 | — | 4 | 681 / 708 | — |
| `RT_038` | S'akum-\|ena ↔ K'uré-tawa | col_haute_altitude, maritime_cabotage | 1055 (977) | 57.0 | terre 1055 | — | 0 | 2177 / 5552 | S'akum-\|ena (015, 2200 m); Ṣamar-q'ut (046, 2200 m) ; avr → nov |
| `RT_039` | Kralekh-ner ↔ Qūrāš-Ṣafīḥ | maritime_cabotage | 3308 (2925) | 44.0 | mer Halakhel 3308 | — | 0 | None / 0 | — |
| `RT_040` | Qabḍ-ār-Ǧanūb ↔ Khloreth-klam | maritime_cabotage, terrestre_portage | 3707 (3259) | 61.0 | mer Halakhel 3408, terre 293 | — | 2 | 1232 / 1421 | — |
| `RT_041` | Serékh-khem ↔ Qūrāš-Ṣafīḥ | maritime_cabotage | 3366 (2912) | 45.0 | mer Halakhel 3357, terre 7 | — | 1 | -20 / 7 | — |
| `RT_042` | Ku-jálima-rir ↔ Ports externes NO | maritime_hauturier | 5123 (3922) | 35.0 | océan 5117, terre 3 | — | 1 | -16 / 0 | — |
| `RT_043` | Bannaktì ↔ Ts'idar-‖Sek | col_haute_altitude, terrestre_caravane | 819 (724) | 31.0 | terre 819 | — | 0 | 2842 / 7834 | Hlelak-!uri (032, 2900 m) ; juin → sep |
| `RT_044` | Ts'idar-‖Sek ↔ Cherbekh-khem | col_haute_altitude, terrestre_caravane | 618 (577) | 22.0 | terre 615 | — | 1 | 2842 / 1799 | Hlelak-!uri (032, 2900 m); Kraloth-!enu (035, 2700 m) ; juin → sep |
| `RT_045` | Foyers-Purs ↔ K'uré-tawa | col_haute_altitude, maritime_cabotage | 147 (137) | 7.1 | terre 147 | — | 0 | 2068 / 189 | — |
| `RT_046` | Imekh-stom ↔ Ku-jálima-rir | maritime_cabotage | 5941 (2223) | 87.0 | mer Halakhel 933, océan 4712, terre 285 | terre 275 | 3 | 763 / 1087 | — |
| `RT_047` | Kù-békà ↔ Ku-jálima-rir | fluvial, lacustre, maritime_cabotage | 3857 (2751) | 71.0 | océan 1075, lac 200, fleuve (aval) 1813, fleuve (amont) 313, terre 446 | terre 437 | 3 | 1220 / 527 | — |
| `RT_048` | Voie-Haute ↔ Hae Ts'i-K'uré | col_haute_altitude | 74 (73) | 4.4 | terre 74 | — | 0 | 1839 / 964 | — |
| `RT_049` | Voie-Comptable ↔ Kisralom | maritime_cabotage | 6363 (4983) | 93.0 | mer Halakhel 3618, océan 2410, terre 317 | terre 300 | 6 | 2031 / 325 | — |
| `RT_050` | Cherbekh-khem ↔ Imekh-stom | maritime_cabotage, terrestre_caravane | 379 (229) | 5.0 | mer Halakhel 379 | — | 0 | None / 0 | — |
| `RT_051` | Bannaktì ↔ Cherbekh-khem | terrestre_caravane | 1357 (1255) | 47.0 | terre 1353 | — | 1 | 2016 / 4389 | Hlenik-k'eso (038, 2000 m) ; avr → nov |
| `RT_052` | T'naya-Ḥaem ↔ Q'irel-Ts'idar | terrestre_caravane, terrestre_portage | 875 (812) | 33.0 | terre 875 | — | 0 | 2514 / 6288 | — |
| `RT_053` | Ṣarīq ↔ \|\|Ethak-Kél-Ts'idar | terrestre_caravane | 2501 (2335) | 87.0 | terre 2501 | — | 0 | 2386 / 4468 | T'araq-ɨnkh (010, 2400 m) ; mai → oct |
| `RT_054` | Ku-jálima-rir ↔ Jáli-Fè | maritime_cabotage | 130 (111) | 2.6 | océan 117, terre 6 | — | 2 | 14 / 0 | — |
| `RT_055` | Jáli-Fè ↔ Anses-Jálondù | maritime_cabotage | 239 (211) | 3.6 | océan 232, terre 4 | — | 1 | 14 / 0 | — |
| `RT_056` | Talom-ak ↔ Kisralom | maritime_cabotage | 321 (275) | 12.0 | mer Halakhel 18, terre 291 | terre 279 | 4 | 643 / 447 | — |
| `RT_057` | Talom-ak ↔ Ku-jálima-rir | maritime_hauturier | 4812 (2828) | 34.0 | océan 4802, terre 5 | — | 2 | 365 / 0 | — |
| `RT_058` | Kisralom ↔ Serékh-khem | maritime_cabotage | 765 (636) | 11.0 | mer Halakhel 752, terre 9 | — | 2 | 26 / 0 | — |
| `RT_059` | Ku-Ngúmi ↔ Estuaire Mopámà | fluvial | 673 (498) | 18.0 | océan 15, fleuve (aval) 383, fleuve (amont) 123, terre 145 | mer 15, terre 137 | 2 | 693 / 149 | — |
| `RT_060` | Kù-Bèláà ↔ Ku-jálima-rir | fluvial | 84 (82) | 2.8 | océan 58, terre 13 | mer 58 | 4 | 14 / 0 | — |
| `RT_061` | Ts'idar-‖Sek ↔ K'elis-‖ara | col_haute_altitude | 4200 (3909) | 216.0 | terre 4200 | — | 0 | 2842 / 10683 | K'elis-‖ara (011, 2500 m); Hlelak-!uri (032, 2900 m); Krathal-t'iq (041, 2300 m) ; juin → sep |
| `RT_062` | Gîtes-Ts'idar ↔ \|\|Ethak-Kél-Ts'idar | terrestre_caravane | 71 (63) | 3.8 | terre 71 | — | 0 | 2386 / 1286 | T'araq-ɨnkh (010, 2400 m) ; mai → oct |
| `RT_063` | Qūrāš-Tanīqa ↔ K'umal-Naqra | terrestre_caravane | 360 (331) | 13.0 | terre 360 | — | 0 | 2730 / 1856 | — |
| `RT_064` | Abnī-tɨra ↔ Zagakh-TƗr | col_haute_altitude | 815 (766) | 43.0 | terre 815 | — | 0 | 2515 / 1418 | Abnī-tɨra (001, 2800 m) ; juin → oct |
| `RT_065` | Hae Ts'i-K'uré ↔ P'etsul-!ama | terrestre_caravane | 42 (40) | 1.9 | terre 42 | — | 0 | 2397 / 736 | P'etsul-!ama (013, 2600 m) ; mai → oct |
| `RT_066` | Kot-Skral ↔ Bannaktì | maritime_hauturier, terrestre_caravane | 2106 (1770) | 34.0 | océan 1422, terre 677 | — | 2 | 1262 / 1493 | — |
| `RT_067` | K'umal-Naqra ↔ K'uré-K'ésun | col_haute_altitude | 215 (201) | 11.0 | terre 215 | — | 0 | 2472 / 684 | — |
| `RT_068` | Gîtes-Ts'idar ↔ Q'eša-Kɨ́bò | terrestre_caravane | 1718 (1386) | 63.0 | terre 1718 | — | 0 | 1912 / 6232 | T'amr-khɨna (017, 2450 m) ; mai → oct |
| `RT_069` | Ku-Pɨla-Mù-Sùkú ↔ Q'eša-Kɨ́bò | lacustre, terrestre_portage | 220 (143) | 6.6 | lac 126, terre 90 | — | 1 | 1178 / 238 | — |
| `RT_070` | Lisières Ba-lóngó ↔ Q'eša-Kɨ́bò | terrestre_caravane | 1846 (1736) | 65.0 | terre 1846 | — | 0 | 1178 / 3646 | — |
| `RT_071` | Šālim ↔ Abnīqa | fluvial | 3832 (2195) | 73.0 | fleuve (aval) 3665, fleuve (amont) 60, terre 106 | terre 106 | 0 | 1146 / 348 | — |
| `RT_072` | Sa-nùbè yì Mù-Sùkú ↔ Talom-ak | fluvial, maritime_cabotage | 9368 (4347) | 156.0 | océan 4580, lac 387, fleuve (aval) 4079, fleuve (amont) 122, terre 184 | terre 167 | 5 | 1529 / 1315 | — |
| `RT_073` | \|'Urum-‖Sek ↔ Ḥamūqaš | col_haute_altitude, terrestre_caravane | 2217 (2068) | 76.0 | terre 2217 | — | 0 | 2243 / 2171 | — |
| `RT_074` | Hae K'umel ↔ Talom-ak | maritime_cabotage | 7149 (5324) | 104.0 | océan 6774, terre 363 | terre 352 | 4 | 2369 / 1110 | ʿUbayl-t'iq (044, 2000 m) ; avr → nov |

### E. Routes : milieux et hivers traversés (voies de terre)

| ID | Milieux traversés (km) | Faciès \|'Arin traversés (km) |
|---|---|---|
| `RT_001` | herbage_arbore 1158, steppe_piemont 1127, desert_pierreux 78, foret_tropicale_humide 47 | hors \|'Arin 2439 |
| `RT_002` | — | — |
| `RT_003` | foret_tropicale_humide 672, herbage_arbore 83, foret_maree 28, zone_humide_lacustre 20 | hors \|'Arin 803 |
| `RT_004` | steppe_piemont 143, fourre_cotier_sec 57, foret_montagne 52, herbage_arbore 37 | Hiver Gris 147, hiver pluvieux tempéré 122 |
| `RT_005` | — | — |
| `RT_006` | steppe_piemont 679, desert_pierreux 236, plaine_alluviale 21 | hors \|'Arin 913, Hiver Jaune 23 |
| `RT_007` | plaine_alluviale 2063, desert_pierreux 133, desert_sableux 20 | hors \|'Arin 2034, Hiver Jaune 190 |
| `RT_008` | — | — |
| `RT_009` | foret_montagne 305, steppe_piemont 20 | hors \|'Arin 229, Hiver Gris 96 |
| `RT_010` | desert_pierreux 519, herbage_arbore 293, steppe_piemont 238, foret_berge 102 | hors \|'Arin 1180 |
| `RT_011` | — | — |
| `RT_012` | plaine_alluviale 58 | Hiver de Vapeur 53 |
| `RT_013` | plaine_alluviale 67 | Hiver de Vapeur 62 |
| `RT_014` | — | — |
| `RT_015` | plaine_alluviale 25 | Hiver de Vapeur 25 |
| `RT_016` | — | — |
| `RT_017` | plaine_alluviale 27 | Hiver de Vapeur 41 |
| `RT_018` | steppe_piemont 143, fourre_cotier_sec 57, foret_montagne 52, herbage_arbore 37 | Hiver Gris 147, hiver pluvieux tempéré 122 |
| `RT_019` | foret_montagne 20 | Hiver Gris 20 |
| `RT_020` | herbage_arbore 1970, foret_tropicale_humide 422, foret_montagne 195, steppe_piemont 168 | hors \|'Arin 2679, Hiver Gris 93 |
| `RT_021` | desert_pierreux 1593, steppe_piemont 270, plaine_alluviale 179, foret_montagne 62, herbage_arbore 59 | hors \|'Arin 1587, Hiver Jaune 591 |
| `RT_022` | — | — |
| `RT_023` | plaine_alluviale 25 | Hiver de Vapeur 25 |
| `RT_024` | steppe_piemont 1727, desert_pierreux 1048, herbage_arbore 160, plaine_alluviale 73, foret_montagne 39, depression_saline 25 | hors \|'Arin 1579, Hiver Jaune 1089, Hiver de Vapeur 324, Hiver Gris 79 |
| `RT_025` | herbage_arbore 309, foret_montagne 61, foret_tropicale_humide 27 | hors \|'Arin 405 |
| `RT_026` | foret_montagne 97 | hors \|'Arin 83, Hiver Gris 26 |
| `RT_027` | steppe_piemont 130, foret_montagne 52, fourre_cotier_sec 50, herbage_arbore 46 | Hiver Gris 143, hiver pluvieux tempéré 116, Hiver de Vapeur 33 |
| `RT_028` | depression_saline 43, desert_pierreux 43, plaine_alluviale 38 | Hiver de Vapeur 105 |
| `RT_029` | foret_berge 842, herbage_arbore 622, steppe_piemont 464, foret_tropicale_humide 60 | hors \|'Arin 1996 |
| `RT_030` | plaine_alluviale 2654, desert_sableux 22 | hors \|'Arin 2075, Hiver Jaune 572, Hiver de Vapeur 43 |
| `RT_031` | plaine_alluviale 641, foret_montagne 147, foret_berge 122, herbage_arbore 62, steppe_piemont 22 | hors \|'Arin 994 |
| `RT_032` | plaine_alluviale 532, desert_pierreux 117, fourre_cotier_sec 81, steppe_piemont 28 | Hiver Jaune 526, Hiver Gris 115, hors \|'Arin 85, Hiver de Vapeur 32 |
| `RT_033` | steppe_piemont 145, herbage_arbore 135 | Hiver Gris 188, hiver pluvieux tempéré 72, Hiver de Vapeur 25 |
| `RT_034` | desert_pierreux 172, steppe_piemont 87 | Hiver Jaune 247 |
| `RT_035` | steppe_piemont 34, desert_pierreux 24 | hors \|'Arin 43, Hiver de Vapeur 24 |
| `RT_036` | plaine_alluviale 493, fourre_cotier_sec 81 | Hiver Jaune 427, Hiver Gris 115, hors \|'Arin 34 |
| `RT_037` | herbage_arbore 155, steppe_piemont 141, desert_pierreux 21 | Hiver Gris 246, Hiver de Vapeur 40, hiver pluvieux tempéré 23 |
| `RT_038` | steppe_piemont 291, herbage_arbore 287, desert_pierreux 259, foret_montagne 205 | hors \|'Arin 671, Hiver Jaune 328, Hiver Gris 57 |
| `RT_039` | — | — |
| `RT_040` | steppe_piemont 143, fourre_cotier_sec 57, foret_montagne 52, herbage_arbore 37 | Hiver Gris 147, hiver pluvieux tempéré 122, Hiver de Vapeur 25 |
| `RT_041` | — | — |
| `RT_042` | — | — |
| `RT_043` | steppe_piemont 494, desert_pierreux 283, prairie_altitude 35 | Hiver Jaune 715, hors \|'Arin 71, Hiver Blanc 33 |
| `RT_044` | steppe_piemont 216, desert_pierreux 205, plaine_alluviale 85, prairie_altitude 70, littoral_rocheux 21 | Hiver Jaune 204, hors \|'Arin 168, Hiver de Vapeur 123, Hiver Blanc 116 |
| `RT_045` | desert_pierreux 78, steppe_piemont 61 | Hiver Jaune 98, hors \|'Arin 49 |
| `RT_046` | steppe_piemont 129, herbage_arbore 94, fourre_cotier_sec 49 | Hiver Gris 129, hiver pluvieux tempéré 126 |
| `RT_047` | foret_berge 1230, foret_tropicale_humide 714, steppe_piemont 405, herbage_arbore 174, zone_humide_lacustre 48 | hors \|'Arin 2576 |
| `RT_048` | herbage_arbore 57 | hors \|'Arin 74 |
| `RT_049` | fourre_cotier_sec 231, desert_pierreux 39, steppe_piemont 34 | hiver pluvieux tempéré 135, Hiver Gris 64, Hiver Jaune 45, hors \|'Arin 42, Hiver de Vapeur 29 |
| `RT_050` | — | — |
| `RT_051` | steppe_piemont 748, desert_pierreux 481, plaine_alluviale 89, littoral_rocheux 21 | Hiver Jaune 1012, hors \|'Arin 197, Hiver de Vapeur 142 |
| `RT_052` | steppe_piemont 456, herbage_arbore 255, foret_montagne 99, desert_pierreux 28 | hors \|'Arin 718, Hiver Gris 145 |
| `RT_053` | desert_pierreux 1288, plaine_alluviale 564, steppe_piemont 339, foret_montagne 142, herbage_arbore 113, depression_saline 40 | hors \|'Arin 1891, Hiver Jaune 573, Hiver Gris 37 |
| `RT_054` | — | — |
| `RT_055` | — | — |
| `RT_056` | steppe_piemont 134, herbage_arbore 109, fourre_cotier_sec 32 | Hiver Gris 178, hiver pluvieux tempéré 80, Hiver de Vapeur 25 |
| `RT_057` | — | — |
| `RT_058` | — | — |
| `RT_059` | foret_tropicale_humide 587, herbage_arbore 51 | hors \|'Arin 651 |
| `RT_060` | — | — |
| `RT_061` | steppe_piemont 2710, desert_pierreux 900, herbage_arbore 467, foret_montagne 92, prairie_altitude 24 | hors \|'Arin 3089, Hiver Jaune 885, Hiver Gris 203, Hiver Blanc 24 |
| `RT_062` | foret_montagne 63 | hors \|'Arin 45, Hiver Gris 25 |
| `RT_063` | steppe_piemont 294, desert_pierreux 38 | Hiver Jaune 240, hors \|'Arin 67, Hiver Gris 52 |
| `RT_064` | steppe_piemont 396, desert_pierreux 171, foret_montagne 130, herbage_arbore 99 | Hiver Jaune 288, Hiver Gris 285, hors \|'Arin 242 |
| `RT_065` | — | Hiver Gris 22 |
| `RT_066` | steppe_piemont 469, herbage_arbore 208 | hors \|'Arin 648, Hiver Jaune 29 |
| `RT_067` | desert_pierreux 107, steppe_piemont 82 | Hiver Jaune 140, hors \|'Arin 76 |
| `RT_068` | herbage_arbore 1235, steppe_piemont 215, foret_montagne 210, foret_tropicale_humide 40 | hors \|'Arin 1713 |
| `RT_069` | herbage_arbore 93 | hors \|'Arin 93 |
| `RT_070` | herbage_arbore 1006, steppe_piemont 757, foret_tropicale_humide 65 | hors \|'Arin 1846 |
| `RT_071` | plaine_alluviale 3260, foret_berge 414, herbage_arbore 114, foret_montagne 23, desert_sableux 20 | hors \|'Arin 3219, Hiver Jaune 551, Hiver de Vapeur 62 |
| `RT_072` | plaine_alluviale 2834, foret_tropicale_humide 789, desert_pierreux 381, steppe_piemont 183, foret_berge 73, foret_montagne 67, herbage_arbore 35, desert_sableux 20 | hors \|'Arin 3599, Hiver Jaune 541, hiver pluvieux tempéré 192, Hiver Gris 55 |
| `RT_073` | desert_pierreux 1558, steppe_piemont 270, plaine_alluviale 214, foret_montagne 62, herbage_arbore 59, depression_saline 21 | hors \|'Arin 1650, Hiver Jaune 469, Hiver de Vapeur 92 |
| `RT_074` | desert_pierreux 169, fourre_cotier_sec 119, steppe_piemont 59 | Hiver Jaune 205, Hiver Gris 64, hiver pluvieux tempéré 59, hors \|'Arin 33 |

### F. Variantes imposées par une indication du corpus

| ID | Étapes imposées | Longueur km | Durée (j) | Altitude max (m) | Cols franchis ; mois ouverts | Écart avec le tracé optimal |
|---|---|---|---|---|---|---|
| `RT_010` | GEO_COL_014 | 2614 | 69.0 | 2624 | T'iqur-ɨlkh (014, 2700 m) ; juin → oct | +1357 km, +30.0 j |
| `RT_027` | LUR_STAKHR-DUREK_NO | 302 | 15.0 | 1232 | — ; — | +11 km, +1.0 j |
| `RT_066` | LUR_STALOMAR-KOT_NO | 2924 | 44.0 | 1347 | — ; — | +818 km, +10.0 j |

<!-- GENERE:FIN -->
