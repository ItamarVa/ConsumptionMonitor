/**
 * Chart.js bar chart for consumption series: RTL tooltips, multi-series comparison,
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

function seriesColor(index, alpha = 0.9) {
  const raw = cssVar(`--series-${(index % 12) + 1}`);
  if (raw.startsWith("#")) {
    return hexToRgba(raw, alpha);
  }
  return raw || cssVar("--primary");
}

const numberFmt = new Intl.NumberFormat("he-IL", { maximumFractionDigits: 4 });

function formatAxisValue(value) {
  if (value == null || Number.isNaN(value)) {
    return "";
  }
  return numberFmt.format(value);
}

function barAlpha(point, granularity, estimated) {
  if (granularity === "hour" && estimated && (point?.estimated || point?.partial)) {
    return 0.65;
  }
  if (point?.partial) {
    return 0.5;
  }
  return 0.9;
}

function reducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

export function createChart(canvasEl, t) {
  const border = cssVar("--border") || "#E2E8F0";
  const textMuted = cssVar("--text-muted") || "#475569";

  let chart;
  chart = new Chart(canvasEl, {
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
              return chart?.$categories?.[idx] ?? "";
            },
            label(ctx) {
              const ds = chart?.data.datasets[ctx.datasetIndex];
              if (!ds || ds.hidden) {
                return null;
              }
              const val = ctx.parsed.y;
              if (val == null) {
                return null;
              }
              const unit = chart?.$unit ?? "";
              const point = ds.$points?.[ctx.dataIndex];
              const lines = [`${ds.label}: ${numberFmt.format(val)} ${unit}`];
              const note =
                chart?.$granularity === "hour"
                  ? point?.estimated && chart?.$t?.["chart.estimated_note"]
                  : point?.partial && chart?.$t?.["chart.partial_note"];
              if (note) {
                lines.push(note);
              }
              return lines;
            },
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: { color: textMuted, maxRotation: 0, autoSkip: true },
        },
        y: {
          beginAtZero: true,
          grid: { color: border },
          border: { display: false },
          ticks: {
            color: textMuted,
            callback(value) {
              return formatAxisValue(value);
            },
          },
        },
      },
      onClick(evt, elements) {
        if (!barClickHandler || !elements.length) {
          return;
        }
        const el = elements[0];
        const ds = chart.data.datasets[el.datasetIndex];
        const point = ds?.$points?.[el.index];
        if (point && point.value != null) {
          barClickHandler({
            seriesKey: ds.$seriesKey,
            category: chart.$categories?.[el.index],
            point,
            granularity: chart.$granularity,
          });
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
 * @param {{categories: string[], series: Array, granularity: string, unit: string, estimated: boolean, hiddenKeys: Set, t: object}} opts
 */
export function renderSeries(chart, { categories, series, granularity, unit, estimated, hiddenKeys, t }) {
  const datasets = series.map((s) => {
    const hidden = hiddenKeys?.has(s.key);
    const alpha = (p) => barAlpha(p, granularity, estimated);
    return {
      label: s.label,
      data: s.points.map((p) => p.value),
      backgroundColor: s.points.map((p) => seriesColor(s.colorIndex, alpha(p))),
      hoverBackgroundColor: seriesColor(s.colorIndex, 1),
      hidden,
      $seriesKey: s.key,
      $points: s.points,
    };
  });

  chart.data.labels = categories;
  chart.data.datasets = datasets;
  chart.$categories = categories;
  chart.$granularity = granularity;
  chart.$unit = unit;
  chart.$t = t;
  chart.update();
}

export function onBarClick(handler) {
  barClickHandler = handler;
}

/** Re-read CSS tokens after theme switch without rebuilding datasets. */
export function refreshChartTheme(chart) {
  if (!chart) {
    return;
  }
  const border = cssVar("--border") || "#E2E8F0";
  const textMuted = cssVar("--text-muted") || "#475569";
  chart.options.scales.x.ticks.color = textMuted;
  chart.options.scales.y.ticks.color = textMuted;
  chart.options.scales.y.grid.color = border;
  chart.update("none");
}

export { seriesColor };
