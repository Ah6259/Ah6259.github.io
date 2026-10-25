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
