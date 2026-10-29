# -*- coding: utf-8 -*-
"""Robot « Reels Instagram » de l'Immobilier (demande d'Ahmed du 28/10/2026).

DEUX courtes vidéos verticales par jour (1080 x 1920, ~17 s), une par GOUVERNORAT, à tour de rôle : chacun des 24 revient tous
les 12 jours. Chaque vidéo a ses propres couleurs, sa mise en page, ses polices, ses transitions et sa phrase d'accroche
(Ahmed : « nouvelle couleur, nouveau design et nouveau message attirant à chaque fois ») : tout est choisi d'après le numéro du
créneau, avec des listes de longueurs différentes, donc deux vidéos qui se suivent ne se ressemblent jamais.

Chiffres LUS sur le site publié (immobilier.clicvia.com/donnees/...), jamais inventés : nombre d'annonces du gouvernorat, nouvelles
du jour, prix médian du m² des appartements à vendre, loyer médian d'un S+2, et deux annonces que notre IA juge « peut-être une
bonne affaire » (x % sous les biens semblables). Aucune photo d'annonce (elles appartiennent aux annonceurs), aucun nom de site
source, aucun numéro de téléphone, aucune image générée ni voix ; musique Bach (Musopen, CC0 : tools/reels/musique-licence-CC0.json).

Images dessinées par Chrome sans écran (français + arabe bien formés), vidéo montée par ffmpeg, publiée sur le compte Instagram
relié à la page Facebook Clicvia (API Instagram, envoi « resumable » : aucun fichier à héberger).

RÈGLE GÉNÉRALE du lien (Ahmed, 29/10/2026 : « celui qui regarde la vidéo doit pouvoir cliquer », règle commune § 48) : Instagram ne
rend AUCUN lien cliquable dans un Reel (ni vidéo, ni légende, ni commentaire). Donc chaque vidéo : (1) renvoie au « lien dans la bio »,
qui est https://immobilier.clicvia.com (choix d'Ahmed du 29/10/2026 ; le texte dit de toucher le gouvernorat de la vidéo) ;
la page https://clicvia.com/instagram/ reste refaite à CHAQUE vidéo (lien de secours, page de liens cliquables (gros bouton du gouvernorat de la vidéo en haut,
puis les autres), fichiers instagram/index.html + donnees/reels.json du portail) ; (2) est publiée AUSSI en Reel sur la page Facebook
Clicvia, avec le lien du gouvernorat dans le texte (cliquable sur Facebook).

Secrets du dépôt : FB_PAGE_ID + FB_PAGE_TOKEN (les mêmes que le robot facebook ; le jeton doit avoir en plus les autorisations
instagram_basic et instagram_content_publish). Facultatif : IG_USER_ID (sinon lu sur la page Facebook).
Sans secrets ou avec ESSAI=1 : la vidéo est fabriquée (reels-sortie/) mais rien n'est publié.

  python tools/reels.py                              créneau du moment (CRENEAU=0 matin, 1 soir)
  ESSAI=1 GOUV=sousse python tools/reels.py          essai sur un gouvernorat, sans publier
  ESSAI=1 N=37 python tools/reels.py                 essai du créneau n° 37 (pour voir un autre design)
Variables : FFMPEG (chemin de ffmpeg), NAVIGATEUR (chemin de Chrome), JOUR=AAAA-MM-JJ.
"""
import datetime as dt, html, json, os, pathlib, re, shutil, statistics, subprocess, sys, time, urllib.parse, urllib.request

ICI = pathlib.Path(__file__).resolve().parent
SORTIE = ICI.parent / "reels-sortie"
SITE = "https://immobilier.clicvia.com"
GRAPH = "https://graph.facebook.com/v21.0"
UA = {"User-Agent": "ClicviaRobot/1.0 (+https://clicvia.com/)"}
W, H, FPS, FONDU = 1080, 1920, 30, 0.5

# grands et petits gouvernorats mélangés : les deux vidéos d'un même jour parlent de régions différentes
ORDRE = ["tunis", "sousse", "ariana", "sfax", "nabeul", "monastir", "ben-arous", "bizerte", "mahdia", "manouba", "medenine", "kairouan",
         "gabes", "zaghouan", "beja", "gafsa", "jendouba", "le-kef", "siliana", "kasserine", "sidi-bouzid", "tozeur", "kebili", "tataouine"]
DEPART = dt.date(2026, 10, 29)

# couleurs : fond 1, fond 2, accent, texte, fond des cartes (11 palettes : 24 % 11 = 2, un gouvernorat change de couleurs à chaque tour)
PALETTES = [
    ("#0b3d2e", "#14684d", "#f2c14e", "#ffffff", "rgba(255,255,255,.10)"),   # vert sapin et or
    ("#102a5c", "#1f4fa3", "#ff8a5b", "#ffffff", "rgba(255,255,255,.10)"),   # bleu nuit et corail
    ("#fdf3e7", "#f7dcc0", "#c2410c", "#2b1a0e", "rgba(43,26,14,.07)"),      # sable et terre cuite
    ("#3b0d3f", "#7b1e6b", "#ffd166", "#ffffff", "rgba(255,255,255,.10)"),   # prune et jaune
    ("#eef6f8", "#cfe8ee", "#0e7490", "#0f2a33", "rgba(15,42,51,.07)"),      # ciel clair et bleu canard
    ("#1c1c1c", "#383838", "#e63946", "#ffffff", "rgba(255,255,255,.08)"),   # anthracite et rouge
    ("#f4f1ea", "#e6dfcf", "#1d4ed8", "#1b1b1b", "rgba(0,0,0,.06)"),         # papier et bleu roi
    ("#06404f", "#0b7285", "#a3e635", "#ffffff", "rgba(255,255,255,.10)"),   # pétrole et citron vert
    ("#5c1a1a", "#9b2c2c", "#fde68a", "#ffffff", "rgba(255,255,255,.10)"),   # bordeaux et crème
    ("#fff7ed", "#ffe4c7", "#047857", "#1f2937", "rgba(31,41,55,.06)"),      # pêche et émeraude
    ("#13111c", "#2e2a4a", "#38bdf8", "#ffffff", "rgba(255,255,255,.09)"),   # nuit et cyan
]
# polices (latin, arabe) : 5 paires
POLICES = [("Poppins", "Cairo"), ("Montserrat", "Tajawal"), ("DM Serif Display", "Amiri"), ("Archivo Black", "Changa"), ("Space Grotesk", "Almarai")]
MISES_EN_PAGE = ["degrade", "bandeau", "cadre", "diagonale", "cercle", "colonne", "grille"]          # 7 mises en page
TRANSITIONS = ["fade", "slideleft", "slideup", "circleopen", "wipeleft", "smoothup", "radial", "dissolve", "slideright"]
# accroches (17 : 24 % 17 = 7, un gouvernorat a une nouvelle phrase à chaque tour). {g} = nom du gouvernorat
ACCROCHES = [
    ("Vous cherchez à {g} ?", "تبحث عن سكن في {g}؟"),
    ("{g} : les prix d'aujourd'hui", "{g}: أسعار اليوم"),
    ("Acheter à {g}, c'est combien ?", "الشراء في {g}، بكم؟"),
    ("Louer à {g} sans se tromper", "اكتري في {g} بلا غلطة"),
    ("Ce que coûte vraiment {g}", "كم تكلف {g} حقًّا"),
    ("Nouveau à {g} aujourd'hui", "جديد اليوم في {g}"),
    ("{g} : bonnes affaires repérées", "{g}: صفقات جيدة رصدناها"),
    ("Avant d'acheter à {g}, regardez ça", "قبل ما تشري في {g}، شوف هذا"),
    ("{g} en chiffres", "{g} بالأرقام"),
    ("Le vrai prix du m² à {g}", "السعر الحقيقي للمتر في {g}"),
    ("Toutes les annonces de {g}, gratuites", "كل إعلانات {g}، مجانًا"),
    ("Payer le juste prix à {g}", "ادفع السعر الصحيح في {g}"),
    ("{g} : où en est le marché ?", "{g}: وين وصل السوق؟"),
    ("Un logement à {g} ? Commencez ici", "سكن في {g}؟ ابدأ من هنا"),
    ("Notre IA a regardé {g} pour vous", "ذكاؤنا الاصطناعي درس {g} من أجلك"),
    ("{g} : cher ou pas cher ?", "{g}: غالي ولا رخيص؟"),
    ("Investir à {g} ?", "تستثمر في {g}؟"),
]
FINS = [("Toutes les annonces, gratuites", "كل الإعلانات مجانًا"), ("Comparez avant de signer", "قارن قبل ما تمضي"),
        ("Alertes gratuites chaque jour", "تنبيهات مجانية كل يوم"), ("L'avis de l'IA sur chaque bien", "رأي الذكاء الاصطناعي في كل عقار"),
        ("Le juste prix, quartier par quartier", "السعر الصحيح، حي بحي")]


