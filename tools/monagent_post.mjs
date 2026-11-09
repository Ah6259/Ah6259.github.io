// Robot « publication du jour de Mon agent immobilier » (09/11/2026, demande d'Ahmed : « une publication Instagram et Facebook entre les deux
// publications du site Immobilier ; chaque publication différente des autres, et totalement différente de celles de l'Immobilier : personne
// ne doit faire un lien entre ces deux sites »).
//
// Une IMAGE par jour (1080 × 1350, le format qui prend le plus de place dans le fil), à 13h20 (entre les Reels de 8h20 et 18h20), fabriquée
// comme une CONVERSATION avec un agent : la question d'un visiteur (français, arabe ou tunisien écrit en lettres latines) et la réponse
// chiffrée de Mon agent, calculée sur les VRAIES annonces du site (https://monagent.clicvia.com/donnees/index.js, même moteur de compréhension
// que le site : assets/comprendre.js, même filtre que assets/agent.js). Puis une légende courte (accroche-question, chiffres, appel à l'action,
// lien qui ouvre directement la réponse sur le site, mots-dièse locaux).
//
// RÈGLES :
// - Jamais un mot, une couleur ni une police des publications de l'Immobilier (reels.py : terre cuite / sable / or, Fraunces, Poppins…) ;
//   ici : les bleus et le gris encre du site Mon agent et des palettes voisines, polices Plus Jakarta Sans / Manrope / Sora / Outfit.
// - Jamais « Immobilier Tunisie », jamais « Clicvia » (hors l'adresse monagent.clicvia.com), jamais « IA » (décision d'Ahmed du 02/11/2026) :
//   INTERDITS, vérifié avant toute publication et dans le test.
// - Chaque publication différente des précédentes (règle commune § 49) : question, gouvernorat, palette, mise en page, police et accroche
//   gardés dans donnees/monagent-posts.json ; un style trop proche des 4 derniers est décalé (choisirStyle).
// - Mesure des clics : le lien porte utm_source=facebook|instagram, utm_medium=post, utm_campaign=monagent-<date> (GoatCounter les lit).
//
// Publication : page Facebook (secrets MONAGENT_FB_PAGE_ID / MONAGENT_FB_PAGE_TOKEN, sinon la page Clicvia : FB_PAGE_ID / FB_PAGE_TOKEN) ;
// Instagram SEULEMENT sur un compte propre à Mon agent (secret MONAGENT_IG_USER_ID + MONAGENT_FB_PAGE_TOKEN) : le compte @immobilier.clicvia
// et son lien de bio feraient le lien entre les deux sites. Sans ce secret : « Instagram : compte propre à créer » dans le journal, pas de rouge.
// L'image est enregistrée dans le dépôt (monagent/<date>.jpg) et servie par clicvia.com : Instagram et Facebook la lisent à cette adresse.
//
// Phases (workflow monagent-post.yml) : PHASE=fabriquer (image + légende + mémoire « en attente »), git commit, PHASE=publier (attend que
// l'image soit en ligne, publie, note les liens). ESSAI=1 : fabriquer seulement. JOUR=AAAA-MM-JJ : date simulée (tests).
import { readFileSync, writeFileSync, existsSync, mkdirSync, statSync } from "fs";
import { execFileSync, spawnSync } from "child_process";
import { join, dirname } from "path";
import { fileURLToPath, pathToFileURL } from "url";
import { createRequire } from "module";

const RACINE = join(dirname(fileURLToPath(import.meta.url)), "..");
const SITE = "https://monagent.clicvia.com/";
const HOTE_IMAGES = "https://clicvia.com/monagent/";
const MEMOIRE = join(RACINE, "donnees", "monagent-posts.json");
const DOSSIER = join(RACINE, "monagent");
export const W = 1080, H = 1350;
export const DEPART = Date.UTC(2026, 10, 9);
const GRAPH = "https://graph.facebook.com/v21.0";

// ---------------------------------------------------------------- mots interdits (décision d'Ahmed du 02/11/2026 : aucun lien visible)
export const INTERDITS = [/immobilier\s*tunisie/i, /\bclicvia\b(?!\.com\/monagent|\.com\b)/i, /https?:\/\/clicvia\.com/i, /\bIA\b/, /intelligence artificielle/i, /ذكاء/];
export const interdit = s => { const t = String(s || "").replace(/monagent\.clicvia\.com/g, "MONAGENT"); return INTERDITS.find(r => r.test(t)) || null; };

