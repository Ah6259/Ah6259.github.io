// Publication PRÉPARÉE (image + texte) sur la page Facebook Clicvia (18/10/2026, Ahmed : « fais la publication toi-même »).
// Une publication = une image dans assets/publications/<nom>.jpg + son texte dans donnees/publications/<nom>.txt (même nom).
// Lancement à la main : robot facebook-publication.yml (champ « nom »). Jamais deux fois la même : mémoire donnees/facebook-publications.json
// (et contrôle des dernières publications de la page). Secrets : FB_PAGE_ID, FB_PAGE_TOKEN (jamais dans un fichier). ESSAI=1 : rien n'est publié.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
const NOM = (process.env.NOM || "").trim();
if (!/^[a-z0-9-]+$/.test(NOM)) { console.log("ÉCHEC : nom de publication invalide"); process.exit(1); }
const img = new URL(`../assets/publications/${NOM}.jpg`, import.meta.url), txt = new URL(`../donnees/publications/${NOM}.txt`, import.meta.url);
if (!existsSync(img) || !existsSync(txt)) { console.log("ÉCHEC : image ou texte introuvable pour " + NOM); process.exit(1); }
const message = readFileSync(txt, "utf8").trim();
const urlImage = `https://clicvia.com/assets/publications/${NOM}.jpg`;
const F = new URL("../donnees/facebook-publications.json", import.meta.url);
const memoire = existsSync(F) ? JSON.parse(readFileSync(F, "utf8")) : { publiees: {} };
if (memoire.publiees[NOM]) { console.log("déjà publiée le " + memoire.publiees[NOM].date + " : rien à faire"); process.exit(0); }
console.log(`PUBLICATION ${NOM}\nimage : ${urlImage}\n---\n${message}\n---`);
const r0 = await fetch(urlImage);
if (!r0.ok) { console.log("ÉCHEC : l'image n'est pas encore en ligne (" + r0.status + ")"); process.exit(1); }
if (process.env.ESSAI === "1") { console.log("ESSAI : rien n'est publié."); process.exit(0); }
const ID = process.env.FB_PAGE_ID, JETON = process.env.FB_PAGE_TOKEN;
if (!ID || !JETON) { console.log("ÉCHEC : secrets FB_PAGE_ID / FB_PAGE_TOKEN absents"); process.exit(1); }
const r = await fetch(`https://graph.facebook.com/${ID}/photos`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ url: urlImage, caption: message, access_token: JETON }) });
const rep = await r.json().catch(() => ({}));
if (!r.ok || !(rep.post_id || rep.id)) { console.log("ÉCHEC : Facebook a refusé — " + ((rep.error && [rep.error.message, rep.error.error_user_msg].filter(Boolean).join(" · ")) || r.status)); process.exit(1); }
memoire.publiees[NOM] = { date: new Date().toISOString().slice(0, 10), id: rep.post_id || rep.id };
writeFileSync(F, JSON.stringify(memoire, null, 1) + "\n");
console.log("Publié : https://www.facebook.com/" + (rep.post_id || rep.id));
