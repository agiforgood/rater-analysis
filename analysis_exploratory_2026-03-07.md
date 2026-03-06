# Exploratory Analyses

**Date:** 2026-03-07

Captures ad-hoc investigations done during the analysis session.

---

## 1. Item12 Score Distribution Deep-Dive

**Item:** item12 — "来访者相信他们处理其问题的方式是正确的" (Correct approach)
**Context:** Best ICC (0.097) of all questions — chosen for closer inspection.

### Overall Distribution (N=721, 36 raters, 20 dialogs)

| Score | Count | Pct |
|-------|-------|-----|
| 1 | 6 | 0.8% |
| 2 | 16 | 2.2% |
| 3 | 70 | 9.7% |
| 4 | 245 | 34.0% |
| 5 | 187 | 25.9% |
| 6 | 156 | 21.6% |
| 7 | 41 | 5.7% |

Mean = 4.70, Std = 1.19. Left-skewed, mode at 4.

### Per-Rater Baselines

- Most lenient: User 189 (mean 6.65) — almost always gives 6–7
- Most strict: User 562 (mean 3.25) — almost always gives 3–4
- Gap: **3.4 points** on a 7-point scale
- User 465: mean = 4.00, std = 0.00 — gives exactly 4 on every dialog (zero differentiation)

### Most Disagreed Dialogs

| Dialog | Mean | Std | Min | Max | Range |
|--------|------|-----|-----|-----|-------|
| 24 | 4.86 | 1.57 | 1 | 7 | 6 |
| 17 | 4.58 | 1.44 | 1 | 7 | 6 |
| 6 | 4.47 | 1.32 | 1 | 7 | 6 |
| 1 | 4.78 | 1.27 | 1 | 7 | 6 |

### Most Agreed Dialogs

| Dialog | Mean | Std | Min | Max | Range |
|--------|------|-----|-----|-----|-------|
| 11 | 5.03 | 0.88 | 4 | 7 | 3 |
| 9 | 4.81 | 0.89 | 3 | 7 | 4 |
| 10 | 5.14 | 0.90 | 4 | 7 | 3 |

**Takeaway:** Even the "best" question shows a 3.4-point rater baseline gap. The divergence is primarily about rater calibration, not question ambiguity.

---

## 2. Per-Dialog ICC Analysis

**Question:** Which dialogs produce the most rater agreement (across questions within each dialog)?

**Method:** For each (dialog, dimension), build a rater × question matrix and compute ICC(2,1).

### Top Dialogs by ICC

| Dialog | Dimension | ICC |
|--------|-----------|-----|
| 10 | WAI | 0.405 |
| 2 | WAI | 0.369 |
| 4 | WAI | 0.344 |
| 11 | WAI | 0.336 |
| 3 | WAI | 0.282 |

### Key Finding: Dimension Matters More Than Dialog

- **All top ICC dialogs are WAI.** The best WAI dialog (0.405) is 7x better than the best TES dialog (0.057).
- **TES ICC is near zero for every dialog** (0.003–0.057). Raters cannot agree on the relative empathy profile of any dialog.
- **Same dialog, different scales:** Dialog 10 gets ICC 0.405 on WAI but 0.021 on TES. Same raters, same conversation, 20x difference.
- **无条件积极关注 (positive regard):** ICC = NaN for all dialogs because it has only 1 question (ICC needs ≥2 items).

**Interpretation:** WAI items (goal agreement, trust, problem-solving approach) are behaviorally observable in transcripts. TES items (warmth, resonance, attunement) require subjective emotional inference that raters can't do consistently from text.

---

## 3. Bimodality Check

**Question:** Are score distributions unimodal (averaging is fine) or bimodal (averaging masks genuine splits)?

**Method:** Computed bimodality coefficient (BC > 0.555 suggests bimodality) and polarization index for all 440 (dialog, question) combinations.

### Result: Bimodality is Rare

- **8 out of 440** cases (1.8%) show bimodal patterns
- **432 out of 440** (98.2%) are unimodal — averaging is appropriate

### The 8 Bimodal Cases

| Dialog | Question | Dimension | BC | Pattern |
|--------|----------|-----------|-----|---------|
| 24 | positive_regard_level | 积极关注 | 0.61 | Split high/low |
| 24 | q6 | TES | 0.60 | Cluster at 1–2 and 5–7 |
| 18 | item4 | WAI | 0.58 | Reverse-item confusion |
| 24 | q7 | TES | 0.58 | Cluster at 1–2 and 5–7 |
| 2 | item4 | WAI | 0.57 | 10 raters gave 1, 3 gave 7 |
| 24 | item3 | WAI | 0.57 | Split |
| 13 | item12 | WAI | 0.57 | Mild split |
| 24 | q5 | TES | 0.56 | Cluster at 1–2 and 5–7 |

### Patterns

- **Dialog 24 appears 5 times** — it's the most polarizing conversation
- **Reverse-worded items (item4)** appear twice — interpretation confusion creates artificial bimodality
- For these specific cases, median + IQR would be more appropriate than mean

**Takeaway:** For 98% of cases, averaging is fine. Bimodality is concentrated in dialog 24 (inherently ambiguous) and reverse-worded items (design flaw).

---

## 4. ICC(2,k) — Reliability of Averaged Scores

**Question:** If individual rater ICC is poor (0.02–0.10), does averaging 36 raters produce usable reliability?

**Method:** Spearman-Brown formula: ICC(2,k) = k × ICC(2,1) / [1 + (k−1) × ICC(2,1)]

### Results with k=36 Raters

| Question Group | ICC(2,1) Range | ICC(2,36) Range | Quality |
|----------------|----------------|-----------------|---------|
| WAI items (best) | 0.07–0.10 | **0.73–0.80** | Good |
| Positive regard | 0.06 | **0.70** | Moderate |
| TES items (mixed) | 0.02–0.05 | **0.42–0.67** | Poor–Moderate |

### Minimum Raters Needed for ICC(2,k) > 0.5

| Question type | ICC(2,1) | Raters needed |
|---------------|----------|---------------|
| Best (item12) | 0.097 | ~10 |
| Median | 0.050 | ~20 |
| Worst (q2) | 0.020 | ~50 |

**Takeaway:** Averaging 36 raters gives reliable scores for WAI (good) and borderline for TES (some moderate, some still poor). The group mean is the signal; individual scores are noise.