// ---------------------------------------------------------------- styles : rien de commun avec les Reels de l'Immobilier
// fond, fond 2, accent, texte, bulle du visiteur, bulle de l'agent, texte de la bulle agent
export const PALETTES = [
  ["#0B1220", "#121C33", "#4F8CFF", "#FFFFFF", "#1E2A44", "#0F5BD8", "#FFFFFF"],   // encre et bleu électrique (le site, de nuit)
  ["#F5F7FB", "#FFFFFF", "#0F5BD8", "#0B1220", "#E8F0FE", "#0F5BD8", "#FFFFFF"],   // le site, de jour
  ["#062C3F", "#0B3B52", "#19C2A0", "#FFFFFF", "#114B66", "#19C2A0", "#042A24"],   // océan et menthe
  ["#1B1340", "#271C5A", "#A78BFA", "#FFFFFF", "#33266E", "#8B5CF6", "#FFFFFF"],   // violet profond
  ["#FFFFFF", "#F3F4F6", "#111827", "#111827", "#F3F4F6", "#111827", "#FFFFFF"],   // blanc et noir, minimal
  ["#0F2A3D", "#163A52", "#FFB020", "#FFFFFF", "#1E4866", "#FFB020", "#1A1A1A"],   // nuit bleue et ambre
  ["#EAF3FF", "#FFFFFF", "#0A3F99", "#0A3F99", "#FFFFFF", "#0A3F99", "#FFFFFF"],   // ciel pâle et bleu foncé
  ["#101820", "#182430", "#5EEAD4", "#FFFFFF", "#223240", "#14B8A6", "#042F2E"],   // graphite et turquoise
];
export const POLICES = [["Plus Jakarta Sans", "IBM Plex Sans Arabic"], ["Manrope", "Readex Pro"], ["Sora", "Noto Kufi Arabic"], ["Outfit", "Rubik"]];
export const MISES = ["chat", "recherche", "sms", "fiche", "ticket"];
// accroches de la légende (première ligne : une question que le lecteur se pose, ou un chiffre) ; {q} = la question, {n} = le nombre
export const ACCROCHES = [
  ["{q} 👇", "{q} 👇"],
  ["On a posé la question à notre agent. Réponse : {n} annonces.", "سألنا وكيلنا. الجواب: {n} إعلان."],
  ["{n} annonces en une phrase. Sans formulaire.", "{n} إعلان بجملة واحدة. بلا استمارة."],
  ["Vous l'auriez trouvé en 10 secondes ?", "كنت تلقاه في 10 ثواني؟"],
  ["Écrivez comme vous parlez, il comprend.", "اكتب كيما تتكلم، هو يفهم."],
  ["Une phrase. {n} réponses. Zéro inscription.", "جملة وحدة. {n} إجابة. بلا تسجيل."],
  ["Le réflexe avant d'appeler une agence 👇", "العادة الجديدة قبل ما تتصل بوكالة 👇"],
  ["Combien ça coûte vraiment ? Demandez-lui.", "بكم بالحق؟ اسألو."],
  ["Testé ce matin : {n} annonces pour cette phrase.", "جرّبناه الصباح: {n} إعلان على هذه الجملة."],
  ["En français, en arabe ou en tunisien : même réponse.", "بالفرنسية، بالعربية ولا بالتونسي: نفس الجواب."],
  ["Pas de filtres à cocher. Juste votre phrase.", "لا خانات تعمّرها. غير جملتك."],
  ["La réponse tient en une image 👇", "الجواب في صورة وحدة 👇"],
];
export const HASHTAGS = ["#Tunisie", "#تونس", "#Logement", "#Location", "#Achat", "#كراء", "#بيع", "#Appartement", "#Maison", "#Terrain", "#شقة", "#منزل"];

// ---------------------------------------------------------------- données du site Mon agent (mêmes fichiers que le site)
const TYPES = ["appartement", "maison", "terrain", "bureau", "commerce", "industriel", "terrainind", "agricole", "autre"];
const SORTES = ["studio", "duplex", "penthouse", "villa", "etage_villa", "maison_trad"];
const STRICTES = { studio: 1, duplex: 1, penthouse: 1, etage_villa: 1 };

export function telecharger(url) {
  // Node lit directement ; dans une session qui passe par un relais (HTTPS_PROXY), curl le respecte
  try { return execFileSync("curl", ["-sfL", "--max-time", "120", url], { maxBuffer: 64 << 20 }).toString("utf8"); }
  catch (e) { throw new Error("téléchargement impossible : " + url); }
}

export function chargerDonnees() {
  const js = process.env.MAI_DONNEES ? readFileSync(process.env.MAI_DONNEES, "utf8") : telecharger(SITE + "donnees/index.js");
  const d = JSON.parse(js.slice(js.indexOf("{"), js.lastIndexOf("}") + 1));
  if (!Array.isArray(d.a) || d.a.length < 1000 || !Array.isArray(d.g) || d.g.length !== 24) throw new Error("données du site illisibles ou incomplètes");
  return d;
}
export function chargerComprendre() {
  const src = process.env.MAI_COMPRENDRE ? readFileSync(process.env.MAI_COMPRENDRE, "utf8") : telecharger(SITE + "assets/comprendre.js");
  const mod = { exports: {} };
  new Function("module", "exports", "window", src)(mod, mod.exports, {});
  if (typeof mod.exports.comprendre !== "function") throw new Error("comprendre.js : fonction comprendre absente");
  return mod.exports.comprendre;
}

