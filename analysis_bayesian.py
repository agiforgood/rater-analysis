"""
Hierarchical Bayesian-style Analysis of Rater Scoring Data
===========================================================
Uses a mixed linear model (empirical Bayes / REML) to estimate:
  - Dialog quality (random effect) with credible intervals
  - Rater bias (random effect)
  - Question/item difficulty (fixed effect)
  - Residual noise

Model: score_ijk = mu + dialog_quality_i + rater_bias_j + question_effect_k + epsilon

We fit this via statsmodels MixedLM with dialog and rater as random effects,
question as fixed effect. This yields shrunken (empirical Bayes) estimates
with standard errors, which we convert to 95% credible/confidence intervals.
"""

import re
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

warnings.filterwarnings("ignore")

# ── 1. Load and preprocess data ──────────────────────────────────────────────

df = pd.read_csv("问卷0305.csv")
df = df[df["question_type"] == "choice"].copy()


def extract_score(val):
    """Extract numeric score from answer_value."""
    val = str(val).strip()
    if re.match(r"^\d+$", val):
        return int(val)
    m = re.search(r"(\d+)分", val)
    if m:
        return int(m.group(1))
    return np.nan


df["score"] = df["answer_value"].apply(extract_score)
df = df.dropna(subset=["score"])
df["score"] = df["score"].astype(float)

# Create clean categorical columns
df["dialog"] = df["dialog_id"].astype(str)
df["rater"] = df["user_id"].astype(str)
df["question"] = df["question_id"].astype(str)
df["dimension"] = df["dimension_name"].astype(str)

print(f"Data loaded: {len(df)} observations")
print(f"  Dialogs: {df['dialog'].nunique()}, Raters: {df['rater'].nunique()}, Questions: {df['question'].nunique()}")
print(f"  Dimensions: {df['dimension'].nunique()}")
print()

# ── 2. Fit mixed linear model ────────────────────────────────────────────────
# We use dialog and rater as random intercepts, question as fixed effect.
# statsmodels MixedLM supports one grouping factor for random effects natively,
# so we use a variance components approach: fit with rater as group,
# dialog as random effect via variance components.

# Approach: Use MixedLM with rater as groups and dialog as variance component
# This gives us BLUPs (best linear unbiased predictors) = empirical Bayes estimates.

print("=" * 70)
print("FITTING HIERARCHICAL MODEL")
print("=" * 70)
print()

# Encode question as dummy variables (fixed effect)
# Use C() in formula for categorical
# Group by rater, add dialog as random effect via vc_formula

# statsmodels MixedLM with variance components
vc = {"dialog": "0 + C(dialog)"}
model = smf.mixedlm(
    "score ~ C(question)",
    data=df,
    groups=df["rater"],
    re_formula="1",
    vc_formula=vc,
)
result = model.fit(reml=True)

print("Model fit complete.")
print(f"  Converged: {result.converged}")
print(f"  Log-likelihood: {result.llf:.1f}")
print()

# ── 3. Extract variance components ──────────────────────────────────────────

# Random effect variances
rater_var = float(result.cov_re.iloc[0, 0])  # Group (rater) random intercept variance
dialog_var = float(result.vcomp[0])  # Dialog variance component
resid_var = float(result.scale)

total_var = rater_var + dialog_var + resid_var

print("VARIANCE COMPONENTS")
print("-" * 40)
print(f"  Rater variance:   {rater_var:.4f} ({100*rater_var/total_var:.1f}%)")
print(f"  Dialog variance:  {dialog_var:.4f} ({100*dialog_var/total_var:.1f}%)")
print(f"  Residual variance:{resid_var:.4f} ({100*resid_var/total_var:.1f}%)")
print(f"  Total variance:   {total_var:.4f}")
print(f"  ICC (dialog):     {dialog_var/total_var:.3f}")
print(f"  ICC (rater):      {rater_var/total_var:.3f}")
print()

