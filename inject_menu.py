#!/usr/bin/env python3
# Inject the page-aware version+changes menu into ALL v1 pages.
# The menu markup is self-contained (own CSS); behaviour comes from shared site.js.
import os, re

SITE = "site"
V1_PAGES = ["mainpage.html", "maysale2026_7.html",
            "oferta_fitnes.html", "personaldata.html", "protection_fitnes.html"]

MENU = '''
<!-- site-menu: versions + changes (offline-copy author) -->
<div id="siteMenu" class="smenu">
  <button class="smenu__toggle" type="button" aria-label="Версии и правки">
    <span class="smenu__bars"><i></i><i></i><i></i></span> Версии и правки
  </button>
  <div class="smenu__panel">
    <div class="smenu__label">Версия страницы</div>
    <div class="smenu__versions">
      <a class="smenu__ver" data-v="1" href="#">V1<small>Копия оригинала</small></a>
      <a class="smenu__ver" data-v="2" href="#">V2<small>Редизайн</small></a>
    </div>
    <div class="smenu__label">Отличия от оригинала</div>
    <ul class="smenu__list">
      <li><b>Плавная прокрутка</b> по якорям страницы.</li>
      <li><b>Фикс кнопки «Выбрать программу»</b> — на оригинале ведёт на несуществующий якорь <code>#form</code>; здесь добавлен якорь.</li>
      <li><b>Починена модалка заказа</b> — на оригинале кнопки «Забрать набор» шлют форму на недоступный бэкенд; здесь показывается демо-подтверждение.</li>
      <li><b>V2 — полностью новый дизайн</b> сайта.</li>
    </ul>
  </div>
</div>
<link rel="stylesheet" href="assets/v2/menu.css">
<script src="assets/v2/site.js"></script>
'''

# remove any previously injected block. Current blocks end with the site.js
# <script>; strip through it (crossing any inline <style>). Ancient copy-note
# blocks (no script) ended at </style> — handled by the fallback alternative.
OLD_RE = re.compile(
    r'\n?<!-- (?:copy-(?:note|changes-menu)|site-menu)[^>]*-->'
    r'(?:.*?</script>|.*?</style>)\s*',
    re.S)

for p in V1_PAGES:
    fp = os.path.join(SITE, p)
    if not os.path.exists(fp):
        print("!! missing", p); continue
    s = open(fp, encoding="utf-8").read()
    # strip all previously-injected blocks (idempotent, handles multiple)
    s, n = OLD_RE.subn("\n", s)
    # sweep up any leftover artifacts from older injections (orphaned tags)
    s = re.sub(r'\n?<script src="assets/v2/site\.js"></script>\s*', '\n', s)
    s = re.sub(r'\n?<link rel="stylesheet" href="assets/v2/menu\.css">\s*', '\n', s)
    b = s.lower().rfind("</body>")
    s = (s[:b] + MENU + s[b:]) if b != -1 else (s + MENU)
    open(fp, "w", encoding="utf-8").write(s)
    print(f"{p}: removed {n} old block(s), injected menu")
print("done")