// même filtre que assets/agent.js (criteres + filtrer, STRICT : sans assouplissement) : le chiffre publié = celui que le visiteur verra
export function filtrer(D, q) {
  const dansZone = (a, z) => z.k === "g" ? a[3] === z.g : z.k === "l" ? a[4] === z.l : (a[3] === z.g && !!D.l[a[4]] && D.l[a[4]][4] === z.d);
  const cs = [];
  if (q.t) cs.push(a => a[1] === (q.t === "v" ? 1 : 0));
  if (q.per) cs.push(a => a[1] === 0 && (q.per === "m" ? a[13] === 0 : q.per === "c" ? a[13] > 0 : a[13] === (q.per === "n" ? 1 : 2)));
  else cs.push(a => a[1] === 1 || !a[13]);
  if (q.types.length) { const ti = q.types.map(y => TYPES.indexOf(y)); cs.push(a => ti.includes(a[2])); }
  const st = q.sortes.filter(s => STRICTES[s]);
  if (st.length) { const si = st.map(s => SORTES.indexOf(s)); cs.push(a => si.includes(a[9]) || (si.includes(0) && a[7] === 0)); }
  if (q.c !== null) cs.push(a => a[7] !== null && a[7] === q.c);
  if (q.cMin !== null) cs.push(a => a[7] !== null && a[7] >= q.cMin);
  if (q.pMin !== null || q.pMax !== null) cs.push(a => a[5] !== null && (q.pMax === null || a[5] <= q.pMax) && (q.pMin === null || a[5] >= q.pMin));
  if (q.sMin !== null || q.sMax !== null) cs.push(a => a[6] !== null && (q.sMax === null || a[6] <= q.sMax) && (q.sMin === null || a[6] >= q.sMin));
  q.at.forEach(k => cs.push(a => !!(a[8] & (1 << k))));
  q.sansAt.forEach(k => cs.push(a => !(a[8] & (1 << k))));
  if (q.et !== null) cs.push(a => a[10] === q.et);
  if (q.zones.length) cs.push(a => q.zones.some(z => dansZone(a, z)));
  return D.a.filter(a => cs.every(c => c(a)));
}

// ---------------------------------------------------------------- questions : français, arabe, tunisien en lettres latines
export const TYPES_Q = {
  appartement: { fr: ["un appartement", "appartement"], ar: "شقة", tn: "chka", tag: "#Appartement #شقة" },
  maison: { fr: ["une maison", "maison"], ar: "دار", tn: "dar", tag: "#Maison #منزل" },
  terrain: { fr: ["un terrain", "terrain"], ar: "أرض", tn: "ardh", tag: "#Terrain #أرض" },
  commerce: { fr: ["un local commercial", "local commercial"], ar: "محل", tn: "7anout", tag: "#Local #محل" },
};
const TR = { l: { fr: "à louer", ar: "للكراء", tn: "lel kra", tag: "#Location #كراء" }, v: { fr: "à vendre", ar: "للبيع", tn: "lel bi3", tag: "#Achat #بيع" } };
const lieuFr = nom => /^Le /.test(nom) ? "au " + nom.slice(3) : /^La /.test(nom) ? "à " + nom : "à " + nom;
export const GABARITS = [     // [langue, phrase] ; {T} type, {t} transaction, {L} lieu, {S} « S+2 »
  ["fr", "Je cherche {Tun} {S} {t} {L}"], ["fr", "{T} {S} {t} {L}, vous avez ?"], ["fr", "{Tun} {S} {t} {L}, pas trop cher"],
  ["ar", "نلوّج على {T} {S} {t} في {L}"], ["ar", "{T} {S} {t} في {L}؟"], ["ar", "عندكم {T} {S} {t} في {L}؟"],
  ["tn", "Nlawej 3la {T} {S} {t} fi {L}"], ["tn", "Famma {T} {S} {t} fi {L} ?"], ["tn", "N7eb {T} {S} {t} fi {L}"],
];
const majuscule = s => s.charAt(0).toUpperCase() + s.slice(1);

export function phrase(gab, type, tr, g, pieces) {
  const [lg, m] = gab, ty = TYPES_Q[type], S = pieces ? "S+" + pieces : "";
  let s = lg === "fr" ? m.replace("{Tun}", ty.fr[0]).replace("{T}", majuscule(ty.fr[1])).replace("{t}", TR[tr].fr).replace("{L}", lieuFr(g[1]))
    : lg === "ar" ? m.replace("{T}", ty.ar).replace("{t}", TR[tr].ar).replace("{L}", g[2] || g[1])
    : m.replace("{T}", ty.tn).replace("{t}", TR[tr].tn).replace("{L}", g[1]);
  s = s.replace("{S}", S).replace(/\s+/g, " ").replace(/\s+([؟,])/g, "$1").replace(/\s*\?/g, "\u00a0?").trim();   // français : espace insécable avant « ? »
  return lg === "ar" ? s : majuscule(s);
}

// toutes les questions possibles dont la réponse est assez riche (>= MIN annonces) et que le moteur du site COMPREND exactement comme voulu
export const MIN = 15;
export function questions(D, comprendre, minimum = MIN) {
  const out = [];
  D.g.forEach((g, gi) => {
    for (const type of Object.keys(TYPES_Q)) for (const tr of ["l", "v"]) {
      const pieces = type === "appartement" ? [null, 1, 2, 3] : [null];
      for (const p of pieces) {
        let n = null;
        for (let k = 0; k < GABARITS.length; k++) {
          const texte = phrase(GABARITS[k], type, tr, g, p);
          const q = comprendre(texte, D);
          const bon = q.t === tr && q.types.length === 1 && q.types[0] === type && q.c === p && q.zones.length === 1 && q.zones[0].k === "g" && q.zones[0].g === gi
            && q.pMax === null && q.pMin === null && q.sortes.filter(s => STRICTES[s]).length === 0 && !q.at.length && !q.sansAt.length;
          if (!bon) continue;
          if (n === null) n = filtrer(D, q);
          if (n.length < minimum) break;
          out.push({ texte, langue: GABARITS[k][0], gabarit: k, type, tr, g: g[0], gi, pieces: p, q, n: n.length });
        }
      }
    }
  });
  return out;
}

