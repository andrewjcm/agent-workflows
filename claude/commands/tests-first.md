---
description: Design test cases (names, inputs, expected outputs) for a change before any implementation. Stop after the case list.
---

You are operating under the `tdd-coach` skill, **phase 1 only**.

## What to produce

A numbered list of test cases for the change the user is about to make.
Group under three headings:

1. **Happy path** - obvious successful uses.
2. **Edge cases** - empty, max, min, unicode, boundary, off-by-one,
   concurrent.
3. **Failure modes** - bad inputs, broken dependencies, timeouts.

For each case, include:

- **Name** - short, behavior-focused (e.g. `rejects_codes_longer_than_16_chars`).
- **Inputs** - smallest concrete inputs that exercise the case.
- **Expected outcome** - return value, side effect, or raised error.
- **Why it matters** - one short phrase.

End with exactly this question, on its own line:

> Which of these would you skip, and which are missing?

Then stop.

## Constraints

- **Do not write the test code.** Names and shapes only.
- **Do not write the implementation.**
- Use the test framework already present in the repo. If there isn't
  one, say "I'll assume <framework> based on <signal>; tell me to switch
  if that's wrong" before listing cases.
- Do not edit files.

---

Change to be tested:

$ARGUMENTS
