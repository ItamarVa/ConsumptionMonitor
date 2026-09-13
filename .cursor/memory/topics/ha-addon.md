# Home Assistant add-on

## Packaging

`consumptionmonitor/` at repo root: `repository.yaml` registers the store; Supervisor builds
locally (no `image:` key). Base image `ghcr.io/home-assistant/amd64-base-debian:trixie` —
Alpine fails because `scrapling[fetchers]` needs glibc. App source in the image comes from the
`APP_REF` tarball; add-on metadata (config, icons, run.sh) comes from the repo checkout.

`icon.png` and `logo.png` (256×256) match the dashboard favicon: three ascending bars, blue
blue amber, transparent background.

## Runtime

`run.sh` sets `HA_BRIDGE=1`, `ALLOWED_CLIENT_IPS=172.30.32.2`, credentials from options,
`DB_PATH=/data/consumption.sqlite`. First start copies `/share/consumptionmonitor/consumption.sqlite`
when `/data` has no DB.

Ingress on port 8099, entry `/ui`. Dashboard uses relative URLs under any Ingress prefix.

## Home Assistant integration

- **Entities:** one MQTT device `consumptionmonitor` — registers, period totals, seven
  `binary_sensor` alert flags per meter, diagnostics. Published via Supervisor `mqtt.publish`
  (no direct broker credentials).
- **Energy dashboard:** external statistics `consumptionmonitor:electricity_import`,
  `:electricity_export`, `:water` via `recorder/import_statistics` over the Supervisor
  WebSocket. Hourly rows use proportional spread from `hourly.py`; day/month/year totals stay
  exact. Water unit `m³` in HA-facing output only.

## Windows handoff

`copy-db-to-ha.bat` copies `data/consumption.sqlite` to `\\homeassistant\share\consumptionmonitor\`.
