#!/bin/bash

# Check if input param is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <app_name>"
  exit 1
fi

APP_NAME=$1
HOST_ENTRY="192.168.1.124 ${APP_NAME}.home.lan"

# Check if the entry already exists in /etc/hosts
if grep -q "$HOST_ENTRY" /etc/hosts; then
  echo "Entry already exists: $HOST_ENTRY"
else
  echo "$HOST_ENTRY" | sudo tee -a /etc/hosts > /dev/null
  echo "Added entry: $HOST_ENTRY"
fi