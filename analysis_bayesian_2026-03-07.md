# Hierarchical Bayesian Analysis of Rater Scoring Data

Date: 2026-03-07

## Model Specification

```
score_ijk = mu + dialog_quality_i + rater_bias_j + question_effect_k + epsilon
```

- **Dialog quality**: random effect (empirical Bayes / BLUP)
- **Rater bias**: random intercept per rater
- **Question effect**: fixed effect (dummy-coded)
- **Estimation**: REML via statsmodels MixedLM

## Variance Components

| Component | Variance | % of Total |
|-----------|----------|------------|
| Rater | 0.4006 | 24.7% |
| Dialog | 0.4069 | 25.1% |
| Residual | 0.8145 | 50.2% |
| **Total** | **1.6220** | **100%** |

- ICC (dialog): 0.251
- ICC (rater): 0.247
- Grand mean (mu): 4.733

## Dialog Quality Rankings

Estimates are empirical Bayes (shrunken) estimates with 95% credible intervals.

| Rank | Dialog ID | Name | Quality | 95% CI | CI Width | Confidence | Raw Mean | N |
|------|-----------|------|---------|--------|----------|------------|----------|---|
| 1 | 57 | 10 | 5.203 | [5.14, 5.27] | 0.126 | HIGH | 5.114 | 792 |
| 2 | 65 | 2 | 5.039 | [4.98, 5.10] | 0.126 | HIGH | 4.936 | 792 |
| 3 | 64 | 3 | 5.019 | [4.96, 5.08] | 0.124 | HIGH | 4.907 | 810 |
| 4 | 63 | 4 | 4.929 | [4.87, 4.99] | 0.126 | HIGH | 4.816 | 792 |
| 5 | 66 | 1 | 4.891 | [4.83, 4.95] | 0.126 | HIGH | 4.774 | 792 |
| 6 | 56 | 11 | 4.855 | [4.79, 4.92] | 0.126 | HIGH | 4.735 | 792 |
| 7 | 47 | 24 | 4.822 | [4.76, 4.88] | 0.124 | HIGH | 4.690 | 810 |
| 8 | 60 | 7 | 4.818 | [4.76, 4.88] | 0.126 | HIGH | 4.694 | 792 |
| 9 | 48 | 19 | 4.799 | [4.74, 4.86] | 0.125 | HIGH | 4.678 | 804 |
| 10 | 58 | 9 | 4.788 | [4.73, 4.85] | 0.126 | HIGH | 4.662 | 792 |
| 11 | 59 | 8 | 4.769 | [4.71, 4.83] | 0.126 | HIGH | 4.640 | 792 |
| 12 | 62 | 5 | 4.642 | [4.58, 4.71] | 0.126 | HIGH | 4.503 | 792 |
| 13 | 61 | 6 | 4.624 | [4.56, 4.69] | 0.126 | HIGH | 4.482 | 792 |
| 14 | 54 | 13 | 4.611 | [4.55, 4.67] | 0.126 | HIGH | 4.468 | 792 |
| 15 | 50 | 17 | 4.602 | [4.54, 4.66] | 0.125 | HIGH | 4.467 | 801 |
| 16 | 55 | 12 | 4.576 | [4.51, 4.64] | 0.123 | HIGH | 4.479 | 819 |
| 17 | 52 | 15 | 4.559 | [4.50, 4.62] | 0.126 | HIGH | 4.412 | 792 |
| 18 | 51 | 16 | 4.512 | [4.45, 4.57] | 0.126 | HIGH | 4.360 | 792 |
| 19 | 49 | 18 | 4.309 | [4.25, 4.37] | 0.126 | HIGH | 4.139 | 792 |
| 20 | 53 | 14 | 4.292 | [4.23, 4.35] | 0.126 | HIGH | 4.120 | 792 |

### Interpretation

- **Best dialog**: 57 (name=10) with quality 5.203
- **Worst dialog**: 53 (name=14) with quality 4.292
- Quality range: 0.911 points

### Confidence Summary

- HIGH confidence (CI < 0.3): 20 dialogs
- MEDIUM confidence (0.3-0.5): 0 dialogs
- LOW confidence (CI >= 0.5): 0 dialogs

## Rater Bias Estimates

