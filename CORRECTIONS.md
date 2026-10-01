# Corrections

Author's corrections to:

> Sanitdee, Natchanun (2024). *Who was done what? A parser-based study of passive voice
> constructions in media discourse on the Russo-Ukrainian War.* MA thesis, University of
> Helsinki. Helda: [http://hdl.handle.net/10138/585905](http://hdl.handle.net/10138/585905) · Zenodo: [10.5281/zenodo.14031334](https://doi.org/10.5281/zenodo.14031334)

Version 1.0, issued 1 October 2026. The deposited thesis is unchanged; this note records
errors found afterwards and gives the corrected values. Section and table numbers refer to
the deposited PDF, against which every figure was checked (the Helda and Zenodo copies are
identical in text and pagination); recomputed values use the extraction scripts and derived
data released in the thesis repository.

**Two items withdraw findings:** the decline in passive verb use (§1), and the choice of the
t-score together with the claim that the Leipzig pairs are more significant than the Ukraine
War pairs (§10). The rest correct reported numbers, labels, links and a worked example. The
by-agent findings (§5.3) are unaffected, and no coding or categorisation error was found.

---

## 1. The decline in passive verb use (§5.2.2.1, Figure 8) does not hold

**What the thesis says.** Figure 8 and the surrounding text report that both passive
sentences and passive verbs declined across 2014–2023, and read this as agreeing with
Seoane & Loureiro-Porto (2005, cited in Di Ferrante 2023).

**What is wrong.** Table 18's `# Pass. V.` column agrees with the passive-pair counts in
Table 19 for 2016–2020, to within 1, but is misextracted for **2014, 2015 and 2023**, where
it is off by 20,000 to 35,000:

| | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2023 |
|---|---|---|---|---|---|---|---|---|
| Table 18, `# Pass. V.` | 86,172 | 156,883 | 123,474 | 126,258 | 126,646 | 125,510 | 132,617 | 105,213 |
| Table 19, `# Pass. Pair` | 120,683 | 125,582 | 123,474 | 126,257 | 126,646 | 125,510 | 132,617 | 125,547 |

These three cells produce the downward slope. 2015 is too high early in the series and
2023 too low at its end; 2014, also too low, pulls the other way and only partly offsets
them.

**Corrected.** Recomputing each year from Table 19's pair counts over Table 2's word
counts gives:

| | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2023 |
|---|---|---|---|---|---|---|---|---|
| as published | 0.51 | 0.91 | 0.67 | 0.70 | 0.71 | 0.69 | 0.72 | 0.57 |
| corrected | 0.716 | 0.730 | 0.670 | 0.705 | 0.705 | 0.692 | 0.723 | 0.679 |

The slope falls from −0.0077 to −0.0027 points per year. **The passive-verb series is
flat, and the claim of a decline in passive verb use is withdrawn.**

**What survives.** The passive *sentence* series is unaffected — 18.69% in 2014 to 17.56%
in 2023, slope −0.10/yr — and the decline reported there stands. So do the short-passive
trend in §5.2.2.2, computed from Table 19, and the get-passive trend in §5.2.2.3, computed
from Table 20.

---

## 2. "Leipzig 2014/2023" names two different preparations

§3.1.2 describes three cleaning steps and reports that they leave "12 and 13 million
words" — but points to Table 2, which shows 16.9 and 18.5 million.

Table 2 reflects the first two steps only. Table 14 (570,512 sentences / 12,322,647
words for 2014; 625,932 / 13,224,845 for 2023) reflects all three, including the removal
of lines containing direct speech. Sentences present in Table 2 but not Table 14 average
24.4 words against 21.6 for those kept in 2014, and 23.0 against 21.1 in 2023, consistent
with quote-bearing news lines being longer.

§5.2.1 (the pair-level lookup) uses the fully cleaned version; §5.2.2 (Tables 18–20, the
eight-year series) uses the partially cleaned one. Both are internally consistent; the
error is that §3.1.2 describes one and cites the other.

## 3. "Passive pair" is used for two different quantities

Table 14's pair counts (Ukraine War 1,061; Leipzig 2014 60,973; Leipzig 2023 64,688) are
**distinct pairs**. Table 19's (Leipzig 2014 120,683; Leipzig 2023 125,547) are
**occurrences**. The text calls both "passive pairs". The two tables also count different
preparations of the Leipzig corpora (correction 2), so they cannot be compared row by row.

For the Ukraine War corpus, the pair-frequency table has 1,061 rows whose frequencies sum
to 1,330; it is available from the author on request.

## 4. Table 18's `%Pass. V.` column uses two denominators

§5.2.2.1 states that passive verbs are expressed as a percentage of total words. That
holds for the Leipzig rows (0.51 to 0.91, average 0.69), but the Ukraine War row divides by
total verbs, active plus passive: 1,473 / (8,909 + 1,473) = 14.19%. The column therefore
sets 0.69 beside 14.19. On the stated basis the Ukraine War figure is 0.86% of words.

The text compares a Leipzig average of 12.90% with the Ukraine War's 14.19%. Both are on
the verb denominator, so that comparison is like with like, but 12.90% does not appear in
Table 18, whose Leipzig average is 0.69%. The comparison with Di Ferrante (2023) that
follows uses the word denominator and is unaffected.

## 5. Russia/Russian as agent: the schema is computed on 35 of 37 clauses (§5.3.2)

Table 29 prints 37 clauses. The schema beneath it counts 35 (14 restrictive + 12 violent +
4 negative + 3 neutral + 2 positive), and all five percentages — and the 85.72% in the
interpretation — are computed on 35. Two clauses are uncategorised.

The corresponding Ukraine figures are correct: 10+9+8+3+2 = 32 matches Table 32, and
56.25% / 43.75% follow. Russia-as-modifier is also correct at 11 clauses and 72.72%.

## 6. Table 25 contains a duplicated row

`citizen_detained · by_pro_-_Russian_separatists_forces` is printed twice — 21 rows, 20
distinct. Table 26 is clean at 16. The §5.3.1 percentages use 21, so on distinct rows:
restrictive 10/20 = 50.00% (published 52.38%) and violent 3/20 = 15.00% (published
14.29%). The subset total is 36, not 37. The finding — violent predicates concentrating on
non-human agents, restrictive on human agents — is unaffected.

## 7. Two Average rows are miscalculated

| | published | correct |
|---|---|---|
| Table 2, mean sentences | 826,347 | 823,249 |
| Table 2, mean words | 17,829,303 | 17,914,504 |
| Table 2, mean words/sentence | 21.82 | 21.78 |
| Table 33, mean words | 210,737 | 210,070 |

Each correct value is the mean of the column above it, as in the thesis's other Average
rows; for words per sentence, total words over total sentences gives 21.76. Tables 18–20
print the correct Leipzig averages; only the two dataset tables are wrong.

## 8. Abstract corpus size

The abstract gives the Leipzig corpora as "17M". This is the eight-year average on Table
2's basis and reads against §3.1.2's "12 and 13 million" — see correction 2.

## 9. The links in Appendices 1 and 2 are dead

Appendix 1 (corpora) and Appendix 2 (source code) link to files at
`github.com/aminomewza/Who-was-done-what-master-s_thesis-`, each pinned to a specific
commit. The repository is now at
**https://github.com/n-sanitdee/Who-was-done-what-master-s_thesis-**, and the pinned commits
are no longer in it, so the old links return 404 even with the new account name.

## 10. The "t-score" is the z-score, and its p-values are not valid (§4.2.2)

**What the thesis says.** §4.2.2 adopts the t-score as its association measure, defines it
as (O − E)/√E, and supports the choice with Dennis (1965, cited in Evert 2004), Lijffijt et
al. (2016) and Evert et al. (2008). Each score is converted to a p-value, and pairs with
p < 0.05 and more than 2 occurrences (Ukraine War corpus) or 15 (Leipzig corpora) are
reported as significant.

**What is wrong.** (O − E)/√E is the z-score (Evert 2004); the t-score is (O − E)/√O. The
two rank pairs differently, so the sources cited for the t-score do not support the measure
actually used. The p-values come from a Student's t distribution with one degree of freedom
(`p_value_calculation_t-score.py`), which has no basis for either score, so they are not
valid p-values. Under that conversion p < 0.05 is the same as a score above 12.706:
"significant" in the thesis means a z-score above 12.706.

**What it changes.** In the Ukraine War corpus, 46 pairs occur more than twice:

| Rule | Pairs kept |
|---|---|
| thesis: z-score > 12.706 (Table 6) | 28 |
| t-score > 12.706 | 0 |
| t-score > 2 | 9 |

The two selections differ: four of the nine pairs kept by the t-score (*soldiers_killed*,
*civilians_killed*, *people_injured*, *person_killed*) are not among the 28. In the Leipzig
corpora the frequency floor already decides the result: all 127 pairs that occur more than
15 times in 2014 also pass under the t-score, so the choice of measure changes nothing there.

The effect on each analysis that uses the scores:

| Where | Analysis | Effect |
|---|---|---|
| §4.2.2; Table 5; Figures 2, 19 | the t-score as the most appropriate measure | **withdrawn** |
| §5.1.1; Tables 6, 7 | the 28 significant Ukraine War pairs and their category proportions | the selection depends on the measure. Under both, civilian subjects and harmful verbs dominate (in the t-score selection, 86% and 95% of occurrences), so that observation holds. Restrictive verbs (*operations_stopped*, *units_shut*, *urey_captured* and four others) appear only in the z-score selection, and the percentages in Table 7 hold only for it |
| §5.1.1.2, §5.2.1.2; Tables 8–11, 15, 16 | the filtered Leipzig pairs and their categories | unchanged for 2014; the 2023 scores were not preserved, but the same frequency floor applies |
| §5.1.1.3; Figures 4, 5 | category proportions compared across corpora | Leipzig side unchanged; Ukraine War side as for §5.1.1 |
| §5.2.1.2, §5.2.1.3, §5.2.2.1; Tables 17, 18, 56 | the Leipzig pairs as "more significant" than the Ukraine War pairs | **withdrawn**: the p-values are not valid, and z-scores grow with corpus size, so averages from a 170,000-word corpus and corpora of 12 to 18 million words cannot be compared |
| §5.4.1; Tables 33, 34 | filtered pairs in the Russian sources | read as for Table 6 (z-score above 12.706); not recomputed |

The by-agent analyses (§5.3, and §5.4.2, which by its own account drops the p-value filter),
the passive frequency series (§5.2.2) and the topic models do not use association scores and
are unaffected. Throughout, the tables' "t-score" columns are z-scores.

## 11. Table 4's expected frequencies belong to another pair (§4.2.1, §4.2.2)

Table 4, the contingency table for *sovereignty_threatened*, gives expected frequencies of
94.511 and 1,162.489 for the two cells where the subject is absent. Those are the values for
*people_killed*. From the table's own margins they are 4.985 and 1,321.015; as printed, the
four expected frequencies sum to 1,261 rather than 1,330. The chi-squared worked example in
§4.2.2 uses 1,162.489 and so gives 1,211.03; with the correct value it is about 1,063. The
scores in Table 6 match a recomputation from the released counts, so only the printed
example is affected.

---

## Not affected

Checked and found correct: Table 24 (category frequencies, word lists, percentages, total
158); Table 23 (semantic roles, 158 + 1 = 159); the subject and verb category percentages
in §5.1 and §5.4 (every column sums to 100); the passive sub-corpora statistics; and the
81.25% (13/16) non-human-to-violent figure in §5.3.1, verified clause by clause.

Table 20's be+get totals running 995 to 1,955 below Table 19's pair totals is **not** an
error: `passive_constructions_be_get.py` records a pair only when an `auxpass` dependent is
present, so passives without an auxiliary are excluded by design.
