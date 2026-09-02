<br>

### Break it once: move the API server manifest away

Now cause an outage on purpose — this exact scenario is far easier to
diagnose in week 4 of the course if you've seen it once in calm conditions.

Deploy something small first, so you have a workload Pod to watch while the
control plane is down:

```
kubectl create deployment web --image=nginx --replicas=1
```{{exec}}

Move the API server's static-pod manifest out of the directory the kubelet
watches:

```
mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/kube-apiserver.yaml
```{{exec}}

Within seconds the kubelet notices the manifest is gone, stops the API
server's static Pod, and every `kubectl` command starts failing:

```
kubectl get nodes
```{{exec}}
You should see something like `connection refused` or a timeout.

While it's down, this is exactly the moment to practise the tools that do
**not** need the API server — the same ones week 4's troubleshooting lesson
leans on:

```
systemctl status kubelet
```{{exec}}

```
crictl ps
```{{exec}}
(containers are still running — your `web` Deployment's Pod is one of them.
The control plane manages *change*, not *traffic*: losing it does not stop
already-running Pods from serving.)

```
journalctl -u kubelet -n 50 --no-pager
```{{exec}}

Write down, in your own words, what each of those three showed while the API
server was down — that note is your week-4 cheat sheet.

When you're done reading, click **Check** — it confirms the manifest really
is gone and the API server really is unreachable right now.