| Rater | Bias | Interpretation |
|-------|------|----------------|
| 549 | -1.261 | Strict (rates 1.3 pts lower) |
| 562 | -1.095 | Strict (rates 1.1 pts lower) |
| 479 | -1.024 | Strict (rates 1.0 pts lower) |
| 523 | -0.757 | Strict (rates 0.8 pts lower) |
| 526 | -0.751 | Strict (rates 0.8 pts lower) |
| 542 | -0.632 | Strict (rates 0.6 pts lower) |
| 208 | -0.432 | Strict (rates 0.4 pts lower) |
| 465 | -0.431 | Strict (rates 0.4 pts lower) |
| 460 | -0.290 | Near average |
| 494 | -0.251 | Near average |
| 167 | -0.251 | Near average |
| 575 | -0.236 | Near average |
| 512 | -0.210 | Near average |
| 498 | -0.180 | Near average |
| 513 | -0.178 | Near average |
| 458 | -0.165 | Near average |
| 402 | -0.122 | Near average |
| 529 | -0.103 | Near average |
| 532 | -0.079 | Near average |
| 484 | -0.059 | Near average |
| 502 | -0.057 | Near average |
| 396 | +0.007 | Near average |
| 570 | +0.096 | Near average |
| 492 | +0.240 | Near average |
| 15 | +0.264 | Near average |
| 324 | +0.406 | Lenient (rates 0.4 pts higher) |
| 500 | +0.406 | Lenient (rates 0.4 pts higher) |
| 112 | +0.453 | Lenient (rates 0.5 pts higher) |
| 566 | +0.494 | Lenient (rates 0.5 pts higher) |
| 491 | +0.547 | Lenient (rates 0.5 pts higher) |
| 514 | +0.623 | Lenient (rates 0.6 pts higher) |
| 472 | +0.677 | Lenient (rates 0.7 pts higher) |
| 495 | +0.724 | Lenient (rates 0.7 pts higher) |
| 483 | +0.966 | Lenient (rates 1.0 pts higher) |
| 178 | +1.157 | Lenient (rates 1.2 pts higher) |
| 189 | +1.506 | Lenient (rates 1.5 pts higher) |

- Rater bias std dev: 0.608
- Rater bias range: [-1.261, 1.506]

## Question/Item Effects

| Question | Dimension | Effect |
|----------|-----------|--------|
| q4 | TES | +0.037 |
| q5 | TES | +0.041 |
| q8 | TES | +0.070 |
| q7 | TES | +0.080 |
| q3 | TES | +0.185 |
| q2 | TES | +0.275 |
| q6 | TES | +0.345 |
| q1 | TES | +0.346 |
| q9 | TES | +0.467 |
| positive_regard_level | UPR | -1.111 |
| item4 | WAI | -1.621 |
| item10 | WAI | -1.393 |
| item7 | WAI | -0.417 |
| item11 | WAI | -0.311 |
| item8 | WAI | -0.184 |
| item3 | WAI | -0.067 |
| item12 | WAI | -0.037 |
| item1 | WAI | +0.000 |
| item5 | WAI | +0.026 |
| item2 | WAI | +0.101 |
| item9 | WAI | +0.112 |
| item6 | WAI | +0.160 |

## Significantly Different Dialog Pairs

Found 141 pairs with non-overlapping 95% CIs:

