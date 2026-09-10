/**
 * Consumption dashboard controller: state, drill-down, URL hash sync, 60s polling,
 * comparison fold mode, and KPI/legend/table wiring. Depends on api.js, chart.js,
 * controls.js, series.js, and index.html shell.
 */

import { ApiError, fetchHealth, fetchLocale, fetchSeries } from "./api.js";
import { createChart, onBarClick, refreshChartTheme, renderSeries } from "./chart.js";
import {
  DEFAULT_PRESET,
  applyPreset,
  defaultRangeFor,
  detectPreset,
  daysInMonth,
  onGranularityChange,
  readRangeFromControls,
  rebuildPresetSelect,
  snapRangeForMode,
  syncRangeControls,
} from "./controls.js";
import {
  buildRunningChart,
  computeKpis,
  flatPointsForTable,
  foldForComparison,
  formatNumber,
  isEmptyChart,
} from "./series.js";

const POLL_MS = 60_000;
const STALE_HOURS = 4;
const THEME_KEY = "cm-theme";

const $ = (id) => document.getElementById(id);
const chartWrap = document.querySelector(".chart-wrap");

const els = {
  utility: $("utility"),
  granularity: $("granularity"),
  mode: $("mode"),
  rangeStart: $("range-start"),
  rangeEnd: $("range-end"),
  yearStart: $("year-start"),
  yearEnd: $("year-end"),
  monthStart: $("month-start"),
  monthEnd: $("month-end"),
  hourDayStart: $("hour-day-start"),
  hourDayEnd: $("hour-day-end"),
  hourStart: $("hour-start"),
  hourEnd: $("hour-end"),
  preset: $("preset"),
  kpiTotal: $("kpi-total"),
  kpiAverage: $("kpi-average"),
  kpiPeak: $("kpi-peak"),
  kpiLatest: $("kpi-latest"),
  breadcrumb: $("breadcrumb"),
  chart: $("chart"),
  chartTitle: $("chart-title"),
  chartSubtitle: $("chart-subtitle"),
  chartLegend: $("chart-legend"),
  chartNote: $("chart-note"),
  coverageNote: $("coverage-note"),
  themeToggle: $("theme-toggle"),
  statusPill: $("status-pill"),
  dataTable: $("data-table"),
  tableToggle: $("table-toggle"),
  downloadCsv: $("download-csv"),
  stateLoading: $("state-loading"),
  stateEmpty: $("state-empty"),
  stateError: $("state-error"),
  retry: $("retry"),
};

const state = {
  utility: "electricity",
  direction: "import",
  granularity: "day",
  mode: "running",
  start: "",
  end: "",
  hourStart: "00:00",
  hourEnd: "23:00",
  drillStack: [],
};

let t = {};
let chart = null;
let pollTimer = null;
let chartData = { categories: [], series: [], capped: false };
let seriesMeta = { unit: "", estimated: false };
let coverage = {};
let hiddenSeries = new Set();
let rawPoints = [];

function setText(el, text) {
  if (el) {
    el.textContent = text ?? "";
  }
}

function seriesLabel() {
  if (state.utility === "water") {
    return t["utility.water"] ?? "water";
  }
  const key = `utility.${state.utility}_${state.direction}`;
  return t[key] ?? `${state.utility} ${state.direction}`;
}

function granularityLabel() {
  return t[`granularity.${state.granularity}`] ?? state.granularity;
}

function syncPresetFromState() {
  if (!els.preset) {
    return;
  }
  const id = detectPreset(state.granularity, state, coverage);
  els.preset.value = id;
}

function syncControlsFromState() {
  snapRangeForMode(state);
  syncRangeControls(els, state, state.granularity, coverage);
  syncPresetFromState();
  syncUtilityButtons();
  syncGranularityButtons();
  syncModeButtons();
}

function syncModeButtons() {
  const modeGroup = document.getElementById("mode-group");
  const allowed = state.granularity !== "year";
  if (modeGroup) {
    modeGroup.hidden = !allowed;
  }
  if (!allowed) {
    state.mode = "running";
  }
  if (!els.mode) {
    return;
  }
  for (const btn of els.mode.querySelectorAll("button")) {
    const m = btn.dataset.mode;
    btn.setAttribute("aria-pressed", m === state.mode ? "true" : "false");
  }
}

