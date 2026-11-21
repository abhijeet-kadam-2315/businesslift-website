/* ==========================================================================
   BusinessLift — main.js
   Site configuration + shared interactions (menu, FAQ, reveal, WhatsApp, social).
   Edit the CONFIG block below to change contact details or social profiles.
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- 1. CONFIG (edit here) ---------- */
  var CONFIG = {
    brandName: 'BusinessLift',
    phoneDisplay: '+91 9284569706',
    phoneTel: '+919284569706',
    whatsappNumber: '919284569706',
    email: 'kadamabhijeet2315@gmail.com',

    // Contact form endpoint (e.g. a Formspree / Web3Forms URL or your own backend).
    // Leave empty to use the WhatsApp / email fallback. See README.
    formEndpoint: '',

    // Social profiles: add a full https:// URL to show a link. Empty = hidden.
    social: { facebook: '', instagram: '', linkedin: '', youtube: '', x: '' }
  };

  /* ---------- 2. Contextual WhatsApp messages ---------- */
  var WA_MESSAGES = {
    general: "Hello BusinessLift, I'd like to book a free consultation about growing my business.",
    seo: "Hello BusinessLift, I'd like to know more about your SEO services for my business.",
    social: "Hello BusinessLift, I'm interested in social media management for my business.",
    website: "Hello BusinessLift, I'd like to discuss a website for my business.",
    ads: "Hello BusinessLift, I'd like to discuss Google Ads / Meta Ads management for my business.",
    branding: "Hello BusinessLift, I'd like to discuss branding and logo design for my business.",
    gbp: "Hello BusinessLift, I'd like help with my Google Business Profile.",
    leads: "Hello BusinessLift, I'd like to discuss lead generation for my business.",
    video: "Hello BusinessLift, I'm interested in reel and video editing.",
    design: "Hello BusinessLift, I'd like to discuss graphic and flyer design.",
    strategy: "Hello BusinessLift, I'd like a digital marketing strategy discussion for my business.",
    pricing: "Hello BusinessLift, I'd like to request a custom proposal for my business."
  };

  function waLink(message) {
    return 'https://wa.me/' + CONFIG.whatsappNumber + '?text=' + encodeURIComponent(message);
  }
  window.BL = { config: CONFIG, waLink: waLink, waMessages: WA_MESSAGES };

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 3. WhatsApp links ([data-wa="seo"]) ---------- */
  function initWhatsApp() {
    var links = document.querySelectorAll('[data-wa]');
    for (var i = 0; i < links.length; i++) {
      var key = links[i].getAttribute('data-wa');
      var msg = WA_MESSAGES[key] || WA_MESSAGES.general;
      links[i].setAttribute('href', waLink(msg));
      links[i].setAttribute('target', '_blank');
      links[i].setAttribute('rel', 'noopener noreferrer');
    }
  }

  /* ---------- 4. Mobile menu ---------- */
  function initMenu() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.getElementById('site-nav');
    if (!toggle || !nav) return;
    var desktop = window.matchMedia('(min-width: 1080px)');

    function setOpen(open) {
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); toggle.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('is-open') && !nav.contains(e.target) && !toggle.contains(e.target)) setOpen(false);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });
    var onChange = function () { if (desktop.matches) setOpen(false); };
    if (desktop.addEventListener) desktop.addEventListener('change', onChange); else desktop.addListener(onChange);
  }

  /* ---------- 5. Sticky header shadow ---------- */
  function initHeader() {
    var header = document.querySelector('[data-header]');
    if (!header) return;
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- 6. FAQ accordion ---------- */
  function initAccordion() {
    var buttons = Array.prototype.slice.call(document.querySelectorAll('.faq-q'));
    buttons.forEach(function (btn, idx) {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!open));
        if (panel) panel.hidden = open;
      });
      btn.addEventListener('keydown', function (e) {
        var next = null;
        if (e.key === 'ArrowDown') next = buttons[(idx + 1) % buttons.length];
        else if (e.key === 'ArrowUp') next = buttons[(idx - 1 + buttons.length) % buttons.length];
        else if (e.key === 'Home') next = buttons[0];
        else if (e.key === 'End') next = buttons[buttons.length - 1];
        if (next) { e.preventDefault(); next.focus(); }
      });
    });
  }

  /* ---------- 7. Scroll reveal ---------- */
  function initReveal() {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      for (var i = 0; i < items.length; i++) items[i].classList.add('is-visible');
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    for (var j = 0; j < items.length; j++) io.observe(items[j]);
  }

  /* ---------- 8. Move focus to in-page anchor targets ---------- */
  function initAnchors() {
    function focusTarget() {
      var id = decodeURIComponent(window.location.hash.slice(1));
      var el = id && document.getElementById(id);
      if (el) { if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1'); el.focus({ preventScroll: true }); }
    }
    window.addEventListener('hashchange', focusTarget);
  }

  /* ---------- 9. Social links (hidden until a URL is configured) ---------- */
  function initSocial() {
    var labels = { facebook: 'Facebook', instagram: 'Instagram', linkedin: 'LinkedIn', youtube: 'YouTube', x: 'X' };
    var wraps = document.querySelectorAll('[data-social-wrap]');
    for (var w = 0; w < wraps.length; w++) {
      var list = wraps[w].querySelector('[data-social-list]');
      var count = 0;
      Object.keys(labels).forEach(function (key) {
        var url = CONFIG.social[key];
        if (list && typeof url === 'string' && /^https:\/\//i.test(url)) {
          var a = document.createElement('a');
          a.href = url; a.textContent = labels[key];
          a.target = '_blank'; a.rel = 'noopener noreferrer';
          a.setAttribute('aria-label', 'BusinessLift on ' + labels[key] + ' (opens in a new tab)');
          list.appendChild(a); count++;
        }
      });
      if (count) wraps[w].hidden = false;
    }
  }

  /* ---------- 10. Footer year ---------- */
  function initYear() {
    var els = document.querySelectorAll('[data-year]');
    for (var i = 0; i < els.length; i++) els[i].textContent = String(new Date().getFullYear());
  }

  initWhatsApp(); initMenu(); initHeader(); initAccordion(); initReveal(); initAnchors(); initSocial(); initYear();
})();
