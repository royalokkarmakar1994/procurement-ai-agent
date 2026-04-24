import pandas as pd

# ─────────────────────────────────────────────
# Scoring Weights — adjust to match your use case
# ─────────────────────────────────────────────
WEIGHTS = {
    "price_score": 0.30,
    "delivery_score": 0.25,
    "quality_score": 0.20,
    "reliability_score": 0.15,
    "payment_score": 0.07,
    "dispute_penalty": 0.03,
}


def normalize_inverse(series: pd.Series) -> pd.Series:
    """Lower is better — normalize so lowest value = 10."""
    return 10 - (series - series.min()) / (series.max() - series.min() + 1e-9) * 10


def normalize(series: pd.Series) -> pd.Series:
    """Higher is better — normalize to 0–10."""
    return (series - series.min()) / (series.max() - series.min() + 1e-9) * 10


def score_vendors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes raw vendor DataFrame and returns scored + ranked DataFrame.
    """
    scored = df.copy()

    # Normalize each criterion
    scored["price_score"] = normalize_inverse(df["unit_price_usd"])
    scored["delivery_score"] = normalize_inverse(df["delivery_days"])
    scored["quality_score_norm"] = normalize(df["quality_score"])
    scored["reliability_score_norm"] = normalize(df["reliability_score"])
    scored["payment_score"] = normalize(df["payment_terms_days"])
    scored["dispute_penalty"] = normalize_inverse(df["past_disputes"])

    # Weighted composite score
    scored["total_score"] = (
        scored["price_score"] * WEIGHTS["price_score"]
        + scored["delivery_score"] * WEIGHTS["delivery_score"]
        + scored["quality_score_norm"] * WEIGHTS["quality_score"]
        + scored["reliability_score_norm"] * WEIGHTS["reliability_score"]
        + scored["payment_score"] * WEIGHTS["payment_score"]
        + scored["dispute_penalty"] * WEIGHTS["dispute_penalty"]
    ).round(2)

    # Rank vendors
    scored["rank"] = scored["total_score"].rank(ascending=False).astype(int)
    scored = scored.sort_values("total_score", ascending=False).reset_index(drop=True)

    return scored


def get_summary_text(scored_df: pd.DataFrame, top_n: int = 3) -> str:
    """
    Converts top-N scored vendors into plain text for the LLM.
    """
    top = scored_df.head(top_n)
    lines = ["Top Vendor Scores (weighted composite out of 10):\n"]
    for _, row in top.iterrows():
        lines.append(
            f"- {row['vendor_name']}: Score={row['total_score']}/10 | "
            f"Price=${row['unit_price_usd']} | Delivery={row['delivery_days']} days | "
            f"Quality={row['quality_score']}/10 | Reliability={row['reliability_score']}/10 | "
            f"Payment Terms={row['payment_terms_days']} days | Past Disputes={row['past_disputes']}"
        )
    return "\n".join(lines)
