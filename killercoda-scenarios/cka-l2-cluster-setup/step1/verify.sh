#!/bin/bash
# Zettacard cka-l2 verify: step 1 - control plane initialised and healthy.
# Original verification logic written for this project; not copied from any
# Killercoda/Katacoda scenario or third-party training-vendor material.
set -u
export KUBECONFIG="${KUBECONFIG:-/etc/kubernetes/admin.conf}"

command -v kubectl >/dev/null 2>&1 || { echo "kubectl not found on PATH yet"; exit 1; }

# 1. the four control-plane static-pod manifests exist on disk
for m in kube-apiserver kube-controller-manager kube-scheduler etcd; do
  if [ ! -f "/etc/kubernetes/manifests/${m}.yaml" ]; then
    echo "missing static-pod manifest: /etc/kubernetes/manifests/${m}.yaml (did kubeadm init succeed?)"
    exit 1
  fi
done

# 2. those four show up Running as Pods in kube-system
for c in kube-apiserver kube-controller-manager kube-scheduler etcd; do
  if ! kubectl get pods -n kube-system --no-headers 2>/dev/null | awk -v n="$c" '$1 ~ "^"n"-" && $3=="Running" {found=1} END{exit !found}'; then
    echo "${c} Pod is not Running in kube-system yet"
    exit 1
  fi
done

# 3. CoreDNS is up (proves the API server + scheduler + controller-manager loop is working end to end)
if ! kubectl get pods -n kube-system --no-headers 2>/dev/null | awk '$1 ~ "^coredns-" && $3=="Running" {found=1} END{exit !found}'; then
  echo "CoreDNS is not Running yet - give the control plane a bit more time"
  exit 1
fi

# 4. at least one node reached Ready - only possible once a CNI plugin is applied
if ! kubectl get nodes --no-headers 2>/dev/null | awk '$2=="Ready" {found=1} END{exit !found}'; then
  echo "no node is Ready yet - has a CNI plugin (e.g. flannel) been applied?"
  exit 1
fi

# 5. /readyz reports ok
if ! kubectl get --raw='/readyz' 2>/dev/null | grep -q "^ok$"; then
  echo "/readyz did not report ok yet"
  exit 1
fi

echo "control plane is initialised, CNI is applied, and the node is Ready"
exit 0
