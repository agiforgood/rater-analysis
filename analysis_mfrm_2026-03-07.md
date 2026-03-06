# Many-Facet Rasch Model (MFRM) Analysis Report

**Date**: 2026-03-07

**Data**: 15924 observations from 36 raters, 20 dialogs, 22 items across 3 dimensions

**Model**: score = mu + theta(dialog) - delta(rater) - beta(item)
- Grand mean (mu) = 4.6018
- RMSE = 1.0661

## Dialog Quality Ranking (Fair Scores)

Fair score = mu + theta (adjusted for rater severity and item difficulty)

| Rank | Dialog | Theta | Fair Score | Raw Avg | N Ratings |
|------|--------|-------|------------|---------|-----------|
| 1 | 10 | +0.512 | 5.114 | 5.114 | 792 |
| 2 | 2 | +0.334 | 4.936 | 4.936 | 792 |
| 3 | 3 | +0.308 | 4.910 | 4.907 | 810 |
| 4 | 4 | +0.214 | 4.816 | 4.816 | 792 |
| 5 | 1 | +0.172 | 4.774 | 4.774 | 792 |
| 6 | 11 | +0.133 | 4.735 | 4.735 | 792 |
| 7 | 7 | +0.093 | 4.694 | 4.694 | 792 |
| 8 | 24 | +0.087 | 4.689 | 4.690 | 810 |
| 9 | 19 | +0.070 | 4.672 | 4.678 | 804 |
| 10 | 9 | +0.060 | 4.662 | 4.662 | 792 |
| 11 | 8 | +0.038 | 4.640 | 4.640 | 792 |
| 12 | 5 | -0.099 | 4.503 | 4.503 | 792 |
| 13 | 6 | -0.119 | 4.482 | 4.482 | 792 |
| 14 | 13 | -0.133 | 4.468 | 4.468 | 792 |
| 15 | 17 | -0.144 | 4.457 | 4.467 | 801 |
| 16 | 12 | -0.151 | 4.451 | 4.479 | 819 |
| 17 | 15 | -0.190 | 4.412 | 4.412 | 792 |
| 18 | 16 | -0.242 | 4.360 | 4.360 | 792 |
| 19 | 18 | -0.463 | 4.139 | 4.139 | 792 |
| 20 | 14 | -0.482 | 4.120 | 4.120 | 792 |

## Rater Severity (delta)

Positive delta = more severe (gives lower scores); Negative = more lenient

| Rank | Rater | Severity | Mean Score | N Ratings |
|------|-------|----------|------------|-----------|
| 1 | 549 | +1.331 | 3.270 | 440 |
| 2 | 562 | +1.156 | 3.445 | 440 |
| 3 | 479 | +1.081 | 3.520 | 440 |
| 4 | 523 | +0.799 | 3.802 | 440 |
| 5 | 526 | +0.793 | 3.809 | 440 |
| 6 | 542 | +0.668 | 3.934 | 440 |
| 7 | 208 | +0.479 | 4.131 | 449 |
| 8 | 465 | +0.461 | 4.166 | 458 |
| 9 | 460 | +0.306 | 4.295 | 440 |
| 10 | 494 | +0.265 | 4.336 | 440 |
| 11 | 167 | +0.265 | 4.336 | 440 |
| 12 | 575 | +0.249 | 4.352 | 440 |
| 13 | 512 | +0.222 | 4.380 | 440 |
| 14 | 498 | +0.190 | 4.411 | 440 |
| 15 | 513 | +0.188 | 4.414 | 440 |
| 16 | 458 | +0.174 | 4.427 | 440 |
| 17 | 402 | +0.129 | 4.473 | 440 |
| 18 | 529 | +0.108 | 4.493 | 440 |
| 19 | 532 | +0.083 | 4.518 | 440 |
| 20 | 484 | +0.063 | 4.539 | 440 |
| 21 | 502 | +0.056 | 4.555 | 449 |
| 22 | 396 | -0.007 | 4.609 | 440 |
| 23 | 570 | -0.101 | 4.702 | 440 |
| 24 | 492 | -0.253 | 4.855 | 440 |
| 25 | 15 | -0.278 | 4.880 | 440 |
| 26 | 500 | -0.428 | 5.030 | 440 |
| 27 | 324 | -0.428 | 5.030 | 440 |
| 28 | 112 | -0.514 | 5.126 | 467 |
| 29 | 566 | -0.519 | 5.125 | 449 |
| 30 | 491 | -0.574 | 5.173 | 452 |
| 31 | 514 | -0.657 | 5.259 | 440 |
| 32 | 472 | -0.714 | 5.316 | 440 |
| 33 | 495 | -0.764 | 5.366 | 440 |
| 34 | 483 | -1.019 | 5.620 | 440 |
| 35 | 178 | -1.221 | 5.823 | 440 |
| 36 | 189 | -1.589 | 6.191 | 440 |

