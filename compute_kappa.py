#!/usr/bin/env python3
"""Cohen's kappa between two coders, per variable.

    python3 compute_kappa.py coding_key.csv coding_sheet_returned.csv

Reports observed agreement, chance agreement, kappa with a bootstrap confidence
interval, per-category agreement, and every disagreement so you can adjudicate.
No sklearn required.
"""
import argparse
import random
from collections import Counter

import pandas as pd

VARIABLES = ["include", "animacy", "valence", "category"]

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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("coder1", help="your codings (coding_key.csv)")
    ap.add_argument("coder2", help="second coder's returned sheet")
    ap.add_argument("--no-ci", action="store_true")
    args = ap.parse_args()

    d1 = pd.read_csv(args.coder1).set_index("item_id")
    d2 = pd.read_csv(args.coder2).set_index("item_id")
    shared = [i for i in d1.index if i in d2.index]
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
