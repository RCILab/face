'use strict';

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const hero = document.querySelector('#hero-video');
const motionToggle = document.querySelector('#motion-toggle');
let manuallyPaused = reducedMotion.matches;
let heroVisible = false;
function syncMotionLabel() {
  motionToggle.textContent = hero.paused ? 'Play preview' : 'Pause preview';
  motionToggle.setAttribute('aria-label', motionToggle.textContent);
}
function updateMotion() {
  if (heroVisible && !document.hidden && !manuallyPaused) hero.play().catch(syncMotionLabel);
  else hero.pause();
}
motionToggle.hidden = false;
motionToggle.addEventListener('click', () => { manuallyPaused = !hero.paused; updateMotion(); });
hero.addEventListener('play', syncMotionLabel);
hero.addEventListener('pause', syncMotionLabel);
hero.addEventListener('error', () => { motionToggle.hidden = true; });
reducedMotion.addEventListener('change', event => { manuallyPaused = event.matches; updateMotion(); });
document.addEventListener('visibilitychange', updateMotion);
if ('IntersectionObserver' in window) {
  new IntersectionObserver(entries => { heroVisible = entries[0].isIntersecting; updateMotion(); }, { threshold: 0.15 }).observe(hero);
} else { heroVisible = true; updateMotion(); }
syncMotionLabel();

const video = document.querySelector('#main-video');
document.querySelectorAll('[data-video-time]').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    const seekAndPlay = () => {
      video.currentTime = Number(link.dataset.videoTime);
      video.play().catch(() => { /* Native controls remain available. */ });
    };
    if (video.readyState >= 1) seekAndPlay();
    else video.addEventListener('loadedmetadata', seekAndPlay, { once: true });
    document.querySelector('#video').scrollIntoView({ behavior: reducedMotion.matches ? 'instant' : 'smooth' });
    video.focus({ preventScroll: true });
  });
});

const copy = document.querySelector('#copy-citation');
copy.hidden = false;
copy.addEventListener('click', async () => {
  const status = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText(document.querySelector('#bibtex').textContent);
    copy.textContent = 'Copied!';
    status.textContent = 'Citation copied to clipboard.';
    window.setTimeout(() => { copy.textContent = 'Copy citation'; }, 2000);
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(document.querySelector('#bibtex'));
    selection.removeAllRanges(); selection.addRange(range);
    copy.textContent = 'Text selected';
    status.textContent = 'Citation selected. Press Control+C or Command+C to copy.';
  }
});
