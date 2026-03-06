"""
Many-Facet Rasch Model (MFRM) Analysis for Rater Scoring Data.

Implements iterative estimation (Joint Maximum Likelihood style) to
simultaneously estimate:
  - Dialog quality (theta): fair quality measure for each dialog
  - Rater severity (delta): how strict/lenient each rater is
  - Item difficulty (beta): how hard each question is to score highly

Model: E[score] = mu + theta_dialog - delta_rater - beta_item
Estimation via iterative least-squares with centering constraints.
"""

import re
import numpy as np
import pandas as pd
from datetime import date


# ── 1. Load and clean data ──────────────────────────────────────────────────

def load_data(path="问卷0305.csv"):
    df = pd.read_csv(path)
    df = df[df["question_type"] == "choice"].copy()

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
    df["score"] = df["score"].astype(float)

    # Use dialog_name as the dialog identifier for readability
    df["dialog"] = df["dialog_name"].astype(str)
    df["rater"] = df["user_id"].astype(str)
    df["item"] = df["question_id"].astype(str)
    df["dimension"] = df["dimension_name"].astype(str)

    print(f"Loaded {len(df)} choice observations")
    print(f"  Dialogs: {df['dialog'].nunique()}, Raters: {df['rater'].nunique()}, Items: {df['item'].nunique()}")
    return df


# ── 2. MFRM via iterative least squares ─────────────────────────────────────

def estimate_mfrm(df, max_iter=200, tol=1e-6):
    """
    Iterative estimation of the additive model:
        score_ijk = mu + theta_i - delta_j - beta_k + residual

    At each iteration:
      1. Compute residuals from current estimates.
      2. Update each facet parameter as the mean residual for that facet level.
      3. Re-center rater and item effects to sum to zero.

    This is equivalent to iterative proportional fitting / least-squares
    for a main-effects-only model and converges to the OLS solution.
    """
    dialogs = df["dialog"].unique()
    raters = df["rater"].unique()
    items = df["item"].unique()

    # Initialise
    mu = df["score"].mean()
    theta = {d: 0.0 for d in dialogs}   # dialog quality
    delta = {r: 0.0 for r in raters}    # rater severity
    beta  = {q: 0.0 for q in items}     # item difficulty

    # Pre-compute group indices for speed
    dialog_groups = df.groupby("dialog").indices
    rater_groups  = df.groupby("rater").indices
    item_groups   = df.groupby("item").indices

    scores = df["score"].values
    dialog_arr = df["dialog"].values
    rater_arr  = df["rater"].values
    item_arr   = df["item"].values

    for iteration in range(max_iter):
        # Compute predicted and residual
        pred = np.array([mu + theta[dialog_arr[i]] - delta[rater_arr[i]] - beta[item_arr[i]]
                         for i in range(len(df))])
        resid = scores - pred

        max_change = 0.0

        # Update theta (dialog quality)
        for d in dialogs:
            idx = dialog_groups[d]
            adj = resid[idx].mean()
            theta[d] += adj
            max_change = max(max_change, abs(adj))

        # Re-compute residuals
        pred = np.array([mu + theta[dialog_arr[i]] - delta[rater_arr[i]] - beta[item_arr[i]]
                         for i in range(len(df))])
        resid = scores - pred

        # Update delta (rater severity)
        for r in raters:
            idx = rater_groups[r]
            adj = -resid[idx].mean()  # negative because model has -delta
            delta[r] += adj
            max_change = max(max_change, abs(adj))

        # Re-compute residuals
        pred = np.array([mu + theta[dialog_arr[i]] - delta[rater_arr[i]] - beta[item_arr[i]]
                         for i in range(len(df))])
        resid = scores - pred

        # Update beta (item difficulty)
        for q in items:
            idx = item_groups[q]
            adj = -resid[idx].mean()  # negative because model has -beta
            beta[q] += adj
            max_change = max(max_change, abs(adj))

        # Center constraints: sum(delta) = 0, sum(beta) = 0
        delta_mean = np.mean(list(delta.values()))
        for r in raters:
            delta[r] -= delta_mean
        mu -= delta_mean

        beta_mean = np.mean(list(beta.values()))
        for q in items:
            beta[q] -= beta_mean
        mu -= beta_mean

        if max_change < tol:
            print(f"  Converged at iteration {iteration + 1} (max change = {max_change:.2e})")
            break
    else:
        print(f"  Did not converge after {max_iter} iterations (max change = {max_change:.2e})")

    # Compute final residual stats
    pred = np.array([mu + theta[dialog_arr[i]] - delta[rater_arr[i]] - beta[item_arr[i]]
                     for i in range(len(df))])
    resid = scores - pred
    rmse = np.sqrt(np.mean(resid ** 2))
    print(f"  Grand mean (mu) = {mu:.4f}")
    print(f"  RMSE = {rmse:.4f}")

    return mu, theta, delta, beta, rmse


