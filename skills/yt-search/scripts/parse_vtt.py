#!/usr/bin/env python3
"""Parse VTT subtitle files into clean plain text.

Usage:
    python parse_vtt.py <vtt_file> [--output <output_file>]

If --output is omitted, prints to stdout.
Handles: time codes, HTML tags, duplicate lines, VTT headers.
Exit code 1 if file not found or empty result.
"""

import re
import sys
import argparse


def parse_vtt(vtt_path: str) -> str:
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()

    seen, text = set(), []
    for line in content.split("\n"):
        line = line.strip()
        # Skip VTT headers and blank lines
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        # Skip timestamps and cue identifiers
        if re.match(r"^\d{2}:\d{2}", line) or "-->" in line or re.match(r"^\d+$", line):
            continue
        # Strip HTML tags
        clean = re.sub(r"<[^>]+>", "", line).strip()
        if clean and clean not in seen:
            seen.add(clean)
            text.append(clean)

    return " ".join(text)


def main():
    parser = argparse.ArgumentParser(description="Convert VTT subtitles to plain text")
    parser.add_argument("vtt_file", help="Path to .vtt file")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    args = parser.parse_args()

    try:
        transcript = parse_vtt(args.vtt_file)
    except FileNotFoundError:
        print(f"Error: File not found: {args.vtt_file}", file=sys.stderr)
        sys.exit(1)

    if not transcript:
        print("Error: No text extracted (file may be empty or contain only timestamps)", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"Saved transcript ({len(transcript)} chars) to {args.output}")
    else:
        print(transcript)


if __name__ == "__main__":
    main()
