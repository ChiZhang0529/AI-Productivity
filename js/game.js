    // Stick Hero vs Monsters Game
    (function() {
      const canvas = document.getElementById('game-canvas');
      const ctx = canvas.getContext('2d');
      const scoreEl = document.getElementById('game-score');
      const waveEl = document.getElementById('game-wave');
      const livesEl = document.getElementById('game-lives');
      const bestEl = document.getElementById('game-best');
      const startBtn = document.getElementById('game-start-btn');
      const gameOverOverlay = document.getElementById('game-over-overlay');
      const finalScoreEl = document.getElementById('game-final-score');
      const finalWaveEl = document.getElementById('game-final-wave');
      const restartBtn = document.getElementById('game-restart-btn');
      const mobileControls = document.getElementById('mobile-controls');

      // Responsive canvas
      function resizeCanvas() {
        const wrapper = document.getElementById('game-wrapper');
        const maxW = Math.min(wrapper.offsetWidth, 640);
        canvas.style.width = maxW + 'px';
        canvas.style.height = (maxW * 0.5625) + 'px';
      }
      resizeCanvas();
      window.addEventListener('resize', resizeCanvas);

      let isPlaying = false;
      let score = 0;
      let wave = 1;
      let lives = 3;
      let bestScore = parseInt(localStorage.getItem('stickHeroBest') || '0');
      bestEl.textContent = bestScore;

      let animFrame;
      let lastTime = 0;
      let spawnTimer = 0;
      let waveTimer = 0;
      let attackCooldown = 0;
      let isAttacking = false;
      let attackAnim = 0;
      let screenShake = 0;
      let particles = [];
      let hitFlash = 0;

      const W = 640, H = 360;
      const GROUND_Y = H - 40;

      // Hero
      const hero = {
        x: W / 2, y: GROUND_Y,
        w: 24, h: 48,
        speed: 5,
        vx: 0,
        facing: 1,
        moving: false
      };

      let monsters = [];
      let attacks = [];

      // Monster types
      const MONSTER_TYPES = [
        { name: 'slime', color: '#22c55e', w: 28, h: 22, speed: 1.2, hp: 1, pts: 10, eyeColor: '#fff' },
        { name: 'goblin', color: '#f97316', w: 22, h: 38, speed: 1.8, hp: 1, pts: 15, eyeColor: '#fff' },
        { name: 'demon', color: '#ef4444', w: 30, h: 40, speed: 2.2, hp: 2, pts: 25, eyeColor: '#ffff00' },
        { name: 'ghost', color: '#a855f7', w: 26, h: 36, speed: 1.5, hp: 1, pts: 20, eyeColor: '#fff', float: true },
        { name: 'skull', color: '#64748b', w: 24, h: 34, speed: 2.5, hp: 1, pts: 30, eyeColor: '#ef4444' }
      ];

      // Input
      const keys = { left: false, right: false };
      document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft' || e.key === 'a') keys.left = true;
        if (e.key === 'ArrowRight' || e.key === 'd') keys.right = true;
        if (e.key === ' ') { e.preventDefault(); triggerAttack(); }
      });
      document.addEventListener('keyup', (e) => {
        if (e.key === 'ArrowLeft' || e.key === 'a') keys.left = false;
        if (e.key === 'ArrowRight' || e.key === 'd') keys.right = false;
      });

      // Mobile buttons
      const btnLeft = document.getElementById('btn-left');
      const btnRight = document.getElementById('btn-right');
      const btnAttack = document.getElementById('btn-attack');
      btnLeft.addEventListener('touchstart', (e) => { e.preventDefault(); keys.left = true; });
      btnLeft.addEventListener('touchend', () => { keys.left = false; });
      btnRight.addEventListener('touchstart', (e) => { e.preventDefault(); keys.right = true; });
      btnRight.addEventListener('touchend', () => { keys.right = false; });
      btnAttack.addEventListener('touchstart', (e) => { e.preventDefault(); triggerAttack(); });

      canvas.addEventListener('click', triggerAttack);
      canvas.addEventListener('touchstart', (e) => { e.preventDefault(); triggerAttack(); });

      function triggerAttack() {
        if (!isPlaying || attackCooldown > 0) return;
        isAttacking = true;
        attackAnim = 0;
        attackCooldown = 20;
        
        // Check hit
        const atkRange = 80;
        monsters.forEach((m, i) => {
          const dx = m.x - hero.x;
          const dy = m.y - hero.y - m.h / 2;
          if (Math.abs(dx) < atkRange && Math.abs(dy) < m.h && Math.sign(dx) === hero.facing || Math.abs(dx) < 40) {
            m.hp--;
            screenShake = 5;
            spawnParticles(m.x, m.y - m.h / 2, m.color, 8);
            if (m.hp <= 0) {
              score += m.pts;
              scoreEl.textContent = score;
              spawnParticles(m.x, m.y - m.h / 2, '#fff', 12);
              monsters.splice(i, 1);
            }
          }
        });
      }

      function spawnParticles(x, y, color, count) {
        for (let i = 0; i < count; i++) {
          particles.push({
            x, y,
            vx: (Math.random() - 0.5) * 8,
            vy: (Math.random() - 0.5) * 8 - 3,
            life: 30,
            color
          });
        }
      }

      function spawnMonster() {
        const types = MONSTER_TYPES;
        const pool = wave < 3 ? [types[0], types[1]] : wave < 5 ? [types[0], types[1], types[3]] : types;
        const t = pool[Math.floor(Math.random() * pool.length)];
        const side = Math.random() < 0.5 ? 0 : 1;
        const m = {
          ...t,
          x: side === 0 ? -t.w : W + t.w,
          y: GROUND_Y,
          dir: side === 0 ? 1 : -1,
          anim: Math.random() * Math.PI * 2
        };
        monsters.push(m);
      }

      function drawStickFigure(x, y, facing, attacking, attackFrame) {
        ctx.save();
        ctx.translate(x, y);
        ctx.scale(facing, 1);

        const headR = 9;
        const bodyH = 20;
        const legLen = 18;
        const armLen = 16;

        // Attack arm angle
        let armAngle = attacking ? -Math.PI / 3 + attackFrame * 0.3 : -0.3;

        ctx.strokeStyle = '#e2e8f0';
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        // Legs
        const legSpread = attacking ? 6 : 0;
        ctx.beginPath();
        ctx.moveTo(-legSpread, 0);
        ctx.lineTo(-4, -legLen);
        ctx.moveTo(legSpread, 0);
        ctx.lineTo(4, -legLen);
        ctx.stroke();

        // Body
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(0, -bodyH);
        ctx.stroke();

        // Head
        ctx.beginPath();
        ctx.arc(0, -bodyH - headR, headR, 0, Math.PI * 2);
        ctx.stroke();

        // Back arm
        ctx.beginPath();
        ctx.moveTo(0, -bodyH + 4);
        ctx.lineTo(-armLen * 0.8, -bodyH + 4 + armLen * 0.5);
        ctx.stroke();

        // Attack arm (with weapon)
        ctx.beginPath();
        ctx.moveTo(0, -bodyH + 4);
        const ax = Math.cos(armAngle) * armLen;
        const ay = Math.sin(armAngle) * armLen;
        ctx.lineTo(ax, -bodyH + 4 + ay);
        ctx.stroke();

        // Sword
        if (attacking) {
          ctx.strokeStyle = '#7dd3fc';
          ctx.lineWidth = 2;
          const sx = ax, sy = -bodyH + 4 + ay;
          ctx.beginPath();
          ctx.moveTo(sx, sy);
          ctx.lineTo(sx + 20, sy - 15);
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(sx + 5, sy + 5);
          ctx.lineTo(sx + 18, sy - 5);
          ctx.stroke();
        }

        ctx.restore();
      }

      function drawMonster(m) {
        ctx.save();
        ctx.translate(m.x, m.y);

        const bounce = Math.sin(m.anim) * 3;
        const floatY = m.float ? bounce : 0;

        if (m.name === 'slime') {
          ctx.fillStyle = m.color;
          ctx.beginPath();
          ctx.ellipse(0, -m.h / 2 + floatY, m.w / 2, m.h / 2, 0, 0, Math.PI * 2);
          ctx.fill();
          // Eyes
          ctx.fillStyle = '#fff';
          ctx.beginPath();
          ctx.arc(-5, -m.h / 2 - 2 + floatY, 4, 0, Math.PI * 2);
          ctx.arc(5, -m.h / 2 - 2 + floatY, 4, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#000';
          ctx.beginPath();
          ctx.arc(-4, -m.h / 2 - 2 + floatY, 2, 0, Math.PI * 2);
          ctx.arc(6, -m.h / 2 - 2 + floatY, 2, 0, Math.PI * 2);
          ctx.fill();
        } else if (m.name === 'goblin') {
          // Body
          ctx.fillStyle = m.color;
          ctx.beginPath();
          ctx.ellipse(0, -m.h / 2 + floatY, m.w / 2, m.h / 2, 0, 0, Math.PI * 2);
          ctx.fill();
          // Ears
          ctx.beginPath();
          ctx.moveTo(-8, -m.h + 5 + floatY);
          ctx.lineTo(-14, -m.h - 5 + floatY);
          ctx.lineTo(-5, -m.h + floatY);
          ctx.fill();
          ctx.beginPath();
          ctx.moveTo(8, -m.h + 5 + floatY);
          ctx.lineTo(14, -m.h - 5 + floatY);
          ctx.lineTo(5, -m.h + floatY);
          ctx.fill();
          // Eyes
          ctx.fillStyle = m.eyeColor;
          ctx.beginPath();
          ctx.arc(-4, -m.h / 2 - 3 + floatY, 3, 0, Math.PI * 2);
          ctx.arc(4, -m.h / 2 - 3 + floatY, 3, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#000';
          ctx.beginPath();
          ctx.arc(-3, -m.h / 2 - 3 + floatY, 1.5, 0, Math.PI * 2);
          ctx.arc(5, -m.h / 2 - 3 + floatY, 1.5, 0, Math.PI * 2);
          ctx.fill();
        } else if (m.name === 'demon') {
          ctx.fillStyle = m.color;
          ctx.beginPath();
          ctx.ellipse(0, -m.h / 2 + floatY, m.w / 2, m.h / 2, 0, 0, Math.PI * 2);
          ctx.fill();
          // Horns
          ctx.fillStyle = '#7f1d1d';
          ctx.beginPath();
          ctx.moveTo(-8, -m.h + 8 + floatY);
          ctx.lineTo(-14, -m.h - 8 + floatY);
          ctx.lineTo(-5, -m.h + 3 + floatY);
          ctx.fill();
          ctx.beginPath();
          ctx.moveTo(8, -m.h + 8 + floatY);
          ctx.lineTo(14, -m.h - 8 + floatY);
          ctx.lineTo(5, -m.h + 3 + floatY);
          ctx.fill();
          // Eyes
          ctx.fillStyle = m.eyeColor;
          ctx.beginPath();
          ctx.arc(-5, -m.h / 2 - 3 + floatY, 4, 0, Math.PI * 2);
          ctx.arc(5, -m.h / 2 - 3 + floatY, 4, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#000';
          ctx.beginPath();
          ctx.arc(-4, -m.h / 2 - 3 + floatY, 2, 0, Math.PI * 2);
          ctx.arc(6, -m.h / 2 - 3 + floatY, 2, 0, Math.PI * 2);
          ctx.fill();
        } else if (m.name === 'ghost') {
          ctx.globalAlpha = 0.8;
          ctx.fillStyle = m.color;
          ctx.beginPath();
          ctx.arc(0, -m.h / 2 + 5 + floatY, m.w / 2, Math.PI, 0);
          ctx.lineTo(m.w / 2, -m.h / 2 + floatY);
          for (let i = 0; i < 4; i++) {
            const gx = m.w / 2 - i * (m.w / 4) - m.w / 8;
            ctx.quadraticCurveTo(gx + 5, -m.h / 2 + 8 + floatY, gx, -m.h / 2 + floatY);
          }
          ctx.fill();
          ctx.globalAlpha = 1;
          ctx.fillStyle = m.eyeColor;
          ctx.beginPath();
          ctx.arc(-5, -m.h / 2 - 2 + floatY, 4, 0, Math.PI * 2);
          ctx.arc(5, -m.h / 2 - 2 + floatY, 4, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#000';
          ctx.beginPath();
          ctx.arc(-4, -m.h / 2 - 2 + floatY, 2, 0, Math.PI * 2);
          ctx.arc(6, -m.h / 2 - 2 + floatY, 2, 0, Math.PI * 2);
          ctx.fill();
        } else if (m.name === 'skull') {
          ctx.fillStyle = m.color;
          ctx.beginPath();
          ctx.arc(0, -m.h / 2 + 8 + floatY, m.w / 2, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillRect(-m.w / 4, -m.h / 2 + floatY, m.w / 2, m.h / 2);
          // Eyes
          ctx.fillStyle = m.eyeColor;
          ctx.beginPath();
          ctx.arc(-4, -m.h / 2 + 5 + floatY, 4, 0, Math.PI * 2);
          ctx.arc(4, -m.h / 2 + 5 + floatY, 4, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#000';
          ctx.beginPath();
          ctx.arc(-3, -m.h / 2 + 5 + floatY, 2, 0, Math.PI * 2);
          ctx.arc(5, -m.h / 2 + 5 + floatY, 2, 0, Math.PI * 2);
          ctx.fill();
        }

        ctx.restore();
      }

      function drawAttackEffect() {
        if (!isAttacking) return;
        ctx.save();
        ctx.globalAlpha = Math.max(0, 1 - attackAnim / 15);
        const ax = hero.x + hero.facing * 30;
        const ay = hero.y - 30;
        ctx.strokeStyle = '#7dd3fc';
        ctx.lineWidth = 2;
        for (let i = 0; i < 3; i++) {
          ctx.beginPath();
          ctx.arc(ax + i * 8 * hero.facing, ay - i * 5, 15 + i * 8, 0, Math.PI * 2);
          ctx.stroke();
        }
        ctx.restore();
      }

      function drawParticles() {
        particles.forEach(p => {
          ctx.save();
          ctx.globalAlpha = p.life / 30;
          ctx.fillStyle = p.color;
          ctx.beginPath();
          ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        });
      }

      function drawGround() {
        ctx.fillStyle = '#1a1a24';
        ctx.fillRect(0, GROUND_Y, W, H - GROUND_Y);
        ctx.strokeStyle = 'rgba(14,141,232,0.3)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, GROUND_Y);
        ctx.lineTo(W, GROUND_Y);
        ctx.stroke();
        // Ground details
        ctx.fillStyle = '#22222e';
        for (let i = 0; i < W; i += 40) {
          ctx.fillRect(i, GROUND_Y, 20, 3);
        }
      }

      function drawBG() {
        ctx.fillStyle = '#0a0a0f';
        ctx.fillRect(0, 0, W, H);
        // Stars
        ctx.fillStyle = 'rgba(255,255,255,0.3)';
        for (let i = 0; i < 30; i++) {
          const sx = (i * 97 + 13) % W;
          const sy = (i * 53 + 7) % (GROUND_Y - 20);
          ctx.beginPath();
          ctx.arc(sx, sy, 1, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      function draw() {
        ctx.save();
        // Screen shake
        if (screenShake > 0) {
          ctx.translate(
            (Math.random() - 0.5) * screenShake,
            (Math.random() - 0.5) * screenShake
          );
        }
        // Hit flash
        if (hitFlash > 0) {
          ctx.fillStyle = `rgba(239,68,68,${hitFlash * 0.1})`;
          ctx.fillRect(0, 0, W, H);
        }

        drawBG();
        drawGround();
        drawParticles();

        // Monsters
        monsters.forEach(m => drawMonster(m));

        // Attack effect
        drawAttackEffect();

        // Hero
        drawStickFigure(hero.x, hero.y, hero.facing, isAttacking, attackAnim);
        ctx.restore();
      }

      function update(dt) {
        if (!isPlaying) return;

        // Hero movement
        hero.vx = 0;
        if (keys.left) { hero.vx = -hero.speed; hero.facing = -1; hero.moving = true; }
        if (keys.right) { hero.vx = hero.speed; hero.facing = 1; hero.moving = true; }
        hero.x += hero.vx;
        hero.x = Math.max(20, Math.min(W - 20, hero.x));

        // Attack animation
        if (isAttacking) {
          attackAnim++;
          if (attackAnim > 15) { isAttacking = false; attackAnim = 0; }
        }
        if (attackCooldown > 0) attackCooldown--;

        // Screen shake decay
        if (screenShake > 0) screenShake *= 0.8;
        if (hitFlash > 0) hitFlash--;

        // Particles
        particles.forEach(p => {
          p.x += p.vx;
          p.y += p.vy;
          p.vy += 0.3;
          p.life--;
        });
        particles = particles.filter(p => p.life > 0);

        // Spawn monsters
        spawnTimer++;
        const spawnRate = Math.max(30, 90 - wave * 10);
        if (spawnTimer >= spawnRate) {
          spawnMonster();
          spawnTimer = 0;
        }

        // Wave progression
        waveTimer++;
        if (waveTimer >= 600) {
          wave++;
          waveEl.textContent = wave;
          waveTimer = 0;
          // Spawn extra
          spawnMonster();
          spawnMonster();
        }

        // Move monsters
        monsters.forEach(m => {
          m.anim += 0.1;
          m.x += m.dir * m.speed * (1 + wave * 0.1);
          // Float effect for ghosts
          if (m.float) {
            m.y = GROUND_Y + Math.sin(m.anim * 0.5) * 8;
          }
        });

        // Check collision with hero
        monsters.forEach((m, i) => {
          const dx = Math.abs(m.x - hero.x);
          if (dx < m.w / 2 + 15) {
            lives--;
            livesEl.textContent = lives;
            hitFlash = 10;
            screenShake = 10;
            spawnParticles(hero.x, hero.y - 24, '#ef4444', 10);
            monsters.splice(i, 1);
            if (lives <= 0) {
              endGame();
            }
          }
        });
      }

      function gameLoop(timestamp) {
        const dt = timestamp - lastTime;
        lastTime = timestamp;
        update(dt);
        draw();
        if (isPlaying) {
          animFrame = requestAnimationFrame(gameLoop);
        }
      }

      function startGame() {
        score = 0;
        wave = 1;
        lives = 3;
        monsters = [];
        particles = [];
        spawnTimer = 0;
        waveTimer = 0;
        attackCooldown = 0;
        isAttacking = false;
        attackAnim = 0;
        screenShake = 0;
        hero.x = W / 2;
        hero.facing = 1;
        scoreEl.textContent = '0';
        waveEl.textContent = '1';
        livesEl.textContent = '3';
        isPlaying = true;
        gameOverOverlay.classList.add('hidden');
        mobileControls.classList.remove('hidden');
        startBtn.textContent = 'Playing...';
        startBtn.disabled = true;
        startBtn.classList.add('opacity-50');
        lastTime = performance.now();
        animFrame = requestAnimationFrame(gameLoop);
      }

      function endGame() {
        isPlaying = false;
        cancelAnimationFrame(animFrame);
        if (score > bestScore) {
          bestScore = score;
          localStorage.setItem('stickHeroBest', bestScore);
          bestEl.textContent = bestScore;
        }
        finalScoreEl.textContent = score;
        finalWaveEl.textContent = wave;
        gameOverOverlay.classList.remove('hidden');
        startBtn.textContent = 'Start Game';
        startBtn.disabled = false;
        startBtn.classList.remove('opacity-50');
        mobileControls.classList.add('hidden');
      }

      startBtn.addEventListener('click', startGame);
      restartBtn.addEventListener('click', startGame);

      // Draw initial frame
      draw();
    })();