**Most severe rater**: Rater 549 (delta = +1.331, mean score = 3.270)
**Most lenient rater**: Rater 189 (delta = -1.589, mean score = 6.191)
**Severity range**: 2.920 (spread between most severe and most lenient)

## Item/Question Difficulty (beta)

Positive beta = harder (receives lower scores); Negative = easier

| Rank | Item | Dimension | Difficulty | Mean Score | N Ratings |
|------|------|-----------|------------|------------|-----------|
| 1 | item4 | 咨访同盟WAI-Obse... | +1.490 | 3.112 | 721 |
| 2 | item10 | 咨访同盟WAI-Obse... | +1.261 | 3.341 | 721 |
| 3 | positive_regard_level | 无条件积极关注 | +0.979 | 3.622 | 720 |
| 4 | item7 | 咨访同盟WAI-Obse... | +0.286 | 4.316 | 721 |
| 5 | item11 | 咨访同盟WAI-Obse... | +0.179 | 4.423 | 721 |
| 6 | item8 | 咨访同盟WAI-Obse... | +0.053 | 4.549 | 721 |
| 7 | item3 | 咨访同盟WAI-Obse... | -0.065 | 4.667 | 721 |
| 8 | item12 | 咨访同盟WAI-Obse... | -0.094 | 4.696 | 721 |
| 9 | item1 | 咨访同盟WAI-Obse... | -0.131 | 4.734 | 721 |
| 10 | item5 | 咨访同盟WAI-Obse... | -0.158 | 4.760 | 721 |
| 11 | q4 | 共情评估量表 (TES) | -0.169 | 4.772 | 728 |
| 12 | q5 | 共情评估量表 (TES) | -0.173 | 4.776 | 728 |
| 13 | q8 | 共情评估量表 (TES) | -0.202 | 4.805 | 728 |
| 14 | q7 | 共情评估量表 (TES) | -0.212 | 4.815 | 728 |
| 15 | item2 | 咨访同盟WAI-Obse... | -0.232 | 4.835 | 721 |
| 16 | item9 | 咨访同盟WAI-Obse... | -0.244 | 4.846 | 721 |
| 17 | item6 | 咨访同盟WAI-Obse... | -0.291 | 4.893 | 721 |
| 18 | q3 | 共情评估量表 (TES) | -0.318 | 4.920 | 728 |
| 19 | q2 | 共情评估量表 (TES) | -0.407 | 5.010 | 728 |
| 20 | q6 | 共情评估量表 (TES) | -0.477 | 5.080 | 728 |
| 21 | q1 | 共情评估量表 (TES) | -0.478 | 5.081 | 728 |
| 22 | q9 | 共情评估量表 (TES) | -0.599 | 5.202 | 728 |

**Hardest item**: item4 (beta = +1.490, dim = 咨访同盟WAI-Observer-Short)
**Easiest item**: q9 (beta = -0.599, dim = 共情评估量表 (TES))

## Per-Dimension Summary

### 共情评估量表 (TES)
- Items: q1, q2, q3, q4, q5, q6, q7, q8, q9
- Score range: 1 - 7
- Mean score: 4.940 (SD = 1.282)
- Top 3 dialogs: 10 (5.61), 3 (5.20), 1 (5.10)
- Bottom 3 dialogs: 16 (4.58), 14 (4.53), 18 (4.35)

### 无条件积极关注
- Items: positive_regard_level
- Score range: 1 - 5
- Mean score: 3.622 (SD = 1.011)
- Top 3 dialogs: 10 (4.17), 24 (3.97), 3 (3.89)
- Bottom 3 dialogs: 16 (3.19), 14 (3.14), 18 (3.06)

### 咨访同盟WAI-Observer-Short
- Items: item1, item10, item11, item12, item2, item3, item4, item5, item6, item7, item8, item9
- Score range: 1 - 7
- Mean score: 4.431 (SD = 1.403)
- Top 3 dialogs: 2 (4.92), 10 (4.82), 3 (4.76)
- Bottom 3 dialogs: 13 (4.17), 18 (4.07), 14 (3.89)

## Model Fit Summary
- R-squared: 0.4011 (40.1% of variance explained)
- RMSE: 1.0661
- Total SS: 30222.99, Residual SS: 18100.16

### Variance Decomposition of Facet Effects
- Dialog quality (theta): variance = 0.0607 (8.0%)
- Rater severity (delta): variance = 0.4135 (54.1%)
- Item difficulty (beta): variance = 0.2894 (37.9%)

---
*Generated by analysis_mfrm.py using iterative least-squares MFRM estimation.*