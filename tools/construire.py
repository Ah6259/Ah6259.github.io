# -*- coding: utf-8 -*-
"""Fabrique le portail clicvia.com en TROIS langues, une adresse par langue (demande d'Ahmed, 13/10/2026) :
     index.html (français)   ar/index.html (arabe)   en/index.html (anglais)
à partir de tools/gabarit.html (l'en-tête technique et le style) et des listes ci-dessous (THEMES, SITES, TEXTES).
Usage :  python tools/construire.py        puis  node tools/test_video.mjs  et  node tools/test_portail.mjs
Ajouter un site : une ligne dans SITES (nom et description dans les 3 langues), son icône dans assets/sites/, relancer.
NE PAS modifier index.html, ar/ ni en/ à la main : ils sont réécrits ici."""
import datetime, html, io, json, os, re

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
BASE = "https://clicvia.com/"
LANGUES = ["fr", "ar", "en"]
E = lambda s: html.escape(s, quote=True)
RTL, COURANT = ' dir="rtl"', ' aria-current="true"'  # hors des f-strings : Python 3.11 refuse « \\ » dedans

TEXTES = {
    "titre": {"fr": "Clicvia — sites pratiques pour la Tunisie : immobilier, prix de l'eau, code de la route, appels d'offres, documents",
              "ar": "Clicvia — مواقع عملية لتونس: عقارات، أسعار الماء، مجلة الطرقات، طلبات العروض، وثائق",
              "en": "Clicvia — practical websites for Tunisia: property, water prices, highway code, tenders, documents"},
    "description": {
        "fr": "Clicvia : des services gratuits pour la Tunisie, en français et en arabe : annonces immobilières dans les 24 gouvernorats, prix de l'eau minérale comparés chaque jour, calculateurs (salaire, impôt, crédit), appels d'offres et concours publics, code de la route, documents prêts à remplir, annuaires de professionnels.",
        "ar": "Clicvia: خدمات مجانية لتونس، بالعربية والفرنسية: إعلانات عقارية في الولايات الـ24، مقارنة يومية لأسعار المياه المعدنية، حاسبات (الأجر، الضريبة، القرض)، طلبات العروض والمناظرات العمومية، مجلة الطرقات، وثائق جاهزة للتعمير، ودلائل المهنيين.",
        "en": "Clicvia: free services for Tunisia: property listings in all 24 governorates, mineral water prices compared every day, calculators (salary, income tax, loan), public tenders and civil-service competitions, the highway code, ready-to-fill documents and directories of professionals."},
    "og_titre": {"fr": "Clicvia : 18 services gratuits pour la Tunisie", "ar": "Clicvia: 18 خدمة مجانية لتونس", "en": "Clicvia: 18 free services for Tunisia"},
    "og_description": {
        "fr": "Annonces immobilières (logements, bureaux, usines, terrains) dans les 24 gouvernorats, prix de l'eau minérale, calculateurs (salaire, impôt, crédit), appels d'offres et concours publics, code de la route, documents prêts à remplir — en français et en arabe.",
        "ar": "إعلانات عقارية (مساكن، مكاتب، مصانع، أراضٍ) في الولايات الـ24، أسعار المياه المعدنية، حاسبات (الأجر، الضريبة، القرض)، طلبات العروض والمناظرات العمومية، مجلة الطرقات، وثائق جاهزة للتعمير — بالعربية والفرنسية.",
        "en": "Property listings (homes, offices, factories, land) in all 24 governorates, mineral water prices, calculators (salary, tax, loan), public tenders and competitions, the highway code, ready-to-fill documents — most sites in French and Arabic."},
    "h1": {"fr": "Des services gratuits pour la Tunisie", "ar": "خدمات مجانية لتونس", "en": "Free services for Tunisia"},
    "intro": {"fr": "Comparer, calculer, trouver, remplir : des outils simples, en français et en arabe, mis à jour automatiquement.",
              "ar": "قارن، احسب، ابحث، عمِّر: أدوات بسيطة، بالعربية والفرنسية، تُحيَّن آليًا.",
              "en": "Compare, calculate, find, fill in: simple tools, updated automatically. Most sites are in French and Arabic; the language of each one is shown on its card."},
    "partager": {"fr": "Partager", "ar": "شارك", "en": "Share"},
    "partager_aria": {"fr": "Partager ces sites", "ar": "شارك هذه المواقع", "en": "Share these websites"},
    "facebook": {"fr": "Suivez Clicvia sur Facebook", "ar": "تابعوا Clicvia على فيسبوك", "en": "Follow Clicvia on Facebook"},
    "pied": {"fr": "Sites indépendants, non officiels. Statistiques de visite anonymes, sans cookies. © 2026 — tous droits réservés.",
             "ar": "مواقع مستقلة، غير رسمية. إحصائيات زيارة مجهولة الهوية، دون ملفات تعريف الارتباط. © 2026 — جميع الحقوق محفوظة.",
             "en": "Independent, unofficial websites. Anonymous visit statistics, no cookies. © 2026 — all rights reserved."},
    "langue_aria": {"fr": "Langue", "ar": "اللغة", "en": "Language"},
    "a_propos": {"fr": "Comment fonctionne le site ?", "ar": "كيف يعمل الموقع؟", "en": "How does the site work?"},
    "tous": {"fr": "Tous nos services", "ar": "كل خدماتنا", "en": "All our services"},
    "liste": {"fr": "Services Clicvia", "ar": "خدمات Clicvia", "en": "Clicvia services"},
    "autre_nom": {"fr": "Clicvia — services pratiques pour la Tunisie", "ar": "Clicvia — خدمات عملية لتونس", "en": "Clicvia — practical services for Tunisia"},
}
NOM_LANGUE = [("fr", "Français", "fr"), ("ar", "العربية", "ar"), ("en", "English", "en")]
LOCALE = {"fr": "fr_FR", "ar": "ar_AR", "en": "en_US"}