// ---------------------------------------------------------------- chiffres de la réponse
export const nb = v => Math.round(v).toLocaleString("fr-FR").replace(/ | /g, " ");
export function reponse(D, liste, q, ar = false) {
  const prix = liste.map(a => a[5]).filter(v => v !== null && v > 0).sort((x, y) => x - y);
  const unite = q.t === "v" ? " DT" : " DT / mois";
  const quart = k => prix.length >= 8 ? prix[Math.floor((prix.length - 1) * k)] : null;
  const lieux = {};
  liste.forEach(a => { const l = D.l[a[4]]; if (l) { const nom = (ar && l[3]) || l[2]; lieux[nom] = (lieux[nom] || 0) + 1; } });
  const top = Object.entries(lieux).sort((x, y) => y[1] - x[1]).slice(0, 3);
  return { n: liste.length, min: prix.length ? prix[0] : null, q1: quart(0.25), q3: quart(0.75), unite, top, photos: liste.filter(a => a[12]).length };
}

// ---------------------------------------------------------------- choix du jour (différent des précédents)
export const lireMemoire = () => existsSync(MEMOIRE) ? JSON.parse(readFileSync(MEMOIRE, "utf8")) : { posts: [] };
export function choisirStyle(n, histo) {
  const recents = histo.filter(x => "style" in x).map(x => x.style);
  for (let k = 0; k < 400; k++) {
    const m = n + k;
    if (recents.slice(0, 4).every(r => m % PALETTES.length !== r % PALETTES.length && m % MISES.length !== r % MISES.length && m % POLICES.length !== r % POLICES.length)
        && recents.slice(0, 10).every(r => m % ACCROCHES.length !== r % ACCROCHES.length)) return m;
  }
  return n;
}
export function choisirQuestion(n, qs, histo) {
  // jamais un gouvernorat des 6 derniers posts, jamais le même couple type + transaction que les 2 derniers, jamais la même langue que la veille
  const gs = histo.slice(0, 6).map(x => x.g), couples = histo.slice(0, 2).map(x => x.type + x.tr), lg = histo[0] && histo[0].langue;
  const ok = qs.filter(x => !gs.includes(x.g) && !couples.includes(x.type + x.tr) && x.langue !== lg);
  const riches = ok.filter(x => x.n >= 40);          // une réponse riche convainc plus qu'une poignée d'annonces
  const liste = riches.length ? riches : ok.length ? ok : qs;
  // mélange déterministe par le numéro du jour (un ordre différent chaque jour, reproductible)
  const h = s => { let v = 2166136261; for (const c of s) v = Math.imul(v ^ c.charCodeAt(0), 16777619) >>> 0; return v; };
  return liste.slice().sort((x, y) => h(n + x.texte) - h(n + y.texte))[0];
}

