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

**One item changes a stated finding (§1).** The rest are reported numbers, labels and
arithmetic in summary rows. None of them changes a conclusion, and no coding or
categorisation error was found.

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

---

## Not affected

Checked and found correct: Table 24 (category frequencies, word lists, percentages, total
158); Table 23 (semantic roles, 158 + 1 = 159); the subject and verb category percentages
in §5.1 and §5.4 (every column sums to 100); the skewness table; the passive sub-corpora
statistics; the association-measure method and worked example in §4.2; and the 81.25%
(13/16) non-human-to-violent figure in §5.3.1, verified clause by clause.

Table 20's be+get totals running 995 to 1,955 below Table 19's pair totals is **not** an
error: `passive_constructions_be_get.py` records a pair only when an `auxpass` dependent is
present, so passives without an auxiliary are excluded by design.