function initTheme() {
  const stored = localStorage.getItem(THEME_KEY);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const theme = stored === "light" || stored === "dark" ? stored : prefersDark ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", theme);
  if (els.themeToggle) {
    els.themeToggle.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
  }
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem(THEME_KEY, next);
  if (els.themeToggle) {
    els.themeToggle.setAttribute("aria-pressed", next === "dark" ? "true" : "false");
  }
  if (chart && chartData.series.length) {
    paintChart();
  } else {
    refreshChartTheme(chart);
  }
}

function showState(which) {
  const states = { loading: els.stateLoading, empty: els.stateEmpty, error: els.stateError };
  for (const [name, el] of Object.entries(states)) {
    if (el) {
      el.hidden = name !== which;
    }
  }
  if (chartWrap) {
    chartWrap.hidden = true;
  }
}

function hideStates() {
  for (const el of [els.stateLoading, els.stateEmpty, els.stateError]) {
    if (el) {
      el.hidden = true;
    }
  }
  if (chartWrap) {
    chartWrap.hidden = false;
  }
}

function parseHash() {
  const raw = location.hash.replace(/^#/, "");
  if (!raw) {
    return null;
  }
  const params = new URLSearchParams(raw);
  return {
    utility: params.get("u"),
    direction: params.get("d"),
    granularity: params.get("g"),
    mode: params.get("m"),
    compare: params.get("c"),
    start: params.get("s"),
    end: params.get("e"),
    hourStart: params.get("hs"),
    hourEnd: params.get("he"),
  };
}

function writeHash() {
  const params = new URLSearchParams({
    u: state.utility,
    d: state.direction,
    g: state.granularity,
    m: state.mode,
    s: state.start,
    e: state.end,
    hs: state.hourStart,
    he: state.hourEnd,
  });
  const next = `#${params}`;
  if (location.hash !== next) {
    history.replaceState(null, "", next);
  }
}

function applyHash(hash) {
  if (!hash) {
    return;
  }
  if (hash.utility) {
    state.utility = hash.utility;
  }
  if (hash.direction) {
    state.direction = hash.direction;
  }
  if (hash.granularity) {
    state.granularity = hash.granularity;
  }
  if (hash.mode === "comparison" || hash.mode === "running") {
    state.mode = hash.mode;
  } else if (hash.compare && hash.compare !== "none") {
    state.mode = "comparison";
  }
  if (state.granularity === "year" && state.mode === "comparison") {
    state.mode = "running";
  }
  if (hash.start) {
    state.start = hash.start;
  }
  if (hash.end) {
    state.end = hash.end;
  }
  if (hash.hourStart) {
    state.hourStart = hash.hourStart;
  }
  if (hash.hourEnd) {
    state.hourEnd = hash.hourEnd;
  }
  state.drillStack = [];
}

function buttonMatchesUtility(btn) {
  const u = btn.dataset.utility;
  const d = btn.dataset.direction;
  if (u === "water") {
    return state.utility === "water";
  }
  return state.utility === u && state.direction === d;
}

function syncUtilityButtons() {
  if (!els.utility) {
    return;
  }
  for (const btn of els.utility.querySelectorAll("button")) {
    btn.setAttribute("aria-pressed", buttonMatchesUtility(btn) ? "true" : "false");
  }
}

function syncGranularityButtons() {
  if (!els.granularity) {
    return;
  }
  for (const btn of els.granularity.querySelectorAll("button")) {
    const g = btn.dataset.granularity ?? btn.value;
    btn.setAttribute("aria-pressed", g === state.granularity ? "true" : "false");
  }
}

function readUtilityFromEvent(btn) {
  const u = btn.dataset.utility;
  if (!u) {
    return;
  }
  state.utility = u;
  state.direction = u === "water" ? "water" : btn.dataset.direction ?? "import";
}

function buildChartData(points) {
  if (state.mode === "comparison") {
    return foldForComparison(points, state.granularity, t, state.hourStart, state.hourEnd);
  }
  return buildRunningChart(points, state.granularity, t);
}

function paintChart() {
  if (!chart) {
    return;
  }
  chart.resize();
  renderSeries(chart, {
    categories: chartData.categories,
    series: chartData.series,
    granularity: state.granularity,
    unit: seriesMeta.unit,
    estimated: seriesMeta.estimated,
    hiddenKeys: hiddenSeries,
    t,
  });
}

function renderKpiDelta(el, current, previous) {
  if (!el || current == null || previous == null) {
    if (el) {
      el.hidden = true;
    }
    return;
  }
  const diff = current - previous;
  if (diff === 0) {
    el.hidden = true;
    return;
  }
  el.hidden = false;
  const valueEl = el.querySelector("[data-kpi-delta-value]");
  setText(valueEl, formatNumber(Math.abs(diff)));
  el.classList.remove("kpi-delta--positive", "kpi-delta--negative");
  el.classList.add(diff < 0 ? "kpi-delta--positive" : "kpi-delta--negative");
  const svg = el.querySelector("svg path");
  if (svg) {
    svg.setAttribute(
      "d",
      diff < 0
        ? "M12 5v14m0 0 7-7m-7 7-7-7"
        : "M12 19V5m0 0-7 7m7-7 7 7",
    );
  }
}

function kpiSourceSeries() {
  const visible = chartData.series.filter((s) => !hiddenSeries.has(s.key));
  if (!visible.length) {
    return [];
  }
  if (state.mode === "comparison") {
    return visible[visible.length - 1].points;
  }
  return visible[0].points;
}

function renderKpis() {
  const points = kpiSourceSeries();
  const kpis = computeKpis(points);
  setText(els.kpiTotal, formatNumber(kpis.total));
  setText(els.kpiAverage, formatNumber(kpis.average));
  setText(els.kpiPeak, kpis.peak != null ? formatNumber(kpis.peak) : "—");
  setText(els.kpiLatest, formatNumber(kpis.latest));
  const unitKey = seriesMeta.unit === "m3" || seriesMeta.unit === "m³" ? "unit.m3" : "unit.kwh";
  const unitLabel = t[unitKey] ?? seriesMeta.unit ?? "";
  for (const el of document.querySelectorAll("[data-kpi-unit]")) {
    setText(el, unitLabel);
  }

  let compKpis = null;
  if (state.mode === "comparison" && chartData.series.length > 1) {
    const visible = chartData.series.filter((s) => !hiddenSeries.has(s.key));
    if (visible.length >= 2) {
      compKpis = computeKpis(visible[visible.length - 2].points);
    }
  }

  const cards = document.querySelectorAll(".kpi-card");
  const deltas = [kpis.total, kpis.average, kpis.peak, kpis.latest];
  const compDeltas = compKpis
    ? [compKpis.total, compKpis.average, compKpis.peak, compKpis.latest]
    : [];
  cards.forEach((card, idx) => {
    const deltaEl = card.querySelector("[data-kpi-delta]");
    renderKpiDelta(deltaEl, deltas[idx], state.mode === "comparison" ? compDeltas[idx] : null);
  });
}

function renderChartTitles() {
  const titleTpl = t["chart.title_template"] ?? "{series} — {granularity}";
  const modeSuffix =
    state.mode === "comparison" ? ` (${t["mode.comparison"] ?? ""})` : "";
  setText(
    els.chartTitle,
    titleTpl
      .replace("{series}", seriesLabel())
      .replace("{granularity}", granularityLabel()) + modeSuffix,
  );
  const subTpl = t["chart.subtitle_range"] ?? "{start} – {end}";
  let subtitle = subTpl.replace("{start}", state.start).replace("{end}", state.end);
  if (state.granularity === "hour") {
    subtitle += ` · ${state.hourStart}–${state.hourEnd}`;
  }
  if (state.mode === "comparison" && chartData.series.length > 1) {
    const visible = chartData.series.filter((s) => !hiddenSeries.has(s.key));
    if (visible.length >= 2) {
      const tpl = t["chart.subtitle_compare"] ?? "{current} מול {previous}";
      subtitle = tpl
        .replace("{current}", visible[visible.length - 1].label)
        .replace("{previous}", visible[visible.length - 2].label);
    }
  }
  setText(els.chartSubtitle, subtitle);
}

function renderLegend() {
  if (!els.chartLegend) {
    return;
  }
  while (els.chartLegend.firstChild) {
    els.chartLegend.removeChild(els.chartLegend.firstChild);
  }
  els.chartLegend.hidden = chartData.series.length === 0;
  if (chartData.series.length === 0) {
    return;
  }
  for (const s of chartData.series) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "chart-legend__item";
    const hidden = hiddenSeries.has(s.key);
    btn.setAttribute("aria-pressed", hidden ? "false" : "true");
    btn.dataset.seriesKey = s.key;
    const swatch = document.createElement("span");
    swatch.className = "chart-legend__swatch";
    swatch.style.background = `var(--series-${(s.colorIndex % 12) + 1})`;
    if (hidden) {
      swatch.style.opacity = "0.35";
    }
    const label = document.createElement("span");
    const total = s.total != null ? formatNumber(s.total) : "—";
    label.textContent = `${s.label} (${total})`;
    btn.appendChild(swatch);
    btn.appendChild(label);
    btn.addEventListener("click", () => {
      if (hiddenSeries.has(s.key)) {
        hiddenSeries.delete(s.key);
      } else {
        hiddenSeries.add(s.key);
      }
      paintChart();
      renderLegend();
      renderKpis();
      renderChartTitles();
    });
    els.chartLegend.appendChild(btn);
  }
}

