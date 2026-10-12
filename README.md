# ah6259.github.io — site racine

- Page d'accueil qui présente tous les sites.
- `robots.txt` COMMUN à tous les sites (les robots ne lisent que celui de la racine) : moteurs de recherche autorisés,
  robots d'IA et aspirateurs interdits, page de relecture du code de la route exclue, sitemaps de tous les sites.
- Fichier de vérification Google Search Console (propriété « préfixe d'URL » https://ah6259.github.io/ = tous les sites).

Ajouter un nouveau site : une carte dans index.html + une ligne `Sitemap:` dans robots.txt.
The Message (islam, multilingue ; nom unique dans toutes les langues depuis le 12/10/2026) : carte ajoutée le 11/10/2026 (thème « Religion et patrimoine ») ; depuis le 12/10/2026 son adresse est
https://message.clicvia.com/ (dépôt sur un autre compte GitHub : lemessagelemessage8-lab) ; icône `assets/sites/le-message.svg`.

- Statistiques **GoatCounter** (anonymes, sans cookies) : compteur partagé `https://prix-eaux-tunisie.goatcounter.com`
  (chaque site est séparé par son chemin). CSP : `script-src https://gc.zgo.at` seulement, `connect-src` / `img-src` + le compteur.
- Image d'aperçu `og-image-v2.jpg` (11/10/2026 : adresse clicvia.com, « 17 services », l'immobilier en tête ; 1200 × 630, JPEG < 250 Ko,
  sinon WhatsApp n'affiche qu'une petite vignette) : modèle `tools/og-image.html`, capture Chrome sans écran puis `convert` en JPEG.
  Si on la change : **nouveau nom** (`og-image-v2.jpg`), WhatsApp/Facebook gardent l'ancienne en cache.

- **Vidéo de présentation** (06/10/2026) : `assets/video/presentation.mp4` (1080 × 1920, vraies captures de chaque site et annuaire ;
  musique de fond : J. S. Bach, Aria des Variations Goldberg, enregistrement Musopen, CC0) + couverture et aperçu 1200 × 630.
  Page **`video/`** (lecteur, bouton « Ouvrir le site », Partager ; og:video / og:image) fabriquée par `node tools/page_video.mjs`
  à partir de index.html (à relancer si index.html change). Bouton « Partager » (en haut de l'accueil, `assets/portail.js`) : envoie
  le lien de la page vidéo + l'adresse du portail. CSP : `script-src 'self'` ajouté pour ce fichier, `media-src 'self'`.
  Test : `node tools/test_video.mjs` (robot `tests.yml`). Pour refaire la vidéo : `python fabriquer.py portail` dans le dossier
  PRIVÉ du PC `videos (outil)/`.

- **Adresse depuis le 11/10/2026 : https://clicvia.com/** (fichier CNAME ; Cloudflare : `@` et `www` en CNAME → ah6259.github.io, nuage gris). Les 16 sites ont chacun leur sous-domaine (fichier CNAME propre), ils ne bougent pas avec le portail. Logos des sites copiés dans assets/sites/.

- **Visibilité Google (12/10/2026, règle commune § 8)** : liens vers nos autres sites en `https://<site>.clicvia.com/` (jamais `ah6259.github.io`), lien « Tous nos services » → https://clicvia.com/ dans le pied de page, `robots.txt` avec ligne Sitemap, `sitemap.xml` daté, JSON-LD sur l'accueil, clé IndexNow `377f054ba9c5ed40d6796adc8d87d1e8.txt` à la racine (ne pas supprimer : robot `indexnow` du portail). Contrôle : `node "outils visibilite/controle.mjs"` (dépôt projets-ahmed). Sitemap envoyé dans Search Console par Ahmed le 12/10/2026.
- **Robot `indexnow`** (`tools/indexnow.mjs`, chaque jour 14h37) : prévient Bing / Yandex des pages nouvelles de tous les sites ; nouveau site = l'ajouter à sa liste `SITES`.

- **Robot `facebook`** (`tools/facebook.mjs`, chaque jour 18h05) : une publication par jour sur la page Facebook Clicvia, un site à tour de rôle (Concours — seulement ceux encore ouverts —, Code de la route, Prix des Eaux, Documents) ; titre et description lus sur la page, message FR + AR, lien. Secrets du dépôt : `FB_PAGE_ID`, `FB_PAGE_TOKEN` (sans eux : essai, rien n'est publié). Essai : `ESSAI=1 node tools/facebook.mjs`. Nouveau site : l'ajouter à `SITES` et `TOUR`.

- **Page Facebook Clicvia (12/10/2026)** : https://www.facebook.com/1327283777142447 — le robot `facebook` du dépôt du portail (`Ah6259.github.io`, `tools/facebook.mjs`, chaque jour 18h05) publie tout seul une page de ce site à son tour (titre, description et image `og:image` lus sur la page : les garder soignés). Ahmed ne publie rien à la main. Détail et dépannage : `nouveau site - procedure.md` § 4 étape 6 (dépôt projets-ahmed).
