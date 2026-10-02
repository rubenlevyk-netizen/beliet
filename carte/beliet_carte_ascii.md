# Carte ASCII du Beliet (v0.3.2)

Version texte de la carte générée, pour un usage sans image : corpus, agents, recherche de positions.
Elle complète la carte visuelle et ne la remplace pas. Elle est régénérée par `python3 outils/carte_ascii.py`.

## Lecture

- **Grille** : projection équirectangulaire, une case = 0.5° de longitude × 0.5° de latitude (≈ 55 km × 55 km à l'équateur, ≈ 45 km × 55 km à 35° N).
- **Emprise** : -18.0° à 52.0° de longitude ; 38.0° N à -2.0° de latitude. 140 colonnes × 80 lignes.
- **Repères** : en haut et en bas, la longitude (`|` tous les 10°, `'` tous les 5°) ; à gauche, la latitude du bord supérieur de la ligne (toutes les 2°).
- **Retrouver une case** : colonne = (longitude + 18) ÷ 0,5 ; ligne = (38 − latitude) ÷ 0,5, en comptant à partir de 0.
- **Case** : altitude = 90e centile des terres de la case ; milieu = milieu majoritaire ; eau quand elle couvre ≥ 40 % (mer Halakhel), ≥ 30 % (lac) ou ≥ 50 % (océan).
- Le Sud estompé (au-delà de la limite du Beliet) et les terres hors Beliet restent en blanc.

## 1. Relief et eaux

| Signe | Sens | Signe | Sens |
|---|---|---|---|
| `~` | océan, mers extérieures | `=` | mer Halakhel |
| `o` | lac (Tùmázì, Akhtir, Mopámà) | `w` | fleuve nommé |
| `_` | terre sous le niveau de la mer | `.` | 0-300 m |
| `:` | 300-700 m | `+` | 700-1 200 m |
| `n` | 1 200-1 800 m | `m` | 1 800-2 600 m |
| `M` | 2 600-3 600 m | `A` | > 3 600 m |
| `^` | point culminant d'une chaîne nommée | `X` | col (48, voir §4) |
| `#` | détroit, goulet, débouché, delta, estuaire | | |



```
                        -10                 0                   10                  20                  30                  40                  50  
              '         |         '         |         '         |         '         |         '         |         '         |         '         |   
  38.0 |~~~~~~~~~~~~~~~~~~                ~~~~~~~~~~~~~~~~~~~~~~~~~~~      ~~~~~~~~~~~~    ~~~~~~~                                            ~~~~~~|
       |~~~~~~~~~~~~~~~~~~               ~~~~~~~~~~~~~~~~~~~~~..~~~~~~~   ~~~~~~~~~~~~~   ~~~~~~~~~                                            ~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~        ~~~~~~~~~~~::++~++::::::...~~~~~~~ ~~~~~~~~~~~~~~~ ~~~~~~~~~~     ~~      ~                                ~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~:::++++n++nnnnn++:::~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ~~~~   ~~~~                                |
  36.0 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.::+++++++nnnnnnnnn+:..~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                |
       |~~~~~~~~~~~~~~~~~~~~~~~~:+~~~~~~~:::+++n+++++::+nnnnnnn:..~~~~~~~~~~~~~~~~~~~~~~~~~~   ~~~~~~~~~~~~~~~  ~~~~                                |
       |~~~~~~~~~~~~~~~~~~~~~~~..:nnn+:++nn++++++nnn++:.++++++++:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ~~~~~                                |
       |~~~~~~~~~~~~~~~~~~~~~~~.:::++:++nnn++++nnn++::.....:::::+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                 |
  34.0 |~~~~~~~~~~~~~~~~~~~~~~::+nnnnnn+++++nnnnn+++:::.........:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                 |
       |~~~~~~~~~~~~~~~~~~~ .:+++nnn+nnnnnnnnnn+++++::.........:+:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                  |
       |~~~~~~~~~~~~~~~~~~.::+++nnnnnnnnnnnn+++++++:::.........::::....:~~~~~~~~~~~~~~:++~~~~~~~~~~~~~~~~~~~~~~~~~                                  |
       |~~~~~~~~~~~~~~~~~~::::+nnnnnnn++++++++++:::::..........:::::::+:...~~~~~~~~~.:++++:~~~~~~~~~~~~~~~~~~~~~~~                                  |
  32.0 |~~~~~~~~~~~~~~~~~::::nnmnnn++++::+++++:::::::..........:::::++++:..~~~~~~~~~:++:....::~~~~~~~~~~~~~~~~~~~                                   |
       |~~~~~~~~~~~~~~~~:nnnmnnnnn+++:::::::::::::::...........:::::::::::::.~~~~~~~+:.......::::::~~~~~ww#w~~~~                                    |
       |~~~~~~~~~~~~~~~~+nnnnnnnn++++:..=.::::::::::...==...===.:::::::::.:::::.~~~~............:::.::::.w#...:.:                                   |
       |~~~~~~~~~~~~~~~~~:nnnnn++++:::.==.:::..:::::..==========.:::::::::..::::::::......==...===.......ww..::::                                   |
  30.0 |~~~~~~~~~~~~~~~~ nnn+::::::::...#....==.:::::..=========.::::::::.==....::....=..==========.......w:::+:++                           ~~~~   |
       |~~~~~~~~~~~~~~~~+n+::::::.....=========.::::::.=======..::::::::..===.==....================......w++.+nn+                          ~~~~~   |
       |~~~~~~~~~~~~~~ :++::::::.============.=....:::.=========.:::.::.=============================....ww:+::nn                            ~~~~~  |
       |~~~~~~~~~~~~~:::::::.==..============.=...=.:..==============...=============================....w::++.nn                            ~~~~~  |
  28.0 |~~~~~~~~~~..::::::::..#==================.====.=============================================#wwwww::++:~~~~                           ~~~~~~|
       |~~~~~~~~~...:::::::.ww.====.==========================================..=====================....ww:::+:~~~                            ~~~~~|
       |~~~~~~~~~.....:::::#:ww==....================...=====.......=========.::=====================.....ww::++~~~~                            ~~~~|
       |~~~~~~~....:::::::::::ww::::......==========.:::..:..:::::::.=======.:::====================..:::::www::.~~~~                           ~~~~|
  26.0 |~~~~~~~...:::::::::::::wwwwwww:::::.#......:::::::::::+++:::....====.::.====================.:::::::ww:::~~~~~                          ~~ ~|
       |~~~~~~....:::::::::::::::::::wwwwww:wwww:::::+++++++++nn+++:::..==...:::.================#...:::.::::w::::~~~~                             ~|
       |~~~~~~..:..::::::::::::+:::::::+w+ww:::ww+++++nnnnnnwwwnn+++ww.#.:::::::....============ww::::::.::::w.:::~~~~~                            ~|
       |~~~~~..:::....::::::+::+::::+n++nnn++++nwwwwwwmwwwwwwnwwwwwww::::::+::::::::=====..===.ww:::::::.::::w:::++~~~~                            ~|
  24.0 |~~~~..:::::::.::++++n+nnnnmnnnnnmMMXmmMMmmmmXMMMmmmmmmmnwn+++++:::++:::::++::...=..==.:ww+:::::...:::w:::::~~~~~~                           |
       |~~~~..:::::::::+:+nnMMmmMMMMXmMMMXMm^MXMmXMMMMMMMMXMmMmnnmnn++n++:+++::+++++::::..=...:www+:::.....::w:::::~~~~~~~                          |
       |~~~...::::::::+:nmXMmMMMMXAMnMMXMmmnnmmmmmmmmmmMMmmmXMMmnmmnmMn+++++++++nnnn++++++++wwww+w:::......www::::+.~~~~~~                          |
       |~~~..:::::::+++++mmMMM^MMnMMmnm+nnnnnnnmmnmmmnnmMmmmMMnnmmMmmMmmmnn+++mnnnmnnnnnnnoww++n+w:::::.::ww::::::+::~~~~~                          |
  22.0 |~~.....::++nmmmnmXmmnMm+++nnm++:+n+nn++mXmn++++nnnmn+m++m+mMMMMmmnn+nnMMmmmnnnnooooonnnn+ww:::::::w:::::::+:++~~~~                          |
       |~~...:.::+nmXMXmX++mm+++n+++n+++++::++nnmmn+++++++++++++nmnmMmmmnmMMAMMMMMnnnnoooooonnnn++w::::::w:::::::++::+~~~~                          |
       |~~..::+nXmXXmmnmn++nn:::::::+::::+::+nnnnn+++++::+::+++:+nn+nn+nMMMXAAAAAMmnwwwooooonnnn+++:::::ww:::::::::::+~~~~~                         |
       |~~~.::nXnn+++++nn:+::::::::::::::::++nnnnm+++:+++::++++:::+:+nnnmmMMmMA^AMmmwMnoowwnnnnn+++:::::ww::::::::::++~~~~~~                        |
  20.0 |~~~.:.:++::::::::::::::::::::::+:::::+nnXmm++::+:::++++::::::++::+nmMnMAAAAwwMmnnwwnnnn++++:::::ww:::ww::::+++.~~~~~~                       |
       |~~~.......:::::::::::::::::...::::::+nnnmmmXn+++++:++n+::::::::::::mMmnMAAAAAMnnnwwnn++++++::::.w.::wwww::::++:~~~~~~~                      |
       |~~~~......:::::::::::::::::...::::::+++++n+nnn++++++nnn+:::::::::::+n+mnmMAMXMMnnwnnn++++++::::.ww:ww::w:::++++~~~~~~~                      |
       |~~~~.......:::::::::::::::::..:::::::::++++nmmn+:++++n++::::::::::::::n:++mmMMmmnwn++++++++::::::www:::w:::::++.~~~~~~~                     |
  18.0 |~~~~.......:::......::::::::...::::::++++++nnXn++n+++n++:::::::::::::::::::nmMXmwwnnn+++::::::::::w::::ww::::+:+n.~~~~~~                    |
       |~~~~.......::........:::.......::::::::::+++nmn++n+:++++::::::::::::::::::::+mmMmnnn++++:::::::::::::::www:::::+n:~~~~~~~                   |
       |~~~.........:..:.....:::....:....::::::::+::+nnmn++:::++::::::::::::...::::++nmMMmnn+++++++::::::::::www:ww::::+mn~~~~~~~                   |
       |~~~.........:.:.......::..:....:::::::::::::+nnmmnn+:++::::::::::::::::::::+++nXmmmn++++++++:::::::::w::::ww:::nmn+~~~~~~~                  |
  16.0 |~~~...................::::....:::::::::::::::++nXnn++++::::::::::::::::::::::+nMMMXmn++n++++::::::::ww:::::w:+++nm+~~~~~~                   |
       |~~...............:::..:::...:::::::::.::::::::+nnn+++++::::::::::::::::::::::+nnMmMXmnn+nn+++:+::::::ww::::w:+++nXm+~~~~~                  ~|
       |~..............:.::..:......:::...:::.::::::::++nnnn++++::::::::::::::::::::::+nmnmmnnnn++++++::::::::w::::w:+++nmmm..~~~~             ~~~~~|
       |~~............::.::::::.....::.:::::::.:::::::++nXmn++++:::::::::::::::::::::++nnmMMmmnn++++++::::::::ww:::wwwwwXmXM::+~~~            ~~~~~~|
  14.0 |~~~...........::.::::::....::.:::::::::::::::::++nnnnn+::::::::::::::::::::::+++nnmmMmnn+++++++::::::::w:::::+mwwwmm+.++~~         ~~~~~~~~~|
       |~~~..........:.:::::::::..:::.::::::::::::::::::++nXnn+::::::::::::::::::::::+++++mMXMmmm++++++++::::::w::::++mM^wmm+.:+:~~    ~~~~~~~~~~~~~|
       |~~...........:::::::::::::::..::::::::::::::::::++nnn+++:::::::::::::::::::::+++++nmmmmXn+++++++:::::::ww:::+nmXwwMM+:::::~  ~~~~~~~~~~~~~~~|
       |~~~.......:+::::::::::::::::::.:::::::::::::::::+nn+n+++:::::::::::::::::+:::+++++nmmXmmmnnn+n+++++:::::w::+nmmMwwMm++:::+:~~~~~~~~~~~~~~~~~|
  12.0 |~~~~~.....:+++::::::::::::::::.:::.:::.:::++::++nnn+nn+++++::::::::::::::+::+++++++++nn+n+nnnn+n++++::::ww+++mwXMwwm++:+++~~~~~~~~~~~~~~~+~~|
       |~~~~~...::++++::::::::::::::::.:::..:..:::+++:+nn+++nnn++++:::::::::::::+::::+++++++++++++++mnmmmnn++::++ww+nwwwwMMMn:+::+.~~~~~~~~~~:+n++~~|
       |~~~~~~..:::+++:::::::::::::::::::..::.::::+nn:++oo++nnn++++++::++:::::::::::++++++++++++++++nmnmXmn+++++++wmnmmMwwMMn+++++:.~~~::+mnnn+n+:~~|
       |~~~~~~~..::+++::::::::::::::::::......::::+n++ooooo+nnnn+++:+:++:::::::::::::++++++++++++++++++nnnnmmn++nnwwwwwwwmMMn++++nn+++nn+nnnn++:::~~|
  10.0 |~~~~~~~~~::.:::::::::::::::::::::.....::::+^++ooo+++nnnn++::::+:::::::::::::::+++++++++++++++:+++++nXnmXnnnwmmmwMMMM++nnmmnnnnnn+n++++++::~~|
       |~~~~~~~~~...::::+++:::::::::::::.....:::::+++woo+++++nn++::::::::::::::+:::::+++++nn+++++++++::::::::+nmmmmmmmmmMMMm+mmmmmmnnnn++++++++::.~~|
       |~~~~~~~~~~..::::++++::::::::.::......::::::+ww++::+++::::::+:+::::::::::::::+++++nnoooo+++++++::::::::++nXXmXmmMMMmmmmmmnnnnn++++++:::+::~~~|
       |~~~~~~~~~~..:::::++::::::::..::......:::::www:+n+++n+::::::+::+::+:::::::::++++++noooooooo+++++:::::::::+nmmmmmmMmmMmmmmnnnn+++++++++:::~~~~|
   8.0 |~~~~~~~~~~ ...::::::+:::.:....:::...:+::.ww::+++nn^+:::::++++n+nn+++:::::::++++++ooooooooo+++++::::::::::mXXmmmMmMMmmmn++++++++:+::::::.~~~~|
       |~~~~~~~~~~~~..::::::::........::::...+..ww::::::+++::::::+nnn++nnn++++:::++++++++ooooooooo++++++:::::::::+mmmmmmmMMMmmn++++++++:::::::.~~~~~|
       |~~~~~~~~~~~~~.....:.:..........:.::..:.ww....:::::::..:++nnn+++nnnnn+++:+++++++^nn+oooooo+++++++:+:::::::+mmnnmmmMMAmnn+:+:+++::::::...~~~~~|
       |~~~~~~~~~~~~~~~...................::.www..~~....:::...+nnn+++++++++++++++++++++nnn++++++++++++++++::::::++nn+mMmMMmnnn+++:::::::::....~~~~~~|
   6.0 |~~~~~~~~~~~~~~~~.....................w#~~~~~~~....:..::nnn++++++++++++++++++++++++++++++++++++++++:::::::nn++mmmmmmnn++:+::::::::.....~~~~~~|
       |~~~~~~~~~~~~~~~~~..................~~~~~~~~~~~~......::nn+++++++++++++++++::+++++++++++++++++++++++::::::++:+nnnnnnnnn+:::::::::....:~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~....~~~~~~~~.~~~~~~~~~~~~~~~.......++:+:::++++++++++++++++++++++++++++++++++++++++++++:++++nnnn+n+++:::::::::...:~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..~~~~n.++::++++:+:+:+++::++::+++++++++++++++++ +++++nnn+::+:++nnnn++++:.:::::.:..:.~~~~~~~~|
   4.0 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..:++++++++++++::::::::+++++++++++++  +   n++ mnnm++::+:+nn++++::.:::::.....~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:++:+++:::+:::::::::::++++++++++             nnnn+::+:++:++::::::::::....~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~: +++::::::: : :  ::::::+  +                  +nnn++:++:::::::::::::.....~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.  :   :           :                              nn++n+++:::::::.:......~~~~~~~~~~~~|
   2.0 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.                                                   ++nn::::::.........~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.                                                   mnmn+::...........~~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.                                                         :    ......~~~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.                                                                 .~~~~~~~~~~~~~~~~~~|
   0.0 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..                                                                 ~~~~~~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..                                                                 ~~~~~~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..                                                                ~~~~~~~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..                                                               ~~~~~~~~~~~~~~~~~~~~~|
              '         |         '         |         '         |         '         |         '         |         '         |         '         |   
                        -10                 0                   10                  20                  30                  40                  50  
```

## 2. Milieux (vocabulaire du Géosystème)

| Signe | Milieu | Signe | Milieu |
|---|---|---|---|
| `d` | Désert de pierre (`desert_pierreux`) | `s` | Désert de sable (`desert_sableux`) |
| `u` | Cordons dunaires côtiers (`dunes_littorales`) | `O` | Oasis (`oasis`) |
| `-` | Steppe semi-aride de piémont (`steppe_piemont`) | `f` | Fourré côtier sec (`fourre_cotier_sec`) |
| `x` | Dépression saline (`depression_saline`) | `c` | Côte désertique (`cote_desertique`) |
| `r` | Récif corallien (`recif_corallien`) | `l` | Littoral rocheux (`littoral_rocheux`) |
| `a` | Plaine alluviale irriguée (`plaine_alluviale`) | `M` | Forêt de montagne et de piémont (`foret_montagne`) |
| `p` | Prairie d'altitude (`prairie_altitude`) | `g` | Zone périglaciaire (`zone_periglaciaire`) |
| `*` | Glacier (`glacier`) | `T` | Forêt tropicale humide (`foret_tropicale_humide`) |
| `h` | Herbage arboré (`herbage_arbore`) | `b` | Forêt de berge (`foret_berge`) |
| `v` | Forêt de marée (`foret_maree`) | `w` | Zone humide lacustre (`zone_humide_lacustre`) |
| `o` | Eaux lacustres et hauts-fonds (`eaux_lacustres`) | `i` | Île aride (`ile_aride`) |

`~` océan, `=` mer Halakhel, `o` lac, blanc : hors Beliet ou estompé.



```
                        -10                 0                   10                  20                  30                  40                  50  
              '         |         '         |         '         |         '         |         '         |         '         |         '         |   
  38.0 |~~~~~~~~~~~~~~~~~~                ~~~~~~~~~~~~~~~~~~~~~~~~~~~      ~~~~~~~~~~~~    ~~~~~~~                                            ~~~~~~|
       |~~~~~~~~~~~~~~~~~~               ~~~~~~~~~~~~~~~~~~~~~ff~~~~~~~   ~~~~~~~~~~~~~   ~~~~~~~~~                                            ~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~        ~~~~~~~~~~~ffff~fffffffffff~~~~~~~ ~~~~~~~~~~~~~~~ ~~~~~~~~~~     ~~      ~                                ~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~fffffffff-fhhhffffff~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ~~~~   ~~~~                                |
  36.0 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~fffffffff-----------ddd~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                |
       |~~~~~~~~~~~~~~~~~~~~~~~~ff~~~~~~~fffff-----------------ddd~~~~~~~~~~~~~~~~~~~~~~~~~~   ~~~~~~~~~~~~~~~  ~~~~                                |
       |~~~~~~~~~~~~~~~~~~~~~~~ffffhhffffh------------dddddddddddd~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ~~~~~                                |
       |~~~~~~~~~~~~~~~~~~~~~~~ffffffffh-----------ddddddddddddd-~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                 |
  34.0 |~~~~~~~~~~~~~~~~~~~~~~fffhh-------------ddddddddddddxxddd~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                 |
       |~~~~~~~~~~~~~~~~~~~ ffffhh-----------ddddddddddddddddddd--d~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                  |
       |~~~~~~~~~~~~~~~~~~fffffh------------ddddddddddddddddddddd--dffff~~~~~~~~~~~~~~fff~~~~~~~~~~~~~~~~~~~~~~~~~                                  |
       |~~~~~~~~~~~~~~~~~~fffhhh----------ddddddddddddddddssssdddx--fffffdd~~~~~~~~~fffffff~~~~~~~~~~~~~~~~~~~~~~~                                  |
  32.0 |~~~~~~~~~~~~~~~~~fffhhh--------dddddddddddddddddddsssssddd-------dd~~~~~~~~~ffffffffff~~~~~~~~~~~~~~~~~~~                                   |
       |~~~~~~~~~~~~~~~~fffhhh--------dddssssssssddddddddssssssdddddddddd--ff~~~~~~~ffdddddffffffff~~~~~aaaa~~~~                                    |
       |~~~~~~~~~~~~~~~~ffMhh---------dd=sssssssddddddd==ddd===ddddddddddd--ffff~~~~ffdddddddfffffffffffaaaaaffff                                   |
       |~~~~~~~~~~~~~~~~~ffh---------dd==ssdssdsdddddd==========dddddddddddddffffffffsssss==sdx===fffffffaaffffff                                   |
  30.0 |~~~~~~~~~~~~~~~~ fhh------dddddd=dddd==dddddddd=========dddddddddd==dddfffffxd=ss==========xdff---afffffff                           ~~~~   |
       |~~~~~~~~~~~~~~~~hhh-----dddddd=========dddddddd=======dddddddddddd===d==dddd================xdd-dxa-------                          ~~~~~   |
       |~~~~~~~~~~~~~~ hhh-----dd============d=dddddddd=========dddddddd=============================dxxddd--dd--                            ~~~~~  |
       |~~~~~~~~~~~~~hhhhh---==dd============d=ddd=dddd==============ddd=============================dddddd---ddd                            ~~~~~  |
  28.0 |~~~~~~~~~~-h-hh-------===================d====d==============================================xdddadd--d~~~~                           ~~~~~~|
       |~~~~~~~~~-hh-----------====-==========================================dd=====================xdddddddddc~~~                            ~~~~~|
       |~~~~~~~~~hhh-----------==---d================ddd=====-------=========ddd=====================ddddddddddd~~~~                            ~~~~|
       |~~~~~~~hhh------------------dddddd==========dd-d-------hhh---=======dd-d====================ddddddddddddc~~~~                           ~~~~|
  26.0 |~~~~~~~hhh-----------------addd--ddd=dddddddd-------hhhh--------====dddd====================ddddddddddddd~~~~~                          ~~ ~|
       |~~~~~~hhhh-----------------dddd-----dadddd-----------h----------==--d-ddd================xdddddddddddddddd~~~~                             ~|
       |~~~~~~hhhh-------dd-------dx-dd--------------------------------hh----ddddddd============add-dddddddddddddd~~~~~                            ~|
       |~~~~~hhhh--------d--------s------------------------------------------ddddd-d=====dd===dd----ddddddddddddddd~~~~                            ~|
  24.0 |~~~~hhhhh---------------sdd----dd-----------ppp---------------------dddddd-ddddd=dd==dd----dsssdddddddddddd~~~~~~                           |
       |~~~~hhhh---------------ddddpddddppddppppdddppppppp------------------ddddddd----ddd=d-d-----dsssdsxddddddddd~~~~~~~                          |
       |~~~hhhhh--------------pppdppddpdddddddddddddddddp----p--------------ddddddddd---------------sssssssddddddddc~~~~~~                          |
       |~~~hhhhh-------------p-----dddddddddddddddddddddd----p-------------ddddddddddd----oah--------sssssddddddddddd~~~~~                          |
  22.0 |~~hhhhh-hh------------------dddxdddddd-dddddddd------------p-pp----xdddddddddd-ooooohh-------sssssaddddddddddd~~~~                          |
       |~~hhhhhh-hhhhp-------------dddddd--------dddd-----------------------pdppppddddooooooMh--------ssssdddddddddddd~~~~                          |
       |~~hhhhhhMhhhhhhh-------------------------------------------------ppp-pggppdxdd-oooooMh---------sssdddddddddddd~~~~~                         |
       |~~~hhhMMMMhhhhhh------------------------------------------------------pggpddd--ooMMh---------sssssdddddddddddd~~~~~~                        |
  20.0 |~~~hhhhhhhhhhhhh-------------------hhhhMMh---------h-------------------pggpppp--hha--ddddd-dddddddddddddddddddc~~~~~~                       |
       |~~~hhhhhhhhhhhh---------------hhhhhhhMMMMMhh-------------------xx-------pggpp-----a-ddddddddddddddddddddddddddd~~~~~~~                      |
       |~~~~hhhhhhhhhhhhhhhhhhh---hhhhhhhhhhhhhhhMMMhh------------------------h-hhhp--------ddddddddddddddddddsasdddddd~~~~~~~                      |
       |~~~~hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhMMMMhh-----------------------hhhhMMpp------ddddddddddddddddddsssddddddd~~~~~~~                     |
  18.0 |~~~~hhhTThTTThhhhhhhThhhhhhhhhhhhhhhhhhhhhhMMMh----------------------hhhhhhhhhp------ddddddddddddddddsssssdddddddc~~~~~~                    |
       |~~~~hTTTTTTTTTTTTTTTTTTThhhThhhhhhhhhhhhhhhMMMMh-h------------------hhhhhhhhhhhh-----dddddddddddd---ddssddddddd--d~~~~~~~                   |
       |~~~hTTTTTTTTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhhhMMMhh------------------hhhhhhhhhhhhh-----dddddddddd-------sddddddddd--~~~~~~~                   |
       |~~~TTTTTTTTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhhhhhMMMh------------------hhhhhh--hhhhh---------ddddd------dddddddddddd--d~~~~~~~                  |
  16.0 |~~~TTTTTTTTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhhhhhhMMMh-----------------hhhh-----hhhhppp--------d--------ddddddddddd----~~~~~~                   |
       |~~TTTTTTTTTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhhhhhhhMMMhh---------------hhh-----hhhhhMMp-----------------ddddddda------dc~~~~~                  ~|
       |~TTTTTTTTTTTTTTTTTTTTTTThhhhhhhhhhhh-h-hhhhhhhTMMMMh-----------d----h----hhhhhhhMMhh---------------dddddd-------dddddc~~~~             ~~~~~|
       |~~TTTTTTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhhhhhhhhhhTMMMMh---------xxx------hhhhhhhhhhMMh----------------dd----------ddddddd~~~            ~~~~~~|
  14.0 |~~~TTTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhhhhhhhhhhhhhMMMMh--------xxxx----hhhhhhhhhhhhhMh----------------d-----------dddddddd~~         ~~~~~~~~~|
       |~~~TTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhhhhhhhhhhhhhhhhMMh--------dxxx---hhhhhhhhhhhhhhhhp---------------------------pdddddd-d~~    ~~~~~~~~~~~~~|
       |~~vTTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh---------x-------hhhhhhh-hhhhhMhhh-----------dd-----------pp-----dd-d~  ~~~~~~~~~~~~~~~|
       |~~~TTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh------------------------hhhhhhMMMMMMh-------dd------------pppp-------d~~~~~~~~~~~~~~~~~|
  12.0 |~~~~~TTTTTTTTTTTTTTTTThTThhhhhhhhhhhhhhhhhhhhhhhMMMhMhhh---------d----------hhhhhhhhhhMhhhh--------------hhhhMMhppp-------~~~~~~~~~~~~~~~d~~|
       |~~~~~vTTTTTTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhMMhhhMMMTTMMMhhh-----------------hhhhhhhhhhhhh-h------------hhhhhTTMMhhpp--------~~~~~~~~~~d----~~|
       |~~~~~~vTTTTTTTTTTTTTTTTTTTThhhhhhhhhhhhhhhMMMhhhooTTMMMh-----------------hhhhhhhhhhh--------hhhhMMMMMMTTTTTMMMMphhp---------~~~-----------~~|
       |~~~~~~~TTTTTTTTTTTTTTTTTTTTThhhhhhhhhhhhhhMMMhoooooTMMMh-----------------hhhhhhhhh---------hhhhMMMMMMMTTMMTTTMMMMhhp----------------------~~|
  10.0 |~~~~~~~~~TTTTTTTTTTTTTTTTTTTThhhhhhhhhhhhhTMThoooTTTMMMhhhh--------------hhhh-----hhhhhhhhhhhTTTTTTMMMMMMMMMMMMMMpp-----------------------~~|
       |~~~~~~~~~TTTTTTTTTTTTTTTTTTTThhhhhhhhhhhhhTMMTooTTThhMhhhhhhh-------------------hhhhhhTTTTThTTTTTTTTTTMMMMMMMMMMppp-----------------------~~|
       |~~~~~~~~~~TTTTTTTTTTTTTTTTTTTThhhhhhTThhhhTTTTTTTTTThhhhhhhhhhhhhh-----------hhhhhhooooTTTTTTTTTTTTTTTTTMMMMpMMMMph----------------------~~~|
       |~~~~~~~~~~TTTTTTTTTTTTTTTTTTTTTThhhTTThhhTTTTTTMTTTMTTTTTTTThhhhh----------hhhhhhhooooooooTTTTTTTTTTTTTTTTMMMMMMpphp--------------------~~~~|
   8.0 |~~~~~~~~~~ TTTTTTTTTTTTTTTTTTTTTThhTTThhhTTTTTTMMMMTTTTTTTTThhhhh---------hhhMhhhoooooooooTTTTTTTTTTTTTTTTMMMMMMMpp---------------------~~~~|
       |~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTMhhhMhhh---hhhhhhMMMhoooooooooTTTTTTTTTTTTTTTTTMMMMMMppp-------------------~~~~~|
       |~~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTMMhhhhhhhhhhhhhhhhTTMMMMTooooooTTTTTTTTTTTTTTTTTTMTTMMMppph------------------~~~~~|
       |~~~~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTTTTTTTTT~~TTTTTTTTTTTTMMTThhhhhhhhhhhhhhTTTTTMMMMTTTTTTTTTTTTTTTTTTTTTTTTMTMMMMMMhhhhhh--hhhh-------~~~~~~|
   6.0 |~~~~~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTTTT~~~~~~~~TTTTTTTTTTMTTTTTTTTTTTTThhTTTTTTTTTMTTTTTTTTTTTTTTTTTTTTTTTTTTTMTMMMMMhhhhhhhhhhhh------~~~~~~|
       |~~~~~~~~~~~~~~~~~TTTTTTTTTTTTTTTTTT~~~~~~~~~~~~TTTTTTTTTMTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTMMTMThhhhhhhhhhhh----~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~TTTT~~~~~~~~T~~~~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTMMTTThhhhhhhhhhhh---~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TT~~~~TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT TTTTTTTTTTTTTTTTMMTThhhhhhhhhhhhhh--~~~~~~~~|
   4.0 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT  T   TTT TTMMTTTTTTTTTTThhhhhhhhhhhhh--~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT             TTMTTTTTTTTTThhhhhhhhhhhhhh-~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~T TTTTTTTTTT T T  TTTTTTT  T                  TTTTTTTTTTTThhhhhhhhhh-hhh-~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~T  T   T           T                              MTTTTTTThhhhhhhhhh-----~~~~~~~~~~~~|
   2.0 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~T                                                   TTMTThhhhhhhhh-----~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~T                                                   TTMTThhhhhh-------~~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~T                                                         h    ------~~~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~T                                                                 -~~~~~~~~~~~~~~~~~~|
   0.0 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TT                                                                 ~~~~~~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TT                                                                 ~~~~~~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TT                                                                ~~~~~~~~~~~~~~~~~~~~|
       |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TT                                                               ~~~~~~~~~~~~~~~~~~~~~|
              '         |         '         |         '         |         '         |         '         |         '         |         '         |   
                        -10                 0                   10                  20                  30                  40                  50  
```

## 3. Répertoire des lieux

Coordonnées [longitude, latitude] en degrés décimaux ; « case » = colonne·ligne de la grille ci-dessus.

### Mers et golfes

| Élément | geo_id | Position | Case | Données |
|---|---|---|---|---|
| Mer Halakhel (Qibṣān) | `GEO_MER_HALAKHEL` | -7.99° à 28.85° E ; 23.01° à 31.17° N | — | 1 280 030 km² ; 3640 km O-E ; niveau -20 m ; prof. max 1439 m ; 47 îles |
| golfe de Serek (nom de travail) | — | [-1.73, 30.58] | c32·l14 | golfe nord derrière la passe Khreth-na-Serek |
| Méditerranée | `GEO_EXT_MEDITERRANEE` | [18.0, 34.3] | c72·l7 | étiquette |
| Océan Atlantique | `GEO_EXT_ATLANTIQUE` | [-22.0, 25.0] | — | étiquette |
| Mer Rouge | `GEO_EXT_MERROUGE` | [38.4, 19.2] | c112·l37 | étiquette |
| Océan de l'Est | `GEO_EXT_OCEAN_EST` | [50.0, 4.0] | c136·l68 | étiquette |
| Ku-jálima-rir | `GEO_GLF_KUJALIMARIR` | [-5.0, 3.3] | c26·l69 | étiquette |
| Golfe Jálondù | `GEO_GLF_JALONDU` | [0.5, 4.75] | c37·l66 | étiquette |

### Lacs

| Lac | geo_id | Centre | Case | Données |
|---|---|---|---|---|
| Tùmázì | `GEO_LAC_TUMAZI` | [24.77  7.66] | c85·l60 | 92,194 km² ; 620 m ; prof. 601 m ; 22.24-27.47° E, 6.51-9.1° N |
| Akhtir | `GEO_LAC_AKHTIR` | [22.61  21.31] | c81·l33 | 44,753 km² ; 1200 m ; prof. 592 m ; 21.2-24.17° E, 20.22-22.23° N |
| Mopámà | `GEO_LAC_MOPAMA` | [6.08  10.1] | c48·l55 | 28,555 km² ; 800 m ; prof. 255 m ; 4.97-7.26° E, 9.13-11.03° N |

### Chaînes

| Chaîne | Longueur | Point culminant | Case | Extrémités |
|---|---|---|---|---|
| \|\|Urumati-halekh | 1797 km | 4350 m à [-6.54, 22.39] | c22·l31 | [-16.3, 20.0] → [0.6, 23.75] |
| !Okheti | 190 km | 3454 m à [0.38, 23.39] | c36·l29 | [0.0, 24.45] → [1.2, 23.15] |
| \|\|Urumati-k'ara | 2881 km | 5350 m à [17.81, 20.33] | c71·l35 | [0.6, 23.75] → [24.4, 13.3] |
| GEO_ORO_URUMATI_KARA (segment 24.4, 13.3) | 1444 km | 3285 m à [23.34, 14.37] | c82·l47 | [24.4, 13.3] → [36.6, 8.7] |
| \|\|Urumati-lóngò | 1736 km | 3454 m à [0.38, 23.39] | c36·l29 | [0.9, 23.6] → [9.2, 10.2] |
| GEO_ORO_URUMATI_LONGO (segment 5.6, 16.6) | 392 km | 2056 m à [5.6, 16.59] | c47·l42 | [5.6, 16.6] → [8.4, 18.9] |
| GEO_ORO_URUMATI_LONGO (segment 8.0, 12.9) | 324 km | 2228 m à [7.82, 13.19] | c51·l49 | [8.0, 12.9] → [5.6, 11.2] |
| GEO_ORO_URUMATI_LONGO (segment 2.6, 20.4) | 259 km | 2689 m à [2.51, 19.55] | c41·l36 | [2.6, 20.4] → [0.7, 18.9] |
| \|\|Urumati-qoyra | 2020 km | 4673 m à [38.38, 13.22] | c112·l49 | [38.8, 15.4] → [48.5, 10.6] |
| GEO_ORO_COTIERE_N (segment 6.2, 36.2) | 2622 km | 1631 m à [8.33, 35.61] | c52·l4 | [6.2, 36.2] → [29.5, 30.6] |
| Mù-wúlè | 355 km | 1800 m à [3.79, 9.98] | c43·l56 | [3.4, 11.7] → [4.2, 8.6] |
| Mù-dárhòbì | 289 km | 2100 m à [7.2, 7.71] | c50·l60 | [5.5, 8.15] → [7.9, 8.2] |
| Kù-kɨ́bò | 287 km | 1400 m à [21.81, 6.62] | c79·l62 | [20.5, 7.6] → [22.7, 6.25] |
| \|'Ara-Sukhì (`GEO_ORO_ARASUKHI`) | — | [17.8, 20.3] | c71·l35 | massif ou site |
| !Ayk-ma-‖Ixa (`GEO_SIT_AYKMAIXA`) | — | [36.9, 9.1] | c109·l57 | massif ou site |

### Fleuves nommés

| Fleuve | geo_id | Longueur dessinée | Amont | Aval | Cases amont → aval |
|---|---|---|---|---|---|
| Tira-ñara / Tanāḥil | `GEO_FLV_TANAHIL` | 1755 km | [37.18, 11.04] | [32.49, 15.63] | c110·l53 → c100·l44 |
| Buhlela | `GEO_FLV_BUHLELA` | 1135 km | [39.27, 11.97] | [33.98, 17.67] | c114·l52 → c103·l40 |
| Tira-qoyra / Abnuḥīl | `GEO_FLV_ABNUHIL` | 2446 km | [32.49, 15.63] | [30.86, 27.6] | c100·l44 → c97·l20 |
| Šafāqil | `GEO_FLV_ABNUHIL_SAFAQIL` | 768 km | [30.88, 27.63] | [30.4, 31.44] | c97·l20 → c96·l13 |
| Abnīqa | `GEO_FLV_ABNUHIL_ABNIQA` | 262 km | [30.78, 27.6] | [28.3, 27.6] | c97·l20 → c92·l20 |
| \|Na-madikh / Madīlan | `GEO_FLV_MADIKH` | 808 km | [5.7, 24.25] | [12.8, 24.75] | c47·l27 → c61·l26 |
| Imikhrel | `GEO_FLV_IMIKHREL` | 536 km | [4.6, 24.0] | [0.49, 25.15] | c45·l28 → c36·l25 |
| Ehukhtal | `GEO_FLV_EHUKHTAL` | 918 km | [-0.1, 24.5] | [-7.69, 27.22] | c35·l27 → c20·l21 |
| \|Na-khuwel / Ḥawqal | `GEO_FLV_HAWQAL` | 1087 km | [19.9, 19.7] | [26.72, 25.2] | c75·l36 → c89·l25 |
| \|Na-khuwel-ra | `GEO_FLV_HAWQAL_RA` | 635 km | [22.4, 17.7] | [23.3, 20.8] | c80·l40 → c82·l34 |
| \|Na-khuwel-ɨn | `GEO_FLV_HAWQAL_IN` | 292 km | [27.0, 21.4] | [25.93, 23.62] | c90·l33 → c87·l28 |
| émissaire du Mopámà (nom en lacune) | `GEO_FLV_EMISSAIRE_MOPAMA` | 653 km | [5.0, 9.45] | [0.98, 5.93] | c46·l57 → c37·l64 |

### Détroits, goulets, débouchés, deltas, estuaires

| Nom | geo_id | Position | Case |
|---|---|---|---|
| Khreth-na-Serek | `GEO_DET_KHRETHNASEREK` | [-1.85, 29.75] | c32·l16 |
| Hlom-khetal | `GEO_DET_HLOMKHETAL` | [-6.9, 27.65] | c22·l20 |
| Imekh-stom | `GEO_DET_IMEKHSTOM` | [0.2, 25.8] | c36·l24 |
| Abnīqa | `GEO_DET_ABNIQA` | [28.35, 27.6] | c92·l20 |
| Ḥawqil | `GEO_DET_HAWQIL` | [26.85, 25.35] | c89·l25 |
| Šafāqil | `GEO_DET_SAFAQIL_PASSE` | [31.2, 31.5] | c98·l13 |
| Šafāqil | `GEO_DLT_SAFAQIL` | [31.0, 30.9] | c98·l14 |
| Akhidalet | `GEO_EST_AKHIDALET` | [-8.2, 27.0] | c19·l22 |
| Tawālmaz | `GEO_EST_TAWALMAZ` | [13.6, 24.55] | c63·l26 |
| delta du Mopámà | `GEO_DLT_MOPAMA` | [1.3, 5.75] | c38·l64 |

### Régions et archipels

| Nom | geo_id | Position | Case |
|---|---|---|---|
| Désert du Sumdan | `GEO_DES_SUMDAN` | [9.5, 31.4] | c55·l13 |
| Interfluve oriental | `GEO_ZON_INTERFLUVE_E` | [29.7, 25.6] | c95·l24 |
| Staur-Khlōr | `GEO_ARC_STAURKHLOR` | [-24.0, 18.0] | — |
| Khlōr-Naw | `GEO_ILE_KHLORNAW` | [-24.38, 14.95] | — |
| Li-sèk-dì | `GEO_ARC_LISEKDI` | [-1.7, 4.1] | c32·l67 |

## 4. Les 48 cols

| geo_id | Nom | Altitude | Position | Case | Groupe | Chaîne | Passage | Hiver | Ouverture (mois) |
|---|---|---|---|---|---|---|---|---|---|
| `GEO_COL_001` | Abnī-tɨra | 2800 m | [23.96, 15.332] | c83·l45 | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | haute_route | hiver_blanc | 6-10 |
| `GEO_COL_002` | Ṭanīkhūr | 3200 m | [21.319, 17.798] | c78·l40 | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | haute_route_extreme | hiver_blanc | 7-8 |
| `GEO_COL_003` | Ṣabūl-tɨkh | 2900 m | [15.678, 20.524] | c67·l34 | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | haute_route | hiver_blanc | 6-10 |
| `GEO_COL_004` | Ḥamīr-ɨlkh | 3000 m | [23.01, 15.768] | c82·l44 | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | haute_route | hiver_blanc | 7-9 |
| `GEO_COL_005` | Qaṣūl-tɨra | 2700 m | [20.26, 18.55] | c76·l38 | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | secondaire | hiver_blanc | 6-10 |
| `GEO_COL_006` | Maḥēl-!ara | 2950 m | [21.777, 16.057] | c79·l43 | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | haute_route | hiver_blanc | 7-9 |
| `GEO_COL_007` | Ṭubayl | 2850 m | [24.178, 13.441] | c84·l49 | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara | haute_route | hiver_blanc | 6-10 |
| `GEO_COL_008` | Šaqra-t'em | 2400 m | [24.503, 12.481] | c85·l51 | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | haute_route | hiver_blanc | 5-10 |
| `GEO_COL_009` | Kurel-ahek | 2150 m | [25.553, 12.554] | c87·l50 | Šamqiriyyūn ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | principal | cycle_mixte | 4-11 |
| `GEO_COL_010` | T'araq-ɨnkh | 2400 m | [34.758, 8.873] | c105·l58 | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | secondaire | cycle_mixte | 5-10 |
| `GEO_COL_011` | K'elis-‖ara | 2500 m | [32.099, 9.98] | c100·l56 | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | secondaire | hiver_blanc | 5-10 |
| `GEO_COL_012` | Q'ami-tɨra | 2300 m | [35.03, 7.796] | c106·l60 | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | secondaire | cycle_mixte | 5-10 |
| `GEO_COL_013` | P'etsul-!ama | 2600 m | [30.075, 10.977] | c96·l54 | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | haute_route | hiver_blanc | 5-10 |
| `GEO_COL_014` | T'iqur-ɨlkh | 2700 m | [36.183, 8.701] | c108·l58 | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | haute_route | hiver_blanc | 6-10 |
| `GEO_COL_015` | S'akum-\|ena | 2200 m | [35.665, 7.59] | c107·l60 | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | secondaire | cycle_mixte | 4-11 |
| `GEO_COL_016` | Q'usa-\|\|ema | 2100 m | [35.432, 8.586] | c106·l58 | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | principal | cycle_mixte | 4-11 |
| `GEO_COL_017` | T'amr-khɨna | 2450 m | [33.608, 9.527] | c103·l56 | Qoyra-ña-ra ↔ Tɨrakh | \|\|Urumati-k'ara (prolongement SE) | secondaire | cycle_mixte | 5-10 |
| `GEO_COL_018` | Ku-Pámà-Rikh-te | 1600 m | [-12.952, 20.913] | c10·l34 | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | bas_col | hiver_gris | 4-12 |
| `GEO_COL_019` | Ku-Mázì-Klek-te | 1900 m | [-14.336, 20.402] | c7·l35 | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | principal | hiver_gris | 4-11 |
| `GEO_COL_020` | Kù-Lábà | 1700 m | [-12.405, 20.938] | c11·l34 | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | bas_col | hiver_gris | 4-12 |
| `GEO_COL_021` | Ku-Sikal-Ktet-te | 1800 m | [-10.915, 21.194] | c14·l33 | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | bas_col | hiver_gris | 4-11 |
| `GEO_COL_022` | Ku-Dúma-te | 1650 m | [-13.729, 20.559] | c8·l34 | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | bas_col | hiver_gris | 4-12 |
| `GEO_COL_023` | Kù-Sepá | 1750 m | [-11.623, 21.139] | c12·l33 | Ba-mbaro ↔ Halaktim | \|\|Urumati-halekh | bas_col | hiver_gris | 4-12 |
| `GEO_COL_024` | Ku-Pámà-Tɨra-te | 2000 m | [7.88, 13.059] | c51·l49 | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | principal | cycle_mixte | 4-11 |
| `GEO_COL_025` | Lémakhɨ | 2200 m | [6.604, 14.407] | c49·l47 | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | secondaire | cycle_mixte | 4-11 |
| `GEO_COL_026` | Ku-Sogo-!Ara-te | 2100 m | [6.311, 15.863] | c48·l44 | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | secondaire | cycle_mixte | 4-11 |
| `GEO_COL_027` | Kù-Pété-‖Eni | 1900 m | [3.581, 19.229] | c43·l37 | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | bas_col | hiver_gris | 4-11 |
| `GEO_COL_028` | Ku-Ténɨlkh-te | 2300 m | [4.886, 17.745] | c45·l40 | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | secondaire | cycle_mixte | 5-10 |
| `GEO_COL_029` | Ku-Darikámba-!Ari-te | 2400 m | [2.313, 19.76] | c40·l36 | Ba-mbaro ↔ Tɨrakh | \|\|Urumati-lóngò | secondaire | hiver_blanc | 5-10 |
| `GEO_COL_030` | Ktalep-tɨra | 2600 m | [1.194, 23.154] | c38·l29 | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | haute_route | hiver_blanc | 5-10 |
| `GEO_COL_031` | Tkrilan-ɨkh | 2800 m | [-5.028, 22.903] | c25·l30 | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | haute_route | hiver_blanc | 6-10 |
| `GEO_COL_032` | Hlelak-!uri | 2900 m | [-2.117, 22.914] | c31·l30 | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | haute_route | hiver_blanc | 6-9 |
| `GEO_COL_033` | Rekal-‖ene | 2500 m | [-3.648, 23.157] | c28·l29 | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | secondaire | hiver_blanc | 5-10 |
| `GEO_COL_034` | Ktamar-khɨ | 3000 m | [4.313, 23.601] | c44·l28 | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | haute_route | hiver_blanc | 7-9 |
| `GEO_COL_035` | Kraloth-!enu | 2700 m | [-1.477, 23.34] | c33·l29 | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | haute_route | hiver_blanc | 6-10 |
| `GEO_COL_036` | Narkh-ɨlkh | 2550 m | [7.442, 23.081] | c50·l29 | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | secondaire | hiver_blanc | 5-10 |
| `GEO_COL_037` | Kurahek | 2100 m | [-9.494, 21.843] | c17·l32 | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | principal | cycle_mixte | 4-11 |
| `GEO_COL_038` | Hlenik-k'eso | 2000 m | [-8.698, 22.642] | c18·l30 | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | principal | cycle_mixte | 4-11 |
| `GEO_COL_039` | Pēlakh-t'sira | 1750 m | [-9.927, 21.123] | c16·l33 | Halaktim ↔ Tɨrakh | \|\|Urumati-halekh | bas_col | hiver_gris | 4-12 |
| `GEO_COL_040` | Namkural | 1800 m | [2.838, 23.089] | c41·l29 | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | bas_col | hiver_gris | 4-12 |
| `GEO_COL_041` | Krathal-t'iq | 2300 m | [2.366, 21.929] | c40·l32 | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | secondaire | cycle_mixte | 5-10 |
| `GEO_COL_042` | Ktalor-p'es | 2600 m | [8.376, 22.98] | c52·l30 | Halaktim ↔ Tɨrakh | \|\|Urumati-k'ara | haute_route | hiver_blanc | 5-10 |
| `GEO_COL_043` | Halek-t'ama | 1900 m | [-0.344, 23.746] | c35·l28 | Halaktim ↔ Tɨrakh | !Okheti | bas_col | hiver_gris | 4-11 |
| `GEO_COL_044` | ʿUbayl-t'iq | 2000 m | [39.339, 14.45] | c114·l47 | Šamqiriyyūn ↔ Qoyra-ña-ra | \|\|Urumati-qoyra (escarpement) | secondaire | hiver_gris | 4-11 |
| `GEO_COL_045` | Ḥazīr-k'ama | 2100 m | [38.749, 15.3] | c113·l45 | Šamqiriyyūn ↔ Qoyra-ña-ra | \|\|Urumati-qoyra (escarpement) | secondaire | cycle_mixte | 4-11 |
| `GEO_COL_046` | Ṣamar-q'ut | 2200 m | [38.462, 14.05] | c112·l47 | Šamqiriyyūn ↔ Qoyra-ña-ra | \|\|Urumati-qoyra (escarpement) | secondaire | cycle_mixte | 4-11 |
| `GEO_COL_047` | Rafīq-t'sal | 2300 m | [37.729, 13.0] | c111·l50 | Šamqiriyyūn ↔ Qoyra-ña-ra | \|\|Urumati-qoyra (escarpement) | secondaire | cycle_mixte | 5-10 |
| `GEO_COL_048` | Nrelat-q'urm | 2200 m | [37.777, 11.85] | c111·l52 | Šamqiriyyūn ↔ Qoyra-ña-ra | \|\|Urumati-qoyra (escarpement) | secondaire | cycle_mixte | 4-11 |

## 5. Façades de la mer Halakhel

Voir `ALIGNEMENT_CORPUS.md` §4 pour les segments de rivage et les lieux de LIEUX qui s'y rattachent.

