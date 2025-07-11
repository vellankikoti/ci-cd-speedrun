#!/bin/bash
set -e

if ! command -v ngrok &>/dev/null; then
  echo "ngrok not found! Please install ngrok first."
  exit 1
fi

ngrok http 5000 