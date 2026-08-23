#!/bin/bash
# Zettacard cka-l9 verify: step 2 - Service still exists but has zero
# endpoints because its selector no longer matches any Pod. Original logic
# written for this project.
set -u

if ! kubectl get service web >/dev/null 2>&1; then
  echo "Service 'web' should still exist - only the selector should have changed"
  exit 1
fi

sel=$(kubectl get service web -o jsonpath='{.spec.selector.app}' 2>/dev/null)
if [ "$sel" == "web" ]; then
  echo "the selector still matches app=web - break it first (e.g. patch it to app=web-typo)"
  exit 1
fi

ep_ips=$(kubectl get endpoints web -o jsonpath='{.subsets[*].addresses[*].ip}' 2>/dev/null)
count=$(echo "$ep_ips" | wc -w)
if [ "$count" -ne 0 ]; then
  echo "Service 'web' still has ${count} endpoint(s) - the selector doesn't appear broken yet"
  exit 1
fi

echo "confirmed: Service 'web' exists with a broken selector and zero endpoints"
exit 0
