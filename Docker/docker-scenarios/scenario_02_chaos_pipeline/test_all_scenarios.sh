#!/bin/bash
set -e

SCENARIOS=(step1_fail_network step2_fail_resource step3_fail_service step4_fail_db step5_success)
SCENARIO_PATH="scenarios"

for step in "${SCENARIOS[@]}"; do
  echo "\n=== Testing $step ==="
  docker build -t chaos-$step $SCENARIO_PATH/$step
  if [[ "$step" == "step2_fail_resource" ]]; then
    docker run --rm --memory=64m --memory-swap=64m chaos-$step
  else
    docker run --rm chaos-$step
  fi
done