THEMES = {
    "voiture": {"fr": "Permis et voiture", "ar": "الرخصة والسيارة", "en": "Driving licence and car"},
    "papiers": {"fr": "Papiers, démarches et justice", "ar": "الوثائق والإجراءات والعدالة", "en": "Paperwork, procedures and law"},
    "travail": {"fr": "Travail, argent et entreprises", "ar": "الشغل والمال والمؤسسات", "en": "Work, money and business"},
    "maison": {"fr": "Maison, famille et artisans", "ar": "المنزل والعائلة والحرفيون", "en": "Home, family and tradespeople"},
    "religion": {"fr": "Religion et patrimoine", "ar": "الدين والتراث", "en": "Religion and heritage"},
    "recherche": {"fr": "Enseignants et chercheurs", "ar": "الأساتذة والباحثون", "en": "Teachers and researchers"},
}
# « ar » / « en » : adresse du site dans cette langue. "?" = même adresse + ?lang=xx ; "dossier" = sous-dossier xx/ ; absent = le site
# n'a pas cette langue (on ouvre alors son accueil, et la carte indique ses langues).
FR_AR = {"ar": "?"}
SITES = [
    ("voiture", "code", "code-route-tunisie", FR_AR,
     {"fr": "Code de la route Tunisie", "ar": "مجلة الطرقات تونس", "en": "Tunisia Highway Code"},
     {"fr": "Leçons, panneaux, entraînement, examen blanc et amendes.", "ar": "دروس، علامات، تمارين، امتحان تجريبي وخطايا.",
      "en": "Lessons, road signs, practice, mock exam and fines."}),
    ("voiture", "auto-ecoles", "auto-ecoles-tunisie", FR_AR,
     {"fr": "Auto-écoles Tunisie", "ar": "مدارس تعليم السياقة تونس", "en": "Driving schools Tunisia"},
     {"fr": "Trouver une auto-école près de chez vous, dans les 24 gouvernorats.", "ar": "اعثر على مدرسة تعليم سياقة قريبة منك، في الولايات الـ24.",
      "en": "Find a driving school near you, in all 24 governorates."}),
    ("voiture", "voiture", "ma-voiture-tunisie", FR_AR,
     {"fr": "Ma voiture Tunisie", "ar": "مواعيد سيارتك", "en": "My car Tunisia"},
     {"fr": "Vignette, visite technique, assurance, vidange : vos échéances et des rappels dans l'agenda. Prix des carburants.",
      "ar": "معلوم الجولان، الفحص الفني، التأمين، تغيير الزيت: مواعيدك وتذكيرات في الرزنامة. أسعار المحروقات.",
      "en": "Road tax, roadworthiness test, insurance, oil change: your deadlines with calendar reminders. Fuel prices."}),
    ("papiers", "documents", "documents-tunisie", FR_AR,
     {"fr": "Documents Tunisie", "ar": "وثائق تونس", "en": "Documents Tunisia"},
     {"fr": "Modèles prêts à remplir en PDF (français et arabe) et les étapes expliquées.", "ar": "نماذج جاهزة للتعمير بصيغة PDF (بالعربية والفرنسية) مع شرح المراحل.",
      "en": "Ready-to-fill PDF templates (French and Arabic) with the steps explained."}),
    ("papiers", "avocats", "avocats-notaires-tunisie", FR_AR,
     {"fr": "Avocats et notaires Tunisie", "ar": "محامون وعدول إشهاد تونس", "en": "Lawyers and notaries Tunisia"},
     {"fr": "Avocats, notaires, huissiers et traducteurs, par gouvernorat.", "ar": "محامون، عدول إشهاد، عدول منفذون ومترجمون، حسب الولاية.",
      "en": "Lawyers, notaries, bailiffs and translators, by governorate."}),
    ("travail", "outils", "outils-pratiques-tunisie", FR_AR,
     {"fr": "Outils pratiques Tunisie", "ar": "أدوات عملية تونس", "en": "Practical tools Tunisia"},
     {"fr": "Salaire net, impôt sur le revenu, crédit, auto-entrepreneur, retenue à la source.", "ar": "الأجر الصافي، الضريبة على الدخل، القرض، المبادر الذاتي، الخصم من المورد.",
      "en": "Net salary, income tax, loan, self-employed status, withholding tax."}),
    ("travail", "comptables", "comptables-tunisie", FR_AR,
     {"fr": "Comptables Tunisie", "ar": "محاسبون تونس", "en": "Accountants Tunisia"},
     {"fr": "Comptables, experts-comptables et conseillers fiscaux, par gouvernorat.", "ar": "محاسبون، خبراء محاسبون ومستشارون جبائيون، حسب الولاية.",
      "en": "Accountants, chartered accountants and tax advisers, by governorate."}),
    ("travail", "appels-offres", "appels-offres-tunisie", FR_AR,
     {"fr": "Appels d'offres Tunisie", "ar": "طلبات العروض تونس", "en": "Public tenders Tunisia"},
     {"fr": "Les appels d'offres publics du jour, par métier et par gouvernorat, et les ventes aux enchères.", "ar": "طلبات العروض العمومية لليوم، حسب المهنة والولاية، والبيوعات بالمزاد.",
      "en": "Today's public tenders, by trade and by governorate, and auction sales."}),
    ("travail", "concours", "alerte-concours-tunisie", FR_AR,
     {"fr": "Alerte Concours Tunisie", "ar": "تنبيه المناظرات تونس", "en": "Competition Alert Tunisia"},
     {"fr": "Tous les concours publics ouverts, par gouvernorat et par métier : date limite, postes et lien officiel.", "ar": "كل المناظرات العمومية المفتوحة، حسب الولاية والمهنة: آخر أجل، الخطط والرابط الرسمي.",
      "en": "All open civil-service competitions, by governorate and by trade: deadline, posts and official link."}),
    ("maison", "immobilier", "immobilier-tunis", FR_AR,
     {"fr": "Immobilier Tunisie", "ar": "عقارات تونس", "en": "Property Tunisia"},
     {"fr": "Logements, bureaux, commerces, usines et terrains à vendre ou à louer dans les 24 gouvernorats ; déposez votre annonce gratuitement.",
      "ar": "مساكن، مكاتب، محلات، مصانع وأراضٍ للبيع أو للكراء في الولايات الـ24؛ انشر إعلانك مجانًا.",
      "en": "Homes, offices, shops, factories and land for sale or rent in all 24 governorates; post your listing for free."}),
    ("maison", "prix-eau", "prix-eaux-tunisie", FR_AR,
     {"fr": "Prix des Eaux de Tunisie", "ar": "أسعار المياه في تونس", "en": "Water prices in Tunisia"},
     {"fr": "Les prix de l'eau minérale dans les magasins, comparés chaque jour.", "ar": "أسعار المياه المعدنية في المغازات، مقارنة كل يوم.",
      "en": "Mineral water prices in the shops, compared every day."}),
    ("maison", "comptes", "mes-comptes-tunisie", FR_AR,
     {"fr": "Mes comptes", "ar": "حساباتي", "en": "My accounts"},
     {"fr": "Loyers, salaire, dépenses, impôt et rappels sur votre téléphone. Gratuit 3 mois.", "ar": "الكراءات، الأجر، المصاريف، الضريبة وتذكيرات على هاتفك. مجانًا لمدة 3 أشهر.",
      "en": "Rents, salary, expenses, tax and reminders on your phone. Free for 3 months."}),
    ("maison", "pros", "professionnels-tunisie", FR_AR,
     {"fr": "Professionnels Tunisie", "ar": "المهنيون تونس", "en": "Professionals Tunisia"},
     {"fr": "Annuaire gratuit des artisans et professionnels, gouvernorat par gouvernorat.", "ar": "دليل مجاني للحرفيين والمهنيين، ولاية بولاية.",
      "en": "Free directory of tradespeople and professionals, governorate by governorate."}),
    ("maison", "mariage", "mariage-tunisie", FR_AR,
     {"fr": "Mariage Tunisie", "ar": "الزواج تونس", "en": "Wedding Tunisia"},
     {"fr": "Salles des fêtes, photographes, traiteurs, pâtisseries, coiffure et beauté.", "ar": "قاعات أفراح، مصورون، ممونون، حلويات، حلاقة وتجميل.",
      "en": "Wedding halls, photographers, caterers, pastry shops, hair and beauty."}),
    ("religion", "mosquees", "mosquees-tunisie", {"ar": "dossier", "en": "dossier", "plus": 21},
     {"fr": "Mosquées en Tunisie", "ar": "مساجد تونس", "en": "Mosques in Tunisia"},
     {"fr": "Toutes les mosquées et salles de prière sur une carte, la plus proche de vous, et l'histoire des grandes mosquées (21 langues).",
      "ar": "كل المساجد والمصليات على خريطة، الأقرب إليك، وتاريخ المساجد الكبرى (21 لغة).",
      "en": "Every mosque and prayer room on a map, the nearest one to you, and the history of the great mosques (21 languages)."}),
    ("religion", "eau", "points-eau-tunisie", {"ar": "dossier", "en": "dossier", "plus": 21},
     {"fr": "Points d'eau Tunisie", "ar": "نقاط الماء في تونس", "en": "Water Points Tunisia"},
     {"fr": "Carte des sources, fontaines, robinets publics et majels ; trouvez le plus proche, signalez-en un.", "ar": "خريطة العيون والسبّالات والحنفيات العمومية والمواجل؛ اعثر على الأقرب، وبلّغ عن نقطة.",
      "en": "Map of springs, drinking fountains, public taps and rainwater cisterns; find the nearest one, report one."}),
    ("religion", "message", "le-message", {"en": "?", "plus": 19, "sans_ar": True},
     {"fr": "The Message — الرسالة", "ar": "The Message — الرسالة", "en": "The Message — الرسالة"},
     {"fr": "Découvrir l'Islam, le Coran et son message, en 19 langues (français, anglais, espagnol…).", "ar": "اكتشف الإسلام والقرآن ورسالته، بـ19 لغة (الفرنسية، الإنجليزية، الإسبانية…).",
      "en": "Discover Islam, the Quran and its message, in 19 languages (English, French, Spanish…)."}),
    ("recherche", "conferences", "conferences-alertes", {"ar": "?", "en": "?"},
     {"fr": "Conference Radar · Radar des conférences", "ar": "رادار المؤتمرات · Conference Radar", "en": "Conference Radar"},
     {"fr": "Conférences scientifiques à venir et dates limites, dont comptabilité, finance et finance islamique (EN, FR, AR).",
      "ar": "المؤتمرات العلمية القادمة وآخر الآجال، منها المحاسبة والمالية والمالية الإسلامية (EN، FR، AR).",
      "en": "Upcoming scientific conferences and deadlines, including accounting, finance and Islamic finance (EN, FR, AR)."}),
]