| Higher Dialog | Lower Dialog | Difference |
|--------------|--------------|------------|
| 57 (name=10) | 65 (name=2) | 0.163 |
| 57 (name=10) | 64 (name=3) | 0.184 |
| 57 (name=10) | 63 (name=4) | 0.273 |
| 57 (name=10) | 66 (name=1) | 0.311 |
| 57 (name=10) | 56 (name=11) | 0.347 |
| 57 (name=10) | 47 (name=24) | 0.381 |
| 57 (name=10) | 60 (name=7) | 0.384 |
| 57 (name=10) | 48 (name=19) | 0.403 |
| 57 (name=10) | 58 (name=9) | 0.414 |
| 57 (name=10) | 59 (name=8) | 0.434 |
| 57 (name=10) | 62 (name=5) | 0.560 |
| 57 (name=10) | 61 (name=6) | 0.579 |
| 57 (name=10) | 54 (name=13) | 0.591 |
| 57 (name=10) | 50 (name=17) | 0.601 |
| 57 (name=10) | 55 (name=12) | 0.626 |
| 57 (name=10) | 52 (name=15) | 0.643 |
| 57 (name=10) | 51 (name=16) | 0.691 |
| 57 (name=10) | 49 (name=18) | 0.893 |
| 57 (name=10) | 53 (name=14) | 0.911 |
| 65 (name=2) | 66 (name=1) | 0.148 |
| 65 (name=2) | 56 (name=11) | 0.184 |
| 65 (name=2) | 47 (name=24) | 0.218 |
| 65 (name=2) | 60 (name=7) | 0.221 |
| 65 (name=2) | 48 (name=19) | 0.240 |
| 65 (name=2) | 58 (name=9) | 0.251 |
| 65 (name=2) | 59 (name=8) | 0.271 |
| 65 (name=2) | 62 (name=5) | 0.397 |
| 65 (name=2) | 61 (name=6) | 0.415 |
| 65 (name=2) | 54 (name=13) | 0.428 |
| 65 (name=2) | 50 (name=17) | 0.437 |
| 65 (name=2) | 55 (name=12) | 0.463 |
| 65 (name=2) | 52 (name=15) | 0.480 |
| 65 (name=2) | 51 (name=16) | 0.528 |
| 65 (name=2) | 49 (name=18) | 0.730 |
| 65 (name=2) | 53 (name=14) | 0.748 |
| 64 (name=3) | 66 (name=1) | 0.128 |
| 64 (name=3) | 56 (name=11) | 0.163 |
| 64 (name=3) | 47 (name=24) | 0.197 |
| 64 (name=3) | 60 (name=7) | 0.201 |
| 64 (name=3) | 48 (name=19) | 0.219 |
| 64 (name=3) | 58 (name=9) | 0.231 |
| 64 (name=3) | 59 (name=8) | 0.250 |
| 64 (name=3) | 62 (name=5) | 0.376 |
| 64 (name=3) | 61 (name=6) | 0.395 |
| 64 (name=3) | 54 (name=13) | 0.408 |
| 64 (name=3) | 50 (name=17) | 0.417 |
| 64 (name=3) | 55 (name=12) | 0.442 |
| 64 (name=3) | 52 (name=15) | 0.460 |
| 64 (name=3) | 51 (name=16) | 0.507 |
| 64 (name=3) | 49 (name=18) | 0.710 |
| 64 (name=3) | 53 (name=14) | 0.727 |
| 63 (name=4) | 48 (name=19) | 0.130 |
| 63 (name=4) | 58 (name=9) | 0.141 |
| 63 (name=4) | 59 (name=8) | 0.161 |
| 63 (name=4) | 62 (name=5) | 0.287 |
| 63 (name=4) | 61 (name=6) | 0.306 |
| 63 (name=4) | 54 (name=13) | 0.318 |
| 63 (name=4) | 50 (name=17) | 0.328 |
| 63 (name=4) | 55 (name=12) | 0.353 |
| 63 (name=4) | 52 (name=15) | 0.370 |
| 63 (name=4) | 51 (name=16) | 0.418 |
| 63 (name=4) | 49 (name=18) | 0.620 |
| 63 (name=4) | 53 (name=14) | 0.638 |
| 66 (name=1) | 62 (name=5) | 0.249 |
| 66 (name=1) | 61 (name=6) | 0.267 |
| 66 (name=1) | 54 (name=13) | 0.280 |
| 66 (name=1) | 50 (name=17) | 0.289 |
| 66 (name=1) | 55 (name=12) | 0.315 |
| 66 (name=1) | 52 (name=15) | 0.332 |
| 66 (name=1) | 51 (name=16) | 0.380 |
| 66 (name=1) | 49 (name=18) | 0.582 |
| 66 (name=1) | 53 (name=14) | 0.599 |
| 56 (name=11) | 62 (name=5) | 0.213 |
| 56 (name=11) | 61 (name=6) | 0.231 |
| 56 (name=11) | 54 (name=13) | 0.244 |
| 56 (name=11) | 50 (name=17) | 0.253 |
| 56 (name=11) | 55 (name=12) | 0.279 |
| 56 (name=11) | 52 (name=15) | 0.296 |
| 56 (name=11) | 51 (name=16) | 0.344 |
| 56 (name=11) | 49 (name=18) | 0.546 |
| 56 (name=11) | 53 (name=14) | 0.564 |
| 47 (name=24) | 62 (name=5) | 0.179 |
| 47 (name=24) | 61 (name=6) | 0.198 |
| 47 (name=24) | 54 (name=13) | 0.210 |
| 47 (name=24) | 50 (name=17) | 0.220 |
| 47 (name=24) | 55 (name=12) | 0.245 |
| 47 (name=24) | 52 (name=15) | 0.263 |
| 47 (name=24) | 51 (name=16) | 0.310 |
| 47 (name=24) | 49 (name=18) | 0.513 |
| 47 (name=24) | 53 (name=14) | 0.530 |
| 60 (name=7) | 62 (name=5) | 0.176 |
| 60 (name=7) | 61 (name=6) | 0.194 |
| 60 (name=7) | 54 (name=13) | 0.207 |
| 60 (name=7) | 50 (name=17) | 0.216 |
| 60 (name=7) | 55 (name=12) | 0.242 |
| 60 (name=7) | 52 (name=15) | 0.259 |
| 60 (name=7) | 51 (name=16) | 0.307 |
| 60 (name=7) | 49 (name=18) | 0.509 |
| 60 (name=7) | 53 (name=14) | 0.527 |
| 48 (name=19) | 62 (name=5) | 0.157 |
| 48 (name=19) | 61 (name=6) | 0.175 |
| 48 (name=19) | 54 (name=13) | 0.188 |
| 48 (name=19) | 50 (name=17) | 0.197 |
| 48 (name=19) | 55 (name=12) | 0.223 |
| 48 (name=19) | 52 (name=15) | 0.240 |
| 48 (name=19) | 51 (name=16) | 0.288 |
| 48 (name=19) | 49 (name=18) | 0.490 |
| 48 (name=19) | 53 (name=14) | 0.508 |
| 58 (name=9) | 62 (name=5) | 0.146 |
| 58 (name=9) | 61 (name=6) | 0.164 |
| 58 (name=9) | 54 (name=13) | 0.177 |
| 58 (name=9) | 50 (name=17) | 0.186 |
| 58 (name=9) | 55 (name=12) | 0.212 |
| 58 (name=9) | 52 (name=15) | 0.229 |
| 58 (name=9) | 51 (name=16) | 0.277 |
| 58 (name=9) | 49 (name=18) | 0.479 |
| 58 (name=9) | 53 (name=14) | 0.496 |
| 59 (name=8) | 62 (name=5) | 0.126 |
| 59 (name=8) | 61 (name=6) | 0.145 |
| 59 (name=8) | 54 (name=13) | 0.157 |
| 59 (name=8) | 50 (name=17) | 0.167 |
| 59 (name=8) | 55 (name=12) | 0.192 |
| 59 (name=8) | 52 (name=15) | 0.209 |
| 59 (name=8) | 51 (name=16) | 0.257 |
| 59 (name=8) | 49 (name=18) | 0.459 |
| 59 (name=8) | 53 (name=14) | 0.477 |
| 62 (name=5) | 51 (name=16) | 0.131 |
| 62 (name=5) | 49 (name=18) | 0.333 |
| 62 (name=5) | 53 (name=14) | 0.351 |
| 61 (name=6) | 49 (name=18) | 0.315 |
| 61 (name=6) | 53 (name=14) | 0.332 |
| 54 (name=13) | 49 (name=18) | 0.302 |
| 54 (name=13) | 53 (name=14) | 0.319 |
| 50 (name=17) | 49 (name=18) | 0.293 |
| 50 (name=17) | 53 (name=14) | 0.310 |
| 55 (name=12) | 49 (name=18) | 0.267 |
| 55 (name=12) | 53 (name=14) | 0.285 |
| 52 (name=15) | 49 (name=18) | 0.250 |
| 52 (name=15) | 53 (name=14) | 0.267 |
| 51 (name=16) | 49 (name=18) | 0.203 |
| 51 (name=16) | 53 (name=14) | 0.220 |

