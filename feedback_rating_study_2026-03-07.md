# Feedback on Rating Study Design

**Date:** 2026-03-07
**Context:** Review of the counseling dialog rating study (36 raters, 20 dialogs, 3 scales)

---

## What Went Well

**Balanced design was the right call.** Having all 36 raters rate all 20 dialogs saved this dataset. It means rater biases cancel out in the average, and we can extract a reliable signal despite terrible individual agreement. With an unbalanced design (different raters for different dialogs), this data would be uninterpretable.

**Sample size is adequate.** 36 raters is enough to push ICC(2,k) into the moderate-to-good range for WAI items. With fewer than ~15 raters, the averaged scores wouldn't reach usable reliability.

---

## What Needs to Change

### 1. Raters need calibration training

Rater bias accounts for **54% of the variance** in scores. The most lenient rater (mean 6.19) and most strict (mean 3.27) differ by nearly 3 points on a 7-point scale. One rater gave exactly 4.00 on every single dialog with zero differentiation.

**Action:** Before the next round, run a calibration session — have all raters score 2–3 example dialogs together, discuss disagreements, and align on what a "3" vs a "5" looks like concretely. This is standard practice in content analysis and clinical rating studies.

### 2. The TES (empathy) scale doesn't work

TES ICC is 0.003–0.057 per dialog — essentially zero. Raters fundamentally cannot agree on empathy facets (warmth, resonance, attunement) from reading transcripts. For comparison, WAI items reach ICC 0.40 on the same dialogs with the same raters, so the problem is the instrument, not the raters.

**Possible causes:**
- The rubric descriptions are too vague for text-based rating (these constructs may need video/audio to observe tone, body language)
- The 9 TES questions are too conceptually similar for raters to distinguish
- Empathy may simply not be reliably observer-rated from text alone

**Action:** Either fix the rubric with concrete behavioral anchors and transcript examples for each score level, switch to a different empathy measure validated for text, or acknowledge that TES scores from this study are not reliable and should not be used for decisions.

### 3. Remove or reword the reverse-scored WAI items (item4, item10)

These two are the most divergent questions (+0.26 std above normal WAI items). They rank #1 and #2 in disagreement. Raters get confused by negatively-worded statements — some score high to mean "yes, there are doubts" while others mentally flip the scale. They also appear in the bimodal cases (raters literally splitting into two camps on interpretation).

**Action:** Either reword them as positive statements or add bold, explicit instructions like "Note: higher score = MORE disagreement/doubt between client and counselor."

### 4. The positive regard scale needs more items

With only 1 question, you can't compute per-dialog ICC, can't detect response patterns, and a single rating is inherently less stable than a multi-item composite. It's also structurally inconsistent with TES (9 items) and WAI (12 items).

**Action:** Add 2–3 sub-facets to parallel the structure of the other scales.

### 5. Add anchor examples to the rubric

The questions with highest divergence all involve subjective emotional judgment (warmth, acceptance, attunement). The questions with lowest divergence are concrete and observable (goal agreement, problem-solving approach, professional confidence).

**Action:** For each subjective question, provide 1–2 concrete dialog excerpts illustrating each score level. Example: "A score of 3 on warmth looks like this: [excerpt]. A score of 6 looks like this: [excerpt]." This is standard practice in validated rating instruments and would likely cut disagreement substantially.

---

## Summary

The study design is solid — the balanced fully-crossed layout is exactly right, and 36 raters is sufficient. The problems are in the instruments and rater preparation. Calibrate your raters, fix the reverse items, add behavioral anchors to the rubric, and either overhaul or drop TES for text-based rating. With these changes, the next round should produce much more reliable data.
