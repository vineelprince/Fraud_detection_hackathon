import streamlit as st
import numpy as np
import joblib
from db_utils import authorized_emails

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="FraudSense AI",
    layout="wide"
)

# =====================================================
# CREATIVE UI CSS
# =====================================================
st.markdown("""
<style>
:root {
    --deep-navy: #0b1220;
    --night-sky: #101b33;
    --indigo: #2b1b6d;
    --accent: #62d2ff;
    --soft-white: rgba(255, 255, 255, 0.88);
}
.stApp {
    background: linear-gradient(-45deg, #0b1220, #101b33, #2b1b6d, #0f2a52);
    background-size: 400% 400%;
    animation: gradientBG 18s ease infinite;
    font-family: 'Poppins', sans-serif;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.hero-title {
    font-size: 56px;
    font-weight: 900;
    text-align: left;
    color: #ffffff;
}
.hero-subtitle {
    font-size: 20px;
    text-align: left;
    color: var(--soft-white);
    margin-bottom: 20px;
    line-height: 1.6;
}
.glass-card {
    background: rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 25px;
    margin-bottom: 25px;
    color: white;
    box-shadow: 0 10px 35px rgba(0,0,0,0.35);
}
.feature-card {
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 22px;
    border-radius: 20px;
    color: white;
    box-shadow: 0 14px 40px rgba(0,0,0,0.35);
    height: 100%;
}
.feature-title {
    font-size: 20px;
    font-weight: 700;
}
.pill {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(98, 210, 255, 0.16);
    color: #9be7ff;
    font-size: 13px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}
.section-title {
    font-size: 28px;
    font-weight: 800;
    color: white;
    margin-bottom: 5px;
}
.section-subtitle {
    color: var(--soft-white);
    margin-bottom: 20px;
}
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    margin: 10px 0 30px;
}
.trusted-logo {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 12px 16px;
    text-align: center;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
    letter-spacing: 0.6px;
}
.signal-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: white;
    height: 100%;
}
.signal-title {
    font-weight: 700;
    font-size: 18px;
    margin-bottom: 6px;
}
.cta-card {
    background: linear-gradient(120deg, rgba(98, 210, 255, 0.18), rgba(255, 81, 47, 0.15));
    border-radius: 24px;
    padding: 24px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: white;
}
.stButton>button {
    background: linear-gradient(135deg, #ff512f, #dd2476);
    color: white;
    font-size: 16px;
    font-weight: 700;
    padding: 12px 22px;
    border-radius: 14px;
}
.badge-fraud {
    background: #ff3b3b;
    padding: 6px 14px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
}
.badge-safe {
    background: #00e676;
    padding: 6px 14px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    color: black;
}
.metric-card {
    background: rgba(255, 255, 255, 0.12);
    padding: 18px 20px;
    border-radius: 16px;
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.12);
}
.metric-number {
    font-size: 26px;
    font-weight: 800;
}
.chat-chip {
    background: rgba(255, 255, 255, 0.15);
    padding: 8px 14px;
    border-radius: 18px;
    margin-right: 8px;
    display: inline-block;
    font-size: 13px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD ML COMPONENTS
# =====================================================
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")

# =====================================================
# SESSION STATE
# =====================================================
if "transactions" not in st.session_state:
    st.session_state.transactions = {}

if "trust_scores" not in st.session_state:
    st.session_state.trust_scores = {}

if "active_dialog" not in st.session_state:
    st.session_state.active_dialog = None

# =====================================================
# MONGODB STATUS (PROOF)
# =====================================================
st.markdown("### 📡 Database Status")
try:
    count = authorized_emails.count_documents({})
    st.success(f"✅ MongoDB Connected | Trusted Emails: {count}")
except Exception as e:
    st.error("❌ MongoDB Connection Failed")
    st.write(e)

st.divider()

# =====================================================
# HERO SECTION
# =====================================================
hero_left, hero_right = st.columns([1.1, 0.9], gap="large")
with hero_left:
    st.markdown("<div class='pill'>AI-Powered RiskOps</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-title'>🧠 FraudSense AI</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='hero-subtitle'>Deliver a premium fraud defense experience with "
        "dynamic risk scoring, behavioral intelligence, and adaptive signals built "
        "for modern fintech teams.</div>",
        unsafe_allow_html=True
    )
    if st.button("Launch the AI Suite →"):
        st.switch_page("pages/1_Dashboard.py")
    st.markdown(
        "<span class='chat-chip'>Risk Scoring</span>"
        "<span class='chat-chip'>Behavioral Signals</span>"
        "<span class='chat-chip'>Trusted Customers</span>",
        unsafe_allow_html=True
    )

with hero_right:
    st.image(
        "https://illustrations.popsy.co/white/artificial-intelligence.svg",
        use_container_width=True
    )
    metric_cols = st.columns(2)
    with metric_cols[0]:
        st.markdown(
            "<div class='metric-card'><div class='metric-number'>99.2%</div>Detection Precision</div>",
            unsafe_allow_html=True
        )
    with metric_cols[1]:
        st.markdown(
            "<div class='metric-card'><div class='metric-number'>4.8s</div>Risk Response</div>",
            unsafe_allow_html=True
        )

st.divider()

# =====================================================
# INSPIRATION SECTION
# =====================================================
st.markdown("<div class='section-title'>✨ Inspired by Elite Fraud Platforms</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='section-subtitle'>Experience a premium-first interface that mirrors the clarity "
    "and confidence of industry leaders.</div>",
    unsafe_allow_html=True
)

trusted_cols = st.columns(5)
trusted_labels = ["TRUSTED BY", "E-COMMERCE", "NEO BANKS", "PAYMENTS", "CRYPTO"]
for col, label in zip(trusted_cols, trusted_labels):
    with col:
        st.markdown(f"<div class='trusted-logo'>{label}</div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

inspire_cols = st.columns(3)
inspiration = [
    ("Sift", "AI-driven fraud detection and dynamic risk scoring for e-commerce."),
    ("Feedzai", "Comprehensive, real-time RiskOps for banking and fintech."),
    ("Signifyd", "Guaranteed fraud protection and chargeback coverage."),
    ("SEON", "Flexible API-based detection with social and digital footprinting."),
    ("Salv Bridge", "Collaborative detection between institutions with rapid recovery."),
    ("BioCatch", "Behavioral biometrics that analyze motion and typing signals.")
]
for idx, (title, desc) in enumerate(inspiration):
    with inspire_cols[idx % 3]:
        st.markdown(
            f"<div class='feature-card'><div class='feature-title'>{title}</div>"
            f"<p style='color:var(--soft-white);margin-top:8px;'>{desc}</p></div>",
            unsafe_allow_html=True
        )

st.divider()

# =====================================================
# FEATURE MODULES
# =====================================================
st.markdown("<div class='section-title'>🚀 Core Modules</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='section-subtitle'>Deploy multi-layer protection in minutes across "
    "email, transaction, and conversational channels.</div>",
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        "<div class='feature-card'>📧<div class='feature-title'>Email Fraud</div>"
        "<p style='color:var(--soft-white);'>Verify trusted senders, detect phishing, "
        "and enrich email intelligence.</p></div>",
        unsafe_allow_html=True
    )
    if st.button("Explore", key="email"):
        st.switch_page("pages/2_Email_Fraud_Detection.py")

with col2:
    st.markdown(
        "<div class='feature-card'>🧩<div class='feature-title'>Scenario Fraud</div>"
        "<p style='color:var(--soft-white);'>Simulate real-world attack patterns and "
        "triage high-risk behaviors.</p></div>",
        unsafe_allow_html=True
    )
    if st.button("Explore", key="scenario"):
        st.switch_page("pages/3_Scenario_Fraud_Detection.py")

with col3:
    st.markdown(
        "<div class='feature-card'>🤖<div class='feature-title'>AI Assistant</div>"
        "<p style='color:var(--soft-white);'>Instant guidance, policy insights, "
        "and fraud education with a premium chat UI.</p></div>",
        unsafe_allow_html=True
    )
    if st.button("Chat", key="chatbot"):
        st.switch_page("pages/v_chatbot.py")

st.divider()

# =====================================================
# SIGNAL INTELLIGENCE
# =====================================================
st.markdown("<div class='section-title'>🛰️ Signal Intelligence</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='section-subtitle'>Blend device, identity, behavioral, and transaction "
    "signals into a unified risk narrative.</div>",
    unsafe_allow_html=True
)

signal_cols = st.columns(3, gap="large")
signals = [
    ("Device & Identity", "Detect anomalies across device fingerprints, geolocation, and session hygiene."),
    ("Behavioral Biometrics", "Spot account takeover by analyzing typing cadence and mouse velocity."),
    ("Network & Velocity", "Catch rapid-fire transactions, mule rings, and coordinated attacks.")
]
for col, (title, desc) in zip(signal_cols, signals):
    with col:
        st.markdown(
            f"<div class='signal-card'><div class='signal-title'>{title}</div>"
            f"<p style='color:var(--soft-white);margin-top:6px;'>{desc}</p></div>",
            unsafe_allow_html=True
        )

st.divider()

# =====================================================
# CTA SECTION
# =====================================================
cta_left, cta_right = st.columns([1.2, 0.8], gap="large")
with cta_left:
    st.markdown(
        "<div class='cta-card'><div class='section-title'>Ready to orchestrate RiskOps?</div>"
        "<p style='color:var(--soft-white);margin-top:8px;'>Launch workflows that pair ML "
        "scoring with trusted-customer intelligence. Add a transaction below to see "
        "the trust score engine respond.</p></div>",
        unsafe_allow_html=True
    )
with cta_right:
    st.markdown(
        "<div class='metric-card'><div class='metric-number'>4 Layers</div>Signals + ML + Rules + Trust</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='metric-card' style='margin-top:12px;'><div class='metric-number'>24/7</div>Continuous Monitoring</div>",
        unsafe_allow_html=True
    )

st.divider()

# =====================================================
# ADD TRANSACTION
# =====================================================
if st.button("➕ Add Customer Transaction"):
    st.session_state.active_dialog = "new_transaction"

# =====================================================
# TRANSACTION POPUP
# =====================================================
@st.dialog("🧾 New Customer Transaction")
def new_transaction_popup():

    customer_name = st.text_input("👤 Customer Name")
    email = st.text_input("📧 Customer Email")

    transaction_type = st.selectbox(
        "Transaction Type",
        ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN", "EMAIL"]
    )

    amount = st.number_input("Amount", min_value=0.0)
    oldbalanceOrg = st.number_input("Sender Old Balance", min_value=0.0)
    newbalanceOrg = st.number_input("Sender New Balance", min_value=0.0)
    oldbalanceDest = st.number_input("Receiver Old Balance", min_value=0.0)
    newbalanceDest = st.number_input("Receiver New Balance", min_value=0.0)

    if st.button("Analyze & Save"):
        if customer_name == "" or email == "":
            st.warning("Enter customer name and email")
            return

        # Initialize trust score
        if customer_name not in st.session_state.trust_scores:
            st.session_state.trust_scores[customer_name] = 50

        # EMAIL → MongoDB only
        if transaction_type == "EMAIL":
            if not authorized_emails.find_one({"email": email.lower()}):
                authorized_emails.insert_one({"email": email.lower()})
                st.success("📧 Email saved as trusted")
                st.session_state.trust_scores[customer_name] += 10
            else:
                st.info("Email already trusted")
            return

        # ML Prediction
        t = encoder.transform([transaction_type])[0]
        data = np.array([[t, amount, oldbalanceOrg, newbalanceOrg, oldbalanceDest, newbalanceDest]])
        data = scaler.transform(data)

        prediction = model.predict(data)[0]
        result = "Fraudulent" if prediction == 1 else "Legitimate"

        # Update trust score
        if prediction == 1:
            st.session_state.trust_scores[customer_name] -= 20
        else:
            st.session_state.trust_scores[customer_name] += 5

        # Clamp score
        score = st.session_state.trust_scores[customer_name]
        st.session_state.trust_scores[customer_name] = max(0, min(100, score))

        record = {
            "Email": email,
            "Type": transaction_type,
            "Amount": amount,
            "Status": result
        }

        st.session_state.transactions.setdefault(customer_name, []).append(record)

        if prediction == 1:
            st.error("🚨 Fraudulent Transaction")
        else:
            st.success("✅ Transaction Saved")

    if st.button("Close"):
        st.session_state.active_dialog = None

# =====================================================
# CUSTOMER PORTFOLIO (WITH TRUST SCORE)
# =====================================================
st.divider()
st.subheader("👥 Customer Portfolio")

if st.session_state.transactions:
    for customer, records in st.session_state.transactions.items():

        score = st.session_state.trust_scores.get(customer, 50)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(f"### 👤 {customer}")

        if score >= 80:
            st.markdown(f"<span class='badge-safe'>🟢 Trust Score: {score} (Highly Trusted)</span>", unsafe_allow_html=True)
        elif score >= 50:
            st.markdown(f"<span style='background:#ffc107;padding:6px 14px;border-radius:12px;'>🟡 Trust Score: {score} (Monitor)</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='badge-fraud'>🔴 Trust Score: {score} (High Risk)</span>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No customers added yet.")

# =====================================================
# DIALOG CONTROLLER
# =====================================================
if st.session_state.active_dialog == "new_transaction":
    new_transaction_popup()














