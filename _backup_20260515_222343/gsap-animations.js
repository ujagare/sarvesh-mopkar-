
/* =====================================================
   GSAP SCROLL ANIMATIONS — Sarvesh Mopkar Website
   Premium scroll-triggered text + image animations
   ===================================================== */

(function () {
  'use strict';

  // Wait for GSAP to be available
  if (typeof gsap === 'undefined') return;

  // Register ScrollTrigger plugin
  gsap.registerPlugin(ScrollTrigger);

  /* ── Sync with Lenis smooth scroll ── */
  if (window.Lenis) {
    const lenis = window.__lenis;
    if (lenis) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add((time) => lenis.raf(time * 1000));
      gsap.ticker.lagSmoothing(0);
    }
  }

  /* ─────────────────────────────────────
     UTILITY: split text into word spans
  ───────────────────────────────────── */
  function splitWords(el) {
    const text = el.innerHTML;
    // Don't split if it contains child elements (other than <br>)
    if (/<(?!br)[^>]+>/i.test(text)) return null;
    const words = text.split(' ');
    el.innerHTML = words
      .map((w) => `<span class="gsap-word" style="display:inline-block;overflow:hidden;"><span class="gsap-word-inner" style="display:inline-block;">${w}</span></span>`)
      .join(' ');
    return el.querySelectorAll('.gsap-word-inner');
  }

  /* ─────────────────────────────────────
     1. HERO SECTION
  ───────────────────────────────────── */
  const heroLines = document.querySelectorAll('.hero__line');
  if (heroLines.length) {
    gsap.fromTo(
      heroLines,
      { y: 60, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 1.1,
        ease: 'power3.out',
        stagger: 0.18,
        delay: 0.3,
      }
    );
  }

  const heroEyebrow = document.querySelector('.hero__content .eyebrow');
  if (heroEyebrow) {
    gsap.fromTo(
      heroEyebrow,
      { x: -40, opacity: 0 },
      { x: 0, opacity: 1, duration: 0.9, ease: 'power2.out', delay: 0.1 }
    );
  }

  const heroCopy = document.querySelector('.hero__copy');
  if (heroCopy) {
    gsap.fromTo(
      heroCopy,
      { y: 30, opacity: 0 },
      { y: 0, opacity: 1, duration: 1, ease: 'power2.out', delay: 0.7 }
    );
  }

  const heroActions = document.querySelector('.hero__actions');
  if (heroActions) {
    gsap.fromTo(
      heroActions,
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.9, ease: 'power2.out', delay: 0.95 }
    );
  }

  /* About-page hero */
  const aboutHeroTitle = document.querySelector('.about-hero__title');
  if (aboutHeroTitle) {
    gsap.fromTo(
      aboutHeroTitle,
      { y: 70, opacity: 0 },
      { y: 0, opacity: 1, duration: 1.2, ease: 'power3.out', delay: 0.2 }
    );
  }
  const aboutHeroText = document.querySelector('.about-hero__text');
  if (aboutHeroText) {
    gsap.fromTo(
      aboutHeroText,
      { y: 40, opacity: 0 },
      { y: 0, opacity: 1, duration: 1, ease: 'power2.out', delay: 0.55 }
    );
  }

  /* Work-page hero h1 */
  const workHeroH1 = document.querySelector('.work-hero h1');
  if (workHeroH1) {
    gsap.fromTo(
      workHeroH1,
      { y: 60, opacity: 0 },
      { y: 0, opacity: 1, duration: 1.2, ease: 'power3.out', delay: 0.3 }
    );
  }

  /* ─────────────────────────────────────
     2. SECTION HEADINGS (scroll-triggered)
  ───────────────────────────────────── */
  document.querySelectorAll('.section-head h2, .work-section-head h2, .about-section-title, .section-header h2').forEach((el) => {
    gsap.fromTo(
      el,
      { y: 50, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 1,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 88%',
          once: true,
        },
      }
    );
  });

  /* Eyebrow labels */
  document.querySelectorAll('.eyebrow, .about-label, .work-kicker').forEach((el) => {
    gsap.fromTo(
      el,
      { x: -30, opacity: 0 },
      {
        x: 0,
        opacity: 1,
        duration: 0.8,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 90%',
          once: true,
        },
      }
    );
  });

  /* Gold rule / dividers */
  document.querySelectorAll('.title-rule, .work-rule, .work-rule--center').forEach((el) => {
    gsap.fromTo(
      el,
      { scaleX: 0, transformOrigin: 'left center', opacity: 0 },
      {
        scaleX: 1,
        opacity: 1,
        duration: 0.9,
        ease: 'power2.inOut',
        scrollTrigger: {
          trigger: el,
          start: 'top 90%',
          once: true,
        },
      }
    );
  });

  /* ─────────────────────────────────────
     3. CARDS — staggered fade-up
  ───────────────────────────────────── */
  function animateCardGroup(selector, staggerDelay) {
    const groups = {};
    document.querySelectorAll(selector).forEach((card) => {
      const parent = card.parentElement;
      const key = parent ? parent.dataset.gsapGroup || (parent.dataset.gsapGroup = Math.random()) : 'solo';
      if (!groups[key]) groups[key] = [];
      groups[key].push(card);
    });

    Object.values(groups).forEach((cards) => {
      gsap.fromTo(
        cards,
        { y: 60, opacity: 0, scale: 0.97 },
        {
          y: 0,
          opacity: 1,
          scale: 1,
          duration: 0.85,
          ease: 'power3.out',
          stagger: staggerDelay || 0.14,
          scrollTrigger: {
            trigger: cards[0],
            start: 'top 87%',
            once: true,
          },
        }
      );
    });
  }

  animateCardGroup('.pillar-card', 0.14);
  animateCardGroup('.service-card', 0.14);
  animateCardGroup('.work-card', 0.16);
  animateCardGroup('.who-i-am__card', 0.12);
  animateCardGroup('.note-item', 0.12);
  animateCardGroup('.comparison-card', 0.18);

  /* ─────────────────────────────────────
     4. IMAGES — fade + slight scale
  ───────────────────────────────────── */
  document.querySelectorAll(
    '.pillar-card__image, .feature-banner__art, .about__media img, .about-hero__image-wrapper img, .journey-image-wrap img, .work-card__image img, .work-process__item img, .about-cta__bg img, .philosophy-bg-image img, .work-difference__panel img, .work-invite img'
  ).forEach((img) => {
    gsap.fromTo(
      img,
      { scale: 1.08, opacity: 0 },
      {
        scale: 1,
        opacity: 1,
        duration: 1.3,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: img,
          start: 'top 90%',
          once: true,
        },
      }
    );
  });

  /* ─────────────────────────────────────
     5. PARALLAX on large images
  ───────────────────────────────────── */
  document.querySelectorAll('.about-cta__bg img, .philosophy-bg-image img').forEach((img) => {
    gsap.to(img, {
      yPercent: 20,
      ease: 'none',
      scrollTrigger: {
        trigger: img.closest('section') || img,
        start: 'top bottom',
        end: 'bottom top',
        scrub: 1.5,
      },
    });
  });

  /* ─────────────────────────────────────
     6. VALUE / HIGHLIGHT STRIP items
  ───────────────────────────────────── */
  const stripItems = document.querySelectorAll('.value-strip__item, .highlight-item');
  if (stripItems.length) {
    gsap.fromTo(
      stripItems,
      { y: 40, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.8,
        ease: 'power2.out',
        stagger: 0.15,
        scrollTrigger: {
          trigger: stripItems[0],
          start: 'top 88%',
          once: true,
        },
      }
    );
  }

  /* Value strip statement */
  const stripStatement = document.querySelector('.value-strip__statement');
  if (stripStatement) {
    gsap.fromTo(
      stripStatement,
      { y: 30, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 1,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: stripStatement,
          start: 'top 88%',
          once: true,
        },
      }
    );
  }

  /* ─────────────────────────────────────
     7. PHILOSOPHY ITEMS
  ───────────────────────────────────── */
  const philItems = document.querySelectorAll('.philosophy__item');
  if (philItems.length) {
    gsap.fromTo(
      philItems,
      { y: 40, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.8,
        ease: 'power2.out',
        stagger: 0.18,
        scrollTrigger: {
          trigger: philItems[0],
          start: 'top 88%',
          once: true,
        },
      }
    );
  }

  /* ─────────────────────────────────────
     8. FEATURE BANNER
  ───────────────────────────────────── */
  const bannerCard = document.querySelector('.feature-banner__card');
  if (bannerCard) {
    const bannerImg = bannerCard.querySelector('.feature-banner__art');
    const bannerContent = bannerCard.querySelector('.feature-banner__content');
    const bannerAction = bannerCard.querySelector('.feature-banner__action');

    const tl = gsap.timeline({
      scrollTrigger: { trigger: bannerCard, start: 'top 82%', once: true },
    });
    if (bannerImg) tl.fromTo(bannerImg, { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 1, ease: 'power3.out' }, 0);
    if (bannerContent) tl.fromTo(bannerContent, { x: 50, opacity: 0 }, { x: 0, opacity: 1, duration: 1, ease: 'power3.out' }, 0.15);
    if (bannerAction) tl.fromTo(bannerAction, { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power2.out' }, 0.4);
  }

  /* ─────────────────────────────────────
     9. ABOUT GRID (image + content)
  ───────────────────────────────────── */
  const aboutMedia = document.querySelector('.about__media');
  const aboutContent = document.querySelector('.about__content');
  if (aboutMedia && aboutContent) {
    const tl = gsap.timeline({
      scrollTrigger: { trigger: aboutMedia.closest('section') || aboutMedia, start: 'top 82%', once: true },
    });
    tl.fromTo(aboutMedia, { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 1.1, ease: 'power3.out' }, 0);
    tl.fromTo(aboutContent, { x: 60, opacity: 0 }, { x: 0, opacity: 1, duration: 1.1, ease: 'power3.out' }, 0.15);
  }

  /* About page journey section */
  const journeyContent = document.querySelector('.journey__content');
  const journeyVisual = document.querySelector('.journey__visual');
  if (journeyContent && journeyVisual) {
    const tl = gsap.timeline({
      scrollTrigger: { trigger: journeyContent.closest('section') || journeyContent, start: 'top 82%', once: true },
    });
    tl.fromTo(journeyContent, { x: -50, opacity: 0 }, { x: 0, opacity: 1, duration: 1, ease: 'power3.out' }, 0);
    tl.fromTo(journeyVisual, { x: 50, opacity: 0 }, { x: 0, opacity: 1, duration: 1, ease: 'power3.out' }, 0.2);
  }

  /* ─────────────────────────────────────
     10. TESTIMONIAL STATS
  ───────────────────────────────────── */
  const stats = document.querySelectorAll('.testimonial-stat');
  if (stats.length) {
    gsap.fromTo(
      stats,
      { y: 40, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.8,
        ease: 'power2.out',
        stagger: 0.15,
        scrollTrigger: { trigger: stats[0], start: 'top 88%', once: true },
      }
    );
  }

  /* ─────────────────────────────────────
     11. FAQ ITEMS
  ───────────────────────────────────── */
  const faqItems = document.querySelectorAll('.faq__item');
  if (faqItems.length) {
    gsap.fromTo(
      faqItems,
      { y: 30, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.7,
        ease: 'power2.out',
        stagger: 0.1,
        scrollTrigger: { trigger: faqItems[0], start: 'top 88%', once: true },
      }
    );
  }

  /* ─────────────────────────────────────
     12. FINAL CTA
  ───────────────────────────────────── */
  const finalCta = document.querySelector('.final-cta__inner, .about-cta__content, .work-invite__inner');
  if (finalCta) {
    gsap.fromTo(
      finalCta,
      { y: 50, opacity: 0, scale: 0.97 },
      {
        y: 0,
        opacity: 1,
        scale: 1,
        duration: 1.1,
        ease: 'power3.out',
        scrollTrigger: { trigger: finalCta, start: 'top 85%', once: true },
      }
    );
  }

  /* ─────────────────────────────────────
     13. WORK PROCESS STEPS
  ───────────────────────────────────── */
  const processItems = document.querySelectorAll('.work-process__item');
  if (processItems.length) {
    gsap.fromTo(
      processItems,
      { y: 50, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.9,
        ease: 'power3.out',
        stagger: 0.2,
        scrollTrigger: { trigger: processItems[0], start: 'top 85%', once: true },
      }
    );
  }

  /* ─────────────────────────────────────
     14. WORK DIFFERENCE PANEL
  ───────────────────────────────────── */
  const diffPanel = document.querySelector('.work-difference__panel');
  if (diffPanel) {
    const diffCopy = diffPanel.querySelector('.work-difference__copy');
    const diffImg = diffPanel.querySelector('img');
    const tl = gsap.timeline({
      scrollTrigger: { trigger: diffPanel, start: 'top 82%', once: true },
    });
    if (diffCopy) tl.fromTo(diffCopy, { x: -50, opacity: 0 }, { x: 0, opacity: 1, duration: 1, ease: 'power3.out' }, 0);
    if (diffImg) tl.fromTo(diffImg, { x: 50, opacity: 0, scale: 1.05 }, { x: 0, opacity: 1, scale: 1, duration: 1.1, ease: 'power3.out' }, 0.15);
  }

  /* ─────────────────────────────────────
     15. FOOTER fade-up
  ───────────────────────────────────── */
  const footerCols = document.querySelectorAll('.footer__brand, .footer__column, .footer__newsletter');
  if (footerCols.length) {
    gsap.fromTo(
      footerCols,
      { y: 40, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.8,
        ease: 'power2.out',
        stagger: 0.12,
        scrollTrigger: { trigger: footerCols[0], start: 'top 92%', once: true },
      }
    );
  }

  /* ─────────────────────────────────────
     16. WORK OVERVIEW items
  ───────────────────────────────────── */
  const overviewItems = document.querySelectorAll('.work-overview__item');
  if (overviewItems.length) {
    gsap.fromTo(
      overviewItems,
      { y: 50, opacity: 0, scale: 0.97 },
      {
        y: 0,
        opacity: 1,
        scale: 1,
        duration: 0.8,
        ease: 'power3.out',
        stagger: 0.12,
        scrollTrigger: { trigger: overviewItems[0], start: 'top 87%', once: true },
      }
    );
  }

  /* ─────────────────────────────────────
     17. PHILOSOPHY PAGE SECTIONS
  ───────────────────────────────────── */
  document.querySelectorAll('.philosophy-section__content, .philosophy-section__visual').forEach((el, i) => {
    gsap.fromTo(
      el,
      { x: i === 0 ? -50 : 50, opacity: 0 },
      {
        x: 0,
        opacity: 1,
        duration: 1,
        ease: 'power3.out',
        scrollTrigger: { trigger: el, start: 'top 84%', once: true },
      }
    );
  });

  /* ─────────────────────────────────────
     18. HOVER microinteractions on cards
  ───────────────────────────────────── */
  document.querySelectorAll('.pillar-card, .service-card, .work-card article, .who-i-am__card').forEach((card) => {
    card.addEventListener('mouseenter', () => {
      gsap.to(card, { y: -6, duration: 0.35, ease: 'power2.out' });
    });
    card.addEventListener('mouseleave', () => {
      gsap.to(card, { y: 0, duration: 0.4, ease: 'power2.inOut' });
    });
  });

  /* ─────────────────────────────────────
     19. BUTTON hover microinteractions
  ───────────────────────────────────── */
  document.querySelectorAll('.btn').forEach((btn) => {
    btn.addEventListener('mouseenter', () => {
      gsap.to(btn.querySelector('.btn__arrow'), { x: 5, duration: 0.3, ease: 'power2.out' });
    });
    btn.addEventListener('mouseleave', () => {
      gsap.to(btn.querySelector('.btn__arrow'), { x: 0, duration: 0.3, ease: 'power2.inOut' });
    });
  });

  /* ─────────────────────────────────────
     20. HEADER logo subtle entrance
  ───────────────────────────────────── */
  const brand = document.querySelector('.brand__mark');
  if (brand) {
    gsap.fromTo(brand, { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 1, ease: 'power2.out', delay: 0.1 });
  }

  /* ─────────────────────────────────────
     21. COMPARISON section
  ───────────────────────────────────── */
  const compVs = document.querySelector('.comparison-vs');
  if (compVs) {
    gsap.fromTo(
      compVs,
      { scale: 0.5, opacity: 0, rotation: -15 },
      {
        scale: 1,
        opacity: 1,
        rotation: 0,
        duration: 0.9,
        ease: 'back.out(1.7)',
        scrollTrigger: { trigger: compVs, start: 'top 85%', once: true },
      }
    );
  }

  /* ─────────────────────────────────────
     22. JOURNEY LIST ITEMS
  ───────────────────────────────────── */
  const journeyListItems = document.querySelectorAll('.journey-list li');
  if (journeyListItems.length) {
    gsap.fromTo(
      journeyListItems,
      { x: -30, opacity: 0 },
      {
        x: 0,
        opacity: 1,
        duration: 0.7,
        ease: 'power2.out',
        stagger: 0.15,
        scrollTrigger: { trigger: journeyListItems[0], start: 'top 88%', once: true },
      }
    );
  }

  /* ─────────────────────────────────────
     23. WORK-WITH-ME page specifics
  ───────────────────────────────────── */
  document.querySelectorAll('.wwm-hero__title, .wwm-hero__sub, .wwm-hero__intro').forEach((el, i) => {
    gsap.fromTo(
      el,
      { y: 50, opacity: 0 },
      { y: 0, opacity: 1, duration: 1, ease: 'power3.out', delay: 0.2 + i * 0.18 }
    );
  });

  /* Offering cards on work-with-me */
  const offeringCards = document.querySelectorAll('.offering-card, .wwm-card');
  if (offeringCards.length) {
    gsap.fromTo(
      offeringCards,
      { y: 60, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.9,
        ease: 'power3.out',
        stagger: 0.16,
        scrollTrigger: { trigger: offeringCards[0], start: 'top 86%', once: true },
      }
    );
  }

  /* Contact form */
  const contactForm = document.querySelector('[data-contact-form]');
  if (contactForm) {
    gsap.fromTo(
      contactForm,
      { y: 50, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 1,
        ease: 'power3.out',
        scrollTrigger: { trigger: contactForm, start: 'top 85%', once: true },
      }
    );
  }

  /* ─────────────────────────────────────
     24. SECTION HORIZONTAL DIVIDERS
  ───────────────────────────────────── */
  document.querySelectorAll('.highlight-divider, .value-strip__divider, .philosophy__divider').forEach((el) => {
    gsap.fromTo(
      el,
      { scaleY: 0, opacity: 0 },
      {
        scaleY: 1,
        opacity: 1,
        duration: 0.6,
        ease: 'power2.inOut',
        scrollTrigger: { trigger: el, start: 'top 90%', once: true },
      }
    );
  });

  /* ─────────────────────────────────────
     25. TESTIMONIALS SECTION HEAD
  ───────────────────────────────────── */
  const testimHead = document.querySelector('.testimonials .section-head');
  if (testimHead) {
    gsap.fromTo(
      testimHead,
      { y: 40, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.9,
        ease: 'power2.out',
        scrollTrigger: { trigger: testimHead, start: 'top 88%', once: true },
      }
    );
  }

  /* ─────────────────────────────────────
     26. FLOATING LOTUS (about page)
  ───────────────────────────────────── */
  const lotus = document.querySelector('.floating-lotus');
  if (lotus) {
    gsap.to(lotus, {
      y: -18,
      duration: 3,
      ease: 'sine.inOut',
      repeat: -1,
      yoyo: true,
    });
  }

})();
