/* Progressive enhancement: the complete paper, media and comparisons work
   without JavaScript. Clips keep native controls and original timing. */
(() => {
  'use strict';
  const states = new Map([...document.querySelectorAll('video.research-clip')].map(video =>
    [video, { video, visible: false, userPaused: false, internalPause: false }]));

  function pause(state) {
    state.video.autoplay = false;
    if (!state.video.paused) {
      state.internalPause = true;
      state.video.pause();
    }
  }
  function playIfVisible(state) {
    if (!state.visible || state.userPaused || document.hidden || state.video.closest('[hidden]')) return;
    state.video.muted = true;
    state.video.defaultMuted = true;
    state.video.autoplay = true;
    state.video.play().catch(() => { /* Retry on readiness, page activation or user interaction. */ });
  }
  function refresh(state) {
    const rect = state.video.getBoundingClientRect();
    state.visible = !state.video.closest('[hidden]') && rect.width > 0 && rect.height > 0 &&
      rect.bottom > 0 && rect.top < innerHeight && rect.right > 0 && rect.left < innerWidth;
    if (state.visible && !document.hidden) playIfVisible(state);
    else pause(state);
  }
  function refreshAll() { states.forEach(refresh); }
  states.forEach(state => {
    state.video.muted = true;
    state.video.defaultMuted = true;
    state.video.addEventListener('canplay', () => refresh(state));
    state.video.addEventListener('pause', () => {
      if (state.internalPause) state.internalPause = false;
      else if (!state.video.ended) state.userPaused = true;
    });
    state.video.addEventListener('play', () => { state.userPaused = false; });
  });

  document.querySelectorAll('[data-tabs]').forEach(group => {
    const list = group.querySelector('[role="tablist"]');
    const tabs = [...list.querySelectorAll('[role="tab"]')];
    const panels = [...group.querySelectorAll('[data-tab-panel]')];
    function select(index, focus = false) {
      tabs.forEach((tab, i) => {
        tab.setAttribute('aria-selected', String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
        if (i !== index) panels[i].querySelectorAll('video').forEach(video => {
          const state = states.get(video);
          state.visible = false;
          pause(state);
        });
        panels[i].hidden = i !== index;
      });
      if (focus) tabs[index].focus();
      refreshAll();
    }
    panels.forEach((panel, i) => {
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tabs[i].id);
      panel.tabIndex = 0;
    });
    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => select(i));
      tab.addEventListener('keydown', event => {
        let index;
        if (event.key === 'ArrowRight') index = (i + 1) % tabs.length;
        if (event.key === 'ArrowLeft') index = (i - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') index = 0;
        if (event.key === 'End') index = tabs.length - 1;
        if (index !== undefined) { event.preventDefault(); select(index, true); }
      });
    });
    group.classList.add('enhanced');
    list.hidden = false;
    select(Number(group.dataset.initialTab || 0));
  });

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        const state = states.get(entry.target);
        refresh(state);
      });
    }, { threshold: [0, .01] });
    states.forEach(state => observer.observe(state.video));
  }
  document.addEventListener('visibilitychange', refreshAll);
  window.addEventListener('pageshow', refreshAll);
  window.addEventListener('load', refreshAll);
  window.addEventListener('resize', refreshAll);
  // Browser autoplay restrictions may lift after an actual user interaction.
  document.addEventListener('pointerup', refreshAll, { passive: true });
  document.addEventListener('keydown', refreshAll);
  if (!('IntersectionObserver' in window)) {
    window.addEventListener('scroll', refreshAll, { passive: true });
  }
  refreshAll();

})();