function renderCoverageNote(health) {
  if (!els.coverageNote) {
    return;
  }
  const cov = health?.coverage?.[state.utility];
  if (!cov?.first_date) {
    els.coverageNote.hidden = true;
    return;
  }
  const tpl = t["coverage.note"] ?? "";
  setText(
    els.coverageNote,
    tpl
      .replace("{first}", cov.first_date)
      .replace("{last}", cov.last_date ?? cov.first_date)
      .replace("{count}", String(cov.reading_count ?? 0)),
  );
  els.coverageNote.hidden = false;
}

function crumbLabel(granularity, start, end) {
  if (granularity === "year") {
    const from = start.slice(0, 4);
    const to = end.slice(0, 4);
    return from === to ? from : `${from}\u2013${to}`;
  }
  if (granularity === "month") {
    return start.slice(0, 4);
  }
  if (granularity === "day") {
    const mo = Number(start.slice(5, 7));
    return `${t[`month.${mo}`] ?? start.slice(5, 7)} ${start.slice(0, 4)}`;
  }
  return start;
}

function renderBreadcrumb() {
  if (!els.breadcrumb) {
    return;
  }
  while (els.breadcrumb.firstChild) {
    els.breadcrumb.removeChild(els.breadcrumb.firstChild);
  }
  const crumbs = [...state.drillStack, { granularity: state.granularity, start: state.start, end: state.end }];
  if (crumbs.length <= 1 && state.drillStack.length === 0) {
    els.breadcrumb.hidden = true;
    return;
  }
  els.breadcrumb.hidden = false;
  crumbs.forEach((crumb, idx) => {
    if (idx > 0) {
      const sep = document.createElement("span");
      sep.className = "breadcrumb__sep";
      sep.textContent = " / ";
      sep.setAttribute("aria-hidden", "true");
      els.breadcrumb.appendChild(sep);
    }
    const label = crumbLabel(crumb.granularity, crumb.start, crumb.end);
    if (idx === crumbs.length - 1) {
      const current = document.createElement("span");
      current.className = "breadcrumb__item breadcrumb__item--current";
      current.setAttribute("aria-current", "page");
      current.textContent = label;
      els.breadcrumb.appendChild(current);
      return;
    }
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "breadcrumb__item";
    btn.textContent = label;
    btn.addEventListener("click", () => popDrill(idx));
    els.breadcrumb.appendChild(btn);
  });
}

