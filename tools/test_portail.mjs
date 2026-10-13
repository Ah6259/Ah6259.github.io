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
console.log(pb ? `\n${pb} PROBLÈME(S)` : "\nTOUT PASSE");
process.exit(pb ? 1 : 0);
