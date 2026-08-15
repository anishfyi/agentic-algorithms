/** Motion.dev helpers for Algorithm Atlas (vanilla JS, no build step). */

import { animate, stagger } from "https://cdn.jsdelivr.net/npm/motion@11.15.0/+esm";

const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

export function motionEnabled() {
  return !reduced;
}

export function markMotionReady() {
  if (motionEnabled()) {
    document.documentElement.classList.add("motion-ui");
  }
}

export function animateHero(parts) {
  if (!motionEnabled()) return;
  const targets = [parts.eyebrow, parts.title, parts.sub, parts.search].filter(Boolean);
  animate(
    targets,
    { opacity: [0, 1], y: [20, 0] },
    { delay: stagger(0.09), duration: 0.55, ease: [0.22, 1, 0.36, 1] },
  );
}

export function animateControls(controls) {
  if (!motionEnabled() || !controls) return;
  animate(controls, { opacity: [0, 1], y: [12, 0] }, { duration: 0.45, delay: 0.25, ease: [0.22, 1, 0.36, 1] });
}

export function animateCards(cards) {
  if (!motionEnabled() || !cards.length) return;
  animate(
    cards,
    { opacity: [0, 1], y: [16, 0], scale: [0.98, 1] },
    {
      delay: stagger(0.022, { start: 0.04 }),
      duration: 0.38,
      ease: [0.22, 1, 0.36, 1],
    },
  );
}

export function bindCardHover(card) {
  if (!motionEnabled()) return;
  card.addEventListener("mouseenter", () => {
    animate(card, { y: -4 }, { type: "spring", stiffness: 520, damping: 30 });
  });
  card.addEventListener("mouseleave", () => {
    animate(card, { y: 0 }, { type: "spring", stiffness: 520, damping: 30 });
  });
}

let panelCloseAnim = null;

export function animatePanelOpen(backdrop, panel) {
  if (!motionEnabled()) return;
  panelCloseAnim?.stop?.();
  animate(backdrop, { opacity: [0, 1] }, { duration: 0.2, ease: "easeOut" });
  animate(panel, { x: ["100%", "0%"], opacity: [0.6, 1] }, { type: "spring", stiffness: 360, damping: 34 });
}

export function animatePanelClose(backdrop, panel) {
  if (!motionEnabled()) return Promise.resolve();
  const fade = animate(backdrop, { opacity: [1, 0] }, { duration: 0.18, ease: "easeIn" });
  panelCloseAnim = animate(panel, { x: ["0%", "100%"], opacity: [1, 0] }, { duration: 0.28, ease: [0.4, 0, 1, 1] });
  return Promise.all([fade.finished, panelCloseAnim.finished]).then(() => undefined);
}

export function pulseResultCount(el) {
  if (!motionEnabled() || !el) return;
  animate(el, { opacity: [0.5, 1], scale: [0.98, 1] }, { duration: 0.28, ease: "easeOut" });
}
