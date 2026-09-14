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

Ingress on port 8099, entry `/` (not `/ui` — that produced `//ui` and 404). When
`HA_BRIDGE=1`, `/` redirects to relative `ui/`; assets mount at `/ui`. Dashboard uses
relative URLs under any Ingress prefix. Security headers: `X-Frame-Options: SAMEORIGIN`,
`frame-ancestors 'self'`.

## Home Assistant integration

- **Entities:** one MQTT device `consumptionmonitor` — registers, period totals, seven
  `binary_sensor` alert flags per meter (ON/OFF templates), diagnostics. Published via
  Supervisor `mqtt.publish` (no direct broker credentials). Discovery re-publishes when
  add-on version changes (`ha_mqtt_discovery_sent` stores version string).
- **Energy dashboard:** electricity register MQTT sensors (`state_class: total_increasing`,
  recorder statistics for cost tracking). Water only: external statistic
  `consumptionmonitor:water` via `recorder/import_statistics` over the Supervisor
  WebSocket. Hourly rows use proportional spread from `hourly.py` with monotonic cursor;
  import runs only on new data or pending first full sync. Bridge sync is a daemon thread
  with its own DB connection. `mean_type` retries with `has_mean: false` on older cores.
  Water unit `m³` in HA-facing output only.

## Windows handoff

`copy-db-to-ha.bat` copies `data/consumption.sqlite` to `\\homeassistant\share\consumptionmonitor\`.
