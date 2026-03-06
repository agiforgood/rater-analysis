"""
Rater Agreement Analysis for 问卷0305 scoring data.

Quantifies inter-rater differences across dimensions:
1. Per-rater summary stats (mean, std) vs group
2. Inter-rater reliability (ICC, Krippendorff's alpha)
3. Pairwise rater distance matrix
4. Per-dialog consensus & disagreement
5. Outlier raters (those who deviate most from consensus)
"""

import re
import pandas as pd
import numpy as np
from itertools import combinations


def load_and_clean(path: str = "问卷0305.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    # Keep only choice questions (skip free text notes)
    df = df[df["question_type"] == "choice"].copy()

    # Extract numeric score from answer_value
    # Dimension 2 (positive regard) has text like "第4阶段（4分）- ..."
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


def rater_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Per-rater mean and std, compared to grand mean."""
    grand_mean = df["score"].mean()
    stats = (
        df.groupby("user_id")["score"]
        .agg(["mean", "std", "count"])
        .rename(columns={"mean": "rater_mean", "std": "rater_std", "count": "n_ratings"})
    )
    stats["deviation_from_grand"] = stats["rater_mean"] - grand_mean
    stats = stats.sort_values("deviation_from_grand")
    return stats


def rater_summary_by_dimension(df: pd.DataFrame) -> pd.DataFrame:
    """Per-rater mean by dimension, with deviation from dimension grand mean."""
    dim_grand = df.groupby("dimension_id")["score"].mean().rename("dim_grand_mean")
    stats = (
        df.groupby(["user_id", "dimension_id", "dimension_name"])["score"]
        .agg(["mean", "std", "count"])
        .rename(columns={"mean": "rater_mean", "std": "rater_std", "count": "n"})
        .reset_index()
    )
    stats = stats.merge(dim_grand, on="dimension_id")
    stats["deviation"] = stats["rater_mean"] - stats["dim_grand_mean"]
    return stats


def build_rater_dialog_matrix(df: pd.DataFrame, dimension_id: int) -> pd.DataFrame:
    """Build rater x dialog matrix of mean scores for a given dimension."""
    sub = df[df["dimension_id"] == dimension_id]
    matrix = sub.groupby(["user_id", "dialog_name"])["score"].mean().unstack(fill_value=np.nan)
    return matrix


def pairwise_rater_distances(matrix: pd.DataFrame) -> pd.DataFrame:
    """Mean absolute difference between every pair of raters."""
    raters = matrix.index.tolist()
    records = []
    for r1, r2 in combinations(raters, 2):
        v1, v2 = matrix.loc[r1], matrix.loc[r2]
        mask = v1.notna() & v2.notna()
        if mask.sum() == 0:
            continue
        mad = (v1[mask] - v2[mask]).abs().mean()
        records.append({"rater_1": r1, "rater_2": r2, "mean_abs_diff": mad, "n_shared": mask.sum()})
    return pd.DataFrame(records).sort_values("mean_abs_diff", ascending=False)


def per_dialog_consensus(df: pd.DataFrame) -> pd.DataFrame:
    """Per dialog x dimension: mean, std, range, CV across raters."""
    stats = (
        df.groupby(["dialog_name", "dimension_id", "dimension_name"])["score"]
        .agg(["mean", "std", "min", "max", "count"])
        .reset_index()
    )
    stats["range"] = stats["max"] - stats["min"]
    stats["cv"] = stats["std"] / stats["mean"]
    stats = stats.sort_values("std", ascending=False)
    return stats


def icc_two_way_agreement(matrix: pd.DataFrame) -> float:
    """ICC(2,1) two-way random, absolute agreement — single measures.

    matrix: raters (rows) x items (columns), no NaN allowed.
    """
    mat = matrix.dropna(axis=1).values  # drop items with missing raters
    n, k = mat.shape  # n=raters, k=items
    if n < 2 or k < 2:
        return float("nan")

    grand = mat.mean()
    ss_total = ((mat - grand) ** 2).sum()
    ss_rows = k * ((mat.mean(axis=1) - grand) ** 2).sum()  # between raters
    ss_cols = n * ((mat.mean(axis=0) - grand) ** 2).sum()  # between items
    ss_resid = ss_total - ss_rows - ss_cols

    ms_rows = ss_rows / (n - 1)
    ms_cols = ss_cols / (k - 1)
    ms_resid = ss_resid / ((n - 1) * (k - 1))

    icc = (ms_cols - ms_resid) / (ms_cols + (n - 1) * ms_resid + n * (ms_rows - ms_resid) / k)
    return icc


def outlier_raters(df: pd.DataFrame, threshold_z: float = 2.0) -> pd.DataFrame:
    """Find raters whose mean score deviates > threshold_z std from group mean per dimension."""
    stats = rater_summary_by_dimension(df)
    dim_std = df.groupby("dimension_id")["score"].std().rename("dim_std")
    stats = stats.merge(dim_std, on="dimension_id")
    stats["z_score"] = stats["deviation"] / stats["dim_std"]
    outliers = stats[stats["z_score"].abs() > threshold_z].sort_values("z_score", key=abs, ascending=False)
    return outliers


def main():
    df = load_and_clean()
    dim_names = {1: "TES共情", 2: "无条件积极关注", 3: "WAI咨访同盟"}

    print("=" * 70)
    print("RATER AGREEMENT ANALYSIS — 问卷0305")
    print("=" * 70)

    # --- 1. Overall stats ---
    print(f"\nTotal ratings: {len(df)}")
    print(f"Raters: {df['user_id'].nunique()}, Dialogs: {df['dialog_name'].nunique()}, Dimensions: {df['dimension_id'].nunique()}")
    print(f"Grand mean score: {df['score'].mean():.2f}, Grand std: {df['score'].std():.2f}")

    # --- 2. Per-rater summary ---
    print("\n" + "=" * 70)
    print("PER-RATER SUMMARY (sorted by deviation from grand mean)")
    print("=" * 70)
    rs = rater_summary(df)
    print(rs.to_string())

    # --- 3. ICC per dimension ---
    print("\n" + "=" * 70)
    print("ICC(2,1) — INTER-RATER RELIABILITY PER DIMENSION")
    print("=" * 70)
    for dim_id in sorted(df["dimension_id"].unique()):
        matrix = build_rater_dialog_matrix(df, dim_id)
        icc = icc_two_way_agreement(matrix)
        label = dim_names.get(dim_id, str(dim_id))
        quality = (
            "poor" if icc < 0.5 else
            "moderate" if icc < 0.75 else
            "good" if icc < 0.9 else
            "excellent"
        )
        print(f"  Dimension {dim_id} ({label}): ICC = {icc:.3f} ({quality})")

    # --- 4. Per-dialog consensus ---
    print("\n" + "=" * 70)
    print("PER-DIALOG CONSENSUS (top 15 most disagreed, by std)")
    print("=" * 70)
    consensus = per_dialog_consensus(df)
    cols = ["dialog_name", "dimension_name", "mean", "std", "range", "cv", "count"]
    print(consensus[cols].head(15).to_string(index=False, float_format="{:.2f}".format))

    # --- 5. Pairwise rater distances (dimension 1 as example) ---
    print("\n" + "=" * 70)
    print("TOP 15 MOST DIVERGENT RATER PAIRS (Dimension 1: TES)")
    print("=" * 70)
    matrix1 = build_rater_dialog_matrix(df, 1)
    pw = pairwise_rater_distances(matrix1)
    print(pw.head(15).to_string(index=False, float_format="{:.2f}".format))

    # --- 6. Outlier raters ---
    print("\n" + "=" * 70)
    print("OUTLIER RATERS (|z| > 2.0 from dimension mean)")
    print("=" * 70)
    out = outlier_raters(df)
    if len(out) == 0:
        print("  No outlier raters found at z > 2.0 threshold.")
    else:
        cols = ["user_id", "dimension_name", "rater_mean", "dim_grand_mean", "deviation", "z_score"]
        print(out[cols].to_string(index=False, float_format="{:.2f}".format))

    # --- 7. Rater bias direction ---
    print("\n" + "=" * 70)
    print("RATER BIAS SUMMARY (lenient vs strict)")
    print("=" * 70)
    rs = rater_summary(df)
    n_lenient = (rs["deviation_from_grand"] > 0.5).sum()
    n_strict = (rs["deviation_from_grand"] < -0.5).sum()
    n_neutral = len(rs) - n_lenient - n_strict
    print(f"  Lenient (mean > grand+0.5): {n_lenient} raters")
    print(f"  Strict  (mean < grand-0.5): {n_strict} raters")
    print(f"  Neutral (within ±0.5):      {n_neutral} raters")
    print(f"\n  Most lenient: user {rs.index[-1]} (mean={rs.iloc[-1]['rater_mean']:.2f}, dev=+{rs.iloc[-1]['deviation_from_grand']:.2f})")
    print(f"  Most strict:  user {rs.index[0]} (mean={rs.iloc[0]['rater_mean']:.2f}, dev={rs.iloc[0]['deviation_from_grand']:.2f})")


if __name__ == "__main__":
    main()
