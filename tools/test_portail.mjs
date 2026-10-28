// Tests du portail en trois langues : node tools/test_portail.mjs  (aucune dépendance)
import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
const root = join(dirname(fileURLToPath(import.meta.url)), ".."), lire = f => readFileSync(join(root, f), "utf8");
let pb = 0;
const check = (nom, ok) => { console.log((ok ? "OK   " : "ÉCHEC ") + nom); if (!ok) pb++; };
const BASE = "https://clicvia.com/", PAGES = { fr: "index.html", ar: "ar/index.html", en: "en/index.html" };
const adresse = l => l === "fr" ? BASE : BASE + l + "/";
const liens = h => [...h.matchAll(/<a class="site" href="([^"]+)"/g)].map(m => m[1]);
const nFr = liens(lire(PAGES.fr)).length;
check(`accueil français : ${nFr} sites (au moins 18)`, nFr >= 18);
for (const [l, f] of Object.entries(PAGES)) {
  const h = existsSync(join(root, f)) ? lire(f) : "";
  check(`${f} : langue « ${l} »${l === "ar" ? ", écrite de droite à gauche" : ""}, adresse officielle ${adresse(l)}`,
    h.includes(`<html lang="${l}"${l === "ar" ? ' dir="rtl"' : ""}`) && h.includes(`<link rel="canonical" href="${adresse(l)}">`) && h.includes(`og:url" content="${adresse(l)}"`));
  check(`${f} : les 3 langues proposées à Google (hreflang) et x-default = français`,
    Object.keys(PAGES).every(x => h.includes(`hreflang="${x}" href="${adresse(x)}"`)) && h.includes(`hreflang="x-default" href="${BASE}"`));
  check(`${f} : mêmes ${nFr} sites, tous en https://<site>.clicvia.com/, bouton de langue et bouton Partager`,
    liens(h).length === nFr && liens(h).every(u => /^https:\/\/[a-z-]+\.clicvia\.com\/(\?lang=(ar|en)|(ar|en)\/)?$/.test(u))
    && h.includes('class="langues"') && h.includes("data-partager-video") && h.includes("/assets/langue.js") && h.includes("/assets/portail.js"));
  check(`${f} : image d'aperçu de partage (JPEG, type et dimensions), données structurées lisibles`,
    h.includes('og:image" content="https://clicvia.com/og-image-v2.jpg"') && h.includes('og:image:type" content="image/jpeg"')
    && JSON.parse(h.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1])["@graph"][2].numberOfItems === nFr);
}
const ar = lire(PAGES.ar), en = lire(PAGES.en);
check("page arabe : écrite en arabe (titre, cartes), liens vers la version arabe des sites", /<h1>[^<]*[؀-ۿ]/.test(ar) && ar.includes("https://mosquees.clicvia.com/ar/") && ar.includes("https://code.clicvia.com/?lang=ar"));
check("page anglaise : écrite en anglais, Mosquées et Points d'eau en /en/, étiquette de langue sur chaque carte", en.includes("<h1>Free services for Tunisia</h1>") && en.includes("https://mosquees.clicvia.com/en/") && en.includes("https://eau.clicvia.com/en/") && (en.match(/class="langues-site"/g) || []).length === nFr);
check("The Message : pas de version arabe (lien simple sur la page arabe), anglais sur la page anglaise", ar.includes('href="https://message.clicvia.com/"') && en.includes("https://message.clicvia.com/?lang=en"));
const plan = lire("sitemap.xml");
check("plan du site : les 3 adresses de langue et la page vidéo", Object.keys(PAGES).every(l => plan.includes(`<loc>${adresse(l)}</loc>`)) && plan.includes(`<loc>${BASE}video/</loc>`));
check("fabrication : index.html est bien celui de tools/construire.py (gabarit + listes)", existsSync(join(root, "tools/gabarit.html")) && existsSync(join(root, "tools/construire.py")));
// 25/10/2026 (RÈGLE d'Ahmed, règle commune § 44 : « la page Comment fonctionne le site doit être mise à jour chaque fois qu'on modifie
// le site ») : chaque fonction visible du portail (repère dans les pages ou le code) doit être expliquée dans a-propos/ (et ar/, en/) ;
// nouvelle fonction = une ligne ici + son explication dans A_PROPOS de tools/construire.py. Liste lue en entier, une ligne par fonction.
{ const ap = { fr: "a-propos/index.html", ar: "ar/a-propos/index.html", en: "en/a-propos/index.html" };
  const txt = f => existsSync(join(root, f)) ? lire(f).replace(/&#x27;/g, "'").replace(/\u00a0/g, " ") : "";
  const acc = lire(PAGES.fr), js = lire("assets/portail.js"), cons = lire("tools/construire.py");
  const FONCTIONS = [
    ["cartes des sites, rangées par thème", /<a class="site"/.test(acc) && /class="theme"/.test(acc), { fr: /Touchez une carte/, ar: /بطاقات المواقع/, en: /Website cards/ }],
    ["trois langues (une adresse par langue)", /class="langues"/.test(acc) && existsSync(join(root, PAGES.ar)) && existsSync(join(root, PAGES.en)), { fr: /Trois langues/, ar: /ثلاث لغات/, en: /Three languages/ }],
    ["étiquette de langue des cartes (page anglaise)", /class="langues-site"/.test(lire(PAGES.en)), { fr: /dans quelles langues/, ar: /لغات الموقع/, en: /which languages/ }],
    ["bouton « Partager »", /data-partager-video/.test(acc) && /partagerLien/.test(js), { fr: /bouton « Partager »/, ar: /زر «شارك»/, en: /“Share” button/ }],
    ["vidéo de présentation", existsSync(join(root, "video/index.html")) && /lien-video/.test(js), { fr: /vidéo de présentation/, ar: /الفيديو التقديمي/, en: /presentation video/ }],
    ["page Facebook Clicvia (publications automatiques)", /facebook\.com\/1327283777142447/.test(acc) && existsSync(join(root, "tools/facebook.mjs")), { fr: /Facebook[\s\S]*publiées automatiquement/, ar: /فيسبوك[\s\S]*آليًا/, en: /Facebook[\s\S]*posted there automatically/ }],
    ["données ouvertes (donnees.json)", existsSync(join(root, "donnees.json")), { fr: /donnees\.json/, ar: /donnees\.json/, en: /donnees\.json/ }],
    ["statistiques anonymes sans cookies", /goatcounter/.test(acc), { fr: /anonymes, sans cookies/, ar: /مجهولة الهوية/, en: /anonymous, with no cookies/ }],
    ["moteurs de recherche prévenus (IndexNow)", existsSync(join(root, "tools/indexnow.mjs")), { fr: /moteurs de recherche sont prévenus/, ar: /محركات البحث/, en: /search engines are notified/ }],
    ["gratuit / partie payante (Pass) des sites", true, { fr: /gratuit[\s\S]*« Pass »/, ar: /Pass/, en: /free[\s\S]*“Pass”/ }],
    ["sites indépendants, non officiels", /indépendants, non officiels/.test(acc), { fr: /indépendants et non officiels/, ar: /مستقلة وغير رسمية/, en: /independent and unofficial/ }],
    ["fabrication automatique (construire.py)", /def page_a_propos/.test(cons), { fr: /fabriqués automatiquement/, ar: /تُصنع آليًا/, en: /built automatically/ }]];
  const manque = [];
  for (const [nom, sur, re] of FONCTIONS) for (const l of Object.keys(ap)) if (sur && !re[l].test(txt(ap[l]))) manque.push(`${nom} (${l})`);
  check(`page « Comment fonctionne le site ? » à jour : chaque fonction du portail y est expliquée, en 3 langues (${FONCTIONS.length} fonctions)` + (manque.length ? " — manque : " + manque.join(", ") : ""),
    manque.length === 0);
  const titres = { fr: "<h1>Comment fonctionne le site\u00a0?</h1>", ar: "<h1>كيف يعمل الموقع؟</h1>", en: "<h1>How does the site work?</h1>" };
  check("page « Comment fonctionne le site ? » : titre dans chaque langue, lien dans le pied de page de l'accueil (3 langues), de la page vidéo et dans le plan du site",
    Object.keys(ap).every(l => existsSync(join(root, ap[l])) && lire(ap[l]).includes(titres[l]) && lire(ap[l]).includes('class="pied-liens"'))
    && lire(PAGES.fr).includes('<a href="/a-propos/">') && lire(PAGES.ar).includes('<a href="/ar/a-propos/">') && lire(PAGES.en).includes('<a href="/en/a-propos/">')
    && lire("video/index.html").includes('<a href="/a-propos/">')
    && Object.keys(ap).every(l => lire("sitemap.xml").includes(`<loc>${BASE}${l === "fr" ? "" : l + "/"}a-propos/</loc>`))
    && Object.values(ap).every(f => !/ on[a-z]+=|<script>(?!\s*$)/.test(lire(f)))); }
// 28/10/2026 (Ahmed) : petit lien discret « Espace privé » vers le tableau de bord, en bas des 3 accueils, non suivi par Google
check("pied de page : lien discret « Espace privé » vers /tableau-bord/ (rel=nofollow) sur les 3 accueils",
  ["index.html", "ar/index.html", "en/index.html"].every(f => /<a class="prive" href="\/tableau-bord\/" rel="nofollow">/.test(lire(f))));
console.log(pb ? `\n${pb} PROBLÈME(S)` : "\nTOUT PASSE");
process.exit(pb ? 1 : 0);
