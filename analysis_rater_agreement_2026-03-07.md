# Rater Agreement Analysis — 问卷0305

**Date:** 2026-03-07
**Script:** `rater_agreement.py`
**Dataset:** 36 raters, 20 dialogs, 3 dimensions (1–7 scale)

## Key Findings

### ICC (Inter-rater reliability) — Very Poor

ICC scores across all 3 dimensions are extremely low (0.04–0.09), indicating substantial rater disagreement. This is the headline result.

### Rater Spread

- **Most lenient:** User 189 (mean 6.19/7) — rates almost everything highly
- **Most strict:** User 549 (mean 3.27/7) — rates nearly everything low
- **Distribution:** 9 raters lean lenient, 6 lean strict, 21 relatively neutral

### Bias Direction

| Bias     | Count | Example Raters |
|----------|-------|----------------|
| Lenient  | 9     | User 189       |
| Strict   | 6     | User 549       |
| Neutral  | 21    | —              |

### Most Disagreed Dialogs

- **Dialog 24** and **Dialog 2** show the highest disagreement
- Dimensions: WAI (therapeutic alliance) and TES (empathy)
- Full 6-point score ranges across raters on these dialogs

### Pairwise Rater Distances

Most divergent rater pairs differ by ~3.5 points on average (on a 1–7 scale), e.g., Users 483 vs 549.

## Analysis Sections (from script output)

1. Overall stats
2. Per-rater summary (mean, std vs group)
3. ICC reliability
4. Per-dialog consensus
5. Pairwise distances
6. Outlier detection
7. Bias direction

## Implications

- The low ICC values suggest the rating rubrics may need calibration or rater training
- The wide spread between lenient and strict raters (~3 points) undermines comparability
- Dialog-specific disagreement (dialogs 24, 2) may indicate ambiguous scenarios worth reviewing