def adresse(sous, regle, l):
    u = f"https://{sous}.clicvia.com/"
    r = regle.get(l)
    return u if l == "fr" or not r else (u + l + "/" if r == "dossier" else u + "?lang=" + l)


def langues_du_site(regle):
    """Petite étiquette de la carte, sur la page anglaise seulement : dans quelles langues est le site."""
    if regle.get("plus"):
        return f"{regle['plus']} languages"
    return " · ".join(x for x, ok in (("EN", regle.get("en")), ("FR", True), ("AR", regle.get("ar"))) if ok)


def lire(p):
    return io.open(os.path.join(RACINE, p), encoding="utf-8", newline="").read()


def ecrire(p, t):
    os.makedirs(os.path.dirname(os.path.join(RACINE, p)) or RACINE, exist_ok=True)
    io.open(os.path.join(RACINE, p), "w", encoding="utf-8", newline="\n").write(t)


def tete_page(l, gabarit, titre, description, og_titre, og_description, url_de, ld):
    """En-tête technique (meta, CSP, GoatCounter, scripts) commun à l'accueil et à « Comment fonctionne le site ? »."""
    url = url_de(l)
    tete, _, _ = gabarit.partition("<body>")
    hreflang = "".join(f'<link rel="alternate" hreflang="{x}" href="{url_de(x)}">\n' for x in LANGUES) \
        + f'<link rel="alternate" hreflang="x-default" href="{url_de("fr")}">\n'
    rempl = [
        (r'<html lang="fr" translate="no">', f'<html lang="{l}"{RTL if l == "ar" else ""} translate="no">'),
        (r"<title>.*?</title>", f"<title>{E(titre)}</title>"),
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(description)}">'),
        (r'<link rel="canonical" href="[^"]*">\n(?:<link rel="alternate"[^\n]*\n)*', f'<link rel="canonical" href="{url}">\n' + hreflang),
        (r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(og_titre)}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(og_description)}">'),
        (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">'),
        (r'<meta property="og:locale" content="[^"]*">(?:<meta property="og:locale:alternate" content="[^"]*">)*',
         f'<meta property="og:locale" content="{LOCALE[l]}">' + "".join(f'<meta property="og:locale:alternate" content="{LOCALE[x]}">' for x in LANGUES if x != l)),
        (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{E(og_titre)}">'),
        (r'<link rel="icon" href="assets/logo.svg"', '<link rel="icon" href="/assets/logo.svg"'),
        (r'<link rel="icon" href="favicon.ico"', '<link rel="icon" href="/favicon.ico"'),
        (r'<link rel="apple-touch-icon" href="assets/', '<link rel="apple-touch-icon" href="/assets/'),
        (r'<script defer src="/assets/portail.js"></script>', '<script defer src="/assets/portail.js"></script>\n<script defer src="/assets/langue.js"></script>'),
    ]
    for motif, par in rempl:
        tete, n = re.subn(motif, lambda m, par=par: par, tete, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"gabarit : motif introuvable : {motif[:60]}")
    return tete


def pied(l):
    """Pied de page commun : Facebook, lien « Comment fonctionne le site ? » (règle commune § 44), mentions."""
    T = lambda k: TEXTES[k][l]
    return f'''<footer><p class="suivre"><a href="https://www.facebook.com/1327283777142447" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-8h2.7l.4-3.1h-3.1V7.9c0-.9.3-1.5 1.6-1.5h1.7V3.6c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.5-4 4.1v2.3H7.7V13h2.7v8h3.1z"/></svg> {E(T("facebook"))}</a></p>
<p class="pied-liens"><a href="{chemin_a_propos(l)}">{E(T("a_propos"))}</a> · <a href="{"/" if l == "fr" else "/" + l + "/"}">{E(T("tous"))}</a></p>
{E(T("pied"))}</footer>
</body>
</html>
'''


def chemin_a_propos(l):
    return "/a-propos/" if l == "fr" else "/" + l + "/a-propos/"


def page(l, gabarit, jour):
    T = lambda k: TEXTES[k][l]
    url_de = lambda x: BASE if x == "fr" else BASE + x + "/"
    liste = [{"@type": "ListItem", "position": i + 1, "name": nom[l], "description": desc[l], "url": adresse(sous, regle, l)}
             for i, (_, sous, _, regle, nom, desc) in enumerate(SITES)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": BASE + "#organisation", "name": "Clicvia", "url": BASE, "logo": BASE + "og-image-v2.jpg",
         "sameAs": ["https://www.facebook.com/1327283777142447"], "areaServed": "TN"},
        {"@type": "WebSite", "@id": BASE + "#site", "name": "Clicvia", "alternateName": T("autre_nom"), "url": BASE, "inLanguage": LANGUES,
         "publisher": {"@id": BASE + "#organisation"}},
        {"@type": "ItemList", "name": T("liste"), "numberOfItems": len(SITES), "itemListElement": liste}]}
    tete = tete_page(l, gabarit, T("titre"), T("description"), T("og_titre"), T("og_description"), url_de, ld)
    choix = "".join(f'<a href="{"/" if x == "fr" else "/" + x + "/"}" lang="{code}" data-langue="{x}"{COURANT if x == l else ""}>{nom}</a>' for x, nom, code in NOM_LANGUE)
    corps = [f'''<section class="hero"><div class="wrap">
  <nav class="langues" aria-label="{E(T("langue_aria"))}">{choix}</nav>
  <p class="marque"><img class="logo-portail" src="/assets/logo.svg" alt="" width="64" height="64"><span lang="en" dir="ltr">Clicvia</span></p>
  <h1>{E(T("h1"))}</h1>
  <p>{E(T("intro"))}</p>
  <button class="partager" type="button" data-partager-video aria-label="{E(T("partager_aria"))}"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg>{E(T("partager"))}</button>
</div></section>

<main class="grille">''']
    theme = None
    for th, sous, icone, regle, nom, desc in SITES:
        if th != theme:
            theme = th
            corps.append(f'  <h2 class="theme">{E(THEMES[th][l])}</h2>')
        etiquette = f' <small class="langues-site">{E(langues_du_site(regle))}</small>' if l == "en" else ""
        corps.append(f'  <a class="site" href="{adresse(sous, regle, l)}"><img class="ic" src="/assets/sites/{icone}.svg" alt="" width="52" height="52" loading="lazy">\n'
                     f'    <span><h2>{E(nom[l])}{etiquette}</h2><p>{E(desc[l])}</p></span><span class="fl">{"←" if l == "ar" else "→"}</span></a>')
    corps.append("</main>\n\n" + pied(l))
    return tete + "<body>\n" + "\n".join(corps)


