# Computes expected frequencies and association scores from the contingency cells
# produced by observed_freq.py.
#
# This step was previously done outside version control, which meant the scores
# reported in the thesis could not be reproduced from this repository alone.
#
# Input : output of observed_freq.py, tab-delimited, with columns
#         Subject_Verb_Pairs, s, v, O(sy_vy), O(sy_vn), O(sn_vy), O(sn_vn)
# Output: the same rows plus E11, z-score, t-score, chi-squared, and a retained flag.

import argparse
import numpy as np
import pandas as pd

# p < 0.05 against a t-distribution with df = 1 is exactly this score. The thesis
# filter is stated as p < 0.05; it is equivalent to a threshold on the score, and
# reporting it this way avoids implying a significance test the data cannot support.
SCORE_THRESHOLD = 12.7062


def score_table(df, min_freq):
    o11 = df["O(sy_vy)"].astype(float)
    o12 = df["O(sy_vn)"].astype(float)
    o21 = df["O(sn_vy)"].astype(float)
    o22 = df["O(sn_vn)"].astype(float)

    n = o11 + o12 + o21 + o22          # equals the corpus pair total for every row
    r1, r2 = o11 + o12, o21 + o22      # row marginals
    c1, c2 = o11 + o21, o12 + o22      # column marginals

    # Standard expected frequencies. Note these sum to their marginals by
    # construction; the worked example in the thesis (Table 4) does not, so the
    # E21/E22 values printed there should be rechecked against these.
    e11, e12 = r1 * c1 / n, r1 * c2 / n
    e21, e22 = r2 * c1 / n, r2 * c2 / n

    out = df.copy()
    out["E11"] = e11
    out["E12"], out["E21"], out["E22"] = e12, e21, e22

    # z-score: (O − E) / sqrt(E). This is the measure the thesis reports as "t-score".
    out["z_score"] = (o11 - e11) / np.sqrt(e11)

    # t-score: (O − E) / sqrt(O). Evert (2008) — damps the low-frequency bias of z
    # when E < 1, which is most pairs in a corpus this size.
    out["t_score"] = (o11 - e11) / np.sqrt(o11)

    # Chi-squared as computed in the thesis: N(O11 − E11)^2 / (E11 · E22).
    out["chi_squared"] = n * (o11 - e11) ** 2 / (e11 * e22)

    out["retained"] = (o11 > min_freq) & (out["z_score"] > SCORE_THRESHOLD)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("infile", help="output of observed_freq.py")
    ap.add_argument("-o", "--outfile", default="association_scores.txt")
    ap.add_argument("--min-freq", type=int, default=2,
                    help="minimum O11; 2 for the Ukraine War corpus, 15 for Leipzig")
    ap.add_argument("--measure", choices=["z", "t"], default="z",
                    help="which score the retained flag is based on (default: z, "
                         "matching the thesis)")
    args = ap.parse_args()

    df = pd.read_csv(args.infile, sep="\t")
    out = score_table(df, args.min_freq)
    if args.measure == "t":
        out["retained"] = (out["O(sy_vy)"] > args.min_freq) & (out["t_score"] > SCORE_THRESHOLD)

    out.to_csv(args.outfile, sep="\t", index=False, float_format="%.6f")
    print(f"{len(out)} pairs scored, {int(out['retained'].sum())} retained "
          f"(O11 > {args.min_freq}, {args.measure}-score > {SCORE_THRESHOLD}) "
          f"-> {args.outfile}")


if __name__ == "__main__":
    main()