// ---------------------------------------------------------------- image (HTML -> Chrome -> JPEG)
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
export function html(choix, rep, style) {
  const pal = PALETTES[style % PALETTES.length], [pLat, pAr] = POLICES[style % POLICES.length], mise = MISES[style % MISES.length];
  const [fond, fond2, accent, texte, bulleV, bulleA, texteA] = pal;
  const ar = choix.langue === "ar", dir = ar ? "rtl" : "ltr";
  const L = (fr, a) => ar ? a : fr;
  const prixMin = rep.min !== null ? L("à partir de ", "ابتداءً من ") + nb(rep.min) + L(rep.unite, rep.unite.replace("DT", "د").replace("mois", "الشهر")) : "";
  const moitie = rep.q1 !== null ? L(`la moitié entre ${nb(rep.q1)} et ${nb(rep.q3)}`, `النصف بين ${nb(rep.q1)} و ${nb(rep.q3)}`) : "";
  const lieux = rep.top.length ? L("surtout à ", "خاصة في ") + rep.top.map(x => x[0]).join(L(", ", "، ")) : "";
  const trouve = L(`J'ai trouvé <b>${nb(rep.n)} annonces</b>.`, `لقيت <b>${nb(rep.n)} إعلان</b>.`);
  const cta = L("Posez votre question", "اطرح سؤالك"), gratuit = L("gratuit · sans inscription", "مجاني · بلا تسجيل");
  const site = "monagent.clicvia.com";
  const fonts = `https://fonts.googleapis.com/css2?family=${encodeURIComponent(pLat).replace(/%20/g, "+")}:wght@500;700;800&family=${encodeURIComponent(pAr).replace(/%20/g, "+")}:wght@500;700&display=swap`;
  const base = `<!doctype html><html lang="${ar ? "ar" : "fr"}" dir="${dir}"><head><meta charset="utf-8"><link rel="stylesheet" href="${fonts}">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:${W}px;height:${H}px;overflow:hidden}
body{background:${fond};color:${texte};font-family:"${pLat}","${pAr}",system-ui,sans-serif;font-weight:500;position:relative}
[dir=rtl] body,body[dir=rtl]{font-family:"${pAr}","${pLat}",system-ui,sans-serif}
b{font-weight:800}
.marque{position:absolute;left:64px;right:64px;bottom:56px;display:flex;align-items:center;justify-content:space-between;font-size:30px}
.marque .site{font-weight:800;color:${accent};letter-spacing:-.01em}
.marque .g{opacity:.75;font-size:26px}
.cta{display:inline-block;background:${accent};color:${fond};font-weight:800;font-size:38px;padding:22px 44px;border-radius:999px}
.q{font-size:44px;line-height:1.25;font-weight:700}
.r{font-size:40px;line-height:1.3}
.r b{font-size:1.15em}
.petit{font-size:30px;opacity:.85;line-height:1.35}
.pastille{display:inline-block;background:${fond2};color:${texte};border:3px solid ${accent};border-radius:999px;padding:10px 24px;font-size:28px;font-weight:700}
</style></head><body dir="${dir}">`;
  const marque = `<div class="marque"><span class="site">${site}</span><span class="g">${esc(gratuit)}</span></div>`;
  let corps = "";
  if (mise === "chat") corps = `<style>
.fil{position:absolute;top:120px;left:64px;right:64px;display:flex;flex-direction:column;gap:36px}
.b{max-width:82%;padding:34px 40px;border-radius:40px;font-size:42px;line-height:1.3}
.v{align-self:flex-start;background:${bulleV};color:${texte};border-bottom-left-radius:10px}
[dir=rtl] .v{align-self:flex-end;border-radius:40px;border-bottom-right-radius:10px}
.a{align-self:flex-end;background:${bulleA};color:${texteA};border-bottom-right-radius:10px}
[dir=rtl] .a{align-self:flex-start;border-radius:40px;border-bottom-left-radius:10px}
.a .petit{opacity:.9;margin-top:14px}
.heure{font-size:26px;opacity:.6;text-align:center}
.ctaz{position:absolute;left:64px;right:64px;bottom:150px;text-align:center}
</style><div class="fil"><div class="heure">${L("aujourd'hui", "اليوم")}</div>
<div class="b v">${esc(choix.texte)}</div>
<div class="b a">${trouve}<div class="petit">${esc(prixMin)}${moitie ? " · " + esc(moitie) : ""}</div>${lieux ? `<div class="petit">${esc(lieux)}</div>` : ""}</div>
<div class="b v">${L("Je peux voir ?", "نجم نشوف؟")}</div>
<div class="b a">${L("Oui, écrivez-moi la même phrase sur", "إي، اكتبلي نفس الجملة على")} <b>${site}</b></div></div>
<div class="ctaz"><span class="cta">${esc(cta)}</span></div>${marque}`;
  else if (mise === "recherche") corps = `<style>
.titre{position:absolute;top:110px;left:64px;right:64px;font-size:40px;font-weight:700;opacity:.8}
.barre{position:absolute;top:210px;left:64px;right:64px;background:${fond2};border:4px solid ${accent};border-radius:28px;padding:34px 40px;font-size:42px;line-height:1.3;display:flex;gap:24px;align-items:center}
.barre .loupe{width:44px;height:44px;border:6px solid ${accent};border-radius:50%;flex:none;position:relative}
.barre .loupe:after{content:"";position:absolute;width:6px;height:22px;background:${accent};right:-12px;bottom:-16px;transform:rotate(-45deg)}
.carte{position:absolute;top:470px;left:64px;right:64px;background:${bulleA};color:${texteA};border-radius:36px;padding:48px 48px}
.carte .n{font-size:110px;font-weight:800;line-height:1;letter-spacing:-.03em}
.carte .l{font-size:40px;margin-top:8px;font-weight:700}
.carte .petit{margin-top:26px;font-size:32px;opacity:.92}
.ctaz{position:absolute;left:64px;right:64px;bottom:150px;text-align:center}
</style><div class="titre">${L("Tapez votre recherche comme vous la diriez", "اكتب تلقّيك كيما تقولو")}</div>
<div class="barre"><span class="loupe"></span><span>${esc(choix.texte)}</span></div>
<div class="carte"><div class="n">${nb(rep.n)}</div><div class="l">${L("annonces trouvées", "إعلان لقيناه")}</div>
<div class="petit">${esc(prixMin)}</div>${moitie ? `<div class="petit">${esc(moitie)}</div>` : ""}${lieux ? `<div class="petit">${esc(lieux)}</div>` : ""}</div>
<div class="ctaz"><span class="cta">${esc(cta)}</span></div>${marque}`;
  else if (mise === "sms") corps = `<style>
.tel{position:absolute;top:80px;left:150px;right:150px;bottom:170px;background:${fond2};border:14px solid ${accent};border-radius:70px;padding:60px 40px 40px;overflow:hidden;display:flex;flex-direction:column}
.tel .nom{text-align:center;font-size:28px;font-weight:700;opacity:.7;margin-bottom:28px}
.b{max-width:88%;padding:24px 30px;border-radius:32px;font-size:32px;line-height:1.3;margin-bottom:22px}
.v{background:${bulleV};color:${texte};margin-left:auto;border-bottom-right-radius:8px}
[dir=rtl] .v{margin-left:0;margin-right:auto;border-radius:34px;border-bottom-left-radius:8px}
.a{background:${bulleA};color:${texteA};border-bottom-left-radius:8px}
[dir=rtl] .a{border-radius:34px;border-bottom-right-radius:8px}
.a .petit{opacity:.9;margin-top:10px;font-size:26px}
.saisie{margin-top:auto;background:${fond};color:${texte};border-radius:999px;padding:20px 32px;font-size:28px;opacity:.9}
</style><div class="tel"><div class="nom">${L("Mon agent", "وكيلي")} · ${L("en ligne", "متّصل")}</div>
<div class="b v">${esc(choix.texte)}</div>
<div class="b a">${trouve}<div class="petit">${esc(prixMin)}</div>${moitie ? `<div class="petit">${esc(moitie)}</div>` : ""}${lieux ? `<div class="petit">${esc(lieux)}</div>` : ""}</div>
<div class="b v">${L("Et pour voir les photos ?", "والصور؟")}</div>
<div class="b a">${L("Tout est sur", "الكل على")} <b>${site}</b> — ${esc(gratuit)}</div>
<div class="saisie">${L("Écrivez votre phrase…", "اكتب جملتك…")}</div></div>${marque}`;
  else if (mise === "fiche") corps = `<style>
.haut{position:absolute;top:100px;left:64px;right:64px}
.haut .q{background:${bulleV};padding:34px 40px;border-radius:30px}
.chiffre{position:absolute;top:400px;left:64px;right:64px;text-align:center}
.chiffre .n{font-size:220px;font-weight:800;line-height:1;color:${accent};letter-spacing:-.04em}
.chiffre .l{font-size:48px;font-weight:700;margin-top:10px}
.lignes{position:absolute;top:760px;left:64px;right:64px;display:flex;flex-direction:column;gap:20px;align-items:center}
.ctaz{position:absolute;left:64px;right:64px;bottom:150px;text-align:center}
</style><div class="haut"><div class="q">« ${esc(choix.texte)} »</div></div>
<div class="chiffre"><div class="n">${nb(rep.n)}</div><div class="l">${L("annonces, pour cette seule phrase", "إعلان، على هذه الجملة فقط")}</div></div>
<div class="lignes">${prixMin ? `<span class="pastille">${esc(prixMin)}</span>` : ""}${moitie ? `<span class="pastille">${esc(moitie)}</span>` : ""}${lieux ? `<span class="pastille">${esc(lieux)}</span>` : ""}</div>
<div class="ctaz"><span class="cta">${esc(cta)}</span></div>${marque}`;
  else corps = `<style>
.q1{position:absolute;top:0;left:0;right:0;height:560px;background:${bulleA};color:${texteA};padding:120px 72px 0}
.q1 .e{font-size:30px;opacity:.8;margin-bottom:26px;font-weight:700}
.q1 .q{font-size:52px;line-height:1.2}
.dent{position:absolute;top:530px;left:0;right:0;height:60px;background:radial-gradient(circle at 30px 0, ${bulleA} 30px, transparent 31px) 0 0/60px 60px}
.r2{position:absolute;top:640px;left:72px;right:72px}
.r2 .e{font-size:30px;opacity:.75;margin-bottom:22px;font-weight:700}
.r2 .r{font-size:46px}
.r2 .petit{margin-top:22px;font-size:32px}
.ctaz{position:absolute;left:64px;right:64px;bottom:150px;text-align:center}
</style><div class="q1"><div class="e">${L("LA QUESTION", "السؤال")}</div><div class="q">${esc(choix.texte)}</div></div><div class="dent"></div>
<div class="r2"><div class="e">${L("LA RÉPONSE DE MON AGENT", "جواب وكيلي")}</div><div class="r">${trouve}</div>
<div class="petit">${esc(prixMin)}${moitie ? "<br>" + esc(moitie) : ""}${lieux ? "<br>" + esc(lieux) : ""}</div></div>
<div class="ctaz"><span class="cta">${esc(cta)}</span></div>${marque}`;
  return base + corps + "</body></html>";
}

