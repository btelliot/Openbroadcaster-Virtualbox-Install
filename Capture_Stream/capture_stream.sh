#!/bin/bash
#written by Brett Elliot - be.elliot@gmail.com, 867-335-7032

# Set the desired directory to save the recordings
BASE_SAVE_DIR="/media/obmedia/00_live_capture"

# Set the Icecast stream source URL
ICECAST_SOURCE="http://192.168.213.10:8000/cjuc"
#SDP_FILE="/home/obsuser/livewire.sdp"


while true; do
  # Get the current date and time (formatted as: YYYY-MM-DD-24HH)
  FILENAME_DATE=$(TZ='America/Whitehorse' date "+%Y-%m-%d-%H%M%S")

  # Create the output subdirectories for year, month, and day
  SAVE_DIR="${BASE_SAVE_DIR}/$(TZ='America/Whitehorse' date "+%Y")/$(TZ='America/Whitehorse' date "+%m")/$(TZ='America/Whitehorse' date "+%d")_$(TZ='America/Whitehorse' date "+%A")"
  mkdir -p "${SAVE_DIR}"

  # Create the output file path
  OUTPUT_FILE="${SAVE_DIR}/${FILENAME_DATE}.mp3"

  # Calculate the remaining seconds until the next full hour
  SECONDS_TO_NEXT_HOUR=$(( 3600 - (10#$(date "+%M") * 60) - 10#$(date "+%S") ))

  # Record the Icecast stream using FFmpeg
  #ffmpeg -protocol_whitelist file,udp,rtp -i "${SDP_FILE}" -acodec libmp3lame -ab 256k -t "${DURATION}" -vn -y "${OUTPUT_FILE}"
  ffmpeg -i "${ICECAST_SOURCE}" -acodec libmp3lame -ab 256k -t "${SECONDS_TO_NEXT_HOUR}" -vn -y "${OUTPUT_FILE}"

  # Delete folders older than a year to prevent the service from clogging the NAS
  #find "${BASE_SAVE_DIR}" -type d -mtime +365 -exec rm -rf {} +

  # Sleep for a short period to prevent overlapping recordings
  sleep 1
done