function popDrill(index) {
  if (index >= state.drillStack.length) {
    return;
  }
  const target = state.drillStack[index];
  state.drillStack = state.drillStack.slice(0, index);
  state.granularity = target.granularity;
  state.mode = target.mode ?? "running";
  state.start = target.start;
  state.end = target.end;
  state.hourStart = target.hourStart ?? "00:00";
  state.hourEnd = target.hourEnd ?? "23:00";
  hiddenSeries = new Set();
  rebuildPresetSelect(els.preset, state.granularity, t);
  syncControlsFromState();
  writeHash();
  loadData();
}

function drillDown(next) {
  state.drillStack.push({
    granularity: state.granularity,
    mode: state.mode,
    start: state.start,
    end: state.end,
    hourStart: state.hourStart,
    hourEnd: state.hourEnd,
  });
  state.granularity = next.granularity;
  state.mode = next.mode ?? state.mode;
  state.start = next.start;
  state.end = next.end;
  state.hourStart = next.hourStart ?? state.hourStart;
  state.hourEnd = next.hourEnd ?? state.hourEnd;
  hiddenSeries = new Set();
  syncControlsFromState();
  writeHash();
  loadData();
}

function handleBarClick({ seriesKey, point, granularity }) {
  if (state.mode === "comparison") {
    if (granularity === "month") {
      const year = seriesKey;
      const mo = Number(point.iso.slice(5, 7));
      const last = daysInMonth(Number(year), mo);
      const mm = String(mo).padStart(2, "0");
      drillDown({
        granularity: "day",
        mode: "running",
        start: `${year}-${mm}-01`,
        end: `${year}-${mm}-${String(last).padStart(2, "0")}`,
        hourStart: state.hourStart,
        hourEnd: state.hourEnd,
      });
      return;
    }
    if (granularity === "day") {
      const [y, m] = seriesKey.split("-").map(Number);
      const day = Number(point.iso.slice(8, 10));
      const mm = String(m).padStart(2, "0");
      const dd = String(day).padStart(2, "0");
      drillDown({
        granularity: "hour",
        mode: "running",
        start: `${y}-${mm}-${dd}`,
        end: `${y}-${mm}-${dd}`,
        hourStart: "00:00",
        hourEnd: "23:00",
      });
      return;
    }
    if (granularity === "hour") {
      return;
    }
    if (granularity === "year") {
      const year = point.label;
      drillDown({
        granularity: "month",
        mode: state.mode,
        start: `${year}-01-01`,
        end: `${year}-12-31`,
        hourStart: state.hourStart,
        hourEnd: state.hourEnd,
      });
      return;
    }
  }

  if (granularity === "year") {
    const year = point.label;
    drillDown({
      granularity: "month",
      mode: state.mode,
      start: `${year}-01-01`,
      end: `${year}-12-31`,
      hourStart: state.hourStart,
      hourEnd: state.hourEnd,
    });
  } else if (granularity === "month") {
    const [y, m] = point.label.split("-").map(Number);
    const last = daysInMonth(y, m);
    const mm = String(m).padStart(2, "0");
    drillDown({
      granularity: "day",
      mode: state.mode,
      start: `${y}-${mm}-01`,
      end: `${y}-${mm}-${String(last).padStart(2, "0")}`,
      hourStart: state.hourStart,
      hourEnd: state.hourEnd,
    });
  } else if (granularity === "day") {
    drillDown({
      granularity: "hour",
      mode: state.mode,
      start: point.iso,
      end: point.iso,
      hourStart: "00:00",
      hourEnd: "23:00",
    });
  }
}

