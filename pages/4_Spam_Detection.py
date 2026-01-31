import streamlit as st
import joblib

st.set_page_config(page_title="Spam Detection", layout="centered")

st.title("📨 Spam Detection (ML Model)")
st.write("This model classifies messages as **Spam** or **Not Spam**.")

# Load model & vectorizer
spam_model = joblib.load("spam_model.pkl")
spam_vectorizer = joblib.load("spam_vectorizer.pkl")

message = st.text_area("✉️ Enter Email / Message Text")

if st.button("🔍 Detect Spam"):
    if message.strip() == "":
        st.warning("Please enter some text")
    else:
        X = spam_vectorizer.transform([message])
        prediction = spam_model.predict(X)[0]

        if prediction == "spam":
            st.error("🚨 This message is SPAM")
        else:
            st.success("✅ This message is NOT Spam")
