// Test du robot « publication du jour de Mon agent immobilier » (tools/monagent_post.mjs) : node tools/test_monagent_post.mjs
// Données : celles du site en ligne (ou MAI_DONNEES / MAI_COMPRENDRE = fichiers locaux). Sans Chrome, la fabrication de l'image est sautée (dit).
import { existsSync, mkdtempSync, rmSync, statSync, readFileSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import * as M from "./monagent_post.mjs";

let ok = 0, ko = 0;
const check = (nom, cond) => { if (cond) ok++; else { ko++; console.log("ÉCHEC " + nom); } };

const D = M.chargerDonnees(), comprendre = M.chargerComprendre();
const qs = M.questions(D, comprendre);
check("questions : au moins 300 questions possibles, dans les 3 écritures (français, arabe, tunisien), sur au moins 15 gouvernorats",
  qs.length >= 300 && ["fr", "ar", "tn"].every(l => qs.some(q => q.langue === l)) && new Set(qs.map(q => q.g)).size >= 15);
check("questions : chaque question est comprise par le moteur du site exactement comme voulue (transaction, type, pièces, gouvernorat)",
  qs.every(q => q.q.t === q.tr && q.q.types[0] === q.type && q.q.c === q.pieces && q.q.zones.length === 1 && q.q.zones[0].g === q.gi));
check("questions : le chiffre publié = le filtre strict du site, au moins " + M.MIN + " annonces", qs.every(q => M.filtrer(D, q.q).length === q.n && q.n >= M.MIN));
check("questions : français avec majuscule et espace insécable avant « ? » ; arabe sans lettres latines hors « S+N »",
  qs.filter(q => q.langue !== "ar").every(q => /^[A-ZÉ]/.test(q.texte) && !/ \?/.test(q.texte)) && qs.filter(q => q.langue === "ar").every(q => !/[a-zA-Z]/.test(q.texte.replace(/S\+\d/g, ""))));

// 40 jours de suite : jamais le même gouvernorat dans les 6 derniers, jamais couleurs + mise en page + police d'un des 4 derniers, jamais l'accroche des 10 derniers
let histo = [], pb = [];
for (let n = 0; n < 40; n++) {
  const style = M.choisirStyle(n, histo), q = M.choisirQuestion(n, qs, histo);
  if (histo.slice(0, 6).some(x => x.g === q.g)) pb.push(`jour ${n} : gouvernorat ${q.g} déjà vu`);
  if (histo.slice(0, 4).some(r => r.style % M.PALETTES.length === style % M.PALETTES.length)) pb.push(`jour ${n} : même palette qu'un des 4 derniers`);
  if (histo.slice(0, 4).some(r => r.style % M.MISES.length === style % M.MISES.length)) pb.push(`jour ${n} : même mise en page qu'un des 4 derniers`);
  if (histo.slice(0, 10).some(r => r.style % M.ACCROCHES.length === style % M.ACCROCHES.length)) pb.push(`jour ${n} : même accroche qu'un des 10 derniers`);
  if (histo[0] && histo[0].langue === q.langue) pb.push(`jour ${n} : même écriture que la veille`);
  histo.unshift({ style, g: q.g, type: q.type, tr: q.tr, langue: q.langue, date: "j" + n });
}
check("40 jours : chaque publication différente des précédentes (gouvernorat, couleurs, mise en page, accroche, écriture)" + (pb.length ? " — " + pb.slice(0, 3).join(" ; ") : ""), pb.length === 0);

// aucun lien visible avec l'autre site ni avec une « IA » : légendes et pages de 40 jours, toutes les mises en page
pb = [];
for (let n = 0; n < 40; n++) {
  const q = M.choisirQuestion(n, qs, histo.slice(n)), style = n, rep = M.reponse(D, M.filtrer(D, q.q), q.q, q.langue === "ar");
  for (const t of [M.html(q, rep, style), M.legende(q, rep, style, "2026-11-10", "facebook"), M.legende(q, rep, style, "2026-11-10", "instagram")]) {
    const m = M.interdit(t); if (m) pb.push(`jour ${n} : ${m}`);
  }
  const l = M.lien(q, "facebook", "2026-11-10");
  if (!/^https:\/\/monagent\.clicvia\.com\/\?q=.+&utm_source=facebook&utm_medium=post&utm_campaign=monagent-2026-11-10$/.test(l)) pb.push(`jour ${n} : lien ${l}`);
  const leg = M.legende(q, rep, style, "2026-11-10", "facebook");
  if (!leg.includes(l) || !leg.includes(M.nb(rep.n)) || (leg.match(/#\w/g) || []).length > 10 || leg.length > 1200) pb.push(`jour ${n} : légende`);
}
check("légendes et images : jamais « Immobilier Tunisie », « Clicvia » (hors l'adresse du site), « IA » ; lien avec ?q= et utm ; chiffre et 10 mots-dièse au plus" + (pb.length ? " — " + pb.slice(0, 3).join(" ; ") : ""), pb.length === 0);
check("mots interdits : le contrôle attrape bien « Immobilier Tunisie », « clicvia.com/ », « IA »", ["voir Immobilier Tunisie", "sur https://clicvia.com/", "notre IA estime", "un lien Clicvia"].every(t => M.interdit(t)) && !M.interdit("monagent.clicvia.com — gratuit"));
check("couleurs et polices : rien de la terre cuite / sable / or ni des polices des Reels de l'Immobilier",
  !M.PALETTES.some(p => p.some(c => /^#(c2410c|fdf3e7|f7dcc0|f2c14e|b4532f|f7f2ea)$/i.test(c))) && !M.POLICES.flat().some(f => /Fraunces|Poppins|Montserrat|Cairo|Tajawal|Amiri|Changa|Almarai|Archivo|Space Grotesk|DM Serif/.test(f)));

// image : 1080 × 1350 en JPEG (seulement si Chrome est là)
if (M.navigateur()) {
  const dossier = mkdtempSync(join(tmpdir(), "monagent-"));
  try {
    const sauve = process.env.HOME; process.env.HOME = sauve;
    const q = M.choisirQuestion(3, qs, []), rep = M.reponse(D, M.filtrer(D, q.q), q.q, q.langue === "ar");
    const base = join(dossier, "essai");
    const { writeFileSync } = await import("fs");
    writeFileSync(base + ".html", M.html(q, rep, 2));
    M.photographier(base + ".html", base + ".png"); M.enJpeg(base + ".png", base + ".jpg");
    const j = readFileSync(base + ".jpg");
    const dims = (() => { let i = 2; while (i < j.length) { if (j[i] !== 0xff) return null; const m = j[i + 1], l = j.readUInt16BE(i + 2); if (m >= 0xc0 && m <= 0xc2) return [j.readUInt16BE(i + 7), j.readUInt16BE(i + 5)]; i += 2 + l; } return null; })();
    check("image : JPEG de 1080 × 1350 (recadrée : le navigateur sans écran ne dessine pas le bas de la fenêtre)", j[0] === 0xff && j[1] === 0xd8 && dims && dims[0] === M.W && dims[1] === M.H && statSync(base + ".jpg").size > 20000);
  } finally { rmSync(dossier, { recursive: true, force: true }); }
} else console.log("(image non testée : Chrome introuvable)");

console.log(ko ? `${ko} ÉCHEC(S), ${ok} réussite(s)` : `${ok}/${ok} vérifications réussies — tout est bon.`);
process.exit(ko ? 1 : 0);
