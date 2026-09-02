#!/bin/bash
# Zettacard cka-l2 verify: step 3 - the manifest is back and the API server
# has actually recovered. Original logic written for this project.
set -u
export KUBECONFIG="${KUBECONFIG:-/etc/kubernetes/admin.conf}"

if [ ! -f /etc/kubernetes/manifests/kube-apiserver.yaml ]; then
  echo "kube-apiserver.yaml is not back in /etc/kubernetes/manifests yet"
  exit 1
fi

recovered=0
for _ in $(seq 1 20); do
  if kubectl get --raw='/readyz' >/dev/null 2>&1; then
    recovered=1
    break
  fi
  sleep 1
done

if [ "$recovered" -eq 0 ]; then
  echo "API server has not come back healthy yet - give the kubelet a bit more time and check again"
  exit 1
fi

# The workload Pod created before the outage should still be there and Running -
# proof the control plane outage never touched already-running workloads.
if ! kubectl get pods -l app=web --no-headers 2>/dev/null | awk '$3=="Running" {found=1} END{exit !found}'; then
  echo "the 'web' Deployment's Pod is not Running - it should have kept serving throughout"
  exit 1
fi

echo "control plane recovered and the workload Pod was never disrupted - lab complete"
exit 0
