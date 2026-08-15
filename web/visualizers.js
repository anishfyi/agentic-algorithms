/* Category-based canvas visualizers for Algorithm Atlas (black and white). */

"use strict";

const activeAnimations = new Map();

function stopViz(id) {
  const anim = activeAnimations.get(id);
  if (anim) {
    cancelAnimationFrame(anim.frame);
    if (anim.timer) clearInterval(anim.timer);
    activeAnimations.delete(id);
  }
}

function startLoop(id, draw, fps = 30) {
  stopViz(id);
  let frame = 0;
  const tick = () => {
    draw(frame++);
    const handle = requestAnimationFrame(tick);
    activeAnimations.set(id, { frame: handle });
  };
  tick();
}

function setupCanvas(canvas) {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const w = Math.max(1, rect.width);
  const h = Math.max(1, rect.height);
  const needsResize =
    canvas._vizW !== w || canvas._vizH !== h || canvas._vizDpr !== dpr;
  if (needsResize) {
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    canvas._vizW = w;
    canvas._vizH = h;
    canvas._vizDpr = dpr;
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    canvas._vizCtx = ctx;
  }
  return { ctx: canvas._vizCtx || canvas.getContext("2d"), w: canvas._vizW, h: canvas._vizH };
}

function clear(ctx, w, h) {
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, w, h);
}

function strokeBox(ctx, x, y, w, h, fill = "rgba(255,255,255,0.06)") {
  ctx.fillStyle = fill;
  ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = "rgba(255,255,255,0.35)";
  ctx.lineWidth = 1;
  ctx.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1);
}

/* ---------- Visualizers ---------- */

function drawBars(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const n = 12;
  const gap = 6;
  const barW = (w - gap * (n + 1)) / n;
  const values = Array.from({ length: n }, (_, i) => 0.25 + ((i * 7 + frame) % 11) / 11);
  const active = frame % n;
  for (let i = 0; i < n; i++) {
    const barH = values[i] * (h - 40);
    const x = gap + i * (barW + gap);
    const y = h - 20 - barH;
    const bright = i === active || i === (active + 3) % n;
    strokeBox(ctx, x, y, barW, barH, bright ? "rgba(255,255,255,0.22)" : "rgba(255,255,255,0.08)");
  }
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.font = "10px JetBrains Mono, monospace";
  ctx.fillText("compare / swap", 12, 16);
}

function drawArray(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const vals = [3, 7, 1, 9, 4, 6, 2, 8, 5];
  const n = vals.length;
  const gap = 8;
  const cellW = (w - gap * (n + 1)) / n;
  const left = frame % n;
  const right = (frame + 4) % n;
  for (let i = 0; i < n; i++) {
    const x = gap + i * (cellW + gap);
    const barH = (vals[i] / 9) * (h - 50);
    const y = h - 24 - barH;
    const hi = i === left || i === right;
    strokeBox(ctx, x, y, cellW, barH, hi ? "rgba(255,255,255,0.25)" : "rgba(255,255,255,0.08)");
    ctx.fillStyle = "#fff";
    ctx.font = "11px JetBrains Mono, monospace";
    ctx.textAlign = "center";
    ctx.fillText(String(vals[i]), x + cellW / 2, y - 6);
  }
  ctx.textAlign = "left";
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.fillText("two pointers", 12, 16);
}

