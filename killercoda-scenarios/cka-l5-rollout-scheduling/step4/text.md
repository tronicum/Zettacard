<br>

### Unschedulable, reason 1: not enough CPU

Create a Deployment, then edit it to request more CPU than any node has:

```
kubectl create deployment fat --image=nginx
kubectl patch deployment fat --type=json -p='[{"op":"add","path":"/spec/template/spec/containers/0/resources","value":{"requests":{"cpu":"100"}}}]'
```{{exec}}

Read the Pod's event — don't guess, read it:

```
kubectl describe pod -l app=fat | grep -A5 Events
```{{exec}}
You should see something like `Insufficient cpu`.

```
kubectl get pods -l app=fat
```{{exec}}
The Pod stays `Pending`. This is a message from the scheduler, not the
scheduler being slow.

Click **Check** once you can see the Pod is `Pending` with an
`Insufficient cpu` event.

(Leave this broken — you'll clean it up along with the rest at the end.)
