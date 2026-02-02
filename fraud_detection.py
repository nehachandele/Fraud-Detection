import streamlit as st
import pandas as pd
import joblib

model = joblib.load("fraud_detection_pipeline.pkl")

st.title("Fraud Detection Prediction App")
st.markdown(
    "Please enter the transaction details and use the predict button "
    "to check if the transaction is fraudulent or not."
)

st.divider()

transaction_type = st.selectbox(
    "Transaction Type",
    ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"]
)

amount = st.number_input("Amount", min_value=0.0, value=1000.0)
oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, value=10000.0)
newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0, value=9000.0)

oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0, value=0.0)

if st.button("Predict"):
    input_data = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1] * 100
    if probability < 30:
        risk_level = "Low Risk"
    elif probability < 70:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"


    st.subheader("Prediction Result")
    st.write(f"Fraud Probability: **{probability:.2f}%**")
    st.write(f"Risk Level: **{risk_level}**")


    if prediction == 1:
        st.error("⚠️ The transaction can be FRAUD")
    else:
        st.success("✅ This transaction looks legitimate")
