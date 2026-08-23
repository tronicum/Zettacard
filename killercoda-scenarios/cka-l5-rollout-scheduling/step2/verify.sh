#!/bin/bash
# Zettacard cka-l5 verify: step 2 - rollback landed back on nginx:1.25.
# Original logic written for this project.
set -u

image=$(kubectl get deployment web -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null)
if [ "$image" != "nginx:1.25" ]; then
  echo "Deployment 'web' is not back on nginx:1.25 yet (currently: ${image:-unknown})"
  exit 1
fi

available=$(kubectl get deployment web -o jsonpath='{.status.availableReplicas}' 2>/dev/null)
if [ "${available:-0}" -lt 4 ]; then
  echo "Deployment 'web' does not have 4 available replicas yet after rollback (currently: ${available:-0})"
  exit 1
fi

echo "rollback confirmed: deployment/web is back on nginx:1.25 with 4 available replicas"
exit 0
