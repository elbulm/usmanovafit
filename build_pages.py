#!/usr/bin/env python3
# Build v2 versions of maysale + legal pages, reusing the shared v2 design system.
import json, os, re

SITE = "site"

def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="assets/v2/style.css">
</head>
<body>'''

def topbar():
    return '''
<header class="wrap topbar">
  <a href="mainpage-v2.html" class="brand">USMANOVA<span>·</span>FIT</a>
  <nav class="topbar__cta">
    <a href="mainpage-v2.html#programs" class="topbar__link">Программы</a>
    <a href="mainpage-v2.html#about" class="topbar__link">О тренере</a>
    <a href="mainpage-v2.html#faq" class="topbar__link">Вопросы</a>
    <a href="maysale2026_7-v2.html" class="btn btn--flame" style="padding:.7em 1.2em; font-size:.92rem">Выбрать программу</a>
  </nav>
</header>'''

def footer():
    return '''
<footer class="foot">
  <div class="wrap">
    <div class="foot__top">
      <div class="foot__brand">USMANOVA<span>·</span>FIT</div>
      <nav class="foot__links">
        <a href="mainpage-v2.html#programs">Программы</a>
        <a href="mainpage-v2.html#about">О тренере</a>
        <a href="mainpage-v2.html#faq">Вопросы</a>
        <a href="oferta_fitnes-v2.html">Оферта</a>
        <a href="personaldata-v2.html">Персональные данные</a>
        <a href="protection_fitnes-v2.html">Защита данных</a>
      </nav>
    </div>
    <div class="foot__legal">
      Локальная демонстрационная копия сайта usmanovafit.gymteam.ru. Версия&nbsp;2 — независимый редизайн в учебных целях. Все тексты, фотографии и названия программ принадлежат правообладателю.
    </div>
  </div>
</footer>'''

def menu():
    return '''
<!-- site-menu: versions + changes -->
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
      <li><b>Фикс кнопки «Выбрать программу»</b> — на оригинале ведёт на несуществующий якорь <code>#form</code>.</li>
      <li><b>V2 — полностью новый дизайн</b> сайта.</li>
    </ul>
  </div>
</div>
<script src="assets/v2/site.js"></script>
</body>
</html>'''

# ---------------- MAYSALE v2 ----------------
def build_maysale():
    tariffs = [
      {"name":"Лёгкий старт","flag":None,"feat":False,"new":"3 140 ₽","old":"6 400 ₽","disc":"−51%","period":"Доступ: 2 месяца",
       "items":["Обновлённый Метод: 20 тренировок, питание по неделям, растяжка и восстановление",
                "5 лекций по питанию: уходит тяга к сладкому"]},
      {"name":"Преображение","flag":"Выбор большинства","feat":True,"new":"5 490 ₽","old":"22 380 ₽","disc":"−75%","period":"Доступ: 3 месяца",
       "items":["Всё из «Лёгкого старта»",
                "Курс питания с Вероникой Гусаковой: 42 урока без диет",
                "5 тренировок Стаса Свободы: плоский живот и осанка через дыхание"]},
      {"name":"Максимум","flag":"Максимальный результат","feat":False,"new":"6 890 ₽","old":"37 280 ₽","disc":"−82%","period":"Доступ: 6 месяцев",
       "items":["Всё из «Преображения»",
                "Курс «Жиросжигающий»: три уровня по 45 дней на максимальное жиросжигание"]},
    ]
    tcards=[]
    for t in tariffs:
        flag = f'<div class="tcard__flag">{t["flag"]}</div>' if t["flag"] else ""
        feat = " tcard--feat" if t["feat"] else ""
        items = "".join(f"<li>{i}</li>" for i in t["items"])
        btn = "btn--flame" if t["feat"] else "btn--bone" if False else "btn--flame"
        btn = "btn--flame"
        tcards.append(f'''
    <div class="tcard{feat} rv">{flag}
      <div class="tcard__name">{t["name"]}</div>
      <div class="tcard__period">{t["period"]}</div>
      <div class="tcard__price"><span class="tcard__new">{t["new"]}</span><span class="tcard__old">{t["old"]}</span></div>
      <div class="tcard__disc">Скидка {t["disc"]}</div>
      <ul class="tfeat">{items}</ul>
      <a href="#" class="btn {btn}">Забрать набор <span class="btn__arrow">→</span></a>
    </div>''')
    body=f'''
