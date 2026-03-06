"""
Rater-Centered Averaging Analysis
==================================
Adjusts for rater leniency/severity bias by centering each rater's scores
around the grand mean, then compares raw vs adjusted dialog rankings.
"""

import re
import pandas as pd
import numpy as np
from datetime import date

# ── Load & filter ──────────────────────────────────────────────────────────
df = pd.read_csv("问卷0305.csv")
df = df[df["question_type"] == "choice"].copy()

# Extract numeric score
def extract_score(val):
    val = str(val).strip()
    if re.match(r"^\d+$", val):
        return int(val)
    m = re.search(r"(\d+)分", val)
    if m:
        return int(m.group(1))
    return np.nan

df["score"] = df["answer_value"].apply(extract_score)
df = df.dropna(subset=["score"])

print(f"Total choice rows after score extraction: {len(df)}")
print(f"Unique raters: {df['user_id'].nunique()}")
print(f"Unique dialogs: {df['dialog_id'].nunique()}")
print(f"Unique dimensions: {df['dimension_name'].nunique()}")
print(f"Dimensions: {df['dimension_name'].unique().tolist()}")
print()

# ── Step 1: Rater personal means ──────────────────────────────────────────
rater_means = df.groupby("user_id")["score"].mean()
grand_mean = df["score"].mean()

print(f"Grand mean: {grand_mean:.4f}")
print(f"Rater means range: {rater_means.min():.4f} – {rater_means.max():.4f}")
print(f"Rater means std: {rater_means.std():.4f}")
print()

# ── Step 2: Adjusted scores ───────────────────────────────────────────────
df["rater_mean"] = df["user_id"].map(rater_means)
df["adjusted_score"] = df["score"] - df["rater_mean"] + grand_mean

# ── Step 3: Per-dialog quality (raw & adjusted) ──────────────────────────
dialog_raw = df.groupby(["dialog_id", "dialog_name"])["score"].mean().reset_index()
dialog_raw.columns = ["dialog_id", "dialog_name", "raw_mean"]

dialog_adj = df.groupby(["dialog_id", "dialog_name"])["adjusted_score"].mean().reset_index()
dialog_adj.columns = ["dialog_id", "dialog_name", "adj_mean"]

dialog = dialog_raw.merge(dialog_adj, on=["dialog_id", "dialog_name"])
dialog["dialog_id"] = dialog["dialog_id"].astype(int)
dialog["dialog_name"] = dialog["dialog_name"].astype(int)
dialog["raw_rank"] = dialog["raw_mean"].rank(ascending=False).astype(int)
dialog["adj_rank"] = dialog["adj_mean"].rank(ascending=False).astype(int)
dialog["rank_shift"] = (dialog["raw_rank"] - dialog["adj_rank"]).astype(int)
dialog = dialog.sort_values("adj_rank")

print("=" * 80)
print("PER-DIALOG QUALITY SCORES (sorted by adjusted rank)")
print("=" * 80)
fmt = "{:<10} {:<8} {:>8} {:>6} {:>8} {:>6} {:>10}"
print(fmt.format("dialog_id", "name", "raw_mean", "rank", "adj_mean", "rank", "rank_shift"))
print("-" * 80)
for _, r in dialog.iterrows():
    print(fmt.format(
        int(r["dialog_id"]), int(r["dialog_name"]),
        f"{r['raw_mean']:.3f}", int(r["raw_rank"]),
        f"{r['adj_mean']:.3f}", int(r["adj_rank"]),
        f"{int(r['rank_shift']):+d}"
    ))

# ── Step 5: Per-dialog per-dimension (raw vs adjusted) ───────────────────
dim_raw = df.groupby(["dialog_id", "dialog_name", "dimension_name"])["score"].mean().reset_index()
dim_raw.columns = ["dialog_id", "dialog_name", "dimension_name", "raw_mean"]

dim_adj = df.groupby(["dialog_id", "dialog_name", "dimension_name"])["adjusted_score"].mean().reset_index()
dim_adj.columns = ["dialog_id", "dialog_name", "dimension_name", "adj_mean"]

dim_df = dim_raw.merge(dim_adj, on=["dialog_id", "dialog_name", "dimension_name"])

# Rank within each dimension
for dim in dim_df["dimension_name"].unique():
    mask = dim_df["dimension_name"] == dim
    dim_df.loc[mask, "raw_rank"] = dim_df.loc[mask, "raw_mean"].rank(ascending=False).astype(int)
    dim_df.loc[mask, "adj_rank"] = dim_df.loc[mask, "adj_mean"].rank(ascending=False).astype(int)
    dim_df.loc[mask, "rank_shift"] = dim_df.loc[mask, "raw_rank"] - dim_df.loc[mask, "adj_rank"]

dim_df["raw_rank"] = dim_df["raw_rank"].astype(int)
dim_df["adj_rank"] = dim_df["adj_rank"].astype(int)
dim_df["rank_shift"] = dim_df["rank_shift"].astype(int)

print()
for dim in sorted(dim_df["dimension_name"].unique()):
    sub = dim_df[dim_df["dimension_name"] == dim].sort_values("adj_rank")
    print(f"\n{'=' * 80}")
    print(f"DIMENSION: {dim}")
    print(f"{'=' * 80}")
    print(fmt.format("dialog_id", "name", "raw_mean", "rank", "adj_mean", "rank", "rank_shift"))
    print("-" * 80)
    for _, r in sub.iterrows():
        shift_str = f"{int(r['rank_shift']):+d}"
        print(fmt.format(
            r["dialog_id"], r["dialog_name"],
            f"{r['raw_mean']:.3f}", r["raw_rank"],
            f"{r['adj_mean']:.3f}", r["adj_rank"],
            shift_str
        ))

