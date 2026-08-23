#!/bin/bash
# Zettacard cka-l9 verify: step 1 - Service exists and has real endpoints.
# Original logic written for this project.
set -u

if ! kubectl get service web >/dev/null 2>&1; then
  echo "Service 'web' not found yet"
  exit 1
fi

ep_ips=$(kubectl get endpoints web -o jsonpath='{.subsets[*].addresses[*].ip}' 2>/dev/null)
count=$(echo "$ep_ips" | wc -w)
if [ "$count" -lt 2 ]; then
  echo "Service 'web' has ${count} endpoint(s), expected 2 - are both Pods Running and matched by the selector?"
  exit 1
fi

echo "Service 'web' has 2 endpoints and is routing to real Pods"
exit 0
