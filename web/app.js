/**
 * Consumption dashboard controller: state machine, drill-down stack, URL hash
 * sync, 60s polling (paused when hidden), KPI/table/CSV wiring. Binds to the
 * frozen DOM ids from dashboard-contract; no exports. Depends on api.js, chart.js,
 * vendor/chart.umd.min.js, and the HTML shell from index.html.
 */

import { ApiError, fetchHealth, fetchLocale, fetchSeries } from "./api.js";
import { createChart, onBarClick, refreshChartTheme, renderSeries } from "./chart.js";

const POLL_MS = 60_000;
const STALE_HOURS = 4;

const $ = (id) => document.getElementById(id);

const chartWrap = document.querySelector(".chart-wrap");

const els = {
  utility: $("utility"),
  granularity: $("granularity"),
  rangeStart: $("range-start"),
  rangeEnd: $("range-end"),
  preset: $("preset"),
  compare: $("compare"),
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
  start: "",
  end: "",
  compare: "none",
  drillStack: [],
};

let t = {};
let chart = null;
let pollTimer = null;
let primarySeries = [];
let comparisonSeries = null;
let seriesMeta = { unit: "", estimated: false };
let coverage = {};
// Restored when the user leaves the hour view, which had to collapse the range to one day.
let rangeBeforeHour = null;
const THEME_KEY = "cm-theme";

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

function parseIso(s) {
  const [y, m, d] = s.split("-").map(Number);
  return new Date(y, m - 1, d);
}

function formatIso(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

function addDays(iso, n) {
  const d = parseIso(iso);
  d.setDate(d.getDate() + n);
  return formatIso(d);
}

function daysInclusive(start, end) {
  const ms = parseIso(end) - parseIso(start);
  return Math.floor(ms / 86_400_000) + 1;
}

function daysInMonth(year, month) {
  return new Date(year, month, 0).getDate();
}

function shiftYear(iso, delta) {
  const d = parseIso(iso);
  d.setFullYear(d.getFullYear() + delta);
  return formatIso(d);
}

function defaultRange() {
  const end = todayIso();
  const start = addDays(end, -29);
  return { start, end };
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

function detectPreset(start, end) {
  const endToday = todayIso();
  if (end !== endToday) {
    return "custom";
  }
  if (start === addDays(end, -6)) {
    return "7d";
  }
  if (start === addDays(end, -29)) {
    return "30d";
  }
  if (start === `${end.slice(0, 8)}01`) {
    return "this_month";
  }
  if (start === `${end.slice(0, 4)}-01-01`) {
    return "this_year";
  }
  const first = coverage[state.utility]?.first_date;
  if (first && start === first) {
    return "all";
  }
  return "custom";
}

/** Last day that actually holds readings, so the hour view never opens on an empty day. */
function lastCoveredDay(fallback) {
  const last = coverage[state.utility]?.last_date;
  return last && last < fallback ? last : fallback;
}

function syncPresetFromState() {
  if (!els.preset) {
    return;
  }
  els.preset.value = detectPreset(state.start, state.end);
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
  if (chart && primarySeries.length) {
    renderSeries(chart, {
      primary: primarySeries,
      comparison: comparisonSeries,
      granularity: state.granularity,
      unit: seriesMeta.unit,
      estimated: seriesMeta.estimated,
      t,
    });
  } else {
    refreshChartTheme(chart);
  }
}

function setText(el, text) {
  if (el) {
    el.textContent = text ?? "";
  }
}

/** Loading, empty and error replace the canvas only; controls stay reachable. */
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
    start: params.get("s"),
    end: params.get("e"),
    compare: params.get("c"),
  };
}

