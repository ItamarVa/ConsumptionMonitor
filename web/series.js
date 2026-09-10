/**
 * Chart series folding for comparison mode, KPI math, and running-mode payloads.
 * Pure transforms on normalised points from api.js; no DOM or fetch. Consumed by app.js.
 */

export const MAX_SERIES = 12;

const numberFmt = new Intl.NumberFormat("he-IL", { maximumFractionDigits: 2 });

export function formatNumber(n) {
  if (n == null || Number.isNaN(n)) {
    return "—";
  }
  return numberFmt.format(n);
}

export function computeKpis(points) {
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

export function seriesTotal(points) {
  const vals = points.filter((p) => p.value != null).map((p) => p.value);
  return vals.length ? vals.reduce((a, b) => a + b, 0) : null;
}

function formatDayLabel(iso, t) {
  const [, m, d] = iso.split("-");
  return `${Number(d)}.${Number(m)}`;
}

function formatMonthSeriesLabel(isoMonth, t) {
  const [y, mo] = isoMonth.split("-");
  const name = t[`month.${Number(mo)}`] ?? mo;
  return `${name} ${y}`;
}

function formatMonthCategory(mo, t) {
  return t[`month.${mo}`] ?? String(mo);
}

function hourInWindow(label, hourStart, hourEnd) {
  const h = Number(label.slice(0, 2));
  const lo = Number(hourStart.slice(0, 2));
  const hi = Number(hourEnd.slice(0, 2));
  return h >= lo && h <= hi;
}

function buildHourCategories(hourStart, hourEnd) {
  const lo = Number(hourStart.slice(0, 2));
  const hi = Number(hourEnd.slice(0, 2));
  const cats = [];
  for (let h = lo; h <= hi; h += 1) {
    cats.push(`${String(h).padStart(2, "0")}:00`);
  }
  return cats;
}

function capSeries(entries) {
  const sorted = [...entries].sort((a, b) => a.key.localeCompare(b.key));
  const capped = sorted.length > MAX_SERIES;
  const kept = capped ? sorted.slice(-MAX_SERIES) : sorted;
  return { series: kept, capped };
}

/**
 * @returns {{ categories: string[], series: Array<{key, label, colorIndex, points, total}>, capped: boolean }}
 */
export function foldForComparison(points, granularity, t, hourStart, hourEnd) {
  if (granularity === "year") {
    const categories = points.map((p) => p.label);
    const series = points.map((p, idx) => ({
      key: p.label,
      label: p.label,
      colorIndex: idx,
      points: categories.map((cat) => (cat === p.label ? { ...p } : { label: cat, iso: p.iso, value: null })),
      total: p.value,
    }));
    const { series: kept, capped } = capSeries(series);
    return { categories, series: kept, capped };
  }

  if (granularity === "month") {
    const categories = Array.from({ length: 12 }, (_, i) => formatMonthCategory(i + 1, t));
    const byYear = new Map();
    for (const p of points) {
      const year = p.iso.slice(0, 4);
      const mo = Number(p.iso.slice(5, 7));
      if (!byYear.has(year)) {
        byYear.set(year, new Map());
      }
      byYear.get(year).set(mo, p);
    }
    const entries = [...byYear.entries()].map(([year, monthMap]) => {
      const aligned = categories.map((_, idx) => {
        const p = monthMap.get(idx + 1);
        return p ? { ...p } : { label: categories[idx], iso: `${year}-${String(idx + 1).padStart(2, "0")}-01`, value: null };
      });
      return { key: year, label: year, colorIndex: 0, points: aligned, total: seriesTotal(aligned) };
    });
    entries.forEach((e, idx) => {
      e.colorIndex = idx;
    });
    const { series, capped } = capSeries(entries);
    return { categories, series, capped };
  }

  if (granularity === "day") {
    const categories = Array.from({ length: 31 }, (_, i) => String(i + 1));
    const byMonth = new Map();
    for (const p of points) {
      const monthKey = p.iso.slice(0, 7);
      const day = Number(p.iso.slice(8, 10));
      if (!byMonth.has(monthKey)) {
        byMonth.set(monthKey, new Map());
      }
      byMonth.get(monthKey).set(day, p);
    }
    const entries = [...byMonth.entries()].map(([monthKey, dayMap]) => {
      const aligned = categories.map((_, idx) => {
        const p = dayMap.get(idx + 1);
        return p
          ? { ...p }
          : { label: String(idx + 1), iso: `${monthKey}-${String(idx + 1).padStart(2, "0")}`, value: null };
      });
      return {
        key: monthKey,
        label: formatMonthSeriesLabel(monthKey, t),
        colorIndex: 0,
        points: aligned,
        total: seriesTotal(aligned),
      };
    });
    entries.forEach((e, idx) => {
      e.colorIndex = idx;
    });
    const { series, capped } = capSeries(entries);
    return { categories, series, capped };
  }

  // hour
  const categories = buildHourCategories(hourStart, hourEnd);
  const byDay = new Map();
  for (const p of points) {
    if (!hourInWindow(p.label, hourStart, hourEnd)) {
      continue;
    }
    const day = p.iso.slice(0, 10);
    if (!byDay.has(day)) {
      byDay.set(day, new Map());
    }
    byDay.get(day).set(p.label, p);
  }
  const entries = [...byDay.entries()].map(([day, hourMap]) => {
    const aligned = categories.map((hour) => {
      const p = hourMap.get(hour);
      return p ? { ...p } : { label: hour, iso: `${day}T${hour}`, value: null, estimated: true };
    });
    return {
      key: day,
      label: formatDayLabel(day, t),
      colorIndex: 0,
      points: aligned,
      total: seriesTotal(aligned),
    };
  });
  entries.forEach((e, idx) => {
    e.colorIndex = idx;
  });
  const { series, capped } = capSeries(entries);
  return { categories, series, capped };
}

export function buildRunningChart(points, granularity, t) {
  const categories = points.map((p) => {
    if (granularity === "hour") {
      return p.label;
    }
    if (granularity === "day") {
      const [, m, d] = p.iso.split("-");
      return `${Number(d)}.${Number(m)}`;
    }
    if (granularity === "month") {
      const [y, mo] = p.iso.split("-");
      const name = t[`month.${Number(mo)}`] ?? mo;
      return `${name} ${String(y).slice(-2)}`;
    }
    return p.label;
  });
  const series = [
    {
      key: "primary",
      label: "primary",
      colorIndex: 0,
      points,
      total: seriesTotal(points),
    },
  ];
  return { categories, series, capped: false };
}

export function isEmptyChart(chartData) {
  const { series } = chartData;
  if (!series.length) {
    return true;
  }
  return series.every((s) => s.points.every((p) => p.value == null));
}

export function flatPointsForTable(chartData) {
  const rows = [];
  for (const s of chartData.series) {
    for (const p of s.points) {
      if (p.value != null) {
        rows.push({ series: s.label, ...p });
      }
    }
  }
  return rows;
}
