#!/bin/bash
set -e

if ! command -v cloudflared &>/dev/null; then
  echo "cloudflared not found! Please install cloudflared first."
  exit 1
fi

cloudflared tunnel --url http://localhost:5000 