function drawGraph(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const nodes = [
    [w * 0.2, h * 0.5],
    [w * 0.45, h * 0.25],
    [w * 0.45, h * 0.75],
    [w * 0.72, h * 0.4],
    [w * 0.72, h * 0.65],
  ];
  const edges = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 4]];
  const visit = frame % nodes.length;
  ctx.strokeStyle = "rgba(255,255,255,0.25)";
  ctx.lineWidth = 1;
  for (const [a, b] of edges) {
    ctx.beginPath();
    ctx.moveTo(nodes[a][0], nodes[a][1]);
    ctx.lineTo(nodes[b][0], nodes[b][1]);
    ctx.stroke();
  }
  nodes.forEach(([x, y], i) => {
    const active = i <= visit;
    ctx.beginPath();
    ctx.arc(x, y, 14, 0, Math.PI * 2);
    ctx.fillStyle = active ? "#fff" : "rgba(255,255,255,0.12)";
    ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,0.5)";
    ctx.stroke();
    ctx.fillStyle = active ? "#000" : "#fff";
    ctx.font = "10px JetBrains Mono, monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(String.fromCharCode(65 + i), x, y);
  });
  ctx.textAlign = "left";
  ctx.textBaseline = "alphabetic";
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.fillText("BFS traversal", 12, 16);
}

function drawTree(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const levels = [[w / 2], [w * 0.35, w * 0.65], [w * 0.22, w * 0.5, w * 0.78]];
  const edges = [
    [0, 0, 1, 0], [0, 0, 1, 1],
    [1, 0, 2, 0], [1, 0, 2, 1], [1, 1, 2, 2],
  ];
  const y = [h * 0.22, h * 0.52, h * 0.82];
  const highlight = frame % 6;
  let idx = 0;
  ctx.strokeStyle = "rgba(255,255,255,0.25)";
  for (const [pl, pi, cl, ci] of edges) {
    ctx.beginPath();
    ctx.moveTo(levels[pl][pi], y[pl] + 12);
    ctx.lineTo(levels[cl][ci], y[cl] - 12);
    ctx.stroke();
  }
  levels.forEach((row, li) => {
    row.forEach((x) => {
      const on = idx++ === highlight;
      ctx.beginPath();
      ctx.arc(x, y[li], 12, 0, Math.PI * 2);
      ctx.fillStyle = on ? "#fff" : "rgba(255,255,255,0.1)";
      ctx.fill();
      ctx.strokeStyle = "rgba(255,255,255,0.4)";
      ctx.stroke();
    });
  });
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.font = "10px JetBrains Mono, monospace";
  ctx.fillText("tree walk", 12, 16);
}

function drawString(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const text = "algorithm";
  const n = text.length;
  const cell = 28;
  const startX = (w - n * cell) / 2;
  const winStart = frame % (n - 2);
  const winEnd = winStart + 3;
  for (let i = 0; i < n; i++) {
    const x = startX + i * cell;
    const y = h / 2 - 14;
    const inWin = i >= winStart && i <= winEnd;
    strokeBox(ctx, x, y, cell - 4, 28, inWin ? "rgba(255,255,255,0.2)" : "rgba(255,255,255,0.06)");
    ctx.fillStyle = "#fff";
    ctx.font = "13px JetBrains Mono, monospace";
    ctx.textAlign = "center";
    ctx.fillText(text[i], x + (cell - 4) / 2, y + 19);
  }
  ctx.textAlign = "left";
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.fillText("sliding window", 12, 16);
}

function drawGrid(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const rows = 5;
  const cols = 6;
  const pad = 14;
  const cellW = (w - pad * 2) / cols;
  const cellH = (h - pad * 2 - 16) / rows;
  const pathLen = rows + cols - 1;
  const step = frame % (pathLen + 4);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x = pad + c * cellW;
      const y = pad + 16 + r * cellH;
      const dist = r + c;
      const filled = dist < step;
      strokeBox(ctx, x + 2, y + 2, cellW - 4, cellH - 4, filled ? "rgba(255,255,255,0.18)" : "rgba(255,255,255,0.04)");
    }
  }
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.font = "10px JetBrains Mono, monospace";
  ctx.fillText("DP table fill", 12, 16);
}

