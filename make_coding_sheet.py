#!/usr/bin/env python3
"""Build a blind second-coder sheet from the by_agents.py output.

    python3 make_coding_sheet.py by_agents_output.txt --n all

Writes coding_sheet.csv (what the second coder fills in), coding_key.csv (your own
codings, kept aside for comparison) and codebook.md. The sheet is shuffled and carries
no category labels, so the second coder cannot see your decisions or infer the
hypothesis from the ordering.
"""
import argparse
import csv
import hashlib
from pathlib import Path

import pandas as pd

CODEBOOK = """# Coding manual — passive by-agent phrases

You are coding phrases extracted from news reporting. Each row gives a passive
subject–verb pair and the by-phrase naming the agent, e.g.

    town_occupied    by_Russian_forces

Code three columns. Judge each phrase on its own; do not try to be consistent with
any hypothesis about the data, and ask about unclear cases rather than guessing.

## 1. include — circumstance, or actor?

Some by-phrases name the circumstance under which something happened rather than
anything that did it. Those are outside the scope of this exercise.

| Code | Criterion | Examples |
|---|---|---|
| `yes` | The by-phrase names something that performed the action | by Russian forces, by a missile |
| `no` | The by-phrase names a condition, setting or reason | by geography, by propaganda, by the minimum number of days |

Code `no` and leave the remaining columns blank. Deciding this is part of the task —
do not assume a row belongs just because it is on the sheet.

## 2. animacy — of the by-phrase: human or non-human?

| Code | Criterion | Examples |
|---|---|---|
| `human` | An individual, a collectivity, an institution, or a state acting through people | forces, military, separatists, police, parliament, Putin, Russia |
| `nonhuman` | A weapon, munition, vehicle, or an event construed as a cause | drone, missile, shelling, bombardment, explosion |
| `unclear` | Genuinely cannot be decided | — |

A state name is `human`: *occupied by Russia* attributes the act to an actor that
acts through people. A weapon is `nonhuman` even when a nationality modifies it —
in *by Russian shells* the agent is *shells*.

## 3. category — of the by-phrase — what kind of entity is the agent?

`weapon`, `military_authority`, `nonmilitary_party`, `country_city`,
`law_governance`, `death_danger`, `important_figure`, `civilian`, `location`,
`media_tech`, `neutral_entity`, `money_business`, `commute`, `nominalisation`,
`unclear`

Use `unclear` freely. A high `unclear` count is information, not failure.

## 4. valence — of the verb: what does it do to the subject?

| Code | Criterion | Examples |
|---|---|---|
| `violent` | Physical harm or destruction | killed, destroyed, struck, shelled, demolished, wounded |
| `restrictive` | Limitation or control, without direct physical harm | occupied, seized, detained, held, thwarted, controlled |
| `negative` | Adverse, but neither violent nor restrictive | frustrated, blamed, denounced, countered |
| `neutral` | No evaluative loading in context | reported, met, taken, provided, described |
| `positive` | Favourable to the passive subject | welcomed, reclaimed, allowed, recognised, released |
| `unclear` | Genuinely cannot be decided | — |

The line between `violent` and `restrictive` is physical harm. *Seize* and *detain*
constrain; *shell* and *kill* injure. Code the reading in this sentence, not the
verb's most common sense elsewhere.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("infile", help="by_agents.py output (tab-delimited)")
    ap.add_argument("--n", default="all", help="'all' (recommended) or a sample size")
    ap.add_argument("--seed", type=int, default=20260830)
    args = ap.parse_args()

    df = pd.read_csv(args.infile, sep="\t")
    cols = list(df.columns)
    low = {c.lower(): c for c in cols}

    def pick(*names, default=None):
        for n in names:
            if n in low:
                return low[n]
        for c in cols:                       # substring fallback
            if any(n in c.lower() for n in names):
                return c
        return default

    pair = pick("subject_verb", "subject-verb", "pair", "subject_verb_pairs", default=cols[0])
    agent = pick("by_agent", "by-agent", "agent", default=cols[-1])
    if pair == agent:
        raise SystemExit(f"could not tell the pair column from the agent column in {cols}")
    print(f"using pair column '{pair}' and agent column '{agent}'")

    work = df[[pair, agent]].copy()
    work.columns = ["subject_verb", "by_agent"]
    work = work.drop_duplicates().reset_index(drop=True)

    if args.n != "all":
        work = work.sample(n=min(int(args.n), len(work)), random_state=args.seed)

    # stable anonymous id so the two sheets can be realigned after coding
    work["item_id"] = [hashlib.sha1(f"{a}|{b}".encode()).hexdigest()[:8]
                       for a, b in zip(work.subject_verb, work.by_agent)]
    work = work.sample(frac=1, random_state=args.seed).reset_index(drop=True)

    sheet = work[["item_id", "subject_verb", "by_agent"]].copy()
    for c in ("include", "animacy", "category", "valence", "notes"):
        sheet[c] = ""
    sheet.to_csv("coding_sheet.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    key = work[["item_id", "subject_verb", "by_agent"]].copy()
    for c in ("include", "animacy", "category", "valence"):
        key[c] = ""
    key.to_csv("coding_key.csv", index=False)

    Path("codebook.md").write_text(CODEBOOK, encoding="utf-8")
    print(f"coding_sheet.csv  {len(sheet)} items, shuffled, no labels -> give this to the second coder")
    print(f"coding_key.csv    same items -> fill in with YOUR codings")
    print(f"codebook.md       give this to the second coder as well")


if __name__ == "__main__":
    main()
