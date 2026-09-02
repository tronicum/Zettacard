<br>

### A ServiceAccount that cannot delete what it can read

Create a ServiceAccount with narrow, explicit permissions:

```
kubectl create serviceaccount reader -n default
kubectl create role pod-reader --verb=get,list,watch --resource=pods -n default
kubectl create rolebinding reader-binding --role=pod-reader --serviceaccount=default:reader -n default
```{{exec}}

Test **both** directions — least privilege is a thing you verify, not a
thing you intend:

```
kubectl auth can-i list pods --as=system:serviceaccount:default:reader
```{{exec}}
Must answer `yes`.

```
kubectl auth can-i delete pvc --as=system:serviceaccount:default:reader
```{{exec}}
Must answer `no`. This ServiceAccount can read the Pods you created earlier
in this lab, but it cannot touch the PVC that backs them — read access does
not imply write or delete access, and RBAC is additive-only: there's no
`deny` rule here, just the absence of a `grant`.

Click **Check** once both answers come back the way they should.
