# Dashboard frozen contract

Wave 0 contract for the four parallel Wave 1 agents. Do not change without a coordinated re-freeze.

## 1. Hourly endpoint JSON

`GET /readings/hourly?utility=electricity&direction=import&date=2026-09-09`

```json
{
  "utility": "electricity",
  "direction": "import",
  "date": "2026-09-09",
  "unit": "kWh",
  "meter_id": "30400",
  "estimated": true,
  "hours": [
    { "hour": "00:00", "value": 0.412, "source_intervals": 1, "partial": false },
    { "hour": "01:00", "value": null,  "source_intervals": 0, "partial": true }
  ]
}
```

`hours` has 23, 24 or 25 entries depending on the Israeli DST transition. `value` is `null` when no reading covers the hour at all, which is how future hours of today and gaps in history render. `partial` is true when the covered seconds in that hour are under the full hour. `estimated` is always true and the UI must surface it.

## 2. The pure function

```python
def spread_to_hours(
    readings: Sequence[Mapping[str, Any]],
    field: str,
    day: date,
    tz: ZoneInfo,
) -> list[dict]:
    """Distribute each consecutive register delta across the local hours it covers."""
```

No database access, no config import, fully unit-testable. `readings` are rows as returned by the existing `db.meter_readings`, ordered by `reading_time_utc`, and must include the last reading before local midnight so the first hour is not truncated. `field` is one of `total_import_kwh`, `total_export_kwh`, `total_water_data`.

Algorithm:

1. Build bucket boundaries in absolute time: start at local midnight of `day` converted to UTC, step `timedelta(hours=1)` until local midnight of `day + 1`. Stepping in absolute time rather than constructing local wall-clock times avoids the invalid and ambiguous times that Asia/Jerusalem produces twice a year, and naturally yields 23 or 25 buckets on those days. Label each bucket by the local hour of its start.
2. For each consecutive pair of readings, skip the pair if either register value is `None`.
3. `delta = later - earlier`. A negative delta means a meter reset or a portal correction, not consumption: skip the pair and do not count it in `source_intervals`.
4. Clamp the pair's interval to the day window, then add `delta * overlap_seconds / interval_seconds` to each overlapped bucket, and increment that bucket's `source_intervals`.
5. A bucket with `source_intervals == 0` gets `value: null`. Otherwise round to 4 decimals.
6. A zero-length interval (two readings at the same timestamp) is skipped rather than dividing by zero.

`tests/test_hourly.py` must cover: an interval spanning three hours splits proportionally and sums back to the delta; an interval entirely inside one hour lands in that hour only; no readings at all returns 24 nulls; a reading exactly on midnight is not double-counted into both days; a negative delta is skipped; the spring-forward day returns 23 buckets and the fall-back day returns 25; the total of all buckets equals the whole-day register delta within rounding tolerance.

## 3. CSS custom properties

Declared once on `:root` in `styles.css`, consumed by both C and D. Values come from the `ui-ux-pro-max` "Data-Dense Dashboard" system.

- `--bg: #F8FAFC`, `--surface: #FFFFFF`, `--border: #E2E8F0`
- `--text: #1E3A8A`, `--text-muted: #475569`
- `--primary: #1E40AF`, `--primary-hover: #3B82F6`, `--accent: #F59E0B`
- `--positive: #059669`, `--negative: #DC2626`
- `--radius: 10px`, `--shadow: 0 1px 2px rgba(15,23,42,.06), 0 4px 12px rgba(15,23,42,.04)`
- `--space-1: 4px` through `--space-6: 32px`
- `--font: "Segoe UI", "Noto Sans Hebrew", Arial, sans-serif`, `--font-num: "Consolas", "SF Mono", monospace`

Deliberate deviation from the skill's Fira Code / Fira Sans pairing: neither has Hebrew glyphs, and loading them would mean a Google Fonts request from a page that reads local meter data. A system stack keeps the page fully offline and renders Hebrew correctly on Windows. Numeric displays use `font-variant-numeric: tabular-nums` so digits stop jittering during the live refresh.

## 4. Locale keys and JS module exports

`web/locales/he.json` is a flat key-value map, the single place any Hebrew text exists in the repo. Frozen key list: `app.title`, `app.subtitle`, `utility.electricity_import`, `utility.electricity_export`, `utility.water`, `granularity.hour`, `granularity.day`, `granularity.month`, `granularity.year`, `range.from`, `range.to`, `preset.7d`, `preset.30d`, `preset.this_month`, `preset.this_year`, `preset.all`, `compare.none`, `compare.previous`, `compare.last_year`, `kpi.total`, `kpi.average`, `kpi.peak`, `kpi.latest`, `chart.estimated_note`, `chart.no_data`, `chart.error`, `chart.retry`, `chart.download_csv`, `table.toggle`, `table.period`, `table.value`, `status.live`, `status.stale`, `status.offline`, `status.updated_ago`, `unit.kwh`, `unit.m3`, `month.1` through `month.12`.

Module exports, so C's markup ids and D's queries cannot drift:

- `api.js`: `fetchLocale()`, `fetchHealth()`, `fetchSeries({utility, direction, granularity, start, end})` returning a normalized `[{label, iso, value, unit, estimated, partial}]`, and an `ApiError` class carrying `status`.
- `chart.js`: `createChart(canvasEl, t)`, `renderSeries(chart, {primary, comparison, granularity, unit, estimated, t})`, `onBarClick(handler)`.
- `app.js`: no exports; owns state, wiring and the poll timer.

DOM ids C provides and D binds to: `#utility`, `#granularity`, `#range-start`, `#range-end`, `#preset`, `#compare`, `#kpi-total`, `#kpi-average`, `#kpi-peak`, `#kpi-latest`, `#breadcrumb`, `#chart`, `#chart-note`, `#status-pill`, `#data-table`, `#table-toggle`, `#download-csv`, `#state-loading`, `#state-empty`, `#state-error`, `#retry`.
