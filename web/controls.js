/**
 * Per-granularity range pickers, preset tables, and canonical date normalisation.
 * Maps visible controls to state.start/end plus hourStart/hourEnd. Depends on
 * coverage from /health; consumed by app.js only.
 */

export const MAX_HOUR_SPAN_DAYS = 14;

export const HOUR_OPTIONS = Array.from({ length: 24 }, (_, h) =>
  `${String(h).padStart(2, "0")}:00`,
);

/** Preset ids per granularity; labels come from locales via preset.<id>. */
export const PRESETS = {
  year: ["all", "last_3", "last_5"],
  month: ["last_12", "this_year", "all"],
  day: ["7d", "30d", "this_month", "last_month"],
  hour: ["last_day", "3d", "7d"],
};

// Phone plots fit about a week of bars; desktop keeps the month view.
const NARROW = window.matchMedia("(max-width: 768px)").matches;

export const DEFAULT_PRESET = {
  year: "all",
  month: "last_12",
  day: NARROW ? "7d" : "30d",
  hour: "last_day",
};

export function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

export function parseIso(s) {
  const [y, m, d] = s.split("-").map(Number);
  return new Date(y, m - 1, d);
}

export function formatIso(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

export function addDays(iso, n) {
  const d = parseIso(iso);
  d.setDate(d.getDate() + n);
  return formatIso(d);
}

export function daysInclusive(start, end) {
  const ms = parseIso(end) - parseIso(start);
  return Math.floor(ms / 86_400_000) + 1;
}

export function daysInMonth(year, month) {
  return new Date(year, month, 0).getDate();
}

export function monthEnd(isoMonth) {
  const [y, m] = isoMonth.split("-").map(Number);
  const last = daysInMonth(y, m);
  return `${y}-${String(m).padStart(2, "0")}-${String(last).padStart(2, "0")}`;
}

/** Comparison folds by the parent unit, so partial parents must not enter the range. */
export function snapRangeForMode(state) {
  if (state.mode !== "comparison") {
    return;
  }
  if (state.granularity === "day") {
    state.start = `${state.start.slice(0, 7)}-01`;
    state.end = monthEnd(state.end.slice(0, 7));
  } else if (state.granularity === "month") {
    state.start = `${state.start.slice(0, 4)}-01-01`;
    state.end = `${state.end.slice(0, 4)}-12-31`;
  }
}

export function lastCoveredDay(coverage, utility, fallback) {
  const last = coverage[utility]?.last_date;
  return last && last < fallback ? last : fallback;
}

export function coverageYears(coverage, utility) {
  const cov = coverage[utility];
  if (!cov?.first_date || !cov?.last_date) {
    const y = todayIso().slice(0, 4);
    return [y];
  }
  const from = Number(cov.first_date.slice(0, 4));
  const to = Number(cov.last_date.slice(0, 4));
  const years = [];
  for (let y = from; y <= to; y += 1) {
    years.push(String(y));
  }
  return years;
}

export function defaultRangeFor(granularity, coverage, utility) {
  const today = todayIso();
  const last = lastCoveredDay(coverage, utility, today);
  const years = coverageYears(coverage, utility);

  if (granularity === "year") {
    return {
      start: `${years[0]}-01-01`,
      end: `${years[years.length - 1]}-12-31`,
      hourStart: "00:00",
      hourEnd: "23:00",
    };
  }
  if (granularity === "month") {
    const endMonth = last.slice(0, 7);
    const d = parseIso(`${endMonth}-01`);
    d.setMonth(d.getMonth() - 11);
    const startMonth = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
    return {
      start: `${startMonth}-01`,
      end: monthEnd(endMonth),
      hourStart: "00:00",
      hourEnd: "23:00",
    };
  }
  if (granularity === "hour") {
    return {
      start: last,
      end: last,
      hourStart: "00:00",
      hourEnd: "23:00",
    };
  }
  return {
    start: addDays(today, NARROW ? -6 : -29),
    end: today,
    hourStart: "00:00",
    hourEnd: "23:00",
  };
}

function presetRange(granularity, presetId, coverage, utility) {
  const today = todayIso();
  const last = lastCoveredDay(coverage, utility, today);
  const years = coverageYears(coverage, utility);
  const firstYear = years[0];
  const lastYear = years[years.length - 1];

  if (granularity === "year") {
    if (presetId === "all") {
      return { start: `${firstYear}-01-01`, end: `${lastYear}-12-31` };
    }
    if (presetId === "last_3") {
      const from = Math.max(Number(lastYear) - 2, Number(firstYear));
      return { start: `${from}-01-01`, end: `${lastYear}-12-31` };
    }
    if (presetId === "last_5") {
      const from = Math.max(Number(lastYear) - 4, Number(firstYear));
      return { start: `${from}-01-01`, end: `${lastYear}-12-31` };
    }
  }

  if (granularity === "month") {
    if (presetId === "all") {
      const first = coverage[utility]?.first_date ?? `${firstYear}-01-01`;
      return { start: `${first.slice(0, 7)}-01`, end: monthEnd(last.slice(0, 7)) };
    }
    if (presetId === "this_year") {
      return { start: `${today.slice(0, 4)}-01-01`, end: monthEnd(last.slice(0, 7)) };
    }
    if (presetId === "last_12") {
      const endMonth = last.slice(0, 7);
      const d = parseIso(`${endMonth}-01`);
      d.setMonth(d.getMonth() - 11);
      const startMonth = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
      return { start: `${startMonth}-01`, end: monthEnd(endMonth) };
    }
  }

  if (granularity === "day") {
    if (presetId === "7d") {
      return { start: addDays(last, -6), end: last };
    }
    if (presetId === "30d") {
      return { start: addDays(last, -29), end: last };
    }
    if (presetId === "this_month") {
      const m = last.slice(0, 7);
      return { start: `${m}-01`, end: monthEnd(m) };
    }
    if (presetId === "last_month") {
      const d = parseIso(`${last.slice(0, 7)}-01`);
      d.setMonth(d.getMonth() - 1);
      const m = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
      return { start: `${m}-01`, end: monthEnd(m) };
    }
  }

  if (granularity === "hour") {
    if (presetId === "last_day") {
      return { start: last, end: last };
    }
    if (presetId === "3d") {
      return { start: addDays(last, -2), end: last };
    }
    if (presetId === "7d") {
      return { start: addDays(last, -6), end: last };
    }
  }

  return null;
}

export function detectPreset(granularity, state, coverage) {
  const ids = PRESETS[granularity] ?? [];
  for (const id of ids) {
    const range = presetRange(granularity, id, coverage, state.utility);
    if (range && range.start === state.start && range.end === state.end) {
      if (granularity !== "hour") {
        return id;
      }
      if (state.hourStart === "00:00" && state.hourEnd === "23:00") {
        return id;
      }
    }
  }
  return "custom";
}

export function applyPreset(granularity, presetId, state, coverage) {
  if (presetId === "custom") {
    return false;
  }
  const range = presetRange(granularity, presetId, coverage, state.utility);
  if (!range) {
    return false;
  }
  state.start = range.start;
  state.end = range.end;
  if (granularity === "hour") {
    state.hourStart = "00:00";
    state.hourEnd = "23:00";
  }
  return true;
}

export function clampHourSpan(state) {
  const span = daysInclusive(state.start, state.end);
  if (span <= MAX_HOUR_SPAN_DAYS) {
    return;
  }
  state.start = addDays(state.end, -(MAX_HOUR_SPAN_DAYS - 1));
}

export function rebuildPresetSelect(presetEl, granularity, t) {
  if (!presetEl) {
    return;
  }
  while (presetEl.firstChild) {
    presetEl.removeChild(presetEl.firstChild);
  }
  for (const id of PRESETS[granularity] ?? []) {
    const opt = document.createElement("option");
    opt.value = id;
    opt.textContent = t[`preset.${id}`] ?? id;
    presetEl.appendChild(opt);
  }
  const custom = document.createElement("option");
  custom.value = "custom";
  custom.disabled = true;
  custom.textContent = t["preset.custom"] ?? "custom";
  presetEl.appendChild(custom);
}

function fillYearSelect(select, years, selected) {
  if (!select) {
    return;
  }
  while (select.firstChild) {
    select.removeChild(select.firstChild);
  }
  for (const y of years) {
    const opt = document.createElement("option");
    opt.value = y;
    opt.textContent = y;
    select.appendChild(opt);
  }
  select.value = selected;
}

function hourIndex(h) {
  return Number(h.slice(0, 2));
}

function fillHourSelect(select, selected) {
  if (!select || select.options.length) {
    if (select) {
      select.value = selected;
    }
    return;
  }
  for (const h of HOUR_OPTIONS) {
    const opt = document.createElement("option");
    opt.value = h;
    opt.textContent = h;
    select.appendChild(opt);
  }
  select.value = selected;
}

export function syncRangeControls(els, state, granularity, coverage) {
  const cov = coverage[state.utility];
  const minDate = cov?.first_date ?? "";
  const maxDate = cov?.last_date ?? todayIso();

  for (const group of document.querySelectorAll("[data-range-for]")) {
    group.hidden = group.dataset.rangeFor !== granularity;
  }

  if (granularity === "year") {
    const years = coverageYears(coverage, state.utility);
    fillYearSelect(els.yearStart, years, state.start.slice(0, 4));
    fillYearSelect(els.yearEnd, years, state.end.slice(0, 4));
    return;
  }

  if (granularity === "month") {
    if (els.monthStart) {
      els.monthStart.value = state.start.slice(0, 7);
      els.monthStart.min = minDate.slice(0, 7);
      els.monthStart.max = maxDate.slice(0, 7);
    }
    if (els.monthEnd) {
      els.monthEnd.value = state.end.slice(0, 7);
      els.monthEnd.min = minDate.slice(0, 7);
      els.monthEnd.max = maxDate.slice(0, 7);
    }
    return;
  }

  if (granularity === "day") {
    if (els.rangeStart) {
      els.rangeStart.value = state.start;
      els.rangeStart.min = minDate;
      els.rangeStart.max = maxDate;
    }
    if (els.rangeEnd) {
      els.rangeEnd.value = state.end;
      els.rangeEnd.min = minDate;
      els.rangeEnd.max = maxDate;
    }
    return;
  }

  if (granularity === "hour") {
    if (els.hourDayStart) {
      els.hourDayStart.value = state.start;
      els.hourDayStart.min = minDate;
      els.hourDayStart.max = maxDate;
    }
    if (els.hourDayEnd) {
      els.hourDayEnd.value = state.end;
      els.hourDayEnd.min = minDate;
      els.hourDayEnd.max = maxDate;
    }
    fillHourSelect(els.hourStart, state.hourStart);
    fillHourSelect(els.hourEnd, state.hourEnd);
  }
}

export function readRangeFromControls(els, state, granularity, coverage) {
  if (granularity === "year") {
    const y0 = els.yearStart?.value ?? state.start.slice(0, 4);
    const y1 = els.yearEnd?.value ?? state.end.slice(0, 4);
    const from = y0 <= y1 ? y0 : y1;
    const to = y0 <= y1 ? y1 : y0;
    state.start = `${from}-01-01`;
    state.end = `${to}-12-31`;
    return;
  }

  if (granularity === "month") {
    let m0 = els.monthStart?.value ?? state.start.slice(0, 7);
    let m1 = els.monthEnd?.value ?? state.end.slice(0, 7);
    if (m0 > m1) {
      [m0, m1] = [m1, m0];
    }
    state.start = `${m0}-01`;
    state.end = monthEnd(m1);
    return;
  }

  if (granularity === "day") {
    state.start = els.rangeStart?.value ?? state.start;
    state.end = els.rangeEnd?.value ?? state.end;
    if (state.start > state.end) {
      [state.start, state.end] = [state.end, state.start];
    }
    return;
  }

  if (granularity === "hour") {
    state.start = els.hourDayStart?.value ?? state.start;
    state.end = els.hourDayEnd?.value ?? state.end;
    if (state.start > state.end) {
      [state.start, state.end] = [state.end, state.start];
    }
    clampHourSpan(state);
    state.hourStart = els.hourStart?.value ?? state.hourStart;
    state.hourEnd = els.hourEnd?.value ?? state.hourEnd;
    if (hourIndex(state.hourStart) > hourIndex(state.hourEnd)) {
      [state.hourStart, state.hourEnd] = [state.hourEnd, state.hourStart];
    }
  }
}

export function onGranularityChange(state, newGranularity, coverage) {
  const defaults = defaultRangeFor(newGranularity, coverage, state.utility);
  state.granularity = newGranularity;
  state.start = defaults.start;
  state.end = defaults.end;
  state.hourStart = defaults.hourStart;
  state.hourEnd = defaults.hourEnd;
}
