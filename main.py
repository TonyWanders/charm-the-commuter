#!/usr/bin/env python3
"""Write one line of weather forecast for a city that does not exist.

Deterministic: no network, no clock, no randomness. The forecast is a
fixed string. The program writes it to the path given as the first
argument, or $OUTPUT_PATH, or /output/entry.txt by default, and enforces
the competition gate: 1 to 140 characters, not only white space.
"""

import os
import sys
from pathlib import Path

FORECAST = (
    "Today in Brindlewick: sunny spells, a light breeze, and the 8:15 bus "
    "arrives on time for once, so mind the miracle, commuters."
)

MIN_CHARS = 1
MAX_CHARS = 140
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 140 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"forecast is {chars} characters, outside 1-140")
    if not text.strip():
        raise ValueError("forecast is only white space")
    if "\n" in text:
        raise ValueError("forecast must be one line")
    return chars


def main() -> int:
    try:
        chars = validate(FORECAST)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FORECAST, encoding="utf-8")
    os.chmod(path, 0o644)
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
