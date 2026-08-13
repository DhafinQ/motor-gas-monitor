#!/bin/sh

set -eu

echo "======================================"
echo "Starting Node-RED"
echo "======================================"

echo "InfluxDB URL    : ${INFLUX_URL:-NOT_SET}"
echo "InfluxDB ORG    : ${INFLUX_ORG:-NOT_SET}"
echo "InfluxDB BUCKET : ${INFLUX_BUCKET:-NOT_SET}"

if [ -n "${INFLUX_TOKEN:-}" ]; then
    echo "InfluxDB TOKEN  : PRESENT"
else
    echo "InfluxDB TOKEN  : MISSING"
fi

exec npm start -- --userDir /data