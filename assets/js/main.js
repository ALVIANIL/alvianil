/* =========================================================
   Alvi Ibn Amzad Anil - Portfolio
   Vanilla JS: no dependencies, no build step.
   ========================================================= */
(function () {
  'use strict';

  /* ---------------------------------------------------------
     0. EDIT ME - paste your profile links between the quotes.
        Leave a value as "" and the button stays inactive.
     --------------------------------------------------------- */
  var PROFILES = {
    linkedin:     'https://www.linkedin.com/in/alvi-ibn-amzad-anil',
    researchgate: 'https://www.researchgate.net/profile/Alvi-Anil',
    scholar:      'https://scholar.google.com/citations?user=wTuQGOcAAAAJ',
    github:       'https://github.com/ALVIANIL',
    certificate:  ''    // see the note below
  };

  /*  The certificate link is intentionally blank. The URL in the CV was a temporary
      LinkedIn CDN link (media.licdn.com/...?e=1784970000) that expired on 25 Jul 2026,
      so it would fail for visitors. To restore it permanently, drop the certificate
      file into assets/files/ and set:
          certificate: 'assets/files/neural-semiconductor-certificate.pdf'
      Any value left as '' keeps the link visible but inactive.                       */

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var coarsePointer = window.matchMedia('(pointer: coarse)').matches;

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  /* =========================================================
     1. Toast helper
     ========================================================= */
  var toastEl = $('#toast');
  var toastTimer = null;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('is-on');
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function () {
      toastEl.classList.remove('is-on');
    }, 3200);
  }

  /* =========================================================
     2. Profile links
     ========================================================= */
  (function wireProfiles() {
    $$('.js-profile').forEach(function (el) {
      var key = el.getAttribute('data-profile');
      var url = PROFILES[key];
      if (url) {
        el.setAttribute('href', url);
        el.setAttribute('target', '_blank');
        el.setAttribute('rel', 'noopener noreferrer');
      } else {
        el.setAttribute('data-unset', 'true');
        el.addEventListener('click', function (e) {
          e.preventDefault();
          toast('Link not set yet — add your ' + key + ' URL at the top of assets/js/main.js');
        });
      }
    });
  })();

  /* =========================================================
     3. Navigation: sticky state, mobile drawer, scroll spy
     ========================================================= */
  var nav = $('#siteNav');
  var navLinksWrap = $('#navLinks');
  var burger = $('#navBurger');
  var scrim = $('#navScrim');
  var navLinks = $$('.nav__link');
  var sections = navLinks
    .map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); })
    .filter(Boolean);

  function openMenu(open) {
    if (!navLinksWrap || !burger) return;
    navLinksWrap.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (scrim) scrim.hidden = !open;
    document.body.style.overflow = open ? 'hidden' : '';
  }

  if (burger) {
    burger.addEventListener('click', function () {
      openMenu(burger.getAttribute('aria-expanded') !== 'true');
    });
  }
  if (scrim) scrim.addEventListener('click', function () { openMenu(false); });
  navLinks.forEach(function (a) {
    a.addEventListener('click', function () { openMenu(false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') openMenu(false);
  });
  window.addEventListener('resize', function () {
    if (window.innerWidth > 900) openMenu(false);
  });

  /* progress bar + sticky nav + scroll spy + back-to-top */
  var progressBar = $('#progressBar');
  var toTop = $('#toTop');
  var ticking = false;

  function onScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;

    if (nav) nav.classList.toggle('is-stuck', y > 12);

    if (progressBar) {
      var docH = document.documentElement.scrollHeight - window.innerHeight;
      var pct = docH > 0 ? (y / docH) * 100 : 0;
      progressBar.style.width = Math.max(0, Math.min(100, pct)) + '%';
    }

    if (toTop) {
      var show = y > window.innerHeight * 0.75;
      if (show === toTop.hidden) toTop.hidden = !show;
    }

    var threshold = (nav ? nav.offsetHeight : 68) + 48;
    var currentId = '';
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].getBoundingClientRect().top <= threshold) currentId = sections[i].id;
    }
    navLinks.forEach(function (a) {
      a.classList.toggle('is-active', a.getAttribute('href') === '#' + currentId);
    });

    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(onScroll);
    }
  }, { passive: true });

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }

  /* =========================================================
     4. Reveal on scroll
     ========================================================= */
  var revealItems = $$('.reveal');

  if (!('IntersectionObserver' in window) || reduceMotion) {
    revealItems.forEach(function (el) { el.classList.add('is-visible'); });
    startCounters(document);
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        startCounters(entry.target);
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

    revealItems.forEach(function (el) { io.observe(el); });
  }

  /* =========================================================
     5. Number counters
     ========================================================= */
  function startCounters(scope) {
    var nodes = scope.querySelectorAll ? scope.querySelectorAll('.count') : [];
    Array.prototype.forEach.call(nodes, function (node) {
      if (node.getAttribute('data-done') === '1') return;
      node.setAttribute('data-done', '1');

      var target = parseFloat(node.getAttribute('data-to')) || 0;
      var dec = parseInt(node.getAttribute('data-dec'), 10) || 0;

      if (reduceMotion) {
        node.textContent = target.toFixed(dec);
        return;
      }

      var duration = 1500;
      var start = null;

      function step(ts) {
        if (start === null) start = ts;
        var p = Math.min(1, (ts - start) / duration);
        var eased = 1 - Math.pow(1 - p, 3);
        node.textContent = (target * eased).toFixed(dec);
        if (p < 1) window.requestAnimationFrame(step);
        else node.textContent = target.toFixed(dec);
      }
      window.requestAnimationFrame(step);
    });
  }

  /* =========================================================
     6. Typed role line
     ========================================================= */
  (function typewriter() {
    var el = $('#typed');
    if (!el) return;

    var phrases = [
      'Research Assistant, BRAC University',
      'Machine Learning & Computer Vision',
      'Distributed Sensing & Edge Computing',
      'Biomedical AI & Wearable Systems',
      'Author of six Q1 journal papers'
    ];

    if (reduceMotion) {
      el.textContent = phrases[0];
      return;
    }

    var pi = 0, ci = 0, deleting = false;
    el.textContent = '';

    function tick() {
      var full = phrases[pi];
      ci += deleting ? -1 : 1;
      if (ci < 0) ci = 0;
      if (ci > full.length) ci = full.length;
      el.textContent = full.slice(0, ci);

      var delay = deleting ? 34 : 62;
      if (!deleting && ci === full.length) {
        deleting = true;
        delay = 1900;
      } else if (deleting && ci === 0) {
        deleting = false;
        pi = (pi + 1) % phrases.length;
        delay = 420;
      }
      window.setTimeout(tick, delay);
    }
    window.setTimeout(tick, 700);
  })();

  /* =========================================================
     7. Animated PCB background
     ========================================================= */
  (function circuitBackground() {
    var canvas = $('#circuit');
    if (!canvas || reduceMotion) return;

    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var offscreen = document.createElement('canvas');
    var offCtx = offscreen.getContext('2d');
    if (!offCtx) return;

    var W = 0, H = 0, dpr = 1;
    var traces = [];
    var pulses = [];
    var rafId = 0;
    var lastTs = 0;
    var resizeTimer = null;

    var COLORS = [[14, 156, 143], [47, 111, 237], [224, 138, 30]];

    function rnd(min, max) { return min + Math.random() * (max - min); }

    function buildTrace() {
      var step = 30;
      var pts = [];
      var x = Math.round(rnd(0, W) / step) * step;
      var y = Math.round(rnd(0, H) / step) * step;
      pts.push({ x: x, y: y });

      var dirs = [
        [1, 0], [-1, 0], [0, 1], [0, -1],
        [0.7071, 0.7071], [-0.7071, 0.7071], [0.7071, -0.7071], [-0.7071, -0.7071]
      ];
      var d = dirs[Math.floor(rnd(0, 4))];
      var segCount = 3 + Math.floor(rnd(0, 4));

      for (var i = 0; i < segCount; i++) {
        var len = step * (2 + Math.floor(rnd(0, 6)));
        x = Math.max(-60, Math.min(W + 60, x + d[0] * len));
        y = Math.max(-60, Math.min(H + 60, y + d[1] * len));
        pts.push({ x: x, y: y });
        d = dirs[Math.floor(rnd(0, dirs.length))];
      }

      // drop zero-length segments, measure the rest
      var clean = [pts[0]];
      var lens = [];
      var total = 0;
      for (var j = 1; j < pts.length; j++) {
        var a = clean[clean.length - 1];
        var b = pts[j];
        var L = Math.hypot(b.x - a.x, b.y - a.y);
        if (L < 1) continue;
        clean.push(b);
        lens.push(L);
        total += L;
      }
      if (lens.length === 0) return null;
      return { pts: clean, lens: lens, total: total };
    }

    function pointAt(tr, dist) {
      if (dist <= 0) return { x: tr.pts[0].x, y: tr.pts[0].y };
      var acc = 0;
      for (var i = 0; i < tr.lens.length; i++) {
        var L = tr.lens[i];
        if (acc + L >= dist) {
          var t = (dist - acc) / L;
          var a = tr.pts[i], b = tr.pts[i + 1];
          return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t };
        }
        acc += L;
      }
      var last = tr.pts[tr.pts.length - 1];
      return { x: last.x, y: last.y };
    }

    function paintStatic() {
      offCtx.setTransform(1, 0, 0, 1, 0, 0);
      offCtx.clearRect(0, 0, offscreen.width, offscreen.height);
      offCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
      offCtx.lineCap = 'round';
      offCtx.lineJoin = 'round';

      traces.forEach(function (tr, idx) {
        offCtx.beginPath();
        offCtx.moveTo(tr.pts[0].x, tr.pts[0].y);
        for (var i = 1; i < tr.pts.length; i++) offCtx.lineTo(tr.pts[i].x, tr.pts[i].y);
        offCtx.lineWidth = 1.6;
        offCtx.strokeStyle = idx % 3 === 0
          ? 'rgba(47,111,237,0.11)'
          : (idx % 3 === 1 ? 'rgba(14,156,143,0.14)' : 'rgba(224,138,30,0.10)');
        offCtx.stroke();

        // solder pads at both ends
        [tr.pts[0], tr.pts[tr.pts.length - 1]].forEach(function (p) {
          offCtx.beginPath();
          offCtx.arc(p.x, p.y, 3.4, 0, Math.PI * 2);
          offCtx.fillStyle = 'rgba(255,255,255,0.9)';
          offCtx.fill();
          offCtx.lineWidth = 1.6;
          offCtx.strokeStyle = 'rgba(120,155,180,0.30)';
          offCtx.stroke();
        });

        // via at a mid vertex
        if (tr.pts.length > 2) {
          var m = tr.pts[Math.floor(tr.pts.length / 2)];
          offCtx.beginPath();
          offCtx.arc(m.x, m.y, 1.9, 0, Math.PI * 2);
          offCtx.fillStyle = 'rgba(120,155,180,0.28)';
          offCtx.fill();
        }
      });
    }

    function spawnPulse(p) {
      var tr = Math.floor(rnd(0, traces.length));
      p.t = tr;
      p.d = -rnd(0, 260);
      p.speed = rnd(70, 190);
      p.len = rnd(52, 130);
      p.c = COLORS[Math.floor(rnd(0, COLORS.length))];
      p.a = rnd(0.35, 0.75);
      return p;
    }

    function build() {
      var area = W * H;
      var count = Math.max(10, Math.min(34, Math.round(area / 42000)));
      traces = [];
      for (var i = 0; i < count; i++) {
        var tr = buildTrace();
        if (tr) traces.push(tr);
      }
      if (traces.length === 0) return;

      var pulseCount = Math.max(5, Math.min(15, Math.round(traces.length * 0.5)));
      pulses = [];
      for (var j = 0; j < pulseCount; j++) pulses.push(spawnPulse({}));

      paintStatic();
    }

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = window.innerWidth;
      H = window.innerHeight;

      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
      canvas.style.width = W + 'px';
      canvas.style.height = H + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      offscreen.width = canvas.width;
      offscreen.height = canvas.height;

      build();
    }

    function frame(ts) {
      rafId = window.requestAnimationFrame(frame);
      if (document.hidden || traces.length === 0) { lastTs = ts; return; }

      var dt = lastTs ? Math.min((ts - lastTs) / 1000, 0.05) : 0.016;
      lastTs = ts;

      ctx.clearRect(0, 0, W, H);
      ctx.drawImage(offscreen, 0, 0, W, H);

      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      for (var i = 0; i < pulses.length; i++) {
        var p = pulses[i];
        var tr = traces[p.t];
        if (!tr) { spawnPulse(p); continue; }

        p.d += p.speed * dt;
        if (p.d - p.len > tr.total) { spawnPulse(p); continue; }
        if (p.d <= 0) continue;

        var head = Math.min(p.d, tr.total);
        var tail = Math.max(0, head - p.len);
        var p0 = pointAt(tr, tail);
        var p1 = pointAt(tr, head);
        var rgb = p.c[0] + ',' + p.c[1] + ',' + p.c[2];

        var grad = ctx.createLinearGradient(p0.x, p0.y, p1.x, p1.y);
        grad.addColorStop(0, 'rgba(' + rgb + ',0)');
        grad.addColorStop(1, 'rgba(' + rgb + ',' + p.a.toFixed(2) + ')');

        ctx.beginPath();
        ctx.moveTo(p0.x, p0.y);
        var acc = 0;
        for (var s = 0; s < tr.lens.length; s++) {
          acc += tr.lens[s];
          if (acc > tail && acc < head) ctx.lineTo(tr.pts[s + 1].x, tr.pts[s + 1].y);
        }
        ctx.lineTo(p1.x, p1.y);
        ctx.strokeStyle = grad;
        ctx.lineWidth = 2.1;
        ctx.stroke();

        // glowing head
        var halo = ctx.createRadialGradient(p1.x, p1.y, 0, p1.x, p1.y, 11);
        halo.addColorStop(0, 'rgba(' + rgb + ',' + (p.a * 0.55).toFixed(2) + ')');
        halo.addColorStop(1, 'rgba(' + rgb + ',0)');
        ctx.beginPath();
        ctx.arc(p1.x, p1.y, 11, 0, Math.PI * 2);
        ctx.fillStyle = halo;
        ctx.fill();

        ctx.beginPath();
        ctx.arc(p1.x, p1.y, 2.2, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + rgb + ',' + Math.min(1, p.a + 0.2).toFixed(2) + ')';
        ctx.fill();
      }
    }

    window.addEventListener('resize', function () {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(resize, 200);
    });

    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) lastTs = 0;
    });

    resize();
    rafId = window.requestAnimationFrame(frame);
  })();

  /* =========================================================
     8. Oscilloscope readout
     ========================================================= */
  (function oscilloscope() {
    var canvas = $('#scope');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var W = 0, H = 0, dpr = 1, phase = 0, lastTs = 0, resizeTimer = null;

    function resize() {
      var rect = canvas.getBoundingClientRect();
      if (rect.width === 0) return;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = rect.width;
      H = rect.height || 104;
      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      draw();
    }

    function wave(x, t) {
      var k = x * 0.032;
      return 0.52 * Math.sin(k + t * 1.9)
           + 0.26 * Math.sin(k * 2.4 + t * 2.7)
           + 0.13 * Math.sin(k * 4.7 - t * 1.4)
           + 0.07 * Math.sin(k * 9.1 + t * 3.6);
    }

    function draw() {
      if (W === 0) return;
      ctx.clearRect(0, 0, W, H);

      // grid
      ctx.lineWidth = 1;
      ctx.strokeStyle = 'rgba(120,155,180,0.16)';
      ctx.beginPath();
      for (var gx = 0; gx <= W; gx += 26) { ctx.moveTo(gx + 0.5, 0); ctx.lineTo(gx + 0.5, H); }
      for (var gy = 0; gy <= H; gy += 26) { ctx.moveTo(0, gy + 0.5); ctx.lineTo(W, gy + 0.5); }
      ctx.stroke();

      // centre line
      ctx.beginPath();
      ctx.setLineDash([4, 6]);
      ctx.strokeStyle = 'rgba(120,155,180,0.32)';
      ctx.moveTo(0, H / 2);
      ctx.lineTo(W, H / 2);
      ctx.stroke();
      ctx.setLineDash([]);

      var amp = H * 0.33;
      var mid = H / 2;
      var pts = [];
      for (var x = 0; x <= W; x += 2) pts.push([x, mid - wave(x, phase) * amp]);

      // filled area
      var fill = ctx.createLinearGradient(0, 0, 0, H);
      fill.addColorStop(0, 'rgba(14,156,143,0.20)');
      fill.addColorStop(1, 'rgba(14,156,143,0.01)');
      ctx.beginPath();
      ctx.moveTo(0, mid);
      pts.forEach(function (p) { ctx.lineTo(p[0], p[1]); });
      ctx.lineTo(W, mid);
      ctx.closePath();
      ctx.fillStyle = fill;
      ctx.fill();

      // trace
      ctx.beginPath();
      pts.forEach(function (p, i) { i === 0 ? ctx.moveTo(p[0], p[1]) : ctx.lineTo(p[0], p[1]); });
      ctx.lineWidth = 2;
      ctx.lineJoin = 'round';
      ctx.strokeStyle = '#0e9c8f';
      ctx.stroke();

      // leading marker
      var last = pts[pts.length - 1];
      if (last) {
        ctx.beginPath();
        ctx.arc(last[0] - 1, last[1], 3.2, 0, Math.PI * 2);
        ctx.fillStyle = '#e08a1e';
        ctx.fill();
      }
    }

    function frame(ts) {
      window.requestAnimationFrame(frame);
      if (document.hidden) { lastTs = ts; return; }
      var dt = lastTs ? Math.min((ts - lastTs) / 1000, 0.05) : 0.016;
      lastTs = ts;
      phase += dt * 1.6;
      draw();
    }

    window.addEventListener('resize', function () {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(resize, 160);
    });

    resize();
    if (reduceMotion) { draw(); } else { window.requestAnimationFrame(frame); }

    // sample-rate readout
    var hzEl = $('#scopeHz');
    if (hzEl && !reduceMotion) {
      var rates = ['128 Hz', '256 Hz', '512 Hz', '250 Hz'];
      var ri = 0;
      window.setInterval(function () {
        ri = (ri + 1) % rates.length;
        hzEl.textContent = rates[ri];
      }, 3400);
    }
  })();

  /* =========================================================
     9. Publication filters
     ========================================================= */
  (function pubFilters() {
    var buttons = $$('.filter');
    var pubs = $$('#pubList .pub');
    var empty = $('#pubEmpty');
    if (buttons.length === 0 || pubs.length === 0) return;

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var mode = btn.getAttribute('data-filter');

        buttons.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');

        var shown = 0;
        pubs.forEach(function (pub) {
          var match = mode === 'all' || pub.getAttribute('data-role') === mode;
          pub.classList.toggle('is-hidden', !match);
          if (match) {
            shown++;
            pub.classList.remove('is-anim');
            void pub.offsetWidth;            // restart the entry animation
            if (!reduceMotion) pub.classList.add('is-anim');
          }
        });

        if (empty) empty.hidden = shown !== 0;
      });
    });

    document.addEventListener('animationend', function (e) {
      if (e.target.classList && e.target.classList.contains('is-anim')) {
        e.target.classList.remove('is-anim');
      }
    });
  })();

  /* =========================================================
     10. Subtle pointer tilt on cards
     ========================================================= */
  (function tilt() {
    if (reduceMotion || coarsePointer) return;
    var MAX = 4.5;

    $$('.tilt').forEach(function (el) {
      el.addEventListener('mouseenter', function () {
        if (!el.classList.contains('is-visible')) return;
        el.style.transition = 'transform .16s ease-out, box-shadow .35s ease';
      });

      el.addEventListener('mousemove', function (e) {
        if (!el.classList.contains('is-visible')) return;
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform =
          'perspective(900px) rotateX(' + (-py * MAX).toFixed(2) + 'deg) rotateY(' +
          (px * MAX).toFixed(2) + 'deg) translateY(-3px)';
      });

      el.addEventListener('mouseleave', function () {
        el.style.transform = '';
        window.setTimeout(function () { el.style.transition = ''; }, 320);
      });
    });
  })();

  /* =========================================================
     11. Footer year
     ========================================================= */
  var yearEl = $('#year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

})();