# ── 4. Extract random effects (empirical Bayes / BLUPs) ─────────────────────

# Rater random effects: "Group" key is the rater intercept
# Dialog BLUPs are also stored per rater; we average them across raters
rater_effects = result.random_effects  # dict: rater_id -> Series

rater_blups = {r: float(v["Group"]) for r, v in rater_effects.items()}
rater_df = pd.DataFrame(
    {"rater": list(rater_blups.keys()), "rater_bias": list(rater_blups.values())}
)
rater_df = rater_df.sort_values("rater_bias")

# Dialog BLUPs: the model gives per-rater dialog effects (variance components).
# Average the dialog BLUPs across all raters to get the dialog-level estimate.
dialog_ids_in_re = [c for c in list(rater_effects.values())[0].index if c.startswith("dialog")]
dialog_blups_raw = {}
for col in dialog_ids_in_re:
    # Extract dialog id from column name like "dialog[C(dialog)[47]]"
    d_id = col.split("[")[-1].rstrip("]")
    vals = [float(v[col]) for v in rater_effects.values()]
    dialog_blups_raw[d_id] = np.mean(vals)

# Grand mean
mu = result.fe_params["Intercept"]

# Get question fixed effects
question_effects = {}
for param_name, val in result.fe_params.items():
    if param_name.startswith("C(question)"):
        q = param_name.replace("C(question)[T.", "").rstrip("]")
        question_effects[q] = val
# Reference question has effect 0
ref_q = [q for q in df["question"].unique() if q not in question_effects]
for q in ref_q:
    question_effects[q] = 0.0

# ── 5. Compute dialog quality estimates with uncertainty ─────────────────────
# The BLUPs from the model are already shrunken. We compute SE from the
# empirical Bayes posterior variance formula.

dialog_quality = {}
dialog_quality_se = {}

for d in df["dialog"].unique():
    n_obs = len(df[df["dialog"] == d])

    # Use the model's BLUP if available, otherwise compute manually
    if d in dialog_blups_raw:
        eb_estimate = dialog_blups_raw[d]
    else:
        eb_estimate = 0.0

    # SE of empirical Bayes estimate
    if dialog_var > 0:
        eb_se = np.sqrt(dialog_var * resid_var / (n_obs * dialog_var + resid_var))
    else:
        eb_se = np.sqrt(resid_var / n_obs)

    dialog_quality[d] = eb_estimate
    dialog_quality_se[d] = eb_se

# Build dialog results dataframe
dialog_results = pd.DataFrame({
    "dialog_id": list(dialog_quality.keys()),
    "quality_estimate": list(dialog_quality.values()),
    "se": list(dialog_quality_se.values()),
})

# Add dialog names
dialog_name_map = df.drop_duplicates("dialog_id").set_index("dialog_id")["dialog_name"].to_dict()
dialog_results["dialog_name"] = dialog_results["dialog_id"].astype(int).map(dialog_name_map)

# Compute credible intervals (95%)
z = 1.96
dialog_results["ci_lower"] = dialog_results["quality_estimate"] - z * dialog_results["se"]
dialog_results["ci_upper"] = dialog_results["quality_estimate"] + z * dialog_results["se"]
dialog_results["ci_width"] = dialog_results["ci_upper"] - dialog_results["ci_lower"]

# Raw mean for comparison
raw_means = df.groupby("dialog")["score"].mean().reset_index()
raw_means.columns = ["dialog_id", "raw_mean"]
dialog_results = dialog_results.merge(raw_means, on="dialog_id", how="left")

# Count observations per dialog
obs_counts = df.groupby("dialog")["score"].count().reset_index()
obs_counts.columns = ["dialog_id", "n_obs"]
dialog_results = dialog_results.merge(obs_counts, on="dialog_id", how="left")

# Sort by quality
dialog_results = dialog_results.sort_values("quality_estimate", ascending=False).reset_index(drop=True)

