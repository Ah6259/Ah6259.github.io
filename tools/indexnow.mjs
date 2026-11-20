// IndexNow : prévient Bing, Yandex, Seznam, Naver (et les moteurs qui lisent Bing : DuckDuckGo, Yahoo) des pages
// nouvelles ou modifiées de TOUS les sites clicvia.com. Google n'utilise pas IndexNow (lui : sitemap.xml + Search Console).
// Chaque site a le fichier <clé>.txt à sa racine (la clé n'est pas un secret : elle prouve seulement que le site est à nous).
// Chaque jour : les adresses dont <lastmod> date de moins de 2 jours. Le lundi (ou TOUT=1) : toutes les adresses.
// Usage : node tools/indexnow.mjs          (ESSAI=1 : n'envoie rien, affiche seulement)
const CLE = "377f054ba9c5ed40d6796adc8d87d1e8";
const LISTE = ["clicvia.com", "prix-eau", "eau", "mosquees", "concours", "tendances", "documents", "code", "voiture", "outils", "appels-offres",
  "pros", "auto-ecoles", "avocats", "comptables", "mariage", "comptes", "conferences", "immobilier", "monagent", "hygiene"].map(s => s.includes(".") ? s : s + ".clicvia.com");
// 21/11/2026 (règle commune § 55) : hygiene.clicvia.com n'était pas dans la liste écrite à la main -> la liste est COMPLÉTÉE SEULE par les
// sous-domaines cités sur l'accueil du portail (tout nouveau site y est ajouté) : un nouveau site n'est plus jamais oublié par IndexNow.
const PAS_UN_SITE = /^(www|api-[a-z-]+|data)\.clicvia\.com$/;
let duPortail = [];
try {
  const h = await fetch("https://clicvia.com/").then(r => r.ok ? r.text() : "");
  duPortail = [...new Set([...h.matchAll(/https:\/\/([a-z0-9-]+\.clicvia\.com)\//g)].map(m => m[1]))].filter(x => !PAS_UN_SITE.test(x));
} catch { /* portail injoignable : la liste écrite suffit */ }
const nouveaux = duPortail.filter(x => !LISTE.includes(x));
if (nouveaux.length) console.log(`sites trouvés sur le portail et absents de la liste : ${nouveaux.join(", ")} (ajoutés pour ce passage)`);
const SITES = [...LISTE, ...nouveaux];
const TOUT = process.env.TOUT === "1" || new Date().getUTCDay() === 1, ESSAI = process.env.ESSAI === "1";
const limite = new Date(Date.now() - 2 * 864e5).toISOString().slice(0, 10);
let echecs = 0, total = 0;
for (const hote of SITES) {
  try {
    const cle = await fetch(`https://${hote}/${CLE}.txt`).then(r => r.ok ? r.text() : "");
    if (cle.trim() !== CLE) { console.log(`ÉCHEC ${hote} : fichier de clé absent`); echecs++; continue; }
    const plan = await fetch(`https://${hote}/sitemap.xml`).then(r => r.ok ? r.text() : "");
    const pages = [...plan.matchAll(/<url>\s*<loc>([^<]+)<\/loc>(?:\s*<lastmod>([^<]+)<\/lastmod>)?/g)]
      .filter(m => m[1].startsWith(`https://${hote}/`) && (TOUT || (m[2] && m[2].slice(0, 10) >= limite))).map(m => m[1]).slice(0, 10000);
    if (!pages.length) { console.log(`rien   ${hote}`); continue; }
    total += pages.length;
    if (ESSAI) { console.log(`essai  ${hote} : ${pages.length} adresse(s)`); continue; }
    const r = await fetch("https://api.indexnow.org/indexnow", { method: "POST", headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({ host: hote, key: CLE, keyLocation: `https://${hote}/${CLE}.txt`, urlList: pages }) });
    const ok = r.status === 200 || r.status === 202;
    console.log(`${ok ? "envoyé" : "ÉCHEC "} ${hote} : ${pages.length} adresse(s), réponse ${r.status}`);
    if (!ok) echecs++;
  } catch (e) { console.log(`ÉCHEC ${hote} : ${e.message}`); echecs++; }
}
console.log(`${total} adresse(s), ${echecs} échec(s)${ESSAI ? " (essai : rien envoyé)" : ""}`);
process.exit(echecs > SITES.length / 2 ? 1 : 0);   // un site en panne ne fait pas échouer le robot ; la moitié en panne, si
