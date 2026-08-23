#!/bin/bash
# Zettacard cka-l5 verify: step 1 - rolling update completed, old ReplicaSet
# kept at 0 rather than deleted. Original logic written for this project.
set -u

if ! kubectl get deployment web >/dev/null 2>&1; then
  echo "Deployment 'web' not found yet"
  exit 1
fi

image=$(kubectl get deployment web -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null)
if [ "$image" != "nginx:1.27" ]; then
  echo "Deployment 'web' is not yet running nginx:1.27 (currently: ${image:-unknown})"
  exit 1
fi

available=$(kubectl get deployment web -o jsonpath='{.status.availableReplicas}' 2>/dev/null)
if [ "${available:-0}" -lt 4 ]; then
  echo "Deployment 'web' does not have 4 available replicas yet (currently: ${available:-0})"
  exit 1
fi

rs_count=$(kubectl get replicaset -l app=web --no-headers 2>/dev/null | wc -l)
if [ "$rs_count" -lt 2 ]; then
  echo "expected two ReplicaSets for app=web (old kept at 0, new scaled up) - found ${rs_count}"
  exit 1
fi

echo "rolling update to nginx:1.27 completed, old ReplicaSet preserved at 0 replicas"
exit 0
