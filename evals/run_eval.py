#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Windows-compatible version. Replaces select.select() with threading-based
non-blocking I/O, which works on Windows subprocess pipes.

Usage:
    python evals/run_eval.py --eval-set evals/notebooklm-trigger-eval.json \
        --skill-path skills/anything-to-notebooklm --verbose

Requires: claude CLI on PATH.
"""

import argparse
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


def parse_skill_md(skill_path: Path) -> tuple:
    """Parse SKILL.md frontmatter, returning (name, description, content)."""
    for candidate in ("SKILL.md", "skill.md"):
        p = skill_path / candidate
        if p.exists():
            content = p.read_text(encoding="utf-8")
            break
    else:
        raise FileNotFoundError(f"No SKILL.md or skill.md in {skill_path}")

    lines = content.split("\n")
    if lines[0].strip() != "---":
        raise ValueError("Missing frontmatter (no opening ---)")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("Missing frontmatter (no closing ---)")

    name = ""
    description = ""
    fm = lines[1:end_idx]
    i = 0
    while i < len(fm):
        line = fm[i]
        if line.startswith("name:"):
            name = line[len("name:") :].strip().strip("\"'")
        elif line.startswith("description:"):
            value = line[len("description:") :].strip()
            if value in (">", "|", ">-", "|-"):
                parts = []
                i += 1
                while i < len(fm) and (
                    fm[i].startswith("  ") or fm[i].startswith("\t")
                ):
                    parts.append(fm[i].strip())
                    i += 1
                description = " ".join(parts)
                continue
            else:
                description = value.strip("\"'")
        i += 1

    return name, description, content


def find_project_root() -> Path:
    """Walk up from cwd looking for .claude/ directory."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


def _read_stream(pipe, lines_out, done_event):
    """Read lines from pipe in a background thread (Windows-safe).

    Unlike select.select(), this works on Windows where subprocess pipes
    are not selectable file descriptors.
    """
    try:
        for raw in pipe:
            lines_out.append(raw.decode("utf-8", errors="replace"))
    except Exception:
        pass
    finally:
        done_event.set()


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run a single query and detect whether the skill was triggered.

    Creates a temporary command file so the skill appears in Claude's
    available_skills list, then runs `claude -p` and parses stream events
    to detect triggering. Uses threading instead of select.select() for
    Windows compatibility.
    """
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    commands_dir = Path(project_root) / ".claude" / "commands"
    command_file = commands_dir / f"{clean_name}.md"

    try:
        commands_dir.mkdir(parents=True, exist_ok=True)
        indented = "\n  ".join(skill_description.split("\n"))
        command_file.write_text(
            f"---\ndescription: |\n  {indented}\n---\n\n"
            f"# {skill_name}\n\nThis skill handles: {skill_description}\n",
            encoding="utf-8",
        )

        cmd = [
            "claude",
            "-p",
            query,
            "--output-format",
            "stream-json",
            "--verbose",
            "--include-partial-messages",
        ]
        if model:
            cmd.extend(["--model", model])

        # Remove CLAUDECODE env var to allow nesting claude -p
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=project_root,
            env=env,
        )

        # Thread-based non-blocking read (replaces select.select)
        lines: list[str] = []
        done_event = threading.Event()
        reader = threading.Thread(
            target=_read_stream,
            args=(process.stdout, lines, done_event),
            daemon=True,
        )
        reader.start()

        triggered = False
        pending_tool_name = None
        accumulated_json = ""
        start_time = time.time()
        processed_idx = 0

        try:
            while time.time() - start_time < timeout:
                # Process new lines from the reader thread
                while processed_idx < len(lines):
                    raw_line = lines[processed_idx].strip()
                    processed_idx += 1
                    if not raw_line:
                        continue

                    try:
                        event = json.loads(raw_line)
                    except json.JSONDecodeError:
                        continue

                    # Early detection via stream events
                    if event.get("type") == "stream_event":
                        se = event.get("event", {})
                        se_type = se.get("type", "")

                        if se_type == "content_block_start":
                            cb = se.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                tool_name = cb.get("name", "")
                                if tool_name in ("Skill", "Read"):
                                    pending_tool_name = tool_name
                                    accumulated_json = ""
                                else:
                                    return False

                        elif (
                            se_type == "content_block_delta" and pending_tool_name
                        ):
                            delta = se.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated_json += delta.get(
                                    "partial_json", ""
                                )
                                if clean_name in accumulated_json:
                                    return True

                        elif se_type in ("content_block_stop", "message_stop"):
                            if pending_tool_name:
                                return clean_name in accumulated_json
                            if se_type == "message_stop":
                                return False

                    # Fallback: full assistant message
                    elif event.get("type") == "assistant":
                        message = event.get("message", {})
                        for item in message.get("content", []):
                            if item.get("type") != "tool_use":
                                continue
                            inp = item.get("input", {})
                            nm = item.get("name", "")
                            if nm == "Skill" and clean_name in inp.get(
                                "skill", ""
                            ):
                                return True
                            elif nm == "Read" and clean_name in inp.get(
                                "file_path", ""
                            ):
                                return True
                        return False

                    elif event.get("type") == "result":
                        return triggered

                # Check if reader finished
                if done_event.is_set() and processed_idx >= len(lines):
                    break

                time.sleep(0.1)

        finally:
            if process.poll() is None:
                process.kill()
                process.wait()

        return triggered
    finally:
        if command_file.exists():
            command_file.unlink()


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    results = []
    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should = item["should_trigger"]
        if should:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append(
            {
                "query": query,
                "should_trigger": should,
                "trigger_rate": trigger_rate,
                "triggers": sum(triggers),
                "runs": len(triggers),
                "pass": did_pass,
            }
        )

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run trigger evaluation (Windows-compatible)"
    )
    parser.add_argument(
        "--eval-set", required=True, help="Path to eval set JSON"
    )
    parser.add_argument(
        "--skill-path", required=True, help="Path to skill directory"
    )
    parser.add_argument(
        "--description", default=None, help="Override description"
    )
    parser.add_argument("--num-workers", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--runs-per-query", type=int, default=3)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--model", default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    skill_path = Path(args.skill_path)

    name, original_description, _ = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        n_true = sum(1 for e in eval_set if e["should_trigger"])
        n_false = len(eval_set) - n_true
        print(f"Skill: {name}", file=sys.stderr)
        print(
            f"Queries: {len(eval_set)} ({n_true} should-trigger, "
            f"{n_false} should-not)",
            file=sys.stderr,
        )
        print(f"Runs per query: {args.runs_per_query}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        s = output["summary"]
        print(
            f"\nResults: {s['passed']}/{s['total']} passed", file=sys.stderr
        )
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate = f"{r['triggers']}/{r['runs']}"
            print(
                f"  [{status}] rate={rate} expected={r['should_trigger']}: "
                f"{r['query'][:70]}",
                file=sys.stderr,
            )

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
