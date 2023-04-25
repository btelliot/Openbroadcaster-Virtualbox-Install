#!/bin/bash

# Variables
ICECAST_SERVER="https://stream.openbroadcaster.com:8043"
#CSV_FILE="/var/www/observer/listeners.csv"
CSV_FILE="/home/ob/www/listeners.csv"
TIMEZONE="America/Whitehorse"
INTERVAL_SECONDS=600

# Create the CSV file if it doesn't exist
if [[ ! -f $CSV_FILE ]]; then
  echo "Timestamp,Listeners,ListenerPeak" > $CSV_FILE
fi


# Infinite loop to check listener count every 10 minutes
while true; do
  # Set the timezone and get the current timestamp
  TIMESTAMP=$(TZ=$TIMEZONE date '+%Y-%m-%d %H:%M:%S')

  JSON_DATA=$(curl -s "${ICECAST_SERVER}/status-json.xsl")
  LISTENERS=$(echo "${JSON_DATA}" | jq '.icestats.source.listeners')
  LISTENER_PEAK=$(echo "${JSON_DATA}" | jq '.icestats.source.listener_peak')
  
  echo "$TIMESTAMP,$LISTENERS,$LISTENER_PEAK" >> $CSV_FILE

  sleep $INTERVAL_SECONDS
done