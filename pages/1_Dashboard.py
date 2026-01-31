import streamlit as st
import pandas as pd
import plotly.express as px

from db_utils import authorized_emails, email_logs

st.set_page_config(page_title="FraudSense AI | Dashboard", layout="wide")

# -------------------------------------------------
# DATABASE METRICS
# -------------------------------------------------
trusted_email_count = authorized_emails.count_documents({})
email_log_count = email_logs.count_documents({})

# Mock values (can be replaced later)
legit_txns = 5
fraud_txns = 1

# Trust score formula (same logic you explained)
trust_score = (trusted_email_count * 10) + (legit_txns * 5) - (fraud_txns * 20)
trust_score = max(0, min(100, trust_score))

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("## 📊 FraudSense AI – Trust Dashboard")

st.success(
    f"✅ MongoDB Connected | Trusted Emails: {trusted_email_count} | Email Logs: {email_log_count}"
)

# -------------------------------------------------
# TRUST SCORE GAUGE
# -------------------------------------------------
st.subheader("🔐 Trust Score")

gauge_df = pd.DataFrame({
    "score": [trust_score],
    "label": ["Trust Score"]
})

fig_gauge = px.bar(
    gauge_df,
    x="score",
    y="label",
    orientation="h",
    range_x=[0, 100],
    color="score",
    color_continuous_scale=["red", "yellow", "green"],
    text="score"
)

fig_gauge.update_layout(
    height=200,
    xaxis_title="Trust Level",
    yaxis_title="",
    coloraxis_showscale=False
)

st.plotly_chart(fig_gauge, use_container_width=True)

# -------------------------------------------------
# EMAIL TRUST BREAKDOWN
# -------------------------------------------------
st.subheader("📧 Email Trust Breakdown")

email_df = pd.DataFrame({
    "Category": ["Trusted Emails", "Unknown Emails"],
    "Count": [trusted_email_count, max(0, email_log_count - trusted_email_count)]
})

fig_email = px.bar(
    email_df,
    x="Category",
    y="Count",
    color="Category",
    title="Email Risk Classification"
)

st.plotly_chart(fig_email, use_container_width=True)

# -------------------------------------------------
# TRANSACTION DISTRIBUTION
# -------------------------------------------------
st.subheader("💳 Transaction Outcomes")

txn_df = pd.DataFrame({
    "Type": ["Legitimate", "Fraudulent"],
    "Count": [legit_txns, fraud_txns]
})

fig_txn = px.pie(
    txn_df,
    names="Type",
    values="Count",
    title="ML Transaction Classification"
)

st.plotly_chart(fig_txn, use_container_width=True)

# -------------------------------------------------
# INSIGHTS
# -------------------------------------------------
st.subheader("🧠 Key Insights")

st.markdown("""
- ✅ Trust score increases as verified emails and safe transactions grow  
- 🚨 Unknown emails are treated as risky by default  
- 🤖 ML + Rules + MongoDB = layered fraud protection  
""")

if trust_score >= 80:
    st.success("🟢 System is highly trusted")
elif trust_score >= 50:
    st.warning("🟡 System should be monitored")
else:
    st.error("🔴 System is currently high risk")

