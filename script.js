const loadingScreen = document.getElementById("loading-screen");
const loadingWord = document.getElementById("loading-word");
const loadingCounter = document.getElementById("loading-counter");
const loadingProgress = document.getElementById("loading-progress");
const loadingWords = ["Wealth", "Consciousness", "Alignment"];
const wordIntervalMs = 900;
const progressDurationMs = 2700;
const loaderExitDurationMs = 600;
const loaderCompleteDelayMs = 400;
const isHomePage = !document.body.classList.contains("about-page");

function loadVercelSpeedInsights() {
  const host = window.location.hostname;
  const isLocal =
    host === "localhost" || host === "127.0.0.1" || host === "" || host.endsWith(".local");

  if (isLocal) return;

  window.si =
    window.si ||
    function () {
      (window.siq = window.siq || []).push(arguments);
    };

  const script = document.createElement("script");
  script.defer = true;
  script.src = "/_vercel/speed-insights/script.js";
  document.head.appendChild(script);
}

loadVercelSpeedInsights();

function runLoadingScreen() {
  if (!isHomePage || !loadingScreen || !loadingWord || !loadingCounter || !loadingProgress) {
    document.body.classList.add("is-loaded");
    document.body.classList.remove("is-loading");
    return;
  }

  let wordIndex = 0;
  let rafId = 0;
  let wordIntervalId = 0;
  let isCompleted = false;

  const setWord = (nextWord) => {
    loadingWord.classList.remove("is-visible", "is-exiting");
    loadingWord.textContent = nextWord;
    requestAnimationFrame(() => {
      loadingWord.classList.add("is-visible");
    });
  };

  const transitionWord = (nextWord) => {
    loadingWord.classList.remove("is-visible");
    loadingWord.classList.add("is-exiting");
    window.setTimeout(() => {
      if (!loadingWord) return;
      loadingWord.classList.remove("is-exiting");
      loadingWord.textContent = nextWord;
      requestAnimationFrame(() => {
        loadingWord.classList.add("is-visible");
      });
    }, 400);
  };

  const completeLoader = () => {
    if (isCompleted) return;
    isCompleted = true;
    if (wordIntervalId) window.clearInterval(wordIntervalId);
    
    loadingScreen.classList.add("is-exiting");
    window.setTimeout(() => {
      window.scrollTo({ top: 0, left: 0, behavior: "auto" });
      document.body.classList.add("is-loaded");
      document.body.classList.remove("is-loading");
      loadingScreen.remove();
    }, loaderExitDurationMs);
  };

  setWord(loadingWords[0]);

  wordIntervalId = window.setInterval(() => {
    if (wordIndex >= loadingWords.length - 1) {
      window.clearInterval(wordIntervalId);
      return;
    }
    wordIndex += 1;
    transitionWord(loadingWords[wordIndex]);
  }, wordIntervalMs);

  const startedAt = performance.now();

  const tick = (timestamp) => {
    const elapsed = timestamp - startedAt;
    const progress = Math.min((elapsed / progressDurationMs) * 100, 100);
    const roundedProgress = Math.round(progress);

    loadingCounter.textContent = roundedProgress.toString().padStart(3, "0");
    loadingProgress.style.transform = `scaleX(${progress / 100})`;

    if (progress < 100) {
      rafId = requestAnimationFrame(tick);
      return;
    }

    loadingCounter.textContent = "100";
    loadingProgress.style.transform = "scaleX(1)";
    window.setTimeout(completeLoader, loaderCompleteDelayMs);
  };

  rafId = requestAnimationFrame(tick);

  window.addEventListener(
    "pagehide",
    () => {
      cancelAnimationFrame(rafId);
      window.clearInterval(wordIntervalId);
    },
    { once: true }
  );
}

runLoadingScreen();

const header = document.querySelector(".site-header");
const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");
const navClose = document.querySelector(".site-nav__close");
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
  window.lenis = lenis;

  const raf = (time) => {
    lenis.raf(time);
    requestAnimationFrame(raf);
  };

  requestAnimationFrame(raf);
  lenis.on("scroll", setHeaderState);
  window.dispatchEvent(new CustomEvent("lenis:ready", { detail: lenis }));
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
  navToggle.classList.toggle("is-open", !expanded);
  siteNav.classList.toggle("is-open");
  document.body.classList.toggle("nav-open", !expanded);
});

function closeMobileMenu() {
  siteNav?.classList.remove("is-open");
  navToggle?.classList.remove("is-open");
  navToggle?.setAttribute("aria-expanded", "false");
  document.body.classList.remove("nav-open");
}

navClose?.addEventListener("click", closeMobileMenu);

navLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    const href = link.getAttribute("href");

    if (!href?.startsWith("#")) {
      if (siteNav?.classList.contains("is-open")) {
        closeMobileMenu();
      }
      return;
    }

    if (lenis) {
      event.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        lenis.scrollTo(target, { offset: -84 });
      }
    }

    if (siteNav?.classList.contains("is-open")) {
      closeMobileMenu();
    }
  });
});

