#!/bin/bash
# Zettacard cka-l5 verify: step 6 - Pod scheduled after a matching node label
# was added, with no change to the Pod itself. Original logic written for
# this project.
set -u

pod=$(kubectl get pods -l app=labeled -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ -z "$pod" ]; then
  echo "no Pod found for deployment 'labeled' yet"
  exit 1
fi

selector=$(kubectl get pod "$pod" -o jsonpath='{.spec.nodeSelector.disktype}' 2>/dev/null)
if [ "$selector" != "ssd" ]; then
  echo "Pod '$pod' does not have nodeSelector disktype=ssd - that's the point of this step"
  exit 1
fi

phase=$(kubectl get pod "$pod" -o jsonpath='{.status.phase}' 2>/dev/null)
if [ "$phase" != "Running" ]; then
  echo "Pod '$pod' is not Running yet (currently: ${phase:-unknown}) - label a node disktype=ssd"
  exit 1
fi

node=$(kubectl get pod "$pod" -o jsonpath='{.spec.nodeName}' 2>/dev/null)
label=$(kubectl get node "$node" -o jsonpath='{.metadata.labels.disktype}' 2>/dev/null)
if [ "$label" != "ssd" ]; then
  echo "the node the Pod landed on does not carry disktype=ssd - something's off"
  exit 1
fi

echo "confirmed: Pod scheduled purely because the node gained the matching label"
exit 0