# Page « Comment fonctionne le site ? » (règle commune § 44, Ahmed, 25/10/2026) : à mettre à jour à CHAQUE modification visible
# du portail, dans le même envoi. Le test FONCTIONS de tools/test_portail.mjs vérifie que chaque fonction y est expliquée.
# Chaque section : (titre, [phrases ou lignes]) ; une ligne qui commence par « - » devient un point de liste.
A_PROPOS = {
    "fr": {
        "titre": "Comment fonctionne le site ? — Clicvia",
        "description": "Comment fonctionne Clicvia : un portail gratuit qui rassemble nos services pour la Tunisie, en trois langues. D'où viennent les informations, vos données, les mises à jour automatiques.",
        "intro": "Clicvia est un portail : une seule page qui rassemble {n} sites gratuits pour la Tunisie. Voici comment il marche.",
        "sections": [
            ("À quoi sert Clicvia ?", [
                "Il vous montre tous nos services en un coup d'œil, rangés par thème : permis et voiture, papiers, travail, maison, religion, enseignants et chercheurs.",
                "Touchez une carte pour ouvrir le site. Chaque carte donne le nom du site et ce qu'il fait."]),
            ("Comment s'en servir", [
                "- Les cartes des sites : une carte par site, rangées par thème. Elle ouvre le site dans votre langue quand il l'a.",
                "- Trois langues : les boutons Français, العربية et English en haut de la page. Chaque langue a sa propre adresse (clicvia.com/ar/ et clicvia.com/en/).",
                "- Sur la page en anglais, une petite étiquette sur chaque carte dit dans quelles langues est le site.",
                "- Le bouton « Partager » envoie à vos proches le lien de notre vidéo de présentation et l'adresse du portail (menu de partage du téléphone, sinon WhatsApp).",
                "- La vidéo de présentation : un lien en bas de la page ouvre une courte vidéo qui montre nos services.",
                "- La page Facebook Clicvia : le bouton « Suivez Clicvia sur Facebook » en bas de page. Nos pages y sont publiées automatiquement chaque jour."]),
            ("D'où viennent les informations ?", [
                "Chaque site relève lui-même ses informations (sources officielles, sites des magasins, données libres) et écrit sa source et sa date sur ses pages.",
                "Le portail ne fait que présenter les sites. Les assistants et les programmeurs trouvent la liste de nos données ouvertes dans le fichier donnees.json."]),
            ("Gratuit ou payant ?", [
                "Le portail est gratuit, sans compte et sans inscription.",
                "La plupart de nos services sont gratuits. Certains sites proposent en plus une partie payante (un « Pass »). Elle est toujours indiquée clairement sur le site concerné."]),
            ("Vos données", [
                "Le portail ne vous demande rien : ni nom, ni téléphone, ni e-mail.",
                "Les statistiques de visite sont anonymes, sans cookies (GoatCounter). Elles comptent seulement les pages vues et les clics sur les boutons."]),
            ("Mises à jour automatiques", [
                "La liste des sites, les trois langues, le plan du site et cette page sont fabriqués automatiquement.",
                "Quand une page change, les moteurs de recherche sont prévenus automatiquement. Chaque site met à jour ses propres données tout seul."]),
            ("Un site indépendant", [
                "Clicvia et ses sites sont indépendants et non officiels : ils ne dépendent d'aucune administration ni d'aucune entreprise citée."]),
        ]},
    "ar": {
        "titre": "كيف يعمل الموقع؟ — Clicvia",
        "description": "كيف يعمل Clicvia: بوابة مجانية تجمع خدماتنا لتونس بثلاث لغات. من أين تأتي المعلومات، معطياتك، والتحيين الآلي.",
        "intro": "Clicvia بوابة: صفحة واحدة تجمع {n} موقعًا مجانيًا لتونس. إليك كيف تعمل.",
        "sections": [
            ("ما فائدة Clicvia؟", [
                "تعرض لك كل خدماتنا بنظرة واحدة، مرتّبة حسب الموضوع: الرخصة والسيارة، الوثائق، الشغل، المنزل، الدين، الأساتذة والباحثون.",
                "اضغط على بطاقة لفتح الموقع. كل بطاقة تذكر اسم الموقع وما يقدّمه."]),
            ("كيف تستعملها", [
                "- بطاقات المواقع: بطاقة لكل موقع، مرتّبة حسب الموضوع. تفتح الموقع بلغتك إن وُجدت.",
                "- ثلاث لغات: أزرار Français و العربية و English في أعلى الصفحة. لكل لغة عنوانها (clicvia.com/ar/ و clicvia.com/en/).",
                "- في الصفحة الإنجليزية، تُبيّن علامة صغيرة على كل بطاقة لغات الموقع.",
                "- زر «شارك» يرسل إلى أقاربك رابط الفيديو التقديمي وعنوان البوابة (قائمة المشاركة في الهاتف، وإلا واتساب).",
                "- الفيديو التقديمي: رابط أسفل الصفحة يفتح فيديو قصيرًا يعرض خدماتنا.",
                "- صفحة Clicvia على فيسبوك: زر «تابعوا Clicvia على فيسبوك» أسفل الصفحة. تُنشر فيها صفحاتنا آليًا كل يوم."]),
            ("من أين تأتي المعلومات؟", [
                "كل موقع يجمع معلوماته بنفسه (مصادر رسمية، مواقع المغازات، معطيات حرّة) ويكتب مصدرها وتاريخها في صفحاته.",
                "البوابة تعرض المواقع فقط. يجد المساعدون والمبرمجون قائمة معطياتنا المفتوحة في الملف donnees.json."]),
            ("مجاني أم بمقابل؟", [
                "البوابة مجانية، دون حساب ودون تسجيل.",
                "أغلب خدماتنا مجانية. بعض المواقع تقترح جزءًا بمقابل (Pass)، ويكون مذكورًا بوضوح في الموقع المعني."]),
            ("معطياتك", [
                "البوابة لا تطلب منك شيئًا: لا اسم ولا هاتف ولا بريد إلكتروني.",
                "إحصائيات الزيارة مجهولة الهوية ودون ملفات تعريف الارتباط (GoatCounter). تحسب فقط الصفحات المزارة والنقرات على الأزرار."]),
            ("تحيين آلي", [
                "قائمة المواقع واللغات الثلاث وخريطة الموقع وهذه الصفحة تُصنع آليًا.",
                "عندما تتغيّر صفحة، تُعلَم محركات البحث آليًا. وكل موقع يحيّن معطياته بنفسه."]),
            ("موقع مستقل", [
                "Clicvia ومواقعها مستقلة وغير رسمية: لا تتبع أي إدارة ولا أي مؤسسة مذكورة."]),
        ]},
    "en": {
        "titre": "How does the site work? — Clicvia",
        "description": "How Clicvia works: a free portal that brings together our services for Tunisia, in three languages. Where the information comes from, your data, automatic updates.",
        "intro": "Clicvia is a portal: one page that brings together {n} free websites for Tunisia. Here is how it works.",
        "sections": [
            ("What is Clicvia for?", [
                "It shows all our services at a glance, sorted by theme: driving and car, paperwork, work, home, religion, teachers and researchers.",
                "Tap a card to open the website. Each card gives the website's name and what it does."]),
            ("How to use it", [
                "- Website cards: one card per website, sorted by theme. It opens the website in your language when it has it.",
                "- Three languages: the Français, العربية and English buttons at the top of the page. Each language has its own address (clicvia.com/ar/ and clicvia.com/en/).",
                "- On the English page, a small label on each card says which languages the website is in.",
                "- The “Share” button sends your friends the link to our presentation video and the portal's address (your phone's share menu, otherwise WhatsApp).",
                "- The presentation video: a link at the bottom of the page opens a short video showing our services.",
                "- The Clicvia Facebook page: the “Follow Clicvia on Facebook” button at the bottom. Our pages are posted there automatically every day."]),
            ("Where does the information come from?", [
                "Each website collects its own information (official sources, shop websites, open data) and writes its source and date on its pages.",
                "The portal only presents the websites. Assistants and programmers will find the list of our open data in the donnees.json file."]),
            ("Free or paid?", [
                "The portal is free, with no account and no sign-up.",
                "Most of our services are free. Some websites also offer a paid part (a “Pass”), always clearly shown on the website concerned."]),
            ("Your data", [
                "The portal asks you for nothing: no name, no phone number, no e-mail.",
                "Visit statistics are anonymous, with no cookies (GoatCounter). They only count pages viewed and button clicks."]),
            ("Automatic updates", [
                "The list of websites, the three languages, the sitemap and this page are built automatically.",
                "When a page changes, search engines are notified automatically. Each website updates its own data by itself."]),
            ("An independent website", [
                "Clicvia and its websites are independent and unofficial: they do not depend on any administration or on any company mentioned."]),
        ]},
}


