# -*- coding: utf-8 -*-
"""Pages « Confidentialité » et « Conditions d'utilisation » COMMUNES à tous les sites clicvia.com (17/11/2026, liste des 20 points
d'Ahmed, règle commune § 58). Fabriquées par tools/construire.py en 3 langues :
  /confidentialite/, /ar/confidentialite/, /en/confidentialite/   et   /conditions/, /ar/conditions/, /en/conditions/
Chaque site met dans son pied de page les liens https://clicvia.com/confidentialite/ et https://clicvia.com/conditions/
(contrôle : outils visibilite/controle_20_points.mjs). Un site qui collecte une NOUVELLE donnée (nouveau formulaire, nouveau service)
= une ligne de plus ici, dans les 3 langues, dans le même envoi.
Texte écrit d'après ce que les sites font vraiment (formulaires Formspree, GoatCounter sans cookies, hébergement GitHub Pages,
paiements par virement / D17 traités à la main, alertes par e-mail ou Telegram). Ce n'est pas un avis juridique."""

MAJ = {"fr": "Mise à jour : 17 novembre 2026.", "ar": "آخر تحديث: 17 نوفمبر 2026.", "en": "Last updated: 17 November 2026."}

CONFIDENTIALITE = {
    "fr": {
        "titre": "Confidentialité — Clicvia",
        "nom": "Confidentialité",
        "description": "Quelles données nos sites gratuits pour la Tunisie recueillent, pourquoi, combien de temps, et comment demander leur effacement.",
        "intro": "Cette page vaut pour clicvia.com et pour tous ses sites (adresses en .clicvia.com). Nous recueillons le moins de données possible.",
        "sections": [
            ("Ce que nous ne faisons pas", [
                "- Pas de compte à créer pour utiliser les sites.",
                "- Pas de cookies publicitaires ni de traceurs (pas de Google Analytics, pas de pixel Facebook) : aucun bandeau de cookies n'est donc nécessaire.",
                "- Nous ne vendons ni ne louons aucune donnée."]),
            ("Statistiques de visite (anonymes)", [
                "Nous comptons les visites avec GoatCounter, sans cookies et sans enregistrer qui vous êtes : page vue, pays, type d'appareil, et sur certains sites les clics sur des boutons (Appeler, WhatsApp, Partager) et les mots cherchés sans résultat. Ces chiffres servent seulement à améliorer les sites."]),
            ("Ce que vous nous envoyez", [
                "Seulement quand vous remplissez un formulaire et cliquez sur « Envoyer » :",
                "- « Votre avis » : votre message et l'adresse e-mail que vous donnez (pour vous répondre).",
                "- Annuaires (ajout ou correction d'une fiche, formule Pro) : nom de l'établissement, téléphone, adresse, e-mail.",
                "- Offres payantes (Pass, Alertes Pro) et alertes : e-mail ou numéro, offre choisie, preuve de paiement (virement, D17…) ; le paiement est vérifié à la main, nous ne voyons jamais votre carte bancaire.",
                "- Alertes par Telegram : votre identifiant Telegram, seulement si vous démarrez notre robot.",
                "Ces informations servent uniquement à traiter votre demande. Les formulaires passent par le service Formspree ; les sites sont hébergés par GitHub Pages, qui garde quelques jours des journaux techniques (adresse IP) pour la sécurité."]),
            ("Informations publiées sur les sites", [
                "Les annuaires publient des informations professionnelles déjà publiques (OpenStreetMap, listes officielles, page de l'établissement) ou données par l'établissement. Les annonces immobilières viennent de sites d'annonces publics. Un établissement peut demander une correction ; une demande de retrait n'est traitée qu'après avoir vérifié qu'elle vient bien de lui (appel au numéro de la fiche)."]),
            ("Dans votre téléphone", [
                "Certains sites gardent dans votre navigateur vos réglages (langue, favoris, rappels, code d'un Pass). Ces données restent chez vous : effacez-les en vidant les données du site dans votre navigateur."]),
            ("Durée de conservation", [
                "- Demandes et messages : le temps de les traiter, puis au plus 3 ans.",
                "- Abonnés aux offres payantes : la durée de l'abonnement, puis au plus 3 ans (preuves de paiement : durée légale).",
                "- Statistiques anonymes : sans limite (elles ne permettent pas de vous reconnaître)."]),
            ("Vos droits", [
                "Selon la loi tunisienne sur la protection des données personnelles (loi organique n° 2004-63), vous pouvez demander à voir, corriger ou effacer vos données, ou vous opposer à leur utilisation. Écrivez-nous par le formulaire « Votre avis » du site concerné en indiquant votre demande ; nous répondons sous 30 jours. Vous pouvez aussi vous adresser à l'Instance nationale de protection des données personnelles (INPDP)."]),
        ],
    },
    "ar": {
        "titre": "الخصوصية — Clicvia",
        "nom": "الخصوصية",
        "description": "ما هي المعطيات التي تجمعها مواقعنا المجانية لتونس، ولماذا، وإلى متى، وكيف تطلب حذفها.",
        "intro": "تنطبق هذه الصفحة على clicvia.com وعلى كل مواقعه (العناوين التي تنتهي بـ .clicvia.com). نجمع أقل ما يمكن من المعطيات.",
        "sections": [
            ("ما لا نفعله", [
                "- لا حاجة لإنشاء حساب لاستعمال المواقع.",
                "- لا ملفات تعريف ارتباط إشهارية ولا أدوات تتبّع (لا Google Analytics ولا بكسل فيسبوك): لذلك لا حاجة لشريط ملفات تعريف الارتباط.",
                "- لا نبيع ولا نؤجّر أي معطيات."]),
            ("إحصائيات الزيارة (مجهولة)", [
                "نحسب الزيارات بواسطة GoatCounter دون ملفات تعريف الارتباط ودون معرفة هويتك: الصفحة المزارة، البلد، نوع الجهاز، وفي بعض المواقع النقرات على الأزرار (اتصال، واتساب، مشاركة) والكلمات التي لم تُعط نتيجة. تُستعمل هذه الأرقام فقط لتحسين المواقع."]),
            ("ما ترسله إلينا", [
                "فقط عندما تملأ استمارة وتضغط على « إرسال »:",
                "- « رأيك »: رسالتك والبريد الإلكتروني الذي تقدّمه (للردّ عليك).",
                "- الأدلّة (إضافة بطاقة أو تصحيحها، صيغة Pro): اسم المؤسسة، الهاتف، العنوان، البريد الإلكتروني.",
                "- العروض المدفوعة (Pass، تنبيهات Pro) والتنبيهات: البريد الإلكتروني أو الرقم، العرض المختار، إثبات الدفع (تحويل، D17…)؛ نتثبّت من الدفع يدويًا ولا نرى أبدًا بطاقتك البنكية.",
                "- التنبيهات عبر تيليغرام: معرّفك في تيليغرام، فقط إذا شغّلت روبوتنا.",
                "تُستعمل هذه المعلومات فقط لمعالجة طلبك. تمرّ الاستمارات عبر خدمة Formspree؛ والمواقع مستضافة لدى GitHub Pages التي تحتفظ لبضعة أيام بسجلات تقنية (عنوان IP) لأغراض الأمان."]),
            ("المعلومات المنشورة في المواقع", [
                "تنشر الأدلّة معلومات مهنية منشورة سابقًا (OpenStreetMap، القوائم الرسمية، صفحة المؤسسة) أو قدّمتها المؤسسة. وتأتي الإعلانات العقارية من مواقع إعلانات عامة. يمكن للمؤسسة طلب التصحيح؛ ولا يُعالج طلب الحذف إلا بعد التثبت من أنه صادر عنها (اتصال بالرقم المذكور في البطاقة)."]),
            ("في هاتفك", [
                "تحتفظ بعض المواقع في متصفحك بإعداداتك (اللغة، المفضلة، التذكيرات، رمز Pass). تبقى هذه المعطيات عندك: احذفها بمسح بيانات الموقع في متصفحك."]),
            ("مدة الحفظ", [
                "- الطلبات والرسائل: مدة معالجتها، ثم 3 سنوات على الأكثر.",
                "- المشتركون في العروض المدفوعة: مدة الاشتراك، ثم 3 سنوات على الأكثر (إثباتات الدفع: المدة القانونية).",
                "- الإحصائيات المجهولة: دون حدّ (لا تسمح بالتعرّف عليك)."]),
            ("حقوقك", [
                "طبقًا للقانون التونسي لحماية المعطيات الشخصية (القانون الأساسي عدد 63 لسنة 2004)، يمكنك طلب الاطلاع على معطياتك أو تصحيحها أو حذفها أو الاعتراض على استعمالها. راسلنا عبر استمارة « رأيك » في الموقع المعني مع ذكر طلبك؛ نجيب في أجل 30 يومًا. ويمكنك أيضًا التوجّه إلى الهيئة الوطنية لحماية المعطيات الشخصية."]),
        ],
    },
    "en": {
        "titre": "Privacy — Clicvia",
        "nom": "Privacy",
        "description": "What data our free sites for Tunisia collect, why, for how long, and how to ask for it to be deleted.",
        "intro": "This page covers clicvia.com and all its sites (addresses ending in .clicvia.com). We collect as little data as possible.",
        "sections": [
            ("What we do not do", [
                "- No account is needed to use the sites.",
                "- No advertising cookies or trackers (no Google Analytics, no Facebook pixel): no cookie banner is therefore needed.",
                "- We never sell or rent any data."]),
            ("Visit statistics (anonymous)", [
                "We count visits with GoatCounter, without cookies and without knowing who you are: page viewed, country, device type and, on some sites, clicks on buttons (Call, WhatsApp, Share) and searches with no result. These figures are only used to improve the sites."]),
            ("What you send us", [
                "Only when you fill in a form and press “Send”:",
                "- “Your opinion”: your message and the e-mail address you give (to reply to you).",
                "- Directories (adding or correcting a listing, Pro plan): name of the business, phone, address, e-mail.",
                "- Paid offers (Pass, Pro alerts) and alerts: e-mail or number, chosen offer, proof of payment (bank transfer, D17…); payments are checked by hand, we never see your bank card.",
                "- Telegram alerts: your Telegram ID, only if you start our bot.",
                "This information is only used to handle your request. Forms go through the Formspree service; the sites are hosted by GitHub Pages, which keeps technical logs (IP address) for a few days for security."]),
            ("Information published on the sites", [
                "The directories publish professional information that is already public (OpenStreetMap, official lists, the business's own page) or given by the business. Property listings come from public listing sites. A business can ask for a correction; a removal request is only handled after checking that it really comes from that business (a call to the number on the listing)."]),
            ("On your phone", [
                "Some sites keep your settings in your browser (language, favourites, reminders, Pass code). This data stays with you: delete it by clearing the site's data in your browser."]),
            ("How long we keep data", [
                "- Requests and messages: as long as needed to handle them, then 3 years at most.",
                "- Subscribers to paid offers: the length of the subscription, then 3 years at most (proofs of payment: legal period).",
                "- Anonymous statistics: no limit (they cannot identify you)."]),
            ("Your rights", [
                "Under the Tunisian personal data protection law (Organic Law No. 2004-63) you can ask to see, correct or delete your data, or object to its use. Write to us through the “Your opinion” form of the site concerned, stating your request; we answer within 30 days. You can also contact the National Authority for the Protection of Personal Data (INPDP)."]),
        ],
    },
}