# ── 6. Print results ────────────────────────────────────────────────────────

print("=" * 70)
print("DIALOG QUALITY RANKINGS (Empirical Bayes Estimates)")
print("=" * 70)
print(f"{'Rank':<5} {'Dialog':<10} {'Name':<8} {'EB Est':>8} {'95% CI':>18} {'CI Width':>9} {'Raw Mean':>9} {'N':>5}")
print("-" * 75)

for i, row in dialog_results.iterrows():
    rank = i + 1
    ci_str = f"[{row['ci_lower']:+.3f}, {row['ci_upper']:+.3f}]"
    print(
        f"{rank:<5} {row['dialog_id']:<10} {str(row['dialog_name']):<8} "
        f"{row['quality_estimate']:+.3f}   {ci_str:>18} {row['ci_width']:.3f}     {row['raw_mean']:.3f}  {row['n_obs']:>5.0f}"
    )

# Add absolute quality (mu + dialog_effect)
dialog_results["absolute_quality"] = mu + dialog_results["quality_estimate"]
dialog_results["abs_ci_lower"] = mu + dialog_results["ci_lower"]
dialog_results["abs_ci_upper"] = mu + dialog_results["ci_upper"]

print()
print(f"Grand mean (mu): {mu:.3f}")
print(f"Absolute quality = mu + dialog_effect")
print()

print("=" * 70)
print("DIALOG QUALITY (ABSOLUTE SCALE)")
print("=" * 70)
print(f"{'Rank':<5} {'Dialog':<10} {'Name':<8} {'Quality':>8} {'95% CI':>20} {'Confidence':>12}")
print("-" * 70)

for i, row in dialog_results.iterrows():
    rank = i + 1
    ci_str = f"[{row['abs_ci_lower']:.2f}, {row['abs_ci_upper']:.2f}]"
    confidence = "HIGH" if row["ci_width"] < 0.3 else ("MEDIUM" if row["ci_width"] < 0.5 else "LOW")
    print(
        f"{rank:<5} {row['dialog_id']:<10} {str(row['dialog_name']):<8} "
        f"{row['absolute_quality']:.3f}   {ci_str:>20}   {confidence:>10}"
    )

# ── 7. Rater bias ───────────────────────────────────────────────────────────

print()
print("=" * 70)
print("RATER BIAS ESTIMATES (Random Intercepts)")
print("=" * 70)
print(f"{'Rater':<8} {'Bias':>8} {'Interpretation':<30}")
print("-" * 50)

rater_df_sorted = rater_df.sort_values("rater_bias")
for _, row in rater_df_sorted.iterrows():
    bias = row["rater_bias"]
    if abs(bias) < 0.3:
        interp = "Near average"
    elif bias < -0.3:
        interp = f"Strict rater (rates {abs(bias):.1f} pts lower)"
    else:
        interp = f"Lenient rater (rates {bias:.1f} pts higher)"
    print(f"{row['rater']:<8} {bias:+.3f}   {interp}")

print()
print(f"Rater bias std dev: {np.std(list(rater_blups.values())):.3f}")
print(f"Rater bias range: [{min(rater_blups.values()):.3f}, {max(rater_blups.values()):.3f}]")

# ── 8. Question effects ─────────────────────────────────────────────────────

print()
print("=" * 70)
print("QUESTION/ITEM EFFECTS (Fixed Effects, relative to reference)")
print("=" * 70)

q_df = pd.DataFrame({"question": list(question_effects.keys()), "effect": list(question_effects.values())})
q_df["dimension"] = q_df["question"].apply(
    lambda q: (
        "TES" if q.startswith("q") else
        "WAI" if q.startswith("item") else
        "UPR"
    )
)
q_df = q_df.sort_values(["dimension", "effect"])

print(f"{'Question':<25} {'Dimension':<6} {'Effect':>8}")
print("-" * 45)
for _, row in q_df.iterrows():
    print(f"{row['question']:<25} {row['dimension']:<6} {row['effect']:+.3f}")

