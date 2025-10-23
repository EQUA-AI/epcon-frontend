// EPCON Frontend Tweaks JS fallback
// Dynamically mark help / documentation / getting started / about links for hiding when CSS selectors miss dynamic insertion.

(function() {
  const KEYWORDS = [
    'Documentation', 'Getting Started', 'About'
  ];
  const HREF_PARTS = [
    '/docs', '/documentation', '/getting-started', '/about', 'docs.inventree.org'
  ];

  function shouldHide(el) {
    if (!el) return false;
    const text = (el.textContent || '').trim();
    for (const k of KEYWORDS) {
      if (text.toLowerCase().includes(k.toLowerCase())) return true;
    }
    if (el.getAttribute) {
      const href = el.getAttribute('href') || '';
      for (const h of HREF_PARTS) {
        if (href.includes(h)) return true;
      }
      const title = el.getAttribute('title') || '';
      const aria = el.getAttribute('aria-label') || '';
      const testId = el.getAttribute('data-test') || '';
      const combined = [title, aria, testId].join(' ').toLowerCase();
      for (const k of KEYWORDS) {
        if (combined.includes(k.toLowerCase())) return true;
      }
    }
    return false;
  }

  function mark() {
    const candidates = document.querySelectorAll('a, button, li, div, span');
    candidates.forEach(el => {
      if (shouldHide(el)) {
        el.setAttribute('data-epcon-hidden', 'true');
      }
    });
  }

  // Initial run
  mark();
  // Observe for future dynamic insertions
  const obs = new MutationObserver(() => mark());
  obs.observe(document.documentElement, { childList: true, subtree: true });
})();