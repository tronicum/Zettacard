<br>

### Lab: stand up a cluster and break it once

This is the Killercoda counterpart to Zettacard's CKA course, lesson **cka-l2**
("Lab: stand up a cluster and break it once"). Same objective as the original
prose lesson, now with a real machine under you and each step checked for
real: you'll run `kubeadm init` on a bare Ubuntu host, verify the control
plane the way the lesson describes, then deliberately break the API server
and bring it back.

This environment is a single plain Ubuntu VM with nothing pre-installed —
that is intentional. The CKA exam is 100% hands-on, and this scenario is
built the same way: nobody has pre-built a cluster for you.

Budget about the same time the original lesson does: ~20 minutes to install
the container runtime and Kubernetes tooling and run `kubeadm init`, ~10
minutes to break and repair the API server, and the rest to actually read
what each command shows you.

**Container runtime and Kubernetes tooling** (do this first, it's not part of
the graded steps):

Install containerd:
```
apt-get update && apt-get install -y containerd
mkdir -p /etc/containerd
containerd config default | tee /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
systemctl restart containerd
```{{exec}}

Install kubeadm, kubelet, kubectl from the official Kubernetes apt repository:
```
apt-get install -y apt-transport-https ca-certificates curl gpg
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list
apt-get update && apt-get install -y kubelet kubeadm kubectl
```{{exec}}

Disable swap and load the kernel modules/sysctls kubeadm expects:
```
swapoff -a
modprobe overlay && modprobe br_netfilter
echo -e "overlay\nbr_netfilter" > /etc/modules-load.d/k8s.conf
echo -e "net.bridge.bridge-nf-call-iptables = 1\nnet.ipv4.ip_forward = 1" > /etc/sysctl.d/k8s.conf
sysctl --system
```{{exec}}

Once that's done, move to Step 1.
