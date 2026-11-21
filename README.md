# BusinessLift Website

Static, framework-free website for **BusinessLift — Lift Your Business. Grow Your Brand.**
Built with HTML5, CSS3 and vanilla JavaScript. No build step is required to run it.

## Project structure

```
businesslift-website/
├── index.html, about.html, services.html, industries.html, portfolio.html,
│   case-studies.html, pricing.html, blog.html, contact.html,
│   privacy-policy.html, terms.html, blog-post-template.html (noindex)
├── assets/ images/ (og-image.png) · icons/ (favicon.svg) · logo/ (logo-temporary.svg)
├── css/ styles.css (tokens + components) · responsive.css (breakpoints)
├── js/  main.js (config, menu, FAQ, reveal, WhatsApp, social) · forms.js · portfolio.js
├── build.py   (optional page generator)
├── sitemap.xml, robots.txt
└── README.md
```

## 1. Run locally

Open `index.html` directly, or serve the folder (recommended):

```bash
cd businesslift-website
python3 -m http.server 8000
# open http://localhost:8000
```

## 2. Editing content: two ways

- **Direct:** edit the `.html` files. Header and footer repeat on each page, so shared changes must be made in every file.
- **Generator (optional):** edit `build.py`, then run `python3 build.py`. It regenerates every page, `sitemap.xml` and `robots.txt` from one place. Note: it overwrites the HTML files, so don't mix both ways without care.

## 3. Replace the logo and images

The logo is a **temporary text-based BL monogram**, not the official logo.

1. Put your logo in `assets/logo/` (e.g. `logo.svg`).
2. In `build.py`, edit the `logo()` function to output `<img src="assets/logo/logo.svg" alt="BusinessLift" width="170" height="44">`, then run `python3 build.py`. (Without the generator, replace the `<a class="logo">…</a>` block in each HTML file.)
3. Replace `assets/icons/favicon.svg` with your favicon.
4. Replace `assets/images/og-image.png` with a **1200×630** branded PNG for social sharing (the current one is a simple placeholder).
5. Portfolio images: see section 8.

## 4. Update phone, email and WhatsApp

Contact details appear in several places. Search the whole project for these strings and replace them:

| Detail | Search for |
|---|---|
| Phone (display) | `+91 9284569706` |
| Phone link | `+919284569706` |
| WhatsApp number | `919284569706` |
| Email | `kadamabhijeet2315@gmail.com` |

Also update the `CONFIG` block at the top of `js/main.js` and the `SITE` block in `build.py`.

**Social profiles:** in `js/main.js`, set `CONFIG.social` (e.g. `instagram: 'https://www.instagram.com/yourpage'`). Links appear in the footer only when a URL is provided.

## 5. Connect the contact form

By default **no data is sent anywhere automatically**. After validation, the visitor sees a clear message and can send the prepared enquiry via WhatsApp or email.

To connect a real endpoint, set `formEndpoint` in `js/main.js`:

```js
formEndpoint: 'https://formspree.io/f/your-form-id',   // or Web3Forms, Getform, your own API
```

The form then POSTs `multipart/form-data` (fields: name, business, phone, email, industry, services, budget, message) and shows a success message only when the endpoint returns an OK response. Also update the Privacy Policy "How contact-form enquiries are processed" section.

If you build your own backend, you must add server-side validation, spam protection (rate limiting, CAPTCHA or similar), CORS configuration for your domain, and secure storage. **Never put API keys or secrets in front-end code.** Submitted details are never saved in localStorage.

## 6. Set the real domain and canonical URLs

All canonical, Open Graph, sitemap and robots URLs use the placeholder `https://www.your-domain.com`.

- With the generator: change `SITE["base"]` in `build.py` and run `python3 build.py`.
- Without it: search and replace `https://www.your-domain.com` across all `.html`, `sitemap.xml` and `robots.txt`.

Then submit `sitemap.xml` in Google Search Console.

## 7. Deploy to static hosting

Upload the whole folder (you can skip `build.py` and `README.md`) to any static host:

- **Netlify / Cloudflare Pages / Vercel:** connect a Git repo or drag-and-drop the folder; no build command; publish directory is the project root.
- **GitHub Pages:** push to a repo and enable Pages from the branch root.
- **cPanel / shared hosting:** upload files to `public_html`.

Then connect your domain, enable HTTPS, and verify every page loads with the production URL.

## 8. Portfolio, pricing, blog, testimonials

- **Portfolio:** edit `PORTFOLIO_ITEMS` in `js/portfolio.js`. Set `image`, `imageAlt`, `services`, optional *verified* `results`, and `isSample: false` for genuine work. Put images in `assets/images/work/` (use WebP/JPEG, about 800×500).
- **Pricing:** replace the text `Custom quote` (marked `data-package-price`) with a real price, and adjust included services and exclusions.
- **Blog:** duplicate `blog-post-template.html`, fill in real content, date and author, and link it from `blog.html`. Remove the `noindex` meta tag and add the page to `sitemap.xml`.
- **Case studies:** use the `<template id="case-study-template">` in `case-studies.html` with verified information only.
- **Testimonials:** the homepage shows an invitation instead of quotes. Add genuine, permitted testimonials there when available.

## 9. Content & compliance notes

- No office address, testimonials, statistics, awards or results are invented.
- Privacy Policy and Terms are **starter templates, not legal advice**; have them reviewed.
- Google Fonts (Manrope) is loaded from the CDN. Mention it in your privacy policy.

## 10. Final launch checklist

**Responsiveness**
- [ ] Check 360px, 390px, 768px, 1024px, 1280px and 1920px widths
- [ ] No horizontal scrolling on any page
- [ ] Mobile menu opens, closes (button, Esc, link click) and the current page is highlighted
- [ ] Pricing table scrolls sideways on small screens
- [ ] Floating WhatsApp button does not hide key content

**Links & functionality**
- [ ] All navigation, footer and CTA links go to real pages
- [ ] Phone, email and WhatsApp links work (and open the right number/address)
- [ ] Contextual WhatsApp messages differ by service
- [ ] FAQ accordion works with mouse and keyboard
- [ ] Portfolio filters work
- [ ] Contact form: required-field, email and phone errors appear; fallback panel (or your endpoint) works; no false "sent" message

**SEO**
- [ ] Real domain set in canonical URLs, Open Graph, sitemap, robots
- [ ] Each page has a unique title and description
- [ ] 1200×630 social image replaced
- [ ] Structured data passes Google's Rich Results Test
- [ ] Sitemap submitted to Search Console

**Accessibility**
- [ ] Tab through every page: visible focus, logical order, skip link works
- [ ] Meets colour contrast (run Lighthouse / axe)
- [ ] Form fields have labels and errors are announced
- [ ] Content is usable with `prefers-reduced-motion` enabled
- [ ] Lighthouse scores reviewed for Performance, Accessibility, SEO, Best Practices
