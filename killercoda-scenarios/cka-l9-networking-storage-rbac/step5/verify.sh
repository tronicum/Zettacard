#!/bin/bash
# Zettacard cka-l9 verify: step 5 - the 'reader' ServiceAccount can list pods
# but cannot delete pvcs, checked in both directions rather than assuming
# the Role/RoleBinding was written correctly. Original logic written for
# this project.
set -u

if ! kubectl get serviceaccount reader -n default >/dev/null 2>&1; then
  echo "ServiceAccount 'reader' not found in namespace default"
  exit 1
fi

can_list=$(kubectl auth can-i list pods --as=system:serviceaccount:default:reader -n default 2>/dev/null)
if [ "$can_list" != "yes" ]; then
  echo "expected 'yes' for 'can-i list pods' as reader, got: '${can_list}'"
  exit 1
fi

can_delete_pvc=$(kubectl auth can-i delete pvc --as=system:serviceaccount:default:reader -n default 2>/dev/null)
if [ "$can_delete_pvc" != "no" ]; then
  echo "expected 'no' for 'can-i delete pvc' as reader, got: '${can_delete_pvc}' - the Role is granting too much"
  exit 1
fi

echo "confirmed: reader can list pods but cannot delete pvcs - least privilege verified in both directions"
exit 0
