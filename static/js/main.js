// Footer year
document.getElementById("year").textContent = new Date().getFullYear();

// ---------------------------------------------------------------------------
// Typewriter effect for hero role line
// ---------------------------------------------------------------------------
(function typewriter() {
  const el = document.getElementById("typed-role");
  if (!el || typeof ROLES === "undefined" || !ROLES.length) return;

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (prefersReduced) {
    el.textContent = ROLES.join(" · ");
    return;
  }

  let roleIndex = 0;
  let charIndex = 0;
  let deleting = false;

  function tick() {
    const current = ROLES[roleIndex];
    if (!deleting) {
      charIndex++;
      el.textContent = current.slice(0, charIndex);
      if (charIndex === current.length) {
        deleting = true;
        setTimeout(tick, 1400);
        return;
      }
    } else {
      charIndex--;
      el.textContent = current.slice(0, charIndex);
      if (charIndex === 0) {
        deleting = false;
        roleIndex = (roleIndex + 1) % ROLES.length;
      }
    }
    setTimeout(tick, deleting ? 35 : 60);
  }
  tick();
})();

// ---------------------------------------------------------------------------
// Scroll reveal
// ---------------------------------------------------------------------------
(function scrollReveal() {
  const targets = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    targets.forEach((t) => t.classList.add("revealed"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const delay = Number(entry.target.dataset.delay || 0) * 90;
          setTimeout(() => entry.target.classList.add("revealed"), delay);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );
  targets.forEach((t) => observer.observe(t));
})();

// ---------------------------------------------------------------------------
// Nav background on scroll
// ---------------------------------------------------------------------------
(function navScroll() {
  const nav = document.getElementById("site-nav");
  if (!nav) return;
  function update() {
    if (window.scrollY > 24) nav.classList.add("nav-scrolled");
    else nav.classList.remove("nav-scrolled");
  }
  window.addEventListener("scroll", update, { passive: true });
  update();
})();

// ---------------------------------------------------------------------------
// Mobile nav toggle
// ---------------------------------------------------------------------------
(function mobileNav() {
  const toggle = document.getElementById("nav-toggle");
  const panel = document.getElementById("nav-mobile");
  if (!toggle || !panel) return;

  function close() {
    panel.classList.add("hidden");
    toggle.setAttribute("aria-expanded", "false");
  }
  function open() {
    panel.classList.remove("hidden");
    toggle.setAttribute("aria-expanded", "true");
  }

  toggle.addEventListener("click", () => {
    panel.classList.contains("hidden") ? open() : close();
  });
  panel.querySelectorAll(".nav-mobile-link").forEach((link) => {
    link.addEventListener("click", close);
  });
})();

// ---------------------------------------------------------------------------
// Resource type filter
// ---------------------------------------------------------------------------
(function resourceFilter() {
  const buttons = document.querySelectorAll(".resource-filter-btn");
  const cards = document.querySelectorAll(".resource-card");
  if (!buttons.length) return;

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => {
        b.classList.remove("active", "border-cyan", "text-cyan");
        b.classList.add("border-line", "text-muted");
      });
      btn.classList.add("active", "border-cyan", "text-cyan");
      btn.classList.remove("border-line", "text-muted");

      const filter = btn.dataset.filter;
      cards.forEach((card) => {
        const show = filter === "all" || card.dataset.type === filter;
        card.style.display = show ? "" : "none";
      });
    });
  });
})();

// ---------------------------------------------------------------------------
// Contact form
// ---------------------------------------------------------------------------
(function contactForm() {
  const form = document.getElementById("contact-form");
  if (!form) return;
  const status = document.getElementById("contact-status");
  const btn = document.getElementById("contact-submit");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      name: form.name.value,
      email: form.email.value,
      message: form.message.value,
    };

    btn.disabled = true;
    btn.textContent = "sending...";
    status.textContent = "";
    status.className = "font-mono text-xs mt-2";

    try {
      const res = await fetch("/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();

      if (data.ok) {
        status.textContent = "✓ Message sent — I'll get back to you soon.";
        status.classList.add("text-cyan");
        form.reset();
      } else {
        status.textContent = "✗ " + (data.error || "Something went wrong.");
        status.classList.add("text-amber");
      }
    } catch (err) {
      status.textContent = "✗ Network error — please email me directly instead.";
      status.classList.add("text-amber");
    } finally {
      btn.disabled = false;
      btn.textContent = "send_message()";
    }
  });
})();
