/* USMANOVA·FIT v2 — shared interactions */
(function () {
  /* reveal on scroll */
  var rv = document.querySelectorAll('.rv');
  if (rv.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) {
      // elements taller than the viewport can never reach the 12% threshold — reveal them straight away
      if (el.offsetHeight > window.innerHeight * 0.85) { el.classList.add('in'); }
      else { io.observe(el); }
    });
    // safety net: if the observer hasn't revealed on-screen items shortly after
    // load (some mobile browsers fire it late/not at all), reveal them manually
    // so content is never stuck invisible. Below-the-fold items still animate.
    var revealVisible = function () {
      rv.forEach(function (el) {
        if (!el.classList.contains('in') && el.getBoundingClientRect().top < window.innerHeight * 0.95) {
          el.classList.add('in'); io.unobserve(el);
        }
      });
    };
    window.addEventListener('load', function () { setTimeout(revealVisible, 350); });
    setTimeout(revealVisible, 1600);
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  /* faq accordion */
  document.querySelectorAll('.acc__q').forEach(function (q) {
    q.addEventListener('click', function () { q.parentElement.classList.toggle('open'); });
  });

  /* offer countdown */
  var cd = document.querySelector('.cd[data-days]');
  if (cd) {
    var days = parseFloat(cd.getAttribute('data-days')) || 4;
    var target = new Date().getTime() + days * 864e5;
    var cells = {
      d: cd.querySelector('[data-u="d"] .cd__n'),
      h: cd.querySelector('[data-u="h"] .cd__n'),
      m: cd.querySelector('[data-u="m"] .cd__n'),
      s: cd.querySelector('[data-u="s"] .cd__n')
    };
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var tick = function () {
      var diff = Math.max(0, target - new Date().getTime());
      var t = Math.floor(diff / 1000);
      if (cells.d) cells.d.textContent = Math.floor(t / 86400);
      if (cells.h) cells.h.textContent = pad(Math.floor(t / 3600) % 24);
      if (cells.m) cells.m.textContent = pad(Math.floor(t / 60) % 60);
      if (cells.s) cells.s.textContent = pad(t % 60);
    };
    tick();
    setInterval(tick, 1000);
  }

  /* order modal (offer / tariffs page) */
  var modal = document.getElementById('orderModal');
  if (modal) {
    var lastFocus = null;
    var get = function (card, sel) {
      var el = card.querySelector(sel);
      return el ? el.textContent.trim() : '';
    };
    var openModal = function (card) {
      modal.querySelector('#orderPlan').textContent = get(card, '.tcard__name');
      modal.querySelector('#orderMeta').textContent = get(card, '.tcard__period');
      modal.querySelector('#orderNew').textContent = get(card, '.tcard__new');
      modal.querySelector('#orderOld').textContent = get(card, '.tcard__old');
      modal.querySelector('#orderDisc').textContent = get(card, '.tcard__disc');
      modal.querySelector('#okPlan').textContent = get(card, '.tcard__name');
      // reset to the order view each open
      modal.querySelector('.modal__order').hidden = false;
      modal.querySelector('.modal__success').hidden = true;
      lastFocus = document.activeElement;
      modal.hidden = false;
      void modal.offsetWidth; // force reflow so the open transition plays
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
      var f = modal.querySelector('input');
      if (f) setTimeout(function () { f.focus(); }, 60);
    };
    var closeModal = function () {
      modal.classList.remove('open');
      document.body.style.overflow = '';
      setTimeout(function () { modal.hidden = true; }, 320);
      if (lastFocus) lastFocus.focus();
    };
    document.querySelectorAll('.tcard .btn').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.preventDefault();
        var card = b.closest('.tcard');
        if (card) openModal(card);
      });
    });
    modal.querySelectorAll('[data-close]').forEach(function (el) {
      el.addEventListener('click', closeModal);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
    });
    var form = modal.querySelector('#orderForm');
    if (form) form.addEventListener('submit', function (e) {
      e.preventDefault();
      modal.querySelector('.modal__order').hidden = true;
      modal.querySelector('.modal__success').hidden = false;
    });
  }

  /* v1 original order modal (GetCourse "Забрать набор"): the checkout form
     POSTs to the live backend, which is unreachable in this offline copy — so
     the button silently does nothing. Intercept it and show a demo confirmation. */
  var GC_ACTION = /block-public\/process/;
  var gcDemoConfirm = function (form) {
    if (form.dataset.gcDemoDone) return;
    var vis = [].filter.call(
      form.querySelectorAll('input[type=text],input[type=email],input[type=tel]'),
      function (i) { return i.offsetParent !== null; });
    var empty = vis.filter(function (i) { return !i.value.trim(); });
    if (empty.length) { empty[0].style.borderColor = '#f5347f'; empty[0].focus(); return; }
    form.dataset.gcDemoDone = '1';
    var ok = document.createElement('div');
    ok.style.cssText = 'text-align:center;padding:20px 8px;font-family:inherit';
    ok.innerHTML =
      '<div style="width:58px;height:58px;margin:0 auto 14px;border-radius:50%;background:#f5347f;' +
      'display:flex;align-items:center;justify-content:center">' +
      '<svg width="30" height="30" viewBox="0 0 24 24" fill="none"><path d="M5 12.5l4.5 4.5L19 7" ' +
      'stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>' +
      '<div style="font-size:21px;font-weight:700;color:#2b241f;margin-bottom:8px">Заявка принята!</div>' +
      '<p style="color:#777;font-size:14px;line-height:1.5;margin:0">Это демонстрационная копия сайта&nbsp;— ' +
      'реальная оплата не производится.</p>';
    form.style.display = 'none';
    form.parentNode.insertBefore(ok, form);
  };
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (form && GC_ACTION.test(form.action || '')) {
      e.preventDefault(); e.stopImmediatePropagation();
      gcDemoConfirm(form);
    }
  }, true);
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('button[type=submit].f-btn, button.btn-success');
    if (!btn) return;
    var form = btn.closest('form');
    if (form && GC_ACTION.test(form.action || '')) {
      e.preventDefault(); e.stopImmediatePropagation();
      gcDemoConfirm(form);
    }
  }, true);

  /* site menu: versions + changes, page-aware */
  var m = document.getElementById('siteMenu');
  if (m) {
    var toggle = m.querySelector('.smenu__toggle');
    toggle.addEventListener('click', function (e) { e.stopPropagation(); m.classList.toggle('open'); });
    document.addEventListener('click', function (e) { if (!m.contains(e.target)) m.classList.remove('open'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') m.classList.remove('open'); });

    /* derive this page's v1/v2 counterparts from the current filename */
    var file = (location.pathname.split('/').pop() || 'index.html');
    var isV2 = /-v2\.html$/.test(file);
    var base = file.replace(/-v2\.html$/, '.html').replace(/\.html$/, '');
    if (!base || base === 'index') base = 'mainpage';
    var v1 = base + '.html';
    var v2 = base + '-v2.html';
    var links = m.querySelectorAll('.smenu__ver');
    links.forEach(function (a) {
      var v = a.dataset.v;
      a.href = (v === '2') ? v2 : v1;
      if ((v === '2') === isV2) a.classList.add('active');
    });
  }
})();
