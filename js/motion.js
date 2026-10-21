/**
 * MotionSites-inspired cinematic motion layer
 * particles · word stagger · marquee · tilt · reveal · magnetic · scroll progress
 */
(function () {
  'use strict';

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarse = window.matchMedia('(pointer: coarse)').matches;

  /* ——— Scroll progress bar ——— */
  function initProgress() {
    const bar = document.querySelector('[data-scroll-progress]');
    if (!bar) return;
    const onScroll = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const t = max > 0 ? window.scrollY / max : 0;
      bar.style.transform = `scaleX(${t})`;
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ——— Nav state ——— */
  function initNav() {
    const nav = document.querySelector('[data-nav]');
    if (!nav) return;
    const tick = () => nav.classList.toggle('is-scrolled', window.scrollY > 20);
    window.addEventListener('scroll', tick, { passive: true });
    tick();
  }

  /* ——— Word / line stagger reveal on load ——— */
  function initHeroWords() {
    const root = document.querySelector('[data-split-words]');
    if (!root) return;
    const text = root.textContent.trim();
    const words = text.split(/\s+/);
    root.textContent = '';
    root.setAttribute('aria-label', text);

    words.forEach((word, i) => {
      const wrap = document.createElement('span');
      wrap.className = 'word-wrap';
      const inner = document.createElement('span');
      inner.className = 'word';
      inner.textContent = word;
      inner.style.setProperty('--i', String(i));
      wrap.appendChild(inner);
      root.appendChild(wrap);
      root.appendChild(document.createTextNode(' '));
    });

    requestAnimationFrame(() => {
      root.classList.add('is-ready');
      document.querySelector('[data-hero]')?.classList.add('is-ready');
    });
  }

  /* ——— Hero particle field (mouse-reactive) ——— */
  function initParticles() {
    const canvas = document.querySelector('[data-particles]');
    if (!canvas || reduce) return;
    const ctx = canvas.getContext('2d');
    let w = 0,
      h = 0,
      dpr = 1;
    let mouse = { x: 0.5, y: 0.4 };
    let target = { x: 0.5, y: 0.4 };
    const COUNT = coarse ? 36 : 72;
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
        x: Math.random(),
        y: Math.random(),
        r: 1 + Math.random() * 2.2,
        vx: (Math.random() - 0.5) * 0.00025,
        vy: (Math.random() - 0.5) * 0.00025,
        phase: Math.random() * Math.PI * 2,
      });
    }

    window.addEventListener(
      'pointermove',
      (e) => {
        const rect = canvas.getBoundingClientRect();
        target.x = (e.clientX - rect.left) / rect.width;
        target.y = (e.clientY - rect.top) / rect.height;
      },
      { passive: true }
    );

    function frame(t) {
      mouse.x += (target.x - mouse.x) * 0.06;
      mouse.y += (target.y - mouse.y) * 0.06;
      ctx.clearRect(0, 0, w, h);

      // soft accent bloom near cursor
      const g = ctx.createRadialGradient(
        mouse.x * w,
        mouse.y * h,
        0,
        mouse.x * w,
        mouse.y * h,
        Math.max(w, h) * 0.35
      );
      g.addColorStop(0, 'rgba(200, 245, 66, 0.16)');
      g.addColorStop(0.45, 'rgba(200, 245, 66, 0.04)');
      g.addColorStop(1, 'rgba(200, 245, 66, 0)');
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, w, h);

      for (const d of dots) {
        d.x += d.vx + (mouse.x - 0.5) * 0.00008;
        d.y += d.vy + (mouse.y - 0.5) * 0.00008;
        if (d.x < 0) d.x = 1;
        if (d.x > 1) d.x = 0;
        if (d.y < 0) d.y = 1;
        if (d.y > 1) d.y = 0;

        const px = d.x * w;
        const py = d.y * h;
        const dist = Math.hypot(d.x - mouse.x, d.y - mouse.y);
        const pulse = 0.35 + Math.sin(t * 0.002 + d.phase) * 0.15;
        const alpha = Math.max(0.08, 0.55 - dist * 0.9) * pulse;

        ctx.beginPath();
        ctx.fillStyle = `rgba(17, 17, 17, ${alpha})`;
        ctx.arc(px, py, d.r, 0, Math.PI * 2);
        ctx.fill();

        // connect nearby to cursor
        if (dist < 0.18) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(200, 245, 66, ${0.35 - dist})`;
          ctx.lineWidth = 1;
          ctx.moveTo(px, py);
          ctx.lineTo(mouse.x * w, mouse.y * h);
          ctx.stroke();
        }
      }
      requestAnimationFrame(frame);
    }

    resize();
    window.addEventListener('resize', resize);
    requestAnimationFrame(frame);
  }

  /* ——— Infinite marquee pause on hover is CSS; ensure duplicated track ——— */
  function initMarquee() {
    document.querySelectorAll('[data-marquee]').forEach((el) => {
      const track = el.querySelector('[data-marquee-track]');
      if (!track || track.dataset.cloned) return;
      track.innerHTML = track.innerHTML + track.innerHTML;
      track.dataset.cloned = '1';
    });
  }

  /* ——— 3D tilt on interactive panels ——— */
  function initTilt() {
    if (reduce || coarse) return;
    document.querySelectorAll('[data-tilt]').forEach((card) => {
      const max = parseFloat(card.getAttribute('data-tilt') || '8');
      card.addEventListener('pointermove', (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(900px) rotateY(${x * max}deg) rotateX(${-y * max}deg) translateY(-4px)`;
        card.style.setProperty('--mx', `${(x + 0.5) * 100}%`);
        card.style.setProperty('--my', `${(y + 0.5) * 100}%`);
      });
      card.addEventListener('pointerleave', () => {
        card.style.transform = '';
      });
    });
  }

  /* ——— Scroll reveals ——— */
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
      { threshold: 0.14, rootMargin: '0px 0px -6% 0px' }
    );
    els.forEach((el) => io.observe(el));
  }

  /* ——— Magnetic CTAs ——— */
  function initMagnetic() {
    if (reduce || coarse) return;
    document.querySelectorAll('[data-magnetic]').forEach((btn) => {
      btn.addEventListener('pointermove', (e) => {
        const r = btn.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        btn.style.transform = `translate(${x * 0.22}px, ${y * 0.22}px)`;
      });
      btn.addEventListener('pointerleave', () => {
        btn.style.transform = '';
      });
    });
  }

  /* ——— Count up ——— */
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
          const dur = 1200;
          const tick = (now) => {
            const p = Math.min(1, (now - start) / dur);
            const eased = 1 - Math.pow(1 - p, 3);
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

  /* ——— Smooth hash links ——— */
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

  document.addEventListener('DOMContentLoaded', () => {
    initProgress();
    initNav();
    initHeroWords();
    initParticles();
    initMarquee();
    initTilt();
    initReveals();
    initMagnetic();
    initCounters();
  });
})();
