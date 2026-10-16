/* Page 404 de clicvia.com (scripts sortis de la page le 16/10/2026 : politique de sécurité stricte, aucun script dans la page). */
// Page servie par GitHub pour toute adresse inconnue de clicvia.com.
// 1) Les liens du tableau de bord GoatCounter ouvrent « clicvia.com/<préfixe du site>/… ». GitHub renvoie seul vers le bon
//    sous-domaine pour nos dépôts, mais PAS pour The Message (autre compte GitHub) : on le fait ici.
// 2) Les lignes « partage/… » et « lien-site/… » de GoatCounter sont des CLICS comptés, pas des pages : on l'explique.
(function () {
  var p = location.pathname, SITES = { "/le-message": "https://message.clicvia.com" };
  for (var k in SITES) if (p === k || p.indexOf(k + "/") === 0) { location.replace(SITES[k] + (p.slice(k.length) || "/") + location.search + location.hash); return; }
  window.CLIC_COMPTE = /^\/(partage|lien-site)(\/|$)/.test(p);
})();
if (window.CLIC_COMPTE) document.getElementById("texte").textContent = "Cette ligne des statistiques n'est pas une page : c'est le compte des clics sur un bouton (« Partager » ou un lien vers un autre de nos sites).";
