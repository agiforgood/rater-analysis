# Rater Analysis Project

Counseling/coaching evaluation dataset — therapist-parent dialogs paired with observer-rated assessment questionnaires measuring empathy, alliance, and positive regard.

## Data Files

- `问卷对话内容0305.csv` — Coach-parent dialog transcripts (14 scenarios)
- `问卷内容.csv` — Questionnaire definitions (TES empathy, unconditional positive regard, WAI alliance)
- `问卷0305.csv` — Rater scores/responses (36 raters, 20 dialogs, 3 dimensions)

## Data Flow

```
问卷对话内容0305 (dialogs) → evaluated using → 问卷内容 (rating scales) → producing → 问卷0305 (scores)
```

## Scripts

- `rater_agreement.py` — Inter-rater agreement analysis (ICC, pairwise distances, outlier detection)
- `question_divergence.py` — Per-question divergence, reverse-item effects, agreement clusters
- `analysis_centered_avg.py` — Rater-centered averaging vs raw averages
- `analysis_mfrm.py` — Many-Facet Rasch Model (fair scores, variance decomposition)
- `analysis_bayesian.py` — Hierarchical Bayesian model (quality estimates with credible intervals)

## Analysis Reports

- `analysis_summary_2026-03-07.md` — **Master summary** of all findings
- `analysis_rater_agreement_2026-03-07.md` — Initial ICC & rater bias
- `analysis_question_divergence_2026-03-07.md` — Per-question divergence & clusters
- `analysis_centered_averaging_2026-03-07.md` — Rater-centered averaging
- `analysis_mfrm_2026-03-07.md` — Many-Facet Rasch Model
- `analysis_bayesian_2026-03-07.md` — Hierarchical Bayesian model
- `analysis_exploratory_2026-03-07.md` — Ad-hoc investigations (item12, per-dialog ICC, bimodality)
- `feedback_rating_study_2026-03-07.md` — Honest feedback on study design
- `next_round_recommendations_2026-03-07.md` — Recommendations, pilot protocol, revised rubric template

## Analysis Convention

**Every time an analysis is run, output the results into a Markdown file** (e.g., `analysis_<topic>_<date>.md`) for future reference. This ensures findings are preserved and reviewable without re-running scripts.
