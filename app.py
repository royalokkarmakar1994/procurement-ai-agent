import streamlit as st
import pandas as pd
import os
from scorer import score_vendors, get_summary_text
from agent import get_recommendation

st.set_page_config(
    page_title="Procurement AI Agent",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Procurement AI Agent")
st.markdown(
    "Upload vendor data, score them automatically, and get **AI-powered procurement recommendations**."
)
st.divider()

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Your Groq API key. Free at console.groq.com",
    )
    st.markdown("---")
    st.header("📋 Context (Optional)")
    user_context = st.text_area(
        "Tell the AI about your procurement needs",
        placeholder="e.g., We need delivery within 7 days. Budget is tight. Quality is the top priority.",
        height=130,
    )
    top_n = st.slider("Top vendors to analyse", min_value=2, max_value=5, value=3)

st.subheader("📂 Step 1 — Load Vendor Data")

data_source = st.radio(
    "Choose data source:",
    ["Use sample data (demo)", "Upload your own CSV"],
    horizontal=True,
)

df_raw = None

if data_source == "Use sample data (demo)":
    sample_path = os.path.join(os.path.dirname(__file__), "data", "vendors.csv")
    df_raw = pd.read_csv(sample_path)
    st.success("✅ Sample vendor data loaded.")
else:
    uploaded = st.file_uploader(
        "Upload a CSV with columns: vendor_name, unit_price_usd, delivery_days, "
        "quality_score, reliability_score, payment_terms_days, past_disputes",
        type=["csv"],
    )
    if uploaded:
        df_raw = pd.read_csv(uploaded)
        st.success(f"✅ Uploaded: {uploaded.name} ({len(df_raw)} vendors)")

if df_raw is not None:
    with st.expander("📄 View Raw Vendor Data", expanded=False):
        st.dataframe(df_raw, use_container_width=True)

    st.divider()
    st.subheader("📊 Step 2 — Vendor Scoring")

    scored_df = score_vendors(df_raw)

    display_cols = [
        "rank", "vendor_name", "total_score",
        "unit_price_usd", "delivery_days",
        "quality_score", "reliability_score",
        "payment_terms_days", "past_disputes",
    ]

    st.dataframe(
        scored_df[display_cols].rename(columns={
            "rank": "Rank",
            "vendor_name": "Vendor",
            "total_score": "Score /10",
            "unit_price_usd": "Price (USD)",
            "delivery_days": "Delivery (days)",
            "quality_score": "Quality",
            "reliability_score": "Reliability",
            "payment_terms_days": "Payment Terms",
            "past_disputes": "Disputes",
        }),
        use_container_width=True,
    )

    st.bar_chart(
        scored_df.set_index("vendor_name")["total_score"],
        use_container_width=True,
    )

    st.divider()
    st.subheader("🤖 Step 3 — AI Procurement Recommendation")

    if not api_key:
        st.warning("⚠️ Enter your Groq API key in the sidebar to enable AI recommendations.")
    else:
        if st.button("🚀 Generate AI Recommendation", type="primary"):
            with st.spinner("Analysing vendors and generating recommendation..."):
                try:
                    vendor_summary = get_summary_text(scored_df, top_n=top_n)
                    recommendation = get_recommendation(
                        vendor_summary=vendor_summary,
                        context=user_context,
                        api_key=api_key,
                    )
                    st.success("✅ Recommendation ready!")
                    st.markdown("### 📋 AI Recommendation")
                    st.markdown(recommendation)

                    st.download_button(
                        label="⬇️ Download Recommendation (TXT)",
                        data=recommendation,
                        file_name="procurement_recommendation.txt",
                        mime="text/plain",
                    )
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("Built with Python · LangChain · Groq LLaMA 3 · Streamlit · Pandas")