function drawStack(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const items = ["push", "pop", "peek", "top", "base"];
  const shown = Math.min(items.length, 2 + (frame % 4));
  const boxW = 120;
  const boxH = 28;
  const x = w / 2 - boxW / 2;
  for (let i = 0; i < shown; i++) {
    const y = h - 30 - i * (boxH + 6);
    const top = i === shown - 1;
    strokeBox(ctx, x, y - boxH, boxW, boxH, top ? "rgba(255,255,255,0.2)" : "rgba(255,255,255,0.08)");
    ctx.fillStyle = "#fff";
    ctx.font = "11px JetBrains Mono, monospace";
    ctx.textAlign = "center";
    ctx.fillText(items[i], x + boxW / 2, y - boxH / 2 + 4);
  }
  ctx.textAlign = "left";
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.fillText("LIFO stack", 12, 16);
}

function drawIntervals(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const intervals = [
    [0.08, 0.35],
    [0.22, 0.55],
    [0.48, 0.78],
    [0.62, 0.9],
  ];
  const active = frame % intervals.length;
  intervals.forEach(([a, b], i) => {
    const y = 40 + i * 28;
    const x1 = a * (w - 40) + 20;
    const x2 = b * (w - 40) + 20;
    ctx.strokeStyle = i === active ? "#fff" : "rgba(255,255,255,0.35)";
    ctx.lineWidth = i === active ? 3 : 1;
    ctx.beginPath();
    ctx.moveTo(x1, y);
    ctx.lineTo(x2, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(x1, y, 4, 0, Math.PI * 2);
    ctx.arc(x2, y, 4, 0, Math.PI * 2);
    ctx.fillStyle = "#fff";
    ctx.fill();
  });
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.font = "10px JetBrains Mono, monospace";
  ctx.fillText("interval merge", 12, 16);
}

function drawLinked(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const n = 5;
  const nodeW = 44;
  const gap = 36;
  const startX = (w - (n * nodeW + (n - 1) * gap)) / 2;
  const y = h / 2;
  const head = frame % n;
  for (let i = 0; i < n; i++) {
    const x = startX + i * (nodeW + gap);
    strokeBox(ctx, x, y - 16, nodeW, 32, i === head ? "rgba(255,255,255,0.22)" : "rgba(255,255,255,0.08)");
    ctx.fillStyle = "#fff";
    ctx.font = "11px JetBrains Mono, monospace";
    ctx.textAlign = "center";
    ctx.fillText(String(i + 1), x + nodeW / 2, y + 4);
    if (i < n - 1) {
      ctx.strokeStyle = "rgba(255,255,255,0.4)";
      ctx.beginPath();
      ctx.moveTo(x + nodeW, y);
      ctx.lineTo(x + nodeW + gap - 8, y);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x + nodeW + gap - 8, y);
      ctx.lineTo(x + nodeW + gap - 14, y - 4);
      ctx.lineTo(x + nodeW + gap - 14, y + 4);
      ctx.closePath();
      ctx.fillStyle = "rgba(255,255,255,0.4)";
      ctx.fill();
    }
  }
  ctx.textAlign = "left";
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.fillText("linked list", 12, 16);
}

function drawBits(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const bits = "10110100".split("");
  const n = bits.length;
  const cell = 30;
  const startX = (w - n * cell) / 2;
  const flip = frame % n;
  for (let i = 0; i < n; i++) {
    const x = startX + i * cell;
    const y = h / 2 - 14;
    strokeBox(ctx, x, y, cell - 4, 28, i === flip ? "rgba(255,255,255,0.22)" : "rgba(255,255,255,0.06)");
    ctx.fillStyle = "#fff";
    ctx.font = "12px JetBrains Mono, monospace";
    ctx.textAlign = "center";
    ctx.fillText(bits[i], x + (cell - 4) / 2, y + 19);
  }
  ctx.textAlign = "left";
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.fillText("bit operations", 12, 16);
}

