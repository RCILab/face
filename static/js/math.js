(() => {
  'use strict';
  if (!window.katex) return;
  document.querySelectorAll('.math').forEach(el => {
    window.katex.render(el.textContent, el, {
      throwOnError: false, displayMode: el.classList.contains('math-display') });
  });
})();