# ── 3. Compute fair scores ───────────────────────────────────────────────────

def compute_fair_scores(df, mu, theta, delta, beta):
    """
    Fair score for a dialog = mu + theta_dialog
    (removing rater and item effects, evaluated at average rater/item).
    Also compute raw average for comparison.
    """
    raw_avg = df.groupby("dialog")["score"].mean()
    records = []
    for d in sorted(theta, key=lambda x: theta[x], reverse=True):
        fair = mu + theta[d]
        records.append({
            "dialog": d,
            "theta": theta[d],
            "fair_score": fair,
            "raw_avg": raw_avg.get(d, np.nan),
            "n_ratings": int((df["dialog"] == d).sum()),
        })
    return pd.DataFrame(records)


# ── 4. Per-dimension analysis ────────────────────────────────────────────────

def per_dimension_analysis(df):
    """Run a simpler per-dimension fair-average for supplementary insight."""
    results = {}
    for dim in df["dimension"].unique():
        sub = df[df["dimension"] == dim]
        # Simple: dialog mean minus rater mean plus grand mean
        grand = sub["score"].mean()
        rater_means = sub.groupby("rater")["score"].mean()
        dialog_means = sub.groupby("dialog")["score"].mean()

        # Fair score = dialog_mean - (avg of rater_means for raters who rated it - grand)
        # Simpler: just report dialog means for each dimension
        results[dim] = dialog_means.sort_values(ascending=False)
    return results


# ── 5. Reporting ─────────────────────────────────────────────────────────────

