#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant add-on entrypoint for ConsumptionMonitor.
# Reads add-on options via bashio, adopts an existing SQLite from the Samba share
# on first run, then execs the Python API (Ingress on 8099, HA bridge enabled).
# ==============================================================================

bashio::log.info "Starting ConsumptionMonitor $(bashio::addon.version)..."

DB="/data/consumption.sqlite"
SHARE_DB="/share/consumptionmonitor/consumption.sqlite"

if [[ ! -f "${DB}" && -f "${SHARE_DB}" ]]; then
    bashio::log.info "Adopting existing database from ${SHARE_DB}"
    cp "${SHARE_DB}" "${DB}"
fi

export HOST="0.0.0.0"
export PORT="8099"
export DB_PATH="${DB}"
export ALLOWED_HOSTS="*"
export ALLOWED_CLIENT_IPS="172.30.32.2"
export LOCAL_TZ="$(bashio::config 'local_tz')"
export MYCITYGRID_USERNAME="$(bashio::config 'username')"
export MYCITYGRID_PASSWORD="$(bashio::config 'password')"
export HA_BRIDGE="1"
export ADDON_VERSION="$(bashio::addon.version)"

if bashio::config.true 'energy_statistics'; then
    export ENERGY_STATISTICS="1"
else
    export ENERGY_STATISTICS="0"
fi

cd /app || bashio::exit.nok "Application directory /app missing"
exec /app/.venv/bin/python -m consumption
