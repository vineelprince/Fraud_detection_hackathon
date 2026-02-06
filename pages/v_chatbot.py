import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Fraud Assistant Chatbot",
    layout="wide"
)

# =====================================================
# UI
# =====================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #0b1220, #101b33, #1b2a6d);
    color: #ffffff;
    font-family: 'Poppins', sans-serif;
}
.chat-hero {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 28px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
}
.hero-title {
    font-size: 34px;
    font-weight: 800;
}
.hero-subtitle {
    color: rgba(255, 255, 255, 0.84);
    line-height: 1.6;
}
.chip {
    display: inline-block;
    margin: 6px 6px 0 0;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(98, 210, 255, 0.18);
    color: #9be7ff;
    font-size: 13px;
}
.panel {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 18px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.panel-title {
    font-weight: 700;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

hero_left, hero_right = st.columns([1.2, 0.8], gap="large")
with hero_left:
    st.markdown(
        "<div class='chat-hero'>"
        "<div class='hero-title'>🤖 FraudSense Assistant</div>"
        "<p class='hero-subtitle'>Your premium fraud analyst for risk scoring, behavioral signals, "
        "and transaction guidance. Ask anything about fraud patterns or request a mitigation checklist.</p>"
        "<span class='chip'>Risk Scoring</span>"
        "<span class='chip'>Behavioral Biometrics</span>"
        "<span class='chip'>Chargeback Defense</span>"
        "</div>",
        unsafe_allow_html=True
    )
with hero_right:
    st.markdown(
        "<div class='panel'>"
        "<div class='panel-title'>Assistant Capabilities</div>"
        "<ul>"
        "<li>Explain why a transaction is risky</li>"
        "<li>Summarize suspicious email traits</li>"
        "<li>Provide scenario-based mitigation tips</li>"
        "<li>Suggest next-best actions for agents</li>"
        "</ul>"
        "</div>",
        unsafe_allow_html=True
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
def format_response(title, summary, actions):
    bullet_list = "\n".join([f"- {item}" for item in actions])
    return (
        f"### {title}\n"
        f"{summary}\n\n"
        f"**Recommended Actions**\n{bullet_list}"
    )

def fraud_chatbot(user_input):
    text = user_input.lower()

    if any(keyword in text for keyword in ["email", "phishing", "inbox"]):
        return format_response(
            "📧 Email Fraud Detection",
            "We focus on suspicious sender domains, spoofing cues, urgent payment requests, "
            "and mismatched reply-to addresses that signal phishing or BEC attempts.",
            [
                "Verify unknown senders with callback verification",
                "Enforce domain allow-lists for sensitive workflows",
                "Log high-risk inbox events into the case queue"
            ]
        )

    if any(keyword in text for keyword in ["scenario", "story", "situation", "case"]):
        return format_response(
            "🧩 Scenario Detection",
            "Behavior-based red flags include urgency, OTP requests, new device logins, "
            "or sudden beneficiary changes.",
            [
                "Trigger step-up verification for stacked risk signals",
                "Route to manual review if behavior deviates from baseline",
                "Capture device/location metadata for audit trails"
            ]
        )

    if any(keyword in text for keyword in ["ml", "model", "machine learning", "predict"]):
        return format_response(
            "🤖 ML Risk Scoring",
            "The model evaluates transaction type, amount, and balance deltas to score risk in real time.",
            [
                "Surface the risk score alongside analyst notes",
                "Tune thresholds based on false-positive tolerance",
                "Combine ML scores with rule-based overrides"
            ]
        )

    if "cash out" in text or "cashout" in text:
        return format_response(
            "⚠️ CASH_OUT Risk",
            "CASH_OUT is high-risk because fraudsters often withdraw funds immediately after account takeover.",
            [
                "Apply velocity limits for repeated cash-out attempts",
                "Require step-up verification for unusual withdrawals",
                "Freeze accounts with repeated high-risk signals"
            ]
        )

    if any(keyword in text for keyword in ["trusted", "trust score", "trust"]):
        return format_response(
            "✅ Trust Score Guidance",
            "Trusted customers maintain stable behavior across transactions, emails, and scenarios.",
            [
                "Re-verify if signals change suddenly or new devices appear",
                "Reward safe history with faster approvals",
                "Log trust score changes for audit transparency"
            ]
        )

    if any(keyword in text for keyword in ["fraud", "chargeback", "risk"]):
        return format_response(
            "🚨 Fraud & Chargeback Risk",
            "Fraud signals often emerge from identity mismatches, velocity spikes, and policy violations.",
            [
                "Review chargeback history for similar merchants",
                "Pause high-risk transactions until verified",
                "Share fraud intelligence with partner teams"
            ]
        )

    if any(keyword in text for keyword in ["behavior", "biometric", "mouse", "typing"]):
        return format_response(
            "🧬 Behavioral Biometrics",
            "Mouse movement, typing speed, and session patterns can reveal account takeover attempts.",
            [
                "Compare sessions against customer baseline profiles",
                "Trigger MFA on high-confidence anomalies",
                "Record biometric drift for analyst review"
            ]
        )

    if any(keyword in text for keyword in ["playbook", "checklist", "mitigation", "next steps"]):
        return format_response(
            "🧭 Rapid Response Playbook",
            "Use this checklist when a high-risk event is detected.",
            [
                "Confirm identity with step-up authentication",
                "Place a temporary hold and notify the customer",
                "Document signals, timestamps, and analyst notes",
                "Escalate to risk ops for coordinated action"
            ]
        )

    return (
        "🤔 I didn’t understand that clearly.\n\n"
        "Try asking about:\n"
        "- Email fraud signals\n"
        "- Scenario fraud response\n"
        "- ML risk scoring\n"
        "- CASH_OUT risk\n"
        "- Trust score guidance\n"
        "- Behavioral biometrics"
    )

# =====================================================
# USER INPUT
# =====================================================
quick_col1, quick_col2, quick_col3, quick_col4 = st.columns([1, 1, 1, 0.6])
with quick_col1:
    if st.button("Explain email fraud"):
        st.session_state.chat_history.append(("You", "Explain email fraud signals."))
with quick_col2:
    if st.button("Scenario mitigation tips"):
        st.session_state.chat_history.append(("You", "Give scenario mitigation tips."))
with quick_col3:
    if st.button("Behavioral biometrics"):
        st.session_state.chat_history.append(("You", "How does behavioral biometrics help?"))
with quick_col4:
    if st.button("Clear chat"):
        st.session_state.chat_history = []

user_input = st.chat_input("💬 Ask about fraud detection, trust scoring, or risk signals")
if user_input:
    st.session_state.chat_history.append(("You", user_input))

# =====================================================
# DISPLAY CHAT
# =====================================================
for sender, message in st.session_state.chat_history:
    if sender == "You":
        with st.chat_message("user"):
            st.markdown(message)
    else:
        with st.chat_message("assistant"):
            st.markdown(message)

if st.session_state.chat_history:
    last_sender, last_message = st.session_state.chat_history[-1]
    if last_sender == "You":
        reply = fraud_chatbot(last_message)
        st.session_state.chat_history.append(("Assistant", reply))
        with st.chat_message("assistant"):
            st.markdown(reply)
