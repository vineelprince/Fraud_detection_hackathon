import streamlit as st

st.set_page_config(
    page_title="Scenario Fraud Detection",
    layout="centered"
)

st.markdown("## 🧩 Scenario-based Fraud Detection")
st.write("Enter a real-life situation and the system will analyze whether it is fraud or not, along with reasons.")

st.divider()

scenario = st.text_area(
    "✍️ Describe the situation",
    placeholder="Example: Someone called me asking for my OTP urgently...",
    height=150
)

# Fraud keywords
fraud_keywords = [
    "otp", "password", "pin", "urgent", "immediately",
    "click", "link", "lottery", "prize", "refund",
    "unknown", "crypto", "investment", "transfer"
]

safe_keywords = [
    "bank branch", "official", "statement",
    "college", "government", "no link",
    "id proof", "verified"
]

if st.button("🔍 Analyze Scenario"):

    scenario_lower = scenario.lower()
    reasons = []
    is_fraud = False

    # Check fraud indicators
    for word in fraud_keywords:
        if word in scenario_lower:
            is_fraud = True
            reasons.append(f"Contains suspicious keyword: '{word}'")

    # Check safe indicators
    for word in safe_keywords:
        if word in scenario_lower:
            reasons.append(f"Mentions trusted context: '{word}'")

    st.divider()

    if is_fraud:
        st.error("🚨 FRAUD DETECTED")

        st.markdown("### ❗ Reasons:")
        for r in reasons:
            st.markdown(f"- {r}")

        st.markdown(
            "> ⚠️ This scenario involves urgency, sensitive information, or suspicious requests commonly seen in fraud cases."
        )

    else:
        st.success("✅ NOT FRAUD")

        if reasons:
            st.markdown("### ✔ Reasons:")
            for r in reasons:
                st.markdown(f"- {r}")
        else:
            st.markdown(
                "- No suspicious keywords detected\n"
                "- No request for sensitive information\n"
                "- Appears to be a normal and safe interaction"
            )

        st.markdown(
            "> 👍 This scenario does not show common fraud indicators."
        )


