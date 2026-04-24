const header = document.querySelector(".site-header");
const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");
const navLinks = document.querySelectorAll(".site-nav__link, .footer__column a, .text-link, .btn, .brand");
const revealItems = document.querySelectorAll(".reveal");
function setHeaderState() {
  if (window.scrollY > 12) {
    header.classList.add("is-scrolled");
  } else {
    header.classList.remove("is-scrolled");
  }
}

const lenis =
  window.Lenis &&
  new window.Lenis({
    duration: 1.15,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    smoothTouch: false,
    wheelMultiplier: 1,
  });

if (lenis) {
  const raf = (time) => {
    lenis.raf(time);
    requestAnimationFrame(raf);
  };

  requestAnimationFrame(raf);
  lenis.on("scroll", setHeaderState);
}

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.18, rootMargin: "0px 0px -60px 0px" }
);

revealItems.forEach((item) => observer.observe(item));

navToggle?.addEventListener("click", () => {
  const expanded = navToggle.getAttribute("aria-expanded") === "true";
  navToggle.setAttribute("aria-expanded", String(!expanded));
  siteNav.classList.toggle("is-open");
});

navLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    const href = link.getAttribute("href");

    if (href?.startsWith("#") && lenis) {
      event.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        lenis.scrollTo(target, { offset: -84 });
      }
    }

    if (siteNav.classList.contains("is-open")) {
      siteNav.classList.remove("is-open");
      navToggle?.setAttribute("aria-expanded", "false");
    }
  });
});

window.addEventListener("scroll", setHeaderState, { passive: true });
setHeaderState();

const sections = document.querySelectorAll("main section[id]");
const navAnchors = document.querySelectorAll(".site-nav__link");

const sectionObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      navAnchors.forEach((anchor) => {
        anchor.classList.toggle("is-active", anchor.getAttribute("href") === `#${entry.target.id}`);
      });
    });
  },
  { threshold: 0.4 }
);

sections.forEach((section) => sectionObserver.observe(section));
