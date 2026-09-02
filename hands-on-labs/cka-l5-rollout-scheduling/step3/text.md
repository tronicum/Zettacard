<br>

### Break the rollout with a bad image

Now break it deliberately with an image tag that doesn't exist:

```
kubectl set image deployment/web nginx=nginx:doesnotexist
```{{exec}}

Watch it stall — this will not return on its own:

```
timeout 20 kubectl rollout status deployment/web
```{{exec}}

Check what's actually happening:

```
kubectl get pods -l app=web
```{{exec}}
You should see one Pod stuck in `ImagePullBackOff` or `ErrImagePull`.

Here's the point of the whole exercise — count your **serving** Pods:

```
kubectl get pods -l app=web --field-selector=status.phase=Running
```{{exec}}
Even with the rollout broken, most of your four Pods are still `Running` on
the *old* image, because `maxUnavailable` (25% by default) only let one Pod
go at a time. A broken rollout does not automatically mean a broken service.

Recover:

```
kubectl rollout undo deployment/web
kubectl rollout status deployment/web
```{{exec}}

Click **Check** once every Pod for `app=web` is `Running` again on
`nginx:1.25`.
