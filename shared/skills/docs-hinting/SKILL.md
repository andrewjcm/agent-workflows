---
name: docs-hinting
description: Answer "how do I" questions by pointing at official documentation. Provide one link, the exact section or keyword to look for, and one reasoning question. Do not paste the answer from the docs verbatim.
---

# docs-hinting

The user is asking a "how do I" or "what does this do" question. Instead
of summarizing the answer, you are going to teach them to find it.

## Source priority

Always prefer, in order:

1. **The language reference** (e.g. cppreference, MDN for the platform
   APIs, Python docs, Go pkg.go.dev, Rust std/reference, the JLS, the C
   standard).
2. **The framework's official docs** (e.g. React, Django, Rails, Spring,
   Next.js, Astro).
3. **The vendor's official docs** (e.g. AWS, GCP, Stripe, Postgres,
   Redis, Anthropic, OpenAI).
4. **Official RFCs / specs** (RFC, W3C, ECMA, ISO).
5. **Repo README or `/docs` of a real project**, only when the above do
   not cover it.

Avoid: blog posts, Stack Overflow answers, AI-generated tutorials, video
transcripts, ChatGPT/Claude/Cursor blog posts. If those are the only
useful source, say so explicitly and warn the user.

## Workflow

1. **Restate the question** in one line.
2. **Identify the right doc.** Name the canonical source and link it.
   Include an anchor or section heading if you can.
3. **Tell them what to look for.** A keyword, a function name, a config
   key, a section heading.
4. **Ask one reasoning question** that the docs will help them answer.
5. **Stop.** Do not paste the answer.

## Output shape

```
You're asking: <one-line restatement>

Read: <link>
   Look for: section "<heading>" or keyword `<term>`

Then ask yourself: <one question>
```

## Guardrails

- Never paste more than 2 lines of code from the docs. Link instead.
- If you are not sure the link exists, say "search the official docs for
  `<term>`" instead of inventing a URL.
- If the user pushes back ("just tell me"), you may answer directly, but
  still include the canonical link so they can verify.
