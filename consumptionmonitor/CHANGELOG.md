# Changelog

## 1.0.5

- Electricity Energy dashboard: MQTT register sensors use `state_class: total_increasing`
  so manual/static cost tracking works via the recorder.
- Registers publish unavailable (`null`) when the `recent` scrape fails — never `0` or
  a stale value.
- Drop duplicate electricity external statistics; water history still imports via
  `consumptionmonitor:water`.

## 1.0.4

- Mobile dashboard: collapse date/preset/mode controls behind a "סינון וטווח"
  button so the chart is visible without scrolling.
- Two-tap drill on touch: first tap shows the tooltip, second tap on the same
  bar drills down (mouse unchanged).
- Narrow screens default to 7 days instead of 30 for day granularity.
- Taller mobile chart, compact header/KPI/legend, horizontally scrolling
  comparison legend.

## 1.0.3

- Fix CPU burn: `build_hourly_rows` uses a monotonic reading cursor and per-day
  slices instead of rescanning the full history on every hour.
- Import Energy statistics only when new readings arrive or the first full sync
  is still pending; MQTT state still publishes every tick.
- Run the HA bridge on a daemon thread with its own DB connection so scraping
  never blocks on MQTT or WebSocket work.
- MQTT: binary sensors use ON/OFF templates; timestamp sensors ignore empty
  values; scraper errors truncate to 255 characters.
- Re-publish MQTT discovery when the add-on version changes.
- Ingress iframe: `X-Frame-Options: SAMEORIGIN` and `frame-ancestors 'self'`
  instead of dropping security headers.
- `recorder/import_statistics` retries with `has_mean: false` on older HA cores.

## 1.0.2

- Ingress dashboard: redirect `/` to relative `ui/` so CSS/JS load from the `/ui` mount.
- Allow iframe embedding when `HA_BRIDGE=1` (drop `X-Frame-Options: DENY` and
  `frame-ancestors 'none'`, which blocked the HA sidebar panel).

## 1.0.1

- Fix Ingress 404: `ingress_entry` is `/` (not `/ui`, which produced `//ui`); dashboard
  served at `/` when `HA_BRIDGE=1`; path middleware collapses duplicate slashes.
- Add-on `icon.png` / `logo.png` from the dashboard favicon.

## 1.0.0

Initial Home Assistant add-on release.

- Ingress dashboard at `/ui` (Hebrew RTL, same UI as the Windows app)
- Scrapes `mycitygrid.com` on a schedule; SQLite stored under `/data`
- Adopts existing history from `/share/consumptionmonitor/consumption.sqlite` on first run
- One MQTT device with meter registers, period totals, and alert binary sensors
- External statistics (`consumptionmonitor:electricity_import`, `:electricity_export`, `:water`)
  for the Energy dashboard, with history back to 2024

### Release process

1. Tag the repo (`v1.0.0`).
2. Bump `version` in `config.yaml`.
3. Bump `APP_REF` in the Dockerfile to match the tag.
4. Add an entry to this file.

The Supervisor builds the image locally from this folder (no container registry).