<section class="offer-hero wrap">
  <div class="offer-hero__grid">
    <div>
      <p class="eyebrow rv">Метод Усмановой · обновлённая программа</p>
      <h1 class="rv" style="margin-top:1rem">За лето верните<br><span class="flame">лёгкость,</span> энергию<br>и форму</h1>
      <p class="offer-hero__lead rv rv-d1">Домашние тренировки с Катей и готовое питание по неделям возвращают лёгкость, подтягивают тело и превращают спорт в удовольствие.</p>
      <div class="countdown rv rv-d1">
        <span class="countdown__lbl">Успейте забрать тренировки со скидкой до 82%</span>
        <div class="cd" data-days="4">
          <div class="cd__cell" data-u="d"><div class="cd__n">4</div><div class="cd__u">дня</div></div>
          <div class="cd__cell" data-u="h"><div class="cd__n">01</div><div class="cd__u">часов</div></div>
          <div class="cd__cell" data-u="m"><div class="cd__n">17</div><div class="cd__u">минут</div></div>
          <div class="cd__cell" data-u="s"><div class="cd__n">08</div><div class="cd__u">секунд</div></div>
        </div>
      </div>
      <div class="hero__actions rv rv-d2" style="margin-top:1.8rem">
        <a href="#tariffs" class="btn btn--flame">Получить метод <span class="btn__arrow">→</span></a>
      </div>
    </div>
    <div class="offer-hero__media rv rv-d1">
      <div class="hero__blob"></div>
      <img class="offer-hero__ph" src="assets/fs-thb01.getcourse.ru/thumb_481964f1ff.png" alt="Катя Усманова">
    </div>
  </div>
</section>

<div class="marq" aria-hidden="true"><div class="marq__row">
  <span>−82% до конца лета</span><span>20 тренировок</span><span>питание по неделям</span><span>растяжка</span><span>без диет</span><span>рассрочка</span>
  <span>−82% до конца лета</span><span>20 тренировок</span><span>питание по неделям</span><span>растяжка</span><span>без диет</span><span>рассрочка</span>
</div></div>

<section class="tariffs wrap" id="tariffs">
  <a id="form" style="position:relative; top:-90px"></a>
  <div class="sec-head">
    <h2 class="rv">Выберите формат и начните сегодня</h2>
    <p class="rv rv-d1">Чем раньше старт, тем больше успеете до конца лета. Цены вырастут после окончания акции.</p>
  </div>
  <div class="tgrid">{"".join(tcards)}</div>
  <div class="guar">
    <div class="guar__i rv"><span>Рассрочка</span> без переплат</div>
    <div class="guar__i rv rv-d1"><span>Оплата</span> картами РФ и других стран</div>
    <div class="guar__i rv rv-d2"><span>Доступ</span> сразу после оплаты</div>
    <div class="guar__i rv rv-d3"><span>Занятия</span> дома, 20–45 минут</div>
  </div>
</section>

<section class="final">
  <div class="wrap">
    <h2 class="rv">Лето — лучшее время начать</h2>
    <p class="rv rv-d1">Заберите обновлённый Метод Усмановой со скидкой, пока действует акция, и занимайтесь в своём темпе.</p>
    <a href="#tariffs" class="btn btn--bone rv rv-d1">Получить метод <span class="btn__arrow">→</span></a>
    <small class="rv rv-d2">Более 580 000 участниц уже тренируются с Катей</small>
  </div>
</section>'''
    return head("USMANOVA·FIT — Метод Усмановой со скидкой до 82%",
                "Обновлённый Метод Усмановой: домашние тренировки и питание. Успейте забрать со скидкой до 82%.") \
           + topbar() + body + footer() + menu()

# ---------------- LEGAL v2 ----------------
def render_legal(els):
    """turn [(tag,text)] into html, grouping consecutive li into ul; first heading is the page title."""
    title = None; rest = []
    for i,(tag,txt) in enumerate(els):
        if title is None and tag in ("h1","h2","h3","h4"):
            title = txt; rest = els[i+1:]; break
    if title is None:
        title = None; rest = els
    out=[]; buf=[]
    def flush():
        if buf: out.append("<ul>"+"".join(f"<li>{x}</li>" for x in buf)+"</ul>"); buf.clear()
    for tag,txt in rest:
        if tag=="li": buf.append(txt); continue
        flush()
        if tag in ("h1","h2"): out.append(f"<h2>{txt}</h2>")
        elif tag in ("h3","h4"): out.append(f"<h3>{txt}</h3>")
        else: out.append(f"<p>{txt}</p>")
    flush()
    return title, "\n".join(out)

def build_legal(key, page_title, eyebrow, fallback_h1):
    data=json.load(open("scratch_legal.json",encoding="utf-8"))
    title, doc = render_legal(data[key])
    h1 = title or fallback_h1
    body=f'''
<section class="legal">
  <div class="legal__head">
    <p class="legal__eyebrow rv">{eyebrow}</p>
    <h1 class="rv rv-d1">{h1}</h1>
  </div>
  <article class="legal__doc">
{doc}
  </article>
</section>'''
    return head(page_title, eyebrow) + topbar() + body + footer() + menu()

# ---------------- write all ----------------
pages = {
  "maysale2026_7-v2.html": build_maysale(),
  "oferta_fitnes-v2.html": build_legal("oferta_fitnes","USMANOVA·FIT — Договор оферты","Юридические документы","Договор публичной оферты"),
  "personaldata-v2.html": build_legal("personaldata","USMANOVA·FIT — Согласие на обработку персональных данных","Юридические документы","Согласие на обработку персональных данных"),
  "protection_fitnes-v2.html": build_legal("protection_fitnes","USMANOVA·FIT — Политика защиты персональных данных","Юридические документы","Политика в отношении обработки персональных данных"),
}
for fn, html in pages.items():
    open(os.path.join(SITE, fn), "w", encoding="utf-8").write(html)
    print("wrote", fn, f"({len(html)} chars)")
print("done")