window.addEventListener("scroll", setHeaderState, { passive: true });
setHeaderState();

const sections = document.querySelectorAll("main section[id]");
const navAnchors = document.querySelectorAll(".site-nav__link");
const testimonialsRail = document.querySelector("[data-testimonials-rail]");
const testimonialPrev = document.querySelector("[data-testimonial-prev]");
const testimonialNext = document.querySelector("[data-testimonial-next]");
const testimonialDots = document.querySelectorAll("[data-testimonial-dot]");

const sectionObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      navAnchors.forEach((anchor) => {
        const href = anchor.getAttribute("href");
        if (!href?.startsWith("#")) return;
        anchor.classList.toggle("is-active", href === `#${entry.target.id}`);
      });
    });
  },
  { threshold: 0.4 }
);

sections.forEach((section) => sectionObserver.observe(section));

function setupTestimonialsSlider() {
  if (!testimonialsRail || !testimonialDots.length) return;

  const totalSlides = testimonialDots.length;
  const testimonialCards = testimonialsRail.querySelectorAll(".testimonial-card");
  let currentSlide = 0;
  let autoPlayId = 0;

  const updateSlider = (index) => {
    currentSlide = (index + totalSlides) % totalSlides;
    const activeCard = testimonialCards[currentSlide];
    const offset = activeCard ? activeCard.offsetLeft : 0;
    testimonialsRail.style.transform = `translateX(-${offset}px)`;
    testimonialDots.forEach((dot, dotIndex) => {
      dot.classList.toggle("is-active", dotIndex === currentSlide);
    });
  };

  const nextSlide = () => updateSlider(currentSlide + 1);
  const prevSlide = () => updateSlider(currentSlide - 1);

  const startAutoplay = () => {
    stopAutoplay();
    autoPlayId = window.setInterval(nextSlide, 3500);
  };

  const stopAutoplay = () => {
    if (autoPlayId) {
      window.clearInterval(autoPlayId);
      autoPlayId = 0;
    }
  };

  testimonialNext?.addEventListener("click", () => {
    nextSlide();
    startAutoplay();
  });

  testimonialPrev?.addEventListener("click", () => {
    prevSlide();
    startAutoplay();
  });

  testimonialDots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      updateSlider(index);
      startAutoplay();
    });
  });

  testimonialsRail.addEventListener("mouseenter", stopAutoplay);
  testimonialsRail.addEventListener("mouseleave", startAutoplay);

  updateSlider(0);
  startAutoplay();
  window.addEventListener("resize", () => updateSlider(currentSlide), { passive: true });

  window.addEventListener(
    "pagehide",
    () => {
      stopAutoplay();
    },
    { once: true }
  );
}

setupTestimonialsSlider();

function setupContactForm() {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;

  const status = form.querySelector("[data-contact-status]");
  const submitButton = form.querySelector('button[type="submit"]');
  const buttonLabel = submitButton?.querySelector("span:first-child");
  const defaultButtonText = buttonLabel?.textContent || "Send Message";

  const setStatus = (message, type) => {
    if (!status) return;
    status.textContent = message;
    status.dataset.state = type;
  };

  let toastTimer = 0;

  const showToast = (message, type) => {
    let toast = document.querySelector("[data-contact-toast]");

    if (!toast) {
      toast = document.createElement("div");
      toast.className = "contact-toast";
      toast.setAttribute("data-contact-toast", "");
      toast.setAttribute("role", "status");
      toast.setAttribute("aria-live", "polite");
      document.body.appendChild(toast);
    }

    window.clearTimeout(toastTimer);
    toast.textContent = message;
    toast.dataset.state = type;
    toast.classList.add("is-visible");

    toastTimer = window.setTimeout(() => {
      toast.classList.remove("is-visible");
    }, type === "pending" ? 1800 : 5200);
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const formData = new FormData(form);
    const payload = {
      name: formData.get("name"),
      email: formData.get("email"),
      phone: formData.get("phone"),
      subject: formData.get("subject"),
      message: formData.get("message"),
      company: formData.get("company"),
      terms: formData.get("terms") === "on",
    };

    if (submitButton) submitButton.disabled = true;
    if (buttonLabel) buttonLabel.textContent = "Sending...";
    setStatus("Sending your message...", "pending");
    showToast("Sending your message...", "pending");

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(result.message || "Something went wrong. Please try again.");
      }

      form.reset();
      const successMessage =
        result.message || "Thank you. Your message has been sent successfully.";
      setStatus(successMessage, "success");
      showToast(successMessage, "success");
    } catch (error) {
      const errorMessage =
        error.message || "Could not send your message. Please try again.";
      setStatus(errorMessage, "error");
      showToast(errorMessage, "error");
    } finally {
      if (submitButton) submitButton.disabled = false;
      if (buttonLabel) buttonLabel.textContent = defaultButtonText;
    }
  });
}

setupContactForm();
