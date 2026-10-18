// Robot « page Facebook Clicvia » : DEUX publications par jour (matin et après-midi), toutes seules, deux sites différents
// (décisions d'Ahmed : 12/10/2026 « je n'ai pas le temps de publier », 13/10/2026 « deux par jour, avec d'autres sites »).
// Chaque créneau a son site, à tour de rôle sur 7 jours (TOUR) ; le robot choisit une page du site dans son plan du site, lit son
// titre et sa description (ceux que Google voit) et publie un message court FR + AR avec le lien — Facebook affiche l'aperçu
// de la page (image og:image). Aucune mémoire à garder : le choix se calcule d'après la date, donc jamais deux fois la même
// page avant d'avoir fait le tour. Concours : les pages les plus récentes d'abord.
// Sécurité contre les doublons (GitHub lance parfois avec des heures de retard) : avant de publier, le robot relit les
// dernières publications de la page ; si le lien y est déjà, il prend la page suivante du même site.
// CRENEAU=0 (matin) ou 1 (après-midi) : donné par le robot facebook.yml selon l'horaire qui l'a lancé.
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
  // ajoutés le 13/10/2026 (demande d'Ahmed : deux publications par jour, avec d'autres sites)
  // 18/10/2026 (« Fais » d'Ahmed) : le rapport du mois fini (bilan national des prix) est publié à la 1re place de l'immobilier de chaque mois
  // (« prioritaire ») ; les pages de rapports ne sont pas dans le tour normal
  immobilier: { hote: "immobilier.clicvia.com", garder: /^\/[a-z-]+\/[^/]+\/$/, sauf: /^\/(video|a-propos|deposer|alertes|rapports)\//,
    prioritaire: j => { const d = new Date(Date.UTC(j.getUTCFullYear(), j.getUTCMonth() - 1, 1)); return `https://immobilier.clicvia.com/rapports/${d.toISOString().slice(0, 7)}/`; },
    fr: "Immobilier en Tunisie — annonces de vente et de location, gratuites :", ar: "عقارات في تونس — إعلانات بيع وكراء، مجانًا:", mots: "#Immobilier #Tunisie #عقارات #تونس" },
  "appels-offres": { hote: "appels-offres.clicvia.com", garder: /^\/((gouvernorat|metier)\/[^/]+|encheres)\/$/,
    fr: "Appels d'offres publics en Tunisie, mis à jour chaque jour :", ar: "طلبات العروض العمومية في تونس، تُحيَّن كل يوم:", mots: "#AppelsDoffres #Tunisie #طلبات_العروض #تونس" },
  voiture: { hote: "voiture.clicvia.com", garder: /^\/(visite-technique|vignette|entretien|carburant|achat-vente)\/$/,
    fr: "Votre voiture en Tunisie — vignette, visite technique, carburant : calculez et n'oubliez plus rien :", ar: "سيارتك في تونس — معلوم الجولان، الفحص الفني، الوقود: احسب ولا تنسَ شيئًا:", mots: "#Voiture #Vignette #Tunisie #سيارة" },
  outils: { hote: "outils.clicvia.com", garder: /^\/(salaire-net|retenue-source|impot-revenu|credit|auto-entrepreneur)\/$/,
    fr: "Calculateur gratuit pour la Tunisie (salaire, impôt, crédit) :", ar: "حاسبة مجانية لتونس (الأجر، الضريبة، القرض):", mots: "#Salaire #Impot #Tunisie #حاسبة" },
  mosquees: { hote: "mosquees.clicvia.com", garder: /^\/mosquee\/[^/]+\/$/,
    fr: "Une mosquée de Tunisie — son histoire, ses photos, la carte :", ar: "مسجد من مساجد تونس — تاريخه، صوره والخريطة:", mots: "#Mosquée #Tunisie #مساجد #تونس" },
  eau: { hote: "eau.clicvia.com", garder: /^\/(coran-et-eau\/|majels-et-puits\/)?$/,
    fr: "Où trouver de l'eau en Tunisie — sources, fontaines et majels sur une carte :", ar: "أين تجد الماء في تونس — عيون وسبّالات ومواجل على خريطة:", mots: "#Eau #Tunisie #ماء #تونس" },
};
// deux sites par jour sur 7 jours : [matin, après-midi] × 7 (jamais le même site deux fois le même jour)
// 15/10/2026 (Ahmed : « fais les deux ») : l'immobilier passe de 2 à 4 publications par semaine (une place de Documents et une de
// Mosquées lui sont données)
const TOUR = ["concours", "immobilier", "code", "appels-offres", "immobilier", "documents", "prix-eau", "voiture",
  "concours", "outils", "immobilier", "mosquees", "eau", "immobilier"];
