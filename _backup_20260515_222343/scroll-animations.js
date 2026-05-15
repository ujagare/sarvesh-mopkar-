/*!
 * scroll-animations.js - polished reveal animations for Sarvesh Mopkar pages
 */

(function () {
  "use strict";

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  function onReady(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback, { once: true });
      return;
    }

    callback();
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const existing = document.querySelector(`script[src="${src}"]`);
      if (existing) {
        existing.addEventListener("load", resolve, { once: true });
        existing.addEventListener("error", reject, { once: true });
        if (window.gsap && src.includes("gsap.min.js")) resolve();
        if (window.ScrollTrigger && src.includes("ScrollTrigger.min.js")) resolve();
        return;
      }

      const script = document.createElement("script");
      script.src = src;
      script.async = true;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  async function ensureGsap() {
    if (!window.gsap) {
      await loadScript(
        "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"
      );
    }

    if (!window.ScrollTrigger) {
      await loadScript(
        "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"
      );
    }

    if (!window.gsap || !window.ScrollTrigger) return false;
    window.gsap.registerPlugin(window.ScrollTrigger);
    return true;
  }

  function injectBaseStyles() {
    if (document.getElementById("sa-animation-styles")) return;

    const style = document.createElement("style");
    style.id = "sa-animation-styles";
    style.textContent = `
      #sa-progress-bar {
        position: fixed;
        top: 0;
        left: 0;
        z-index: 99999;
        width: 100%;
        height: 3px;
        pointer-events: none;
        transform: scaleX(0);
        transform-origin: left center;
        background: linear-gradient(90deg, #c9a24a, #f0d36a, #a67c2e);
        box-shadow: 0 0 14px rgba(201, 162, 74, 0.22);
        will-change: transform;
      }

      @media (pointer: fine) and (prefers-reduced-motion: no-preference) {
        html.sa-premium-cursor,
        html.sa-premium-cursor body,
        html.sa-premium-cursor a,
        html.sa-premium-cursor button,
        html.sa-premium-cursor [role="button"],
        html.sa-premium-cursor input[type="submit"],
        html.sa-premium-cursor input[type="button"] {
          cursor: none;
        }

        #sa-cursor-dot,
        #sa-cursor-ring {
          position: fixed;
          top: 0;
          left: 0;
          z-index: 100000;
          pointer-events: none;
          border-radius: 999px;
          transform: translate3d(-50%, -50%, 0);
          will-change: transform, width, height, opacity, border-color, background;
        }

        #sa-cursor-dot {
          width: 9px;
          height: 9px;
          background: #d6a62f;
          border: 1px solid rgba(48, 35, 15, 0.22);
          box-shadow:
            0 0 0 3px rgba(255, 247, 224, 0.92),
            0 0 14px rgba(139, 105, 20, 0.4),
            0 0 26px rgba(201, 162, 74, 0.28);
        }

        #sa-cursor-ring {
          width: 42px;
          height: 42px;
          border: 1.5px solid rgba(120, 84, 18, 0.78);
          background: rgba(255, 248, 232, 0.16);
          box-shadow:
            inset 0 0 0 1px rgba(255, 255, 255, 0.72),
            0 0 0 1px rgba(255, 247, 224, 0.62),
            0 0 28px rgba(120, 84, 18, 0.2);
        }

        html.sa-cursor-hover #sa-cursor-dot {
          width: 7px;
          height: 7px;
          background: #6f4d12;
        }

        html.sa-cursor-hover #sa-cursor-ring {
          width: 62px;
          height: 62px;
          border-color: rgba(110, 75, 12, 0.9);
          background: rgba(214, 166, 47, 0.14);
        }

        html.sa-cursor-down #sa-cursor-ring {
          width: 30px;
          height: 30px;
          border-color: rgba(139, 105, 20, 0.72);
        }

        html.sa-cursor-hidden #sa-cursor-dot,
        html.sa-cursor-hidden #sa-cursor-ring {
          opacity: 0;
        }
      }

      .reveal,
      .hero__content,
      .about-hero__content,
      .work-hero__content,
      .philo-hero__inner,
      .contact-hero__copy,
      .wwm-hero__copy,
      .blog-hero__content,
      .legal-hero__inner {
        backface-visibility: hidden;
      }

      .sa-text-mask {
        overflow: hidden;
      }

      .sa-text-mask-inner {
        display: inline-block;
        max-width: 100%;
        will-change: transform, opacity;
        transform: translateZ(0);
      }

      .sa-media-reveal {
        will-change: transform, opacity;
        transform: translateZ(0);
      }

      @media (prefers-reduced-motion: reduce) {
        #sa-progress-bar {
          display: none;
        }

        .reveal {
          opacity: 1 !important;
          transform: none !important;
          transition: none !important;
        }

        .sa-text-mask {
          overflow: visible !important;
        }

        .sa-text-mask-inner,
        .sa-media-reveal {
          opacity: 1 !important;
          transform: none !important;
        }
      }
    `;
    document.head.appendChild(style);
  }

  function setupProgressBar(gsap, ScrollTrigger) {
    if (document.getElementById("sa-progress-bar")) return;

    const bar = document.createElement("div");
    bar.id = "sa-progress-bar";
    document.body.prepend(bar);

    gsap.to(bar, {
      scaleX: 1,
      ease: "none",
      scrollTrigger: {
        trigger: document.documentElement,
        start: "top top",
        end: "bottom bottom",
        scrub: 0.25,
      },
    });

    ScrollTrigger.refresh();
  }

  function setupPremiumCursor() {
    const canUseCursor =
      window.matchMedia("(pointer: fine)").matches && !prefersReducedMotion;

    if (!canUseCursor || document.getElementById("sa-cursor-dot")) return;

    const root = document.documentElement;
    const dot = document.createElement("div");
    const ring = document.createElement("div");

    dot.id = "sa-cursor-dot";
    ring.id = "sa-cursor-ring";
    document.body.append(dot, ring);
    root.classList.add("sa-premium-cursor", "sa-cursor-hidden");

    let targetX = window.innerWidth / 2;
    let targetY = window.innerHeight / 2;
    let ringX = targetX;
    let ringY = targetY;
    let isVisible = false;

    const render = () => {
      ringX += (targetX - ringX) * 0.18;
      ringY += (targetY - ringY) * 0.18;

      dot.style.transform = `translate3d(${targetX}px, ${targetY}px, 0) translate(-50%, -50%)`;
      ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0) translate(-50%, -50%)`;

      requestAnimationFrame(render);
    };

    document.addEventListener(
      "mousemove",
      (event) => {
        targetX = event.clientX;
        targetY = event.clientY;

        if (!isVisible) {
          ringX = targetX;
          ringY = targetY;
          root.classList.remove("sa-cursor-hidden");
          isVisible = true;
        }
      },
      { passive: true }
    );

    document.addEventListener("mouseleave", () => {
      root.classList.add("sa-cursor-hidden");
      isVisible = false;
    });

    document.addEventListener("mouseenter", () => {
      root.classList.remove("sa-cursor-hidden");
    });

    document.addEventListener("mousedown", () => {
      root.classList.add("sa-cursor-down");
    });

    document.addEventListener("mouseup", () => {
      root.classList.remove("sa-cursor-down");
    });

    document.addEventListener("mouseover", (event) => {
      const target = event.target;
      if (
        target instanceof Element &&
        target.closest("a, button, [role='button'], input, textarea, select, summary, .btn")
      ) {
        root.classList.add("sa-cursor-hover");
      }
    });

    document.addEventListener("mouseout", (event) => {
      const target = event.target;
      if (
        target instanceof Element &&
        target.closest("a, button, [role='button'], input, textarea, select, summary, .btn")
      ) {
        root.classList.remove("sa-cursor-hover");
      }
    });

    requestAnimationFrame(render);
  }

  function syncSmoothScroll(ScrollTrigger) {
    const connect = (lenis) => {
      if (!lenis || lenis.datasetSaSynced === true || typeof lenis.on !== "function") {
        return;
      }

      lenis.datasetSaSynced = true;
      lenis.on("scroll", ScrollTrigger.update);
    };

    connect(window.lenis);
    window.addEventListener("lenis:ready", (event) => connect(event.detail), {
      once: true,
    });
  }

  function isInFirstView(el) {
    const rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight * 0.92 && rect.bottom > 0;
  }

  function getTextTargets(root) {
    const selector = [
      "h1",
      "h2",
      "h3",
      ".hero__copy",
      ".about-hero__text",
      ".work-hero p:not(.work-kicker)",
      ".philo-hero p:not(.philo-kicker)",
      ".contact-hero p:not(.contact-kicker)",
      ".wwm-hero p:not(.wwm-eyebrow)",
      ".blog-hero p:not(.blog-eyebrow)",
      ".eyebrow",
      ".about-label",
      ".work-kicker",
      ".philo-kicker",
      ".contact-kicker",
      ".wwm-eyebrow",
      ".blog-eyebrow",
      ".section-head p",
      ".section-header p",
    ].join(", ");

    const scope = root || document;
    const targets = scope.matches?.(selector)
      ? [scope]
      : Array.from(scope.querySelectorAll(selector));

    return targets.filter((el) => {
      if (el.dataset.saTextPrepared === "true") return false;
      if (!el.textContent.trim()) return false;
      if (el.closest("button, .btn, input, textarea, select")) return false;

      const style = window.getComputedStyle(el);
      return style.display !== "none" && style.visibility !== "hidden";
    });
  }

  function prepareTextMask(el) {
    if (el.dataset.saTextPrepared === "true") {
      return el.querySelector(":scope > .sa-text-mask-inner");
    }

    const inner = document.createElement("span");
    inner.className = "sa-text-mask-inner";

    while (el.firstChild) {
      inner.appendChild(el.firstChild);
    }

    el.appendChild(inner);
    el.classList.add("sa-text-mask");
    el.dataset.saTextPrepared = "true";

    return inner;
  }

  function animateTextTargets(gsap, targets, options) {
    const inners = targets.map(prepareTextMask).filter(Boolean);
    if (!inners.length) return null;

    return gsap.fromTo(
      inners,
      {
        autoAlpha: 1,
        yPercent: 108,
      },
      {
        autoAlpha: 1,
        yPercent: 0,
        duration: options?.duration || 1.05,
        ease: "power4.out",
        stagger: options?.stagger ?? 0.075,
        delay: options?.delay || 0,
        overwrite: "auto",
        clearProps: "opacity,visibility,transform",
        scrollTrigger: options?.scrollTrigger,
      }
    );
  }

  function getMediaTargets(root) {
    const selector = [
      ".reveal img",
      ".about__media img",
      ".about-hero__image-wrapper img",
      ".journey-image-wrap img",
      ".feature-banner__art",
      ".pillar-card__image",
      ".work-card__image img",
      ".work-process__item img",
      ".work-difference__panel img",
      ".work-invite img",
      ".philosophy-bg-image img",
      ".about-cta__bg img",
      ".wwm-card img",
      ".contact-service-card img",
    ].join(", ");

    return Array.from((root || document).querySelectorAll(selector)).filter((el) => {
      if (el.dataset.saMediaAnimated === "true") return false;
      const style = window.getComputedStyle(el);
      return style.display !== "none" && style.visibility !== "hidden";
    });
  }

  function getMediaDirection(el) {
    const rect = el.getBoundingClientRect();
    const center = rect.left + rect.width / 2;
    return center < window.innerWidth / 2 ? -1 : 1;
  }

  function setupHeroEntrance(gsap) {
    const heroSelectors = [
      ".hero__content",
      ".about-hero__content",
      ".work-hero__content",
      ".philo-hero__inner",
      ".contact-hero__copy",
      ".wwm-hero__copy",
      ".blog-hero__content",
      ".legal-hero__inner",
    ];

    const hero = document.querySelector(heroSelectors.join(", "));
    if (!hero || hero.dataset.saHeroAnimated === "true") return;

    hero.dataset.saHeroAnimated = "true";
    hero.classList.add("is-visible");
    gsap.set(hero, { autoAlpha: 1, y: 0, clearProps: "transform" });

    const parts = Array.from(hero.children).filter((child) => {
      const style = window.getComputedStyle(child);
      return style.display !== "none" && style.visibility !== "hidden";
    });

    if (!parts.length || !isInFirstView(hero)) return;

    const textTargets = getTextTargets(hero);
    const nonTextParts = parts.filter((part) => !textTargets.includes(part));

    gsap.fromTo(
      nonTextParts,
      { autoAlpha: 0, y: 20 },
      {
        autoAlpha: 1,
        y: 0,
        duration: 0.8,
        ease: "power2.out",
        stagger: 0.1,
        delay: document.body.classList.contains("is-loading") ? 3.2 : 0.1,
        overwrite: "auto",
        clearProps: "opacity,visibility,transform",
      }
    );

    animateTextTargets(gsap, textTargets, {
      delay: document.body.classList.contains("is-loading") ? 3.25 : 0.12,
      stagger: 0.085,
      duration: 1.15,
    });
  }

  function setupRevealAnimations(gsap, ScrollTrigger) {
    const revealItems = gsap.utils.toArray(".reveal");

    revealItems.forEach((el) => {
      if (el.dataset.saRevealAnimated === "true") return;
      el.dataset.saRevealAnimated = "true";

      const isHeroReveal = el.matches(
        ".hero__content, .about-hero__content, .work-hero__content, .philo-hero__inner, .contact-hero__copy, .wwm-hero__copy, .blog-hero__content, .legal-hero__inner"
      );

      if (isHeroReveal) {
        el.classList.add("is-visible");
        gsap.set(el, { autoAlpha: 1, y: 0, clearProps: "transform" });
        return;
      }

      const immediate = el.classList.contains("is-visible") && isInFirstView(el);

      if (immediate) {
        gsap.set(el, { autoAlpha: 1, y: 0, clearProps: "transform" });
        return;
      }

      gsap.fromTo(
        el,
        { autoAlpha: 0, y: 18 },
        {
          autoAlpha: 1,
          y: 0,
          duration: 0.76,
          ease: "power2.out",
          overwrite: "auto",
          onStart: () => el.classList.add("is-visible"),
          clearProps: "opacity,visibility,transform",
          scrollTrigger: {
            trigger: el,
            start: "top 86%",
            once: true,
          },
        }
      );

      const textTargets = getTextTargets(el);
      if (textTargets.length) {
        animateTextTargets(gsap, textTargets, {
          duration: 1.05,
          stagger: 0.055,
          scrollTrigger: {
            trigger: el,
            start: "top 86%",
            once: true,
          },
        });
      }
    });

    ScrollTrigger.refresh();
  }

  function setupGroupedStaggers(gsap, ScrollTrigger) {
    const groups = [
      ".pillars__grid",
      ".services__grid",
      ".highlight-strip__grid",
      ".who-i-am__grid",
      ".personal-note__grid",
      ".work-overview__grid",
      ".work-cards",
      ".work-process__grid",
      ".contact-services__grid",
      ".contact-info-grid",
    ];

    groups.forEach((selector) => {
      document.querySelectorAll(selector).forEach((group) => {
        if (group.dataset.saGroupAnimated === "true") return;

        const children = Array.from(group.children).filter((child) =>
          child.classList.contains("reveal")
        );

        if (children.length < 2) return;
        group.dataset.saGroupAnimated = "true";

        children.forEach((child) => {
          child.dataset.saRevealAnimated = "true";
          child.classList.add("is-visible");
        });

        gsap.fromTo(
          children,
          { autoAlpha: 0, y: 20 },
          {
            autoAlpha: 1,
            y: 0,
            duration: 0.74,
            ease: "power2.out",
            stagger: 0.08,
            overwrite: "auto",
            clearProps: "opacity,visibility,transform",
            scrollTrigger: {
              trigger: group,
              start: "top 84%",
              once: true,
            },
          }
        );

        children.forEach((child) => {
          const textTargets = getTextTargets(child);
          if (!textTargets.length) return;

          animateTextTargets(gsap, textTargets, {
            duration: 0.98,
            stagger: 0.04,
            scrollTrigger: {
              trigger: group,
              start: "top 84%",
              once: true,
            },
          });
        });
      });
    });

    ScrollTrigger.refresh();
  }

  function setupDirectionalMedia(gsap, ScrollTrigger) {
    getMediaTargets(document).forEach((el) => {
      el.dataset.saMediaAnimated = "true";
      el.classList.add("sa-media-reveal");

      const direction = getMediaDirection(el);
      const trigger = el.closest(".reveal") || el;

      gsap.fromTo(
        el,
        {
          autoAlpha: 0,
          x: direction * 46,
        },
        {
          autoAlpha: 1,
          x: 0,
          duration: 0.95,
          ease: "power4.out",
          overwrite: "auto",
          clearProps: "opacity,visibility,transform",
          scrollTrigger: {
            trigger,
            start: "top 86%",
            once: true,
          },
        }
      );
    });

    ScrollTrigger.refresh();
  }

  function setupSoftParallax(gsap) {
    const media = gsap.utils.toArray(
      ".hero, .about-hero, .work-hero__media, .wwm-hero__media, .philo-hero, .contact-hero"
    );

    media.forEach((el) => {
      if (el.dataset.saParallax === "true") return;
      el.dataset.saParallax = "true";

      gsap.to(el, {
        backgroundPositionY: "52%",
        ease: "none",
        scrollTrigger: {
          trigger: el,
          start: "top top",
          end: "bottom top",
          scrub: 1.2,
        },
      });
    });
  }

  function setupHoverPolish(gsap) {
    const hoverables = document.querySelectorAll(
      ".card, .pillar-card, .service-card, .work-card, .wwm-card, .contact-service-card, .blog-article-card, .blog-topic-card"
    );

    hoverables.forEach((el) => {
      if (el.dataset.saHover === "true") return;
      el.dataset.saHover = "true";

      el.addEventListener("mouseenter", () => {
        gsap.to(el, { y: -6, duration: 0.28, ease: "power2.out" });
      });

      el.addEventListener("mouseleave", () => {
        gsap.to(el, { y: 0, duration: 0.34, ease: "power2.out" });
      });
    });
  }

  onReady(async function init() {
    injectBaseStyles();

    if (prefersReducedMotion) {
      document.querySelectorAll(".reveal").forEach((el) => {
        el.classList.add("is-visible");
      });
      return;
    }

    const hasGsap = await ensureGsap();
    if (!hasGsap) {
      document.querySelectorAll(".reveal").forEach((el) => {
        el.classList.add("is-visible");
      });
      return;
    }

    const gsap = window.gsap;
    const ScrollTrigger = window.ScrollTrigger;

    gsap.config({ nullTargetWarn: false });
    setupPremiumCursor();
    syncSmoothScroll(ScrollTrigger);
    setupProgressBar(gsap, ScrollTrigger);
    setupHeroEntrance(gsap);
    setupGroupedStaggers(gsap, ScrollTrigger);
    setupRevealAnimations(gsap, ScrollTrigger);
    setupDirectionalMedia(gsap, ScrollTrigger);
    setupSoftParallax(gsap);
    setupHoverPolish(gsap);

    window.addEventListener("load", () => ScrollTrigger.refresh(), { once: true });
  });
})();
