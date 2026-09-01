#!/usr/bin/env python3
"""Inter-coder reliability, per variable, for two or more coders.

    python3 compute_kappa.py coder_a.csv coder_b.csv [coder_c.csv ...]

With two files: Cohen's kappa, a bootstrap confidence interval, per-category
agreement, and every disagreement so you can adjudicate.

With three or more: Fleiss' kappa across all coders, plus Cohen's kappa for each
pair so you can see whether one coder is the outlier, and the items where the
panel splits. No sklearn required.
"""
import argparse
import random
from collections import Counter

import pandas as pd

VARIABLES = ["include", "animacy", "category", "valence"]

# Landis & Koch (1977). Content analysis conventionally wants >= .80 for firm
# conclusions and >= .67 for tentative ones (Krippendorff).
def band(k):
    if k < 0:    return "poor — worse than chance"
    if k < .21:  return "slight"
    if k < .41:  return "fair"
    if k < .61:  return "moderate"
    if k < .81:  return "substantial"
    return "almost perfect"


def kappa(a, b):
    """Cohen's kappa for two equal-length label sequences."""
    n = len(a)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    k = 1.0 if pe == 1 else (po - pe) / (1 - pe)
    return k, po, pe


def bootstrap_ci(a, b, iters=5000, seed=20260830):
    rng = random.Random(seed)
    n = len(a)
    ks = []
    for _ in range(iters):
        idx = [rng.randrange(n) for _ in range(n)]
        k, _, _ = kappa([a[i] for i in idx], [b[i] for i in idx])
        if k == k:
            ks.append(k)
    ks.sort()
    if not ks:
        return float("nan"), float("nan")
    return ks[int(.025 * len(ks))], ks[int(.975 * len(ks))]


def fleiss(rows):
    """Fleiss' kappa. rows = list of label-lists, one list per item."""
    rows = [r for r in rows if len(r) > 1]
    if not rows:
        return float("nan")
    n = len(rows[0])
    if any(len(r) != n for r in rows):
        return float("nan")                      # unequal raters per item
    cats = sorted({v for r in rows for v in r})
    N = len(rows)
    P = []
    for r in rows:
        c = Counter(r)
        P.append((sum(v * v for v in c.values()) - n) / (n * (n - 1)))
    pj = [sum(r.count(c) for r in rows) / (N * n) for c in cats]
    Pbar = sum(P) / N
    Pe = sum(p * p for p in pj)
    return 1.0 if Pe == 1 else (Pbar - Pe) / (1 - Pe)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("coders", nargs="+", help="two or more returned coding files")
    ap.add_argument("--no-ci", action="store_true")
    args = ap.parse_args()

    frames = [(f, pd.read_csv(f).set_index("item_id")) for f in args.coders]
    if len(frames) < 2:
        raise SystemExit("need at least two coding files")

    shared = set(frames[0][1].index)
    for _, d in frames[1:]:
        shared &= set(d.index)
    shared = [i for i in frames[0][1].index if i in shared]

    if len(frames) > 2:
        print(f"{len(frames)} coders, {len(shared)} items coded by all\n")
        for var in VARIABLES:
            if any(var not in d.columns for _, d in frames):
                continue
            rows, keep = [], []
            for i in shared:
                vals = [str(d.at[i, var]).strip().lower() for _, d in frames]
                if all(v and v != "nan" for v in vals):
                    rows.append(vals); keep.append(i)
            if not rows:
                continue
            print(f"=== {var}   (n = {len(rows)}, {len(frames)} coders)")
            print(f"    Fleiss' kappa       {fleiss(rows):.3f}   {band(fleiss(rows))}")
            print("    pairwise Cohen's kappa:")
            for a in range(len(frames)):
                for b in range(a + 1, len(frames)):
                    ka, _, _ = kappa([r[a] for r in rows], [r[b] for r in rows])
                    na = frames[a][0].split("/")[-1][:18]
                    nb = frames[b][0].split("/")[-1][:18]
                    print(f"      {na:<20} vs {nb:<20} {ka:.3f}")
            split = [(i, r) for i, r in zip(keep, rows) if len(set(r)) > 1]
            print(f"    {len(split)} item(s) where the panel does not agree")
            for i, r in split[:10]:
                sv = frames[0][1].at[i, "subject_verb"] if "subject_verb" in frames[0][1].columns else i
                print(f"      {sv}   {' / '.join(r)}")
            if len(split) > 10:
                print(f"      ... and {len(split) - 10} more")
            print()
        return

    (_, d1), (_, d2) = frames
    print(f"{len(shared)} items coded by both\n")

    for var in VARIABLES:
        if var not in d1.columns or var not in d2.columns:
            continue
        pairs = [(str(d1.at[i, var]).strip().lower(), str(d2.at[i, var]).strip().lower())
                 for i in shared]
        # rows either coder excluded carry no downstream codings; kappa on
        # `include` is computed over everything, the rest only over rows both kept
        if var != "include":
            keep = [str(d1.at[i, "include"]).strip().lower() != "no" and
                    str(d2.at[i, "include"]).strip().lower() != "no"
                    for i in shared] if "include" in d1.columns and "include" in d2.columns \
                   else [True] * len(shared)
            pairs = [pr for pr, k in zip(pairs, keep) if k]
        pairs = [(a, b) for a, b in pairs if a and b and a != "nan" and b != "nan"]
        if not pairs:
            print(f"— {var}: no coded values\n")
            continue
        a, b = [p[0] for p in pairs], [p[1] for p in pairs]
        k, po, pe = kappa(a, b)

        print(f"=== {var}   (n = {len(pairs)}, {len(set(a) | set(b))} categories used)")
        print(f"    observed agreement  {po:.3f}")
        print(f"    chance agreement    {pe:.3f}")
        line = f"    Cohen's kappa       {k:.3f}   {band(k)}"
        if not args.no_ci:
            lo, hi = bootstrap_ci(a, b)
            line += f"   95% CI [{lo:.3f}, {hi:.3f}]"
        print(line)

        # per-category, one-vs-rest — shows which distinctions are unstable
        cats = sorted(set(a) | set(b))
        if len(cats) > 2:
            print("    per category (one-vs-rest kappa):")
            for c in cats:
                kc, _, _ = kappa([x == c for x in a], [y == c for y in b])
                n_c = sum(x == c for x in a)
                flag = "   <-- weak" if kc == kc and kc < .6 else ""
                print(f"      {c:<22} n={n_c:<4} kappa={kc:.3f}{flag}")

        dis = [(i, x, y) for i, (x, y) in zip(shared, pairs) if x != y]
        if dis:
            print(f"    {len(dis)} disagreement(s) to adjudicate:")
            for i, x, y in dis[:15]:
                sv = d1.at[i, "subject_verb"] if "subject_verb" in d1.columns else i
                ag = d1.at[i, "by_agent"] if "by_agent" in d1.columns else ""
                print(f"      {sv} {ag}".rstrip() + f"   you={x} / them={y}")
            if len(dis) > 15:
                print(f"      ... and {len(dis) - 15} more")
        print()


if __name__ == "__main__":
    main()
