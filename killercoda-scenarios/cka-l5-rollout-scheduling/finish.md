<br>

### Done

You watched a rolling update replace ReplicaSets without deleting the old
one, rolled it back, broke a rollout without breaking the service, and
produced (and read the real event for) all three common reasons a Pod ends
up `Pending`: insufficient resources, an untolerated taint, and an
unmatched node selector.

Back in Zettacard: mark **Lab: roll out, roll back, and make the scheduler
say no** as complete, and carry on to week 3.
