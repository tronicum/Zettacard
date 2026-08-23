#!/bin/bash
# Zettacard cka-l5 verify: step 5 - Pod scheduled onto a tainted node via a
# toleration, not by removing the taint. Original logic written for this
# project.
set -u

taint_present=0
for n in $(kubectl get nodes -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
  if kubectl get node "$n" -o jsonpath='{.spec.taints[*].key}' 2>/dev/null | grep -qw "tier"; then
    taint_present=1
  fi
done
if [ "$taint_present" -eq 0 ]; then
  echo "the 'tier=db:NoSchedule' taint is gone - the point of this step is to tolerate it, not remove it"
  exit 1
fi

pod=$(kubectl get pods -l app=plain -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ -z "$pod" ]; then
  echo "no Pod found for deployment 'plain' yet"
  exit 1
fi

phase=$(kubectl get pod "$pod" -o jsonpath='{.status.phase}' 2>/dev/null)
if [ "$phase" != "Running" ]; then
  echo "Pod '$pod' is not Running yet (currently: ${phase:-unknown}) - add a matching toleration"
  exit 1
fi

tol=$(kubectl get pod "$pod" -o jsonpath='{.spec.tolerations[?(@.key=="tier")].value}' 2>/dev/null)
if [ "$tol" != "db" ]; then
  echo "Pod '$pod' is Running but has no toleration for key 'tier' value 'db' - check how it got scheduled"
  exit 1
fi

echo "confirmed: taint still present, Pod scheduled via a matching toleration"
exit 0
