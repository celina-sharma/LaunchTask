#!/bin/bash

URL="http://localhost:3000/ping"
LOG_FILE="/home/celinasharma/Desktop/LaunchPad1/Week1/Day5/logs/health.log"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")

if [ "$STATUS" -ne 200 ]; then
    echo "$(date): Server DOWN (Status $STATUS)" >> "$LOG_FILE"
fi