function renderTable() {
  if (!els.dataTable) {
    return;
  }
  const tbody = els.dataTable.querySelector("tbody");
  if (!tbody) {
    return;
  }
  while (tbody.firstChild) {
    tbody.removeChild(tbody.firstChild);
  }
  const rows = flatPointsForTable(chartData);
  for (const p of rows) {
    const tr = document.createElement("tr");
    const tdPeriod = document.createElement("td");
    tdPeriod.textContent = state.mode === "comparison" ? `${p.series} · ${p.label}` : p.label;
    const tdValue = document.createElement("td");
    tdValue.dir = "ltr";
    tdValue.textContent =
      p.value != null ? `${formatNumber(p.value)} ${seriesMeta.unit}` : "—";
    tr.appendChild(tdPeriod);
    tr.appendChild(tdValue);
    tbody.appendChild(tr);
  }
}

function updateChartAria() {
  if (!els.chart) {
    return;
  }
  const count = chartData.categories.length;
  const tpl = t["chart.aria_summary"] ?? "{count} periods, unit {unit}";
  const summary = count
    ? tpl.replace("{count}", String(count)).replace("{unit}", seriesMeta.unit)
    : t["chart.no_data"] ?? "no data";
  els.chart.setAttribute("aria-label", summary);
}

function renderChartNote() {
  if (!els.chartNote) {
    return;
  }
  const notes = [];
  if (state.granularity === "hour" && seriesMeta.estimated) {
    notes.push(t["chart.estimated_note"] ?? "");
  }
  if (rawPoints.some((p) => p.partial)) {
    notes.push(t["chart.partial_note"] ?? "");
  }
  if (chartData.capped) {
    notes.push(t["chart.series_cap_note"] ?? "");
  }
  if (!notes.length) {
    els.chartNote.hidden = true;
    return;
  }
  setText(els.chartNote, notes.join(" "));
  els.chartNote.hidden = false;
}

