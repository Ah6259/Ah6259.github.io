# ah6259.github.io — site racine

- Page d'accueil qui présente tous les sites.
- `robots.txt` COMMUN à tous les sites (les robots ne lisent que celui de la racine) : moteurs de recherche autorisés,
  robots d'IA et aspirateurs interdits, page de relecture du code de la route exclue, sitemaps de tous les sites.
- Fichier de vérification Google Search Console (propriété « préfixe d'URL » https://ah6259.github.io/ = tous les sites).

Ajouter un nouveau site : une carte dans index.html + une ligne `Sitemap:` dans robots.txt.

- Statistiques **GoatCounter** (anonymes, sans cookies) : compteur partagé `https://prix-eaux-tunisie.goatcounter.com`
  (chaque site est séparé par son chemin). CSP : `script-src https://gc.zgo.at` seulement, `connect-src` / `img-src` + le compteur.
- Image d'aperçu `og-image-v1.jpg` (1200 × 630, JPEG < 250 Ko, sinon WhatsApp n'affiche qu'une petite vignette) :
  capture Chrome sans écran d'une petite page HTML aux couleurs de l'accueil (liste des 5 sites), puis conversion JPEG.
  Si on la change : **nouveau nom** (`og-image-v2.jpg`), WhatsApp/Facebook gardent l'ancienne en cache.

- **Vidéo de présentation** (06/10/2026) : `assets/video/presentation.mp4` (1080 × 1920, vraies captures de chaque site et annuaire ;
  musique de fond : J. S. Bach, Aria des Variations Goldberg, enregistrement Musopen, CC0) + couverture et aperçu 1200 × 630.
  Page **`video/`** (lecteur, bouton « Ouvrir le site », Partager ; og:video / og:image) fabriquée par `node tools/page_video.mjs`
  à partir de index.html (à relancer si index.html change). Bouton « Partager » (en haut de l'accueil, `assets/portail.js`) : envoie
  le lien de la page vidéo + l'adresse du portail. CSP : `script-src 'self'` ajouté pour ce fichier, `media-src 'self'`.
  Test : `node tools/test_video.mjs` (robot `tests.yml`). Pour refaire la vidéo : `python fabriquer.py portail` dans le dossier
  PRIVÉ du PC `videos (outil)/`.

- **Adresse depuis le 11/10/2026 : https://clicvia.com/** (fichier CNAME ; Cloudflare : `@` et `www` en CNAME → ah6259.github.io, nuage gris). Les 16 sites ont chacun leur sous-domaine (fichier CNAME propre), ils ne bougent pas avec le portail. Logos des sites copiés dans assets/sites/.
