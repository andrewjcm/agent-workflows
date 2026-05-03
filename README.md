# agent-workflows

Portable, skill-preserving coding-agent workflows for [OpenCode](https://opencode.ai)
and [Claude Code](https://docs.claude.com/en/docs/claude-code).

## Purpose

Most agent setups optimize for raw ship time. They will happily generate the
whole feature, the whole test suite, and the whole commit message while you
stop typing and stop thinking. That is fast, and it is also how you forget how
your own codebase works.

This repo is the opposite bet. It bundles a small, curated set of:

- **Shared skills** (`shared/skills/`) - reusable prompts that bias agents
  toward hints, questions, official docs, and small reasoning steps.
- **OpenCode commands and agents** (`opencode/`) - slash commands and
  sub-agents wired up for OpenCode.
- **Claude Code commands and agents** (`claude/`) - the same workflows in a
  Claude-compatible shape.
- **Installer** (`setup.py`) - a Python 3 script that copies the above into
  the right config directories on your machine or into a project, prompting
  before overwriting any existing file.

The defaults assume you are a working developer who wants agents to *shorten*
the slog without *replacing* the thinking. You can always escalate to a
heavier "just build it" mode, but you have to opt in.

## Recommended workflow loop

The intended day-to-day loop is:

```
write myself  ->  review  ->  fix myself  ->  tests-first  ->  implement tests  ->  explain diff
```

Concretely:

1. **write myself** - draft the code by hand. No agent.
2. **review** - run `/review-mine` to get a rubric-based review. The reviewer
   does not rewrite code; it points at issues and asks questions.
3. **fix myself** - apply the review feedback yourself.
4. **tests-first** - run `/tests-first` to get a list of test cases (names,
   inputs, expected outcomes) *before* you write any test code.
5. **implement tests** - write the tests yourself from that list.
6. **explain diff** - run `/explain-diff` to get a plain-language description
   of what the change actually does, so you catch surprises before commit.

Stuck? Use `/hint` or `/docs-hint` instead of asking the agent to solve it.
Genuinely stuck on a bug? Use `/debug-coach` and bring a hypothesis.

## Product Planning Workflow

The coding loop above assumes you already know what you're building. When
you don't, run the product loop *first* - before any code gets written:

```
idea  ->  /product-plan  ->  /generate-tickets  ->  build
```

- **`/product-plan`** invokes the `product-persona` voice (a senior PM
  crossed with a pragmatic product engineer) under the
  `product-discovery` skill. It interrogates the idea before producing
  anything: who is it for, what pain exists today, why now, what would
  make users ignore it, what is the smallest valuable version. Then it
  outputs a structured plan with MVP scope, risks, success metrics, and
  a clear recommendation - **ship now**, **validate first**, **defer**,
  or **needs more research**.
- **`/generate-tickets`** turns a validated plan (or a raw feature
  description, in a pinch) into a small, sequenced set of engineering
  tickets with observable acceptance criteria, dependencies, and rough
  sizes. Capped at 10 tickets unless it justifies more, and explicitly
  names what is parallelizable and what is deferred.

### Examples

```text
/product-plan      Add shared team dashboards
/product-plan      Add admin CSV import flow
/product-plan      Let users save AI prompt presets

/generate-tickets  Add admin CSV import flow
/generate-tickets  [paste /product-plan output]
```

### Benefits

- Prevents overbuilding by forcing MVP scope before tickets exist.
- Clarifies user value in concrete persona-and-pain terms.
- Exposes hidden complexity early - migrations, permissions, error
  states, abuse paths, accessibility.
- Produces implementation-ready plans that don't need follow-up
  questions to start.
- Especially useful for solo founders and IC engineers who do their
  own product thinking.

**Use this before coding begins.** The product persona will say "don't
build this yet" when an idea isn't ready - that's a feature, not a
bug. Running `/product-plan` and getting back "validate first" has
already saved you a sprint.

## Expected ship-time factor

Rough, honest estimates of how these modes change shipping speed - and what
they cost in skill retention:

| Mode             | Ship-time factor | Skill risk |
|------------------|------------------|------------|
| no agent         | 1.0x             | none       |
| hint-only        | 1.1x - 1.3x      | very low   |
| hint + docs      | 1.25x - 1.7x     | low        |
| agent-heavy      | 1.5x - 3x        | high       |

"Agent-heavy" means the builder agent is editing files for you. It is the
fastest and the most corrosive to your understanding of the codebase. Use it
when you have already understood the change and want to skip the typing -
not as a substitute for the understanding.

## Install

Installation uses a single Python script, `setup.py`, that **copies** files
from this repo into your agent config directories. Missing directories are
created. If a destination file already exists and differs from the source,
you'll be prompted before it gets overwritten - so a stale install never
silently clobbers a file you've edited.

> Despite the name, `setup.py` is *not* a setuptools script. It's a plain
> Python 3 program with no third-party dependencies.

Clone the repo somewhere stable:

```bash
git clone https://github.com/andrewjcm/agent-workflows ~/code/agent-workflows
cd ~/code/agent-workflows
```

### Default install (everything)

```bash
python3 setup.py
```

This copies, in order:

- `opencode/commands/*` -> `~/.config/opencode/commands/`
- `opencode/agents/*`   -> `~/.config/opencode/agents/`
- `claude/commands/*`   -> `~/.claude/commands/`
- `claude/agents/*`     -> `~/.claude/agents/`
- `shared/skills/*`     -> `~/.claude/skills/`
- `shared/skills/*`     -> `~/.agents/skills/` (cross-tool location)

For each file, `setup.py` prints one of:

- `copy` - new file written
- `over` - existing file overwritten (after you confirmed)
- `same` - destination already matches source byte-for-byte; no prompt, no write
- `skip` - you declined to overwrite, or `--skip-existing` was set
- `plan` - dry-run only; nothing written

### Single tool

```bash
python3 setup.py --target opencode    # OpenCode only
python3 setup.py --target claude      # Claude Code only
```

> Claude Code's exact paths can vary by version and OS. The defaults assume
> `~/.claude/...`. If your install uses different locations, set
> `CLAUDE_HOME` (see "Customizing paths" below).

### Project-local install

To install into the current project (so the workflows travel with the repo
and are visible to teammates):

```bash
cd /path/to/your/project
python3 /path/to/agent-workflows/setup.py --target project
```

This copies:

- `shared/skills/*`     -> `./.claude/skills/`
- `opencode/commands/*` -> `./.opencode/commands/`
- `opencode/agents/*`   -> `./.opencode/agents/`
- `AGENTS.md`           -> `./AGENTS.md`

The script refuses to run `--target project` from inside the
`agent-workflows` repo itself.

### Non-interactive flags

```bash
python3 setup.py --yes              # overwrite everything; never prompt
python3 setup.py --skip-existing    # keep existing files; never prompt
python3 setup.py --dry-run          # show what would happen; write nothing
```

`--dry-run` composes with `--yes` or `--skip-existing` to preview either
policy.

During an interactive prompt, the answer keys are:

- `o` (or just Enter) - **overwrite** this one
- `s` - **skip** this one
- `a` - **all-overwrite**: stop prompting and overwrite the rest of this run
- `n` - **none**: stop prompting and skip the rest of this run
- `q` - **quit** the install immediately

### Uninstall

There is no uninstall command. Because `setup.py` copies (not symlinks),
the installed files are independent and may be ones you've edited - the
script can't tell a stale install apart from your customizations. To remove
an install, delete the files yourself, e.g.:

```bash
rm -rf ~/.claude/skills ~/.claude/commands ~/.claude/agents
rm -rf ~/.config/opencode/commands ~/.config/opencode/agents
rm -rf ~/.agents/skills
```

For project installs, remove the matching paths under your project root.

## Customizing paths

`setup.py` respects these env vars:

- `AGENT_WORKFLOWS_HOME` - where this repo lives. Defaults to the script's
  own directory.
- `CLAUDE_HOME` - Claude Code config dir. Defaults to `~/.claude`.
- `OPENCODE_HOME` - OpenCode config dir. Defaults to `~/.config/opencode`.
- `SHARED_SKILLS_HOME` - cross-tool skills dir. Defaults to
  `~/.agents/skills`.

Example:

```bash
CLAUDE_HOME=~/.config/claude-code python3 setup.py --target claude
```

## Examples

After installing, try these in order on a real change you are working on:

```text
/product-plan      Let users save AI prompt presets
/generate-tickets  [paste /product-plan output]
/hint              I am trying to debounce this input but it still fires every keystroke.
/docs-hint         How do I cancel an in-flight fetch in modern browsers?
/tests-first       Add a discount code field to the checkout form.
/review-mine       (run this with a diff staged)
/debug-coach       My migration runs but the new column is null for old rows.
/explain-diff      (run this with a diff staged)
/refactor-plan     This module has grown to 800 lines, plan a split.
```

Builder mode is opt-in. To actually have an agent edit files, invoke the
`builder` agent explicitly and tell it what scope it owns:

```text
@builder Implement the parser tests we just designed in tests/parser_test.py.
         Do not touch parser.py. Stop after tests are red.
```

## Repo layout

```
agent-workflows/
  README.md
  AGENTS.md
  setup.py              # copy-based installer (Python 3, stdlib only)
  shared/skills/        # SKILL.md files, shared between OpenCode and Claude
  opencode/
    commands/           # OpenCode slash commands (agent: plan by default)
    agents/             # OpenCode sub-agents
  claude/
    commands/           # Claude Code slash commands (portable prompts)
    agents/             # Claude Code sub-agents
```

## License

MIT. Use it, fork it, rip out the parts you disagree with.