# ── 9. Confidence analysis ──────────────────────────────────────────────────

print()
print("=" * 70)
print("CONFIDENCE ANALYSIS")
print("=" * 70)

high_conf = dialog_results[dialog_results["ci_width"] < 0.3]
med_conf = dialog_results[(dialog_results["ci_width"] >= 0.3) & (dialog_results["ci_width"] < 0.5)]
low_conf = dialog_results[dialog_results["ci_width"] >= 0.5]

print(f"HIGH confidence (CI width < 0.3):   {len(high_conf)} dialogs")
if len(high_conf) > 0:
    for _, r in high_conf.iterrows():
        print(f"  Dialog {r['dialog_id']} (name={r['dialog_name']}): {r['absolute_quality']:.2f} +/- {r['se']:.3f}")

print(f"MEDIUM confidence (0.3-0.5):        {len(med_conf)} dialogs")
if len(med_conf) > 0:
    for _, r in med_conf.iterrows():
        print(f"  Dialog {r['dialog_id']} (name={r['dialog_name']}): {r['absolute_quality']:.2f} +/- {r['se']:.3f}")

print(f"LOW confidence (CI width >= 0.5):    {len(low_conf)} dialogs")
if len(low_conf) > 0:
    for _, r in low_conf.iterrows():
        print(f"  Dialog {r['dialog_id']} (name={r['dialog_name']}): {r['absolute_quality']:.2f} +/- {r['se']:.3f}")

# ── 10. Pairwise comparisons (which dialogs are significantly different?) ────

print()
print("=" * 70)
print("SIGNIFICANTLY DIFFERENT DIALOG PAIRS (non-overlapping 95% CIs)")
print("=" * 70)

sig_pairs = []
dialogs_sorted = dialog_results.sort_values("quality_estimate", ascending=False)
for i_idx in range(len(dialogs_sorted)):
    for j_idx in range(i_idx + 1, len(dialogs_sorted)):
        r1 = dialogs_sorted.iloc[i_idx]
        r2 = dialogs_sorted.iloc[j_idx]
        # Check if CIs don't overlap
        if r1["ci_lower"] > r2["ci_upper"] or r2["ci_lower"] > r1["ci_upper"]:
            diff = r1["quality_estimate"] - r2["quality_estimate"]
            sig_pairs.append((r1["dialog_id"], r1["dialog_name"], r2["dialog_id"], r2["dialog_name"], diff))

if sig_pairs:
    print(f"Found {len(sig_pairs)} significantly different pairs:")
    for d1, n1, d2, n2, diff in sig_pairs[:20]:
        print(f"  Dialog {d1} (name={n1}) > Dialog {d2} (name={n2}) by {diff:.3f}")
    if len(sig_pairs) > 20:
        print(f"  ... and {len(sig_pairs) - 20} more pairs")
else:
    print("No pairs with non-overlapping 95% CIs found.")
    print("This suggests substantial uncertainty -- differences between dialogs are modest relative to noise.")

# ── 11. Dimension-specific analysis ─────────────────────────────────────────

print()
print("=" * 70)
print("DIMENSION-SPECIFIC DIALOG MEANS")
print("=" * 70)

for dim in df["dimension"].unique():
    sub = df[df["dimension"] == dim]
    dim_means = sub.groupby(["dialog", "dialog_name"])["score"].agg(["mean", "std", "count"]).reset_index()
    dim_means = dim_means.sort_values("mean", ascending=False)
    print(f"\n{dim}:")
    print(f"  {'Dialog':<10} {'Name':<8} {'Mean':>6} {'SD':>6} {'N':>5}")
    for _, r in dim_means.iterrows():
        print(f"  {r['dialog']:<10} {str(r['dialog_name']):<8} {r['mean']:.2f} {r['std']:.2f} {r['count']:>5.0f}")