## Dimension-Specific Dialog Means

### 共情评估量表 (TES)

| Dialog | Name | Mean | SD | N |
|--------|------|------|-----|---|
| 57 | 10 | 5.61 | 0.97 | 324 |
| 64 | 3 | 5.20 | 1.21 | 342 |
| 66 | 1 | 5.10 | 1.21 | 324 |
| 65 | 2 | 5.08 | 1.46 | 324 |
| 58 | 9 | 5.07 | 1.19 | 324 |
| 56 | 11 | 5.05 | 1.21 | 324 |
| 60 | 7 | 5.03 | 1.27 | 324 |
| 62 | 5 | 5.02 | 1.05 | 324 |
| 63 | 4 | 5.00 | 1.19 | 324 |
| 59 | 8 | 4.98 | 1.18 | 324 |
| 54 | 13 | 4.96 | 1.30 | 324 |
| 48 | 19 | 4.94 | 1.22 | 324 |
| 47 | 24 | 4.92 | 1.73 | 342 |
| 61 | 6 | 4.89 | 1.23 | 324 |
| 50 | 17 | 4.89 | 1.24 | 333 |
| 55 | 12 | 4.87 | 1.22 | 351 |
| 52 | 15 | 4.71 | 1.31 | 324 |
| 51 | 16 | 4.58 | 1.26 | 324 |
| 53 | 14 | 4.53 | 1.18 | 324 |
| 49 | 18 | 4.35 | 1.32 | 324 |

