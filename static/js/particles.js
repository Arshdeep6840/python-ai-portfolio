(() => {

  const canvas = document.getElementById("network-canvas");

  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  const prefersReduced =
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let width;
  let height;
  let particles = [];
  let animationId;

  const mouse = {
    x: null,
    y: null,
    radius: 180
  };

  const COLORS = [

    "0,245,255",
    "51,204,255",
    "59,130,255",
    "122,92,255",
    "181,76,255",
    "255,255,255"

  ];

  const CONFIG = {

    particleDensity: 1 / 650,

    maxParticles: 280,

    speed: 0.18,

    connectDistance: 145,

    glow: 18,

    pulseSpeed: 0.03

  };

  /* ===========================================
     Canvas Resize
  =========================================== */

  function resizeCanvas() {

    const rect =
      canvas.parentElement.getBoundingClientRect();

    const dpr =
      window.devicePixelRatio || 1;

    width = rect.width;
    height = rect.height;

    canvas.width = width * dpr;
    canvas.height = height * dpr;

    canvas.style.width = width + "px";
    canvas.style.height = height + "px";

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    createParticles();

  }

  /* ===========================================
     Particle Class
  =========================================== */

  class Particle {

    constructor() {

      this.reset();

      this.x =
        Math.random() * width;

      this.y =
        Math.random() * height;

    }

    reset() {

      this.x = Math.random() * width;
      this.y = Math.random() * height;

      this.vx =
        (Math.random() - .5) * CONFIG.speed;

      this.vy =
        (Math.random() - .5) * CONFIG.speed;

      this.radius =
        Math.random() * 1.8 + 1;

      this.depth =
        Math.random();

      this.color =
        COLORS[Math.floor(
          Math.random() * COLORS.length
        )];

      this.pulse =
        Math.random() * Math.PI * 2;

    }

    update() {

      this.x += this.vx;
      this.y += this.vy;

      if (this.x < 0 || this.x > width)
        this.vx *= -1;

      if (this.y < 0 || this.y > height)
        this.vy *= -1;

      this.pulse +=
        CONFIG.pulseSpeed;

      if (mouse.x !== null) {

        const dx =
          this.x - mouse.x;

        const dy =
          this.y - mouse.y;

        const dist =
          Math.sqrt(dx * dx + dy * dy);

        if (dist < mouse.radius) {

          const force =
            (mouse.radius - dist) /
            mouse.radius;

          const angle =
            Math.atan2(dy, dx);

          this.x +=
            Math.cos(angle) *
            force *
            1.2;

          this.y +=
            Math.sin(angle) *
            force *
            1.2;

        }

      }

    }

    draw() {

      const r =
        this.radius +
        Math.sin(this.pulse) * 0.45;

      ctx.globalAlpha =
        0.45 +
        this.depth * 0.55;

      ctx.shadowBlur =
        CONFIG.glow;

      ctx.shadowColor =
        `rgb(${this.color})`;

      ctx.beginPath();

      ctx.arc(
        this.x,
        this.y,
        r,
        0,
        Math.PI * 2
      );

      ctx.fillStyle =
        `rgba(${this.color},1)`;

      ctx.fill();

      ctx.shadowBlur = 0;

    }

  }

  /* ===========================================
     Create Particles
  =========================================== */

  function createParticles() {

    const count =
      Math.min(

        CONFIG.maxParticles,

        Math.floor(
          width *
          height *
          CONFIG.particleDensity
        )

      );

    particles = [];

    for (let i = 0; i < count; i++) {

      particles.push(
        new Particle()
      );

    }

  }

  /* ===========================================
     Draw Background
  =========================================== */

  function clearCanvas() {

    ctx.clearRect(
      0,
      0,
      width,
      height
    );

  }

  /* ===========================================
     Draw Particles
  =========================================== */

  function drawParticles() {

    for (const particle of particles) {

      particle.update();

      particle.draw();

    }

    ctx.globalAlpha = 1;

  }

  /* ===========================================
     Animation Loop
  =========================================== */

  function animate() {

    clearCanvas();

    drawConnections();   // Part 2

    drawParticles();

    animationId =
      requestAnimationFrame(
        animate
      );

  }

  /* ===========================================
     Init
  =========================================== */

  resizeCanvas();

  if (!prefersReduced) {

    animate();

  } else {

    clearCanvas();

    drawConnections();

    drawParticles();

  }
  /* ===========================================
     Draw Neural Connections
  =========================================== */

  function drawConnections() {

    ctx.save();

    for (let i = 0; i < particles.length; i++) {

      const a = particles[i];

      for (let j = i + 1; j < particles.length; j++) {

        const b = particles[j];

        const dx = a.x - b.x;
        const dy = a.y - b.y;

        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > CONFIG.connectDistance) continue;

        const opacity =
          (1 - dist / CONFIG.connectDistance) * 0.18;

        const gradient = ctx.createLinearGradient(
          a.x,
          a.y,
          b.x,
          b.y
        );

        gradient.addColorStop(
          0,
          `rgba(${a.color},${opacity})`
        );

        gradient.addColorStop(
          1,
          `rgba(${b.color},${opacity})`
        );

        ctx.beginPath();

        ctx.moveTo(a.x, a.y);

        ctx.lineTo(b.x, b.y);

        ctx.strokeStyle = gradient;

        ctx.lineWidth = 0.55;

        ctx.stroke();

      }

    }

    ctx.restore();

  }

  /* ===========================================
     Mouse Interaction
  =========================================== */

  canvas.parentElement.addEventListener("mousemove", e => {

    const rect = canvas.getBoundingClientRect();

    mouse.x = e.clientX - rect.left;

    mouse.y = e.clientY - rect.top;

  });

  canvas.parentElement.addEventListener("mouseleave", () => {

    mouse.x = null;

    mouse.y = null;

  });

  /* ===========================================
     Resize
  =========================================== */

  window.addEventListener("resize", () => {

    cancelAnimationFrame(animationId);

    resizeCanvas();

    if (!prefersReduced) {

      animate();

    } else {

      clearCanvas();

      drawConnections();

      drawParticles();

    }

  });

  /* ===========================================
     Cursor Glow
  =========================================== */

  const cursorGlow = document.getElementById("cursor-glow");

  if (cursorGlow) {

    window.addEventListener("mousemove", e => {

      cursorGlow.style.left = e.clientX + "px";

      cursorGlow.style.top = e.clientY + "px";

    });

  }

  /* ===========================================
     Navbar Scroll Effect
  =========================================== */

  const nav = document.getElementById("site-nav");

  if (nav) {

    window.addEventListener("scroll", () => {

      if (window.scrollY > 40) {

        nav.classList.add("nav-scrolled");

      } else {

        nav.classList.remove("nav-scrolled");

      }

    });

  }

  /* ===========================================
     Scroll Reveal
  =========================================== */

  const revealItems = document.querySelectorAll(".reveal");

  if ("IntersectionObserver" in window) {

    const observer = new IntersectionObserver(

      entries => {

        entries.forEach(entry => {

          if (entry.isIntersecting) {

            entry.target.classList.add("revealed");

            observer.unobserve(entry.target);

          }

        });

      },

      {

        threshold: 0.12

      }

    );

    revealItems.forEach(el => observer.observe(el));

  } else {

    revealItems.forEach(el => el.classList.add("revealed"));

  }

  /* ===========================================
     Smooth Hero Entrance
  =========================================== */

  window.addEventListener("load", () => {

    document.body.classList.add("page-loaded");

  });

  /* ===========================================
     Optional FPS Limiter
  =========================================== */

  // Uncomment if you want to cap animation to 60 FPS.
  // The current implementation already uses requestAnimationFrame,
  // so this is generally unnecessary.

  /*
  let last = 0;
  
  function animate(now) {
  
      if (now - last < 16) {
  
          animationId = requestAnimationFrame(animate);
  
          return;
  
      }
  
      last = now;
  
      clearCanvas();
  
      drawConnections();
  
      drawParticles();
  
      animationId = requestAnimationFrame(animate);
  
  }
  */

  /* ===========================================
     End of File
  =========================================== */

})();