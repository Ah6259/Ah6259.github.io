// IndexNow : prévient Bing, Yandex, Seznam, Naver (et les moteurs qui lisent Bing : DuckDuckGo, Yahoo) des pages
// nouvelles ou modifiées de TOUS les sites clicvia.com. Google n'utilise pas IndexNow (lui : sitemap.xml + Search Console).
// Chaque site a le fichier <clé>.txt à sa racine (la clé n'est pas un secret : elle prouve seulement que le site est à nous).
// Chaque jour : les adresses dont <lastmod> date de moins de 2 jours. Le lundi (ou TOUT=1) : toutes les adresses.
// Usage : node tools/indexnow.mjs          (ESSAI=1 : n'envoie rien, affiche seulement)
const CLE = "377f054ba9c5ed40d6796adc8d87d1e8";
const SITES = ["clicvia.com", "prix-eau", "eau", "mosquees", "concours", "documents", "code", "voiture", "outils", "appels-offres",
  "pros", "auto-ecoles", "avocats", "comptables", "mariage", "comptes", "conferences", "immobilier"].map(s => s.includes(".") ? s : s + ".clicvia.com");
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