### 无条件积极关注

| Dialog | Name | Mean | SD | N |
|--------|------|------|-----|---|
| 57 | 10 | 4.17 | 0.77 | 36 |
| 47 | 24 | 3.97 | 1.21 | 36 |
| 64 | 3 | 3.89 | 1.01 | 36 |
| 63 | 4 | 3.83 | 0.97 | 36 |
| 66 | 1 | 3.78 | 0.96 | 36 |
| 56 | 11 | 3.78 | 1.02 | 36 |
| 62 | 5 | 3.78 | 0.93 | 36 |
| 65 | 2 | 3.75 | 1.11 | 36 |
| 58 | 9 | 3.75 | 0.91 | 36 |
| 59 | 8 | 3.69 | 0.92 | 36 |
| 50 | 17 | 3.61 | 0.90 | 36 |
| 54 | 13 | 3.61 | 0.96 | 36 |
| 48 | 19 | 3.58 | 0.91 | 36 |
| 60 | 7 | 3.58 | 1.00 | 36 |
| 61 | 6 | 3.44 | 1.05 | 36 |
| 55 | 12 | 3.42 | 1.00 | 36 |
| 52 | 15 | 3.42 | 1.02 | 36 |
| 51 | 16 | 3.19 | 1.04 | 36 |
| 53 | 14 | 3.14 | 1.07 | 36 |
| 49 | 18 | 3.06 | 0.89 | 36 |

### 咨访同盟WAI-Observer-Short

| Dialog | Name | Mean | SD | N |
|--------|------|------|-----|---|
| 65 | 2 | 4.92 | 1.60 | 432 |
| 57 | 10 | 4.82 | 1.42 | 432 |
| 64 | 3 | 4.76 | 1.46 | 432 |
| 63 | 4 | 4.76 | 1.50 | 432 |
| 66 | 1 | 4.62 | 1.48 | 432 |
| 48 | 19 | 4.58 | 1.26 | 444 |
| 56 | 11 | 4.58 | 1.42 | 432 |
| 47 | 24 | 4.56 | 1.75 | 432 |
| 60 | 7 | 4.53 | 1.29 | 432 |
| 59 | 8 | 4.46 | 1.27 | 432 |
| 58 | 9 | 4.43 | 1.27 | 432 |
| 51 | 16 | 4.29 | 1.15 | 432 |
| 52 | 15 | 4.27 | 1.34 | 432 |
| 61 | 6 | 4.26 | 1.40 | 432 |
| 55 | 12 | 4.25 | 1.22 | 432 |
| 50 | 17 | 4.21 | 1.45 | 432 |
| 62 | 5 | 4.18 | 1.31 | 432 |
| 54 | 13 | 4.17 | 1.32 | 432 |
| 49 | 18 | 4.07 | 1.24 | 432 |
| 53 | 14 | 3.89 | 1.27 | 432 |

## Methodology Notes

1. **Model**: Linear mixed model with rater as random intercept grouping factor, dialog as variance component random effect, and question as fixed effect.
2. **Estimation**: Restricted Maximum Likelihood (REML) via statsmodels MixedLM.
3. **Dialog quality**: Computed as empirical Bayes (shrunken) estimates. Raw dialog means are shrunk toward the grand mean based on the ratio of dialog variance to total variance. This reduces noise from small samples.
4. **Credible intervals**: 95% intervals based on the posterior standard error of the empirical Bayes estimates: SE = sqrt(sigma2_dialog * sigma2_resid / (n * sigma2_dialog + sigma2_resid)).
5. **Shrinkage**: Dialogs with fewer raters are shrunk more toward the grand mean, reflecting greater uncertainty.
6. **Score extraction**: Numeric scores extracted from answer_value; only question_type=='choice' rows used.
