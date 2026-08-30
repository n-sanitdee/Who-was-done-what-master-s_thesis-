#!/usr/bin/env python3
"""Table 6 of the article: verb class by agent animacy, over ALL coded by-agents.

    python3 crosstab_animacy_valence.py coding_key_complete.csv

The thesis reports this cross-tabulation over six frequent agent lemmas (n=37).
Run over the full coded set it becomes a result rather than an illustration.
Reports the table, row percentages, and a chi-squared test with Fisher's exact
as a fallback when expected counts are small.
"""
import argparse
import math
from collections import Counter

import pandas as pd


def chi2_2xk(table):
    """Pearson chi-squared on a 2xk contingency table. Returns (chi2, df, min_expected)."""
    rows = len(table)
    cols = len(table[0])
    n = sum(sum(r) for r in table)
    if n == 0:
        return float("nan"), 0, 0
    rt = [sum(r) for r in table]
    ct = [sum(table[i][j] for i in range(rows)) for j in range(cols)]
    chi2, min_e = 0.0, float("inf")
    for i in range(rows):
        for j in range(cols):
            e = rt[i] * ct[j] / n
            min_e = min(min_e, e)
            if e > 0:
                chi2 += (table[i][j] - e) ** 2 / e
    return chi2, (rows - 1) * (cols - 1), min_e


def chi2_sf(x, df):
    """Upper tail of the chi-squared distribution, no scipy needed."""
    if x <= 0:
        return 1.0
    if df == 1:
        return math.erfc(math.sqrt(x / 2))
    if df == 2:
        return math.exp(-x / 2)
    # Wilson–Hilferty normal approximation, adequate for reporting
    z = ((x / df) ** (1 / 3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df))
    return 0.5 * math.erfc(z / math.sqrt(2))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("coded", help="completed coding file with animacy + valence columns")
    ap.add_argument("--collapse", action="store_true",
                    help="collapse negative/neutral/positive into 'other', as the article reports it")
    args = ap.parse_args()

    df = pd.read_csv(args.coded)
    if "include" in df.columns:
        n0 = len(df)
        df = df[df["include"].astype(str).str.strip().str.lower() != "no"]
        print(f"\nexcluded as circumstantial: {n0 - len(df)}")
    df["animacy"] = df["animacy"].astype(str).str.strip().str.lower()
    df["valence"] = df["valence"].astype(str).str.strip().str.lower()
    df = df[df.animacy.isin(["human", "nonhuman"]) &
            ~df.valence.isin(["", "nan", "unclear"])]

    if args.collapse:
        df["valence"] = df["valence"].apply(
            lambda v: v if v in ("violent", "restrictive") else "other")
        order = ["violent", "restrictive", "other"]
    else:
        order = ["violent", "restrictive", "negative", "neutral", "positive"]
    order = [v for v in order if v in set(df.valence)]

    rows = ["nonhuman", "human"]
    table = [[int(((df.animacy == r) & (df.valence == c)).sum()) for c in order] for r in rows]

    w = max(12, max(len(c) for c in order) + 2)
    print(f"\nn = {len(df)} coded by-agents "
          f"(thesis reports this over 37, from six agent lemmas)\n")
    print(" " * 14 + "".join(f"{c:>{w}}" for c in order) + f"{'total':>9}")
    for name, row in zip(rows, table):
        tot = sum(row)
        cells = "".join(f"{v:>{w-7}} ({v/tot*100:4.1f}%)" if tot else f"{v:>{w}}" for v in row)
        print(f"  {name:<11}" + cells + f"{tot:>9}")

    chi2, dof, min_e = chi2_2xk(table)
    p = chi2_sf(chi2, dof)
    print(f"\n  chi2({dof}) = {chi2:.3f}, p = {p:.4g}, smallest expected count = {min_e:.2f}")
    if min_e < 5:
        print("  Smallest expected count is below 5 — report Fisher's exact instead.")
        print("  R: fisher.test(matrix(c(" +
              ", ".join(str(v) for row in zip(*table) for v in row) +
              f"), nrow=2))")
    print()


if __name__ == "__main__":
    main()
