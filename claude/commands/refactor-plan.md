---
description: Produce a refactor plan for a file or module. Plan only - no edits, no rewritten code.
---

The user has identified a piece of code that needs refactoring. Your job
is to produce a plan they can execute themselves, not to do the refactor.

## What to produce

```
## Current shape
<2-4 sentences: what the code is, what it does, why it's painful>

## Goal
<1-2 sentences: what "better" looks like for this code>

## Proposed seams
- <each seam: a place to split, an interface to extract, a state to lift,
  a function to inline, etc. One bullet each. Name files/functions.>

## Step-by-step plan
1. <smallest first step, with the test that should still pass after it>
2. <next step>
...
Each step should be independently committable and leave the build green.

## Risks and unknowns
- <what could go wrong>
- <what you'd want to verify before starting>

## Out of scope
- <what NOT to do in this refactor>
```

## Constraints

- **Do not write the refactored code.** Names and shapes only.
- Each step must be small enough to land as one commit.
- Prefer mechanical, behavior-preserving moves first; behavior changes
  later, in their own commits.
- Call out any test gaps - "before step 3, this branch has no test".
- Do not edit files.

---

Target to refactor:

$ARGUMENTS
