#!/bin/bash
# Docker wrapper script for Jenkins container
# This script uses the host Docker daemon

# Set Docker host to use the host's Docker daemon
export DOCKER_HOST=unix:///var/run/docker.sock

# Execute the docker command with the host Docker
exec docker "$@"
