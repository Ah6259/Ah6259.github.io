# Mémoire du projet — Portail clicvia.com (dépôt Ah6259/Ah6259.github.io)

Fichier lu automatiquement par Claude Code au début de chaque session dans ce dossier. Dépôt PUBLIC : rien de personnel ni de secret.
Le détail de chaque fonction est dans **README.md** (à tenir à jour en même temps que ce fichier, à chaque « update workflow »).

## Qui et comment travailler
- Propriétaire : Ahmed (compte GitHub `Ah6259`), débutant : expliquer simplement, **en français**. Toujours demander avant d'installer
  un logiciel. Tout doit être automatique. **Toujours `git pull` avant de travailler** (Ahmed modifie aussi depuis son téléphone).
- Commits : `user.name Ah6259`, `user.email 200752748+Ah6259@users.noreply.github.com`.
- Règles communes à tous les sites : `regles communes a tous les sites.md` du dépôt PRIVÉ `Ah6259/projets-ahmed` (procédure d'un nouveau
  site : `nouveau site - procedure.md`). Toute remarque d'Ahmed sur un site s'applique à tous.

## Le site
- Adresse **https://clicvia.com/** (CNAME) ; trois langues : `/`, `/ar/`, `/en/`, **fabriquées par `python tools/construire.py`**
  (gabarit `tools/gabarit.html`, listes `SITES`, `THEMES`, `TEXTES`) : **ne jamais modifier index.html à la main**.
  Nouveau site : une ligne dans `SITES` + son icône `assets/sites/`, une ligne `Sitemap:` dans robots.txt, puis construire.
