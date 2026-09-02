<br>

### Data that survives the Pod

Create a 1Gi PVC with no `storageClassName`, so it takes the default class:

```
cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-claim
spec:
  accessModes: ["ReadWriteOnce"]
  resources:
    requests:
      storage: 1Gi
EOF
kubectl get pvc data-claim
```{{exec}}
If it sits `Pending`, `kubectl describe pvc data-claim` will name the reason
(usually no default StorageClass, or `WaitForFirstConsumer` waiting for a
Pod — the manifest below satisfies that).

Mount it in a Pod at `/data`, write a file into it:

```
cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: writer
  labels:
    app: writer
spec:
  containers:
  - name: writer
    image: busybox:1.36
    command: ["sh", "-c", "echo hello-from-first-pod > /data/proof.txt && sleep 3600"]
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data-claim
EOF
kubectl wait --for=condition=Ready pod/writer --timeout=60s
kubectl exec writer -- cat /data/proof.txt
```{{exec}}

Delete the Pod, recreate it from the same manifest, and confirm the file is
still there:

```
kubectl delete pod writer
cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: writer
  labels:
    app: writer
spec:
  containers:
  - name: writer
    image: busybox:1.36
    command: ["sh", "-c", "sleep 3600"]
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data-claim
EOF
kubectl wait --for=condition=Ready pod/writer --timeout=60s
kubectl exec writer -- cat /data/proof.txt
```{{exec}}

That's the whole point of persistent storage, and it took four minutes.
Click **Check** once the second Pod can read a file it never wrote.
