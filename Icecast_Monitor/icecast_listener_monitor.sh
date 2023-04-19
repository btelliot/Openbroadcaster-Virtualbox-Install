#!/bin/bash

# Variables
ICECAST_SERVER="https://stream.openbroadcaster.com:8043"
CSV_FILE="listeners.csv"
TIMEZONE="America/Whitehorse"
LOG_FILE="listener_monitor.log"

# Function to log messages
log_message() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Create the CSV file if it doesn't exist
if [[ ! -f $CSV_FILE ]]; then
  echo "Timestamp,Listeners" > $CSV_FILE
fi

# Function to get listener count from status-json.xsl
get_listener_count() {
  JSON_RESPONSE=$(curl -s "${ICECAST_SERVER}/status-json.xsl")
  LISTENERS=$(echo "$JSON_RESPONSE" | grep -oP '(?<="listeners":)\d+')
  echo "$LISTENERS"
}

# Infinite loop to check listener count every 10 minutes
while true; do
  # Set the timezone and get the current timestamp
  TIMESTAMP=$(TZ=$TIMEZONE date '+%Y-%m-%d %H:%M:%S')
  LISTENER_COUNT=$(get_listener_count)

  if [ -z "$LISTENER_COUNT" ]; then
    log_message "Error: Listener count not found. Check the Icecast server URL."
  else
    # Append the result to the CSV file
    echo "${TIMESTAMP},${LISTENER_COUNT}" >> $CSV_FILE
    log_message "Listener count: ${LISTENER_COUNT}"
  fi

  # Wait for 10 minutes (600 seconds)
  sleep 600
done