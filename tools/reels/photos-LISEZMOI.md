# Photos des gouvernorats (fonds des vidéos Instagram)

Fichier : `photos.json` — pour chacun des 24 gouvernorats, 2 à 3 vraies photos de la ville ou de ses paysages.

## Source
- Toutes les photos viennent de **Wikimedia Commons** (https://commons.wikimedia.org), lues par l'API publique
  (User-Agent « ClicviaRobot/1.0 (+https://clicvia.com/) », une requête par seconde au plus).
- Ce sont des **photographies réelles** prises par des personnes : aucune image fabriquée par une IA, aucun dessin, aucune carte.
- Chaque photo a été regardée une par une (planche de contrôle) : pas de personnes en gros plan, pas de photo floue
  ou sombre, et le lieu est bien dans le gouvernorat.

## Licences retenues (et seulement celles-ci)
- **CC0** et **domaine public** ;
- **CC BY** (toutes versions) ;
- **CC BY-SA** (toutes versions).

Refusées : toute licence « NC » (pas d'usage commercial), « ND » (pas de modification), « fair use », ou inconnue.
Les vidéos recadrent et assombrissent la photo : c'est permis par ces licences. Avec CC BY-SA, la photo modifiée reste
sous la même licence (on l'indique dans le crédit, c'est suffisant).

## Crédit obligatoire
Chaque vidéo qui utilise une photo doit porter, **dans la légende de la publication**, la ligne :

    Photo : <auteur>, <licence>, Wikimedia Commons

Exemple : `Photo : IssamBarhoumi, CC BY-SA 4.0, Wikimedia Commons`.
Les champs `auteur` et `licence` de `photos.json` donnent ce texte ; `page` (page Commons de la photo) et
`licence_url` permettent de le vérifier.

## Champs de photos.json
`url` (fichier original sur upload.wikimedia.org), `page` (page Commons), `titre`, `auteur`, `licence`, `licence_url`,
`largeur`, `hauteur` (en pixels, au moins 1600 de large), `sujet` (quelques mots en français).

Conseil : télécharger l'original une fois puis le garder en cache (ne pas le retélécharger à chaque vidéo).
