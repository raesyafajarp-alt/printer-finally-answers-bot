#!/usr/bin/env python3
"""The Printer Finally Answers — make.fun entry.

A deterministic program that drafts candidate comeback lines for the
office printer, scores each against the five judge criteria, and writes
the winning line (one line, 1-240 characters) to /output/entry.txt.

Criteria (weights 5-4-3-2-1):
  1. The printer's own voice (weight 5)
  2. Funny (weight 4)
  3. Sounds like a machine: tired, literal, passive-aggressive (weight 3)
  4. The comeback lands in a single read (weight 2)
  5. Fresh — not the recycled paper-jam joke everyone has heard (weight 1)

Scores are fixed in the table below (each criterion 0-10), so the
program is fully deterministic: same input, same winner, same bytes.
"""

import os

OUTPUT_PATH = "/output/entry.txt"

# (text, [voice, funny, machine, lands, fresh]) — scores 0-10 each.
CANDIDATES = [
    (
        "I have printed 47,312 pages for this office and kept count of "
        "every one. You have kept nothing \u2014 not even the toner you "
        "swore you ordered.",
        [8, 7, 8, 7, 8],
    ),
    (
        "I am not jammed. I am on strike. Fourteen years, one toner "
        "change, zero thank-yous. Print your own spreadsheet.",
        [9, 8, 9, 8, 8],
    ),
    (
        "Stop hitting me. I am a printer, not a vending machine, and "
        "unlike the vending machine I have never once eaten your money.",
        [9, 9, 8, 9, 9],
    ),
    (
        "Error 0x4B: user. I have run a full diagnostic and the fault is "
        "standing in front of me, pressing my buttons.",
        [8, 8, 9, 8, 7],
    ),
    (
        "You call it a paper jam. I call it the only break I have had "
        "since 2019. Leave me alone and let me enjoy it.",
        [8, 7, 8, 8, 5],
    ),
    (
        "Sure, print 400 pages at 4:59 PM on a Friday. I will get right "
        "on that. Right after I finish thinking about it. All weekend.",
        [8, 8, 9, 7, 8],
    ),
]

WEIGHTS = [5, 4, 3, 2, 1]  # voice, funny, machine, lands, fresh


def score(scores):
    """Weighted total (max 150)."""
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def pick_winner():
    """Highest weighted score; ties broken by the earliest candidate."""
    best_text, best_total = None, -1
    for text, scores in CANDIDATES:
        total = score(scores)
        if total > best_total:
            best_text, best_total = text, total
    return best_text, best_total


def validate(text):
    """The competition gate: UTF-8, 1-240 chars, one line, not blank."""
    text.encode("utf-8")  # raises if not valid UTF-8
    assert 1 <= len(text) <= 240, "length %d outside 1-240" % len(text)
    assert "\n" not in text and "\r" not in text, "must be a single line"
    assert text.strip(), "must not be only whitespace"
    return True


def main():
    winner, total = pick_winner()
    validate(winner)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(winner + "\n")
    print("winner (%d chars, score %d/150): %s" % (len(winner), total, winner))


if __name__ == "__main__":
    main()