async function loadData() {
  if (!rawPoints.length) {
    showState("loading");
  }
  try {
    const { points, meta } = await fetchSeries({
      utility: state.utility,
      direction: state.direction,
      granularity: state.granularity,
      start: state.start,
      end: state.end,
      hourStart: state.hourStart,
      hourEnd: state.hourEnd,
    });
    rawPoints = points;
    seriesMeta = meta;
    chartData = buildChartData(points);
    if (state.mode === "running" && chartData.series[0]) {
      const subTpl = t["chart.subtitle_range"] ?? "{start} – {end}";
      chartData.series[0].label = subTpl
        .replace("{start}", state.start)
        .replace("{end}", state.end);
    }

    if (isEmptyChart(chartData)) {
      showState("empty");
      paintChart();
      renderKpis();
      renderTable();
      renderBreadcrumb();
      renderChartTitles();
      renderLegend();
      renderChartNote();
      return;
    }

    hideStates();
    paintChart();
    renderKpis();
    renderTable();
    updateChartAria();
    renderBreadcrumb();
    renderChartTitles();
    renderLegend();
    renderChartNote();
  } catch (err) {
    showState("error");
    const msg = err instanceof ApiError ? err.message : t["chart.error"] ?? String(err);
    const errText =
      els.stateError?.querySelector(".state-panel__message") ?? els.stateError;
    setText(errText, msg);
  }
}

const relativeFmt = new Intl.RelativeTimeFormat("he", { numeric: "auto", style: "short" });

function relativeTime(isoUtc) {
  const diffSec = Math.round((Date.now() - new Date(isoUtc).getTime()) / 1000);
  const abs = Math.abs(diffSec);
  if (abs < 60) {
    return relativeFmt.format(-Math.round(diffSec / 60) || 0, "minute");
  }
  if (abs < 3600) {
    return relativeFmt.format(-Math.round(diffSec / 60), "minute");
  }
  if (abs < 86_400) {
    return relativeFmt.format(-Math.round(diffSec / 3600), "hour");
  }
  return relativeFmt.format(-Math.round(diffSec / 86_400), "day");
}

async function updateStatus() {
  if (!els.statusPill) {
    return;
  }
  let status = "offline";
  let readingTime = null;
  try {
    const health = await fetchHealth();
    coverage = health.coverage ?? {};
    renderCoverageNote(health);
    readingTime = health.coverage?.[state.utility]?.last_reading_utc ?? null;
    if (readingTime) {
      const ageH = (Date.now() - new Date(readingTime).getTime()) / 3_600_000;
      status = ageH < STALE_HOURS ? "live" : "stale";
    } else if (health.status === "ok") {
      status = "stale";
    }
  } catch {
    status = "offline";
    if (els.coverageNote) {
      els.coverageNote.hidden = true;
    }
  }

  els.statusPill.classList.remove(
    "status-pill--live",
    "status-pill--stale",
    "status-pill--offline",
  );
  els.statusPill.classList.add(`status-pill--${status}`);
  const label =
    status === "live"
      ? t["status.live"]
      : status === "stale"
        ? t["status.stale"]
        : t["status.offline"];
  const rel = readingTime ? relativeTime(readingTime) : "";
  const agoTemplate = t["status.updated_ago"] ?? "";
  const ago = rel ? agoTemplate.replace("{0}", rel).replace("{time}", rel) : "";
  const textEl = els.statusPill.querySelector(".status-pill__text");
  setText(textEl, ago || label);
}

async function refresh() {
  await Promise.all([loadData(), updateStatus()]);
}

function startPoll() {
  stopPoll();
  pollTimer = setInterval(() => {
    if (document.visibilityState === "visible") {
      refresh();
    }
  }, POLL_MS);
}

function stopPoll() {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
}