def lire(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode("utf-8")


def objet_js(texte):
    return json.loads(texte[texte.index("{"):texte.rindex("}") + 1])


def milliers(n):
    return f"{int(round(n)):,}".replace(",", "\u202f")


def creneau():
    if os.environ.get("N"):
        return int(os.environ["N"])
    jour = dt.date.fromisoformat(os.environ["JOUR"]) if os.environ.get("JOUR") else dt.datetime.now(dt.timezone.utc).date()
    return max(0, (jour - DEPART).days) * 2 + (1 if os.environ.get("CRENEAU") == "1" else 0)


# ---------------------------------------------------------------- chiffres lus sur le site
def chiffres(g, lieux):
    d = objet_js(lire(f"{SITE}/donnees/annonces/{g}.js"))
    A, maj = d.get("a") or [], d.get("maj") or ""
    nom_lieu = lambda a: (lieux["l"].get(f"{g}/{a.get('l')}") or lieux["g"][g])
    m2 = [a["p"] / a["s"] for a in A if a.get("t") == "v" and a.get("y") == "appartement" and a.get("p") and (a.get("s") or 0) >= 30
          and 300 <= a["p"] / a["s"] <= 15000]
    s2 = [a["p"] for a in A if a.get("t") == "l" and a.get("y") == "appartement" and a.get("c") == 2 and a.get("p") and 200 <= a["p"] <= 10000]
    recent = (dt.date.fromisoformat(maj) - dt.timedelta(days=10)).isoformat() if maj else ""
    # « peut-être une bonne affaire » d'après l'avis de l'IA (ix = [sorte, écart %]) ; écarts trop grands = sans doute une erreur d'annonce
    bonnes = [a for a in A if (a.get("ix") or [""])[0] == "b" and a.get("y") in ("appartement", "maison") and a.get("p") and 10 <= a["ix"][1] <= 30 and (a.get("d") or "") >= recent]
    # d'abord les biens décrits (surface connue), appartements et maisons avant les terrains, puis les plus récents
    bonnes.sort(key=lambda a: (a.get("s") is None, a.get("y") not in ("appartement", "maison"), a.get("d") or ""), reverse=False)
    bonnes.sort(key=lambda a: a.get("d") or "", reverse=True)
    bonnes.sort(key=lambda a: (a.get("s") is None, a.get("y") not in ("appartement", "maison")))
    choix, vus = [], set()
    for a in bonnes:                     # deux biens différents (vente et location si possible, lieux différents)
        cle = (a.get("t"), a.get("l"))
        if cle in vus:
            continue
        vus.add(cle); choix.append(a)
        if len(choix) == 2:
            break
    par_q = {}
    for a in A:
        if a.get("t") == "v" and a.get("y") == "appartement" and a.get("p") and (a.get("s") or 0) >= 30 and 300 <= a["p"] / a["s"] <= 15000 \
                and a.get("l") and f"{g}/{a['l']}" in lieux.get("pq", {}):
            par_q.setdefault(a["l"], []).append(a["p"] / a["s"])
    quartiers = sorted(({"l": l, "nom": lieux["l"].get(f"{g}/{l}") or [l, ""], "pos": lieux["pq"][f"{g}/{l}"],
                         "m2": statistics.median(v), "n": len(v)} for l, v in par_q.items() if len(v) >= 4), key=lambda q: -q["m2"])
    nv = sum(1 for a in A if a.get("t") == "v")
    return {"total": len(A), "nouvelles": sum(1 for a in A if a.get("d") == maj), "maj": maj, "quartiers": quartiers,
            "vente": nv, "location": len(A) - nv,
            "m2": statistics.median(m2) if len(m2) >= 5 else None, "n_m2": len(m2),
            "s2": statistics.median(s2) if len(s2) >= 5 else None, "n_s2": len(s2),
            "annonces": [dict(a, lieu=nom_lieu(a)) for a in choix]}


# ---------------------------------------------------------------- images (HTML -> Chrome)
def css(pal, police, mise):
    f1, f2, acc, txt, carte = pal
    lat, ar = police
    fonds = {
        "degrade": f"linear-gradient(160deg,{f1},{f2})",
        "bandeau": f"linear-gradient(180deg,{f2} 0 26%,{f1} 26% 100%)",
        "cadre": f"{f1}",
        "diagonale": f"linear-gradient(120deg,{f1} 0 58%,{f2} 58% 100%)",
        "cercle": f"radial-gradient(circle at 80% 12%,{f2} 0 22%,transparent 22.2%),radial-gradient(circle at 10% 95%,{f2} 0 18%,transparent 18.2%),{f1}",
        "colonne": f"linear-gradient(90deg,{acc} 0 2.4%,{f1} 2.4% 100%)",
        "grille": f"repeating-linear-gradient(0deg,transparent 0 119px,{carte} 119px 120px),repeating-linear-gradient(90deg,transparent 0 119px,{carte} 119px 120px),linear-gradient(180deg,{f1},{f2})",
    }
    cadre = f"outline:6px solid {acc};outline-offset:-46px;" if mise == "cadre" else ""
    aligne = "left" if mise in ("colonne", "diagonale") else "center"
    return f"""@import url('https://fonts.googleapis.com/css2?family={lat.replace(' ', '+')}:wght@400;700;900&family={ar.replace(' ', '+')}:wght@400;700&display=block');
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{background:{fonds[mise]};color:{txt};font-family:'{lat}',sans-serif;{cadre}display:flex;flex-direction:column;justify-content:center;
  padding:230px 90px 330px;text-align:{aligne};gap:44px}}
.ar{{font-family:'{ar}',sans-serif;direction:rtl}}
.petit{{font-size:40px;opacity:.82;letter-spacing:.04em;text-transform:uppercase;font-weight:700}}
.gros{{font-size:118px;line-height:1.02;font-weight:900}}
.moyen{{font-size:66px;line-height:1.12;font-weight:700}}
.ar.moyen,.ar.gros{{line-height:1.45}}
.acc{{color:{acc}}}
.chiffre{{font-size:190px;font-weight:900;color:{acc};line-height:1}}
.carte{{background:{carte};border-radius:36px;padding:52px 56px;display:flex;flex-direction:column;gap:22px;
  border-{'left' if aligne == 'left' else 'top'}:12px solid {acc}}}
.ligne{{display:flex;justify-content:{'flex-start' if aligne == 'left' else 'center'};gap:28px;flex-wrap:wrap;font-size:46px;font-weight:700}}
.pastille{{display:inline-block;background:{acc};color:{f1};border-radius:999px;padding:14px 38px;font-size:44px;font-weight:900}}
.marque{{position:absolute;top:84px;left:0;right:0;text-align:center;font-size:38px;font-weight:700;opacity:.85}}
.note{{font-size:34px;opacity:.75}}
.fond{{position:absolute;inset:0;background-size:cover;background-position:center;z-index:-2}}.voile{{position:absolute;inset:0;z-index:-1}}
.flou{{position:absolute;inset:0;z-index:-1;backdrop-filter:blur(14px) brightness(.55)}}
.sur-photo{{color:#fff;text-shadow:0 2px 18px #000a;display:flex;flex-direction:column;gap:44px}}.sur-photo .acc{{color:{acc}}}
.titre-haut{{position:absolute;top:150px;left:0;right:0;text-align:center;padding:0 60px}}
.bulle{{position:absolute;transform:translate(-50%,-50%);background:{f1};color:{txt};border:5px solid {acc};border-radius:28px;
  padding:14px 22px;text-align:center;box-shadow:0 10px 30px #0006;white-space:nowrap}}.bulle b{{display:block;font-size:34px}}
.bulle span{{font-size:40px;font-weight:900;color:{acc}}}
.filigrane{{position:absolute;z-index:-1;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-12deg);font-size:300px;
  font-weight:900;color:{acc};opacity:.10;white-space:nowrap;line-height:1}}
.epingle{{position:absolute;width:64px;height:64px;transform:translate(-50%,-100%) rotate(-45deg);background:{acc};
  border:6px solid {txt};border-radius:50% 50% 50% 0;box-shadow:0 8px 24px #0008}}
.bas-carte{{position:absolute;left:60px;right:60px;bottom:280px;display:flex;flex-direction:column;gap:22px;background:{f1}f2;
  border-radius:36px;padding:40px;box-shadow:0 18px 50px #0007}}.bas-carte .carte{{background:transparent;padding:0;box-shadow:none;border:0}}
.bas-carte .chiffre{{font-size:96px!important}}.bas-carte .note{{display:none}}.bas-carte .moyen{{font-size:50px}}
.bas-carte .petit{{font-size:30px}}.haut-carte{{bottom:auto;top:150px}}.fin-carte{{bottom:auto;top:620px;text-align:center;align-items:center}}
.osm{{position:absolute;bottom:250px;left:0;right:0;text-align:center;font-size:24px;opacity:.85;text-shadow:0 1px 6px #000}}
.barre{{text-align:left;margin:6px 0}}.barre-nom{{font-size:38px;font-weight:700;margin-bottom:8px}}
.barre-piste{{background:{carte};border-radius:18px;height:78px}}
.barre-plein{{height:78px;border-radius:18px;background:{acc};color:{f1};font-size:38px;font-weight:900;display:flex;align-items:center;
  justify-content:flex-end;padding:0 22px;white-space:nowrap}}
.duel{{display:flex;flex-direction:column;gap:0;margin:0 -90px}}.duel-moitie{{padding:70px 90px;display:flex;flex-direction:column;gap:18px}}
.duel-b{{background:{acc};color:{f1}}}.duel-b .chiffre{{color:{f1}}}
.duel-vs{{align-self:center;margin:-62px 0;z-index:2;background:{txt};color:{f1};font-size:56px;font-weight:900;border-radius:50%;
  width:124px;height:124px;display:flex;align-items:center;justify-content:center}}"""


def page(corps, style):
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{style}</style></head><body>{corps}' \
           f'<div class="marque">immobilier.clicvia.com</div></body></html>'


# ---------------------------------------------------------------- formats (règle § 49, Ahmed 29/10/2026 : « le fond est le même, tu ne
# fais que changer de couleur ; les visiteurs sont intelligents ; nouveau fond et nouveau design pour donner envie ; je veux de la créativité »)
# Chaque format a SON fond et SA composition : vraie carte OpenStreetMap avec les prix des quartiers, classement en barres, duel
# acheter/louer, vraie photo de la ville (Wikimedia Commons, licence libre, crédit dans la légende), fiches d'annonces.
FORMATS = ["carte", "classement", "photo", "duel", "fiches"]
ACCROCHES_FORMAT = {
    "carte": [("{g} : le prix du m², quartier par quartier", "{g}: سعر المتر، حي بحي"), ("Où acheter à {g} ? La carte des prix", "وين تشري في {g}؟ خريطة الأسعار")],
    "classement": [("Les quartiers les plus chers de {g}", "أغلى أحياء {g}"), ("{g} : du plus cher au plus abordable", "{g}: من الأغلى إلى الأرخص")],
    "duel": [("{g} : acheter ou louer ?", "{g}: تشري ولا تكري؟"), ("Achat contre location à {g}", "الشراء أو الكراء في {g}")],
}
PHOTOS = ICI / "reels" / "photos.json"


def photos_de(g):
    try:
        return json.loads(PHOTOS.read_text(encoding="utf-8")).get(g) or []
    except (OSError, ValueError):
        return []


def formats_possibles(g, c):
    f = ["duel", "fiches"]
    if len(c["quartiers"]) >= 5:
        f += ["carte", "classement"]
    if photos_de(g):
        f.append("photo")
    return [x for x in FORMATS if x in f]


def choisir_format(n, g, c, histo):
    ok, recents = formats_possibles(g, c), [x.get("format") for x in histo[:2]]
    for k in range(len(FORMATS)):
        f = FORMATS[(n + k) % len(FORMATS)]
        if f in ok and f not in recents:
            return f
    return next(f for f in ok)


def tuile(z, x, y, cache):
    f = cache / f"{z}-{x}-{y}.png"
    if not f.exists():
        req = urllib.request.Request(f"https://tile.openstreetmap.org/{z}/{x}/{y}.png", headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            f.write_bytes(r.read())
        time.sleep(0.3)                          # politesse envers les serveurs d'OpenStreetMap (peu de tuiles, 2 vidéos par jour)
    return f


def fond_carte(points, dossier):
    """Vraie carte OpenStreetMap (© contributeurs OpenStreetMap, citée dans la vidéo et la légende) centrée sur les quartiers ;
    renvoie le fichier et la position (x, y) de chaque point sur l'image 1080 x 1920."""
    import math
    from PIL import Image
    px = lambda lat, lon, z: ((lon + 180) / 360 * 256 * 2 ** z,
                              (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 256 * 2 ** z)
    lats, lons = [p[0] for p in points], [p[1] for p in points]
    z = 15
    while z > 8:
        (x1, y1), (x2, y2) = px(max(lats), min(lons), z), px(min(lats), max(lons), z)
        if x2 - x1 <= 820 and y2 - y1 <= 1050:
            break
        z -= 1
    (x1, y1), (x2, y2) = px(max(lats), min(lons), z), px(min(lats), max(lons), z)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 + 60
    gx, gy = cx - W / 2, cy - H / 2
    cache = SORTIE / "tuiles"; cache.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (W, H), "#dddddd")
    for tx in range(int(gx // 256), int((gx + W) // 256) + 1):
        for ty in range(int(gy // 256), int((gy + H) // 256) + 1):
            img.paste(Image.open(tuile(z, tx, ty, cache)).convert("RGB"), (int(tx * 256 - gx), int(ty * 256 - gy)))
    f = dossier / "fond-carte.png"; img.save(f)
    return f, [(px(a, b, z)[0] - gx, px(a, b, z)[1] - gy) for a, b in points]


def fond_photo(g, n, dossier):
    from PIL import Image, ImageOps
    ph = photos_de(g)
    if not ph:
        return None, None
    choix = ph[n % len(ph)]
    brut = dossier / "photo-brute.jpg"
    req = urllib.request.Request(choix["url"], headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        brut.write_bytes(r.read())
    f = dossier / "fond-photo.jpg"
    ImageOps.fit(Image.open(brut).convert("RGB"), (W, H), centering=(0.5, 0.45)).save(f, quality=90)
    return f, choix


def scenes(g, lieux, c, n, fmt="fiches", dossier=None, pal=None):
    """Scènes du format choisi. Les fonds (carte, photo) sont des fichiers posés dans le dossier de la vidéo."""
    nfr, nar = lieux["g"][g]
    E = html.escape
    acc = ACCROCHES_FORMAT.get(fmt)
    acc_fr, acc_ar = acc[n % len(acc)] if acc else ACCROCHES[n % len(ACCROCHES)]
    fin_fr, fin_ar = FINS[n % len(FINS)]
    jour = dt.date.fromisoformat(c["maj"]).strftime("%d/%m/%Y") if c["maj"] else ""
    f1 = (pal or PALETTES[0])[0]
    fin = (3.6, f'<div class="gros">{E(fin_fr)}</div><div class="ar moyen acc">{E(fin_ar)}</div>'
                f'<div class="pastille" style="font-size:40px;padding:16px 30px">immobilier.clicvia.com/{E(g)}</div>'
                f'<div class="moyen">Lien dans la bio · <span class="ar">الرابط في البروفايل</span></div>')
    titre = (f'<div class="petit">{E(jour)}</div><div class="gros">{E(acc_fr.format(g=nfr))}</div>'
             f'<div class="ar moyen acc">{E(acc_ar.format(g=nar))}</div>')
    bonnes = [scene_annonce(a, lieux) for a in c["annonces"]]
    if fmt == "carte":
        Q = c["quartiers"]
        ann_pos = [lieux["pq"].get(f"{g}/{a.get('l')}") for a in c["annonces"]]
        fond, pos = fond_carte([q["pos"] for q in Q] + [p for p in ann_pos if p], dossier)
        pos_ann, k = [], len(Q)
        for p_ in ann_pos:
            pos_ann.append(pos[k] if p_ else None); k += 1 if p_ else 0
        pos = pos[:len(Q)]
        bulles, pris = [], []
        for q, (x, y) in sorted(zip(Q, pos), key=lambda t: -t[0]["n"]):
            if not (60 < x < W - 60 and 360 < y < H - 300) or any(abs(x - a) < 300 and abs(y - b) < 120 for a, b in pris):
                continue
            pris.append((x, y))
            bulles.append(f'<div class="bulle" style="left:{x:.0f}px;top:{y:.0f}px"><b>{E(q["nom"][0])}</b>'
                          f'<span>{milliers(q["m2"])} DT/m²</span></div>')
            if len(bulles) == 7:
                break
        decor = (f'<div class="fond" style="background-image:url(\'{fond.name}\')"></div>'
                 f'<div class="voile" style="background:linear-gradient(180deg,{f1}ee 0%,{f1}55 22%,{f1}22 50%,{f1}88 85%,{f1}ee 100%)"></div>')
        S = [(3.0, decor + titre),
             (4.2, decor + f'<div class="titre-haut"><div class="moyen">Prix du m² · سعر المتر</div><div class="petit">Appartements à vendre, prix médian'
                           f' · شقق للبيع</div></div>' + "".join(bulles) + '<div class="osm">© contributeurs OpenStreetMap</div>')]
        # annonces et fin restent SUR la carte (épingle sur le quartier de l'annonce) : toute la vidéo garde son identité
        for (d, h), pa in zip(bonnes, pos_ann):
            epingle = (f'<div class="epingle" style="left:{pa[0]:.0f}px;top:{pa[1]:.0f}px"></div>'
                       if pa and 60 < pa[0] < W - 60 and 200 < pa[1] < H - 200 else "")
            place = "bas-carte haut-carte" if pa and pa[1] > H * 0.52 else "bas-carte"   # la fiche ne cache jamais l'épingle
            S.append((d, decor + epingle + f'<div class="{place}">{h}</div>'))
        S.append((fin[0], decor + f'<div class="bas-carte fin-carte">{fin[1]}</div>'))
    elif fmt == "classement":
        Q = c["quartiers"]
        haut = max(q["m2"] for q in Q)

        def barres(lst):
            return "".join(f'<div class="barre"><div class="barre-nom">{E(q["nom"][0])} <span class="ar">{E(q["nom"][1])}</span></div>'
                           f'<div class="barre-piste"><div class="barre-plein" style="width:{max(18, q["m2"] / haut * 100):.0f}%">'
                           f'{milliers(q["m2"])} DT</div></div></div>' for q in lst)
        fil = f'<div class="filigrane ar">{E(nar)}</div>'          # grand nom arabe en fond : identité propre du classement
        S = [(3.0, fil + titre),
             (4.0, fil + f'<div class="moyen">Les plus chers · <span class="ar">الأغلى</span></div><div class="petit">Prix du m², appartements à vendre</div>'
                   + barres(Q[:5])),
             (4.0, fil + f'<div class="moyen">Les plus abordables · <span class="ar">الأرخص</span></div><div class="petit">Prix du m², appartements à vendre</div>'
                   + barres(Q[-5:][::-1]) + f'<div class="note">D\'après {milliers(sum(q["n"] for q in Q))} annonces · حسب إعلانات الموقع</div>'),
             fin]
    elif fmt == "duel":
        S = [(3.0, titre),
             (4.2, f'<div class="duel"><div class="duel-moitie"><div class="petit">Acheter · الشراء</div><div class="chiffre">'
                   f'{milliers(c["m2"]) + " DT" if c["m2"] else milliers(c["vente"])}</div><div class="moyen">'
                   f'{"le m² (médian)" if c["m2"] else "annonces à vendre"}</div><div class="note">{milliers(c["vente"])} annonces · إعلان</div></div>'
                   f'<div class="duel-vs">VS</div><div class="duel-moitie duel-b"><div class="petit">Louer · الكراء</div><div class="chiffre">'
                   f'{milliers(c["s2"]) + " DT" if c["s2"] else milliers(c["location"])}</div><div class="moyen">'
                   f'{"S+2 par mois (médian)" if c["s2"] else "annonces à louer"}</div><div class="note">{milliers(c["location"])} annonces · إعلان</div></div></div>')]
        S += bonnes + [fin]
    elif fmt == "photo":
        fond, credit = fond_photo(g, n, dossier)
        decor = (f'<div class="fond" style="background-image:url(\'{fond.name}\')"></div>'
                 f'<div class="voile" style="background:linear-gradient(180deg,#000a 0%,#0004 35%,#0006 65%,#000c 100%)"></div>')
        clair = '<div class="sur-photo">'
        cr = f'<div class="osm">Photo : {E(credit["auteur"])}, {E(credit["licence"])}, Wikimedia Commons</div>'
        S = [(3.2, decor + clair + titre + '</div>' + cr),
             (3.2, decor + clair + f'<div class="petit">{E(nfr)} · {E(nar)}</div><div class="chiffre">{milliers(c["total"])}</div>'
                   f'<div class="moyen">annonces à vendre et à louer</div><div class="ar moyen">إعلان بيع وكراء</div></div>' + cr)]
        S += [(d, decor + '<div class="flou"></div>' + h) for d, h in bonnes] + [(3.6, decor + clair + fin[1] + '</div>' + cr)]
        c["credit_photo"] = credit
    else:                                        # fiches (le format d'origine), ordre des scènes qui tourne
        S = scenes_fiches(g, lieux, c, n)
    return S


def scene_annonce(a, lieux):
    E = html.escape
    typ = lieux["t"].get(a.get("y"), [a.get("y", ""), ""])
    piece = f'S+{a["c"]}' if a.get("c") and a.get("y") == "appartement" else (f'{a["c"]} chambres' if a.get("c") else "")
    info = " · ".join(x for x in (piece, f'{milliers(a["s"])} m²' if a.get("s") else "") if x)
    vl = ("À vendre", "للبيع") if a.get("t") == "v" else ("À louer", "للكراء")
    prix_txt = f'{milliers(a["p"])} DT' + (" / mois" if a.get("t") == "l" else "")
    return (3.2, f'<div class="petit">Repéré par notre IA · رصده ذكاؤنا الاصطناعي</div>'
                 f'<div class="carte"><div class="moyen">{E(typ[0])} {E(vl[0].lower())} · <span class="ar">{E(typ[1])} {E(vl[1])}</span></div>'
                 f'<div class="moyen acc">{E(a["lieu"][0])}{" · <span class=ar>" + E(a["lieu"][1]) + "</span>" if a["lieu"][1] else ""}</div>'
                 f'<div class="ligne"><span>{E(info)}</span></div><div class="chiffre" style="font-size:132px">{E(prix_txt)}</div>'
                 f'<div class="pastille">≈ {a["ix"][1]} % sous les biens semblables</div></div>'
                 f'<div class="note">Peut-être une bonne affaire : vérifiez l\'état du bien · ربما صفقة جيدة، تثبّت من حالة العقار</div>')


def scenes_fiches(g, lieux, c, n):
    nfr, nar = lieux["g"][g]
    acc_fr, acc_ar = ACCROCHES[n % len(ACCROCHES)]
    fin_fr, fin_ar = FINS[n % len(FINS)]
    jour = dt.date.fromisoformat(c["maj"]).strftime("%d/%m/%Y") if c["maj"] else ""
    E = html.escape
    S = [(3.0, f'<div class="petit">{E(jour)}</div><div class="gros">{E(acc_fr.format(g=nfr))}</div>'
               f'<div class="ar moyen acc">{E(acc_ar.format(g=nar))}</div>'),
         (3.0, f'<div class="petit">{E(nfr)} · {E(nar)}</div><div class="chiffre">{milliers(c["total"])}</div>'
               f'<div class="moyen">annonces à vendre et à louer</div><div class="ar moyen">إعلان بيع وكراء</div>'
               + (f'<div class="pastille">+{milliers(c["nouvelles"])} aujourd\'hui · اليوم</div>' if c["nouvelles"] else ""))]
    prix = []
    if c["m2"]:
        prix.append(f'<div class="carte"><div class="petit">Appartement à vendre · شقة للبيع</div><div class="chiffre" style="font-size:150px">'
                    f'{milliers(c["m2"])} DT</div><div class="moyen">le m² (prix médian) · <span class="ar">للمتر المربع</span></div></div>')
    if c["s2"]:
        prix.append(f'<div class="carte"><div class="petit">Location S+2 · كراء S+2</div><div class="chiffre" style="font-size:150px">'
                    f'{milliers(c["s2"])} DT</div><div class="moyen">par mois (loyer médian) · <span class="ar">في الشهر</span></div></div>')
    if prix:
        S.append((3.2, "".join(prix) + f'<div class="note">D\'après {milliers(c["n_m2"] + c["n_s2"])} annonces du site · حسب إعلانات الموقع</div>'))
    for a in c["annonces"]:
        typ = lieux["t"].get(a.get("y"), [a.get("y", ""), ""])
        piece = f'S+{a["c"]}' if a.get("c") and a.get("y") == "appartement" else (f'{a["c"]} chambres' if a.get("c") else "")
        info = " · ".join(x for x in (piece, f'{milliers(a["s"])} m²' if a.get("s") else "") if x)
        vl = ("À vendre", "للبيع") if a.get("t") == "v" else ("À louer", "للكراء")
        prix_txt = f'{milliers(a["p"])} DT' + (" / mois" if a.get("t") == "l" else "")
        S.append((3.2, f'<div class="petit">Repéré par notre IA · رصده ذكاؤنا الاصطناعي</div>'
                       f'<div class="carte"><div class="moyen">{E(typ[0])} {E(vl[0].lower())} · <span class="ar">{E(typ[1])} {E(vl[1])}</span></div>'
                       f'<div class="moyen acc">{E(a["lieu"][0])}{" · <span class=ar>" + E(a["lieu"][1]) + "</span>" if a["lieu"][1] else ""}</div>'
                       f'<div class="ligne"><span>{E(info)}</span></div><div class="chiffre" style="font-size:132px">{E(prix_txt)}</div>'
                       f'<div class="pastille">≈ {a["ix"][1]} % sous les biens semblables</div></div>'
                       f'<div class="note">Peut-être une bonne affaire : vérifiez l\'état du bien · ربما صفقة جيدة، تثبّت من حالة العقار</div>'))
    # ordre des scènes du milieu (chiffres, prix, bonnes affaires) différent d'une vidéo à l'autre (règle § 49)
    milieu = S[1:]
    r = n % max(1, len(milieu))
    S = S[:1] + milieu[r:] + milieu[:r]
    S.append((3.6, f'<div class="gros">{E(fin_fr)}</div><div class="ar moyen acc">{E(fin_ar)}</div>'
                   f'<div class="pastille" style="font-size:40px;padding:16px 30px">immobilier.clicvia.com/{E(g)}</div>'
                   f'<div class="moyen">Lien dans la bio · <span class="ar">الرابط في البروفايل</span></div>'))
    return S


def navigateur():
    for c in (os.environ.get("NAVIGATEUR"), shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chrome"),
              r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if c and os.path.exists(c):
            return c
    sys.exit("ÉCHEC : Chrome introuvable (variable NAVIGATEUR)")


def photographier(fichiers):
    nav, images = navigateur(), []
    for f in fichiers:
        png = f.with_suffix(".png")
        subprocess.run([nav, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-sandbox", "--force-device-scale-factor=1",
                        f"--window-size={W},{H}", "--virtual-time-budget=8000", f"--screenshot={png}", f.as_uri()],
                       capture_output=True, timeout=120)
        if not png.exists() or png.stat().st_size < 10000:
            sys.exit(f"ÉCHEC : image non fabriquée ({f.name})")
        images.append(png)
    return images


# ---------------------------------------------------------------- vidéo (ffmpeg)
def monter(images, durees, n, sortie):
    ff = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
    entrees, filtres = [], []
    zoom_avant = n % 2 == 0
    for i, (img, d) in enumerate(zip(images, durees)):
        entrees += ["-loop", "1", "-t", f"{d:.2f}", "-i", str(img)]
        z = f"(1+0.045*t/{d:.2f})" if zoom_avant else f"(1.045-0.045*t/{d:.2f})"
        filtres.append(f"[{i}:v]fps={FPS},scale=w='trunc({W}*{z}/2)*2':h=-2:eval=frame,crop={W}:{H},setsar=1,format=yuv420p[v{i}]")
    t1, t2 = TRANSITIONS[n % len(TRANSITIONS)], TRANSITIONS[(n + 4) % len(TRANSITIONS)]
    courant, decalage = "v0", 0.0
    for i in range(1, len(images)):
        decalage += durees[i - 1] - FONDU
        sortie_i = f"x{i}"
        filtres.append(f"[{courant}][v{i}]xfade=transition={t1 if i % 2 else t2}:duration={FONDU}:offset={decalage:.2f}[{sortie_i}]")
        courant = sortie_i
    total = sum(durees) - FONDU * (len(images) - 1)
    musique = ICI / "reels" / "musique.m4a"
    filtres.append(f"[{len(images)}:a]atrim=0:{total:.2f},afade=t=in:d=1,afade=t=out:st={total - 1.5:.2f}:d=1.5,volume=0.7[a]")
    cmd = [ff, "-y", "-loglevel", "error", *entrees, "-i", str(musique), "-filter_complex", ";".join(filtres),
           "-map", f"[{courant}]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
           "-r", str(FPS), "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "-t", f"{total:.2f}", str(sortie)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode or not sortie.exists():
        sys.exit("ÉCHEC : ffmpeg — " + (r.stderr or "")[-600:])
    return total


def legende(g, lieux, c, n):
    nfr, nar = lieux["g"][g]
    acc_fr, acc_ar = ACCROCHES[n % len(ACCROCHES)]
    l = [f"🏠 {acc_fr.format(g=nfr)}", f"{milliers(c['total'])} annonces de vente et de location à {nfr}, avec l'avis de notre IA sur chaque bien."]
    if c["m2"]:
        l.append(f"• Appartement à vendre : ≈ {milliers(c['m2'])} DT le m² (prix médian)")
    if c["s2"]:
        l.append(f"• Location S+2 : ≈ {milliers(c['s2'])} DT par mois (loyer médian)")
    l += ["", f"🏠 {acc_ar.format(g=nar)}", f"{milliers(c['total'])} إعلان بيع وكراء في {nar}، مع رأي الذكاء الاصطناعي في كل عقار.", "",
          f"👉 Lien dans la bio : immobilier.clicvia.com → touchez « {nfr} » · الرابط في البروفايل ← اختر {nar}", "",
          f"#Immobilier #Tunisie #{re.sub(r'[^A-Za-z]', '', nfr)} #عقارات #عقارات_{nar.replace(' ', '_')} #تونس #appartement #location",
          f"📍 {g} {c['maj']}"]          # repère : jamais deux fois la même vidéo le même jour
    return "\n".join(l)


# ---------------------------------------------------------------- page de liens de la bio (règle § 48)
RACINE = ICI.parent
HISTO = RACINE / "donnees" / "reels.json"


def lire_histo():
    try:
        return json.loads(HISTO.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []


def ecrire_histo(h):
    HISTO.parent.mkdir(exist_ok=True)
    HISTO.write_text(json.dumps(h[:60], ensure_ascii=False, indent=0) + "\n", encoding="utf-8", newline="\n")


def page_liens(lieux):
    """clicvia.com/instagram/ : le lien de la bio. Vidéos récentes en haut (gros boutons), puis les 24 gouvernorats."""
    E = html.escape
    rec, vus = [], set()
    for x in lire_histo():
        if x["g"] not in vus:
            vus.add(x["g"]); rec.append(x)
        if len(rec) == 4:
            break

    def bouton(g, gros):
        return (f'<a class="{"gros" if gros else "g"}" href="{SITE}/{g}/"><span>{E(lieux["g"][g][0])}</span>'
                f'<span class="ar">{E(lieux["g"][g][1])}</span></a>')
    haut = "".join(f'<div class="video"><p class="date">Vidéo du {dt.date.fromisoformat(x["date"]).strftime("%d/%m")} · فيديو</p>'
                   f'{bouton(x["g"], True)}</div>' for x in rec)
    tous = "".join(bouton(g, False) for g in sorted(lieux["g"], key=lambda g: lieux["g"][g][0]))
    corps = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>immobilier.clicvia.com — liens des vidéos</title><meta name="robots" content="noindex,follow">
<meta name="description" content="Les annonces immobilières de chaque gouvernorat de Tunisie, gratuites : liens des vidéos Instagram de Clicvia Immobilier.">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Instrument+Sans:wght@400;600;700&family=IBM+Plex+Sans+Arabic:wght@400;600&display=swap" rel="stylesheet">
<style>/* mêmes couleurs et polices que immobilier.clicvia.com (assets/style.css du site, 29/10/2026, demande d'Ahmed) */
:root{{--terre:#B4532F;--terre-f:#8E3B1F;--sable:#F7F2EA;--carte:#FFFFFF;--encre:#1E2A30;--doux:#5F6B70;--ligne:#E5DACB;--or:#F2B33D;
--ombre:0 1px 2px rgba(30,42,48,.05),0 6px 18px -10px rgba(30,42,48,.18)}}
*{{box-sizing:border-box;margin:0}}body{{font-family:"Instrument Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--sable);
color:var(--encre);padding:22px 16px 40px;max-width:560px;margin:0 auto}}
h1{{font-family:"Fraunces",Georgia,serif;font-weight:600;font-size:26px;text-align:center;letter-spacing:-.01em}}h1 a{{color:var(--terre)}}
.sous{{text-align:center;color:var(--doux);margin:6px 0 20px}}.ar{{direction:rtl;font-family:"IBM Plex Sans Arabic","Noto Sans Arabic",Tahoma,sans-serif}}
a{{text-decoration:none}}.video{{margin-bottom:14px}}.date{{font-size:13px;color:var(--doux);margin:0 0 6px 4px}}
.gros{{display:flex;justify-content:space-between;align-items:center;gap:12px;background:var(--terre);color:#fff;border-radius:18px;padding:20px 22px;
font-size:22px;font-weight:700;box-shadow:var(--ombre)}}.gros:active{{background:var(--terre-f)}}
h2{{font-family:"Fraunces",Georgia,serif;font-weight:600;font-size:18px;margin:26px 0 10px}}.grille{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.g{{display:flex;flex-direction:column;background:var(--carte);border:1px solid var(--ligne);border-radius:12px;padding:12px;color:var(--encre);
font-weight:600;box-shadow:var(--ombre)}}.g .ar{{font-weight:400;color:var(--doux)}}.pied{{text-align:center;margin-top:26px;font-size:14px}}
.pied a{{color:var(--terre)}}</style>
<script data-goatcounter="https://prix-eaux-tunisie.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script></head><body>
<h1><a href="{SITE}/">immobilier.clicvia.com</a></h1><p class="sous">Touchez le gouvernorat de la vidéo · <span class="ar">اختر ولاية الفيديو</span></p>
{haut or bouton("tunis", True)}
<h2>Tous les gouvernorats · <span class="ar">كل الولايات</span></h2><div class="grille">{tous}</div>
<p class="pied"><a href="{SITE}/alertes/">Alertes gratuites · تنبيهات مجانية</a> · <a href="https://clicvia.com/">clicvia.com</a></p>
</body></html>
"""
    (RACINE / "instagram").mkdir(exist_ok=True)
    (RACINE / "instagram" / "index.html").write_text(corps, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- publication (API Instagram)
def api(methode, chemin, jeton, donnees=None, url=None):
    u = url or f"{GRAPH}/{chemin}"
    if methode == "GET":
        u += ("&" if "?" in u else "?") + "access_token=" + urllib.parse.quote(jeton)
        req = urllib.request.Request(u)
    else:
        req = urllib.request.Request(u, data=urllib.parse.urlencode(dict(donnees or {}, access_token=jeton)).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:          # le jeton n'est jamais affiché, seulement le message d'Instagram / Facebook
        try:
            err = json.loads(e.read()).get("error", {})
        except Exception:
            err = {}
        sys.exit(f"ÉCHEC : refus de l'API ({chemin.split('?')[0].split('/')[-1] or 'envoi'}) — {err.get('message', e.code)} (code {err.get('code', e.code)})")


def publier(video, texte, repere):
    page, jeton = os.environ.get("FB_PAGE_ID"), os.environ.get("FB_PAGE_TOKEN")
    if not page or not jeton:
        sys.exit("ÉCHEC : secrets FB_PAGE_ID / FB_PAGE_TOKEN absents du dépôt : rien n'est publié.")
    ig = os.environ.get("IG_USER_ID") or (api("GET", f"{page}?fields=instagram_business_account", jeton).get("instagram_business_account") or {}).get("id")
    if not ig:
        sys.exit("ÉCHEC : aucun compte Instagram professionnel relié à la page Facebook Clicvia (voir GERER SANS CLAUDE).")
    recents = api("GET", f"{ig}/media?fields=caption&limit=12", jeton).get("data") or []
    if any(repere in (m.get("caption") or "") for m in recents):
        print("déjà publiée sur Instagram (relance tardive de GitHub) : rien à faire"); return None
    cont = api("POST", f"{ig}/media", jeton, {"media_type": "REELS", "upload_type": "resumable", "caption": texte, "share_to_feed": "true"})
    taille = video.stat().st_size
    req = urllib.request.Request(cont["uri"], data=video.read_bytes(), method="POST",
                                 headers={"Authorization": "OAuth " + jeton, "offset": "0", "file_size": str(taille)})
    try:
        urllib.request.urlopen(req, timeout=300).read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ÉCHEC : envoi de la vidéo refusé ({e.code})")
    for _ in range(40):                          # Instagram prépare la vidéo (souvent 30 s à 2 min)
        etat = api("GET", f"{cont['id']}?fields=status_code,status", jeton)
        if etat.get("status_code") == "FINISHED":
            break
        if etat.get("status_code") in ("ERROR", "EXPIRED"):
            sys.exit("ÉCHEC : Instagram a refusé la vidéo — " + str(etat.get("status")))
        time.sleep(10)
    else:
        sys.exit("ÉCHEC : vidéo toujours en préparation chez Instagram après 7 minutes")
    pub = api("POST", f"{ig}/media_publish", jeton, {"creation_id": cont["id"]})
    lien = api("GET", f"{pub['id']}?fields=permalink", jeton).get("permalink", pub["id"])
    print("Publié : " + lien)
    return lien


def publier_facebook(video, texte):
    """Même vidéo en Reel sur la page Facebook Clicvia : là, le lien du texte est cliquable (règle § 48)."""
    page, jeton = os.environ.get("FB_PAGE_ID"), os.environ.get("FB_PAGE_TOKEN")
    debut = api("POST", f"{page}/video_reels", jeton, {"upload_phase": "start"})
    req = urllib.request.Request(debut["upload_url"], data=video.read_bytes(), method="POST",
                                 headers={"Authorization": "OAuth " + jeton, "offset": "0", "file_size": str(video.stat().st_size)})
    try:
        urllib.request.urlopen(req, timeout=300).read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ÉCHEC : envoi de la vidéo à Facebook refusé ({e.code})")
    fin = api("POST", f"{page}/video_reels", jeton, {"upload_phase": "finish", "video_id": debut["video_id"],
                                                    "video_state": "PUBLISHED", "description": texte})
    if not fin.get("success"):
        sys.exit("ÉCHEC : Facebook n'a pas publié le Reel — " + json.dumps(fin)[:200])
    lien = f"https://www.facebook.com/reel/{debut['video_id']}"
    print("Publié sur Facebook : " + lien)
    return lien


def verifier_jeton():
    """29/10/2026 : le jeton collé le 28/10 n'était valable qu'UNE HEURE (étape « Étendre » manquée) : les robots Facebook et
    Instagram sont tombés en panne le soir même. Ce contrôle (VERIFIER=1, et avant chaque vidéo) lit la durée du jeton sans rien
    publier : un jeton de page durable n'expire jamais (expires_at = 0) ; sinon le robot s'arrête en rouge avec la date d'expiration."""
    page, jeton = os.environ.get("FB_PAGE_ID"), os.environ.get("FB_PAGE_TOKEN")
    if not page or not jeton:
        sys.exit("ÉCHEC : secrets FB_PAGE_ID / FB_PAGE_TOKEN absents du dépôt.")
    d = api("GET", "debug_token?input_token=" + urllib.parse.quote(jeton), jeton).get("data") or {}
    fin, valide, droits = d.get("expires_at"), d.get("is_valid"), d.get("scopes") or []
    ig = (api("GET", f"{page}?fields=name,instagram_business_account{{username}}", jeton) if valide else {})
    print(f"jeton : {'valide' if valide else 'NON VALIDE'} ; type {d.get('type')} ; "
          f"expiration : {'jamais' if fin == 0 else dt.datetime.fromtimestamp(fin, dt.timezone.utc).strftime('%d/%m/%Y %H:%M UTC') if fin else '?'} ; "
          f"page : {ig.get('name', '?')} ; Instagram : @{(ig.get('instagram_business_account') or {}).get('username', '?')}")
    manque = [x for x in ("pages_manage_posts", "instagram_basic", "instagram_content_publish") if x not in droits]
    if not valide or fin not in (0, None) or manque:
        sys.exit("ÉCHEC : jeton à refaire (GERER SANS CLAUDE/portail et facebook.md : jeton DURABLE, « Étendre le token d'accès »)"
                 + (f" ; autorisations manquantes : {', '.join(manque)}" if manque else "") + (" ; il EXPIRE" if fin else ""))


def style_libre(n, histo):
    """RÈGLE GÉNÉRALE § 49 (Ahmed, 29/10/2026 : « la vidéo doit changer de couleur et de design, sinon le visiteur dira : c'est la
    même que l'autre ») : le numéro de style n donne couleurs, mise en page, polices, accroche, transitions et ORDRE des scènes ; il est
    gardé dans donnees/reels.json et décalé tant que les couleurs ou la mise en page ressemblent à l'une des 4 dernières vidéos, ou que
    l'accroche a servi dans les 10 dernières. (Le 28/10, une vidéo lancée hors horaire aurait fait reprendre le soir le design de la veille.)"""
    recents = [x["style"] for x in histo if "style" in x]
    for k in range(200):
        m = n + k
        if all(m % len(PALETTES) != r % len(PALETTES) and m % len(MISES_EN_PAGE) != r % len(MISES_EN_PAGE) for r in recents[:4])                 and all(m % len(ACCROCHES) != r % len(ACCROCHES) for r in recents[:10]):
            return m
    return n


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if os.environ.get("VERIFIER") == "1":
        verifier_jeton(); return
    n = creneau()
    histo = lire_histo()
    g = os.environ.get("GOUV") or ORDRE[n % len(ORDRE)]
    if not os.environ.get("GOUV"):                 # jamais un gouvernorat vu dans les 11 dernières vidéos (tour de 12 jours)
        vus = [x["g"] for x in histo[:11]]
        k = 0
        while ORDRE[(n + k) % len(ORDRE)] in vus and k < len(ORDRE):
            k += 1
        g = ORDRE[(n + k) % len(ORDRE)]
    n = style_libre(n, histo)
    lieux = objet_js(lire(f"{SITE}/donnees/lieux.js"))
    if g not in lieux["g"]:
        sys.exit("gouvernorat inconnu : " + g)
    c = chiffres(g, lieux)
    if c["total"] < 5:
        print(f"{g} : seulement {c['total']} annonces, pas de vidéo aujourd'hui"); return
    pal, pol, mise = PALETTES[n % len(PALETTES)], POLICES[n % len(POLICES)], MISES_EN_PAGE[n % len(MISES_EN_PAGE)]
    print(f"créneau {n} — {g} — {c['total']} annonces (+{c['nouvelles']}), m² {c['m2']}, S+2 {c['s2']}, {len(c['annonces'])} bonne(s) affaire(s)"
          f" — couleurs {n % len(PALETTES)}, police {pol[0]}/{pol[1]}, mise en page {mise}")
    dossier = SORTIE / f"{c['maj']}-{g}"
    if dossier.exists():
        shutil.rmtree(dossier)
    dossier.mkdir(parents=True)
    fmt = os.environ.get("FORMAT") or choisir_format(n, g, c, histo)
    print(f"format : {fmt}")
    style, S = css(pal, pol, mise), scenes(g, lieux, c, n, fmt, dossier, pal)
    fichiers = []
    for i, (_, corps) in enumerate(S):
        f = dossier / f"scene{i}.html"
        f.write_text(page(corps, style), encoding="utf-8", newline="\n")
        fichiers.append(f)
    images = photographier(fichiers)
    video = dossier / f"reel-{g}.mp4"
    duree = monter(images, [d for d, _ in S], n, video)
    texte = legende(g, lieux, c, n)
    if c.get("credit_photo"):                    # licence libre : crédit obligatoire
        cp = c["credit_photo"]
        texte = texte.replace("\n#Immobilier", f"\n📷 Photo : {cp['auteur']}, {cp['licence']}, Wikimedia Commons ({cp['page']})\n\n#Immobilier", 1)
    if fmt == "carte":
        texte = texte.replace("\n#Immobilier", "\n🗺️ Carte : © contributeurs OpenStreetMap\n\n#Immobilier", 1)
    (dossier / "legende.txt").write_text(texte, encoding="utf-8", newline="\n")
    print(f"vidéo : {video} ({duree:.1f} s, {video.stat().st_size // 1024} Ko)\n---\n{texte}\n---")
    nfr, nar = lieux["g"][g]
    texte_fb = texte.replace(f"👉 Lien dans la bio : immobilier.clicvia.com → touchez « {nfr} » · الرابط في البروفايل ← اختر {nar}",
                             f"👉 Les annonces de {nfr} · إعلانات {nar} : {SITE}/{g}/")
    if os.environ.get("ESSAI") == "1":
        page_liens(lieux)
        print("ESSAI : rien n'est publié (page des liens refaite sur place, non envoyée).\n--- texte Facebook ---\n" + texte_fb)
        return
    verifier_jeton()
    lien_ig = publier(video, texte, f"📍 {g} {c['maj']}")
    if lien_ig is None:                          # déjà publiée (relance tardive) : rien d'autre à faire
        return
    h = lire_histo()
    h.insert(0, {"g": g, "date": c["maj"], "ig": lien_ig, "fb": "", "style": n, "format": fmt})
    ecrire_histo(h)
    page_liens(lieux)                            # le lien de la bio montre tout de suite le gouvernorat de cette vidéo
    h[0]["fb"] = publier_facebook(video, texte_fb)
    ecrire_histo(h)


if __name__ == "__main__":
    main()
