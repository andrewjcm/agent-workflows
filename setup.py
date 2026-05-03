#!/usr/bin/env python3
"""
setup.py - install agent-workflows into your agent config dirs.

Not a setuptools script. This copies (does not symlink) the shared
skills, OpenCode commands and agents, and Claude Code commands and
agents into the appropriate config directories. Missing directories
are created. If a destination file already exists and differs from the
source, you're prompted before it gets overwritten.

Usage:
    python3 setup.py                       interactive, install everything (default)
    python3 setup.py --target claude       Claude Code only
    python3 setup.py --target opencode     OpenCode only
    python3 setup.py --target project      project-local install in cwd
    python3 setup.py --yes                 overwrite all without prompting
    python3 setup.py --skip-existing       keep every existing file untouched
    python3 setup.py --dry-run             show planned actions without writing

Environment variables (override default install paths):
    AGENT_WORKFLOWS_HOME  repo root (default: dirname of this script)
    CLAUDE_HOME           Claude Code config dir (default: ~/.claude)
    OPENCODE_HOME         OpenCode config dir (default: ~/.config/opencode)
    SHARED_SKILLS_HOME    cross-tool skills dir (default: ~/.agents/skills)
"""
from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(
    os.environ.get("AGENT_WORKFLOWS_HOME") or Path(__file__).resolve().parent
)
CLAUDE_HOME = Path(os.environ.get("CLAUDE_HOME") or Path.home() / ".claude")
OPENCODE_HOME = Path(
    os.environ.get("OPENCODE_HOME") or Path.home() / ".config" / "opencode"
)
SHARED_SKILLS_HOME = Path(
    os.environ.get("SHARED_SKILLS_HOME") or Path.home() / ".agents" / "skills"
)


class Decider:
    """Tracks the user's overwrite policy across files in one run."""

    def __init__(self, mode: str):
        # one of: "ask", "yes", "skip"
        self.mode = mode

    def should_overwrite(self, dest: Path) -> bool:
        if self.mode == "yes":
            return True
        if self.mode == "skip":
            return False
        while True:
            try:
                ans = input(
                    f"  exists: {dest}\n"
                    f"    [O]verwrite / [s]kip / [a]ll-overwrite / "
                    f"[n]one / [q]uit ? "
                ).strip().lower()
            except EOFError:
                print("\n  no input; treating as skip")
                return False
            if ans in ("", "o", "overwrite"):
                return True
            if ans in ("s", "skip"):
                return False
            if ans in ("a", "all"):
                self.mode = "yes"
                return True
            if ans in ("n", "none"):
                self.mode = "skip"
                return False
            if ans in ("q", "quit"):
                print("aborted by user")
                sys.exit(130)
            print("  please answer o, s, a, n, or q")


def install_file(src: Path, dest: Path, decider: Decider, dry_run: bool) -> None:
    if dest.exists():
        if dest.is_dir():
            print(f"  warn  {dest} is a directory but source is a file; skipping")
            return
        if filecmp.cmp(src, dest, shallow=False):
            print(f"  same  {dest}")
            return
        if not decider.should_overwrite(dest):
            print(f"  skip  {dest}")
            return
        verb = "over"
    else:
        verb = "copy"
    if dry_run:
        print(f"  plan  {dest}  ({verb})")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"  {verb}  {dest}")


def install_dir_contents(
    src_dir: Path, dest_dir: Path, decider: Decider, dry_run: bool
) -> None:
    """Mirror each top-level entry of src_dir into dest_dir.

    Files are copied directly. Directories are mirrored recursively.
    """
    if not src_dir.is_dir():
        print(f"  warn  source missing: {src_dir}; skipping")
        return
    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)
    for entry in sorted(src_dir.iterdir()):
        sub_dest = dest_dir / entry.name
        if entry.is_dir():
            for child in sorted(entry.rglob("*")):
                if child.is_dir():
                    continue
                rel = child.relative_to(entry)
                install_file(child, sub_dest / rel, decider, dry_run)
        else:
            install_file(entry, sub_dest, decider, dry_run)


def section(title: str) -> None:
    print()
    print(title)


