/* Page 404 de clicvia.com (scripts sortis de la page le 16/10/2026 : politique de sécurité stricte, aucun script dans la page). */
// Page servie par GitHub pour toute adresse inconnue de clicvia.com.
// 1) Les liens du tableau de bord GoatCounter ouvrent « clicvia.com/<préfixe du site>/… ». GitHub renvoie seul vers le bon
//    sous-domaine pour nos dépôts, mais PAS pour The Message (autre compte GitHub) : on le fait ici.
// 2) Les lignes « partage/… » et « lien-site/… » de GoatCounter sont des CLICS comptés, pas des pages : on l'explique.
// 3) (17/11/2026, Ahmed : « Page introuvable » fait partir le visiteur) : toute autre adresse est CHERCHÉE sur nos sites
//    (liste lue sur l'accueil du portail : un nouveau site y est trouvé seul) ; pendant la recherche la page dit « Recherche de
//    la page… » ; trouvée = renvoi direct ; « Page introuvable » seulement si aucun site ne l'a. Ex. clicvia.com/fiche/… d'une
//    statistique sans préfixe -> avocats.clicvia.com/fiche/… (GitHub Pages répond « Access-Control-Allow-Origin: * »).
(function () {
  var p = location.pathname, SITES = { "/le-message": "https://message.clicvia.com",
    // 16/10/2026 : code de l'Immobilier devenu privé -> GitHub ne renvoie plus seul « clicvia.com/immobilier-tunis » (liens des statistiques)
    "/immobilier-tunis": "https://immobilier.clicvia.com", "/immobilier-tunisie": "https://immobilier.clicvia.com" };
  for (var k in SITES) if (p === k || p.indexOf(k + "/") === 0) { location.replace(SITES[k] + (p.slice(k.length) || "/") + location.search + location.hash); return; }
  var titre = document.getElementById("titre"), texte = document.getElementById("texte"), ar = document.getElementById("texte-ar");
  if (/^\/(partage|lien-site)(\/|$)/.test(p)) {
    texte.textContent = "Cette ligne des statistiques n'est pas une page : c'est le compte des clics sur un bouton (« Partager » ou un lien vers un autre de nos sites).";
    return;
  }
  if (!window.fetch || !window.Promise || p === "/" || p.length > 300) return;
  var fin = function (trouve) {
    if (trouve) { location.replace(trouve + p + location.search + location.hash); return; }
    titre.textContent = "Page introuvable"; texte.textContent = "Cette adresse n'existe pas (ou plus)."; ar.textContent = "هذه الصفحة غير موجودة.";
  };
  titre.textContent = "Recherche de la page…"; texte.textContent = "Un instant : nous cherchons cette page sur nos sites."; ar.textContent = "لحظة من فضلك: نبحث عن هذه الصفحة في مواقعنا.";
  var minuteur = setTimeout(function () { fin(null); }, 8000), fini = false;
  var une = function (x) { if (!fini) { fini = true; clearTimeout(minuteur); fin(x); } };
  fetch("/", { cache: "no-store" }).then(function (r) { return r.text(); }).then(function (h) {
    var vus = {}, hotes = [], m, re = /https:\/\/([a-z0-9-]+)\.clicvia\.com/g;
    while ((m = re.exec(h))) if (m[1] !== "www" && !vus[m[1]]) { vus[m[1]] = 1; hotes.push("https://" + m[1] + ".clicvia.com"); }
    var reste = hotes.length; if (!reste) return une(null);
    hotes.forEach(function (base) {
      fetch(base + p, { method: "HEAD", mode: "cors", redirect: "follow" })
        .then(function (r) { if (r.ok) une(base); }, function () {})
        .then(function () { if (--reste === 0) une(null); });
    });
  }, function () { une(null); });
})();
