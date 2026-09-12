// Footer year
document.getElementById("year").textContent = new Date().getFullYear();

// ---------------------------------------------------------------------------
// Smooth text transition for hero role line
// ---------------------------------------------------------------------------
(function roleCarousel() {
  const container = document.getElementById("role-carousel");
  if (!container || typeof ROLES === "undefined" || !ROLES.length) return;

  // Populate container
  ROLES.forEach(role => {
    const el = document.createElement("div");
    el.textContent = role;
    el.className = "h-8 flex items-center";
    container.appendChild(el);
  });
  
  // Clone first element for seamless looping
  const firstClone = container.firstElementChild.cloneNode(true);
  container.appendChild(firstClone);

  let currentIndex = 0;
  const totalItems = ROLES.length;

  setInterval(() => {
    currentIndex++;
    container.style.transition = "transform 0.7s cubic-bezier(0.65, 0, 0.35, 1)";
    container.style.transform = `translateY(-${currentIndex * 2}rem)`; // 2rem = 32px (h-8)

    // Reset without transition when reaching the clone
    if (currentIndex === totalItems) {
      setTimeout(() => {
        container.style.transition = "none";
        container.style.transform = "translateY(0)";
        currentIndex = 0;
      }, 700);
    }
  }, 3000);
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
    if (window.scrollY > 24) {
      nav.classList.add("bg-surface/70", "backdrop-blur-lg", "shadow-sm", "border-b", "border-line/50");
    } else {
      nav.classList.remove("bg-surface/70", "backdrop-blur-lg", "shadow-sm", "border-b", "border-line/50");
    }
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
// ScrollSpy (Active Nav Link)
// ---------------------------------------------------------------------------
(function scrollSpy() {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link");

  function onScroll() {
    let current = "";
    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      if (window.scrollY >= sectionTop - 150) {
        current = section.getAttribute("id");
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove("active");
      if (link.getAttribute("href").includes(current) && current !== "") {
        link.classList.add("active");
      }
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
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
    btn.textContent = "Sending...";
    status.textContent = "";
    status.className = "text-sm font-medium mt-4";

    try {
      const res = await fetch("/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();

      if (data.ok) {
        status.textContent = "✓ Message sent — I'll get back to you soon.";
        status.classList.add("text-secondary");
        form.reset();
      } else {
        status.textContent = "✗ " + (data.error || "Something went wrong.");
        status.classList.add("text-red-500");
      }
    } catch (err) {
      status.textContent = "✗ Network error — please email me directly instead.";
      status.classList.add("text-red-500");
    } finally {
      btn.disabled = false;
      btn.textContent = "Send Message";
    }
  });
})();
