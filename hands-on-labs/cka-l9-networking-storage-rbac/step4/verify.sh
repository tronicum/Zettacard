#!/bin/bash
# Zettacard cka-l9 verify: step 4 - the PVC is Bound and the file written by
# the first Pod is still readable through the current Pod, proving the data
# survived a Pod delete/recreate cycle. Original logic written for this
# project.
set -u

phase=$(kubectl get pvc data-claim -o jsonpath='{.status.phase}' 2>/dev/null)
if [ "$phase" != "Bound" ]; then
  echo "PVC 'data-claim' is not Bound yet (currently: ${phase:-not found}) - check for a default StorageClass"
  exit 1
fi

if ! kubectl get pod writer >/dev/null 2>&1; then
  echo "Pod 'writer' not found - recreate it from the same manifest after deleting the first one"
  exit 1
fi

content=$(kubectl exec writer -- cat /data/proof.txt 2>/dev/null)
if [ "$content" != "hello-from-first-pod" ]; then
  echo "expected /data/proof.txt to still read 'hello-from-first-pod', got: '${content:-<empty or missing>}'"
  exit 1
fi

echo "confirmed: PVC is Bound and the file survived the Pod being deleted and recreated"
exit 0
