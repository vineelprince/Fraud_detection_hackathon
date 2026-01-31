import streamlit as st
import pandas as pd
import joblib

# 1. Load the trained model pipeline
model = joblib.load("fraud_detection_pipeline.pkl")

# 2. UI Header section
st.title("Fraud Detection Prediction App")
st.markdown("Please enter the transaction details and use the predict button")
st.divider()

# 3. Input fields for transaction data
transaction_type = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"])
amount = st.number_input("Amount", min_value=0.0, value=1000.0)

# Note: In screenshot 1000103272, there was a 'TypeError' because of 'min_values'. 
# The correct parameter is 'min_value' (singular).
oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, value=10000.0)
newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0, value=9000.0)
oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0, value=1000.0)

# 4. Prediction logic
if st.button("Predict"):
    # Create DataFrame to match the model's expected input format
    input_data = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }])

    # Generate prediction (0 for Legitimate, 1 for Fraud)
    prediction = model.predict(input_data)[0]

    # Display results
    st.subheader(f"Prediction: {'Fraud' if prediction == 1 else 'Not Fraud'}")
    
    if prediction == 1:
        st.error("This transaction is flagged as POTENTIAL FRAUD.")
    else:
        st.success("This transaction appears to be LEGITIMATE.")


