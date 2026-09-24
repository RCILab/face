/* Start visible research clips, leave native controls available, and avoid
   decoding an entire gallery at once. A user's pause survives scrolling. */
(() => {
  'use strict';
  const states = [...document.querySelectorAll('video.research-clip')].map(video => ({ video, visible: false, manuallyPaused: false }));
  const byVideo = new Map(states.map(state => [state.video, state]));
  function start(state) {
    if (!state.visible || state.manuallyPaused || document.hidden) return;
    state.video.muted = true;
    // An interrupted play request must not permanently disable autoplay.
    state.video.play().catch(() => { /* Native play controls remain usable. */ });
  }
  for (const state of states) {
    state.video.addEventListener('pause', () => {
      if (state.visible && !document.hidden && !state.video.ended) state.manuallyPaused = true;
    });
    state.video.addEventListener('play', () => { state.manuallyPaused = false; });
  }
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        const state = byVideo.get(entry.target);
        state.visible = entry.isIntersecting;
        if (state.visible) start(state);
        else state.video.pause();
      }
    }, { threshold: 0.15 });
    states.forEach(state => observer.observe(state.video));
  } else {
    states.forEach(state => { state.visible = true; start(state); });
  }
  document.addEventListener('visibilitychange', () => {
    states.forEach(state => {
      if (document.hidden) state.video.pause();
      else start(state);
    });
  });
})();
