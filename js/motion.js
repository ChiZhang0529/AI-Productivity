/**
 * Motion layer v2 — denser, louder, still respectful of prefers-reduced-motion
 * cursor trail · letter stagger · mesh particles · stage waveform · parallax
 * scramble · spotlight · dual marquee · tilt · reveal · magnetic · counters
 */
(function () {
  'use strict';

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarse = window.matchMedia('(pointer: coarse)').matches;

  /* ——— Custom cursor + lime trail ——— */
  function initCursor() {
    if (reduce || coarse) return;
    const dot = document.createElement('div');
    const ring = document.createElement('div');
    dot.className = 'cursor-dot';
    ring.className = 'cursor-ring';
    document.body.appendChild(dot);
    document.body.appendChild(ring);
    document.body.classList.add('has-cursor');

    let x = window.innerWidth / 2;
    let y = window.innerHeight / 2;
    let rx = x;
    let ry = y;
    const trail = [];

    for (let i = 0; i < 8; i++) {
      const t = document.createElement('div');
      t.className = 'cursor-trail';
      t.style.setProperty('--t', String(i));
      document.body.appendChild(t);
      trail.push({ el: t, x, y });
    }

    window.addEventListener(
      'pointermove',
      (e) => {
        x = e.clientX;
        y = e.clientY;
      },
      { passive: true }
    );

    document.querySelectorAll('a, button, [data-tilt], [data-magnetic]').forEach((el) => {
      el.addEventListener('pointerenter', () => document.body.classList.add('cursor-hover'));
      el.addEventListener('pointerleave', () => document.body.classList.remove('cursor-hover'));
    });

    function frame() {
      rx += (x - rx) * 0.18;
      ry += (y - ry) * 0.18;
      dot.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      ring.style.transform = `translate3d(${rx}px, ${ry}px, 0)`;

      let px = x;
      let py = y;
      trail.forEach((node, i) => {
        node.x += (px - node.x) * (0.28 - i * 0.02);
        node.y += (py - node.y) * (0.28 - i * 0.02);
        node.el.style.transform = `translate3d(${node.x}px, ${node.y}px, 0)`;
        px = node.x;
        py = node.y;
      });
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  /* ——— Global mouse spotlight ——— */
  function initSpotlight() {
    if (reduce || coarse) return;
    const spot = document.querySelector('[data-spotlight]');
    if (!spot) return;
    window.addEventListener(
      'pointermove',
      (e) => {
        spot.style.setProperty('--sx', e.clientX + 'px');
        spot.style.setProperty('--sy', e.clientY + 'px');
      },
      { passive: true }
    );
  }

  /* ——— Scroll progress ——— */
  function initProgress() {
    const bar = document.querySelector('[data-scroll-progress]');
    if (!bar) return;
    const onScroll = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = `scaleX(${max > 0 ? window.scrollY / max : 0})`;
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  function initNav() {
    const nav = document.querySelector('[data-nav]');
    if (!nav) return;
    const tick = () => nav.classList.toggle('is-scrolled', window.scrollY > 20);
    window.addEventListener('scroll', tick, { passive: true });
    tick();
  }

  /* ——— Letter-level stagger ——— */
  function initHeroLetters() {
    const root = document.querySelector('[data-split-words]');
    if (!root) return;
    const text = root.textContent.trim();
    root.textContent = '';
    root.setAttribute('aria-label', text);

    let delay = 0;
    [...text].forEach((ch) => {
      if (ch === ' ') {
        root.appendChild(document.createTextNode(' '));
        delay += 1;
        return;
      }
      const wrap = document.createElement('span');
      wrap.className = 'char-wrap';
      const inner = document.createElement('span');
      inner.className = 'char';
      inner.textContent = ch;
      inner.style.setProperty('--i', String(delay++));
      wrap.appendChild(inner);
      root.appendChild(wrap);
    });

    requestAnimationFrame(() => {
      root.classList.add('is-ready');
      document.querySelector('[data-hero]')?.classList.add('is-ready');
    });
  }

  /* ——— Hero scroll parallax ——— */
  function initHeroParallax() {
    const hero = document.querySelector('[data-hero]');
    if (!hero || reduce) return;
    const title = hero.querySelector('.hero-title');
    const stage = hero.querySelector('.hero-stage');
    let ticking = false;

    window.addEventListener(
      'scroll',
      () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          const y = window.scrollY;
          const fade = Math.max(0, 1 - y / (window.innerHeight * 0.85));
          hero.style.setProperty('--hero-fade', fade.toFixed(3));
          if (title) title.style.transform = `translate3d(0, ${y * 0.35}px, 0) scale(${1 + y * 0.0002})`;
          if (stage) stage.style.transform = `translate3d(0, ${y * 0.12}px, 0)`;
          ticking = false;
        });
      },
      { passive: true }
    );
  }

  /* ——— Dense mesh particle field ——— */
  function initParticles() {
    const canvas = document.querySelector('[data-particles]');
    if (!canvas || reduce) return;
    const ctx = canvas.getContext('2d');
    let w = 0;
    let h = 0;
    let dpr = 1;
    let mouse = { x: -999, y: -999 };
    let target = { x: 0.5, y: 0.4 };
    const COUNT = coarse ? 40 : 90;
    const LINK = coarse ? 90 : 120;
    const dots = [];

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.clientWidth;
      h = canvas.clientHeight;
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    for (let i = 0; i < COUNT; i++) {
      dots.push({
        x: Math.random() * 1,
        y: Math.random() * 1,
        r: 1.2 + Math.random() * 2.4,
        vx: (Math.random() - 0.5) * 0.00045,
        vy: (Math.random() - 0.5) * 0.00045,
        phase: Math.random() * Math.PI * 2,
      });
    }

    window.addEventListener(
      'pointermove',
      (e) => {
        const rect = canvas.getBoundingClientRect();
        if (e.clientY < rect.bottom && e.clientY > rect.top) {
          target.x = (e.clientX - rect.left) / rect.width;
          target.y = (e.clientY - rect.top) / rect.height;
          mouse.x = target.x * w;
          mouse.y = target.y * h;
        }
      },
      { passive: true }
    );

    function frame(t) {
      target.x += (0.5 - target.x) * 0.002;
      const mx = target.x;
      const my = target.y;
      ctx.clearRect(0, 0, w, h);

      const bloom = ctx.createRadialGradient(mx * w, my * h, 0, mx * w, my * h, Math.max(w, h) * 0.42);
      bloom.addColorStop(0, 'rgba(200, 245, 66, 0.22)');
      bloom.addColorStop(0.4, 'rgba(200, 245, 66, 0.06)');
      bloom.addColorStop(1, 'rgba(200, 245, 66, 0)');
      ctx.fillStyle = bloom;
      ctx.fillRect(0, 0, w, h);

      // positions in px
      const pts = dots.map((d) => {
        d.x += d.vx + (mx - 0.5) * 0.00012;
        d.y += d.vy + (my - 0.5) * 0.00012;
        if (d.x < 0 || d.x > 1) d.vx *= -1;
        if (d.y < 0 || d.y > 1) d.vy *= -1;
        d.x = Math.min(1, Math.max(0, d.x));
        d.y = Math.min(1, Math.max(0, d.y));

        // mouse repulsion
        const dx = d.x - mx;
        const dy = d.y - my;
        const dist = Math.hypot(dx, dy) || 0.001;
        if (dist < 0.15) {
          d.x += (dx / dist) * 0.0015;
          d.y += (dy / dist) * 0.0015;
        }
        return { x: d.x * w, y: d.y * h, d, dist };
      });

      // mesh links
      for (let i = 0; i < pts.length; i++) {
        for (let j = i + 1; j < pts.length; j++) {
          const a = pts[i];
          const b = pts[j];
          const dx = a.x - b.x;
          const dy = a.y - b.y;
          const dist = Math.hypot(dx, dy);
          if (dist < LINK) {
            const alpha = (1 - dist / LINK) * 0.35;
            ctx.beginPath();
            ctx.strokeStyle = `rgba(17, 17, 17, ${alpha})`;
            ctx.lineWidth = 1;
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
        // link to cursor
        if (mouse.x > 0) {
          const dist = Math.hypot(pts[i].x - mouse.x, pts[i].y - mouse.y);
          if (dist < LINK * 1.2) {
            ctx.beginPath();
            ctx.strokeStyle = `rgba(200, 245, 66, ${(1 - dist / (LINK * 1.2)) * 0.55})`;
            ctx.lineWidth = 1.25;
            ctx.moveTo(pts[i].x, pts[i].y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.stroke();
          }
        }
      }

      pts.forEach(({ x, y, d, dist }) => {
        const pulse = 0.45 + Math.sin(t * 0.003 + d.phase) * 0.25;
        const near = Math.max(0, 1 - dist * 4);
        const r = d.r + near * 2;
        ctx.beginPath();
        ctx.fillStyle = near > 0.2 ? `rgba(200, 245, 66, ${0.55 * pulse})` : `rgba(17, 17, 17, ${0.45 * pulse})`;
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
      });

      requestAnimationFrame(frame);
    }

    resize();
    window.addEventListener('resize', resize);
    requestAnimationFrame(frame);
  }

  /* ——— Hero stage waveform canvas ——— */
  function initStageWave() {
    const canvas = document.querySelector('[data-stage-wave]');
    if (!canvas || reduce) return;
    const ctx = canvas.getContext('2d');
    let w = 0;
    let h = 0;
    let dpr = 1;
    let mouseX = 0.5;

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.clientWidth;
      h = canvas.clientHeight;
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    canvas.parentElement?.addEventListener(
      'pointermove',
      (e) => {
        const r = canvas.getBoundingClientRect();
        mouseX = (e.clientX - r.left) / r.width;
      },
      { passive: true }
    );

    function frame(t) {
      ctx.clearRect(0, 0, w, h);
      const bars = Math.floor(w / 10);
      const mid = h * 0.55;
      for (let i = 0; i < bars; i++) {
        const nx = i / bars;
        const influence = 1 - Math.min(1, Math.abs(nx - mouseX) * 2.2);
        const wave =
          Math.sin(t * 0.004 + i * 0.35) * 0.35 +
          Math.sin(t * 0.002 + i * 0.12) * 0.25 +
          influence * 0.55;
        const bh = Math.max(4, Math.abs(wave) * h * 0.42);
        const x = (i / bars) * w;
        const hueBoost = influence;
        ctx.fillStyle = hueBoost > 0.15 ? `rgba(200, 245, 66, ${0.25 + hueBoost * 0.55})` : `rgba(255,255,255,${0.08 + Math.abs(wave) * 0.12})`;
        ctx.fillRect(x, mid - bh / 2, 5, bh);
      }

      // scanning line
      const scan = ((t * 0.08) % w);
      const g = ctx.createLinearGradient(scan - 40, 0, scan + 40, 0);
      g.addColorStop(0, 'rgba(200,245,66,0)');
      g.addColorStop(0.5, 'rgba(200,245,66,0.35)');
      g.addColorStop(1, 'rgba(200,245,66,0)');
      ctx.fillStyle = g;
      ctx.fillRect(scan - 40, 0, 80, h);

      requestAnimationFrame(frame);
    }

    resize();
    window.addEventListener('resize', resize);
    requestAnimationFrame(frame);
  }

  /* ——— Marquee clone ——— */
  function initMarquee() {
    document.querySelectorAll('[data-marquee]').forEach((el) => {
      const track = el.querySelector('[data-marquee-track]');
      if (!track || track.dataset.cloned) return;
      track.innerHTML = track.innerHTML + track.innerHTML;
      track.dataset.cloned = '1';
    });
  }

  /* ——— Tilt ——— */
  function bindTilt(card) {
    if (card.dataset.tiltBound) return;
    card.dataset.tiltBound = '1';
    const max = Math.min(6, parseFloat(card.getAttribute('data-tilt') || '6'));
    card.style.transformStyle = 'preserve-3d';
    card.style.transition = 'transform 0.15s ease-out, border-color 0.25s';

    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      // no scale / large lift — those cause hover “jump” vs neighbors
      card.style.transform = `perspective(900px) rotateY(${(x * max).toFixed(2)}deg) rotateX(${(-y * max).toFixed(2)}deg)`;
      card.style.setProperty('--mx', `${((x + 0.5) * 100).toFixed(1)}%`);
      card.style.setProperty('--my', `${((y + 0.5) * 100).toFixed(1)}%`);
    });
    card.addEventListener('pointerleave', () => {
      card.style.transform = 'perspective(900px) rotateY(0deg) rotateX(0deg)';
      card.style.setProperty('--mx', '50%');
      card.style.setProperty('--my', '40%');
    });
  }

  function initTilt() {
    if (reduce || coarse) return;
    document.querySelectorAll('[data-tilt]').forEach(bindTilt);
    window.bindTiltCard = bindTilt;
  }

  /* ——— Text scramble on hover ——— */
  function initScramble() {
    if (reduce) return;
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%*';
    document.querySelectorAll('[data-scramble]').forEach((el) => {
      const original = el.textContent;
      let frame = 0;
      let timer;
      el.addEventListener('pointerenter', () => {
        cancelAnimationFrame(timer);
        frame = 0;
        const run = () => {
          el.textContent = original
            .split('')
            .map((c, i) => {
              if (c === ' ' || c === '\n') return c;
              if (i < frame / 2) return original[i];
              return chars[(Math.random() * chars.length) | 0];
            })
            .join('');
          frame++;
          if (frame < original.length * 2) timer = requestAnimationFrame(run);
          else el.textContent = original;
        };
        run();
      });
      el.addEventListener('pointerleave', () => {
        cancelAnimationFrame(timer);
        el.textContent = original;
      });
    });
  }

  /* ——— Reveals ——— */
  function initReveals() {
    const els = document.querySelectorAll('[data-reveal]');
    if (!els.length) return;
    if (reduce) {
      els.forEach((el) => el.classList.add('is-in'));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -8% 0px' }
    );
    els.forEach((el) => io.observe(el));
  }

  /* ——— Magnetic ——— */
  function initMagnetic() {
    if (reduce || coarse) return;
    document.querySelectorAll('[data-magnetic]').forEach((btn) => {
      btn.addEventListener('pointermove', (e) => {
        const r = btn.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        btn.style.transform = `translate(${x * 0.28}px, ${y * 0.28}px)`;
      });
      btn.addEventListener('pointerleave', () => {
        btn.style.transform = '';
      });
    });
  }

  /* ——— Counters ——— */
  function initCounters() {
    const nums = document.querySelectorAll('[data-count]');
    if (!nums.length) return;
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const target = parseFloat(el.dataset.count);
          const suffix = el.dataset.suffix || '';
          const prefix = el.dataset.prefix || '';
          if (reduce) {
            el.textContent = prefix + target + suffix;
            io.unobserve(el);
            return;
          }
          const start = performance.now();
          const dur = 1400;
          const tick = (now) => {
            const p = Math.min(1, (now - start) / dur);
            const eased = 1 - Math.pow(1 - p, 4);
            el.textContent = prefix + Math.round(target * eased) + suffix;
            if (p < 1) requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
          io.unobserve(el);
        });
      },
      { threshold: 0.4 }
    );
    nums.forEach((n) => io.observe(n));
  }

  /* ——— Smooth anchors ——— */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  function boot() {
    initCursor();
    initSpotlight();
    initProgress();
    initNav();
    initHeroLetters();
    initHeroParallax();
    initParticles();
    initStageWave();
    initMarquee();
    initTilt();
    initScramble();
    initReveals();
    initMagnetic();
    initCounters();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
