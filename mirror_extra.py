#!/usr/bin/env python3
# Second pass: catch thumbnail-style URLs where the extension is mid-path
# (e.g. //fs-thb01.getcourse.ru/.../h/<hash>.png/s/s1200x/a/934144/sc/17)
import os, re, ssl, hashlib, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
ASSETS = os.path.join(SITE, "assets")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
PAGES = ["mainpage", "maysale2026_7", "oferta_fitnes", "personaldata", "protection_fitnes"]

# match src/href to getcourse/gymteam thumbnail or fileservice resources w/o trailing ext
URL_RE = re.compile(r'''(src|href)=(["'])((?:https?:)?//[^"']*(?:getcourse\.ru|gymteam\.ru)/[^"']*)\2''', re.I)

cache = {}
def norm(u):
    if u.startswith("//"): return "https:" + u
    return u

def local_for(url):
    p = urllib.parse.urlparse(url)
    path = p.path
    root, ext = os.path.splitext(path)
    if not ext:
        # thumbnail: extension is embedded; grab last known image ext + hash of full path
        m = re.search(r'\.(png|jpe?g|webp|gif|svg)', path, re.I)
        ext = "." + (m.group(1) if m else "png")
    h = hashlib.md5(url.encode()).hexdigest()[:10]
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", p.netloc) + "/thumb_" + h + ext
    return os.path.join(ASSETS, *safe.split("/"))

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
        return r.read()

changed = 0
for pg in PAGES:
    fp = os.path.join(SITE, pg + ".html")
    with open(fp, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    def repl(m):
        global changed
        attr, q, url = m.group(1), m.group(2), m.group(3)
        if "assets/" in url:  # already local
            return m.group(0)
        au = norm(url)
        # only fetch resources that look like media (have an image ext somewhere) and not page navigations
        if not re.search(r'\.(png|jpe?g|webp|gif|svg|woff2?|ttf|css|js|mp4)', au, re.I):
            return m.group(0)
        if au in cache:
            lp = cache[au]
        else:
            lp = local_for(au)
            try:
                data = fetch(au)
                os.makedirs(os.path.dirname(lp), exist_ok=True)
                with open(lp, "wb") as g: g.write(data)
                cache[au] = lp
                print("ok", os.path.relpath(lp, SITE))
            except Exception as e:
                print("FAIL", au, e); return m.group(0)
        rel = os.path.relpath(lp, SITE).replace("\\", "/")
        changed += 1
        return f'{attr}={q}{rel}{q}'
    html2 = URL_RE.sub(repl, html)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html2)
print("total rewrites:", changed)
