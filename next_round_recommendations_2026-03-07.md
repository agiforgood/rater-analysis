# Recommendations for Next Round of Expert Scoring

**Date:** 2026-03-07
**Context:** Planning a new data collection round with expert raters, based on findings from the initial 36-rater study.

---

## Changes Before Next Collection (by priority)

### 1. Calibration Session (non-negotiable)

Have all expert raters score 2–3 of the same dialogs *before* the real scoring begins. Discuss disagreements live. This alone would likely cut the rater variance (currently 54% of total) in half.

### 2. Fix Reverse Items Now

Reword WAI item4 and item10 as positive statements. This is a 5-minute fix that eliminates a known source of confusion. No reason to collect more noisy data from a known design flaw.

- **item4** current: "双方对试图达成的治疗目标，存在疑虑或缺乏理解" → reword as positive: "双方对治疗目标有清晰的共识和理解"
- **item10** current: "来访者和咨询师对来访者的真实问题是什么有不同的看法" → reword as positive: "来访者和咨询师对来访者的真实问题有一致的看法"

### 3. Add Anchor Examples to the Rubric

For each question, provide 1–2 short transcript excerpts showing what a "2", "4", and "6" look like. Focus on the high-divergence questions first: warmth (q4), acceptance (q8), resonance (q3), attunement (q5).

### 4. Decide What to Do with TES

TES ICC was 0.003–0.057 in the current study — essentially zero. Options:

| Option | Pros | Cons |
|--------|------|------|
| **Keep TES with anchors** | Preserves comparability; may fix the issue | Risk of wasting expert time if anchors aren't enough |
| **Reduce TES to 3–4 items** | Less cognitive load; may improve differentiation | Loses granularity |
| **Drop TES entirely** | Focus resources on what works (WAI) | Loses empathy measurement |
| **Pilot first (recommended)** | Low cost; validates before committing | Delays full collection slightly |

**Recommendation:** Pilot first. Have 3–5 experts rate 3 dialogs on the revised TES before committing to the full collection. If ICC improves to >0.3, proceed. If not, drop or radically simplify.

### 5. Expand Positive Regard to 3–4 Items

Currently 1 question — can't compute ICC, can't detect patterns. Add sub-facets, e.g.:
- Non-judgmental acceptance of the client's feelings
- Allowing client autonomy vs imposing agenda
- Genuine interest and engagement with the client's situation

### 6. Design Decision: Same or New Dialogs?

| Option | Pros | Cons |
|--------|------|------|
| Same 20 dialogs | Direct expert vs non-expert comparison; can validate Bayesian estimates | Experts may find it redundant |
| New dialogs | Broader coverage | Lose comparability |
| **Overlap design (recommended)** | Rate 10 of the original 20 + 10 new | Get both comparability and coverage |

---

## Pilot Protocol

### Goal
Verify that revised instruments produce usable inter-rater reliability (ICC > 0.3) before full expert collection.

### Participants
3–5 expert raters

### Materials
- 3 dialogs selected for range: one high-quality (#10), one mid (#8), one low (#14)
- Revised rubric with:
  - Reworded item4 and item10
  - Anchor examples for TES questions
  - Expanded positive regard (3–4 items)

### Procedure

1. **Calibration (30 min)**
   - All experts rate dialog #10 independently
   - Group discussion: compare scores, discuss disagreements
   - Align on rubric interpretation
   - Do NOT re-score — the point is shared understanding, not convergence

2. **Independent rating (45 min)**
   - Each expert independently rates dialogs #8 and #14
   - All 3 scales: TES (revised), WAI (item4/10 reworded), positive regard (expanded)

3. **Analysis**
   - Compute ICC(2,1) per dimension
   - Compare to original study benchmarks
   - Decision criteria:
     - ICC > 0.3 per dimension → proceed to full collection
     - ICC 0.15–0.3 → revise rubric further, re-pilot
     - ICC < 0.15 → drop or fundamentally redesign that scale

### Timeline
- Day 1: Prepare revised rubric with anchors
- Day 2: Calibration session + independent rating
- Day 3: Analyze pilot results, make go/no-go decision
- Day 4+: Full expert collection (if go)

---

## Revised Rubric Template

### WAI Items — Reworded

Original → Revised (reverse items only):

**Item 4 (was reverse):**
- Old: "双方对试图达成的治疗目标，存在疑虑或缺乏理解"
- New: "咨访双方对治疗目标有清晰的共识和理解"
- Scale: 1 (完全不符合) — 7 (完全符合)

**Item 10 (was reverse):**
- Old: "来访者和咨询师对来访者的真实问题是什么有不同的看法"
- New: "来访者和咨询师对来访者的真实问题有一致的看法"
- Scale: 1 (完全不符合) — 7 (完全符合)

### TES Items — Anchor Example Format

For each TES question, add anchors in this format:

> **温暖 Warmth (q4)**
>
> 咨询师的温暖体现在友好、亲切、真诚的说话方式，支持来访者的自我表达。
>
> **Score 2 example:**
> [Insert a 2–3 turn excerpt from a dialog where warmth is minimal — mechanical, distant responses]
>
> **Score 4 example:**
> [Insert a 2–3 turn excerpt showing moderate warmth — polite and supportive but not deeply personal]
>
> **Score 6 example:**
> [Insert a 2–3 turn excerpt showing high warmth — genuinely caring tone, personal engagement, affirming language]

*(Anchor excerpts to be selected from the existing 20 dialogs — choose clear, unambiguous examples that calibration raters agreed on.)*

### Positive Regard — Expanded Items

Current single item → 4 items:

1. **非评判接纳:** 咨询师对来访者的感受和行为展现出非评判的态度 (1–5)
2. **自主性支持:** 咨询师尊重来访者的自主性，而非试图控制或引导 (1–5)
3. **真诚关怀:** 咨询师表现出对来访者作为个体的真诚兴趣和关心 (1–5)
4. **整体积极关注等级:** [保留原有5阶段评分] (1–5)

---

## Success Criteria for Full Collection

After pilot, proceed to full collection only if:

- [ ] WAI ICC(2,1) > 0.3 (was 0.07–0.10 in original)
- [ ] TES ICC(2,1) > 0.15 (was 0.02–0.05 in original)
- [ ] Positive regard ICC(2,1) computable and > 0.2
- [ ] No bimodal distributions on reworded items
- [ ] Expert feedback confirms rubric clarity
