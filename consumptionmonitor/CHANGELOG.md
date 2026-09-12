# Changelog

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
