/* Use native GIF playback so these user-requested loops work without video
   autoplay permissions or JavaScript. Controls provide a still-image pause. */
(() => {
  'use strict';
  const region = document.querySelector('#method-loops');
  const toggle = document.querySelector('#method-loops-toggle');
  if (!region || !toggle) return;
  const images = [...region.querySelectorAll('img[data-still]')];
  const animatedSources = images.map(image => image.getAttribute('src'));
  let paused = false;
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    paused = !paused;
    images.forEach((image, index) => {
      image.src = paused ? image.dataset.still : animatedSources[index];
    });
    toggle.textContent = paused ? 'Play animations' : 'Pause animations';
  });
})();
