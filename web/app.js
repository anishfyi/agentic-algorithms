/* Algorithm Atlas: search, filters, detail panel, visualizers, hash deep links. */

"use strict";

import { destroyVisualizer, renderVisualizer, resizeVisualizer } from "./visualizers.js";

const TRACK_LABELS = {
  dsa: "DSA",
  domain: "Domain",
  llm: "LLM Helpers",
  psychology: "Psychology",
  shopify_commerce: "Shopify Commerce",
};

const state = {
  algorithms: [],
  shopifyDocs: [],
  shopifyLoaded: false,
  shopifyLoading: false,
  query: "",
  track: "all",
  category: null,
  openAlgoId: null,
};

const els = {
  search: document.getElementById("search"),
  trackFilters: document.getElementById("track-filters"),
  categoryChips: document.getElementById("category-chips"),
  resultCount: document.getElementById("result-count"),
  grid: document.getElementById("grid"),
  emptyState: document.getElementById("empty-state"),
  heroCount: document.getElementById("hero-count"),
  backdrop: document.getElementById("panel-backdrop"),
  panel: document.getElementById("detail-panel"),
  panelClose: document.getElementById("panel-close"),
  panelTrack: document.getElementById("panel-track"),
  panelTitle: document.getElementById("panel-title"),
  panelCategory: document.getElementById("panel-category"),
  panelDescription: document.getElementById("panel-description"),
  panelViz: document.getElementById("panel-viz"),
  panelTime: document.getElementById("panel-time"),
  panelSpace: document.getElementById("panel-space"),
  panelSource: document.getElementById("panel-source"),
  panelImport: document.getElementById("panel-import"),
  panelCitationWrap: document.getElementById("panel-citation-wrap"),
  panelCiteUrl: document.getElementById("panel-cite-url"),
  panelCiteElement: document.getElementById("panel-cite-element"),
  panelCiteSelector: document.getElementById("panel-cite-selector"),
  panelPermalink: document.getElementById("panel-permalink"),
  copyImport: document.getElementById("copy-import"),
  copySource: document.getElementById("copy-source"),
};

function allItems() {
  return [...state.algorithms, ...state.shopifyDocs];
}

async function loadShopifyDocs() {
  if (state.shopifyLoaded || state.shopifyLoading) return;
  state.shopifyLoading = true;
  try {
    const res = await fetch("data/shopify_commerce.json");
    if (!res.ok) throw new Error(`shopify HTTP ${res.status}`);
    const data = await res.json();
    state.shopifyDocs = (data.docs || []).map((d) => ({ ...d, kind: "doc" }));
    state.shopifyLoaded = true;
    els.heroCount.textContent = allItems().length;
    render();
  } catch (err) {
    console.error("Shopify docs load failed", err);
  } finally {
    state.shopifyLoading = false;
  }
}

function formatCategory(slug) {
  return slug.replace(/_/g, " ");
}