const DEPART = Date.UTC(2026, 9, 12);

const jour = process.env.JOUR ? new Date(process.env.JOUR + "T00:00:00Z") : new Date();
const jours = Math.max(0, Math.floor((Date.UTC(jour.getUTCFullYear(), jour.getUTCMonth(), jour.getUTCDate()) - DEPART) / 864e5));
const creneau = process.env.CRENEAU === "1" ? 1 : 0;
const n = jours * 2 + creneau;                     // numéro du créneau depuis le départ
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
// dernières publications de la page (lecture seule) : pour ne jamais publier deux fois le même lien si GitHub est en retard
const ID = process.env.FB_PAGE_ID, JETON = process.env.FB_PAGE_TOKEN;
let recents = "";
if (ID && JETON) {
  try {
    const r = await fetch(`https://graph.facebook.com/${ID}/feed?fields=message&limit=25&access_token=${encodeURIComponent(JETON)}`);
    const d = await r.json();
    recents = (d.data || []).map(x => x.message || "").join("\n") + "\n";
    if (!r.ok) console.log("lecture des dernières publications impossible (" + ((d.error && d.error.code) || r.status) + ") : contrôle des doublons sauté");
  } catch (e) { console.log("lecture des dernières publications impossible : contrôle des doublons sauté"); }
}
// page prioritaire (rapport du mois fini) : seulement à la PREMIÈRE place de ce site dans le mois, si la page existe et n'est pas déjà publiée
let prio = null;
if (site.prioritaire) {
  const u = site.prioritaire(jour);
  let premier = true;
  for (let k = n - 1; k >= 0 && Math.floor(k / 2) > jours - jour.getUTCDate(); k--) if (TOUR[k % TOUR.length] === nom) { premier = false; break; }
  if (premier && plan.includes(`<loc>${u}</loc>`) && !recents.includes("👉 " + u + "\n")) prio = { url: u };
}
let rang = passages % pages.length, saut = 0;
while (saut < pages.length && recents.includes("👉 " + pages[rang].url + "\n")) { rang = (rang + 1) % pages.length; saut++; }
if (saut === pages.length) { console.log(`toutes les pages de ${nom} sont dans les dernières publications : rien à publier`); process.exit(0); }
if (saut) console.log(`page déjà publiée récemment : on passe à la suivante (${saut} saut(s))`);
const page = prio || pages[rang];
if (prio) console.log("rapport du mois fini : publié en priorité");

const h = await texte(page.url);
const titre = propre((h.match(/<meta property="og:title" content="([^"]*)"/) || h.match(/<title>([^<]*)<\/title>/) || [])[1]).replace(/\s*[|–—-]\s*[^|–—-]*$/, m => (m.length < 45 ? "" : m));
const desc = propre((h.match(/<meta name="description" content="([^"]*)"/) || [])[1]);
if (!titre) { console.log("page sans titre : " + page.url); process.exit(1); }
const message = [site.fr, "", titre, desc && desc !== titre ? desc.slice(0, 260) : "", "", site.ar, "", "👉 " + page.url, "", site.mots].filter((x, i, a) => !(x === "" && a[i - 1] === "")).join("\n");

console.log(`Jour ${jours}, ${creneau ? "après-midi" : "matin"} — site : ${nom} — page ${prio ? "prioritaire" : (rang + 1) + "/" + pages.length} : ${page.url}\n---\n${message}\n---`);
if (process.env.ESSAI === "1") { console.log("ESSAI : rien n'est publié."); process.exit(0); }
// 14/10/2026 (incident du robot Telegram de Conférences, resté vert sans exister) : secrets absents = ÉCHEC, jamais un vert silencieux
if (!ID || !JETON) { console.log("ÉCHEC : secrets FB_PAGE_ID / FB_PAGE_TOKEN absents du dépôt : rien n'est publié."); process.exit(1); }
const r = await fetch(`https://graph.facebook.com/${ID}/feed`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ message, link: page.url, access_token: JETON }) });
const rep = await r.json().catch(() => ({}));
if (!r.ok || !rep.id) {     // le jeton n'est jamais affiché ; seulement le message d'erreur de Facebook
  console.log("ÉCHEC : Facebook a refusé la publication — " + ((rep.error && (rep.error.message + " (code " + rep.error.code + ")")) || r.status));
  process.exit(1);
}
console.log("Publié : https://www.facebook.com/" + rep.id);
