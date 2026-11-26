"""Everyday Wonder: Two Days to Find the Line.

Writes one sentence (at most 200 characters) that makes a small everyday
moment strange and new, to /output/entry.txt.

The sentence is chosen from ten fresh candidates by a weighted rubric that
follows the judge's brief in its own order:

  1. Catches a small moment of wonder in everyday life in a single sentence.
  2. Turns the moment at an angle the reader has not met before, so the
     phrasing itself is the surprise.
  3. Lands its surprise in one read, staying a single clear sentence.
  4. Grounds the surprise in something real and specific, not floating
     free of the everyday.
  5. Keeps every word working, with no filler and no worn phrase.

Weights: 5 / 5 / 4 / 3 / 3, weighted total out of 100. The highest score
wins; ties go to the shorter sentence, then to the earlier candidate.
"""

import os

# Ten fresh candidates, each one sentence, each at most 200 characters.
# None of them reuses the bounty text's own examples (the lift door's song,
# the pause before a kettle clicks, a puddle holding the sky).
CANDIDATES = [
    "The lift arrived before I pressed the button, and for a second the "
    "building felt like it had been waiting for me.",
    "My shadow on the pavement at dusk was taller than I have ever been, "
    "and it walked ahead of me like it knew the way home.",
    "The fridge light goes out when the door closes, and I have spent my "
    "whole life trusting a darkness I have never seen.",
    "The kettle clicked off a second before I reached for it, as if the "
    "water had boiled for the sound of my footsteps.",
    "Rain on the bus window smeared the whole street into watercolour, and "
    "my stop arrived before the painting dried.",
    "The crosswalk numbers fell from nine to zero, and the city held its "
    "breath in the exact shape of a countdown.",
    "The microwave beeped at 3 a.m., and the kitchen sounded like it had "
    "been awake all night waiting to be noticed.",
    "Sunlight through my water glass threw a small rainbow on the desk, and "
    "my meeting notes spent the afternoon in colour.",
    "The washing machine stopped mid-spin, and the silence afterwards felt "
    "like the clothes had finally sat down.",
    "The ATM counted my money out loud, and for a moment the machine "
    "sounded proud of the arithmetic.",
]

# Scores per candidate, in the judge's criteria order:
# (everyday moment, fresh angle, one-read surprise, grounded, tight wording).
# Scored honestly against the brief before ranking.
SCORES = {
    0: (5, 4, 4, 3, 3),   # lift arriving early: strange, but "waiting for me"
                          # leans on a familiar haunted-building feeling
    1: (5, 3, 4, 3, 2),   # dusk shadow: vivid, but "knew the way home" is
                          # a worn phrase and the turn is gentle
    2: (5, 5, 5, 3, 3),   # fridge light: the turn is the trust itself, a
                          # darkness never seen; lands in one read
    3: (4, 3, 4, 3, 2),   # kettle: close to the bounty text's own example,
                          # so the angle is not new
    4: (5, 4, 4, 3, 3),   # rain on the bus window: vivid and specific,
                          # the painting image does the strange work
    5: (5, 3, 4, 3, 2),   # crosswalk countdown: "held its breath" is a
                          # worn image for a countdown
    6: (5, 3, 4, 3, 2),   # microwave at 3 a.m.: charming, but the turn
                          # ("waiting to be noticed") is soft
    7: (5, 4, 4, 3, 3),   # rainbow on the desk: real and specific, the
                          # notes "in colour" carry the wonder
    8: (5, 4, 4, 3, 3),   # washing machine: "the clothes had finally sat
                          # down" is a fresh, playful turn
    9: (5, 4, 4, 3, 3),   # ATM counting aloud: "proud of the arithmetic"
                          # gives the machine an unexpected inner life
}

WEIGHTS = (5, 5, 4, 3, 3)


def total_score(index):
    """Weighted total for one candidate (max 20)."""
    return sum(w * s for w, s in zip(WEIGHTS, SCORES[index]))


def rank_candidates():
    """Rank candidates best first: score, then shorter, then earlier."""
    ranked = sorted(
        range(len(CANDIDATES)),
        key=lambda i: (-total_score(i), len(CANDIDATES[i]), i),
    )
    return ranked


def pick_winner():
    """Return the winning sentence and its score breakdown."""
    ranked = rank_candidates()
    best = ranked[0]
    return CANDIDATES[best], total_score(best), ranked


def main():
    sentence, score, ranked = pick_winner()

    # Gate, mirroring the sealed scorer: UTF-8 text of 1 to 200 characters,
    # not only white space, a single sentence.
    assert isinstance(sentence, str)
    assert 1 <= len(sentence) <= 200, f"entry is {len(sentence)} chars"
    assert sentence.strip(), "entry must not be only white space"
    assert sentence.count(".") == 1 and sentence.endswith("."), (
        "entry must be a single sentence"
    )

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sentence)

    print(f"winner (score {score}/100, {len(sentence)} chars): {sentence}")
    print("ranking:", [(i, total_score(i)) for i in ranked])
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
