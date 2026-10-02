# Analyse de cohérence — carte du Beliet v0.1

Sources lues en entier : `references/GEOSYSTEME_GLOBAL_DU_BELIET_v3.1.md`, `references/GEOSYSTEME_REGISTRE.v1.json` (132 entrées), `references/MAP_BELIET_ORIGIN.svg`.

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
| Tùmázì (endoréique) | Sudd (Soudan du Sud) : le Nil Blanc y est capté | moyenne |
| Mopámà et son émissaire | piémont du plateau de Jos ; bas Niger jusqu'au delta | moyenne |
| Mù-dárhòbì (≤ 2 100 m) | hautes terres de l'Ouest camerounais, écrêtées | moyenne |
| Ku-jálima-rir (golfe occidental, mangroves) | golfe de Guinée, delta du Niger | moyenne |
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

Une mer de 1 800 km placée à 300 km du Nil s'arrête à ~1 500 km de l'Atlantique. **Choix :** superficie, interfluve et Sumdan priment. Résultat : 1,37 M km², environ 2 200 km d'ouest en est sur 450 à 650 km du nord au sud. La route de 3 jours vers l'Atlantique reste impossible, et la région NO ne touche pas l'Halakhel.

### 3.2 Longueurs de la cordillère
Les longueurs du corpus totalisent 6 500 km. Sur le continent réel, le système « Y couché » demande plus :

| Chaîne | Corpus | Carte |
|---|---|---|
| halekh | 1 200 km | ~1 450 km |
| k'ara (avec la « continuité montagnarde » vers qoyra) | 2 100 km | ~4 000 km |
| lóngò | 1 800 km | ~1 850 km |
| qoyra | 1 400 km | ~2 000 km |

Le rapport moyen est d'environ 1,4. La « continuité montagnarde » k'ara–qoyra (§V.2) impose à elle seule ~1 300 km de crêtes supplémentaires (monts Nouba → escarpement éthiopien).

### 3.3 Halekh ne peut pas être l'Atlas
Halekh a des « versants sumdaniens arides (N) ». Un désert s'étend donc au nord de la chaîne. Au nord de l'Atlas réel s'étendent le Maroc et le Tell, régions humides. **Choix :** halekh va de l'Adrar mauritanien au Tidikelt. Le Sumdan occidental, avec ses ergs Iguidi et Chech, occupe son flanc nord. L'Atlas réel, absent du corpus, est **écrêté** à ~2 100 m [PROPOSITION]. Il forme les « piémonts ondulés » de la région NO.

### 3.4 |'Ara-Sukhì attribué à deux chaînes
§I le place dans k'ara. Les sources de l'Imikhrel (§V.3, §VI.5) disent « |'Ara-Sukhì (||Urumati-lóngò) ». Le registre tranche : `partie_de GEO_ORO_URUMATI_KARA`. **Choix :** k'ara.

### 3.5 Kù-kɨ́bò au nord ou au sud du Tùmázì
§V.5 le place au sud du lac dans « Relief » et au nord dans « Limites ». §I parle de « transition Tùmázì / k'ara ». **Choix :** au nord-ouest du lac, deux mentions contre une.

### 3.6 Voisin oriental du bassin Mopámà
« E : ||Urumati-k'ara (piémonts) » (§V.4) est incompatible avec la position de lóngò, qui sépare les deux. **Choix :** à l'est, une transition vers le bassin du Tùmázì.

### 3.7 Longueur de l'Abnuḥīl
Le corpus annonce 6 800 km et un bassin de 3,2 M km². Le confluent se trouve dans le Beliet, en zone de transition montagne/désert. Le système mesure alors ~3 600 km sur la carte : 1 450 km de Tira-ñara, ~1 850 km de tronc jusqu'à la diffluence, 300 km de bras d'Abnīqa. Les 6 800 km supposent des sources très au-delà du Beliet. Ce sont les longueurs du Nil réel.

### 3.8 Buhlela, « sources hors-Beliet E »
À l'est du Beliet se trouve la mer Rouge. Le Buhlela est placé sur l'Atbara/Tekezé, qui naît dans qoyra. **Non résolu.**

### 3.9 Surfaces
- Les trois zones bioclimatiques totalisent 15,0 M km².
- Les sous-régions détaillées totalisent 10,0 M km², plus 1,35 M km² d'Halakhel, sans compter le Sumdan.
- La carte compte **17,06 M km² de terres émergées et 1,37 M km² de mer intérieure.**

### 3.10 Autres points relevés
- **Chaîne côtière septentrionale.** Le corpus donne « ~1 200 km » ; la côte qu'elle doit border, de la Tunisie au delta, mesure ~2 500 km.
- **Index des façades.** `ATL_INS` décrit Staur-Khlōr comme « ~40 îles : dunes stabilisées, volcans éteints, îlots rocheux ». Cette phrase vient des îles de l'Halakhel ; §V.7 compte 10 îles.
- **Tawālmaz.** « Accès Halakhel zone nord-centrale côtière », alors que la Madīlan vient des versants nord de k'ara, au sud. **Choix :** ria sur la rive sud-centrale.
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