def install_opencode(decider: Decider, dry_run: bool) -> None:
    section(f"OpenCode commands -> {OPENCODE_HOME / 'commands'}")
    install_dir_contents(
        REPO_ROOT / "opencode" / "commands",
        OPENCODE_HOME / "commands",
        decider,
        dry_run,
    )
    section(f"OpenCode agents -> {OPENCODE_HOME / 'agents'}")
    install_dir_contents(
        REPO_ROOT / "opencode" / "agents",
        OPENCODE_HOME / "agents",
        decider,
        dry_run,
    )
    section(f"Shared skills -> {SHARED_SKILLS_HOME}")
    install_dir_contents(
        REPO_ROOT / "shared" / "skills",
        SHARED_SKILLS_HOME,
        decider,
        dry_run,
    )


def install_claude(decider: Decider, dry_run: bool) -> None:
    section(f"Claude commands -> {CLAUDE_HOME / 'commands'}")
    install_dir_contents(
        REPO_ROOT / "claude" / "commands",
        CLAUDE_HOME / "commands",
        decider,
        dry_run,
    )
    section(f"Claude agents -> {CLAUDE_HOME / 'agents'}")
    install_dir_contents(
        REPO_ROOT / "claude" / "agents",
        CLAUDE_HOME / "agents",
        decider,
        dry_run,
    )
    section(f"Claude skills -> {CLAUDE_HOME / 'skills'}")
    install_dir_contents(
        REPO_ROOT / "shared" / "skills",
        CLAUDE_HOME / "skills",
        decider,
        dry_run,
    )
    section(f"Shared skills -> {SHARED_SKILLS_HOME}")
    install_dir_contents(
        REPO_ROOT / "shared" / "skills",
        SHARED_SKILLS_HOME,
        decider,
        dry_run,
    )


def install_project(decider: Decider, dry_run: bool) -> None:
    project = Path.cwd()
    if project.resolve() == REPO_ROOT.resolve():
        print(
            "refusing to install into the agent-workflows repo itself",
            file=sys.stderr,
        )
        sys.exit(2)
    print(f"  project: {project}")
    section(f"Project Claude skills -> {project / '.claude' / 'skills'}")
    install_dir_contents(
        REPO_ROOT / "shared" / "skills",
        project / ".claude" / "skills",
        decider,
        dry_run,
    )
    section(f"Project OpenCode commands -> {project / '.opencode' / 'commands'}")
    install_dir_contents(
        REPO_ROOT / "opencode" / "commands",
        project / ".opencode" / "commands",
        decider,
        dry_run,
    )
    section(f"Project OpenCode agents -> {project / '.opencode' / 'agents'}")
    install_dir_contents(
        REPO_ROOT / "opencode" / "agents",
        project / ".opencode" / "agents",
        decider,
        dry_run,
    )
    section(f"Project AGENTS.md -> {project / 'AGENTS.md'}")
    install_file(
        REPO_ROOT / "AGENTS.md",
        project / "AGENTS.md",
        decider,
        dry_run,
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Copy agent-workflows files into your agent config dirs, "
            "creating directories as needed and prompting before overwrites."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--target",
        choices=["all", "claude", "opencode", "project"],
        default="all",
        help="which install target to run (default: all)",
    )
    g = p.add_mutually_exclusive_group()
    g.add_argument(
        "--yes", "-y",
        action="store_true",
        help="overwrite existing files without prompting",
    )
    g.add_argument(
        "--skip-existing",
        action="store_true",
        help="keep existing files untouched, never prompt",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="print what would happen without writing anything",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.yes:
        decider = Decider("yes")
    elif args.skip_existing:
        decider = Decider("skip")
    else:
        decider = Decider("ask")

    print("agent-workflows install")
    print(f"  repo:           {REPO_ROOT}")
    print(f"  claude home:    {CLAUDE_HOME}")
    print(f"  opencode home:  {OPENCODE_HOME}")
    print(f"  shared skills:  {SHARED_SKILLS_HOME}")
    print(f"  target:         {args.target}")
    if args.dry_run:
        print("  dry run:        yes (no files will be written)")

    if args.target == "project":
        install_project(decider, args.dry_run)
    else:
        if args.target in ("all", "opencode"):
            install_opencode(decider, args.dry_run)
        if args.target in ("all", "claude"):
            install_claude(decider, args.dry_run)

    print()
    print("done.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\naborted", file=sys.stderr)
        sys.exit(130)
