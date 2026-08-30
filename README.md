# Who Was Done What?

Extraction and analysis code for a parser-based study of passive voice constructions in
media discourse on the Russo-Ukrainian War.

## Citation

Sanitdee, Natchanun. 2024. *Who Was Done What? A Parser-Based Study of Passive Voice
Constructions in Media Discourse on the Russo-Ukrainian War.* Master's thesis, University
of Helsinki. https://doi.org/10.5281/zenodo.14031334 ·
https://helda.helsinki.fi/items/c5c9840f-80da-4e21-937a-46fd4ac00797

## Source corpora are not distributed here

The four corpora used in the thesis — a keyword-seeded Ukraine War web corpus (170,834
words) and three URL-seeded corpora from tass.com, themoscowtimes.com and arctic.ru — are
verbatim news text in which the publishers hold copyright. They were removed from this
repository in August 2026 and are not redistributable.

**Rebuilding them.** All four were compiled with [SketchEngine](https://www.sketchengine.eu/).
The Ukraine War corpus used the seed terms *Russian-Ukrainian War*, *Russo-Ukrainian War*,
*Ukraine War* and *Russia's War in Ukraine*, with size and relevance set to larger and max
document size 15,000 kB; the three Russian-source corpora were built from URL seeds with
the same size settings. Cleaning removed HTML paragraph tags, bracketed reference markers
and leading carets.

The Leipzig News corpora (2014–2020, 2023) come from the
[Leipzig Corpora Collection](https://wortschatz.uni-leipzig.de/en/download/English) under
its own terms. Lines were dropped if numbered, under ten words, containing more than four
numerals, or containing direct speech.

## What the scripts do

**Extraction** — run first, over a cleaned corpus file.

| Script | Output |
|---|---|
| `passive_constructions.py` | passive subject–verb pairs via `nsubjpass` |
| `by_agents.py` | by-agent phrases via `agent` + `pobj`, with `amod`/`compound` modifiers |
| `passive_constructions_be_get.py` | the same, split by `auxpass` lemma into *be*- and *get*-passives |
| `active_construction.py` | active-voice counterparts |
| `proper_nouns.py` | proper-noun passive subjects |
| `passive_text.py` | passive-only sub-corpora, input to topic modelling |

**Counting and association**

| Script | Output |
|---|---|
| `frequencies.py` | pair frequencies within the passive set |
| `freq_whole.py` | component frequencies across the whole corpus |
| `observed_freq.py` | the four contingency cells per pair |
| `p_value_calculation_t-score.py` | *p*-values from association scores |
| `p_value_chi-squared.py` | *p*-values from chi-squared scores |
| `fisher_p-value.py` | Fisher's exact *p*-values |
| `cohen_sample_size.py` | Cohen's *w* and required sample size |

**Categorisation and topics**

| Script | Output |
|---|---|
| `group_word_emb.py` | semantic map (Word2Vec + PCA), used as a coding aid |
| `topic_modelling.py` | BERTopic over the passive sub-corpora |

## Reliability and the full cross-tabulation

| Script | Purpose |
|---|---|
| `make_coding_sheet.py` | builds a shuffled, unlabelled sheet for a second coder, plus the codebook |
| `compute_kappa.py` | Cohen's kappa per variable, bootstrap CI, per-category agreement, disagreement list |
| `crosstab_animacy_valence.py` | verb class by agent animacy over all coded agents, with a significance test |

Workflow: run `by_agents.py`, then `make_coding_sheet.py` on its output; code
`coding_key.csv` yourself and give `coding_sheet.csv` plus `codebook.md` to a second
coder; run `compute_kappa.py` on the two files; adjudicate disagreements; run
`crosstab_animacy_valence.py` on the settled codings.

## Known gaps

- **The association score is not computed here.** `observed_freq.py` emits the contingency
  cells; expected frequencies and the score itself were then calculated outside version
  control, and only the score-to-*p*-value step is scripted. A reader cannot currently
  reproduce the scores from this repository alone.
- **`p_value_calculation_t-score.py` uses `df = 1`.** That is correct for chi-squared on a
  2×2 table but not for this statistic, and it is why large scores return moderate
  *p*-values. Because *p* < 0.05 at df = 1 is exactly *score* > 12.7062, the threshold is
  monotone in the score and the retained pair sets are unaffected — but the quantity should
  be read as a score threshold, not a significance test.
- **The measure is the z-score.** `(O − E)/√E` is what Evert (2008) calls the z-score; the
  t-score substitutes *O* for *E* in the denominator.
- **Manual codings are not included.** Semantic categories, animacy and verb valence were
  assigned by hand and are not in this repository.

## Requirements

`spacy` with `en_core_web_trf`, `gensim`, `bertopic`, `scipy`, `statsmodels`, `pandas`,
`numpy`, `matplotlib`, `scikit-learn`.

## Licence

CC0 1.0 — applies to the code in this repository only.