function exportCsv() {
  const unit = seriesMeta.unit ?? "";
  const headerPeriod = t["table.period"] ?? "period";
  const headerValue = t["table.value"] ?? "value";
  const lines = [`\uFEFF${headerPeriod},${headerValue} (${unit})`];
  for (const p of flatPointsForTable(chartData)) {
    const period = state.mode === "comparison" ? `${p.series} · ${p.label}` : p.label;
    const val = p.value != null ? String(p.value) : "";
    lines.push(`"${period.replace(/"/g, '""')}",${val}`);
  }
  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `consumption-${state.utility}-${state.start}-${state.end}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

function onRangeChange() {
  readRangeFromControls(els, state, state.granularity, coverage);
  state.drillStack = [];
  hiddenSeries = new Set();
  syncControlsFromState();
  writeHash();
  loadData();
}

function bindEvents() {
  els.utility?.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) {
      return;
    }
    readUtilityFromEvent(btn);
    state.drillStack = [];
    hiddenSeries = new Set();
    const defaults = defaultRangeFor(state.granularity, coverage, state.utility);
    Object.assign(state, defaults);
    syncUtilityButtons();
    rebuildPresetSelect(els.preset, state.granularity, t);
    syncControlsFromState();
    writeHash();
    refresh();
  });

  els.granularity?.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn || btn.disabled) {
      return;
    }
    const g = btn.dataset.granularity ?? btn.value;
    if (!g) {
      return;
    }
    onGranularityChange(state, g, coverage);
    state.drillStack = [];
    hiddenSeries = new Set();
    rebuildPresetSelect(els.preset, g, t);
    els.preset.value = DEFAULT_PRESET[g] ?? "custom";
    syncControlsFromState();
    writeHash();
    loadData();
  });

  els.mode?.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) {
      return;
    }
    const m = btn.dataset.mode;
    if (!m || m === state.mode) {
      return;
    }
    state.mode = m;
    hiddenSeries = new Set();
    syncControlsFromState();
    writeHash();
    loadData();
  });

  for (const id of [
    "rangeStart",
    "rangeEnd",
    "yearStart",
    "yearEnd",
    "monthStart",
    "monthEnd",
    "hourDayStart",
    "hourDayEnd",
    "hourStart",
    "hourEnd",
  ]) {
    els[id]?.addEventListener("change", onRangeChange);
  }

  els.preset?.addEventListener("change", () => {
    const id = els.preset.value;
    if (id === "custom" || !applyPreset(state.granularity, id, state, coverage)) {
      syncPresetFromState();
      return;
    }
    state.drillStack = [];
    hiddenSeries = new Set();
    syncControlsFromState();
    writeHash();
    loadData();
  });

  els.themeToggle?.addEventListener("click", toggleTheme);
  els.retry?.addEventListener("click", () => loadData());
  els.downloadCsv?.addEventListener("click", exportCsv);

  els.tableToggle?.addEventListener("click", () => {
    const wrap = document.getElementById("table-wrap");
    if (!wrap) {
      return;
    }
    const open = wrap.hidden;
    wrap.hidden = !open;
    els.tableToggle.setAttribute("aria-expanded", open ? "true" : "false");
  });

  window.addEventListener("hashchange", () => {
    applyHash(parseHash());
    hiddenSeries = new Set();
    rebuildPresetSelect(els.preset, state.granularity, t);
    syncControlsFromState();
    loadData();
  });

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") {
      refresh();
    }
  });
}

function applyLocale(strings) {
  for (const el of document.querySelectorAll("[data-i18n]")) {
    const key = el.dataset.i18n;
    if (key && strings[key] != null) {
      setText(el, strings[key]);
    }
  }
  for (const el of document.querySelectorAll("[data-i18n-aria]")) {
    const key = el.dataset.i18nAria;
    if (key && strings[key] != null) {
      el.setAttribute("aria-label", strings[key]);
    }
  }
  document.title = strings["app.title"] ?? document.title;
}

async function init() {
  initTheme();
  t = await fetchLocale();
  applyLocale(t);

  const health = await fetchHealth();
  coverage = health.coverage ?? {};

  const hash = parseHash();
  const g = hash?.granularity ?? "day";
  const defaults = defaultRangeFor(g, coverage, hash?.utility ?? "electricity");
  Object.assign(state, defaults);
  state.granularity = g;
  applyHash(hash);

  rebuildPresetSelect(els.preset, state.granularity, t);
  syncControlsFromState();
  bindEvents();

  if (els.chart) {
    chart = createChart(els.chart, t);
    onBarClick(handleBarClick);
  }

  await refresh();
  startPoll();
}

init();
