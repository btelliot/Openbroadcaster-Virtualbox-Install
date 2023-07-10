#!/bin/bash

ICECAST_SERVER="http://stream.openbroadcaster.com:8043"
OUTPUT_FILE="/home/ob/www/listeners2.csv"
INTERVAL_SECONDS=600

# Write CSV header
echo "Timestamp,Listeners,ListenerPeak" > $OUTPUT_FILE

while true; do
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  
  JSON_DATA=$(curl -s "${ICECAST_SERVER}/status-json.xsl")
  LISTENERS=$(echo "$JSON_DATA" | grep -oP '"listeners":\K\d+')
  LISTENER_PEAK=$(echo "$JSON_DATA" | grep -oP '"listener_peak":\K\d+')
  
  echo "$TIMESTAMP,$LISTENERS,$LISTENER_PEAK" >> $OUTPUT_FILE
  
  sleep $INTERVAL_SECONDS
done
