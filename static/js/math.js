/* Typeset the TeX source of .math elements with the bundled KaTeX.
   Without JavaScript the TeX source stays readable in place. */
(() => {
  'use strict';
  if (!window.katex) return;
  document.querySelectorAll('.math').forEach(el => {
    window.katex.render(el.textContent, el, {
      throwOnError: false, displayMode: el.classList.contains('math-display') });
  });
})();