function matches(item) {
  if (state.track !== "all" && item.track !== state.track) return false;
  if (state.category && item.category !== state.category) return false;
  if (!state.query) return true;
  const q = state.query;
  const haystack = [
    item.name,
    item.title,
    item.category,
    item.module,
    item.function,
    item.description,
    item.content,
    item.page_title,
    item.source_domain,
    item.citation?.element_id,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
  return haystack.includes(q);
}

function highlight(text) {
  if (!state.query) return escapeHtml(text);
  const q = state.query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return escapeHtml(text).replace(new RegExp(`(${q})`, "ig"), "<mark>$1</mark>");
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function truncate(text, max = 90) {
  if (!text) return "";
  return text.length <= max ? text : `${text.slice(0, max - 1)}…`;
}

/* ---------- Filters ---------- */

function renderTrackFilters() {
  const items = allItems();
  const tracks = ["all", ...new Set(items.map((a) => a.track))];
  els.trackFilters.innerHTML = "";
  for (const track of tracks) {
    const count = track === "all" ? items.length : items.filter((a) => a.track === track).length;
    const btn = document.createElement("button");
    btn.className = "track-btn" + (state.track === track ? " active" : "");
    btn.innerHTML = `${track === "all" ? "All" : TRACK_LABELS[track] || track}<span class="count">${count}</span>`;
    btn.addEventListener("click", async () => {
      state.track = track;
      state.category = null;
      if (track === "shopify_commerce") await loadShopifyDocs();
      render();
    });
    els.trackFilters.appendChild(btn);
  }
}

function renderCategoryChips() {
  const pool =
    state.track === "all" ? allItems() : allItems().filter((a) => a.track === state.track);
  const categories = [...new Set(pool.map((a) => a.category))].sort();
  els.categoryChips.innerHTML = "";
  for (const cat of categories) {
    const chip = document.createElement("button");
    chip.className = "chip" + (state.category === cat ? " active" : "");
    chip.textContent = formatCategory(cat);
    chip.addEventListener("click", () => {
      state.category = state.category === cat ? null : cat;
      render();
    });
    els.categoryChips.appendChild(chip);
  }
}

/* ---------- Grid ---------- */

function renderGrid() {
  const visible = allItems().filter(matches);
  els.resultCount.textContent = `${visible.length} of ${allItems().length} entries`;
  els.emptyState.hidden = visible.length > 0;
  els.grid.innerHTML = "";

  visible.forEach((item, i) => {
    const card = document.createElement("button");
    const isDoc = item.kind === "doc";
    card.className = "card" + (isDoc ? " card-kind-doc" : "");
    card.style.animationDelay = `${Math.min(i, 24) * 22}ms`;
    const badge = isDoc ? "Doc" : TRACK_LABELS[item.track] || item.track;
    const badgeClass = item.track === "shopify_commerce" && isDoc ? "badge-shopify" : "";
    card.innerHTML = `
      <div class="card-top">
        <span class="track-badge ${badgeClass}">${badge}</span>
        <span class="card-category">${formatCategory(item.category)}</span>
      </div>
      <h3 class="card-name">${highlight(item.title || item.name)}</h3>
      <p class="card-desc">${escapeHtml(truncate(item.description || ""))}</p>
      ${
        isDoc
          ? ""
          : `<div class="card-complexity">
        <div><span>time</span>${escapeHtml(item.time || "")}</div>
        <div><span>space</span>${escapeHtml(item.space || "")}</div>
      </div>`
      }`;
    card.addEventListener("click", () => openPanel(item, true));
    els.grid.appendChild(card);
  });
}

function render() {
  renderTrackFilters();
  renderCategoryChips();
  renderGrid();
}

/* ---------- Detail panel + deep links ---------- */

function importStatement(algo) {
  if (algo.track === "dsa") {
    return `from agentic_algorithms.dsa.${algo.module} import ${algo.function}`;
  }
  return `from agentic_algorithms.${algo.module} import ${algo.function}`;
}

function openPanel(item, pushHash) {
  if (state.openAlgoId && state.openAlgoId !== item.id) {
    destroyVisualizer(state.openAlgoId);
  }
  state.openAlgoId = item.id;
  const isDoc = item.kind === "doc";

  els.panelTrack.textContent = isDoc
    ? `Shopify docs · ${item.source_domain || "official"}`
    : `${TRACK_LABELS[item.track] || item.track} track`;
  els.panelTitle.textContent = item.title || item.name;
  els.panelCategory.textContent = isDoc
    ? `${formatCategory(item.block_type || item.category)} · ${item.page_title || ""}`
    : `Category: ${formatCategory(item.category)}`;
  els.panelDescription.textContent = item.description || item.content || "No description available.";

  const complexityWrap = els.panelTime.closest(".panel-complexity");
  if (complexityWrap) complexityWrap.style.display = isDoc ? "none" : "grid";

  els.panelTime.textContent = item.time || "";
  els.panelSpace.textContent = item.space || "";
  els.panelSource.textContent = isDoc ? item.content || "" : item.source || "# source not found";
  els.panelImport.textContent = isDoc ? "" : importStatement(item);
  els.panelImport.closest(".panel-usage").style.display = isDoc ? "none" : "block";

  const cite = item.citation;
  if (isDoc && cite?.citation_url) {
    els.panelCitationWrap.classList.remove("hidden");
    els.panelCiteUrl.href = cite.citation_url;
    els.panelCiteUrl.textContent = cite.citation_url;
    els.panelCiteElement.textContent = cite.element_id || cite.dom_tag || "";
    els.panelCiteSelector.textContent = cite.css_selector || cite.xpath || "";
  } else {
    els.panelCitationWrap.classList.add("hidden");
  }

  els.panelPermalink.href = `#/a/${item.id}`;
  els.backdrop.hidden = false;
  els.panel.hidden = false;
  document.body.style.overflow = "hidden";
  els.copyImport.classList.remove("copied");
  els.copyImport.textContent = "Copy";
  els.copySource.classList.remove("copied");
  els.copySource.textContent = "Copy";

  els.panelViz.closest(".panel-viz-wrap").style.display = isDoc ? "none" : "block";
  if (!isDoc) renderVisualizer(els.panelViz, item);

  if (pushHash) history.pushState(null, "", `#/a/${item.id}`);
  els.panelClose.focus();
}

function closePanel(pushHash = true) {
  if (els.panel.hidden) return;
  if (state.openAlgoId) {
    destroyVisualizer(state.openAlgoId);
    state.openAlgoId = null;
  }
  els.backdrop.hidden = true;
  els.panel.hidden = true;
  document.body.style.overflow = "";
  if (pushHash) history.pushState(null, "", "#/");
}

function syncPanelToHash() {
  const match = location.hash.match(/^#\/a\/([a-z0-9-]+)$/);
  if (!match) {
    closePanel(false);
    return;
  }
  const item = allItems().find((a) => a.id === match[1]);
  if (item) openPanel(item, false);
  else closePanel(false);
}

async function copyText(text, btn) {
  try {
    await navigator.clipboard.writeText(text);
    btn.textContent = "Copied";
    btn.classList.add("copied");
  } catch {
    btn.textContent = "Select + Ctrl/Cmd-C";
  }
}

/* ---------- Events ---------- */

let searchTimer;
let resizeTimer;
els.search.addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    state.query = els.search.value.trim().toLowerCase();
    render();
  }, 120);
});