def insecable(l, t):
    """Espace insécable avant « ? ! : ; » (français) et entre un nombre et le mot qui suit (règle commune § 30)."""
    t = re.sub(r"(\d) (?=\w)", "\\1\u00a0", t)
    return re.sub(r" ([?!:;»])", "\u00a0\\1", re.sub(r"« ", "«\u00a0", t)) if l == "fr" else t


def page_a_propos(l, gabarit):
    A, T = A_PROPOS[l], (lambda k: TEXTES[k][l])
    url_de = lambda x: BASE + ("" if x == "fr" else x + "/") + "a-propos/"
    ld = {"@context": "https://schema.org", "@type": "AboutPage", "name": T("a_propos"), "url": url_de(l), "inLanguage": l,
          "isPartOf": {"@type": "WebSite", "name": "Clicvia", "url": BASE}}
    tete = tete_page(l, gabarit, A["titre"], A["description"], A["titre"], A["description"], url_de, ld)
    choix = "".join(f'<a href="{chemin_a_propos(x)}" lang="{code}" data-langue="{x}"{COURANT if x == l else ""}>{nom}</a>' for x, nom, code in NOM_LANGUE)
    I = lambda t: E(insecable(l, t))
    corps = [f'''<section class="hero hero-court"><div class="wrap">
  <nav class="langues" aria-label="{E(T("langue_aria"))}">{choix}</nav>
  <p class="marque"><a class="retour-portail" href="{"/" if l == "fr" else "/" + l + "/"}"><img class="logo-portail" src="/assets/logo.svg" alt="" width="64" height="64"><span lang="en" dir="ltr">Clicvia</span></a></p>
  <h1>{I(T("a_propos"))}</h1>
  <p>{I(A["intro"].format(n=len(SITES)))}</p>
</div></section>

<main class="a-propos">''']
    for titre, lignes in A["sections"]:
        corps.append(f'<section class="ap-carte"><h2>{I(titre)}</h2>')
        liste = []
        for ligne in lignes + [""]:
            if ligne.startswith("- "):
                liste.append(f"<li>{I(ligne[2:])}</li>")
                continue
            if liste:
                corps.append("<ul>" + "".join(liste) + "</ul>")
                liste = []
            if ligne:
                corps.append(f"<p>{I(ligne)}</p>")
        corps.append("</section>")
    corps.append(f'<p class="ap-retour"><a href="{"/" if l == "fr" else "/" + l + "/"}">{"→" if l == "ar" else "←"} {E(T("tous"))}</a></p>')
    corps.append("</main>\n\n" + pied(l))
    return tete + "<body>\n" + "\n".join(corps)


