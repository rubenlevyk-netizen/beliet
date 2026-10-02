# Analyse de cohérence — carte du Beliet v0.2

Sources lues : `references/GEOSYSTEME_GLOBAL_DU_BELIET_v3.1.md`, `references/GEOSYSTEME_REGISTRE.v1.json` (132 entrées), `references/MAP_BELIET_ORIGIN.svg`. Depuis la v0.2, s'y ajoutent `LIEUX_URBAINS.v2.json` (56 lieux, 18 zones secondaires), `RESEAU_ROUTES.v3.json` (74 routes) et `PORTFOLIO_RESSOURCES.v2.json` (111 ressources). L'illustration `TEST_Beliet_MAP.png` n'a servi que d'orientation qualitative, jamais de base géométrique.

## 0. Changements de la v0.2

| Point | v0.1 | v0.2 | Raison |
|---|---|---|---|
| Mer Halakhel | 23,5-31,5° N, de 6° à 28° E | 22,5-28° N, de -11,5° à 28° E ; lobe occidental dans la région NO | demande de l'auteur ; portage NO → Atlantique (RT_027, RT_018) ; §V.1 « E : Mer Halakhel occidentale » |
| Rive sud | glacis | rocheuse, la cordillère touche la mer | LIEUX : Tawālmaz, Cherbekh-khem, Qabḍ-ār-Ǧanūb en `littoral_rocheux` ; Akhileth en `littoral_rocheux` + `foret_montagne` |
| Cordillère | halekh, k'ara et lóngò décalés vers le nord | arc continu vers 20-21° N, nœud !Okheti à 6° O | halekh retrouve ses ~1 200 km canoniques ; lóngò ses ~1 800 km |
| halekh | intérieur mauritanien | atteint la côte face à Staur-Khlōr | RT_066 Kot-Skral ↔ Bannaktì (mer puis caravane) |
| Bras des chotts | présent | supprimé | la mer ne borde plus la Méditerranée |
| Limite sud | frontières politiques réelles | limite lissée, irrégulière, estompée sur ~300 km | demande de l'auteur |
| Façade atlantique SO | golfe de Guinée | côte de Guinée-Bissau et de Guinée | Staur-Khlōr « à ~600 km de la façade SO » = Cap-Vert ; demande de l'auteur |
| Ku-jálima-rir, golfe Jálondù, Li-sèk-dì | baie du Bénin | côte des Rivières du Sud, anse du Geba, archipel des Bijagós | mangroves et rias (§V.4, §IV.6) ; demande de l'auteur |
| Mopámà | plateau de Jos (Nigeria) | Fouta-Djalon (Guinée), 800 m | émissaire de ~600 km vers Ku-jálima-rir (§VI.3) ; Mù-wúlè à l'ouest, Mù-dárhòbì au sud |
| Mù-wúlè / Mù-dárhòbì | Borgou / Ouest camerounais | escarpement du Fouta / monts Loma et Nimba | altitudes réelles (~1 500 / 1 945 m) proches des valeurs canoniques (1 800 / 2 100 m) |
| Tùmázì | Sudd (Soudan du Sud) | cuvette du lac Tchad (« Sud-Centre »), plateau relevé à ~700 m | voisinage du Mopámà (RT_001, RT_029, RT_047, Ku-Bángá, Sa-kúmadì) |
| Kù-kɨ́bò | nord-ouest du Sudd | au sud du Tùmázì, monts Mandara (1 494 m réels) | §V.5 relief + LIEUX (Q'eša-Kɨ́bò en FOR_S) |
| Affluent occidental du Tùmázì | — | Niger réel depuis le pied de Mù-dárhòbì, détourné vers l'est | Ku-Bángá (TUM_SC) au pied de Mù-dárhòbì ; RT_029 et RT_047 « fluvial + lacustre » |

---

## 1. Le contour fourni convient pour débuter

Le contour est l'Afrique réelle, en projection **Web Mercator**. Il se géoréférence exactement sur quatre points :

| Point du SVG | Lieu réel | Coordonnées |
|---|---|---|
| x = 0 | cap Vert (Dakar) | 17,53° O · 14,73° N |
| y = 0 | Ras ben Sakka (Tunisie) | 9,76° E · 37,35° N |
| x = max | Ras Hafun (Somalie) | 51,41° E · 10,44° N |
| y = max | frontière Somalie–Kenya | 41,56° E · 1,66° S |

Chaque point du contour possède donc une longitude et une latitude réelles. Trois conséquences :
- **Le relief réel sert de graine.** Altitude, côtes, vallées et massifs réels forment la base. Les altérations du Beliet s'y ajoutent : cordillère, mer intérieure, lacs.
- **Les distances sont mesurables.** Une échelle exacte existe pour chaque latitude.
- **Le travail futur se fait en coordonnées géographiques.** Une ville se place par sa longitude et sa latitude.

Quatre réserves sur le contour :
1. **Mesures.** La surface réelle est de 18,5 M km², pour ~15 M km² au Géosystème. La largeur est-ouest est de 7 380 km (6 800 km au corpus). La hauteur nord-sud est de 4 320 km (5 200 km au corpus). Le continent réel est plus large et moins haut que celui du texte.
2. **La limite sud suit des frontières politiques modernes.** La ligne droite Kenya–Somalie en est l'exemple. La carte la traite comme une découpe et non comme une côte : le reste du continent apparaît en gris au-delà.
3. **Il manque les îles.** Staur-Khlōr se trouve à ~600 km au large, hors du cadre d'origine. J'ai élargi le cadre vers l'ouest pour l'inclure.
4. **Le contour inclut une partie du Sinaï.** Je l'ai conservé tel quel.

---

## 2. Correspondances réelles ↔ Beliet (lecture « graine + jardin »)

Plusieurs données du Géosystème coïncident avec la géographie réelle. Ces coïncidences ont guidé le placement.

| Beliet | Équivalent réel | Force de la correspondance |
|---|---|---|
| ||Urumati-qoyra | hauts plateaux éthiopiens et somaliens (N-S puis E-O, volcans, escarpements, > 4 500 m) | très forte |
| Tira-ñara / Tanāḥil | Nil Bleu — **1 450 km au corpus, 1 450 km en réalité** | très forte |
| Tira-qoyra / Abnuḥīl, delta Šafāqil | Nil, delta du Nil | très forte |
| Staur-Khlōr | archipel du Cap-Vert : 10 îles volcaniques arides à ~600 km | très forte |
| Khlōr-Naw (point culminant, calderas) | Fogo (2 829 m, caldeira) | forte |
| Buhlela | Atbara / Tekezé (affluent oriental) | moyenne |
| Mer Halakhel | bassins réels du Fezzan, de Syrte, de Koufra, dépression de Qattara | forte (1 800 km × 600-900 km tiennent dans ces bassins) |
| Khreth-na-Serek et bras nord-ouest | chotts tunisiens (à 70-100 km du golfe de Gabès : portage de 5 jours) | forte |
| Désert du Sumdan (hamadas, sables rouges) | Hamada al-Hamra, Tripolitaine | forte |
| Chaîne côtière septentrionale | Dorsale tunisienne, djebel Nefoussa, djebel Akhdar (calcaires, falaises) | forte |
| ||Urumati-k'ara (O-E puis SE) | Tassili, Ahaggar, Djado, Tibesti, Ennedi, Marra : ligne réelle O-E puis SE | forte |
| |'Ara-Sukhì (> 5 000 m, volcanisme, obsidienne) | Tibesti (Emi Koussi, volcanique), surélevé | forte |
| Ehukhtal | Igharghar, fleuve fossile du Hoggar vers les chotts | moyenne |
| Tùmázì (endoréique, « Sud-Centre ») | cuvette du lac Tchad, réellement endoréique | forte (v0.2) |
| Kù-kɨ́bò (≤ 1 400 m) | monts Mandara (1 494 m) | forte (v0.2) |
| Mopámà (800 m) et son émissaire | Fouta-Djalon (~850 m) ; vallée du Corubal-Geba | forte (v0.2) |
| Mù-wúlè (≤ 1 800 m) | escarpement occidental du Fouta-Djalon | moyenne |
| Mù-dárhòbì (≤ 2 100 m) | monts Loma (1 945 m) et Nimba | forte (v0.2) |
| Ku-jálima-rir (golfe occidental, mangroves, rias) | côte des Rivières du Sud (Guinée-Bissau, Guinée) | forte (v0.2) |
| Li-sèk-dì (îlots au large de l'anse Jálondù) | archipel des Bijagós | forte (v0.2) |
| ||Urumati-halekh, ||Urumati-lóngò, !Okheti | aucun : chaînes créées | — |

---

## 3. Incohérences du corpus et choix retenus

Chaque choix est réversible dans `donnees/parametres_carte.yaml`.

### 3.1 Mer Halakhel : dimensions incompatibles avec ses relations
Quatre contraintes du corpus ne tiennent pas ensemble :
- longueur ~1 800 km et largeur 600-900 km (§VI.1) ;
- bordure orientale de la région Atlantique NO (§V.1, « E : Mer Halakhel occidentale ») ;
- route « Halakhel O → Atlantique (3 jours) » (§VI.1.2) ;
- interfluve de ~300 km jusqu'à l'Abnuḥīl (§V.2).

Une mer de 1 800 km placée à 300 km du Nil s'arrête à ~1 500 km de l'Atlantique.

**Choix v0.2 :** la superficie (1,36 M km²), le contact avec le NO, la proximité de l'Atlantique et l'interfluve priment. Pour la superficie, la mer s'étend sur ~3 900 km d'ouest en est et ne mesure que 250 à 500 km du nord au sud. Les dimensions « 1 800 × 600-900 km » ne tiennent plus. Le bassin occidental est relié au bassin principal par le détroit Khreth-na-Serek.

Deux conséquences :
- **Portage vers l'Atlantique : plausible.** La côte NO de la mer se trouve à ~150-250 km de l'Atlantique.
- **« Portage Halakhel N → Méditerranée (5 jours) » (§VI.1.2) : impossible.** Le Sumdan mesure désormais 400 à 900 km de large.

### 3.2 Longueurs de la cordillère
Les longueurs du corpus totalisent 6 500 km. Sur le continent réel, le système « Y couché » demande plus :

| Chaîne | Corpus | Carte |
|---|---|---|
| halekh | 1 200 km | ~1 100 km |
| k'ara (avec la « continuité montagnarde » vers qoyra) | 2 100 km | ~5 000 km |
| lóngò | 1 800 km | ~1 950 km |
| qoyra | 1 400 km | ~2 000 km |

Seule k'ara dépasse nettement sa longueur canonique. La mer, longue de ~3 900 km, impose une chaîne aussi longue sur sa rive sud. La « continuité montagnarde » k'ara–qoyra (§V.2) ajoute ~1 300 km (monts Nouba → escarpement éthiopien).

### 3.3 Halekh ne peut pas être l'Atlas
Halekh a des « versants sumdaniens arides (N) ». Un désert s'étend donc au nord de la chaîne. Au nord de l'Atlas réel s'étendent le Maroc et le Tell, régions humides. **Choix v0.2 :** halekh va de la côte mauritanienne (~20° N) au nœud !Okheti (6° O). Le lobe occidental de l'Halakhel et le Sumdan occidental occupent son flanc nord. L'Atlas réel, absent du corpus, est **écrêté** à ~2 100 m [PROPOSITION]. Il forme les « piémonts ondulés » de la région NO.

### 3.4 |'Ara-Sukhì attribué à deux chaînes
§I le place dans k'ara. Les sources de l'Imikhrel (§V.3, §VI.5) disent « |'Ara-Sukhì (||Urumati-lóngò) ». Le registre tranche : `partie_de GEO_ORO_URUMATI_KARA`. **Choix :** k'ara.

### 3.5 Kù-kɨ́bò au nord ou au sud du Tùmázì
§V.5 le place au sud du lac dans « Relief » et au nord dans « Limites ». §I parle de « transition Tùmázì / k'ara ». LIEUX tranche : Q'eša-Kɨ́bò a pour façades TUM_SC **et FOR_S**, donc côté forêts. **Choix v0.2 :** au sud du lac, sur les monts Mandara, dont l'altitude réelle (1 494 m) correspond à la valeur canonique.

### 3.6 Sud-ouest : recoupement GEO / ROUTES / LIEUX

| Élément | GEO | ROUTES | LIEUX | Placement v0.2 |
|---|---|---|---|---|
| Façade ATL_SO | Staur-Khlōr à ~600 km (§V.7) ; mangroves Ku-jálima-rir, rias SO | RT_042, RT_057 : liaisons hauturières vers le NO | Ku-jálima-rir, Jáli-Fè, Anses-Jálondù, Jáli-lòngò, Gálu-kánda | Guinée-Bissau, Guinée |
| Mopámà | 800 m ; émissaire ~600 km vers Ku-jálima-rir ; N lóngò, O Mù-wúlè, S Mù-dárhòbì | RT_003 Kù-téka → Ku-jálima-rir (fluvial + cabotage) ; RT_060 | Kù-téka (MOP_SO + URU_SO) ; Kù-Bèláà, Mázì-Dúm en `foret_maree` | Fouta-Djalon |
| Tùmázì | « Sud-Centre » ; O : transition Mopámà ; E : piémonts qoyra | RT_001 caravane vers Kù-téka ; RT_029, RT_047 fluvial + lacustre vers Mù-dárhòbì et Ku-jálima-rir ; RT_010 col depuis Tanāḥil | Ku-Bángá (TUM_SC + MOP_SO, piémonts Mù-dárhòbì) ; Sa-kúmadì, Ku-pèpanà (FOR_S, pôle Kù-téka) | cuvette du Tchad, reliée au Fouta par le Niger |
| Li-sèk-dì | îlots secs au large de l'anse Jálondù | — | ZRS rattachée à Anses-Jálondù | Bijagós |

Trois tensions restent :
- **« E : ||Urumati-k'ara (piémonts) » pour le bassin Mopámà (§V.4).** Côté est s'étend le plateau du Tùmázì, que k'ara borde seulement au loin vers le nord-est.
- **« E : piémonts qoyra » et « affluents E venus des plateaux SE » pour le Tùmázì.** Le lac se trouve à ~2 000 km de qoyra, et ces affluents seraient très longs.
- **L'orientation de lóngò.** Le corpus dit « NO-SE » ; une chaîne qui relie le nœud au Fouta est orientée NE-SO. Ses versants humides font face au sud-est.

### 3.7 Longueur de l'Abnuḥīl
Le corpus annonce 6 800 km et un bassin de 3,2 M km². Le confluent se trouve dans le Beliet, en zone de transition montagne/désert. Le système mesure alors ~3 600 km sur la carte : 1 450 km de Tira-ñara, ~1 850 km de tronc jusqu'à la diffluence, 300 km de bras d'Abnīqa. Les 6 800 km supposent des sources très au-delà du Beliet. Ce sont les longueurs du Nil réel.

### 3.7 bis Longueurs des fleuves de la rive sud
Une mer adossée à la cordillère laisse peu de place aux fleuves qui s'y jettent :

| Fleuve | Corpus | Carte |
|---|---|---|
| Ehukhtal | ~1 100 km | ~650 km |
| Imikhrel | ~800 km | ~350 km |
| |Na-madikh / Madīlan | ~1 400 km | ~650 km |

Ces longueurs canoniques supposaient la mer éloignée de la chaîne. Elles ne reviennent qu'en écartant de nouveau la mer de la cordillère.

### 3.8 Buhlela, « sources hors-Beliet E »
À l'est du Beliet se trouve la mer Rouge. Le Buhlela est placé sur l'Atbara/Tekezé, qui naît dans qoyra. **Non résolu.**

### 3.9 Surfaces
- Les trois zones bioclimatiques totalisent 15,0 M km².
- Les sous-régions détaillées totalisent 10,0 M km², plus 1,35 M km² d'Halakhel, sans compter le Sumdan.
- La carte compte **~17,0 M km² de terres émergées (zone estompée pondérée) et 1,36 M km² de mer intérieure.**

### 3.10 Autres points relevés
- **Chaîne côtière septentrionale.** Le corpus donne « ~1 200 km » ; la côte qu'elle doit border, de la Tunisie au delta, mesure ~2 500 km.
- **Index des façades.** `ATL_INS` décrit Staur-Khlōr comme « ~40 îles : dunes stabilisées, volcans éteints, îlots rocheux ». Cette phrase vient des îles de l'Halakhel ; §V.7 compte 10 îles.
- **Tawālmaz.** « Accès Halakhel zone nord-centrale côtière », alors que la Madīlan vient des versants nord de k'ara, au sud. **Choix :** ria sur la rive sud-centrale, confirmée par LIEUX (Tawālmaz en façade HKL_S).

### 3.11 Contraintes et contradictions issues de LIEUX, ROUTES et RESSOURCES
Aucun de ces fichiers ne contient de coordonnées : `distance_approx`, `longueur_km` et `duree_jours` sont tous vides. Ils fixent en revanche des relations de voisinage, que la v0.2 respecte :
- **Proximité Atlantique NO ↔ Halakhel NO.** Le portage du Sas terrestre relie Khloreth-klam à Kralekh-Aktrik (RT_027, RT_004, RT_018, RT_040).
- **Halekh entre l'Atlantique et la rive sud.** Bannaktì est reliée à l'île Kot-Skral (RT_066) et à Cherbekh-khem, sur la rive HKL_S (RT_051).
- **Cordillère franchissable vers le Tùmázì.** La route Tanāḥil → Kù-békà passe par un col de haute altitude (RT_010).
- **Mopámà et Tùmázì reliés.** Une caravane relie Kù-békà et Kù-téka (RT_001), et une voie fluviale et lacustre va du Tùmázì à la côte SO (RT_047). Sur la carte, le bassin du Tùmázì remonte par le Niger jusqu'au pied de Mù-dárhòbì, au sud du Mopámà. Les zones forestières de ce bassin rattachées à Kù-téka (Sa-kúmadì, Ku-pèpanà) s'y trouvent donc. Kù-téka est aussi en façade URU_SO (lóngò).

Contradictions relevées :
- **RT_046 Imekh-stom ↔ Ku-jálima-rir.** La route est notée « maritime_cabotage » seul, entre un port de la mer fermée et la côte atlantique SO. Elle exige un portage.
- **Mangroves au bord du Mopámà.** Ku-Bèláà et Mázì-Dúm (MOP_SO) ont le milieu `foret_maree`, alors que le lac est à 800 m d'altitude. La façade MOP_SO doit donc englober l'estuaire de l'émissaire, à ~600 km du lac.
- **Deux sens pour « Tanāḥil ».** Dans §VI.5, c'est l'affluent venu des plateaux SE (Nil Bleu). Dans §V.2 « Haute Tanāḥil » et dans LIEUX, c'est la vallée qui descend des piémonts nord de k'ara vers le delta Abnīqa-Tanāḥil, sur la rive est de la mer. Sur la carte, le fleuve suit le premier sens ; les villes du second ne sont pas placées.
- **HKL_S : glacis ou côte rocheuse.** L'index des façades dit « glacis », LIEUX dit `littoral_rocheux`. **Choix :** rocheux.
- **Suffixes d'identifiants.** LUR_CHERBEKH-KHEM_NO est en façade HKL_S ; LUR_TAWALMAZ_NE aussi. C'est sans effet sur la carte.
- **RESSOURCES.** Le fichier ne contient aucune donnée de localisation ; il n'a pas servi à la carte.
- **Registre.** `GEO_EXT_ATLANTIQUE` et `GEO_GLF_JALONDU` portent la même forme, « Jálondù ».
- **Gel de l'Halakhel.** La « Mer Halakhel gelée en bordures » (§III) tombe entre 22° et 31° N, à −20 m d'altitude. C'est physiquement extrême ; cela ne figure pas sur la carte.
- **Bassin versant du Tùmázì** (~1,8 M km²) : à vérifier sur le modèle hydrologique.

---

## 4. Ce qui est [PROPOSITION] sur la carte

Tous ces éléments sont des choix de placement. Le corpus ne fixe aucune coordonnée.
- **Tracés et positions :** chaînes, mer Halakhel et son bras nord-ouest, les trois lacs, les fleuves dessinés (Madīlan, Imikhrel, Ehukhtal, Ḥawqal et ses affluents, Abnīqa, émissaire du Mopámà).
- **Écrêtements :** Atlas et ligne du Cameroun.
- **Îles :** ~40 îles de l'Halakhel, îlots de Li-sèk-dì, Khlōr-Naw posé sur Fogo.
- **Milieux :** les ergs et l'ensemble des milieux. Ces derniers sortent d'un modèle climatique calibré sur les précipitations chiffrées du corpus (24 points, dont 14 tirés directement du texte).

## 5. Absent de la v0.1
- **Les 48 cols.** Le registre donne altitudes et interfaces, pas de positions.
- **Les 24 phénomènes.** Leurs zones sont décrites mais non cartographiées.
- **Les noms des îles de Staur-Khlōr,** sauf Khlōr-Naw.
- **Les éléments en lacune au registre,** laissés sans endonyme : chaîne côtière (étiquette descriptive en français), émissaire et delta du Mopámà. Méditerranée, mer Rouge et océan de l'Est portent leur libellé français du corpus.
- **Les villes.** Le calque existe et il est vide.
