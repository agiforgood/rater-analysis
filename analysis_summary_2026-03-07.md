# Rater Analysis — Master Summary

**Date:** 2026-03-07
**Dataset:** 36 raters × 20 dialogs × 3 dimensions (TES empathy, positive regard, WAI alliance)

---

## Analysis Reports

| # | Report | Script | What it covers |
|---|--------|--------|----------------|
| 1 | `analysis_rater_agreement_2026-03-07.md` | `rater_agreement.py` | Overall ICC, rater bias, pairwise distances, outliers |
| 2 | `analysis_question_divergence_2026-03-07.md` | `question_divergence.py` | Per-question divergence, reverse-item effects, agreement clusters |
| 3 | `analysis_centered_averaging_2026-03-07.md` | `analysis_centered_avg.py` | Rater-centered averaging vs raw — ranking stability |
| 4 | `analysis_mfrm_2026-03-07.md` | `analysis_mfrm.py` | Many-Facet Rasch Model — fair scores, variance decomposition |
| 5 | `analysis_bayesian_2026-03-07.md` | `analysis_bayesian.py` | Hierarchical Bayesian model — quality estimates with credible intervals |
| 6 | `analysis_exploratory_2026-03-07.md` | (in-session) | Item12 deep-dive, per-dialog ICC, bimodality check, ICC(2,k) |

---

## Top-Level Findings

### 1. Rater bias dominates the data

MFRM variance decomposition:
- **Rater severity: 54%** of explained variance
- **Item difficulty: 38%**
- **Dialog quality: only 8%**

Rater means range from 3.27 to 6.19 on a 7-point scale (a 3-point spread). One rater gives exactly 4.00 on every dialog.

### 2. Despite this, dialog rankings are stable

All three methods (raw average, rater-centered, MFRM, Bayesian) produce **nearly identical rankings**. The balanced design (all raters rate all dialogs) neutralizes individual bias in the aggregate. Maximum rank shift from centering: 1 position.

### 3. Dialog quality estimates (Bayesian, with uncertainty)

| Rank | Dialog | Quality | 95% CI |
|------|--------|---------|--------|
| 1 | 10 | 5.20 | [5.14, 5.27] |
| 2 | 2 | 5.04 | [4.98, 5.10] |
| 3 | 3 | 5.02 | [4.96, 5.08] |
| 4 | 4 | 4.82 | — |
| 5 | 1 | 4.77 | — |
| ... | | | |
| 19 | 18 | 4.31 | [4.25, 4.37] |
| 20 | 14 | 4.29 | [4.23, 4.35] |

CI width ~0.13; 141 of 190 dialog pairs are significantly different.

### 4. TES (empathy) scale is unreliable from text

- TES ICC per dialog: 0.003–0.057 (near zero)
- WAI ICC per dialog: up to 0.405 (still poor but 10–20x better)
- Same raters, same dialogs — the difference is the construct, not the people
- Empathy facets (warmth, resonance, attunement) require subjective emotional inference that raters can't do consistently from transcripts

### 5. Reverse-worded items (WAI item4, item10) cause extra confusion

- +0.26 std more divergent than normal WAI items
- Appear in 2 of 8 bimodal cases
- Some raters interpret the scale direction differently

### 6. Bimodality is rare (1.8% of cases)

- 98% of (dialog, question) distributions are unimodal — averaging is appropriate
- The 8 bimodal cases cluster around dialog 24 (polarizing) and reverse-worded items

### 7. Two question clusters

**High agreement** (lower divergence): concrete, observable — concern, responsiveness, trust, goal agreement, professional confidence

**Low agreement** (higher divergence): subjective, emotional — warmth, acceptance, resonance, attunement, feeling understanding

---

## Recommendations for Future Rounds

1. **Calibrate raters** before scoring — do 2–3 example dialogs together, discuss, align
2. **Fix or drop TES** — it doesn't produce reliable scores from text. Either add behavioral anchors with transcript examples, or switch to a different measure
3. **Reword reverse items** (item4, item10) as positive statements, or add explicit instructions
4. **Add items to positive regard** — 1 question isn't enough for reliability analysis
5. **Add anchor examples** to the rubric for subjective questions (warmth, acceptance, attunement)
6. **Use Bayesian estimates with CIs** as the "intersubjective quality" scores — when CIs overlap, treat dialogs as equivalent