function drawCurve(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const pad = 24;
  ctx.strokeStyle = "rgba(255,255,255,0.2)";
  ctx.beginPath();
  ctx.moveTo(pad, h - pad);
  ctx.lineTo(w - pad, h - pad);
  ctx.moveTo(pad, h - pad);
  ctx.lineTo(pad, pad);
  ctx.stroke();
  const curves = [
    (x) => x * 0.3,
    (x) => x * Math.log2(x + 1) * 0.12,
    (x) => x * x * 0.004,
  ];
  const colors = ["rgba(255,255,255,0.9)", "rgba(255,255,255,0.55)", "rgba(255,255,255,0.3)"];
  curves.forEach((fn, ci) => {
    ctx.strokeStyle = colors[ci];
    ctx.lineWidth = ci === frame % 3 ? 2 : 1;
    ctx.beginPath();
    for (let px = 0; px <= w - pad * 2; px++) {
      const x = px / (w - pad * 2) * 20 + 1;
      const y = h - pad - fn(x) * (h - pad * 2) / 8;
      if (px === 0) ctx.moveTo(pad + px, y);
      else ctx.lineTo(pad + px, y);
    }
    ctx.stroke();
  });
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.font = "10px JetBrains Mono, monospace";
  ctx.fillText("complexity", 12, 16);
}

function drawPipeline(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const stages = ["input", "validate", "transform", "output"];
  const stageW = (w - 60) / stages.length;
  const active = frame % stages.length;
  stages.forEach((label, i) => {
    const x = 20 + i * (stageW + 10);
    const y = h / 2 - 20;
    strokeBox(ctx, x, y, stageW, 40, i === active ? "rgba(255,255,255,0.2)" : "rgba(255,255,255,0.06)");
    ctx.fillStyle = "#fff";
    ctx.font = "10px JetBrains Mono, monospace";
    ctx.textAlign = "center";
    ctx.fillText(label, x + stageW / 2, y + 24);
    if (i < stages.length - 1) {
      ctx.strokeStyle = "rgba(255,255,255,0.35)";
      ctx.beginPath();
      ctx.moveTo(x + stageW, y + 20);
      ctx.lineTo(x + stageW + 10, y + 20);
      ctx.stroke();
    }
  });
  ctx.textAlign = "left";
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.fillText("pipeline", 12, 16);
}

function drawBlocks(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const blocks = ["system", "context", "user", "assistant"];
  const bh = 32;
  const gap = 10;
  const startY = (h - blocks.length * (bh + gap)) / 2;
  const active = frame % blocks.length;
  blocks.forEach((label, i) => {
    const y = startY + i * (bh + gap);
    const bw = w * (0.45 + (i % 3) * 0.12);
    const x = (w - bw) / 2;
    strokeBox(ctx, x, y, bw, bh, i === active ? "rgba(255,255,255,0.2)" : "rgba(255,255,255,0.06)");
    ctx.fillStyle = "#fff";
    ctx.font = "11px JetBrains Mono, monospace";
    ctx.textAlign = "center";
    ctx.fillText(label, x + bw / 2, y + 20);
  });
  ctx.textAlign = "left";
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.fillText("message flow", 12, 16);
}

function drawSignal(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const bars = 8;
  const gap = 10;
  const barW = (w - gap * (bars + 1)) / bars;
  for (let i = 0; i < bars; i++) {
    const phase = (frame + i * 3) % 20;
    const amp = 0.2 + 0.7 * Math.abs(Math.sin(phase / 20 * Math.PI * 2));
    const barH = amp * (h - 50);
    const x = gap + i * (barW + gap);
    strokeBox(ctx, x, h - 24 - barH, barW, barH, "rgba(255,255,255,0.12)");
  }
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.font = "10px JetBrains Mono, monospace";
  ctx.fillText("signal score", 12, 16);
}

function drawIndex(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const docs = ["doc_a", "doc_b", "doc_c", "doc_d"];
  const rowH = 30;
  const startY = 36;
  docs.forEach((doc, i) => {
    const y = startY + i * (rowH + 8);
    const score = ((frame + i * 5) % 10) / 10;
    strokeBox(ctx, 20, y, w - 40, rowH, "rgba(255,255,255,0.05)");
    ctx.fillStyle = "#fff";
    ctx.font = "10px JetBrains Mono, monospace";
    ctx.fillText(doc, 28, y + 19);
    const barW = (w - 120) * score;
    strokeBox(ctx, w - 28 - barW, y + 8, barW, rowH - 16, "rgba(255,255,255,0.2)");
  });
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.fillText("retrieval rank", 12, 16);
}