document.addEventListener("keydown", (e) => {
  if (e.key === "/" && document.activeElement !== els.search) {
    e.preventDefault();
    els.search.focus();
  }
  if (e.key === "Escape") closePanel();
});

els.panelClose.addEventListener("click", () => closePanel());
els.backdrop.addEventListener("click", () => closePanel());

els.copyImport.addEventListener("click", () => copyText(els.panelImport.textContent, els.copyImport));
els.copySource.addEventListener("click", () => copyText(els.panelSource.textContent, els.copySource));

window.addEventListener("hashchange", syncPanelToHash);
window.addEventListener("popstate", syncPanelToHash);
window.addEventListener("resize", () => {
  if (!state.openAlgoId) return;
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    const item = allItems().find((a) => a.id === state.openAlgoId);
    if (item && item.kind !== "doc") resizeVisualizer(els.panelViz, item);
  }, 150);
});

/* ---------- Boot ---------- */

async function init() {
  try {
    const algoRes = await fetch("data/algorithms.json");
    if (!algoRes.ok) throw new Error(`algorithms HTTP ${algoRes.status}`);
    const algoData = await algoRes.json();
    state.algorithms = algoData.algorithms.map((a) => ({ ...a, kind: "algorithm" }));
    els.heroCount.textContent = state.algorithms.length + "+";
    render();
    syncPanelToHash();
    // Warm-load Shopify docs in the background after algorithms render.
    loadShopifyDocs();
  } catch (err) {
    els.resultCount.textContent =
      "Could not load data. Run scripts/build_algorithm_catalog.py and scripts/build_shopify_knowledge.py.";
    console.error(err);
  }
}

init();
