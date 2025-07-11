#!/bin/bash
set -e

docker rm -f vote-app redis-server 2>/dev/null || true
docker network rm vote-net 2>/dev/null || true

echo "Cleaned up all containers and custom network." 