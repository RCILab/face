/* Small, silent explanatory loops. GIF copies are available for download. */
(() => {
  'use strict';
  const region = document.querySelector('#method-loops');
  const toggle = document.querySelector('#method-loops-toggle');
  const videos = [...region.querySelectorAll('video')];
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reduce.matches;
  let visible = false;
  function sync() {
    toggle.textContent = paused ? 'Play animations' : 'Pause animations';
    videos.forEach(video => {
      if (!paused && visible && !document.hidden) {
        video.play().catch(() => {
          paused = true;
          videos.forEach(item => item.pause());
          toggle.textContent = 'Play animations';
        });
      } else video.pause();
    });
  }
  toggle.hidden = false;
  toggle.addEventListener('click', () => { paused = !paused; sync(); });
  reduce.addEventListener('change', event => { if (event.matches) { paused = true; sync(); } });
  document.addEventListener('visibilitychange', sync);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; sync(); }, { threshold: 0.1 }).observe(region);
  } else visible = true;
  sync();
})();
