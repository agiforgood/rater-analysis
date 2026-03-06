# Question-Level Divergence Analysis

**Date:** 2026-03-07
**Script:** `question_divergence.py`

## 1. Per-Question Divergence Ranking

Questions sorted by average within-dialog std (higher = more rater disagreement):

| Rank | Dimension | Question | Reverse? | Mean | Avg Std | Avg Range | Max Range |
|------|-----------|----------|----------|------|---------|-----------|-----------|
| 1 | 咨访同盟WAI- | ⚠️ 问题看法不同(反向) Different views (REVERSE) | YES | 3.34 | 1.48 | 5.3 | 6 |
| 2 | 咨访同盟WAI- | ⚠️ 目标疑虑(反向) Goal doubts (REVERSE) | YES | 3.11 | 1.43 | 5.2 | 6 |
| 3 | 共情评估量表 ( | 温暖 Warmth |  | 4.77 | 1.36 | 5.6 | 6 |
| 4 | 共情评估量表 ( | 接纳感受 Acceptance |  | 4.80 | 1.36 | 5.7 | 6 |
| 5 | 咨访同盟WAI- | 欣赏来访者 Appreciation |  | 4.32 | 1.32 | 5.6 | 6 |
| 6 | 共情评估量表 ( | 情感共鸣 Resonance |  | 4.92 | 1.32 | 5.4 | 6 |
| 7 | 共情评估量表 ( | 内在同频 Attunement |  | 4.78 | 1.31 | 5.4 | 6 |
| 8 | 共情评估量表 ( | 理解感受 Feeling Understanding |  | 4.81 | 1.29 | 5.5 | 6 |
| 9 | 咨访同盟WAI- | 同频感受 Mutual resonance |  | 4.67 | 1.26 | 5.3 | 6 |
| 10 | 咨访同盟WAI- | 目标共识 Goal consensus |  | 4.55 | 1.24 | 5.2 | 6 |
| 11 | 咨访同盟WAI- | 改变理解 Understanding of change |  | 4.42 | 1.24 | 5.1 | 6 |
| 12 | 咨访同盟WAI- | 共同目标 Working toward goals |  | 4.89 | 1.15 | 4.8 | 6 |
| 13 | 咨访同盟WAI- | 问题解决一致 Problem agreement |  | 4.73 | 1.15 | 4.8 | 6 |
| 14 | 共情评估量表 ( | 理解认知 Cognitive Understanding |  | 5.08 | 1.14 | 4.8 | 6 |
| 15 | 咨访同盟WAI- | 目标重要性一致 Goal importance |  | 4.83 | 1.14 | 4.7 | 6 |
| 16 | 共情评估量表 ( | 关切 Concern |  | 5.08 | 1.13 | 4.8 | 6 |
| 17 | 共情评估量表 ( | 表现力 Expressiveness |  | 5.01 | 1.13 | 4.7 | 6 |
| 18 | 咨访同盟WAI- | 相互信任 Mutual trust |  | 4.85 | 1.13 | 4.9 | 6 |
| 19 | 共情评估量表 ( | 回应性 Responsiveness |  | 5.20 | 1.13 | 4.7 | 6 |
| 20 | 咨访同盟WAI- | 方式正确 Correct approach |  | 4.70 | 1.12 | 4.5 | 6 |
| 21 | 咨访同盟WAI- | 专业信心 Professional confidence |  | 4.76 | 1.10 | 4.5 | 6 |
| 22 | 无条件积极关注 | 积极关注等级 Positive Regard Level |  | 3.62 | 0.98 | 3.4 | 4 |

## 2. Per-Question ICC (Inter-Rater Reliability)

ICC(2,1) per question — lower = worse agreement:

| Question | Label | Reverse? | ICC | Quality |
|----------|-------|----------|-----|---------|
| q2 | 表现力 Expressiveness |  | 0.020 | poor |
| item4 | ⚠️ 目标疑虑(反向) Goal doubts (REVERSE) | YES | 0.020 | poor |
| q6 | 理解认知 Cognitive Understanding |  | 0.022 | poor |
| q9 | 回应性 Responsiveness |  | 0.026 | poor |
| q1 | 关切 Concern |  | 0.032 | poor |
| q3 | 情感共鸣 Resonance |  | 0.038 | poor |
| q8 | 接纳感受 Acceptance |  | 0.043 | poor |
| item10 | ⚠️ 问题看法不同(反向) Different views (REVERSE) | YES | 0.046 | poor |
| q5 | 内在同频 Attunement |  | 0.049 | poor |
| q7 | 理解感受 Feeling Understanding |  | 0.050 | poor |
| q4 | 温暖 Warmth |  | 0.053 | poor |
| positive_regard_level | 积极关注等级 Positive Regard Level |  | 0.061 | poor |
| item7 | 欣赏来访者 Appreciation |  | 0.069 | poor |
| item5 | 专业信心 Professional confidence |  | 0.071 | poor |
| item9 | 相互信任 Mutual trust |  | 0.075 | poor |
| item6 | 共同目标 Working toward goals |  | 0.076 | poor |
| item2 | 目标重要性一致 Goal importance |  | 0.081 | poor |
| item3 | 同频感受 Mutual resonance |  | 0.081 | poor |
| item8 | 目标共识 Goal consensus |  | 0.092 | poor |
| item1 | 问题解决一致 Problem agreement |  | 0.095 | poor |
| item11 | 改变理解 Understanding of change |  | 0.096 | poor |
| item12 | 方式正确 Correct approach |  | 0.097 | poor |

## 3. Reverse-Worded Item Effect (WAI)

Comparing reverse-worded items (item4, item10) vs. normal items:

| Metric | Reverse Items | Normal Items | Delta |
|--------|--------------|--------------|-------|
| Avg within-dialog std | 1.45 | 1.19 | +0.26 |
| Overall std | 1.48 | 1.25 | +0.23 |
| Avg mean score | 3.23 | 4.67 | -1.45 |

**Finding:** Reverse-worded items show **higher** divergence (+0.26 std), suggesting raters may interpret them inconsistently (some may forget to reverse their mental scale).

## 4. Question Agreement Clusters

Median within-dialog std used as cutoff to split questions into two groups.

### High Agreement (lower divergence)

- **item6** (共同目标 Working toward goals): avg std = 1.15
- **item1** (问题解决一致 Problem agreement): avg std = 1.15
- **q6** (理解认知 Cognitive Understanding): avg std = 1.14
- **item2** (目标重要性一致 Goal importance): avg std = 1.14
- **q1** (关切 Concern): avg std = 1.13
- **q2** (表现力 Expressiveness): avg std = 1.13
- **item9** (相互信任 Mutual trust): avg std = 1.13
- **q9** (回应性 Responsiveness): avg std = 1.13
- **item12** (方式正确 Correct approach): avg std = 1.12
- **item5** (专业信心 Professional confidence): avg std = 1.10
- **positive_regard_level** (积极关注等级 Positive Regard Level): avg std = 0.98

### Low Agreement (higher divergence)

- **item10** (⚠️ 问题看法不同(反向) Different views (REVERSE)): avg std = 1.48
- **item4** (⚠️ 目标疑虑(反向) Goal doubts (REVERSE)): avg std = 1.43
- **q4** (温暖 Warmth): avg std = 1.36
- **q8** (接纳感受 Acceptance): avg std = 1.36
- **item7** (欣赏来访者 Appreciation): avg std = 1.32
- **q3** (情感共鸣 Resonance): avg std = 1.32
- **q5** (内在同频 Attunement): avg std = 1.31
- **q7** (理解感受 Feeling Understanding): avg std = 1.29
- **item3** (同频感受 Mutual resonance): avg std = 1.26
- **item8** (目标共识 Goal consensus): avg std = 1.24
- **item11** (改变理解 Understanding of change): avg std = 1.24

## 5. Interpretation & Next Steps

- Questions with **high divergence** may have ambiguous wording or require more subjective judgment
- Questions with **low divergence** are candidates for 'anchor' items that raters can agree on
- Reverse-worded items should be checked for consistent interpretation across raters
- Consider: are high-divergence questions measuring something genuinely harder to observe, or is the rubric unclear?
- Possible follow-up: correlate divergence with dialog difficulty/ambiguity