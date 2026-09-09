/**
 * Chart.js bar chart for consumption series: RTL tooltips, comparison overlay,
 * estimated-hour alpha, and drill-down click forwarding. Expects Chart global
 * from vendor/chart.umd.min.js. Depends on: CSS custom properties on :root.
 */

let barClickHandler = null;

function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function hexToRgba(hex, alpha) {
  const h = hex.replace("#", "");
  const full = h.length === 3 ? h.split("").map((c) => c + c).join("") : h;
  const n = Number.parseInt(full, 16);
  const r = (n >> 16) & 255;
  const g = (n >> 8) & 255;
  const b = n & 255;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function colorVar(name, alpha) {
  const raw = cssVar(name);
  if (raw.startsWith("#")) {
    return hexToRgba(raw, alpha);
  }
  return raw;
}

const numberFmt = new Intl.NumberFormat("he-IL", { maximumFractionDigits: 4 });

function formatAxisValue(value, unit) {
  if (value == null || Number.isNaN(value)) {
    return "";
  }
  return unit ? `${numberFmt.format(value)} ${unit}` : numberFmt.format(value);
}

function formatCategoryLabel(point, granularity, t) {
  if (!point) {
    return "";
  }
  if (granularity === "hour") {
    return point.label;
  }
  if (granularity === "day") {
    const [, m, d] = point.iso.split("-");
    return `${Number(d)}.${Number(m)}`;
  }
  if (granularity === "month") {
    const [y, mo] = point.iso.split("-");
    const monthKey = `month.${Number(mo)}`;
    const name = t[monthKey] ?? mo;
    return `${name} ${String(y).slice(-2)}`;
  }
  return point.label;
}

function barColors(points, granularity, estimated, baseAlpha) {
  const primary = colorVar("--primary", baseAlpha);
  const hover = cssVar("--primary-hover") || colorVar("--primary", 1);
  return points.map((p) => {
    const alpha =
      granularity === "hour" && estimated && (p.estimated || p.partial) ? 0.65 : baseAlpha;
    return {
      backgroundColor: colorVar("--primary", alpha),
      hoverBackgroundColor: hover,
    };
  });
}

function reducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

export function createChart(canvasEl, t) {
  const border = colorVar("--border", 1);
  const textMuted = cssVar("--text-muted") || "#475569";

  const chart = new Chart(canvasEl, {
    type: "bar",
    data: { labels: [], datasets: [] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: reducedMotion() ? false : { duration: 200, easing: "easeOutQuart" },
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          rtl: true,
          textDirection: "rtl",
          callbacks: {
            title(items) {
              const idx = items[0]?.dataIndex ?? 0;
              const labels = chart.$seriesLabels ?? [];
              return labels[idx] ?? "";
            },
            label(ctx) {
              const val = ctx.parsed.y;
              const unit = chart.$unit ?? "";
              const lines = [`${numberFmt.format(val)} ${unit}`];
              const point = chart.$primaryPoints?.[ctx.dataIndex];
              if (point && (point.estimated || point.partial)) {
                lines.push(t["chart.estimated_note"] ?? "");
              }
              return lines;
            },
          },
        },
      },
      scales: {
        x: {
          grid: { display: false, drawBorder: false },
          ticks: { color: textMuted, maxRotation: 0, autoSkip: true },
        },
        y: {
          beginAtZero: true,
          grid: { color: border, drawBorder: false },
          ticks: {
            color: textMuted,
            callback(value) {
              return formatAxisValue(value, chart.$unit ?? "");
            },
          },
        },
      },
      onClick(evt, elements) {
        if (!barClickHandler || !elements.length) {
          return;
        }
        const el = elements.find((e) => e.datasetIndex === 0) ?? elements[0];
        const idx = el.index;
        const point = chart.$primaryPoints?.[idx];
        if (point) {
          barClickHandler({ index: idx, point, granularity: chart.$granularity });
        }
      },
      datasets: {
        bar: {
          maxBarThickness: 48,
          categoryPercentage: 0.8,
          barPercentage: 0.9,
          borderRadius: { topLeft: 4, topRight: 4, bottomLeft: 0, bottomRight: 0 },
        },
      },
    },
  });

  chart.$t = t;
  return chart;
}

/**
 * @param {import('chart.js').Chart} chart
 * @param {{primary: Array, comparison: Array|null, granularity: string, unit: string, estimated: boolean, t: object}} opts
 */
export function renderSeries(chart, { primary, comparison, granularity, unit, estimated, t }) {
  const labels = primary.map((p) => formatCategoryLabel(p, granularity, t));
  const primaryColors = barColors(primary, granularity, estimated, 0.9);

  const datasets = [
    {
      label: "primary",
      data: primary.map((p) => p.value),
      backgroundColor: primaryColors.map((c) => c.backgroundColor),
      hoverBackgroundColor: primaryColors.map((c) => c.hoverBackgroundColor),
    },
  ];

  if (comparison && comparison.length) {
    const compLen = Math.max(primary.length, comparison.length);
    const compData = [];
    for (let i = 0; i < compLen; i += 1) {
      compData.push(comparison[i]?.value ?? null);
    }
    datasets.push({
      label: "comparison",
      data: compData.slice(0, primary.length),
      backgroundColor: colorVar("--accent", 0.75),
      hoverBackgroundColor: colorVar("--accent", 0.9),
    });
  }

  chart.data.labels = labels;
  chart.data.datasets = datasets;
  chart.$primaryPoints = primary;
  chart.$seriesLabels = labels;
  chart.$granularity = granularity;
  chart.$unit = unit;
  chart.$t = t;
  chart.update();
}

export function onBarClick(handler) {
  barClickHandler = handler;
}
