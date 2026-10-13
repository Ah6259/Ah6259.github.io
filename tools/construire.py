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
    "liste": {"fr": "Services Clicvia", "ar": "خدمات Clicvia", "en": "Clicvia services"},
    "autre_nom": {"fr": "Clicvia — services pratiques pour la Tunisie", "ar": "Clicvia — خدمات عملية لتونس", "en": "Clicvia — practical services for Tunisia"},
}
NOM_LANGUE = [("fr", "Français", "fr"), ("ar", "العربية", "ar"), ("en", "English", "en")]
LOCALE = {"fr": "fr_TN", "ar": "ar_TN", "en": "en_US"}

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


def page(l, gabarit, jour):
    T = lambda k: TEXTES[k][l]
    url = BASE if l == "fr" else BASE + l + "/"
    tete, _, _ = gabarit.partition("<body>")
    liste = [{"@type": "ListItem", "position": i + 1, "name": nom[l], "description": desc[l], "url": adresse(sous, regle, l)}
             for i, (_, sous, _, regle, nom, desc) in enumerate(SITES)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": BASE + "#organisation", "name": "Clicvia", "url": BASE, "logo": BASE + "og-image-v2.jpg",
         "sameAs": ["https://www.facebook.com/1327283777142447"], "areaServed": "TN"},
        {"@type": "WebSite", "@id": BASE + "#site", "name": "Clicvia", "alternateName": T("autre_nom"), "url": BASE, "inLanguage": LANGUES,
         "publisher": {"@id": BASE + "#organisation"}},
        {"@type": "ItemList", "name": T("liste"), "numberOfItems": len(SITES), "itemListElement": liste}]}
    hreflang = "".join(f'<link rel="alternate" hreflang="{x}" href="{BASE if x == "fr" else BASE + x + "/"}">\n' for x in LANGUES) \
        + f'<link rel="alternate" hreflang="x-default" href="{BASE}">\n'
    rempl = [
        (r'<html lang="fr" translate="no">', f'<html lang="{l}"{" dir=\"rtl\"" if l == "ar" else ""} translate="no">'),
        (r"<title>.*?</title>", f"<title>{E(T('titre'))}</title>"),
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(T("description"))}">'),
        (r'<link rel="canonical" href="[^"]*">\n(?:<link rel="alternate"[^\n]*\n)*', f'<link rel="canonical" href="{url}">\n' + hreflang),
        (r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(T("og_titre"))}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(T("og_description"))}">'),
        (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">'),
        (r'<meta property="og:locale" content="[^"]*">(?:<meta property="og:locale:alternate" content="[^"]*">)*',
         f'<meta property="og:locale" content="{LOCALE[l]}">' + "".join(f'<meta property="og:locale:alternate" content="{LOCALE[x]}">' for x in LANGUES if x != l)),
        (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{E(T("og_titre"))}">'),
        (r'<link rel="icon" href="assets/logo.svg"', '<link rel="icon" href="/assets/logo.svg"'),
        (r'<link rel="icon" href="favicon.ico"', '<link rel="icon" href="/favicon.ico"'),
        (r'<link rel="apple-touch-icon" href="assets/', '<link rel="apple-touch-icon" href="/assets/'),
        (r'<script defer src="/assets/portail.js"></script>', '<script defer src="/assets/portail.js"></script>\n<script defer src="/assets/langue.js"></script>'),
    ]
    for motif, par in rempl:
        tete, n = re.subn(motif, lambda m, par=par: par, tete, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"gabarit : motif introuvable : {motif[:60]}")
    choix = "".join(f'<a href="{"/" if x == "fr" else "/" + x + "/"}" lang="{code}" data-langue="{x}"{" aria-current=\"true\"" if x == l else ""}>{nom}</a>' for x, nom, code in NOM_LANGUE)
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
    corps.append(f'''</main>

<footer><p class="suivre"><a href="https://www.facebook.com/1327283777142447" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-8h2.7l.4-3.1h-3.1V7.9c0-.9.3-1.5 1.6-1.5h1.7V3.6c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.5-4 4.1v2.3H7.7V13h2.7v8h3.1z"/></svg> {E(T("facebook"))}</a></p>
{E(T("pied"))}</footer>
</body>
</html>
''')
    return tete + "<body>\n" + "\n".join(corps)


def main():
    jour = datetime.date.today().isoformat()
    gabarit = lire("tools/gabarit.html")
    for l in LANGUES:
        ecrire("index.html" if l == "fr" else l + "/index.html", page(l, gabarit, jour))
    liens = "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{BASE if x == "fr" else BASE + x + "/"}"/>' for x in LANGUES) \
        + f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
    ecrire("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + "".join(f'<url><loc>{BASE if l == "fr" else BASE + l + "/"}</loc><lastmod>{jour}</lastmod>{liens}</url>\n' for l in LANGUES)
           + f'  <url><loc>{BASE}video/</loc></url>\n</urlset>\n')
    print(f"portail : {len(LANGUES)} pages ({', '.join(LANGUES)}), {len(SITES)} sites, plan du site à jour")


if __name__ == "__main__":
    main()
