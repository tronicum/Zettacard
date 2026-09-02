<br>

### Unschedulable, reason 3: no node matches the label

Create a Deployment with a `nodeSelector` for a label no node currently has:

```
kubectl create deployment labeled --image=nginx
kubectl patch deployment labeled --type=json -p='[{"op":"add","path":"/spec/template/spec/nodeSelector","value":{"disktype":"ssd"}}]'
kubectl describe pod -l app=labeled | grep -A5 Events
```{{exec}}
You should see `didn't match Pod's node affinity/selector`.

Now label the node — and watch the Pod schedule within seconds, **without
any change to the Pod itself**:

```
NODE=$(kubectl get nodes -o jsonpath='{.items[0].metadata.name}')
kubectl label node "$NODE" disktype=ssd
kubectl get pods -l app=labeled -w
```{{exec interrupt}}

Click **Check** once the `labeled` Pod is `Running`.

Clean up everything from steps 4-6:

```
kubectl delete deployment fat plain labeled
NODE=$(kubectl get nodes -o jsonpath='{.items[0].metadata.name}')
kubectl taint nodes "$NODE" tier=db:NoSchedule-
kubectl label node "$NODE" disktype-
```{{exec}}

The three events you just read cover most scheduling questions you'll meet
on the exam.
