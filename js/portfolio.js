/* ==========================================================================
   BusinessLift — portfolio.js
   Data-driven, filterable portfolio.

   TO ADD GENUINE WORK: add an object to PORTFOLIO_ITEMS (or replace a sample)
   and set isSample to false. Fields:
     title        Project title
     category     One of CATEGORIES below
     description  Short project description
     image        Path to an image, e.g. 'assets/images/work/project-1.webp' ('' = placeholder)
     imageAlt     Descriptive alt text for the image
     services     Array of services delivered
     results      OPTIONAL. Only add VERIFIED results. Leave '' to hide the block.
     isSample     true = shows a "Sample concept" badge. Set false for real client work.
   ========================================================================== */
(function () {
  'use strict';

  var grid = document.getElementById('portfolio-grid');
  var filterBar = document.getElementById('portfolio-filters');
  var countEl = document.getElementById('portfolio-count');
  if (!grid || !filterBar) return;

  var CATEGORIES = ['Branding', 'Graphic Design', 'Social Media', 'Websites', 'SEO', 'Advertising'];

  var PORTFOLIO_ITEMS = [
    {
      title: 'Restaurant Brand Identity',
      category: 'Branding',
      description: 'A concept showing a logo direction, colour palette and typography pairing for a neighbourhood restaurant.',
      image: '', imageAlt: 'Concept artwork for a restaurant brand identity',
      services: ['Logo concepts', 'Colour palette', 'Typography'], results: '', isSample: true
    },
    {
      title: 'Festival Offer Flyer Series',
      category: 'Graphic Design',
      description: 'A flyer layout concept for a retail festive promotion, designed for both print and WhatsApp sharing.',
      image: '', imageAlt: 'Concept artwork for a festive promotional flyer',
      services: ['Flyer design', 'Print-ready files', 'Social variants'], results: '', isSample: true
    },
    {
      title: 'Clinic Social Media Calendar',
      category: 'Social Media',
      description: 'A sample monthly content plan for a clinic: educational posts, announcements and patient-friendly reminders.',
      image: '', imageAlt: 'Concept layout of a monthly social media content calendar',
      services: ['Content planning', 'Post design', 'Caption writing'], results: '', isSample: true
    },
    {
      title: 'Short-Form Reel Concept',
      category: 'Social Media',
      description: 'A storyboard-style concept for a 20-second product reel with subtitles and vertical formatting.',
      image: '', imageAlt: 'Concept storyboard for a short-form product reel',
      services: ['Reel editing', 'Subtitles', 'Vertical formatting'], results: '', isSample: true
    },
    {
      title: 'Service Business Website Layout',
      category: 'Websites',
      description: 'A responsive homepage layout concept with a clear enquiry path for a local service provider.',
      image: '', imageAlt: 'Concept wireframe of a service business website',
      services: ['Responsive design', 'Landing page', 'Enquiry form'], results: '', isSample: true
    },
    {
      title: 'Professional Firm Website Concept',
      category: 'Websites',
      description: 'A trust-focused website concept for a professional practice, with service pages and contact options.',
      image: '', imageAlt: 'Concept layout of a professional firm website',
      services: ['Website design', 'Content structure', 'UX improvements'], results: '', isSample: true
    },
    {
      title: 'Google Business Profile Audit Format',
      category: 'SEO',
      description: 'A sample audit format covering profile completeness, categories, photos, posts and review handling.',
      image: '', imageAlt: 'Concept of a Google Business Profile audit checklist',
      services: ['Profile audit', 'Local SEO', 'Recommendations'], results: '', isSample: true
    },
    {
      title: 'Lead Campaign Structure',
      category: 'Advertising',
      description: 'A sample campaign structure for a solar installer: audiences, ad groups, landing page and lead tracking.',
      image: '', imageAlt: 'Concept diagram of an advertising campaign structure',
      services: ['Campaign planning', 'Audience research', 'Lead tracking'], results: '', isSample: true
    },
    {
      title: 'E-commerce Ad Creative Set',
      category: 'Advertising',
      description: 'A concept set of ad creatives in square and vertical formats for an online store promotion.',
      image: '', imageAlt: 'Concept set of e-commerce advertising creatives',
      services: ['Ad creatives', 'Meta Ads planning', 'Creative testing plan'], results: '', isSample: true
    }
  ];

  var ICONS = {
    'Branding': '<path d="M12 3a9 9 0 1 0 0 18c1.1 0 1.8-.9 1.5-1.9-.3-1 .4-2.1 1.5-2.1H17a4 4 0 0 0 4-4c0-5-4-10-9-10z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
    'Graphic Design': '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    'Social Media': '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="m8.2 10.8 7.6-3.6M8.2 13.2l7.6 3.6"/>',
    'Websites': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 20V9"/>',
    'SEO': '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    'Advertising': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>'
  };

  var active = 'All';

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }
  function svgIcon(category) {
    var wrap = document.createElement('span');
    wrap.innerHTML = '<svg class="icon" width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + (ICONS[category] || '') + '</svg>';
    return wrap.firstChild; // static, trusted markup only
  }

  function buildCard(item) {
    var card = el('li', 'card work-card');
    card.setAttribute('data-category', item.category);

    var thumb = el('div', 'thumb');
    if (item.image) {
      var img = el('img');
      img.src = item.image; img.alt = item.imageAlt || item.title;
      img.loading = 'lazy'; img.decoding = 'async'; img.width = 800; img.height = 500;
      thumb.appendChild(img);
    } else {
      thumb.appendChild(svgIcon(item.category));
      thumb.appendChild(el('span', 'thumb-label', item.category));
    }
    if (item.isSample) thumb.appendChild(el('span', 'badge', 'Sample concept'));
    card.appendChild(thumb);

    var body = el('div', 'work-body');
    body.appendChild(el('p', 'cat-label', item.category));
    body.appendChild(el('h3', '', item.title));
    body.appendChild(el('p', '', item.description));

    if (item.services && item.services.length) {
      var tags = el('ul', 'tag-list');
      tags.setAttribute('aria-label', 'Services delivered');
      item.services.forEach(function (s) { tags.appendChild(el('li', '', s)); });
      body.appendChild(tags);
    }
    if (item.results) body.appendChild(el('p', 'result-box', 'Verified result: ' + item.results));

    var link = el('a', 'btn btn-secondary btn-sm', item.isSample ? 'Discuss a Similar Project' : 'Discuss a Project Like This');
    var text = "Hello BusinessLift, I saw \"" + item.title + "\" on your Our Work page and would like to discuss something similar for my business.";
    link.href = window.BL ? window.BL.waLink(text) : 'https://wa.me/919284569706';
    link.target = '_blank'; link.rel = 'noopener noreferrer';
    link.setAttribute('aria-label', 'Discuss a project like ' + item.title + ' on WhatsApp (opens in a new tab)');
    body.appendChild(link);

    card.appendChild(body);
    return card;
  }

  function render() {
    grid.textContent = '';
    var shown = 0;
    PORTFOLIO_ITEMS.forEach(function (item) {
      if (active === 'All' || item.category === active) { grid.appendChild(buildCard(item)); shown++; }
    });
    if (countEl) countEl.textContent = 'Showing ' + shown + (shown === 1 ? ' project' : ' projects') + (active === 'All' ? '' : ' in ' + active) + '.';
  }

  function buildFilters() {
    ['All'].concat(CATEGORIES).forEach(function (cat) {
      var btn = el('button', 'filter-btn', cat);
      btn.type = 'button';
      btn.setAttribute('aria-pressed', cat === active ? 'true' : 'false');
      btn.addEventListener('click', function () {
        active = cat;
        var all = filterBar.querySelectorAll('.filter-btn');
        for (var i = 0; i < all.length; i++) all[i].setAttribute('aria-pressed', all[i] === btn ? 'true' : 'false');
        render();
      });
      filterBar.appendChild(btn);
    });
  }

  buildFilters();
  render();
})();