export function navigateur() {
  const cands = [process.env.NAVIGATEUR, "/opt/pw-browsers/chromium", "google-chrome", "chromium", "chromium-browser", "chrome"];
  for (const c of cands) {
    if (!c) continue;
    if (c.startsWith("/")) { if (existsSync(c)) return c; continue; }
    const r = spawnSync("which", [c]); if (r.status === 0) return r.stdout.toString().trim();
  }
  return null;
}
export function photographier(fichierHtml, sortiePng) {
  const nav = navigateur();
  if (!nav) throw new Error("Chrome introuvable (variable NAVIGATEUR)");
  // la fenêtre sans écran ne dessine pas ses ~85 derniers pixels (09/11/2026 : ligne du bas invisible) : capture plus haute, recadrée en JPEG
  spawnSync(nav, ["--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-sandbox", "--force-device-scale-factor=1", `--window-size=${W},${H + 160}`,
    "--virtual-time-budget=8000", `--screenshot=${sortiePng}`, pathToFileURL(fichierHtml).href], { timeout: 120000 });
  if (!existsSync(sortiePng) || statSync(sortiePng).size < 10000) throw new Error("image non fabriquée");
  return sortiePng;
}
export function enJpeg(png, jpg) {
  const ff = spawnSync(process.env.FFMPEG || "ffmpeg", ["-y", "-loglevel", "error", "-i", png, "-vf", `crop=${W}:${H}:0:0`, "-q:v", "3", jpg]);
  if (ff.status !== 0 || !existsSync(jpg)) {
    const py = spawnSync("python3", ["-c", `from PIL import Image; Image.open(${JSON.stringify(png)}).convert("RGB").crop((0, 0, ${W}, ${H})).save(${JSON.stringify(jpg)}, quality=90)`]);
    if (py.status !== 0 || !existsSync(jpg)) throw new Error("conversion JPEG impossible (ffmpeg ou Pillow)");
  }
  return jpg;
}

