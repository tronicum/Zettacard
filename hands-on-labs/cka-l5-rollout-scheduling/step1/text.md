<br>

### Watch two ReplicaSets trade places

Make sure ordinary Pods can actually schedule on this single node (safe to
run even if the taint is already gone):

```
kubectl taint nodes --all node-role.kubernetes.io/control-plane- 2>/dev/null || true
```{{exec}}

Create a Deployment with four replicas:

```
kubectl create deployment web --image=nginx:1.25 --replicas=4
kubectl rollout status deployment/web
```{{exec}}

In a second terminal tab, watch Pods and ReplicaSets live:

```
kubectl get pods,replicaset -l app=web -w
```{{exec interrupt}}
(Ctrl+C to stop watching once you've seen enough — or move on and it'll keep
running in that tab.)

Back in the first tab, trigger a rolling update:

```
kubectl set image deployment/web nginx=nginx:1.27
```{{exec}}

Watch the second ReplicaSet appear and the first drain to zero — **without
ever being deleted**:

```
kubectl get replicaset -l app=web
```{{exec}}

Confirm the rollout finished and check the revision history:

```
kubectl rollout status deployment/web
kubectl rollout history deployment/web
```{{exec}}

Click **Check** once `kubectl rollout status` reports the rollout is
complete and `kubectl get replicaset` shows two ReplicaSets for `web` (one
scaled to 0, one at 4).
