# Changelog

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
