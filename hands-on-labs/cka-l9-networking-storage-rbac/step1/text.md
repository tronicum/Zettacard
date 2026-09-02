<br>

### Expose a Deployment and verify it from inside the cluster

```
kubectl create deployment web --image=nginx --replicas=2
kubectl expose deployment web --port=80 --target-port=80
```{{exec}}

Verify it works from inside the cluster with a throwaway Pod:

```
kubectl run tmp --rm -it --image=busybox:1.36 --restart=Never -- wget -qO- web.default.svc.cluster.local
```{{exec}}
You should see nginx's default HTML page.

Click **Check** once the Service exists with two matching endpoints.