def main():
    jour = datetime.date.today().isoformat()
    gabarit = lire("tools/gabarit.html")
    for l in LANGUES:
        ecrire("index.html" if l == "fr" else l + "/index.html", page(l, gabarit, jour))
        ecrire(chemin_a_propos(l).strip("/") + "/index.html", page_a_propos(l, gabarit))
    liens = "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{BASE if x == "fr" else BASE + x + "/"}"/>' for x in LANGUES) \
        + f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
    ecrire("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + "".join(f'<url><loc>{BASE if l == "fr" else BASE + l + "/"}</loc><lastmod>{jour}</lastmod>{liens}</url>\n' for l in LANGUES)
           + "".join(f'<url><loc>{BASE}{chemin_a_propos(l)[1:]}</loc><lastmod>{jour}</lastmod></url>\n' for l in LANGUES)
           + f'  <url><loc>{BASE}video/</loc></url>\n</urlset>\n')
    # llms.txt : présentation du portail et de ses sites pour les assistants IA (référencement sur les IA, 13/10/2026)
    ia = ["# Clicvia — services pratiques gratuits pour la Tunisie", "", "> " + TEXTES["description"]["fr"], "",
          f"Portail de {len(SITES)} sites gratuits et indépendants (non officiels), en français et en arabe pour la plupart ; adresse : {BASE} (aussi {BASE}ar/ et {BASE}en/).",
          "Chaque site a son propre fichier llms.txt à sa racine (exemple : https://concours.clicvia.com/llms.txt).",
          f"Données fraîches au format JSON (concours ouverts, appels d'offres, prix de l'eau, conférences, mosquées, points d'eau) : index dans {BASE}donnees.json", ""]
    theme = None
    for th, sous, _, regle, nom, desc in SITES:
        if th != theme:
            theme = th
            ia += ["## " + THEMES[th]["fr"], ""]
        ia.append(f"- [{nom['fr']}](https://{sous}.clicvia.com/) : {desc['fr']}")
        if all(x[0] != th for x in SITES[SITES.index((th, sous, _, regle, nom, desc)) + 1:]):
            ia.append("")
    ia += ["## À savoir", "", "- Les données (prix, concours, appels d'offres, annonces) sont relevées automatiquement ; la date de mise à jour et la source officielle sont écrites sur les pages.",
           "- Pour citer : le nom du site et le lien de la page utilisée.",
           "- Les assistants IA qui répondent à une question en citant leur source sont les bienvenus ; l'aspiration du contenu pour entraîner un modèle n'est pas autorisée (voir robots.txt).", ""]
    ecrire("llms.txt", chr(10).join(ia))
    print(f"portail : {len(LANGUES)} accueils + {len(LANGUES)} pages « Comment fonctionne le site ? » ({', '.join(LANGUES)}), {len(SITES)} sites, plan du site à jour")


if __name__ == "__main__":
    main()
