#!/usr/bin/env python3
# Simple offline mirror for the usmanovafit GetCourse landing pages.
import os, re, sys, hashlib, urllib.parse, urllib.request, ssl, time

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
ASSETS = os.path.join(SITE, "assets")
BASE = "https://usmanovafit.gymteam.ru/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

PAGES = ["mainpage", "maysale2026_7", "oferta_fitnes", "personaldata", "protection_fitnes"]

# url -> local absolute path (already downloaded)
downloaded = {}
failed = {}

def norm(u, referer=BASE):
    u = u.strip().strip('\'"')
    if not u or u.startswith(("data:", "javascript:", "mailto:", "tel:", "#", "about:")):
        return None
    if u.startswith("//"):
        return "https:" + u
    if u.startswith(("http://", "https://")):
        return u
    return urllib.parse.urljoin(referer, u)

def local_path_for(url):
    """Map a remote URL to a local path under assets/."""
    p = urllib.parse.urlparse(url)
    host = p.netloc
    path = p.path
    if not path or path.endswith("/"):
        path += "index"
    # keep extension; disambiguate by query hash if present
    root, ext = os.path.splitext(path)
    if p.query:
        h = hashlib.md5(p.query.encode()).hexdigest()[:8]
        root = root + "_" + h
    # guess extension if missing
    if not ext:
        ext = ""
    safe = (host + root + ext)
    safe = re.sub(r"[^A-Za-z0-9_./-]", "_", safe)
    return os.path.join(ASSETS, *safe.split("/"))

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": BASE})
    with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
        return r.read(), r.headers.get_content_type()

def rel_from(page_dir, target_abs):
    return os.path.relpath(target_abs, page_dir).replace("\\", "/")

def download(url):
    if url in downloaded:
        return downloaded[url]
    if url in failed:
        return None
    lp = local_path_for(url)
    try:
        data, ctype = fetch(url)
    except Exception as e:
        failed[url] = str(e)
        print("  FAIL", url, "->", e)
        return None
    # add extension for css/js if missing based on content-type
    if not os.path.splitext(lp)[1]:
        ext = {"text/css": ".css", "application/javascript": ".js",
               "text/javascript": ".js", "image/png": ".png",
               "image/jpeg": ".jpg", "image/webp": ".webp",
               "image/svg+xml": ".svg", "image/gif": ".gif"}.get(ctype, "")
        lp += ext
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    with open(lp, "wb") as f:
        f.write(data)
    downloaded[url] = lp
    print("  ok  ", os.path.relpath(lp, SITE), f"({len(data)}b)")
    # process CSS recursively for url() and @import
    if lp.endswith(".css") or ctype == "text/css":
        process_css(lp, url)
    return lp

CSS_URL_RE = re.compile(r"""url\(\s*['"]?([^'")]+)['"]?\s*\)""", re.I)
CSS_IMPORT_RE = re.compile(r"""@import\s+['"]([^'"]+)['"]""", re.I)

def process_css(css_path, css_url):
    with open(css_path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    css_dir = os.path.dirname(css_path)
    refs = set(CSS_URL_RE.findall(text)) | set(CSS_IMPORT_RE.findall(text))
    for ref in refs:
        au = norm(ref, css_url)
        if not au:
            continue
        lp = download(au)
        if lp:
            rel = rel_from(css_dir, lp)
            text = text.replace(ref, rel)
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(text)

# Attribute patterns to rewrite in HTML
ATTR_RE = re.compile(r'''(src|href|data-src|data-original|poster)\s*=\s*(["'])(.*?)\2''', re.I)
SRCSET_RE = re.compile(r'''(srcset|data-srcset)\s*=\s*(["'])(.*?)\2''', re.I)
STYLE_URL_RE = re.compile(r'''(style\s*=\s*)(["'])(.*?)\2''', re.I | re.S)

# skip these page navigations (keep as-is or map to local pages)
PAGE_URLS = {BASE + p: p + ".html" for p in PAGES}
PAGE_URLS[BASE + "mainpage"] = "mainpage.html"

def is_asset(url):
    return bool(re.search(r'\.(css|js|png|jpe?g|webp|gif|svg|woff2?|ttf|eot|ico|mp4|webm|otf)(\?|$)', url, re.I))

def process_html(page):
    src = os.path.join(SITE, page + ".html")
    with open(src, "rb") as f:
        html = f.read().decode("utf-8", "replace")
    page_dir = SITE

    def repl_attr(m):
        attr, q, val = m.group(1), m.group(2), m.group(3)
        au = norm(val)
        if not au:
            return m.group(0)
        # internal page links -> local html
        base_noq = au.split("?")[0].rstrip("/")
        for pu, lf in PAGE_URLS.items():
            if base_noq == pu.rstrip("/"):
                return f'{attr}={q}{lf}{q}'
        if is_asset(au):
            lp = download(au)
            if lp:
                return f'{attr}={q}{rel_from(page_dir, lp)}{q}'
        return m.group(0)

    def repl_srcset(m):
        attr, q, val = m.group(1), m.group(2), m.group(3)
        parts = []
        for item in val.split(","):
            item = item.strip()
            if not item:
                continue
            bits = item.split()
            u = bits[0]
            au = norm(u)
            if au and is_asset(au):
                lp = download(au)
                if lp:
                    bits[0] = rel_from(page_dir, lp)
            parts.append(" ".join(bits))
        return f'{attr}={q}{", ".join(parts)}{q}'

    def repl_style(m):
        pre, q, val = m.group(1), m.group(2), m.group(3)
        def urlrepl(um):
            ref = um.group(1)
            au = norm(ref)
            if au and is_asset(au):
                lp = download(au)
                if lp:
                    return f'url({rel_from(page_dir, lp)})'
            return um.group(0)
        newval = CSS_URL_RE.sub(urlrepl, val)
        return f'{pre}{q}{newval}{q}'

    html = ATTR_RE.sub(repl_attr, html)
    html = SRCSET_RE.sub(repl_srcset, html)
    html = STYLE_URL_RE.sub(repl_style, html)

    # also handle url() inside inline <style>...</style> blocks
    def style_block(m):
        opening, css = m.group(1), m.group(2)
        def urlrepl(um):
            au = norm(um.group(1))
            if au and is_asset(au):
                lp = download(au)
                if lp:
                    return f'url({rel_from(page_dir, lp)})'
            return um.group(0)
        return opening + CSS_URL_RE.sub(urlrepl, css) + "</style>"
    html = re.sub(r'(<style[^>]*>)(.*?)</style>', style_block, html, flags=re.S | re.I)

    out = os.path.join(SITE, page + ".html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("written", page + ".html")

if __name__ == "__main__":
    for pg in PAGES:
        print("=== processing", pg, "===")
        process_html(pg)
    print("\nDownloaded:", len(downloaded), "| Failed:", len(failed))
    if failed:
        for u, e in list(failed.items())[:30]:
            print("FAILED:", u, e)