function drawMap(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const cols = 8;
  const rows = 5;
  const pad = 16;
  const cellW = (w - pad * 2) / cols;
  const cellH = (h - pad * 2 - 12) / rows;
  const px = pad + (frame % cols) * cellW;
  const py = pad + 12 + ((frame * 2) % rows) * cellH;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      strokeBox(
        ctx,
        pad + c * cellW + 1,
        pad + 12 + r * cellH + 1,
        cellW - 2,
        cellH - 2,
        "rgba(255,255,255,0.03)"
      );
    }
  }
  strokeBox(ctx, px + 2, py + 2, cellW - 4, cellH - 4, "rgba(255,255,255,0.25)");
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.font = "10px JetBrains Mono, monospace";
  ctx.fillText("geo grid", 12, 16);
}

function drawSets(canvas, id, frame) {
  const { ctx, w, h } = setupCanvas(canvas);
  clear(ctx, w, h);
  const sets = [
    { x: w * 0.25, y: h * 0.4, nodes: [0, 1, 2] },
    { x: w * 0.75, y: h * 0.55, nodes: [3, 4] },
  ];
  const merging = frame % 60 < 30;
  ctx.strokeStyle = "rgba(255,255,255,0.25)";
  sets.forEach((set, si) => {
    set.nodes.forEach((n, ni) => {
      const angle = (ni / set.nodes.length) * Math.PI * 2;
      const x = set.x + Math.cos(angle) * 28;
      const y = set.y + Math.sin(angle) * 28;
      ctx.beginPath();
      ctx.arc(x, y, 10, 0, Math.PI * 2);
      ctx.fillStyle = merging ? "rgba(255,255,255,0.15)" : "rgba(255,255,255,0.08)";
      ctx.fill();
      ctx.stroke();
    });
  });
  if (merging) {
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(sets[0].x, sets[0].y);
    ctx.lineTo(sets[1].x, sets[1].y);
    ctx.stroke();
    ctx.setLineDash([]);
  }
  ctx.fillStyle = "rgba(255,255,255,0.5)";
  ctx.font = "10px JetBrains Mono, monospace";
  ctx.fillText("union find", 12, 16);
}

function drawTrie(canvas, id, frame) {
  drawTree(canvas, id, frame);
}

function drawHeap(canvas, id, frame) {
  drawTree(canvas, id, frame);
}

function drawFlow(canvas, id, frame) {
  drawPipeline(canvas, id, frame);
}

const RENDERERS = {
  bars: drawBars,
  array: drawArray,
  graph: drawGraph,
  tree: drawTree,
  string: drawString,
  grid: drawGrid,
  stack: drawStack,
  intervals: drawIntervals,
  linked: drawLinked,
  bits: drawBits,
  curve: drawCurve,
  pipeline: drawPipeline,
  blocks: drawBlocks,
  signal: drawSignal,
  index: drawIndex,
  map: drawMap,
  sets: drawSets,
  trie: drawTrie,
  heap: drawHeap,
  flow: drawFlow,
};

export function renderVisualizer(canvas, algo) {
  if (!canvas || !algo) return;
  const fn = RENDERERS[algo.viz] || drawCurve;
  const id = algo.id;
  stopViz(id);
  // Prime canvas size once before animation loop to avoid per-frame clears.
  setupCanvas(canvas);
  let frame = 0;
  const tick = () => {
    fn(canvas, id, frame++);
    const handle = requestAnimationFrame(tick);
    activeAnimations.set(id, { frame: handle });
  };
  tick();
}

export function resizeVisualizer(canvas, algo) {
  if (!canvas || !algo) return;
  canvas._vizW = undefined;
  setupCanvas(canvas);
}

export function destroyVisualizer(algoId) {
  stopViz(algoId);
}
