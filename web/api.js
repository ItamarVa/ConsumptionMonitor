/**
 * Dashboard fetch layer: locale bundle, health probe, and normalized time-series
 * from the ConsumptionMonitor read endpoints. Maps granularity to the correct
 * route and coerces every response into [{label, iso, value, unit, estimated, partial}].
 * Depends on: same-origin API at the site root (/health, /readings/*).
 */

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
  return requestJson("/ui/locales/he.json");
}

export async function fetchHealth() {
  return requestJson("/health");
}

const GRANULARITY_PATHS = {
  hour: "/readings/hourly",
  day: "/readings/daily",
  month: "/readings/monthly",
  year: "/readings/yearly",
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

/**
 * @param {{utility: string, direction: string, granularity: string, start: string, end: string}} opts
 * @returns {Promise<{points: Array, meta: {unit: string, estimated: boolean}}>}
 */
export async function fetchSeries({ utility, direction, granularity, start, end }) {
  const path = GRANULARITY_PATHS[granularity];
  if (!path) {
    throw new ApiError(`unknown granularity: ${granularity}`, 0);
  }

  const params = new URLSearchParams({ utility, direction });

  if (granularity === "hour") {
    params.set("date", start);
  } else {
    params.set("start", start);
    params.set("end", end);
  }

  const body = await requestJson(`${path}?${params}`);

  let points;
  if (granularity === "hour") {
    points = normalizeHourly(body, start);
  } else if (granularity === "day") {
    points = normalizeDaily(body);
  } else if (granularity === "month") {
    points = normalizeMonthly(body);
  } else {
    points = normalizeYearly(body);
  }

  const unit = body.unit ?? points[0]?.unit ?? "";
  const estimated = granularity === "hour" && body.estimated !== false;

  return { points, meta: { unit, estimated } };
}
