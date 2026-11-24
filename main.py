"""Entry for make.fun bounty "Two Lines to Your Past Self".

Moment: the parking meter on Elm Street on a Tuesday afternoon.
Line 1 warns past self about that one specific moment; line 2
traces the cause and effect (ignored fine -> doubled -> a week's
grocery money gone -> phone alarm for every meter since).

Writes exactly one text (two lines) to /output/entry.txt (UTF-8).
Output directory can be overridden with the OUTPUT_DIR env var.
Python stdlib only.
"""

import os
import sys

ENTRY_TEXT = (
    "Don't trust the Elm Street meter Tuesday afternoon \u2014 "
    "it expired while you were still in the interview, "
    "and you came back to a ticket on the windshield.\n"
    "You ignored the fine for a month, so it doubled and ate "
    "a week's grocery money, and now you set a phone alarm "
    "for every meter."
)


def _is_one_sentence(line):
    """One sentence: ends with a single period, no other terminators."""
    stripped = line.strip()
    if not stripped.endswith("."):
        return False
    # Exactly one sentence-ending period, no ? or ! inside.
    return stripped.count(".") == 1 and "?" not in stripped and "!" not in stripped


def main():
    text = ENTRY_TEXT

    # Gate: total length 1-280 characters, not only whitespace.
    assert 1 <= len(text) <= 280, f"total length {len(text)} out of 1-280"
    assert text.strip(), "entry must not be only whitespace"

    # Gate: exactly 2 lines, no excess trailing newline.
    assert not text.endswith("\n"), "entry must not end with a newline"
    lines = text.split("\n")
    assert len(lines) == 2, f"expected exactly 2 lines, got {len(lines)}"
    assert all(line.strip() for line in lines), "lines must not be blank"

    # Gate: line 1 is one sentence (warning about one specific moment),
    # line 2 is one sentence (why it mattered / what changed).
    assert _is_one_sentence(lines[0]), "line 1 must be exactly one sentence"
    assert _is_one_sentence(lines[1]), "line 2 must be exactly one sentence"

    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "entry.txt")

    data = text.encode("utf-8")
    with open(output_path, "wb") as f:
        f.write(data)

    # Read-back: byte-identical.
    with open(output_path, "rb") as f:
        read_back = f.read()
    assert read_back == data, "read-back is not byte-identical to entry text"

    print(f"Wrote {output_path} ({len(text)} characters, 2 lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
