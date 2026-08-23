#!/bin/bash
# Zettacard cka-l5 verify: step 3 - recovered from the broken-image rollout
# back to a fully healthy nginx:1.25 deployment. Original logic written for
# this project.
set -u

image=$(kubectl get deployment web -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null)
if [ "$image" != "nginx:1.25" ]; then
  echo "Deployment 'web' is not back on nginx:1.25 yet (currently: ${image:-unknown})"
  exit 1
fi

running=$(kubectl get pods -l app=web --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)
if [ "$running" -lt 4 ]; then
  echo "expected 4 Running Pods for app=web after recovery, found ${running}"
  exit 1
fi

bad=$(kubectl get pods -l app=web --no-headers 2>/dev/null | grep -c 'ImagePullBackOff\|ErrImagePull' || true)
if [ "${bad:-0}" -gt 0 ]; then
  echo "still seeing Pods stuck on the bad image - recovery is not finished"
  exit 1
fi

echo "recovered: 4/4 Pods Running on nginx:1.25, no broken Pods remain"
exit 0