# ── 12. Generate markdown report ────────────────────────────────────────────

report_date = "2026-03-07"
report_file = f"analysis_bayesian_{report_date}.md"

lines = []
lines.append("# Hierarchical Bayesian Analysis of Rater Scoring Data")
lines.append(f"\nDate: {report_date}")
lines.append(f"\n## Model Specification")
lines.append("")
lines.append("```")
lines.append("score_ijk = mu + dialog_quality_i + rater_bias_j + question_effect_k + epsilon")
lines.append("```")
lines.append("")
lines.append("- **Dialog quality**: random effect (empirical Bayes / BLUP)")
lines.append("- **Rater bias**: random intercept per rater")
lines.append("- **Question effect**: fixed effect (dummy-coded)")
lines.append("- **Estimation**: REML via statsmodels MixedLM")
lines.append("")

lines.append("## Variance Components")
lines.append("")
lines.append("| Component | Variance | % of Total |")
lines.append("|-----------|----------|------------|")
lines.append(f"| Rater | {rater_var:.4f} | {100*rater_var/total_var:.1f}% |")
lines.append(f"| Dialog | {dialog_var:.4f} | {100*dialog_var/total_var:.1f}% |")
lines.append(f"| Residual | {resid_var:.4f} | {100*resid_var/total_var:.1f}% |")
lines.append(f"| **Total** | **{total_var:.4f}** | **100%** |")
lines.append("")
lines.append(f"- ICC (dialog): {dialog_var/total_var:.3f}")
lines.append(f"- ICC (rater): {rater_var/total_var:.3f}")
lines.append(f"- Grand mean (mu): {mu:.3f}")
lines.append("")

lines.append("## Dialog Quality Rankings")
lines.append("")
lines.append("Estimates are empirical Bayes (shrunken) estimates with 95% credible intervals.")
lines.append("")
lines.append("| Rank | Dialog ID | Name | Quality | 95% CI | CI Width | Confidence | Raw Mean | N |")
lines.append("|------|-----------|------|---------|--------|----------|------------|----------|---|")

for i, row in dialog_results.iterrows():
    rank = i + 1
    ci_str = f"[{row['abs_ci_lower']:.2f}, {row['abs_ci_upper']:.2f}]"
    confidence = "HIGH" if row["ci_width"] < 0.3 else ("MEDIUM" if row["ci_width"] < 0.5 else "LOW")
    lines.append(
        f"| {rank} | {row['dialog_id']} | {row['dialog_name']} | "
        f"{row['absolute_quality']:.3f} | {ci_str} | {row['ci_width']:.3f} | "
        f"{confidence} | {row['raw_mean']:.3f} | {row['n_obs']:.0f} |"
    )

lines.append("")
lines.append("### Interpretation")
lines.append("")
lines.append(f"- **Best dialog**: {dialog_results.iloc[0]['dialog_id']} "
             f"(name={dialog_results.iloc[0]['dialog_name']}) "
             f"with quality {dialog_results.iloc[0]['absolute_quality']:.3f}")
lines.append(f"- **Worst dialog**: {dialog_results.iloc[-1]['dialog_id']} "
             f"(name={dialog_results.iloc[-1]['dialog_name']}) "
             f"with quality {dialog_results.iloc[-1]['absolute_quality']:.3f}")
lines.append(f"- Quality range: {dialog_results['absolute_quality'].max() - dialog_results['absolute_quality'].min():.3f} points")
lines.append("")

# Confidence summary
lines.append("### Confidence Summary")
lines.append("")
lines.append(f"- HIGH confidence (CI < 0.3): {len(high_conf)} dialogs")
lines.append(f"- MEDIUM confidence (0.3-0.5): {len(med_conf)} dialogs")
lines.append(f"- LOW confidence (CI >= 0.5): {len(low_conf)} dialogs")
lines.append("")

