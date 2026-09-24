/* Conceptual decoder animation: paper Eqs. (6) and (7), with c=0 and g=1.
   These illustrative values are not measured experimental data. */
(() => {
  'use strict';
  const demo = document.querySelector('#method-demo');
  const toggle = document.querySelector('#demo-toggle');
  const controls = demo.querySelector('.demo-controls');
  const buttons = [...controls.querySelectorAll('button')];
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const scenes = [
    { mu: 0.35, angle: 0, title: '01 / LOWER FRICTION', text: 'Lower friction requires less tangential force for the same normalized interaction.' },
    { mu: 0.85, angle: 0, title: '02 / HIGHER FRICTION', text: 'As friction increases, the decoder increases tangential force. Normal loading stays the same.' },
    { mu: 0.85, angle: -24, title: '03 / TILTED SURFACE', text: 'With friction unchanged, the estimated normal rotates the force reference and projects motion onto the tilted surface.' }
  ];
  const elements = Object.fromEntries(['surface', 'normal', 'motion', 'force-vector', 'friction', 'force', 'step', 'explanation'].map(name => [name, document.querySelector(`#demo-${name}`)]));
  let selected = 0;
  let current = { mu: scenes[0].mu, angle: scenes[0].angle };
  let from = { ...current };
  let transition = 1;
  let elapsed = 0;
  let last = null;
  let frame = null;
  let visible = false;
  let paused = reduce.matches;

  function render() {
    const angle = current.angle * Math.PI / 180;
    const tx = Math.cos(angle), ty = Math.sin(angle);
    const nx = -ty, ny = tx; // Compressive normal points into the surface.
    const normalForce = 10 * 0.4;
    const tangentForce = current.mu * normalForce * Math.exp(0);
    const path = (x, y) => `M230 112L${(230 + x).toFixed(2)} ${(112 + y).toFixed(2)}`;
    elements.surface.setAttribute('transform', `translate(230 112) rotate(${current.angle.toFixed(2)})`);
    elements.normal.setAttribute('d', path(90 * nx, 90 * ny));
    // Project the fixed predicted translation (145, 0) onto the tangent.
    elements.motion.setAttribute('d', path(145 * tx * tx, 145 * tx * ty));
    elements['force-vector'].setAttribute('d', path(18 * (normalForce * nx + tangentForce * tx), 18 * (normalForce * ny + tangentForce * ty)));
    elements.friction.textContent = current.mu.toFixed(2);
    elements.force.innerHTML = `${tangentForce.toFixed(1)} <small>N</small>`;
  }
  function select(index, animate) {
    selected = index;
    from = { ...current };
    transition = animate ? 0 : 1;
    elapsed = 0;
    buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
    elements.step.textContent = scenes[index].title;
    elements.explanation.textContent = scenes[index].text;
    if (!animate) { current = { mu: scenes[index].mu, angle: scenes[index].angle }; render(); }
  }
  function tick(time) {
    frame = null;
    const delta = last === null ? 0 : Math.min(time - last, 100);
    last = time;
    elapsed += delta;
    if (elapsed >= 5500) select((selected + 1) % scenes.length, true);
    if (transition < 1) {
      transition = Math.min(1, transition + delta / 1200);
      const blend = transition * transition * (3 - 2 * transition);
      current.mu = from.mu + (scenes[selected].mu - from.mu) * blend;
      current.angle = from.angle + (scenes[selected].angle - from.angle) * blend;
      render();
    }
    frame = window.requestAnimationFrame(tick);
  }
  function syncPlayback() {
    toggle.textContent = paused ? 'Play animation' : 'Pause animation';
    if (frame !== null) window.cancelAnimationFrame(frame);
    frame = null;
    last = null;
    if (visible && !document.hidden && !paused) frame = window.requestAnimationFrame(tick);
  }
  buttons.forEach((button, index) => button.addEventListener('click', () => {
    // Manual selection stays on that condition until the user resumes the loop.
    paused = true;
    select(index, false);
    syncPlayback();
  }));
  toggle.addEventListener('click', () => { paused = !paused; syncPlayback(); });
  reduce.addEventListener('change', event => {
    if (event.matches) { paused = true; syncPlayback(); }
  });
  document.addEventListener('visibilitychange', syncPlayback);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; syncPlayback(); }, { threshold: 0.15 }).observe(demo);
  } else { visible = true; }
  controls.hidden = false;
  toggle.hidden = false;
  render();
  syncPlayback();
})();
