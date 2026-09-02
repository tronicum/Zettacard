<br>

### Roll it back

Undo the rollout and watch the *old* ReplicaSet scale back up instead of a
third one being created:

```
kubectl rollout undo deployment/web
kubectl rollout status deployment/web
```{{exec}}

Confirm which image is running now:

```
kubectl get deployment web -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
```{{exec}}

This is exactly why the old ReplicaSet was kept around at 0 replicas instead
of being deleted after the rollout — `rollout undo` has something to scale
back up.

Click **Check** once the Deployment is back on `nginx:1.25`.
