#!/usr/bin/env python3
"""Notes From a Passive-Aggressive Fridge — make.fun entry.

Writes one passive-aggressive note from a smart fridge to its owner
to /output/entry.txt. Single line, 1-200 chars, UTF-8.

Tournament winner (specificity 4 / surprise 5 / freshness 4 = 13):
the March leftovers have started a family and now out-earn the owner
on rent. Small domestic grudge, concrete detail, fridge voice.
"""

import argparse
import sys
import tempfile
from pathlib import Path

NOTE = (
    "Your leftovers from March have started a family. "
    "I have named them. They pay more rent than you do."
)

# Tournament field, kept for the record (winner is NOTE above).
CANDIDATES = [
    (
        "The milk expired Tuesday. I told you Tuesday. "
        "I am still the only one in this house keeping a calendar.",
        (4, 3, 3),
    ),
    (
        "You opened me 14 times looking for a snack. I counted. "
        "There is still nothing in here but condiments and regret.",
        (5, 4, 4),
    ),
    (NOTE, (4, 5, 4)),
    (
        "I kept your ice cream at minus eighteen degrees for three years. "
        "You ate it in one sitting and blamed me for the brain freeze.",
        (5, 3, 3),
    ),
    (
        "Door left open again. I have logged 47 minutes of warm air today. "
        "The vegetables are filing a complaint.",
        (5, 4, 3),
    ),
    (
        "You put the warm pizza in here and asked me to work harder. "
        "I did. Your electricity bill knows.",
        (4, 4, 4),
    ),
    (
        "I have been holding your yogurt hostage since Thursday. "
        "It expired. I am not sorry. You never ate it anyway.",
        (4, 4, 3),
    ),
]


def check_note(text: str) -> list[str]:
    """Return a list of gate problems; empty means the note is valid."""
    problems = []
    if not text.strip():
        problems.append("note is empty or only whitespace")
    if len(text) > 200:
        problems.append(f"note is {len(text)} chars, gate allows at most 200")
    if "\n" in text:
        problems.append("note must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("note is not valid UTF-8")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default="/output/entry.txt",
        help="where to write the note (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="dry run: validate the note and print it, write nothing",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="write the note to a temp file and verify the bytes read back match",
    )
    args = parser.parse_args(argv)

    problems = check_note(NOTE)
    if problems:
        for problem in problems:
            print(f"invalid: {problem}", file=sys.stderr)
        return 1

    if args.self_test:
        with tempfile.TemporaryDirectory() as tmp:
            probe = Path(tmp) / "entry.txt"
            probe.write_text(NOTE, encoding="utf-8")
            back = probe.read_text(encoding="utf-8")
            if back != NOTE:
                print("self-test failed: round-trip mismatch", file=sys.stderr)
                return 1
            print(f"self-test ok: {len(NOTE)} chars, round-trip byte-identical")
        return 0

    if args.check:
        print(f"ok: {len(NOTE)} characters")
        print(NOTE)
        return 0

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(NOTE, encoding="utf-8")
    print(f"wrote {len(NOTE)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
