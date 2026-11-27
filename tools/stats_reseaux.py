"""STATISTIQUES DES RÉSEAUX — LECTURE SEULE (27/11/2026, enquête IMM.V d'Ahmed : « pourquoi les sites immobilier ont peu de vues malgré
une publication chaque jour ? »). Ne publie RIEN. Lit, pour la page Facebook Clicvia + @immobilier.clicvia et pour la page / le compte de
Mon agent : vues et interactions des publications des 30 derniers jours (Reels Instagram, Reels et publications Facebook) et les clics sur
le lien de la bio Instagram. N'affiche QUE des totaux et des moyennes (journal d'un dépôt public : ni texte de publication, ni jeton).
Robot : .github/workflows/stats-reseaux.yml (lancé à la main). Secrets : FB_PAGE_ID, FB_PAGE_TOKEN, MONAGENT_FB_PAGE_ID,
MONAGENT_FB_PAGE_TOKEN, MONAGENT_IG_USER_ID."""
import datetime as dt
import json
import os
import urllib.error
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com/v21.0"


def api(chemin, jeton, **p):
    p["access_token"] = jeton
    try:
        with urllib.request.urlopen(f"{GRAPH}/{chemin}?{urllib.parse.urlencode(p)}", timeout=40) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            m = json.load(e).get("error", {}).get("message", "")[:120]
        except Exception:
            m = ""
        return {"erreur": f"{e.code} {m}"}
    except Exception as e:
        return {"erreur": type(e).__name__}


def valeur(ins, nom):
    for x in (ins.get("data") or []):
        if x.get("name") == nom:
            if x.get("total_value"):
                v = x["total_value"].get("value")
            else:
                v = sum(y.get("value") or 0 for y in (x.get("values") or []) if isinstance(y.get("value"), (int, float)))
            return v if isinstance(v, (int, float)) else 0
    return None


def resume(titre, lignes):
    print(f"\n== {titre}")
    for l in lignes:
        print("   " + l)


def instagram(nom, ig, jeton):
    out = []
    medias = api(f"{ig}/media", jeton, fields="id,media_product_type,timestamp,like_count,comments_count", limit=50)
    if "erreur" in medias:
        return resume(f"Instagram {nom}", [f"lecture impossible : {medias['erreur']}"])
    depuis = (dt.datetime.utcnow() - dt.timedelta(days=30)).strftime("%Y-%m-%d")
    ms30 = [m for m in (medias.get("data") or []) if (m.get("timestamp") or "") >= depuis]
    vues, portee, partages, enreg, aimes, comm, err = [], [], 0, 0, 0, 0, ""
    for m in ms30:
        ins = api(f"{m['id']}/insights", jeton, metric="views,reach,shares,saved")
        if "erreur" in ins:
            err = ins["erreur"]
            ins = api(f"{m['id']}/insights", jeton, metric="plays,reach,shares,saved")
        if "erreur" not in ins:
            v = valeur(ins, "views")
            vues.append((v if v is not None else valeur(ins, "plays")) or 0)
            portee.append(valeur(ins, "reach") or 0)
            partages += valeur(ins, "shares") or 0
            enreg += valeur(ins, "saved") or 0
        aimes += m.get("like_count") or 0
        comm += m.get("comments_count") or 0
    out.append(f"publications des 30 derniers jours : {len(ms30)} (statistiques lues : {len(vues)})" + (f" — dernière erreur : {err}" if err and not vues else ""))
    if vues:
        s = sorted(vues)
        out.append(f"vues : total {sum(vues)}, moyenne {sum(vues) // len(vues)}, médiane {s[len(s) // 2]}, max {s[-1]}, min {s[0]}")
        out.append(f"comptes touchés (portée) : moyenne {sum(portee) // len(portee)} par publication")
    out.append(f"j'aime {aimes}, commentaires {comm}, partages {partages}, enregistrements {enreg}")
    compte = api(ig, jeton, fields="followers_count,media_count")
    if "erreur" not in compte:
        out.append(f"abonnés : {compte.get('followers_count')}, publications au total : {compte.get('media_count')}")
    fin = int(dt.datetime.utcnow().timestamp())
    deb = fin - 28 * 86400
    for met in ("website_clicks", "profile_links_taps", "profile_views"):
        r = api(f"{ig}/insights", jeton, metric=met, period="day", metric_type="total_value", since=deb, until=fin)
        out.append(f"{met} (28 jours) : " + (r["erreur"] if "erreur" in r else str(valeur(r, met))))
    resume(f"Instagram {nom}", out)


def facebook(nom, page, jeton):
    out = []
    p = api(page, jeton, fields="followers_count,fan_count,instagram_business_account")
    if "erreur" in p:
        resume(f"Facebook {nom}", [f"lecture impossible : {p['erreur']}"])
        return None
    out.append(f"abonnés de la page : {p.get('followers_count')} (mentions J'aime : {p.get('fan_count')})")
    depuis = int((dt.datetime.utcnow() - dt.timedelta(days=30)).timestamp())
    reels = api(f"{page}/video_reels", jeton, fields="id,created_time", since=depuis, limit=80)
    if "erreur" in reels:
        out.append(f"Reels Facebook : {reels['erreur']}")
    else:
        vs = []
        for r in reels.get("data") or []:
            ins = api(f"{r['id']}/video_insights", jeton, metric="blue_reels_play_count")
            v = None if "erreur" in ins else valeur(ins, "blue_reels_play_count")
            if v is not None:
                vs.append(v)
        n = len(reels.get("data") or [])
        out.append(f"Reels Facebook (30 jours) : {n}" + (f", vues total {sum(vs)}, moyenne {sum(vs) // len(vs)}, max {max(vs)}" if vs else ", vues non lues"))
    posts = api(f"{page}/posts", jeton, fields="id,created_time", since=depuis, limit=100)
    if "erreur" in posts:
        out.append(f"publications Facebook : {posts['erreur']}")
    else:
        imp, clics, err = [], 0, ""
        for x in posts.get("data") or []:
            ins = api(f"{x['id']}/insights", jeton, metric="post_impressions_unique,post_clicks")
            if "erreur" in ins:
                err = ins["erreur"]
            else:
                imp.append(valeur(ins, "post_impressions_unique") or 0)
                clics += valeur(ins, "post_clicks") or 0
        n = len(posts.get("data") or [])
        out.append(f"publications Facebook (30 jours) : {n}" + (f", personnes touchées total {sum(imp)}, moyenne {sum(imp) // len(imp)}, clics {clics}" if imp else f", statistiques non lues {err}"))
    resume(f"Facebook {nom}", out)
    return (p.get("instagram_business_account") or {}).get("id")


if __name__ == "__main__":
    print("Statistiques des réseaux (lecture seule), " + dt.datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC"))
    jeton = os.environ.get("FB_PAGE_TOKEN", "")
    ig = facebook("Clicvia", os.environ.get("FB_PAGE_ID", ""), jeton)
    if ig:
        instagram("@immobilier.clicvia", ig, jeton)
    j2 = os.environ.get("MONAGENT_FB_PAGE_TOKEN") or jeton
    if os.environ.get("MONAGENT_FB_PAGE_ID"):
        facebook("Mon agent", os.environ["MONAGENT_FB_PAGE_ID"], j2)
    if os.environ.get("MONAGENT_IG_USER_ID"):
        instagram("Mon agent", os.environ["MONAGENT_IG_USER_ID"], j2)