def print_and_report(df, mu, theta, delta, beta, rmse):
    lines = []

    def out(s=""):
        print(s)
        lines.append(s)

    out("# Many-Facet Rasch Model (MFRM) Analysis Report")
    out(f"\n**Date**: {date.today()}")
    out(f"\n**Data**: {len(df)} observations from {df['rater'].nunique()} raters, "
        f"{df['dialog'].nunique()} dialogs, {df['item'].nunique()} items across "
        f"{df['dimension'].nunique()} dimensions")
    out(f"\n**Model**: score = mu + theta(dialog) - delta(rater) - beta(item)")
    out(f"- Grand mean (mu) = {mu:.4f}")
    out(f"- RMSE = {rmse:.4f}")

    # ── Dialog quality ranking ──
    fair_df = compute_fair_scores(df, mu, theta, delta, beta)
    out("\n## Dialog Quality Ranking (Fair Scores)")
    out("\nFair score = mu + theta (adjusted for rater severity and item difficulty)")
    out(f"\n| Rank | Dialog | Theta | Fair Score | Raw Avg | N Ratings |")
    out("|------|--------|-------|------------|---------|-----------|")
    for rank, (_, row) in enumerate(fair_df.iterrows(), 1):
        out(f"| {rank} | {row['dialog']} | {row['theta']:+.3f} | {row['fair_score']:.3f} | "
            f"{row['raw_avg']:.3f} | {row['n_ratings']} |")

    # ── Rater severity ──
    rater_df = pd.DataFrame([
        {"rater": r, "severity": delta[r],
         "mean_score": df[df["rater"] == r]["score"].mean(),
         "n_ratings": int((df["rater"] == r).sum())}
        for r in delta
    ]).sort_values("severity", ascending=False)

    out("\n## Rater Severity (delta)")
    out("\nPositive delta = more severe (gives lower scores); Negative = more lenient")
    out(f"\n| Rank | Rater | Severity | Mean Score | N Ratings |")
    out("|------|-------|----------|------------|-----------|")
    for rank, (_, row) in enumerate(rater_df.iterrows(), 1):
        out(f"| {rank} | {row['rater']} | {row['severity']:+.3f} | {row['mean_score']:.3f} | {row['n_ratings']} |")

    out(f"\n**Most severe rater**: Rater {rater_df.iloc[0]['rater']} (delta = {rater_df.iloc[0]['severity']:+.3f}, mean score = {rater_df.iloc[0]['mean_score']:.3f})")
    out(f"**Most lenient rater**: Rater {rater_df.iloc[-1]['rater']} (delta = {rater_df.iloc[-1]['severity']:+.3f}, mean score = {rater_df.iloc[-1]['mean_score']:.3f})")
    out(f"**Severity range**: {rater_df['severity'].max() - rater_df['severity'].min():.3f} (spread between most severe and most lenient)")

    # ── Item difficulty ──
    # Map items to dimensions
    item_dim = df.groupby("item")["dimension"].first().to_dict()
    item_df = pd.DataFrame([
        {"item": q, "difficulty": beta[q],
         "dimension": item_dim.get(q, ""),
         "mean_score": df[df["item"] == q]["score"].mean(),
         "n_ratings": int((df["item"] == q).sum())}
        for q in beta
    ]).sort_values("difficulty", ascending=False)

    out("\n## Item/Question Difficulty (beta)")
    out("\nPositive beta = harder (receives lower scores); Negative = easier")
    out(f"\n| Rank | Item | Dimension | Difficulty | Mean Score | N Ratings |")
    out("|------|------|-----------|------------|------------|-----------|")
    for rank, (_, row) in enumerate(item_df.iterrows(), 1):
        dim_short = row["dimension"][:12] + "..." if len(row["dimension"]) > 15 else row["dimension"]
        out(f"| {rank} | {row['item']} | {dim_short} | {row['difficulty']:+.3f} | {row['mean_score']:.3f} | {row['n_ratings']} |")

    out(f"\n**Hardest item**: {item_df.iloc[0]['item']} (beta = {item_df.iloc[0]['difficulty']:+.3f}, dim = {item_df.iloc[0]['dimension']})")
    out(f"**Easiest item**: {item_df.iloc[-1]['item']} (beta = {item_df.iloc[-1]['difficulty']:+.3f}, dim = {item_df.iloc[-1]['dimension']})")

    # ── Per-dimension summary ──
    out("\n## Per-Dimension Summary")
    for dim in df["dimension"].unique():
        sub = df[df["dimension"] == dim]
        dim_items = sub["item"].unique()
        out(f"\n### {dim}")
        out(f"- Items: {', '.join(sorted(dim_items))}")
        out(f"- Score range: {sub['score'].min():.0f} - {sub['score'].max():.0f}")
        out(f"- Mean score: {sub['score'].mean():.3f} (SD = {sub['score'].std():.3f})")
        # Dialog ranking within dimension
        dim_dialog = sub.groupby("dialog")["score"].mean().sort_values(ascending=False)
        out(f"- Top 3 dialogs: {', '.join(f'{d} ({v:.2f})' for d, v in dim_dialog.head(3).items())}")
        out(f"- Bottom 3 dialogs: {', '.join(f'{d} ({v:.2f})' for d, v in dim_dialog.tail(3).items())}")

    # ── Model fit ──
    out("\n## Model Fit Summary")
    # Variance explained
    ss_total = np.sum((df["score"].values - df["score"].mean()) ** 2)
    pred = np.array([mu + theta[d] - delta[r] - beta[q]
                     for d, r, q in zip(df["dialog"], df["rater"], df["item"])])
    ss_resid = np.sum((df["score"].values - pred) ** 2)
    r_squared = 1 - ss_resid / ss_total
    out(f"- R-squared: {r_squared:.4f} ({r_squared*100:.1f}% of variance explained)")
    out(f"- RMSE: {rmse:.4f}")
    out(f"- Total SS: {ss_total:.2f}, Residual SS: {ss_resid:.2f}")

    # Facet variance contributions
    theta_var = np.var(list(theta.values()))
    delta_var = np.var(list(delta.values()))
    beta_var  = np.var(list(beta.values()))
    total_facet_var = theta_var + delta_var + beta_var
    out(f"\n### Variance Decomposition of Facet Effects")
    out(f"- Dialog quality (theta): variance = {theta_var:.4f} ({theta_var/total_facet_var*100:.1f}%)")
    out(f"- Rater severity (delta): variance = {delta_var:.4f} ({delta_var/total_facet_var*100:.1f}%)")
    out(f"- Item difficulty (beta): variance = {beta_var:.4f} ({beta_var/total_facet_var*100:.1f}%)")

    out("\n---")
    out("*Generated by analysis_mfrm.py using iterative least-squares MFRM estimation.*")

    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  Many-Facet Rasch Model (MFRM) Analysis")
    print("=" * 70)

    df = load_data()

    print("\n--- Estimating MFRM parameters ---")
    mu, theta, delta, beta, rmse = estimate_mfrm(df)

    print("\n" + "=" * 70)
    report = print_and_report(df, mu, theta, delta, beta, rmse)

    outfile = f"analysis_mfrm_{date.today()}.md"
    with open(outfile, "w") as f:
        f.write(report)
    print(f"\nReport saved to {outfile}")


if __name__ == "__main__":
    main()
