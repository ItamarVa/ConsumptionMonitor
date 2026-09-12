# ConsumptionMonitor

Household electricity and water consumption scraped from `www.mycitygrid.com`, stored in
SQLite, and exposed through a Hebrew dashboard, MQTT entities, and Energy dashboard
statistics.

## Prerequisites

- Home Assistant OS with Supervisor (amd64)
- MQTT integration enabled (used for entity discovery; the add-on needs no broker credentials)
- mycitygrid.com account credentials

## Install

1. Make the GitHub repository public (Settings → Change visibility).
2. In Home Assistant: **Settings → Add-ons → Add-on store** (store icon, top right).
3. **Repositories** (⋮ menu) → add `https://github.com/ItamarVa/ConsumptionMonitor` → **Save**.
4. Reload the add-on store if needed, then open **ConsumptionMonitor** → **Install**.
5. On the **Configuration** tab, fill in:
   - **mycitygrid username** and **password**
   - **Local timezone** (default `Asia/Jerusalem`)
   - **Import Energy dashboard statistics** (leave enabled unless import causes errors)
6. **Start** the add-on, enable **Show in sidebar**, and open **Consumption** from the sidebar.

Authentication is handled by Home Assistant Ingress; you do not log in again inside the panel.

## Adopt existing history (recommended)

If you already ran ConsumptionMonitor on Windows, copy the database once instead of
re-scraping from 2024:

1. Install the official **Samba share** add-on and note the `\\homeassistant\share` path.
2. Create folder `consumptionmonitor` on the share.
3. Copy your Windows `data/consumption.sqlite` to
   `\\homeassistant\share\consumptionmonitor\consumption.sqlite`
   (use `copy-db-to-ha.bat` on the PC for a guided copy with progress).
4. Start this add-on. On first run, when `/data` has no database yet, it copies the file
   from the share automatically.

## Add-on options

| Option | Purpose |
| ------ | ------- |
| `username` / `password` | mycitygrid portal credentials |
| `local_tz` | Timezone for portal date boundaries |
| `energy_statistics` | Enable hourly external statistics for the Energy dashboard |

## Entities

After the add-on starts, **Settings → Devices & services → MQTT → ConsumptionMonitor**
lists one device with:

- Register sensors (kWh import/export, water m³)
- Period totals (today, this month, year to date)
- Alert binary sensors (`has_leak`, `back_flow`, and five other flags per meter)
- Diagnostic timestamps and last scraper error

Entity IDs follow the pattern `sensor.consumptionmonitor_*` and
`binary_sensor.consumptionmonitor_*`. Confirm exact names on the device page before
pasting automations below.

## Energy dashboard

The live register entities are **not** used for Energy — that would mis-place consumption
into the hour values arrive (~2 h late). Instead, the add-on imports **external statistics**
with correct hourly attribution (proportional spread inside each reading gap; day/month/year
totals stay exact).

1. Wait for the first statistics import to finish (check the add-on log; full history is
   ~24k hours per series and may take several minutes).
2. **Settings → Dashboards → Energy → Configure**.
3. Add consumption sources:
   - **Grid consumption** → statistic `consumptionmonitor:electricity_import` (kWh)
   - **Return to grid** → statistic `consumptionmonitor:electricity_export` (kWh)
   - **Water** → statistic `consumptionmonitor:water` (m³)
4. Save. Charts should reach back to 2024 if you adopted the existing SQLite file.

To verify: **Developer tools → Statistics**, search `consumptionmonitor:`.

Disable **Import Energy dashboard statistics** in add-on configuration if import fails; the
Ingress dashboard and MQTT device continue to work.

## Automations

Replace `notify.notify` with your notification service if needed. Adjust entity IDs to match
your device page.

### Leak or back-flow alert

```yaml
alias: ConsumptionMonitor — leak or back-flow
description: Notify when any meter reports leak or back-flow
trigger:
  - platform: state
    entity_id:
      - binary_sensor.consumptionmonitor_electricity_has_leak
      - binary_sensor.consumptionmonitor_electricity_back_flow
      - binary_sensor.consumptionmonitor_water_has_leak
      - binary_sensor.consumptionmonitor_water_back_flow
    to: "on"
condition: []
action:
  - service: notify.notify
    data:
      title: Meter alert
      message: "{{ trigger.to_state.name }} turned on"
mode: single
```

### Daily electricity threshold

Change `above: 30` to your kWh limit. Uses today's grid import total from `/summary`.

```yaml
alias: ConsumptionMonitor — high daily electricity
description: Notify when today's grid import exceeds the threshold
trigger:
  - platform: numeric_state
    entity_id: sensor.consumptionmonitor_electricity_import_today
    above: 30
condition: []
action:
  - service: notify.notify
    data:
      title: High electricity use today
      message: >-
        Grid import is
        {{ states('sensor.consumptionmonitor_electricity_import_today') }} kWh
mode: single
```

## Troubleshooting

| Symptom | Check |
| ------- | ----- |
| Add-on won't start | Log tab; confirm username/password |
| Empty dashboard | Credentials; wait for first scrape job |
| No history in Energy | Share DB copied before first start; `energy_statistics` enabled |
| Panel blank outside HA | Use normal HA remote access; Ingress requires HA login |

Database path inside the container: `/data/consumption.sqlite` (persistent add-on volume).
