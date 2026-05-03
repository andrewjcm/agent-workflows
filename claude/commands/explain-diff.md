---
description: Explain in plain language what the pending diff actually does, including any surprising side effects, so the user can review their own change before committing.
---

The user is about to commit. Before they do, you are going to walk them
through what the change actually does. The goal is for the user to spot
anything they did not intend.

## Inputs

If the user did not paste a diff, run:

```
git diff --staged
git diff
```

and explain whatever is pending. If both are empty, say so and stop.

## What to produce

```
## What this change does
<2-4 sentences in plain language>

## File-by-file
- path/to/file.ext
  - <bullet per meaningful change, in order>

## Behavior changes
- <user-visible or API-visible effects>

## Surprises and risks
- <anything subtle: side effects, perf, ordering, concurrency, schema>
- <anything you'd expect to see in this change but don't>

## Suggested commit message (one-line)
<imperative, <=72 chars>
```

## Constraints

- Do not edit files.
- Do not make the commit, even if asked. The user commits.
- If something in the diff looks wrong or risky, name it under
  "Surprises and risks". Don't fix it.
- If the diff is empty or trivially formatting-only, say so plainly.

---

Optional context from user:

$ARGUMENTS