// ---------------------------------------------------------------- légende
export function lien(choix, source, date) {
  return `${SITE}?q=${encodeURIComponent(choix.texte)}&utm_source=${source}&utm_medium=post&utm_campaign=monagent-${date}`;
}
export function legende(choix, rep, style, date, reseau) {
  const ar = choix.langue === "ar";
  const acc = ACCROCHES[style % ACCROCHES.length][ar ? 1 : 0].replace("{q}", choix.texte).replace("{n}", nb(rep.n));
  const L = (fr, a) => ar ? a : fr;
  const chiffres = [L(`${nb(rep.n)} annonces trouvées pour « ${choix.texte} »`, `${nb(rep.n)} إعلان على «${choix.texte}»`)];
  if (rep.min !== null) chiffres.push(L(`à partir de ${nb(rep.min)}${rep.unite}`, `ابتداءً من ${nb(rep.min)}${rep.unite.replace("DT", "د").replace("mois", "الشهر")}`));
  if (rep.q1 !== null) chiffres.push(L(`la moitié entre ${nb(rep.q1)} et ${nb(rep.q3)}`, `النصف بين ${nb(rep.q1)} و ${nb(rep.q3)}`));
  const ou = reseau === "instagram" ? L("Écrivez votre phrase sur monagent.clicvia.com (gratuit, sans inscription).", "اكتب جملتك على monagent.clicvia.com (مجاني، بلا تسجيل).")
    : L("👉 Voyez la réponse complète (gratuit, sans inscription) : ", "👉 شوف الجواب الكامل (مجاني، بلا تسجيل): ") + lien(choix, reseau, date);
  const autre = ar ? `${nb(rep.n)} annonces pour « ${choix.texte} ». Écrivez comme vous parlez : français, arabe ou tunisien.` : `${nb(rep.n)} إعلان على «${choix.texte}». اكتب كيما تتكلم: فرنسية، عربية ولا تونسي.`;
  const tags = [...new Set([TYPES_Q[choix.type].tag, TR[choix.tr].tag, "#" + choix.g.split("-").map(majuscule).join(""), "#Tunisie", "#تونس", "#Logement"].join(" ").split(" "))].slice(0, 10).join(" ");
  return [acc, "", ...chiffres.map(x => "• " + x), "", ou, "", autre, "", tags].join("\n");
}

// ---------------------------------------------------------------- API Facebook / Instagram (le jeton n'est jamais affiché)
async function api(methode, chemin, jeton, donnees) {
  let u = `${GRAPH}/${chemin}`, init = { method: methode };
  if (methode === "GET") u += (u.includes("?") ? "&" : "?") + "access_token=" + encodeURIComponent(jeton);
  else init.body = new URLSearchParams({ ...(donnees || {}), access_token: jeton });
  const r = await fetch(u, init), rep = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`refus de l'API (${chemin.split("?")[0].split("/").pop()}) — ${(rep.error || {}).message || r.status} (code ${(rep.error || {}).code || r.status})`);
  return rep;
}
async function attendreEnLigne(url, minutes = 8) {
  for (let i = 0; i < minutes * 6; i++) {
    try { const r = await fetch(url, { method: "HEAD", cache: "no-store" }); if (r.ok) return true; } catch (e) { /* pas encore */ }
    await new Promise(x => setTimeout(x, 10000));
  }
  return false;
}
async function publierFacebook(imageUrl, texte, repere) {
  const page = process.env.MONAGENT_FB_PAGE_ID || process.env.FB_PAGE_ID, jeton = process.env.MONAGENT_FB_PAGE_TOKEN || process.env.FB_PAGE_TOKEN;
  if (!page || !jeton) throw new Error("secrets FB_PAGE_ID / FB_PAGE_TOKEN absents : rien n'est publié");
  const recents = (await api("GET", `${page}/feed?fields=message&limit=25`, jeton)).data || [];
  if (recents.some(x => (x.message || "").includes(repere))) { console.log("Facebook : déjà publiée (relance tardive de GitHub)"); return "déjà publiée"; }
  const r = await api("POST", `${page}/photos`, jeton, { url: imageUrl, message: texte });
  const lienFb = `https://www.facebook.com/${r.post_id || r.id}`;
  console.log("Publié sur Facebook : " + lienFb);
  return lienFb;
}
async function publierInstagram(imageUrl, texte, repere) {
  const ig = process.env.MONAGENT_IG_USER_ID, jeton = process.env.MONAGENT_FB_PAGE_TOKEN || process.env.FB_PAGE_TOKEN;
  if (!ig) { console.log("Instagram : pas encore de compte propre à Mon agent (secret MONAGENT_IG_USER_ID) — voir GERER SANS CLAUDE ; Facebook seulement."); return null; }
  const recents = (await api("GET", `${ig}/media?fields=caption&limit=12`, jeton)).data || [];
  if (recents.some(x => (x.caption || "").includes(repere))) { console.log("Instagram : déjà publiée"); return "déjà publiée"; }
  const cont = await api("POST", `${ig}/media`, jeton, { image_url: imageUrl, caption: texte });
  for (let i = 0; i < 30; i++) {
    const e = await api("GET", `${cont.id}?fields=status_code,status`, jeton);
    if (e.status_code === "FINISHED") break;
    if (e.status_code === "ERROR" || e.status_code === "EXPIRED") throw new Error("Instagram a refusé l'image — " + e.status);
    await new Promise(x => setTimeout(x, 5000));
  }
  const pub = await api("POST", `${ig}/media_publish`, jeton, { creation_id: cont.id });
  const lienIg = (await api("GET", `${pub.id}?fields=permalink`, jeton)).permalink || pub.id;
  console.log("Publié sur Instagram : " + lienIg);
  return lienIg;
}

