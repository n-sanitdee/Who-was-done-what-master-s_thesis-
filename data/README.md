# Derived data

Extracted from the corpora, not the corpora themselves. Short subject–verb pairs and
by-agent phrases are derived data, not substantial reproduction of the source text.

## `by_agents_ukraine.tsv`

Every passive construction in the Ukraine War corpus that retains a by-agent phrase:
modifier of the subject, the subject–verb pair, and the agent phrase. 168 rows, 167
unique on (subject_verb, by_agent) — `Urey_captured by_Russian_forces` appears twice,
differing only in modifier.

The thesis reports 165 by-agent pairs and 159 after excluding six circumstantial
by-phrases. The two-row gap is a de-duplication judgement, not missing data; the
circumstantial exclusions are visible in the file (`by_geography`, `by_propaganda`,
`by_minimum_number_days` and three others).

## What is not here yet

**Semantic codings.** Animacy, verb valence and agent category were assigned by hand and
were never recorded per pair outside the Russia/Ukraine subset in thesis §5.3.2. They are
being re-coded against a written codebook with a second coder; see `coding/`. The coded
file will be added in a later release.

**Association-score tables.** Two spreadsheet generations survive and they disagree.
`Leipzig 2014.xlsx` holds all 60,973 pairs with a score column that reproduces
`(O − E)/√E` to 4×10⁻¹⁶, but its stored p-values do not match the thesis, and its
chi-squared column is `(O − E)²/E`, which is the square of that score rather than the
2×2 statistic described in thesis §4.2. A later sheet holds the filtered set whose
scores and p-values do match the published tables.

Rather than ship two mutually inconsistent tables, the scores should be regenerated from
the contingency cells with `association_scores.py`, which computes expected frequencies
from the marginals and reports z, t and chi-squared side by side. That is the reproducible
path, and it is why that script exists.
