import streamlit as st
import numpy as np
import joblib
from db_utils import authorized_emails

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="FraudSense AI",
    layout="centered"
)

# =====================================================
# CREATIVE UI CSS
# =====================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #141e30, #243b55, #6a11cb, #2575fc);
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
    font-size: 50px;
    font-weight: 900;
    text-align: center;
    color: #ffffff;
}
.hero-subtitle {
    font-size: 18px;
    text-align: center;
    color: #e0e0e0;
    margin-bottom: 30px;
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
st.markdown("<div class='hero-title'>🧠 FraudSense AI</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-subtitle'>Multi-layer Fraud Detection with Trust Intelligence</div>",
    unsafe_allow_html=True
)

st.image(
    "https://illustrations.popsy.co/white/artificial-intelligence.svg",
    use_container_width=True
)

st.divider()

# =====================================================
# FEATURE MODULES
# =====================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='glass-card' style='text-align:center;'>📧<h3>Email Fraud</h3></div>", unsafe_allow_html=True)
    if st.button("Explore", key="email"):
        st.switch_page("pages/2_Email_Fraud_Detection.py")

with col2:
    st.markdown("<div class='glass-card' style='text-align:center;'>🧩<h3>Scenario Fraud</h3></div>", unsafe_allow_html=True)
    if st.button("Explore", key="scenario"):
        st.switch_page("pages/3_Scenario_Fraud_Detection.py")

with col3:
    st.markdown("<div class='glass-card' style='text-align:center;'>🤖<h3>AI Chatbot</h3></div>", unsafe_allow_html=True)
    if st.button("Chat", key="chatbot"):
        st.switch_page("pages/v_chatbot.py")




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














