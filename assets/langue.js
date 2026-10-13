/* Portail clicvia.com en trois langues, une adresse par langue : / (français), /ar/, /en/ (13/10/2026).
   - un ancien lien « /?lang=ar » ou « /?lang=en » (bouton Partager, page vidéo) ouvre la bonne adresse ;
   - le lien discret « Vidéo de présentation » existe aussi sur /ar/ et /en/ (assets/portail.js ne le pose que sur l'accueil français). */
(function () {
  var p = location.pathname.replace(/index\.html$/, ""), q = new URLSearchParams(location.search).get("lang");
  if (p === "/" && (q === "ar" || q === "en")) { location.replace("/" + q + "/"); return; }
  if (p === "/ar/" && q === "fr" || p === "/en/" && q === "fr") { location.replace("/"); return; }
  var l = document.documentElement.lang;
  if ((p === "/ar/" || p === "/en/") && !document.getElementById("lien-video")) {
    var b = document.createElement("p"), a = document.createElement("a");
    b.id = "lien-video"; b.className = "lien-video"; a.href = "/video/?lang=" + l;
    a.textContent = l === "ar" ? "الفيديو التقديمي" : "Presentation video";
    b.appendChild(a);
    var m = document.querySelector("main"); if (m) m.insertAdjacentElement("afterend", b);
  }
})();
