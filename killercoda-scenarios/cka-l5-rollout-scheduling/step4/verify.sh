#!/bin/bash
# Zettacard cka-l5 verify: step 4 - a Pod is Pending specifically because of
# insufficient CPU, confirmed via the scheduler's own event, not guessed.
# Original logic written for this project.
set -u

pod=$(kubectl get pods -l app=fat -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ -z "$pod" ]; then
  echo "no Pod found for deployment 'fat' yet"
  exit 1
fi

phase=$(kubectl get pod "$pod" -o jsonpath='{.status.phase}' 2>/dev/null)
if [ "$phase" != "Pending" ]; then
  echo "Pod '$pod' is not Pending (currently: ${phase:-unknown})"
  exit 1
fi

if ! kubectl describe pod "$pod" 2>/dev/null | grep -qi "Insufficient cpu"; then
  echo "Pod '$pod' is Pending but no 'Insufficient cpu' event was found - did the CPU request actually get patched in?"
  exit 1
fi

echo "confirmed: 'fat' Pod is Pending with an Insufficient cpu scheduler event"
exit 0
