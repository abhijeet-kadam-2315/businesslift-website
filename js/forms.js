/* ==========================================================================
   BusinessLift — forms.js
   Contact form: validation + submission.
   - If CONFIG.formEndpoint is set (main.js), the enquiry is POSTed there.
   - Otherwise nothing is sent automatically: the visitor is offered a prepared
     WhatsApp message and a prepared email to send manually.
   Submitted details are never stored in localStorage/sessionStorage.
   ========================================================================== */
(function () {
  'use strict';

  var form = document.getElementById('contact-form');
  if (!form) return;

  var BL = window.BL || { config: {}, waLink: function (m) { return 'https://wa.me/919284569706?text=' + encodeURIComponent(m); } };
  var cfg = BL.config || {};
  var endpoint = (cfg.formEndpoint || '').trim();
  var alertBox = form.querySelector('.form-alert');
  var resultBox = document.getElementById('form-result');
  var submitBtn = form.querySelector('[type="submit"]');
  var modeNote = document.querySelector('[data-form-mode-note]');

  /* ---- Describe how the form works right now ---- */
  if (endpoint) {
    if (modeNote) modeNote.textContent = 'Your enquiry will be sent to BusinessLift through our secure form service. We will contact you using the details you provide.';
    if (submitBtn) submitBtn.textContent = 'Send Enquiry';
  }

  /* ---- Prefill from query string (?plan=Growth) ---- */
  (function prefill() {
    try {
      var params = new URLSearchParams(window.location.search);
      var plan = (params.get('plan') || '').slice(0, 40);
      var msg = form.elements.message;
      if (plan && msg && !msg.value) msg.value = "I'm interested in the " + plan + " package and would like a custom proposal.";
    } catch (e) { /* ignore */ }
  })();

  /* ---- Validators: return an error string or '' ---- */
  var validators = {
    name: function (v) { return v.trim().length >= 2 ? '' : 'Please enter your full name.'; },
    phone: function (v) {
      var digits = v.replace(/[\s\-().]/g, '');
      if (!digits) return 'Please enter your phone number.';
      if (/^(\+91|91|0)?[6-9]\d{9}$/.test(digits)) return '';
      if (/^\+\d{8,15}$/.test(digits)) return '';
      return 'Enter a valid 10-digit mobile number (or include a country code, e.g. +91).';
    },
    email: function (v) {
      var val = v.trim();
      if (!val) return 'Please enter your email address.';
      return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val) ? '' : 'Please enter a valid email address.';
    },
    consent: function (checked) { return checked ? '' : 'Please confirm your consent so we can respond to your enquiry.'; }
  };

  function field(name) { return form.elements[name]; }
  function errEl(name) { return document.getElementById('err-' + name); }

  function setError(name, message) {
    var input = field(name); var el = errEl(name);
    if (el) el.textContent = message;
    if (input) { if (message) input.setAttribute('aria-invalid', 'true'); else input.removeAttribute('aria-invalid'); }
  }

  function validateField(name) {
    var input = field(name);
    if (!input || !validators[name]) return true;
    var msg = name === 'consent' ? validators.consent(input.checked) : validators[name](input.value);
    setError(name, msg);
    return !msg;
  }

  ['name', 'phone', 'email'].forEach(function (n) {
    var input = field(n);
    if (!input) return;
    input.addEventListener('blur', function () { validateField(n); });
    input.addEventListener('input', function () { if (input.getAttribute('aria-invalid') === 'true') validateField(n); });
  });
  if (field('consent')) field('consent').addEventListener('change', function () { validateField('consent'); });

  /* ---- Gather data ---- */
  function collect() {
    var services = [];
    var boxes = form.querySelectorAll('input[name="services"]:checked');
    for (var i = 0; i < boxes.length; i++) services.push(boxes[i].value);
    return {
      name: field('name').value.trim(),
      business: field('business').value.trim(),
      phone: field('phone').value.trim(),
      email: field('email').value.trim(),
      industry: field('industry').value,
      services: services,
      budget: field('budget').value,
      message: field('message').value.trim()
    };
  }

  function buildText(d) {
    var lines = ["Hello BusinessLift, I'd like to discuss my business requirements.", ''];
    lines.push('Name: ' + d.name);
    if (d.business) lines.push('Business: ' + d.business);
    lines.push('Phone: ' + d.phone);
    lines.push('Email: ' + d.email);
    if (d.industry) lines.push('Industry: ' + d.industry);
    if (d.services.length) lines.push('Services needed: ' + d.services.join(', '));
    if (d.budget) lines.push('Estimated monthly budget: ' + d.budget);
    if (d.message) { lines.push(''); lines.push('Message: ' + d.message); }
    return lines.join('\n');
  }

  /* ---- Result panel (built with DOM methods; no innerHTML) ---- */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  function showResult(kind, data) {
    resultBox.textContent = '';
    resultBox.hidden = false;
    resultBox.className = 'form-result' + (kind === 'sent' ? ' is-success' : '');

    if (kind === 'sent') {
      resultBox.appendChild(el('h3', '', 'Enquiry submitted'));
      resultBox.appendChild(el('p', '', 'Thank you. Your enquiry was passed to our form service. We will review it and get back to you using the phone number or email you provided.'));
    } else if (kind === 'error') {
      resultBox.appendChild(el('h3', '', 'We could not submit the form'));
      resultBox.appendChild(el('p', '', 'Something went wrong while sending your enquiry. Nothing has been received by BusinessLift. Please use one of the options below instead.'));
    } else {
      resultBox.appendChild(el('h3', '', 'Your enquiry is ready, but not sent yet'));
      resultBox.appendChild(el('p', '', 'This website is not connected to an automatic submission service. Your details have not been sent to BusinessLift. Choose how you would like to send them: the message is prepared for you, and you press Send yourself.'));
    }

    if (kind !== 'sent') {
      var text = buildText(data);
      var row = el('div', 'btn-row');
      var wa = el('a', 'btn btn-whatsapp', 'Send via WhatsApp');
      wa.href = BL.waLink(text); wa.target = '_blank'; wa.rel = 'noopener noreferrer';
      var mail = el('a', 'btn btn-secondary', 'Send via Email');
      mail.href = 'mailto:' + (cfg.email || 'kadamabhijeet2315@gmail.com') +
        '?subject=' + encodeURIComponent('Enquiry from ' + data.name + (data.business ? ' (' + data.business + ')' : '')) +
        '&body=' + encodeURIComponent(text);
      row.appendChild(wa); row.appendChild(mail);
      resultBox.appendChild(row);
      resultBox.appendChild(el('p', 'form-note', 'WhatsApp opens in a new tab and your email app opens with the message filled in. Nothing is sent until you press Send there.'));
    }
    resultBox.setAttribute('tabindex', '-1');
    resultBox.focus();
  }

  /* ---- Submit ---- */
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (alertBox) { alertBox.hidden = true; alertBox.textContent = ''; }
    resultBox.hidden = true;

    // Honeypot: bots fill hidden fields. Quietly stop.
    if (field('website') && field('website').value) return;

    var order = ['name', 'phone', 'email', 'consent'];
    var firstInvalid = null;
    order.forEach(function (n) { if (!validateField(n) && !firstInvalid) firstInvalid = field(n); });

    if (firstInvalid) {
      if (alertBox) { alertBox.textContent = 'Please correct the highlighted fields and try again.'; alertBox.hidden = false; }
      firstInvalid.focus();
      return;
    }

    var data = collect();

    if (!endpoint) { showResult('fallback', data); return; }

    submitBtn.disabled = true;
    var original = submitBtn.textContent;
    submitBtn.textContent = 'Sending…';

    var payload = new FormData();
    payload.append('name', data.name); payload.append('business', data.business);
    payload.append('phone', data.phone); payload.append('email', data.email);
    payload.append('industry', data.industry); payload.append('services', data.services.join(', '));
    payload.append('budget', data.budget); payload.append('message', data.message);
    payload.append('_subject', 'New BusinessLift website enquiry');

    fetch(endpoint, { method: 'POST', body: payload, headers: { Accept: 'application/json' } })
      .then(function (res) {
        if (!res.ok) throw new Error('Bad response');
        form.reset();
        showResult('sent', data);
      })
      .catch(function () { showResult('error', data); })
      .then(function () { submitBtn.disabled = false; submitBtn.textContent = original; });
  });
})();
