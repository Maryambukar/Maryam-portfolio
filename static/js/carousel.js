(function () {
  'use strict';

  document.querySelectorAll('[data-carousel]').forEach(function (carousel) {
    var pages = carousel.querySelectorAll('.carousel-page');
    var prevBtn = carousel.querySelector('[data-carousel-prev]');
    var nextBtn = carousel.querySelector('[data-carousel-next]');
    var current = 0;

    if (pages.length <= 1) {
      // Nothing to page through — no next/prev controls at all.
      if (prevBtn) prevBtn.hidden = true;
      if (nextBtn) nextBtn.hidden = true;
      if (pages.length === 1) pages[0].classList.add('active');
      return;
    }

    function render() {
      pages.forEach(function (page, i) {
        page.classList.toggle('active', i === current);
      });
      prevBtn.hidden = current === 0;
      nextBtn.hidden = current === pages.length - 1;
    }

    prevBtn.addEventListener('click', function () {
      if (current > 0) { current -= 1; render(); }
    });
    nextBtn.addEventListener('click', function () {
      if (current < pages.length - 1) { current += 1; render(); }
    });

    render();
  });
})();
