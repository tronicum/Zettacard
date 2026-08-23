<br>

### Unschedulable, reason 2: an untolerated taint

Find your node's name and taint it:

```
NODE=$(kubectl get nodes -o jsonpath='{.items[0].metadata.name}')
kubectl taint nodes "$NODE" tier=db:NoSchedule
```{{exec}}

Deploy something plain and read the event:

```
kubectl create deployment plain --image=nginx
kubectl describe pod -l app=plain | grep -A5 Events
```{{exec}}
You should see `untolerated taint`.

Now add the matching toleration and watch it schedule, without touching the
taint:

```
kubectl patch deployment plain --type=json -p='[{"op":"add","path":"/spec/template/spec/tolerations","value":[{"key":"tier","operator":"Equal","value":"db","effect":"NoSchedule"}]}]'
kubectl get pods -l app=plain -w
```{{exec interrupt}}

Click **Check** once the `plain` Pod is `Running` while the taint is still
present on the node.
