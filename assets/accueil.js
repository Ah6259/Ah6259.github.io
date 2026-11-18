/* Accueil de clicvia.com (refonte du 18/11/2026) : recherche instantanée dans les cartes des sites et menu des catégories.
   - La recherche lit le nom, la description et les mots de chaque carte (data-mots, liste MOTS de tools/construire.py), en
     ignorant accents et majuscules ; une catégorie sans carte qui correspond est cachée ; message si rien ne correspond.
   - Sans JavaScript, la recherche reste cachée (attribut hidden) et la page montre toutes les cartes.
   - Le menu des catégories marque la catégorie affichée à l'écran (aria-current). Aucun cookie, rien n'est enregistré. */
(function () {
  "use strict";
  var form = document.querySelector(".cherche");
  if (!form) return;
  var champ = form.querySelector("input"), effacer = form.querySelector(".effacer");
  var etat = document.querySelector(".cherche-etat"), vide = document.querySelector(".cherche-vide");
  var cartes = [].slice.call(document.querySelectorAll("a.site")), cats = [].slice.call(document.querySelectorAll("section.cat"));
  function norme(t) {
    return (t || "").toLowerCase().normalize("NFD").replace(/[̀-ًͯ-ٰٟ]/g, "")   // accents et voyelles arabes
      .replace(/[أإآ]/g, "ا").replace(/ة/g, "ه").replace(/ى/g, "ي").replace(/[’'`-]/g, " ");
  }
  var textes = cartes.map(function (a) { return norme(a.textContent + " " + (a.getAttribute("data-mots") || "")); });
  form.hidden = false;

  function filtrer() {
    var mots = norme(champ.value).split(/\s+/).filter(Boolean), n = 0;
    cartes.forEach(function (a, i) {
      var ok = mots.every(function (m) { return textes[i].indexOf(m) >= 0; });
      a.hidden = !ok; if (ok) n++;
    });
    cats.forEach(function (c) { c.hidden = !c.querySelector("a.site:not([hidden])"); });
    var actif = mots.length > 0;
    effacer.hidden = !actif;
    document.body.classList.toggle("en-recherche", actif);
    vide.hidden = !actif || n > 0;
    etat.textContent = !actif ? "" : n === 0 ? vide.textContent : n === 1 ? form.getAttribute("data-un") : form.getAttribute("data-n").replace("{n}", n);
  }
  champ.addEventListener("input", filtrer);
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var premiere = cartes.filter(function (a) { return !a.hidden; })[0];
    if (premiere && champ.value.trim()) premiere.focus();
  });
  effacer.addEventListener("click", function () { champ.value = ""; filtrer(); champ.focus(); });
  champ.addEventListener("keydown", function (e) { if (e.key === "Escape") { champ.value = ""; filtrer(); } });

  // menu des catégories : la catégorie visible est marquée ; un clic vide la recherche pour montrer la catégorie entière
  var liens = [].slice.call(document.querySelectorAll(".cats a"));
  liens.forEach(function (a) {
    a.addEventListener("click", function () { if (champ.value) { champ.value = ""; filtrer(); } });
  });
  if (!("IntersectionObserver" in window)) return;
  var vues = {};
  var obs = new IntersectionObserver(function (entrees) {
    entrees.forEach(function (e) { vues[e.target.id] = e.isIntersecting; });
    var courant = null;
    for (var i = 0; i < cats.length; i++) if (vues[cats[i].id] && !cats[i].hidden) { courant = cats[i].id; break; }
    liens.forEach(function (a) {
      if (a.getAttribute("href") === "#" + courant) {
        if (!a.hasAttribute("aria-current")) {
          a.setAttribute("aria-current", "true");
          var boite = a.parentNode;
          if (boite.scrollWidth > boite.clientWidth) {
            var g = a.offsetLeft - (boite.clientWidth - a.offsetWidth) / 2;
            boite.scrollTo ? boite.scrollTo({ left: g, behavior: "smooth" }) : (boite.scrollLeft = g);
          }
        }
      } else a.removeAttribute("aria-current");
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  cats.forEach(function (c) { obs.observe(c); });
})();