CONDITIONS = {
    "fr": {
        "titre": "Conditions d'utilisation — Clicvia",
        "nom": "Conditions d'utilisation",
        "description": "Conditions d'utilisation de clicvia.com et de ses sites gratuits pour la Tunisie : informations indicatives, sources, offres payantes.",
        "intro": "En utilisant clicvia.com ou l'un de ses sites (adresses en .clicvia.com), vous acceptez ces conditions simples.",
        "sections": [
            ("Des sites indépendants et non officiels", [
                "Nos sites sont édités par Clicvia, éditeur indépendant en Tunisie. Ils ne sont liés à aucune administration, aucun ministère ni aucune entreprise citée. Pour une démarche officielle, la source officielle indiquée sur chaque page fait foi."]),
            ("Informations données à titre indicatif", [
                "Prix, concours, appels d'offres, annonces, adresses et téléphones sont relevés automatiquement à partir de sources publiques, avec leur date et leur source. Ils peuvent changer ou contenir des erreurs : vérifiez auprès de la source (ou appelez) avant de décider ou de vous déplacer. Les calculs (salaire, impôt, crédit…) sont des estimations selon les barèmes publiés.",
                "Nous ne pouvons pas être tenus responsables d'une décision prise sur la seule base de ces informations."]),
            ("Utilisation des sites", [
                "- L'utilisation est gratuite, sauf les offres payantes clairement indiquées.",
                "- Il est interdit de perturber les sites, d'y envoyer de faux formulaires ou de copier leur contenu en masse par des programmes (voir robots.txt). Citer une page avec son lien est bienvenu.",
                "- Les données OpenStreetMap sont sous licence ODbL (© les contributeurs d'OpenStreetMap) ; les photos sous licence libre sont créditées sur chaque site."]),
            ("Offres payantes (Pass, Pro, Alertes)", [
                "Le prix, la durée, ce qui est inclus et le mode de paiement sont affichés sur la page de l'offre avant tout paiement. L'accès est ouvert après vérification du paiement. Une question ou un problème : écrivez-nous par le formulaire « Votre avis » du site ; un accès payé qui ne fonctionne pas est rétabli."]),
            ("Annuaires et fiches", [
                "Un établissement peut demander gratuitement la correction de sa fiche. Une demande de retrait n'est traitée qu'après vérification auprès de l'établissement, pour qu'aucune fiche ne soit retirée par un tiers."]),
            ("Changements et droit applicable", [
                "Ces conditions peuvent être mises à jour ; la date est indiquée en bas de page. Elles sont soumises au droit tunisien.",
                "Vos données personnelles : voir la page Confidentialité."]),
        ],
    },
    "ar": {
        "titre": "شروط الاستعمال — Clicvia",
        "nom": "شروط الاستعمال",
        "description": "شروط استعمال clicvia.com ومواقعه المجانية لتونس: معلومات للإرشاد، المصادر، العروض المدفوعة.",
        "intro": "باستعمالك clicvia.com أو أحد مواقعه (العناوين التي تنتهي بـ .clicvia.com)، فإنك تقبل هذه الشروط البسيطة.",
        "sections": [
            ("مواقع مستقلة وغير رسمية", [
                "ينشر مواقعَنا Clicvia، ناشر مستقل في تونس. لا علاقة لها بأي إدارة أو وزارة أو مؤسسة مذكورة. في أي إجراء رسمي، المصدر الرسمي المذكور في كل صفحة هو المرجع."]),
            ("معلومات للإرشاد فقط", [
                "الأسعار والمناظرات وطلبات العروض والإعلانات والعناوين والهواتف تُجمع آليًا من مصادر عامة مع تاريخها ومصدرها. قد تتغيّر أو تحتوي على أخطاء: تثبّت من المصدر (أو اتصل) قبل اتخاذ قرار أو التنقّل. الحسابات (الأجر، الضريبة، القرض…) تقديرات حسب الجداول المنشورة.",
                "لا نتحمّل المسؤولية عن قرار يُتّخذ بالاعتماد على هذه المعلومات وحدها."]),
            ("استعمال المواقع", [
                "- الاستعمال مجاني، باستثناء العروض المدفوعة المذكورة بوضوح.",
                "- يُمنع تعطيل المواقع أو إرسال استمارات زائفة أو نسخ محتواها بكثافة ببرامج آلية (انظر robots.txt). ذكر صفحة مع رابطها مرحّب به.",
                "- معطيات OpenStreetMap مرخّصة بـ ODbL (© المساهمون في OpenStreetMap)؛ والصور ذات الترخيص الحر مذكور أصحابها في كل موقع."]),
            ("العروض المدفوعة (Pass، Pro، التنبيهات)", [
                "يُعرض السعر والمدة وما يشمله العرض وطريقة الدفع في صفحة العرض قبل أي دفع. يُفتح الوصول بعد التثبّت من الدفع. لأي سؤال أو مشكلة: راسلنا عبر استمارة « رأيك » في الموقع؛ الوصول المدفوع الذي لا يعمل يُصلَح."]),
            ("الأدلّة والبطاقات", [
                "يمكن للمؤسسة طلب تصحيح بطاقتها مجانًا. لا يُعالج طلب الحذف إلا بعد التثبّت مع المؤسسة، حتى لا يحذف أحدٌ بطاقة غيره."]),
            ("التغييرات والقانون المنطبق", [
                "يمكن تحيين هذه الشروط؛ والتاريخ مذكور أسفل الصفحة. وهي خاضعة للقانون التونسي.",
                "معطياتك الشخصية: انظر صفحة الخصوصية."]),
        ],
    },
    "en": {
        "titre": "Terms of use — Clicvia",
        "nom": "Terms of use",
        "description": "Terms of use of clicvia.com and its free sites for Tunisia: information for guidance only, sources, paid offers.",
        "intro": "By using clicvia.com or one of its sites (addresses ending in .clicvia.com), you accept these simple terms.",
        "sections": [
            ("Independent, unofficial sites", [
                "Our sites are published by Clicvia, an independent publisher in Tunisia. They are not linked to any administration, ministry or company mentioned. For any official procedure, the official source shown on each page prevails."]),
            ("Information for guidance only", [
                "Prices, competitions, tenders, listings, addresses and phone numbers are collected automatically from public sources, with their date and source. They may change or contain errors: check with the source (or call) before deciding or travelling. Calculators (salary, tax, loan…) give estimates based on published scales.",
                "We cannot be held responsible for a decision based only on this information."]),
            ("Using the sites", [
                "- Use is free, except for clearly marked paid offers.",
                "- It is forbidden to disrupt the sites, send fake forms or copy their content in bulk with programs (see robots.txt). Quoting a page with its link is welcome.",
                "- OpenStreetMap data is under the ODbL licence (© OpenStreetMap contributors); freely licensed photos are credited on each site."]),
            ("Paid offers (Pass, Pro, Alerts)", [
                "The price, duration, what is included and how to pay are shown on the offer page before any payment. Access is opened once the payment has been checked. Any question or problem: write to us through the site's “Your opinion” form; paid access that does not work is restored."]),
            ("Directories and listings", [
                "A business can ask for its listing to be corrected free of charge. A removal request is only handled after checking with the business, so that no listing can be removed by someone else."]),
            ("Changes and governing law", [
                "These terms may be updated; the date is shown at the bottom of the page. They are governed by Tunisian law.",
                "Your personal data: see the Privacy page."]),
        ],
    },
}
