<br>

### Repair it, then reach it via NodePort

Fix the selector:

```
kubectl patch service web -p '{"spec":{"selector":{"app":"web"}}}'
```{{exec}}

Watch the endpoints come back:

```
kubectl get endpoints web
```{{exec}}

Now convert the Service to NodePort and reach it directly from the node:

```
kubectl patch svc web -p '{"spec":{"type":"NodePort"}}'
NODEPORT=$(kubectl get svc web -o jsonpath='{.spec.ports[0].nodePort}')
curl -s "http://localhost:${NODEPORT}" | head -5
```{{exec}}

Click **Check** once the Service is type `NodePort`, has endpoints again,
and answers on its node port.
