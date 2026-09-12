/**
 * Dashboard fetch layer: locale bundle, health probe, and normalized time-series
 * from the ConsumptionMonitor read endpoints. Maps granularity to the correct
 * route and coerces every response into [{label, iso, value, unit, estimated, partial}].
 * Depends on: same-origin API at the site root (/health, /readings/*).
 * api.js lives under /ui/; import.meta.url resolves paths for any Ingress prefix.
 */

const API_ROOT = new URL("../", import.meta.url);
const url = (path) => new URL(path, API_ROOT).toString();

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function requestJson(url) {
  const res = await fetch(url);
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      if (body && body.detail) {
        detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
      }
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(detail, res.status);
  }
  return res.json();
}

export async function fetchLocale() {
  return requestJson(url("ui/locales/he.json"));
}

export async function fetchHealth() {
  return requestJson(url("health"));
}

const GRANULARITY_PATHS = {
  hour: "readings/hourly",
  day: "readings/daily",
  month: "readings/monthly",
  year: "readings/yearly",
};

function normalizeHourly(body, day) {
  const unit = body.unit ?? "";
  const estimated = body.estimated !== false;
  return (body.hours ?? []).map((row) => ({
    label: row.hour,
    iso: `${day}T${row.hour}`,
    value: row.value ?? null,
    unit,
    estimated,
    partial: Boolean(row.partial),
  }));
}

function normalizeDaily(body) {
  const unit = body.unit ?? "";
  return (body.days ?? []).map((row) => ({
    label: row.date,
    iso: row.date,
    value: row.value ?? null,
    unit: row.unit ?? unit,
    estimated: false,
    partial: Boolean(row.partial),
  }));
}

function normalizeMonthly(body) {
  const unit = body.unit ?? "";
  return (body.months ?? []).map((row) => ({
    label: row.month,
    iso: `${row.month}-01`,
    value: row.value ?? null,
    unit: row.unit ?? unit,
    estimated: false,
    partial: Boolean(row.partial),
  }));
}

function normalizeYearly(body) {
  const unit = body.unit ?? "";
  return (body.years ?? []).map((row) => ({
    label: row.year,
    iso: `${row.year}-01-01`,
    value: row.value ?? null,
    unit: row.unit ?? unit,
    estimated: false,
    partial: Boolean(row.partial),
  }));
}

function addDaysIso(iso, n) {
  const [y, m, d] = iso.split("-").map(Number);
  const dt = new Date(y, m - 1, d);
  dt.setDate(dt.getDate() + n);
  const yy = dt.getFullYear();
  const mm = String(dt.getMonth() + 1).padStart(2, "0");
  const dd = String(dt.getDate()).padStart(2, "0");
  return `${yy}-${mm}-${dd}`;
}

function daysBetween(start, end) {
  const dates = [];
  let cur = start;
  while (cur <= end) {
    dates.push(cur);
    cur = addDaysIso(cur, 1);
  }
  return dates;
}

function hourInWindow(label, hourStart, hourEnd) {
  const h = Number(label.slice(0, 2));
  const lo = Number(hourStart.slice(0, 2));
  const hi = Number(hourEnd.slice(0, 2));
  return h >= lo && h <= hi;
}

async function fetchHourlyRange({ utility, direction, start, end, hourStart, hourEnd }) {
  const days = daysBetween(start, end);
  const params = new URLSearchParams({ utility, direction });
  const chunks = await Promise.all(
    days.map(async (day) => {
      params.set("date", day);
      const body = await requestJson(`${url(GRANULARITY_PATHS.hour)}?${params}`);
      return normalizeHourly(body, day).filter((p) => hourInWindow(p.label, hourStart, hourEnd));
    }),
  );
  const points = chunks.flat();
  const unit = points[0]?.unit ?? "";
  return { points, meta: { unit, estimated: true } };
}

/**
 * @param {{utility: string, direction: string, granularity: string, start: string, end: string, hourStart?: string, hourEnd?: string}} opts
 * @returns {Promise<{points: Array, meta: {unit: string, estimated: boolean}}>}
 */
export async function fetchSeries({ utility, direction, granularity, start, end, hourStart, hourEnd }) {
  const path = GRANULARITY_PATHS[granularity];
  if (!path) {
    throw new ApiError(`unknown granularity: ${granularity}`, 0);
  }

  if (granularity === "hour") {
    return fetchHourlyRange({
      utility,
      direction,
      start,
      end,
      hourStart: hourStart ?? "00:00",
      hourEnd: hourEnd ?? "23:00",
    });
  }

  const params = new URLSearchParams({ utility, direction, start, end });
  const body = await requestJson(`${url(path)}?${params}`);

  let points;
  if (granularity === "day") {
    points = normalizeDaily(body);
  } else if (granularity === "month") {
    points = normalizeMonthly(body);
  } else {
    points = normalizeYearly(body);
  }

  const unit = body.unit ?? points[0]?.unit ?? "";
  return { points, meta: { unit, estimated: false } };
}
