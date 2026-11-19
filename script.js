// Social Pulse — small interactive bits
(function () {
  // Mobile menu
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
  }

  // Highlight current page in the menu
  const norm = (p) => p.replace(/index\.html$/, '').replace(/\/+$/, '') || '/';
  const page = norm(location.pathname);
  document.querySelectorAll('.site-nav a').forEach((a) => {
    if (norm(new URL(a.href, location.href).pathname) === page) a.classList.add('active');
  });

  // Footer year
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Scroll reveal
  const els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    els.forEach((el) => io.observe(el));
  } else {
    els.forEach((el) => el.classList.add('in'));
  }

  // Engagement rate calculator
  const form = document.getElementById('calcForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const n = (id) => Math.max(0, parseFloat(document.getElementById(id).value) || 0);
      const total = n('likes') + n('comments') + n('shares') + n('saves');
      const base = n('base');
      const out = document.getElementById('calcResult');
      if (!base) { out.textContent = 'Enter your reach or follower count to calculate.'; return; }
      const rate = (total / base) * 100;
      let verdict = 'Below average. Try a stronger hook or a clearer call-to-action.';
      if (rate >= 6) verdict = 'Excellent! Study this post and make more like it.';
      else if (rate >= 3) verdict = 'Strong. Your audience is paying attention.';
      else if (rate >= 1) verdict = 'Average. Solid, with room to grow.';
      out.innerHTML = '<strong>' + rate.toFixed(2) + '%</strong>' + total.toLocaleString() + ' interactions. ' + verdict;
    });
  }

  // Checklist with saved progress
  const list = document.getElementById('checklistItems');
  if (list) {
    const boxes = list.querySelectorAll('input[type="checkbox"]');
    const key = 'socialpulse-checklist-' + page;
    let saved = [];
    try { saved = JSON.parse(localStorage.getItem(key)) || []; } catch (_) {}
    boxes.forEach((b, i) => { b.checked = !!saved[i]; });
    const update = () => {
      const done = [...boxes].filter((b) => b.checked).length;
      document.getElementById('progressBar').style.width = (done / boxes.length) * 100 + '%';
      document.getElementById('progressText').textContent = done + ' of ' + boxes.length + ' done' + (done === boxes.length ? ' 🎉 Ready to post!' : '');
      try { localStorage.setItem(key, JSON.stringify([...boxes].map((b) => b.checked))); } catch (_) {}
    };
    boxes.forEach((b) => b.addEventListener('change', update));
    const reset = document.getElementById('resetChecklist');
    if (reset) reset.addEventListener('click', () => { boxes.forEach((b) => (b.checked = false)); update(); });
    update();
  }
})();