# ── Step 6: Biggest movers ───────────────────────────────────────────────
print(f"\n{'=' * 80}")
print("BIGGEST RANK SHIFTS (overall, |shift| >= 2)")
print("=" * 80)
movers = dialog[dialog["rank_shift"].abs() >= 2].sort_values("rank_shift", key=abs, ascending=False)
if movers.empty:
    print("No dialogs shifted by 2+ ranks. Showing top 5 by |shift|:")
    movers = dialog.sort_values("rank_shift", key=abs, ascending=False).head(5)

for _, r in movers.iterrows():
    direction = "UP" if r["rank_shift"] > 0 else "DOWN"
    print(f"  Dialog {int(r['dialog_id'])} (name={int(r['dialog_name'])}): "
          f"rank {int(r['raw_rank'])} -> {int(r['adj_rank'])} ({direction} {abs(int(r['rank_shift']))})")

# ── Rater severity table ─────────────────────────────────────────────────
print(f"\n{'=' * 80}")
print("RATER SEVERITY / LENIENCY (sorted by mean)")
print("=" * 80)
rater_info = df.groupby("user_id").agg(
    mean=("score", "mean"),
    std=("score", "std"),
    n=("score", "count")
).sort_values("mean")
rater_info["bias"] = rater_info["mean"] - grand_mean
print(f"{'user_id':>8} {'mean':>8} {'std':>8} {'bias':>8} {'n':>6}")
print("-" * 44)
for uid, r in rater_info.iterrows():
    print(f"{uid:>8} {r['mean']:>8.3f} {r['std']:>8.3f} {r['bias']:>+8.3f} {r['n']:>6.0f}")


# ════════════════════════════════════════════════════════════════════════════
# Generate markdown report
# ════════════════════════════════════════════════════════════════════════════
report_file = "analysis_centered_averaging_2026-03-07.md"

lines = []
a = lines.append

a("# Rater-Centered Averaging Analysis")
a(f"\n**Generated:** {date.today()}")
a(f"\n**Dataset:** 问卷0305.csv")
a(f"\n**Method:** Each rater's scores are adjusted by subtracting their personal mean ")
a("and adding the grand mean, correcting for systematic leniency/severity bias.")
a("")
a("## Summary Statistics")
a("")
a(f"- Total scored ratings: **{len(df)}**")
a(f"- Raters: **{df['user_id'].nunique()}**")
a(f"- Dialogs: **{df['dialog_id'].nunique()}**")
a(f"- Grand mean: **{grand_mean:.4f}**")
a(f"- Rater mean range: **{rater_means.min():.4f}** – **{rater_means.max():.4f}** (std={rater_means.std():.4f})")
a("")

# Overall dialog rankings
a("## Per-Dialog Quality Rankings")
a("")
a("| dialog_id | name | raw_mean | raw_rank | adj_mean | adj_rank | rank_shift |")
a("|-----------|------|----------|----------|----------|----------|------------|")
for _, r in dialog.iterrows():
    shift = f"{int(r['rank_shift']):+d}"
    a(f"| {int(r['dialog_id'])} | {int(r['dialog_name'])} | {r['raw_mean']:.3f} | {int(r['raw_rank'])} | {r['adj_mean']:.3f} | {int(r['adj_rank'])} | {shift} |")
a("")

# Biggest movers
a("## Biggest Rank Shifts After Adjustment")
a("")
top_movers = dialog.sort_values("rank_shift", key=abs, ascending=False).head(8)
for _, r in top_movers.iterrows():
    direction = "UP" if r["rank_shift"] > 0 else "DOWN"
    a(f"- **Dialog {int(r['dialog_id'])}** (name={int(r['dialog_name'])}): "
      f"rank {int(r['raw_rank'])} → {int(r['adj_rank'])} ({direction} {abs(int(r['rank_shift']))})")
a("")

# Per-dimension tables
a("## Per-Dialog Per-Dimension Rankings")
for dim in sorted(dim_df["dimension_name"].unique()):
    sub = dim_df[dim_df["dimension_name"] == dim].sort_values("adj_rank")
    a(f"\n### {dim}")
    a("")
    a("| dialog_id | name | raw_mean | raw_rank | adj_mean | adj_rank | rank_shift |")
    a("|-----------|------|----------|----------|----------|----------|------------|")
    for _, r in sub.iterrows():
        shift = f"{int(r['rank_shift']):+d}"
        a(f"| {r['dialog_id']} | {r['dialog_name']} | {r['raw_mean']:.3f} | {r['raw_rank']} | {r['adj_mean']:.3f} | {r['adj_rank']} | {shift} |")
    a("")

# Rater table
a("## Rater Severity / Leniency")
a("")
a("Bias = rater_mean - grand_mean. Positive = lenient, negative = harsh.")
a("")
a("| user_id | mean | std | bias | n |")
a("|---------|------|-----|------|---|")
for uid, r in rater_info.iterrows():
    a(f"| {uid} | {r['mean']:.3f} | {r['std']:.3f} | {r['bias']:+.3f} | {r['n']:.0f} |")
a("")

# Interpretation
a("## Interpretation")
a("")
a("- **Rater centering** removes systematic leniency/severity differences between raters.")
a("- Dialogs that move **up** in adjusted rankings were underrated by harsh raters (or had fewer lenient raters).")
a("- Dialogs that move **down** were overrated by lenient raters.")
a("- Large rank shifts indicate dialogs whose raw scores were most distorted by rater bias.")
a("")

with open(report_file, "w") as f:
    f.write("\n".join(lines))

print(f"\nMarkdown report saved to: {report_file}")
