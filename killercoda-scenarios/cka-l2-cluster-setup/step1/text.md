<br>

### kubeadm init, then verify what you just read

Initialize the control plane. Because this VM has only one node, we'll skip
the pod-network CIDR question that a two-node lab would face and pass the
same flag anyway — it costs nothing and matches what the CKA exam expects
you to type:

```
kubeadm init --pod-network-cidr=10.244.0.0/16
```{{exec}}

Copy the admin kubeconfig so `kubectl` works without `sudo`:

```
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
export KUBECONFIG=$HOME/.kube/config
```{{exec}}

Apply a CNI plugin — without one, the node stays `NotReady` forever, which is
expected, not broken:

```
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
```{{exec}}

Since this is a single-node cluster, remove the control-plane taint so
ordinary Pods can actually be scheduled here later in the course:

```
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
```{{exec}}

Now **verify the lesson instead of trusting it**. Don't just skim these —
each answers a specific question about what `kubeadm init` actually did:

```
kubectl get pods -n kube-system
```{{exec}}
Look for `kube-apiserver`, `etcd`, `kube-scheduler`, `kube-controller-manager`,
plus `kube-proxy` and CoreDNS.

```
ls /etc/kubernetes/manifests
```{{exec}}
These four files are what produced the first four Pods above — the kubelet
started them directly from disk, before the API server it depends on even
existed.

```
kubectl get --raw='/readyz?verbose'
```{{exec}}
This is the current way to check control-plane health.
`kubectl get componentstatuses` still prints on many clusters but is
deprecated — don't build the habit.

```
kubectl get nodes -w
```{{exec interrupt}}
Watch the node flip from `NotReady` to `Ready` once the CNI plugin's Pods
come up (Ctrl+C once it does, or let the click-to-run send it for you).

When `kubectl get nodes` shows your node `Ready` and all `kube-system` Pods
are `Running`, click **Check**.
