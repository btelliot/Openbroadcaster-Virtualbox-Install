#!/bin/bash

ICECAST_SERVER="https://stream.openbroadcaster.com:8043"
OUTPUT_FILE="/var/www/observer/listeners.csv"
INTERVAL_SECONDS=600

# Write CSV header
if [ ! -f "$OUTPUT_FILE"]; then
	echo "Timestamp,Listeners,ListenerPeak" > $OUTPUT_FILE
fi

while true; do
  TIMESTAMP=$(TZ='America/Whitehorse' date +"%Y-%m-%dT%H:%M:%S%z")
  
  JSON_DATA=$(curl -s "${ICECAST_SERVER}/status-json.xsl")
  LISTENERS=$(echo "$JSON_DATA" | grep -oP '"listeners":\K\d+')
  LISTENER_PEAK=$(echo "$JSON_DATA" | grep -oP '"listener_peak":\K\d+')
  
  echo "$TIMESTAMP,$LISTENERS,$LISTENER_PEAK" >> $OUTPUT_FILE
  
  sleep $INTERVAL_SECONDS
done