// Robot « page Facebook Clicvia » : UNE publication par jour, toute seule (décision d'Ahmed du 12/10/2026 : il n'a pas le
// temps de publier). Chaque jour un site à tour de rôle ; le robot choisit une page du site dans son plan du site, lit son
// titre et sa description (ceux que Google voit) et publie un message court FR + AR avec le lien — Facebook affiche l'aperçu
// de la page (image og:image). Aucune mémoire à garder : le choix se calcule d'après la date, donc jamais deux fois la même
// page avant d'avoir fait le tour. Concours : les pages les plus récentes d'abord.
//
// Secrets GitHub du dépôt (jamais dans un fichier) : FB_PAGE_ID (numéro de la page) et FB_PAGE_TOKEN (jeton de page).
// Sans ces secrets, ou avec ESSAI=1 : rien n'est publié, le message est seulement affiché.
//   node tools/facebook.mjs                 ESSAI=1 node tools/facebook.mjs        SITE=concours JOUR=2026-10-20 ESSAI=1 node tools/facebook.mjs
// Nouveau site : l'ajouter à SITES et à TOUR (règle « nouveau site », § 4 étape 6).
const SITES = {
  concours: { hote: "concours.clicvia.com", garder: /^\/concours\/[^/]+\/$/, ouverts: "donnees/concours.json",
    fr: "Concours public en Tunisie — date limite, postes et lien officiel :", ar: "مناظرة عمومية في تونس — آخر أجل، عدد الخطط والرابط الرسمي:", mots: "#Concours #Tunisie #مناظرات #تونس" },
  code: { hote: "code.clicvia.com", garder: /^\/(entrainement|examen|panneaux|lecons|amendes|permis)\/$/,
    fr: "Code de la route en Tunisie — révisez gratuitement, en français et en arabe :", ar: "قانون الطرقات في تونس — راجع مجانًا بالعربية والفرنسية:", mots: "#CodeDeLaRoute #Permis #Tunisie #رخصة_السياقة" },
  "prix-eau": { hote: "prix-eau.clicvia.com", garder: /^\/(marque\/[^/]+|prix-[^/]+|quelle-eau)\/$/,
    fr: "Prix de l'eau en bouteille en Tunisie, comparés chaque jour :", ar: "أسعار الماء المعدني في تونس، مقارنة كل يوم:", mots: "#PrixEau #Tunisie #أسعار #تونس" },
  documents: { hote: "documents.clicvia.com", garder: /^\/[^/]+\/$/, sauf: /^\/(a-propos|pass|video|modeles)\/$/,
    fr: "Modèle de document tunisien prêt à remplir (PDF, français et arabe) :", ar: "نموذج وثيقة تونسية جاهز للتعمير (PDF، بالعربية والفرنسية):", mots: "#Documents #Tunisie #نماذج #وثائق" },
};
const TOUR = ["concours", "code", "prix-eau", "documents", "concours", "documents", "prix-eau"];      // un site par jour, sur 7 jours
const DEPART = Date.UTC(2026, 9, 12);

const jour = process.env.JOUR ? new Date(process.env.JOUR + "T00:00:00Z") : new Date();
const n = Math.max(0, Math.floor((Date.UTC(jour.getUTCFullYear(), jour.getUTCMonth(), jour.getUTCDate()) - DEPART) / 864e5));
const nom = process.env.SITE || TOUR[n % TOUR.length];
const site = SITES[nom];
if (!site) { console.log("site inconnu : " + nom); process.exit(1); }
// combien de fois ce site est déjà passé : c'est le numéro de la page à publier aujourd'hui
const passages = Math.floor(n / TOUR.length) * TOUR.filter(x => x === nom).length + TOUR.slice(0, n % TOUR.length).filter(x => x === nom).length;

const texte = async u => { const r = await fetch(u, { headers: { "User-Agent": "ClicviaRobot/1.0 (+https://clicvia.com/)" } }); if (!r.ok) throw new Error(u + " : " + r.status); return r.text(); };
const propre = s => String(s || "").replace(/&amp;/g, "&").replace(/&#x27;|&#39;|&apos;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();

const plan = await texte(`https://${site.hote}/sitemap.xml`);
let pages = [...plan.matchAll(/<url>\s*<loc>([^<]+)<\/loc>(?:\s*<lastmod>([^<]+)<\/lastmod>)?/g)].map(m => ({ url: m[1], maj: m[2] || "" }))
  .filter(p => p.url.startsWith(`https://${site.hote}/`) && site.garder.test(new URL(p.url).pathname) && !(site.sauf && site.sauf.test(new URL(p.url).pathname)));
if (!pages.length) { console.log(`rien à publier pour ${nom} (aucune page retenue dans le plan du site)`); process.exit(0); }
if (site.ouverts) {      // Concours : seulement ceux dont les inscriptions sont encore ouvertes (au moins 2 jours), les plus proches de la fin d'abord
  const limite = new Date(jour.getTime() + 2 * 864e5).toISOString().slice(0, 10);
  const d = JSON.parse(await texte(`https://${site.hote}/${site.ouverts}`));
  const ouverts = (d.concours || []).filter(c => c.cloture_candidatures && c.cloture_candidatures >= limite)
    .sort((a, b) => a.cloture_candidatures.localeCompare(b.cloture_candidatures) || String(a.id).localeCompare(String(b.id)));
  const parAdresse = new Map(pages.map(p => [new URL(p.url).pathname, p]));
  pages = ouverts.map(c => parAdresse.get(`/concours/${c.id}/`)).filter(Boolean);
  if (!pages.length) { console.log("aucun concours ouvert à publier aujourd'hui"); process.exit(0); }
}
const page = pages[passages % pages.length];

const h = await texte(page.url);
const titre = propre((h.match(/<meta property="og:title" content="([^"]*)"/) || h.match(/<title>([^<]*)<\/title>/) || [])[1]).replace(/\s*[|–—-]\s*[^|–—-]*$/, m => (m.length < 45 ? "" : m));
const desc = propre((h.match(/<meta name="description" content="([^"]*)"/) || [])[1]);
if (!titre) { console.log("page sans titre : " + page.url); process.exit(1); }
const message = [site.fr, "", titre, desc && desc !== titre ? desc.slice(0, 260) : "", "", site.ar, "", "👉 " + page.url, "", site.mots].filter((x, i, a) => !(x === "" && a[i - 1] === "")).join("\n");

console.log(`Jour ${n} — site : ${nom} — page ${passages % pages.length + 1}/${pages.length} : ${page.url}\n---\n${message}\n---`);
const ID = process.env.FB_PAGE_ID, JETON = process.env.FB_PAGE_TOKEN;
if (process.env.ESSAI === "1" || !ID || !JETON) { console.log(ID && JETON ? "ESSAI : rien n'est publié." : "Secrets FB_PAGE_ID / FB_PAGE_TOKEN absents : rien n'est publié (essai)."); process.exit(0); }
const r = await fetch(`https://graph.facebook.com/${ID}/feed`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ message, link: page.url, access_token: JETON }) });
const rep = await r.json().catch(() => ({}));
if (!r.ok || !rep.id) {     // le jeton n'est jamais affiché ; seulement le message d'erreur de Facebook
  console.log("ÉCHEC : Facebook a refusé la publication — " + ((rep.error && (rep.error.message + " (code " + rep.error.code + ")")) || r.status));
  process.exit(1);
}
console.log("Publié : https://www.facebook.com/" + rep.id);