- `robots.txt` COMMUN à tous les sites (robots d'IA interdits) ; clé IndexNow à la racine (ne pas supprimer) ; fichier Google à garder.
- Robots : `indexnow` (14h37), `facebook` (publications de la page Clicvia), `facebook-rafraichir` (aperçus des rapports), `tests.yml`.
  Secrets `FB_PAGE_ID`, `FB_PAGE_TOKEN` (jamais écrits ici).

- **Page « Comment fonctionne le site ? »** (25/10/2026) : `a-propos/`, `ar/a-propos/`, `en/a-propos/`, fabriquées par `construire.py`
  (textes dans `A_PROPOS`, fonction `page_a_propos()`), lien dans le pied de page de toutes les pages (`pied()`), dans le plan du site.
- **RÈGLE D'AHMED (25/10/2026, règle commune § 44) : la page Comment fonctionne le site ? est mise à jour à CHAQUE modification visible,
  dans le même envoi (3 langues) ; test FONCTIONS dans `tools/test_portail.mjs`** (nouvelle fonction = une ligne dans FONCTIONS + son
  explication dans `A_PROPOS`, sinon test rouge = publication bloquée).

## Tests (avant tout envoi)
- `node tools/test_portail.mjs`, `node tools/test_video.mjs`, `python3 tools/visiteur_simule.py` (copie IDENTIQUE de l'outil commun
  `outils communs/visiteur-simule/` de projets-ahmed : liens morts, page trop large, « NaN », et depuis le 19/10/2026 le **contrôle des
  espaces** de la règle commune § 29 : éléments qui se touchent, espaces inégaux, bouton pas centré). 0 anomalie avant publication.

## Historique court
- 19/10/2026 : CLAUDE.md créé (avant, la mémoire du portail n'était que dans README.md) ; contrôle des espaces installé, 0 anomalie.
- 25/10/2026 : page « Comment fonctionne le site ? » (3 langues) + test FONCTIONS (règle commune § 44).
- 08/11/2026 : plan SEO d'Ahmed appliqué au portail (phase 2 ; contrôle commun `outils visibilite/controle_seo.mjs`, plan
  `consignes des taches/seo-portail.md` de projets-ahmed) : `titre_seo()` / `desc_seo()` dans `tete_page()` (titre <= 70 caractères, coupé à
  « : » ; description <= 165, coupée en fin de phrase) pour les 3 accueils et les 3 pages « Comment fonctionne le site ? » ; description
  de la page vidéo raccourcie (tools/page_video.json). Avant : titres de 83 à 125 caractères, descriptions de 237 à 327 (Google les coupait).
- 08/11/2026 : `node tools/page_video.mjs` seul REFAIT video/index.html SANS la liste des 21 vidéos des sites (robot tests rouge à 09:00) : après tout changement de la page vidéo, lancer `python tools/construire.py` (qui replace la liste entre ses repères), puis les deux tests.

- 09/11/2026 : Mon agent immobilier passe de 2 à 4 publications Facebook sur 10 jours (« publication automatique », Ahmed), comme l'Immobilier :
  une place de Concours et une de Prix des Eaux (chacun en garde une) dans `TOUR` de tools/facebook.mjs. Sa 1re publication est sortie le
  09/11 à 14h49 (robot du matin lancé en retard par GitHub). Changer `TOUR` décale le compteur de pages des autres sites (une page peut repasser).
- **09/11/2026 — robot `monagent-post` (demande d'Ahmed : « une publication Instagram et Facebook entre les deux publications de l'Immobilier,
  chacune différente, et totalement différente de celles de l'Immobilier : personne ne doit faire le lien entre les deux sites »)** :
  `tools/monagent_post.mjs`, chaque jour 13h20 (entre les Reels de 8h20 et 18h20). UNE image 1080 × 1350 par jour = une CONVERSATION avec
  l'agent : la question d'un visiteur (français, arabe ou tunisien en lettres latines, ~1 200 questions possibles) et la réponse chiffrée
  calculée sur les vraies annonces du site (donnees/index.js + assets/comprendre.js de monagent.clicvia.com, même filtre strict que
  agent.js) ; 5 mises en page (chat, recherche, sms, fiche, ticket) × 8 palettes (bleus / encre, jamais terre cuite, sable ni or) × 4 polices
  (Plus Jakarta Sans, Manrope, Sora, Outfit) × 12 accroches, mémoire `donnees/monagent-posts.json` (rien de commun avec les 4 derniers posts,
  gouvernorat jamais repris sur 6 jours, écriture différente de la veille). Légende : accroche-question, chiffres, lien qui ouvre la réponse
  (`?q=` + utm_source / utm_medium / utm_campaign : les clics se lisent dans GoatCounter), 10 mots-dièse au plus. INTERDITS (vérifiés avant
  publication + test) : « Immobilier Tunisie », « Clicvia » (hors l'adresse monagent.clicvia.com), « IA ». Image enregistrée dans `monagent/`
  et servie par clicvia.com ; Facebook = page Clicvia (secrets FB_*) ou page propre (MONAGENT_FB_PAGE_ID / _TOKEN) ; **Instagram seulement avec
  un compte PROPRE à Mon agent (secret MONAGENT_IG_USER_ID)** : le compte @immobilier.clicvia ferait le lien entre les deux sites — tant qu'il
  manque, journal « compte propre à créer », pas de rouge (gestes d'Ahmed : `GERER SANS CLAUDE/mon agent immobilier.md`). Test
  `tools/test_monagent_post.mjs` (9, dans tests.yml et dans le robot ; sabotage « IA » dans l'image : attrapé). Leçon : Chrome sans écran ne
  dessine pas les ~85 derniers pixels de la fenêtre → capture plus haute puis recadrage (la ligne du bas était invisible).
- 09/11/2026 (nuit) : design des publications de Mon agent refait avec l'outil Design de Claude (canevas « Publications Mon agent »,
  https://claude.ai/artifact/PPCp6kHvkwV6ZwYDyhjN8B : 5 tableaux = les 5 mises en page, mêmes couleurs et textes que le robot ; Ahmed peut y
  commenter) ; reporté dans tools/monagent_post.mjs : point « en ligne » + avatar « M » devant les bulles de l'agent, curseur de saisie et
  pastilles « français · عربي · tounsi » sous la barre de recherche (mise en page en colonne : plus de chevauchement quand la question
  tient sur deux lignes). Un changement de design = le canevas ET le robot, ensemble.
- **11/11/2026 — publications de Mon agent des 10 et 11/11 PERDUES : jeton d'une heure** (le dernier « Generate Access Token » du 10/11 à
  00h40 n'était pas étendu ; la page publiée à 00h58 l'a été dans l'heure, puis « Session has expired », code 190 : même panne qu'au 28/10
  pour Clicvia). Réparé : `examinerJeton()` (Facebook /debug_token) AVANT chaque publication → message clair « JETON D'UNE DURÉE LIMITÉE :
  refaire l'étape Étendre » au lieu d'une erreur illisible ; entrée `verifier = 1` du robot (jeton durable, autorisations, page et Instagram
  reliés, sans rien publier), comme reels.yml. Horaires : GitHub a lancé le passage de 13h20 avec 7 h de retard deux jours de suite
  (19h42 UTC) → cron 12:17 UTC (minute inhabituelle) + 2e chance 14:41 UTC (déjà publié = rien à faire ; échec du midi = nouvel essai).
  Le jeton est à REFAIRE par Ahmed (étape « Étendre » puis débogueur « Expiration : Jamais » avant de coller le secret).
- **17/11/2026 — page 404 qui CHERCHE (Ahmed : « Page introuvable » fait partir le visiteur)** : `assets/404.js` affiche « Recherche de la
  page… », lit la liste des sites sur l'accueil (un nouveau site est trouvé seul), demande l'adresse à chaque sous-domaine (HEAD ; GitHub
  Pages répond `Access-Control-Allow-Origin: *`) et y renvoie dès qu'un site l'a ; « Page introuvable » seulement si aucun ne l'a (8 s au plus).
  CSP de 404.html : `connect-src 'self' https://*.clicvia.com`. Cas d'origine : `clicvia.com/fiche/…` = statistique GoatCounter d'un annuaire
  comptée SANS son préfixe (compteur lancé avant page.js, réparé dans le moteur des annuaires). Test dans `tools/test_portail.mjs`.
- **18/11/2026 — Mon agent : zéro vue sur Instagram (Ahmed) → REEL + heure garantie.** Causes : (1) une PHOTO n'est montrée qu'aux abonnés
  (compte neuf = aucun), alors que les REELS de l'Immobilier sont proposés à des inconnus ; (2) GitHub lance ce dépôt avec 7 à 9 h de retard :
  les publications de « 13h20 » sortaient entre 20h et minuit ; (3) 4 publications seulement (10-14/11 perdues, jeton). Réparé dans
  `tools/monagent_post.mjs` : l'image du jour devient aussi un Reel 1080 × 1920 de 9 s (fond de la palette, zoom lent, fondu, musique du
  domaine public Vivaldi RV 425 `tools/monagent/musique.m4a` + licence, extrait et sens du zoom changeant chaque jour ; jamais le Bach de
  l'Immobilier), couverture = l'image JPEG ; Reel refusé ou non fabriqué = la photo est publiée (rien de perdu). Facebook : photo comme avant
  (lien cliquable). Heure : 3 lancements tôt (02:13, 04:47, 08:23 UTC) et étape « Attendre l'heure de publication » (PHASE=attendre, fonction
  `attente()`) jusqu'à 12:20 UTC = 13h20 à Tunis ; après 20:30 UTC pas de publication (journal, pas de rouge) ; lancement à la main sans
  attente ; timeout 360 min (dépôt public : gratuit). Tests ajoutés (heure, format du Reel, musique propre, fabrication si ffmpeg est là).
  Leçon (essai du 18/11) : une sortie d'étape SAUTÉE est vide, et GitHub compare vide == '0' (conversion en nombre) → toutes les étapes
  sautées ; sortie en `oui`/`non`. Essai sur GitHub ensuite : 12/12 vérifications, Reel fabriqué. Règle : jamais 0/1 dans une sortie testée par `!=`.
- **18/11/2026 (suite, Ahmed : « l'Immobilier publie aussi sur Facebook, pas Mon agent »)** : Mon agent publiait bien chaque jour sur SA page
  Facebook (neuve, presque sans abonnés) mais en PHOTO, montrée aux seuls abonnés ; l'Immobilier publie un REEL sur la page Clicvia (montré aux
  inconnus). Maintenant le Reel du jour part aussi sur la page Facebook de Mon agent (`publierReelFacebook`, /video_reels comme reels.py, lien
  cliquable dans le texte) ; Reel refusé = photo. Test ajouté. À vérifier par Ahmed : la publication se voit-elle sans être connecté (application
  Meta en mode développement = publications cachées au public).
- **18/11/2026 — REFONTE DE L'ACCUEIL (Ahmed : analyse stratégique de Clicvia + design de niveau agence)** : bandeau marine + motif du logo,
  recherche instantanée (`assets/accueil.js`, `MOTS`), 9 catégories par besoin (`THEMES`, `THEMES_COURT`, `THEMES_SOUS`, ordre = logement
  d'abord), menu des catégories collant, barre du haut et pied communs (`barre()`, `pied()`), style unique dans `tools/gabarit.html`.
  Adresses, liens des 20 sites, H1, titres et descriptions SEO INCHANGÉS. Aperçu de partage : nombre de sites calculé (disait « 18 »).
  Analyse stratégique écrite : `etude strategie clicvia 2026-11-18.md` de projets-ahmed. Leçon : le test FONCTIONS ignorait en silence une
  fonction dont le repère avait disparu (la section « Prix et achats » aurait pu casser sans rouge) : c'est maintenant un échec.
- **19/11/2026 — motif du logo en 3D (Ahmed : « le cube du logo doit bouger en 3D »)** : CSS 3D seul (tools/gabarit.html, bloc .motif) : 9 petits cubes
  (face du dessus = la case, 4 côtés = ::before/::after des deux <s> de chaque case, balisage dans page()) sur un plateau vu de biais qui tourne en 48 s,
  vague de hauteur, cube doré qui monte et tourne sur lui-même ; ordinateur seulement (≥ 960 px) ; mouvement réduit demandé = scène 3D immobile.
