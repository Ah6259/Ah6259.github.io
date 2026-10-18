// Robot « rafraîchir les aperçus Facebook » (18/10/2026, demande d'Ahmed : en partageant un rapport du mois, Facebook montrait
// l'image du site au lieu de celle de l'article). Facebook garde en mémoire l'aperçu (titre, image) d'une adresse ; quand nos
// pages changent (chiffres du mois en cours, nouvelle image d'aperçu), on lui demande de les relire.
// Pages relues : les rapports du mois (rapports/…) de chaque site qui en a, lus dans son plan du site (sitemap.xml).
// Secret : FB_PAGE_TOKEN (jeton de page, jamais dans un fichier). ESSAI=1 : liste les adresses sans rien envoyer.
// Une seconde entre deux demandes (règle commune : jamais de rafale).
const SEUL = process.env.SEUL || "";   // essai sur un seul site (ex. SEUL=immobilier)
const SITES = ["immobilier.clicvia.com", "prix-eau.clicvia.com", "concours.clicvia.com", "appels-offres.clicvia.com", "conferences.clicvia.com"];
const JETON = process.env.FB_PAGE_TOKEN, ESSAI = process.env.ESSAI === "1";
const pause = ms => new Promise(r => setTimeout(r, ms));
const urls = [];
for (const h of SITES.filter(x => !SEUL || x.startsWith(SEUL + "."))) {
  try {
    const plan = await (await fetch(`https://${h}/sitemap.xml`)).text();
    for (const m of plan.matchAll(/<loc>([^<]*\/rapports\/[^<]*)<\/loc>/g)) urls.push(m[1]);
  } catch (e) { console.log(`plan du site illisible : ${h}`); }
}
console.log(`${urls.length} pages de rapports à faire relire par Facebook`);
if (ESSAI) { urls.forEach(u => console.log(u)); process.exit(0); }
if (!JETON) { console.log("ÉCHEC : secret FB_PAGE_TOKEN absent : rien n'est envoyé."); process.exit(1); }
let ok = 0, echecs = 0;
for (const u of urls) {
  try {
    const r = await fetch("https://graph.facebook.com/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ id: u, scrape: "true", access_token: JETON }) });
    const d = await r.json().catch(() => ({}));
    if (r.ok && !d.error) ok++; else { echecs++; console.log(`échec : ${u} — ${(d.error && [d.error.message, d.error.error_user_title, d.error.error_user_msg].filter(Boolean).join(" · ")) || r.status}`); if (d.error && [4, 17, 32, 613].includes(d.error.code)) break; }
  } catch (e) { echecs++; console.log(`échec : ${u} — ${e.message}`); }
  await pause(1000);
}
console.log(`Relues : ${ok} ; échecs : ${echecs}`);
if (urls.length && !ok) process.exit(1);
