import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Fraud Assistant Chatbot",
    layout="centered"
)

# =====================================================
# UI
# =====================================================
st.markdown("## 🤖 Fraud Assistant Chatbot")
st.write(
    "Ask questions about transaction fraud, email fraud, scenario detection, "
    "ML model behavior, and trusted customers."
)

st.divider()

# =====================================================
# CHAT MEMORY
# =====================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =====================================================
# CHATBOT BRAIN (RULE-BASED)
# =====================================================
def fraud_chatbot(user_input):
    text = user_input.lower()

    if "email" in text:
        return (
            "📧 **Email Fraud Detection** works by identifying suspicious email patterns. "
            "Emails from unknown or free domains and those asking for urgent actions are more risky."
        )

    elif "scenario" in text:
        return (
            "🧩 **Scenario-based Fraud Detection** analyzes real-life situations for red flags "
            "like urgency, OTP requests, unusual transfers, or unknown senders."
        )

    elif "ml" in text or "model" in text:
        return (
            "🤖 **ML Fraud Detection** uses a Logistic Regression model trained on transaction data. "
            "It considers transaction type, amount, and balance changes to detect fraud."
        )

    elif "cash out" in text:
        return (
            "⚠️ **CASH_OUT transactions** are risky because fraudsters often withdraw money immediately "
            "after gaining unauthorized access."
        )

    elif "trusted" in text or "trust score" in text:
        return (
            "✅ A **Trusted Customer** has a high trust score based on consistent safe behavior across "
            "transactions, emails, and scenarios."
        )

    elif "fraud" in text:
        return (
            "🚨 **Fraud** refers to suspicious or unauthorized activities aimed at stealing money or data. "
            "Our system detects fraud using ML, email analysis, and scenario intelligence."
        )

    else:
        return (
            "🤔 I didn’t understand that clearly.\n\n"
            "Try asking about:\n"
            "- Email fraud\n"
            "- Scenario fraud\n"
            "- ML model\n"
            "- CASH_OUT risk\n"
            "- Trusted customers"
        )

# =====================================================
# USER INPUT
# =====================================================
user_input = st.text_input("💬 Ask a question")

if st.button("Ask"):
    if user_input.strip() != "":
        reply = fraud_chatbot(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Assistant", reply))

# =====================================================
# DISPLAY CHAT
# =====================================================
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Assistant:** {message}")
