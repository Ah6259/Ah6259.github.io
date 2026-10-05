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
