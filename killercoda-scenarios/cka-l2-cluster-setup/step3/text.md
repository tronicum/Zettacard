<br>

### Bring it back and confirm recovery

Move the manifest back into place:

```
mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/kube-apiserver.yaml
```{{exec}}

The kubelet picks it up on its next sync (a few seconds) and starts the
static Pod again. Confirm `kubectl` answers:

```
kubectl get nodes
```{{exec}}

```
kubectl get --raw='/readyz?verbose'
```{{exec}}

And confirm the workload Pod you created in the previous step never actually
went anywhere — it kept serving the whole time the control plane was down:

```
kubectl get pods -l app=web
```{{exec}}

Click **Check** once `kubectl get nodes` responds normally again.

That's the lab: you initialised a control plane, verified every piece of it
independently rather than trusting the previous lesson's description, and
watched first-hand that losing the control plane does not take your
workloads down with it. Keep this cluster around — Zettacard's course
assumes weeks 2 to 4 build on a cluster you already have, and this Killercoda
environment stays available for the duration of your session.
