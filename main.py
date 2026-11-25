#!/usr/bin/env python3
"""The Funniest Honest Appliance Error -- a microwave confesses.

A microwave oven reports the one fault it can never fix: its own
uneven heating. The edges of the food come out scalding while the
middle stays frozen, and the machine, having done exactly what it
was built to do, calls the result a success.

The program writes that one honest error line to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt), exactly one
line of at most 200 characters, and nothing else.
"""

import os
import sys

# The line itself, built from the three things the microwave knows:
# the cycle is over, the heating was uneven, and it is proud anyway.
ANNOUNCEMENT = "Your food is ready."
FAULT_EDGES = "The edges are lava."
FAULT_MIDDLE = "The middle is ice."
VERDICT = "I have achieved balance."

MAX_CHARS = 200


def compose_error():
    """Join the microwave's report into its single error line."""
    parts = [ANNOUNCEMENT, FAULT_EDGES, FAULT_MIDDLE, VERDICT]
    return " ".join(parts)


def check_line(line):
    """Refuse anything the gate would refuse.

    The gate wants UTF-8 text of 1 to 200 characters, not only
    white space, on a single line. Check that here so a bad line
    fails loudly on our side instead of silently on theirs.
    """
    if not line or not line.strip():
        raise ValueError("error line is empty or only white space")
    if "\n" in line or "\r" in line:
        raise ValueError("error line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "error line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    line.encode("utf-8")  # raises if the line is not valid UTF-8
    return line


def output_path():
    """Where the entry text goes: the harness directory, or /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def main():
    line = check_line(compose_error())
    path = output_path()
    # Write exactly the line, no trailing newline: the file's
    # contents are the entry, byte for byte.
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    # Read it back: the file on disk must be the line we checked,
    # so a partial write fails here instead of at the gate.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != line:
        raise ValueError("entry.txt on disk does not match the line")
    print(line)
    print("(%d characters)" % len(line))
    return 0


if __name__ == "__main__":
    sys.exit(main())
