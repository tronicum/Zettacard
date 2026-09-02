<br>

### Lab: roll out, roll back, and make the scheduler say no

This is the Killercoda counterpart to Zettacard's CKA course, lesson
**cka-l5**. Same six exercises the original lesson describes — watch a
rolling update, roll it back, break one on purpose, then produce all three
common "Pending" reasons and fix each — now on a real single-node cluster
that's already up, with each step checked automatically instead of taking
your word for it.

Budget about the same as the original lesson: ~45 minutes of typing plus
~15 minutes of reading events. If you're short on time, the three
"unschedulable" steps (4-6) carry more exam weight than the rollout ones —
do those first if you have to choose.

This is a single-node cluster. If your node still carries the default
control-plane taint, ordinary Pods won't schedule anywhere — Step 1 checks
for that and removes it before you do anything else. Move to Step 1.
