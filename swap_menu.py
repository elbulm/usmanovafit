#!/usr/bin/env python3
# Replace the "liberty" corner notice with a top-left changes menu.
# Preserves the smooth-scroll rule (it lived inside the old notice styles).
import os, re

SITE = "site"

MENU = '''
<!-- copy-changes-menu: added by the offline-copy author -->
<div id="copyMenu" class="copy-menu">
  <button class="copy-menu__btn" type="button"
          onclick="document.getElementById('copyMenu').classList.toggle('open')"
          aria-label="Список изменений копии">
    <span class="copy-menu__bars" aria-hidden="true"><span></span><span></span><span></span></span>
    <span class="copy-menu__label">Изменения</span>
  </button>
  <div class="copy-menu__panel">
    <div class="copy-menu__title">Отличия копии от оригинала</div>
    <ul class="copy-menu__list">
      <li><b>Плавная прокрутка.</b> Переходы по якорям страницы теперь анимированы.</li>
      <li><b>Фикс кнопки «Выбрать программу».</b> На оригинале она ведёт на несуществующий якорь <code>#form</code> и не работает&nbsp;— здесь добавлен якорь, и кнопка плавно прокручивает к&nbsp;выбору&nbsp;программ.</li>
    </ul>
    <div class="copy-menu__note">Локальная копия сайта · внесённые вольности</div>
  </div>
</div>
<style>
  html{ scroll-behavior:smooth; }
  .copy-menu{ position:fixed; top:16px; left:16px; z-index:99999;
    font-family:"ALS Granate VF",Arial,sans-serif; }
  .copy-menu__btn{ display:flex; align-items:center; gap:9px; padding:9px 14px;
    background:#f5347f; color:#fff; border:0; border-radius:9px;
    font-size:13px; font-weight:600; cursor:pointer;
    box-shadow:0 6px 20px rgba(245,52,127,.35); transition:background .15s; }
  .copy-menu__btn:hover{ background:#e01f6c; }
  .copy-menu__bars{ display:inline-flex; flex-direction:column; gap:3px; width:16px; }
  .copy-menu__bars span{ display:block; height:2px; background:#fff; border-radius:2px; transition:.2s; }
  .copy-menu.open .copy-menu__bars span:nth-child(1){ transform:translateY(5px) rotate(45deg); }
  .copy-menu.open .copy-menu__bars span:nth-child(2){ opacity:0; }
  .copy-menu.open .copy-menu__bars span:nth-child(3){ transform:translateY(-5px) rotate(-45deg); }
  .copy-menu__panel{ display:none; margin-top:10px; width:330px;
    max-width:calc(100vw - 32px); padding:16px 18px;
    background:#fff; color:#333; border:1px solid #ffd0e2; border-radius:12px;
    box-shadow:0 14px 36px rgba(0,0,0,.18); font-size:13px; line-height:1.5; }
  .copy-menu.open .copy-menu__panel{ display:block; animation:copyMenuIn .18s ease; }
  @keyframes copyMenuIn{ from{ opacity:0; transform:translateY(-6px); } to{ opacity:1; transform:none; } }
  .copy-menu__title{ font-size:14px; font-weight:700; color:#f5347f; margin-bottom:10px; }
  .copy-menu__list{ margin:0; padding-left:18px; }
  .copy-menu__list li{ margin-bottom:9px; }
  .copy-menu__list li:last-child{ margin-bottom:0; }
  .copy-menu__list code{ background:#fdeaf2; color:#f5347f; padding:1px 5px;
    border-radius:4px; font-size:12px; }
  .copy-menu__note{ margin-top:12px; padding-top:10px; border-top:1px solid #f2f2f2;
    color:#aaa; font-size:11px; }
</style>
'''

# match the old notice block: from its comment through the first </style> after it
OLD_RE = re.compile(
    r'\n?<!-- copy-note: added by the offline-copy author -->.*?</style>\s*',
    re.S)

for p in ["mainpage.html", "maysale2026_7.html"]:
    fp = os.path.join(SITE, p)
    s = open(fp, encoding="utf-8").read()
    if "id=\"copyMenu\"" in s:
        print("menu already present:", p); continue
    if not OLD_RE.search(s):
        print("!! old notice block not found in", p); continue
    s = OLD_RE.sub("\n", s, count=1)
    # insert new menu before </body>
    low = s.lower(); b = low.rfind("</body>")
    s = (s[:b] + MENU + s[b:]) if b != -1 else (s + MENU)
    open(fp, "w", encoding="utf-8").write(s)
    print("swapped in", p)
print("done")