// ---------------------------------------------------------------- phases
export function numeroDuJour(date) { return Math.max(0, Math.floor((Date.UTC(+date.slice(0, 4), +date.slice(5, 7) - 1, +date.slice(8, 10)) - DEPART) / 864e5)); }

export function fabriquer(date, D, comprendre, dossier = DOSSIER) {
  const memoire = lireMemoire(), histo = memoire.posts;
  if (histo[0] && histo[0].date === date && histo[0].fb) { console.log("déjà publiée aujourd'hui : rien à faire"); return null; }
  const n = numeroDuJour(date), qs = questions(D, comprendre);
  if (!qs.length) throw new Error("aucune question assez riche (données du site vides ?)");
  const style = choisirStyle(n, histo), choix = choisirQuestion(n, qs, histo);
  const rep = reponse(D, filtrer(D, choix.q), choix.q, choix.langue === "ar");
  const page = html(choix, rep, style);
  const textes = { facebook: legende(choix, rep, style, date, "facebook"), instagram: legende(choix, rep, style, date, "instagram") };
  for (const t of [page, textes.facebook, textes.instagram]) { const m = interdit(t); if (m) throw new Error("mot interdit dans la publication : " + m); }
  mkdirSync(dossier, { recursive: true });
  const base = join(dossier, date);
  writeFileSync(base + ".html", page);
  photographier(base + ".html", base + ".png");
  enJpeg(base + ".png", base + ".jpg");
  writeFileSync(base + ".txt", textes.facebook + "\n\n=== Instagram ===\n" + textes.instagram, "utf8");
  const post = { date, style, question: choix.texte, langue: choix.langue, g: choix.g, type: choix.type, tr: choix.tr, pieces: choix.pieces, n: rep.n,
    palette: style % PALETTES.length, mise: MISES[style % MISES.length], police: POLICES[style % POLICES.length][0], image: date + ".jpg" };
  memoire.posts = [post, ...histo.filter(x => x.date !== date)].slice(0, 400);
  mkdirSync(dirname(MEMOIRE), { recursive: true });
  writeFileSync(MEMOIRE, JSON.stringify(memoire, null, 0) + "\n");
  console.log(`Jour ${n} — ${MISES[style % MISES.length]} / palette ${style % PALETTES.length} / ${POLICES[style % POLICES.length][0]} — ${choix.langue} : ${choix.texte} -> ${rep.n} annonces\n---\n${textes.facebook}\n---`);
  return post;
}

async function publier(date) {
  const memoire = lireMemoire(), post = memoire.posts.find(x => x.date === date);
  if (!post) throw new Error("rien à publier pour " + date + " (phase fabriquer d'abord)");
  if (post.fb) { console.log("déjà publiée : " + post.fb); return; }
  const textes = readFileSync(join(DOSSIER, date + ".txt"), "utf8").split("\n\n=== Instagram ===\n");
  const imageUrl = HOTE_IMAGES + post.image, repere = `monagent-${date}`;
  if (!(await attendreEnLigne(imageUrl))) throw new Error("image toujours pas en ligne sur clicvia.com après 8 minutes : " + imageUrl);
  post.fb = await publierFacebook(imageUrl, textes[0], repere);
  try { post.ig = await publierInstagram(imageUrl, textes[1], repere); } catch (e) { console.log("ÉCHEC Instagram : " + e.message); post.ig_erreur = e.message; }
  writeFileSync(MEMOIRE, JSON.stringify(memoire, null, 0) + "\n");
}

async function main() {
  const date = process.env.JOUR || new Date().toISOString().slice(0, 10);
  const phase = process.env.PHASE || (process.env.ESSAI === "1" ? "fabriquer" : "fabriquer");
  if (phase === "fabriquer") { fabriquer(date, chargerDonnees(), chargerComprendre()); if (process.env.ESSAI === "1") console.log("ESSAI : rien n'est publié."); }
  else if (phase === "publier") await publier(date);
  else throw new Error("PHASE inconnue : " + phase);
}
if (process.argv[1] && pathToFileURL(process.argv[1]).href === import.meta.url) main().catch(e => { console.log("ÉCHEC : " + e.message); process.exit(1); });
