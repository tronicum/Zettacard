#!/bin/bash
# Zettacard cka-l2 verify: step 2 - the API server manifest was really moved
# away and the control plane really is down right now. Original logic
# written for this project.
set -u
export KUBECONFIG="${KUBECONFIG:-/etc/kubernetes/admin.conf}"

if [ -f /etc/kubernetes/manifests/kube-apiserver.yaml ]; then
  echo "kube-apiserver.yaml is still in /etc/kubernetes/manifests - move it out (e.g. to /tmp) first"
  exit 1
fi

# The kubelet needs a moment to notice the manifest disappeared and stop the
# static Pod; give it a short grace window rather than failing instantly.
still_up=1
for _ in $(seq 1 10); do
  if ! timeout 2 kubectl get nodes >/dev/null 2>&1; then
    still_up=0
    break
  fi
  sleep 1
done

if [ "$still_up" -eq 1 ]; then
  echo "kubectl still succeeds - the API server Pod does not appear to have stopped yet. Give it a few more seconds and check again."
  exit 1
fi

echo "confirmed: the manifest is gone and the API server is unreachable, as expected"
exit 0
