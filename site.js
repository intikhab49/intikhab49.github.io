(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.remove('no-js');
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- rotating headline: every N seconds, with dots, a progress line, pause on hover and a Pause button
  var heads = Array.prototype.slice.call(document.querySelectorAll('.heads span'));
  var dots = Array.prototype.slice.call(document.querySelectorAll('.dots button'));
  var bar = document.querySelector('.bar i');
  var pauseBtn = document.querySelector('.pause');
  var rotor = document.querySelector('.rotor-area');
  var secs = parseFloat(root.style.getPropertyValue('--secs')) || 10;
  var hi = 0, elapsed = 0, paused = still, hover = false;
  function show(i) {
    hi = (i + heads.length) % heads.length;
    heads.forEach(function (h, k) { h.classList.toggle('on', k === hi); });
    dots.forEach(function (d, k) { d.setAttribute('aria-pressed', k === hi ? 'true' : 'false'); });
    elapsed = 0;
    if (bar) { bar.classList.remove('run'); void bar.offsetWidth; if (!still) bar.classList.add('run'); }
    syncBar();
  }
  function syncBar() { if (bar) bar.classList.toggle('hold', paused || hover); }
  if (heads.length) {
    show(0);
    dots.forEach(function (d, k) { d.addEventListener('click', function () { show(k); }); });
    if (pauseBtn) {
      pauseBtn.textContent = paused ? 'Play' : 'Pause';
      pauseBtn.addEventListener('click', function () {
        paused = !paused;
        pauseBtn.textContent = paused ? 'Play' : 'Pause';
        syncBar();
      });
    }
    if (rotor) {
      rotor.addEventListener('mouseenter', function () { hover = true; syncBar(); });
      rotor.addEventListener('mouseleave', function () { hover = false; syncBar(); });
    }
    setInterval(function () {
      if (paused || hover || document.hidden) return;
      elapsed += 250;
      if (elapsed >= secs * 1000) show(hi + 1);
    }, 250);
  }

  // ---- project filters and search
  var cards = Array.prototype.slice.call(document.querySelectorAll('.proj'));
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var q = document.getElementById('q');
  var count = document.querySelector('.count');
  var empty = document.querySelector('.empty');
  var group = 'all';
  function apply() {
    var term = (q && q.value || '').trim().toLowerCase(), n = 0;
    cards.forEach(function (c) {
      var ok = (group === 'all' || c.dataset.group === group) && (!term || c.dataset.text.indexOf(term) !== -1);
      c.hidden = !ok;
      if (ok) n++;
    });
    if (count) count.textContent = n + ' of ' + cards.length + ' projects';
    if (empty) empty.hidden = n !== 0;
  }
  chips.forEach(function (ch) {
    ch.addEventListener('click', function () {
      group = ch.dataset.group;
      chips.forEach(function (o) { o.setAttribute('aria-pressed', o === ch ? 'true' : 'false'); });
      apply();
    });
  });
  if (q) q.addEventListener('input', apply);
  apply();

  // ---- stack tabs (arrow keys move between tabs, as a tablist should)
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  var panels = Array.prototype.slice.call(document.querySelectorAll('.panel'));
  function selectTab(t, focus) {
    tabs.forEach(function (o) {
      var on = o === t;
      o.setAttribute('aria-selected', on ? 'true' : 'false');
      o.tabIndex = on ? 0 : -1;
    });
    panels.forEach(function (p) { p.hidden = p.id !== t.getAttribute('aria-controls'); });
    if (focus) t.focus();
  }
  tabs.forEach(function (t, k) {
    t.addEventListener('click', function () { selectTab(t, false); });
    t.addEventListener('keydown', function (e) {
      var d = (e.key === 'ArrowDown' || e.key === 'ArrowRight') ? 1 : (e.key === 'ArrowUp' || e.key === 'ArrowLeft') ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      selectTab(tabs[(k + d + tabs.length) % tabs.length], true);
    });
  });
  if (tabs.length) selectTab(tabs[0], false);

  // ---- the 3D knot: a (3,5) torus knot drawn as a wireframe tube, drag to spin, leans toward the cursor
  var c = document.getElementById('knot');
  if (!c || !c.getContext) return;
  var ctx = c.getContext('2d');
  var P = 3, Q = 5, N = 260, R = 10, rings = [];
  function centre(t) { var r = 2 + Math.cos(Q * t); return [r * Math.cos(P * t), r * Math.sin(P * t), -Math.sin(Q * t)]; }
  for (var i = 0; i < N; i++) {
    var t = i / N * Math.PI * 2, a = centre(t), b = centre(t + 0.01);
    var tx = b[0] - a[0], ty = b[1] - a[1], tz = b[2] - a[2], tl = Math.hypot(tx, ty, tz);
    tx /= tl; ty /= tl; tz /= tl;
    var nx = -ty, ny = tx, nz = 0, nl = Math.hypot(nx, ny) || 1;
    nx /= nl; ny /= nl;
    var bx = ty * nz - tz * ny, by = tz * nx - tx * nz, bz = tx * ny - ty * nx, ring = [];
    for (var k = 0; k < R; k++) {
      var g = k / R * Math.PI * 2, rr = 0.42;
      ring.push([a[0] + rr * (Math.cos(g) * nx + Math.sin(g) * bx), a[1] + rr * (Math.cos(g) * ny + Math.sin(g) * by),
                 a[2] + rr * (Math.cos(g) * nz + Math.sin(g) * bz)]);
    }
    rings.push(ring);
  }
  var rx = -0.5, ry = 0.3, vx = 0.0022, vy = 0.0035, drag = false, lx = 0, ly = 0, tiltX = 0, tiltY = 0, visible = true;
  function size() {
    var r = c.getBoundingClientRect(), d = Math.min(window.devicePixelRatio || 1, 2);
    c.width = Math.max(1, r.width * d); c.height = Math.max(1, r.height * d);
    if (still) draw();
  }
  window.addEventListener('resize', size);
  c.addEventListener('pointerdown', function (e) { drag = true; lx = e.clientX; ly = e.clientY; c.setPointerCapture(e.pointerId); });
  c.addEventListener('pointerup', function () { drag = false; });
  c.addEventListener('pointercancel', function () { drag = false; });
  c.addEventListener('pointermove', function (e) {
    var r = c.getBoundingClientRect();
    tiltX = ((e.clientY - r.top) / r.height - 0.5) * 0.5;
    tiltY = ((e.clientX - r.left) / r.width - 0.5) * 0.5;
    if (!drag) return;
    vy = (e.clientX - lx) * 0.0009; vx = (e.clientY - ly) * 0.0009;
    ry += (e.clientX - lx) * 0.008; rx += (e.clientY - ly) * 0.008;
    lx = e.clientX; ly = e.clientY;
  });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }).observe(c);
  }
  function draw() {
    var w = c.width, h = c.height, s = Math.min(w, h) / 8.6;
    ctx.clearRect(0, 0, w, h);
    var ax = rx + tiltX, ay = ry + tiltY, cx = Math.cos(ax), sx = Math.sin(ax), cy = Math.cos(ay), sy = Math.sin(ay);
    var pr = rings.map(function (ring) {
      return ring.map(function (p) {
        var x1 = p[0] * cy + p[2] * sy, z1 = -p[0] * sy + p[2] * cy, y2 = p[1] * cx - z1 * sx, z2 = p[1] * sx + z1 * cx;
        var f = 6.5 / (6.5 + z2);
        return [w / 2 + x1 * s * f, h / 2 + y2 * s * f, z2];
      });
    });
    ctx.lineWidth = Math.max(1, (window.devicePixelRatio || 1) * 0.9);
    for (var i = 0; i < N; i++) {
      var A = pr[i], B = pr[(i + 1) % N];
      for (var k = 0; k < R; k++) {
        var p = A[k], q2 = A[(k + 1) % R], u = B[k];
        var depth = Math.max(0.08, Math.min(1, 0.62 - p[2] * 0.2));
        ctx.strokeStyle = 'rgba(198,244,50,' + depth.toFixed(3) + ')';
        ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q2[0], q2[1]); ctx.lineTo(u[0], u[1]); ctx.stroke();
      }
    }
  }
  function loop() {
    if (visible && !document.hidden) {
      if (!drag) { rx += vx; ry += vy; vx += (0.0022 - vx) * 0.02; vy += (0.0035 - vy) * 0.02; }
      draw();
    }
    requestAnimationFrame(loop);
  }
  size();
  if (still) draw(); else loop();
})();
