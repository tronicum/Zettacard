#!/bin/bash
# Zettacard cka-l9 verify: step 3 - selector repaired, endpoints back, and
# the Service is reachable as a NodePort. Original logic written for this
# project.
set -u

sel=$(kubectl get service web -o jsonpath='{.spec.selector.app}' 2>/dev/null)
if [ "$sel" != "web" ]; then
  echo "Service 'web' selector is not back to app=web (currently: ${sel:-unset})"
  exit 1
fi

ep_ips=$(kubectl get endpoints web -o jsonpath='{.subsets[*].addresses[*].ip}' 2>/dev/null)
count=$(echo "$ep_ips" | wc -w)
if [ "$count" -lt 2 ]; then
  echo "Service 'web' has ${count} endpoint(s), expected 2 after repair"
  exit 1
fi

svctype=$(kubectl get service web -o jsonpath='{.spec.type}' 2>/dev/null)
if [ "$svctype" != "NodePort" ]; then
  echo "Service 'web' is type ${svctype:-unknown}, expected NodePort"
  exit 1
fi

nodeport=$(kubectl get service web -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null)
if [ -z "$nodeport" ]; then
  echo "Service 'web' has no nodePort assigned yet"
  exit 1
fi

if ! curl -sf -m 5 "http://localhost:${nodeport}" >/dev/null 2>&1; then
  echo "Service 'web' did not answer on node port ${nodeport}"
  exit 1
fi

echo "confirmed: selector repaired, 2 endpoints, reachable as NodePort ${nodeport}"
exit 0
