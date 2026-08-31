(function () {
  'use strict';

  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Mobile drawer ---------- */
  var sidebar = document.getElementById('sidebar');
  var toggle = document.getElementById('drawerToggle');
  var overlay = document.getElementById('drawerOverlay');

  function openDrawer() {
    sidebar.classList.add('open');
    overlay.classList.add('active');
    toggle.setAttribute('aria-expanded', 'true');
  }
  function closeDrawer() {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
    toggle.setAttribute('aria-expanded', 'false');
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      sidebar.classList.contains('open') ? closeDrawer() : openDrawer();
    });
  }
  if (overlay) overlay.addEventListener('click', closeDrawer);
  sidebar && sidebar.querySelectorAll('.sidebar-link').forEach(function (link) {
    link.addEventListener('click', closeDrawer);
  });

  /* ---------- Scroll reveal (Intersection Observer) ---------- */
  var revealEls = document.querySelectorAll('[data-reveal]');
  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('revealed'); });
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { observer.observe(el); });
  }

  /* ---------- Active section highlight in sidebar (homepage only) ---------- */
  var sectionLinks = document.querySelectorAll('.sidebar-link[data-section]');
  if (sectionLinks.length) {
    var sections = [];
    sectionLinks.forEach(function (link) {
      var id = link.getAttribute('data-section');
      var section = document.getElementById(id);
      if (section) sections.push({ id: id, el: section, link: link });
    });

    var spyObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var match = sections.find(function (s) { return s.el === entry.target; });
        if (!match) return;
        if (entry.isIntersecting) {
          sectionLinks.forEach(function (l) { l.classList.remove('active'); });
          match.link.classList.add('active');
        }
      });
    }, { threshold: 0.4 });

    sections.forEach(function (s) { spyObserver.observe(s.el); });
  }

  /* ---------- Read more toggles (Certifications / Featured Projects) ---------- */
  document.querySelectorAll('[data-readmore-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var grid = btn.previousElementSibling;
      if (!grid) return;
      var hidden = grid.querySelectorAll('.readmore-hidden');
      var isExpanded = btn.dataset.expanded === 'true';
      hidden.forEach(function (item) {
        item.classList.toggle('readmore-hidden', isExpanded);
      });
      btn.dataset.expanded = (!isExpanded).toString();
      btn.textContent = isExpanded ? 'Read more →' : 'Show less';
    });
  });
})();
