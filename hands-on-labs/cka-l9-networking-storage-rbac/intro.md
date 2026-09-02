<br>

### Lab: expose it, store it, lock it down

This is the Killercoda counterpart to Zettacard's CKA course, lesson
**cka-l9**. Same three exercises the original lesson describes — break a
Service selector and watch endpoints disappear, prove persistent storage
actually survives a Pod, and verify least-privilege RBAC in both directions
— now on a real single-node cluster, with each step checked automatically.

Budget about the same as the original lesson: roughly 75 minutes across all
three exercises. If your node still carries the default control-plane
taint, run this first so Pods can actually schedule:

```
kubectl taint nodes --all node-role.kubernetes.io/control-plane- 2>/dev/null || true
```{{exec}}

This cluster needs a default `StorageClass` for the persistence exercise in
Step 4. Most Killercoda Kubernetes images ship one; check now and install a
minimal local one if not:

```
kubectl get storageclass
```{{exec}}
If that returned nothing, install a simple local-path provisioner:
```
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
kubectl patch storageclass local-path -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```{{exec}}

Move to Step 1.
