import streamlit as st
import re

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Email Fraud Detection",
    layout="centered"
)

# =====================================================
# CREATIVE UI
# =====================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364);
    background-size: 400% 400%;
    animation: gradientBG 18s ease infinite;
    color: white;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.glass-card {
    background: rgba(255,255,255,0.18);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 25px;
    margin-top: 25px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.35);
}

.badge-safe {
    background: #00e676;
    padding: 6px 14px;
    border-radius: 12px;
    font-weight: bold;
    color: black;
}

.badge-fraud {
    background: #ff3b3b;
    padding: 6px 14px;
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================
st.markdown("<h1 style='text-align:center;'>📧 Email Fraud Detection</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>Rule-based & memory-driven email trust validation</p>",
    unsafe_allow_html=True
)

st.image(
    "https://illustrations.popsy.co/white/email-campaign.svg",
    width=180
)

# =====================================================
# SESSION STATE (EMAIL MEMORY)
# =====================================================
if "trusted_emails" not in st.session_state:
    st.session_state.trusted_emails = set()

# =====================================================
# LOAD TRUSTED EMAILS FROM MAIN APP TRANSACTIONS
# =====================================================
if "transactions" in st.session_state:
    for customer, records in st.session_state.transactions.items():
        for r in records:
            if "Email" in r and r["Email"]:
                st.session_state.trusted_emails.add(r["Email"].lower())

# =====================================================
# EMAIL INPUT
# =====================================================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

email = st.text_input("📨 Enter Email Address")

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# =====================================================
# CHECK BUTTON
# =====================================================
if st.button("🔍 Analyze Email"):
    if not email:
        st.warning("Please enter an email address")

    elif not is_valid_email(email):
        st.error("❌ Invalid email format")

    else:
        email = email.lower()

        # TRUST LOGIC
        if email in st.session_state.trusted_emails:
            st.success("✅ SAFE EMAIL — Trusted user")
            st.markdown("<span class='badge-safe'>Trusted</span>", unsafe_allow_html=True)

        else:
            # FRAUD POPUP
            @st.dialog("🚨 Email Fraud Alert")
            def fraud_popup():
                st.markdown("### ⚠ Suspicious Email Detected")
                st.write("This email is **NOT found** in trusted customer records.")
                st.write("Recommended Action:")
                st.write("- Verify sender identity")
                st.write("- Avoid clicking links")
                st.write("- Flag for investigation")

                if st.button("Close"):
                    pass

            fraud_popup()
            st.error("🚨 FRAUD EMAIL — Unknown sender")
            st.markdown("<span class='badge-fraud'>High Risk</span>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# TRUSTED EMAIL LIST (OPTIONAL DISPLAY)
# =====================================================
with st.expander("📂 View Trusted Emails"):
    if st.session_state.trusted_emails:
        for e in st.session_state.trusted_emails:
            st.write("✔", e)
    else:
        st.info("No trusted emails saved yet")