# Rater bias
lines.append("## Rater Bias Estimates")
lines.append("")
lines.append("| Rater | Bias | Interpretation |")
lines.append("|-------|------|----------------|")

for _, row in rater_df_sorted.iterrows():
    bias = row["rater_bias"]
    if abs(bias) < 0.3:
        interp = "Near average"
    elif bias < -0.3:
        interp = f"Strict (rates {abs(bias):.1f} pts lower)"
    else:
        interp = f"Lenient (rates {bias:.1f} pts higher)"
    lines.append(f"| {row['rater']} | {bias:+.3f} | {interp} |")

lines.append("")
lines.append(f"- Rater bias std dev: {np.std(list(rater_blups.values())):.3f}")
lines.append(f"- Rater bias range: [{min(rater_blups.values()):.3f}, {max(rater_blups.values()):.3f}]")
lines.append("")

# Question effects
lines.append("## Question/Item Effects")
lines.append("")
lines.append("| Question | Dimension | Effect |")
lines.append("|----------|-----------|--------|")
for _, row in q_df.iterrows():
    lines.append(f"| {row['question']} | {row['dimension']} | {row['effect']:+.3f} |")

lines.append("")

# Significant pairs
lines.append("## Significantly Different Dialog Pairs")
lines.append("")
if sig_pairs:
    lines.append(f"Found {len(sig_pairs)} pairs with non-overlapping 95% CIs:")
    lines.append("")
    lines.append("| Higher Dialog | Lower Dialog | Difference |")
    lines.append("|--------------|--------------|------------|")
    for d1, n1, d2, n2, diff in sig_pairs:
        lines.append(f"| {d1} (name={n1}) | {d2} (name={n2}) | {diff:.3f} |")
else:
    lines.append("No pairs with non-overlapping 95% CIs. Differences between dialogs are modest relative to uncertainty.")

lines.append("")

# Dimension-specific
lines.append("## Dimension-Specific Dialog Means")
lines.append("")
for dim in df["dimension"].unique():
    sub = df[df["dimension"] == dim]
    dim_means = sub.groupby(["dialog", "dialog_name"])["score"].agg(["mean", "std", "count"]).reset_index()
    dim_means = dim_means.sort_values("mean", ascending=False)
    lines.append(f"### {dim}")
    lines.append("")
    lines.append("| Dialog | Name | Mean | SD | N |")
    lines.append("|--------|------|------|-----|---|")
    for _, r in dim_means.iterrows():
        lines.append(f"| {r['dialog']} | {r['dialog_name']} | {r['mean']:.2f} | {r['std']:.2f} | {r['count']:.0f} |")
    lines.append("")

# Methodology note
lines.append("## Methodology Notes")
lines.append("")
lines.append("1. **Model**: Linear mixed model with rater as random intercept grouping factor, "
             "dialog as variance component random effect, and question as fixed effect.")
lines.append("2. **Estimation**: Restricted Maximum Likelihood (REML) via statsmodels MixedLM.")
lines.append("3. **Dialog quality**: Computed as empirical Bayes (shrunken) estimates. "
             "Raw dialog means are shrunk toward the grand mean based on the ratio of "
             "dialog variance to total variance. This reduces noise from small samples.")
lines.append("4. **Credible intervals**: 95% intervals based on the posterior standard error "
             "of the empirical Bayes estimates: SE = sqrt(sigma2_dialog * sigma2_resid / "
             "(n * sigma2_dialog + sigma2_resid)).")
lines.append("5. **Shrinkage**: Dialogs with fewer raters are shrunk more toward the grand mean, "
             "reflecting greater uncertainty.")
lines.append("6. **Score extraction**: Numeric scores extracted from answer_value; "
             "only question_type=='choice' rows used.")
lines.append("")

report_text = "\n".join(lines)

with open(report_file, "w") as f:
    f.write(report_text)

print()
print(f"\nReport saved to {report_file}")
print("Done.")
