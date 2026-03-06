"""
Question-level divergence analysis for 问卷0305.

Investigates:
1. Per-question divergence (std, range, CV across raters) — which questions cause most disagreement?
2. Clustering questions into high/low agreement groups
3. Reverse-worded item effects (WAI item4, item10)
4. Per-question ICC to find which questions are reliably rated
5. Output results to markdown
"""

import re
import pandas as pd
import numpy as np
from itertools import combinations
from datetime import date


def load_and_clean(path: str = "问卷0305.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[df["question_type"] == "choice"].copy()

    def extract_score(val: str) -> float:
        if re.match(r"^\d+$", str(val).strip()):
            return float(val)
        m = re.search(r"(\d+)分", str(val))
        if m:
            return float(m.group(1))
        return float("nan")

    df["score"] = df["answer_value"].apply(extract_score)
    df = df.dropna(subset=["score"])
    return df


# Question labels for readability
TES_LABELS = {
    "q1": "关切 Concern",
    "q2": "表现力 Expressiveness",
    "q3": "情感共鸣 Resonance",
    "q4": "温暖 Warmth",
    "q5": "内在同频 Attunement",
    "q6": "理解认知 Cognitive Understanding",
    "q7": "理解感受 Feeling Understanding",
    "q8": "接纳感受 Acceptance",
    "q9": "回应性 Responsiveness",
}

WAI_LABELS = {
    "item1": "问题解决一致 Problem agreement",
    "item2": "目标重要性一致 Goal importance",
    "item3": "同频感受 Mutual resonance",
    "item4": "⚠️ 目标疑虑(反向) Goal doubts (REVERSE)",
    "item5": "专业信心 Professional confidence",
    "item6": "共同目标 Working toward goals",
    "item7": "欣赏来访者 Appreciation",
    "item8": "目标共识 Goal consensus",
    "item9": "相互信任 Mutual trust",
    "item10": "⚠️ 问题看法不同(反向) Different views (REVERSE)",
    "item11": "改变理解 Understanding of change",
    "item12": "方式正确 Correct approach",
}

ALL_LABELS = {**TES_LABELS, **WAI_LABELS, "positive_regard_level": "积极关注等级 Positive Regard Level"}
REVERSE_ITEMS = {"item4", "item10"}


def per_question_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute divergence stats per question across all raters and dialogs."""
    # For each (dialog, question), compute std across raters
    # Then average that std across dialogs to get "typical rater disagreement" per question
    records = []
    for (dim_name, qid), grp in df.groupby(["dimension_name", "question_id"]):
        # Per-dialog stats
        dialog_stats = grp.groupby("dialog_name")["score"].agg(["mean", "std", "min", "max", "count"])
        dialog_stats["range"] = dialog_stats["max"] - dialog_stats["min"]

        records.append({
            "dimension": dim_name,
            "question_id": qid,
            "label": ALL_LABELS.get(qid, qid),
            "is_reverse": qid in REVERSE_ITEMS,
            "grand_mean": grp["score"].mean(),
            "grand_std": grp["score"].std(),
            "avg_within_dialog_std": dialog_stats["std"].mean(),
            "avg_within_dialog_range": dialog_stats["range"].mean(),
            "max_range_any_dialog": dialog_stats["range"].max(),
            "n_dialogs": len(dialog_stats),
            "n_ratings": len(grp),
        })

    result = pd.DataFrame(records).sort_values("avg_within_dialog_std", ascending=False)
    return result


def per_question_icc(df: pd.DataFrame) -> pd.DataFrame:
    """ICC(2,1) per question: how reliably do raters agree on this specific question?"""
    records = []
    for (dim_name, qid), grp in df.groupby(["dimension_name", "question_id"]):
        # Build rater x dialog matrix for this question
        matrix = grp.pivot_table(index="user_id", columns="dialog_name", values="score", aggfunc="mean")
        # Drop columns (dialogs) with any NaN to compute ICC
        mat = matrix.dropna(axis=1).values
        n, k = mat.shape
        if n < 2 or k < 2:
            records.append({"dimension": dim_name, "question_id": qid, "icc": float("nan"), "n_raters": n, "n_dialogs": k})
            continue

        grand = mat.mean()
        ss_total = ((mat - grand) ** 2).sum()
        ss_rows = k * ((mat.mean(axis=1) - grand) ** 2).sum()
        ss_cols = n * ((mat.mean(axis=0) - grand) ** 2).sum()
        ss_resid = ss_total - ss_rows - ss_cols

        ms_rows = ss_rows / (n - 1)
        ms_cols = ss_cols / (k - 1)
        ms_resid = ss_resid / ((n - 1) * (k - 1))

        icc = (ms_cols - ms_resid) / (ms_cols + (n - 1) * ms_resid + n * (ms_rows - ms_resid) / k)
        records.append({
            "dimension": dim_name,
            "question_id": qid,
            "label": ALL_LABELS.get(qid, qid),
            "is_reverse": qid in REVERSE_ITEMS,
            "icc": icc,
            "n_raters": n,
            "n_dialogs": k,
        })

    return pd.DataFrame(records).sort_values("icc", ascending=True)


def reverse_item_analysis(df: pd.DataFrame) -> dict:
    """Compare divergence between reverse-worded and normal WAI items."""
    wai = df[df["dimension_name"].str.contains("WAI")]
    reverse = wai[wai["question_id"].isin(REVERSE_ITEMS)]
    normal = wai[~wai["question_id"].isin(REVERSE_ITEMS)]

    def divergence_stats(sub):
        per_dialog = sub.groupby("dialog_name")["score"].agg(["std", "mean"])
        return {
            "avg_std": per_dialog["std"].mean(),
            "avg_mean": per_dialog["mean"].mean(),
            "overall_std": sub["score"].std(),
        }

    return {
        "reverse_items": divergence_stats(reverse),
        "normal_items": divergence_stats(normal),
    }


def question_agreement_clusters(qstats: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split questions into high and low agreement groups based on within-dialog std."""
    median_std = qstats["avg_within_dialog_std"].median()
    high_agreement = qstats[qstats["avg_within_dialog_std"] <= median_std].copy()
    low_agreement = qstats[qstats["avg_within_dialog_std"] > median_std].copy()
    return high_agreement, low_agreement


def generate_markdown(qstats, icc_df, rev_analysis, high_agree, low_agree) -> str:
    """Generate full markdown report."""
    lines = []
    lines.append(f"# Question-Level Divergence Analysis")
    lines.append(f"\n**Date:** {date.today()}")
    lines.append(f"**Script:** `question_divergence.py`")

    # Section 1: Per-question divergence ranking
    lines.append("\n## 1. Per-Question Divergence Ranking")
    lines.append("\nQuestions sorted by average within-dialog std (higher = more rater disagreement):\n")
    lines.append("| Rank | Dimension | Question | Reverse? | Mean | Avg Std | Avg Range | Max Range |")
    lines.append("|------|-----------|----------|----------|------|---------|-----------|-----------|")
    for i, (_, row) in enumerate(qstats.iterrows(), 1):
        rev = "YES" if row["is_reverse"] else ""
        lines.append(
            f"| {i} | {row['dimension'][:8]} | {row['label']} | {rev} | "
            f"{row['grand_mean']:.2f} | {row['avg_within_dialog_std']:.2f} | "
            f"{row['avg_within_dialog_range']:.1f} | {row['max_range_any_dialog']:.0f} |"
        )

    # Section 2: Per-question ICC
    lines.append("\n## 2. Per-Question ICC (Inter-Rater Reliability)")
    lines.append("\nICC(2,1) per question — lower = worse agreement:\n")
    lines.append("| Question | Label | Reverse? | ICC | Quality |")
    lines.append("|----------|-------|----------|-----|---------|")
    for _, row in icc_df.iterrows():
        if pd.isna(row.get("icc")):
            continue
        quality = (
            "poor" if row["icc"] < 0.5 else
            "moderate" if row["icc"] < 0.75 else
            "good" if row["icc"] < 0.9 else
            "excellent"
        )
        rev = "YES" if row.get("is_reverse", False) else ""
        lines.append(f"| {row['question_id']} | {row.get('label', '')} | {rev} | {row['icc']:.3f} | {quality} |")

    # Section 3: Reverse-worded items
    lines.append("\n## 3. Reverse-Worded Item Effect (WAI)")
    lines.append("\nComparing reverse-worded items (item4, item10) vs. normal items:\n")
    rev = rev_analysis["reverse_items"]
    nor = rev_analysis["normal_items"]
    lines.append(f"| Metric | Reverse Items | Normal Items | Delta |")
    lines.append(f"|--------|--------------|--------------|-------|")
    lines.append(f"| Avg within-dialog std | {rev['avg_std']:.2f} | {nor['avg_std']:.2f} | {rev['avg_std'] - nor['avg_std']:+.2f} |")
    lines.append(f"| Overall std | {rev['overall_std']:.2f} | {nor['overall_std']:.2f} | {rev['overall_std'] - nor['overall_std']:+.2f} |")
    lines.append(f"| Avg mean score | {rev['avg_mean']:.2f} | {nor['avg_mean']:.2f} | {rev['avg_mean'] - nor['avg_mean']:+.2f} |")

    if rev["avg_std"] > nor["avg_std"]:
        lines.append(f"\n**Finding:** Reverse-worded items show **higher** divergence (+{rev['avg_std'] - nor['avg_std']:.2f} std), "
                      "suggesting raters may interpret them inconsistently (some may forget to reverse their mental scale).")
    else:
        lines.append(f"\n**Finding:** Reverse-worded items do NOT show higher divergence than normal items.")

    # Section 4: Agreement clusters
    lines.append("\n## 4. Question Agreement Clusters")
    lines.append(f"\nMedian within-dialog std used as cutoff to split questions into two groups.\n")

    lines.append("### High Agreement (lower divergence)")
    lines.append("")
    for _, row in high_agree.iterrows():
        lines.append(f"- **{row['question_id']}** ({row['label']}): avg std = {row['avg_within_dialog_std']:.2f}")

    lines.append("\n### Low Agreement (higher divergence)")
    lines.append("")
    for _, row in low_agree.iterrows():
        lines.append(f"- **{row['question_id']}** ({row['label']}): avg std = {row['avg_within_dialog_std']:.2f}")

    # Section 5: Interpretation
    lines.append("\n## 5. Interpretation & Next Steps")
    lines.append("")
    lines.append("- Questions with **high divergence** may have ambiguous wording or require more subjective judgment")
    lines.append("- Questions with **low divergence** are candidates for 'anchor' items that raters can agree on")
    lines.append("- Reverse-worded items should be checked for consistent interpretation across raters")
    lines.append("- Consider: are high-divergence questions measuring something genuinely harder to observe, or is the rubric unclear?")
    lines.append("- Possible follow-up: correlate divergence with dialog difficulty/ambiguity")

    return "\n".join(lines)


def main():
    df = load_and_clean()

    print("Computing per-question divergence stats...")
    qstats = per_question_stats(df)

    print("Computing per-question ICC...")
    icc_df = per_question_icc(df)

    print("Analyzing reverse-worded items...")
    rev_analysis = reverse_item_analysis(df)

    print("Clustering questions by agreement level...")
    high_agree, low_agree = question_agreement_clusters(qstats)

    # Print summary to console
    print("\n" + "=" * 70)
    print("QUESTION-LEVEL DIVERGENCE ANALYSIS")
    print("=" * 70)

    print("\n--- Per-Question Divergence (sorted by avg within-dialog std) ---")
    cols = ["dimension", "question_id", "label", "is_reverse", "grand_mean", "avg_within_dialog_std", "avg_within_dialog_range"]
    print(qstats[cols].to_string(index=False, float_format="{:.2f}".format))

    print("\n--- Per-Question ICC ---")
    cols_icc = ["question_id", "label", "is_reverse", "icc"]
    print(icc_df[cols_icc].to_string(index=False, float_format="{:.3f}".format))

    print("\n--- Reverse Item Effect (WAI) ---")
    print(f"  Reverse items avg std: {rev_analysis['reverse_items']['avg_std']:.2f}")
    print(f"  Normal items avg std:  {rev_analysis['normal_items']['avg_std']:.2f}")

    print(f"\n--- Agreement Clusters ---")
    print(f"  High agreement: {len(high_agree)} questions")
    print(f"  Low agreement:  {len(low_agree)} questions")

    # Generate and save markdown report
    md = generate_markdown(qstats, icc_df, rev_analysis, high_agree, low_agree)
    outfile = f"analysis_question_divergence_{date.today()}.md"
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"\nReport saved to {outfile}")


if __name__ == "__main__":
    main()
