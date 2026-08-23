<br>

### Break the selector on purpose, then watch the endpoints vanish

Break it in the way real clusters actually break — change the Service's
selector to a label nothing has:

```
kubectl patch service web -p '{"spec":{"selector":{"app":"web-typo"}}}'
```{{exec}}

The Service still exists, still has a ClusterIP, still resolves in DNS —
and returns nothing. Confirm each of those claims yourself:

```
kubectl get service web
```{{exec}}
Still there, still has a ClusterIP.

```
kubectl run tmp2 --rm -it --image=busybox:1.36 --restart=Never -- nslookup web.default.svc.cluster.local
```{{exec}}
Still resolves.

```
kubectl get endpoints web
```{{exec}}
**Empty.** This is the signature failure of this whole topic: a healthy DNS
name pointing at nothing. Always check endpoints first when a Service
"isn't working" — it's usually the fastest way to the answer.

Click **Check** once `kubectl get endpoints web` shows no addresses while
the Service itself still exists.
