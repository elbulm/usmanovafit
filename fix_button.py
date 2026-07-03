#!/usr/bin/env python3
# Variant A: give the broken `#form` CTA buttons a real target anchor,
# and add a small honest "liberty taken" notice in the corner.
import os

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

ANCHOR = '<div id="form" class="copy-added-anchor" style="scroll-margin-top:90px"></div>\n'

# page -> marker string to insert the anchor *before* (first occurrence)
TARGETS = {
    "mainpage.html": '<div class="marathon-screen">',      # programs showcase
    "maysale2026_7.html": '<div class="tariff-card2">',     # tariff selection
}

NOTICE = '''
<!-- copy-note: added by the offline-copy author -->
<div id="copyNote" class="copy-note">
  <button class="copy-note__close" onclick="var n=document.getElementById('copyNote'); n.parentNode.removeChild(n);" aria-label="Закрыть">&times;</button>
  <div class="copy-note__text">
    На оригинальном сайте кнопка «Выбрать программу» не работает (ведёт на несуществующий якорь&nbsp;<code>#form</code>).
    В этой копии я допустил вольность и добавил ей функциональность&nbsp;— теперь она прокручивает к выбору&nbsp;программ.
  </div>
</div>
<style>
  .copy-note{
    position:fixed; left:16px; bottom:16px; z-index:99999;
    max-width:300px; padding:14px 34px 14px 16px;
    background:#fff; color:#333; border:1px solid #ffd0e2;
    border-left:4px solid #f5347f; border-radius:10px;
    box-shadow:0 8px 28px rgba(0,0,0,.16);
    font-family:"ALS Granate VF",Arial,sans-serif; font-size:13px; line-height:1.45;
  }
  .copy-note code{ background:#fdeaf2; color:#f5347f; padding:1px 5px; border-radius:4px; font-size:12px; }
  .copy-note__close{
    position:absolute; top:6px; right:8px; border:0; background:transparent;
    font-size:20px; line-height:1; color:#aaa; cursor:pointer; padding:0;
  }
  .copy-note__close:hover{ color:#f5347f; }
  @media (max-width:520px){ .copy-note{ left:10px; right:10px; bottom:10px; max-width:none; } }
</style>
'''

for page, marker in TARGETS.items():
    fp = os.path.join(SITE, page)
    html = open(fp, encoding="utf-8").read()

    # 1) insert anchor before the first target block (only if not already added)
    if 'id="form"' not in html:
        idx = html.find(marker)
        if idx == -1:
            print("!! marker not found in", page, "->", marker)
        else:
            html = html[:idx] + ANCHOR + html[idx:]
            print("anchor added to", page, "before", marker)
    else:
        print("anchor already present in", page)

    # 2) insert the corner notice before </body> (once)
    if 'id="copyNote"' not in html:
        low = html.lower()
        bidx = low.rfind("</body>")
        if bidx == -1:
            html = html + NOTICE
        else:
            html = html[:bidx] + NOTICE + html[bidx:]
        print("notice added to", page)
    else:
        print("notice already present in", page)

    open(fp, "w", encoding="utf-8").write(html)

print("done")