function writeHash() {
  const params = new URLSearchParams({
    u: state.utility,
    d: state.direction,
    g: state.granularity,
    s: state.start,
    e: state.end,
    c: state.compare,
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
  if (hash.start) {
    state.start = hash.start;
  }
  if (hash.end) {
    state.end = hash.end;
  }
  if (hash.compare) {
    state.compare = hash.compare === "prev" ? "previous" : hash.compare;
  }
  state.drillStack = [];
}

function utilityKey() {
  if (state.utility === "water") {
    return "water";
  }
  return `${state.utility}_${state.direction}`;
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

/**
 * The hour endpoint serves exactly one day, so entering the hour view collapses the
 * range and leaving it restores whatever range the user had before.
 */
function setGranularity(g) {
  if (g === "hour" && state.granularity !== "hour") {
    if (state.start !== state.end) {
      rangeBeforeHour = { start: state.start, end: state.end };
    }
    const day = lastCoveredDay(state.end);
    state.start = day;
    state.end = day;
  } else if (g !== "hour" && state.granularity === "hour" && rangeBeforeHour) {
    state.start = rangeBeforeHour.start;
    state.end = rangeBeforeHour.end;
    rangeBeforeHour = null;
  }
  state.granularity = g;
}

function syncControlsFromState() {
  if (els.rangeStart) {
    els.rangeStart.value = state.start;
  }
  if (els.rangeEnd) {
    els.rangeEnd.value = state.end;
  }
  syncPresetFromState();
  if (els.compare) {
    els.compare.value = state.compare;
  }
  syncUtilityButtons();
  syncGranularityButtons();
}

function readUtilityFromEvent(btn) {
  const u = btn.dataset.utility;
  if (!u) {
    return;
  }
  state.utility = u;
  state.direction = u === "water" ? "water" : btn.dataset.direction ?? "import";
}

function comparisonRange() {
  if (state.compare === "none") {
    return null;
  }
  const span = daysInclusive(state.start, state.end);
  if (state.compare === "previous" || state.compare === "prev") {
    const end = addDays(state.start, -1);
    const start = addDays(end, -(span - 1));
    return { start, end };
  }
  if (state.compare === "last_year") {
    return { start: shiftYear(state.start, -1), end: shiftYear(state.end, -1) };
  }
  return null;
}

function alignByPosition(primary, comparison) {
  return primary.map((_, i) => comparison[i] ?? null);
}

function formatNumber(n) {
  if (n == null || Number.isNaN(n)) {
    return "—";
  }
  return new Intl.NumberFormat("he-IL", { maximumFractionDigits: 2 }).format(n);
}

function computeKpis(points) {
  const values = points.filter((p) => p.value != null).map((p) => p.value);
  if (!values.length) {
    return { total: null, average: null, peak: null, peakLabel: "", latest: null };
  }
  const total = values.reduce((a, b) => a + b, 0);
  const average = total / values.length;
  let peak = values[0];
  let peakIdx = 0;
  for (let i = 0; i < points.length; i += 1) {
    const v = points[i].value;
    if (v != null && v >= peak) {
      peak = v;
      peakIdx = i;
    }
  }
  let latest = null;
  for (let i = points.length - 1; i >= 0; i -= 1) {
    if (points[i].value != null) {
      latest = points[i].value;
      break;
    }
  }
  return {
    total,
    average,
    peak,
    peakLabel: points[peakIdx]?.label ?? "",
    latest,
  };
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

function renderKpis(kpis, unit, compKpis = null) {
  setText(els.kpiTotal, formatNumber(kpis.total));
  setText(els.kpiAverage, formatNumber(kpis.average));
  setText(els.kpiPeak, kpis.peak != null ? `${formatNumber(kpis.peak)}` : "—");
  setText(els.kpiLatest, formatNumber(kpis.latest));
  const unitKey = unit === "m3" || unit === "m³" ? "unit.m3" : "unit.kwh";
  const unitLabel = t[unitKey] ?? unit ?? "";
  for (const el of document.querySelectorAll("[data-kpi-unit]")) {
    setText(el, unitLabel);
  }
  const cards = document.querySelectorAll(".kpi-card");
  const deltas = [kpis.total, kpis.average, kpis.peak, kpis.latest];
  const compDeltas = compKpis
    ? [compKpis.total, compKpis.average, compKpis.peak, compKpis.latest]
    : [];
  cards.forEach((card, idx) => {
    const deltaEl = card.querySelector("[data-kpi-delta]");
    renderKpiDelta(deltaEl, deltas[idx], compDeltas[idx] ?? null);
  });
}

function renderChartTitles() {
  const titleTpl = t["chart.title_template"] ?? "{series} — {granularity}";
  setText(
    els.chartTitle,
    titleTpl
      .replace("{series}", seriesLabel())
      .replace("{granularity}", granularityLabel()),
  );
  const subTpl = t["chart.subtitle_range"] ?? "{start} – {end}";
  setText(
    els.chartSubtitle,
    subTpl.replace("{start}", state.start).replace("{end}", state.end),
  );
}

function renderLegend(show) {
  if (!els.chartLegend) {
    return;
  }
  els.chartLegend.hidden = !show;
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

/** A crumb names the view it returns to, not the first period inside that view. */
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
  state.start = target.start;
  state.end = target.end;
  syncControlsFromState();
  writeHash();
  loadData();
}

function drillDown(next) {
  state.drillStack.push({
    granularity: state.granularity,
    start: state.start,
    end: state.end,
  });
  state.granularity = next.granularity;
  state.start = next.start;
  state.end = next.end;
  syncControlsFromState();
  writeHash();
  loadData();
}

function handleBarClick({ point, granularity }) {
  if (granularity === "year") {
    const year = point.label;
    drillDown({ granularity: "month", start: `${year}-01-01`, end: `${year}-12-31` });
  } else if (granularity === "month") {
    const [y, m] = point.label.split("-").map(Number);
    const last = daysInMonth(y, m);
    const mm = String(m).padStart(2, "0");
    drillDown({
      granularity: "day",
      start: `${y}-${mm}-01`,
      end: `${y}-${mm}-${String(last).padStart(2, "0")}`,
    });
  } else if (granularity === "day") {
    drillDown({ granularity: "hour", start: point.iso, end: point.iso });
  }
}

function renderTable(points, unit) {
  if (!els.dataTable) {
    return;
  }
  const tbody = els.dataTable.querySelector("tbody") ?? els.dataTable;
  while (tbody.firstChild) {
    tbody.removeChild(tbody.firstChild);
  }
  for (const p of points) {
    const tr = document.createElement("tr");
    const tdPeriod = document.createElement("td");
    tdPeriod.textContent = p.label;
    const tdValue = document.createElement("td");
    tdValue.dir = "ltr";
    tdValue.textContent =
      p.value != null ? `${formatNumber(p.value)} ${unit}` : "—";
    tr.appendChild(tdPeriod);
    tr.appendChild(tdValue);
    tbody.appendChild(tr);
  }
}

function updateChartAria(points, unit) {
  if (!els.chart) {
    return;
  }
  const count = points.filter((p) => p.value != null).length;
  const tpl = t["chart.aria_summary"] ?? "{count} periods, unit {unit}";
  const summary = count
    ? tpl.replace("{count}", String(count)).replace("{unit}", unit)
    : t["chart.no_data"] ?? "no data";
  els.chart.setAttribute("aria-label", summary);
}

function renderChartNote() {
  if (!els.chartNote) {
    return;
  }
  if (state.granularity === "hour" && seriesMeta.estimated) {
    setText(els.chartNote, t["chart.estimated_note"] ?? "");
    els.chartNote.hidden = false;
    return;
  }
  if (primarySeries.some((p) => p.partial)) {
    setText(els.chartNote, t["chart.partial_note"] ?? "");
    els.chartNote.hidden = false;
    return;
  }
  els.chartNote.hidden = true;
}

function isEmptySeries(points) {
  return !points.length || points.every((p) => p.value == null);
}

async function loadData() {
  // A skeleton on every 60s poll would blink the chart away; only the first load needs it.
  if (!primarySeries.length) {
    showState("loading");
  }
  try {
    const { points, meta } = await fetchSeries({
      utility: state.utility,
      direction: state.direction,
      granularity: state.granularity,
      start: state.start,
      end: state.end,
    });
    primarySeries = points;
    seriesMeta = meta;

    let comparison = null;
    const compRange = comparisonRange();
    if (compRange) {
      const comp = await fetchSeries({
        utility: state.utility,
        direction: state.direction,
        granularity: state.granularity,
        start: compRange.start,
        end: compRange.end,
      });
      comparison = alignByPosition(points, comp.points);
    }
    comparisonSeries = comparison;

    const compKpis = comparison ? computeKpis(comparison.filter(Boolean)) : null;

    if (isEmptySeries(points)) {
      showState("empty");
      if (chart) {
        renderSeries(chart, {
          primary: [],
          comparison: null,
          granularity: state.granularity,
          unit: meta.unit,
          estimated: meta.estimated,
          t,
        });
      }
      renderKpis(computeKpis([]), meta.unit);
      renderTable([], meta.unit);
      renderBreadcrumb();
      renderChartTitles();
      renderLegend(false);
      renderChartNote();
      return;
    }

    hideStates();
    if (chart) {
      chart.resize();
      renderSeries(chart, {
        primary: points,
        comparison,
        granularity: state.granularity,
        unit: meta.unit,
        estimated: meta.estimated,
        t,
      });
    }
    renderKpis(computeKpis(points), meta.unit, compKpis);
    renderTable(points, meta.unit);
    updateChartAria(points, meta.unit);
    renderBreadcrumb();
    renderChartTitles();
    renderLegend(Boolean(comparison));
    renderChartNote();
  } catch (err) {
    showState("error");
    const msg = err instanceof ApiError ? err.message : t["chart.error"] ?? String(err);
    const errText =
      els.stateError?.querySelector(".state-panel__message") ?? els.stateError;
    setText(errText, msg);
  }
}

function applyPreset(value) {
  // "custom" only ever reports a hand-picked range; selecting it must not move the dates.
  if (value === "custom") {
    syncPresetFromState();
    return;
  }
  const end = todayIso();
  let start = end;
  if (value === "7d") {
    start = addDays(end, -6);
  } else if (value === "30d") {
    start = addDays(end, -29);
  } else if (value === "this_month") {
    start = `${end.slice(0, 8)}01`;
  } else if (value === "this_year") {
    start = `${end.slice(0, 4)}-01-01`;
  } else if (value === "all") {
    start = coverage[state.utility]?.first_date ?? `${end.slice(0, 4)}-01-01`;
  }
  state.start = start;
  state.end = end;
  state.drillStack = [];
  if (state.granularity === "hour" && start !== end) {
    state.granularity = "day";
    rangeBeforeHour = null;
  }
  syncControlsFromState();
  writeHash();
  loadData();
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
  for (const p of primarySeries) {
    const val = p.value != null ? String(p.value) : "";
    lines.push(`"${p.label.replace(/"/g, '""')}",${val}`);
  }
  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `consumption-${state.utility}-${state.start}-${state.end}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

function bindEvents() {
  els.utility?.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) {
      return;
    }
    readUtilityFromEvent(btn);
    state.drillStack = [];
    syncUtilityButtons();
    syncPresetFromState();
    writeHash();
    refresh();
  });

  els.granularity?.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn || btn.disabled) {
      return;
    }
    const g = btn.dataset.granularity ?? btn.value;
    if (g) {
      setGranularity(g);
      state.drillStack = [];
      syncControlsFromState();
      writeHash();
      loadData();
    }
  });

  els.rangeStart?.addEventListener("change", () => {
    state.start = els.rangeStart.value;
    if (state.granularity === "hour" || (state.end && state.start > state.end)) {
      state.end = state.start;
    }
    state.drillStack = [];
    syncControlsFromState();
    writeHash();
    loadData();
  });

  els.rangeEnd?.addEventListener("change", () => {
    state.end = els.rangeEnd.value;
    if (state.granularity === "hour" || (state.start && state.end < state.start)) {
      state.start = state.end;
    }
    state.drillStack = [];
    syncControlsFromState();
    writeHash();
    loadData();
  });

  els.preset?.addEventListener("change", () => {
    if (els.preset.value) {
      applyPreset(els.preset.value);
    }
  });

  els.compare?.addEventListener("change", () => {
    state.compare = els.compare.value || "none";
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

  const hash = parseHash();
  const defaults = defaultRange();
  state.start = defaults.start;
  state.end = defaults.end;
  applyHash(hash);

  if (!state.start || !state.end) {
    Object.assign(state, defaults);
  }

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
