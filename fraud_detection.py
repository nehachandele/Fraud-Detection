import streamlit as st
import pandas as pd
import joblib

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="💳",
    layout="wide"
)

# ------------------ LOAD MODEL ------------------
model = joblib.load("fraud_detection_pipeline.pkl")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    text-align: center;
}
.card-title {
    font-size: 14px;
    color: #6b7280;
}
.card-value {
    font-size: 26px;
    font-weight: 700;
    margin-top: 6px;
}
.high-risk { color: #dc2626; }
.medium-risk { color: #f59e0b; }
.low-risk { color: #16a34a; }
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.title("💳 Fraud Detection Prediction System")
st.caption("AI-powered transaction risk analysis using Machine Learning + Rule Engine")

st.divider()

# ------------------ INPUT FORM ------------------
st.subheader("🧾 Transaction Details")

colA, colB = st.columns(2)

with colA:
    transaction_type = st.selectbox(
        "Transaction Type",
        ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"]
    )
    amount = st.number_input("Transaction Amount (₹)", min_value=0.0, value=1000.0)
    oldbalanceOrg = st.number_input("Sender Old Balance (₹)", min_value=0.0, value=10000.0)

with colB:
    newbalanceOrig = st.number_input("Sender New Balance (₹)", min_value=0.0, value=9000.0)
    oldbalanceDest = st.number_input("Receiver Old Balance (₹)", min_value=0.0, value=0.0)
    newbalanceDest = st.number_input("Receiver New Balance (₹)", min_value=0.0, value=0.0)

st.divider()

# ------------------ PREDICTION ------------------
if st.button("🔍 Predict Fraud Risk", use_container_width=True):

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

    # ------------------ RISK LEVEL ------------------
    if probability >= 80:
        risk_label = "🚨 High Risk"
        risk_class = "high-risk"
    elif probability >= 40:
        risk_label = "⚠ Medium Risk"
        risk_class = "medium-risk"
    else:
        risk_label = "✅ Low Risk"
        risk_class = "low-risk"

    # ------------------ FRAUD EXPLANATION ------------------
    reasons = []

    if amount > 200000:
        reasons.append("Unusually high transaction amount")

    if oldbalanceOrg > 0 and newbalanceOrig == 0:
        reasons.append("Sender balance completely drained")

    if oldbalanceDest == 0 and newbalanceDest > 0:
        reasons.append("Receiver account had zero balance before transaction")

    if transaction_type in ["TRANSFER", "CASH_OUT"] and amount > 100000:
        reasons.append("High-risk transaction type with large amount")

    if abs((oldbalanceOrg - newbalanceOrig) - amount) > 1:
        reasons.append("Inconsistent balance change detected")

    # ------------------ SUMMARY CARDS ------------------
    st.subheader("📊 Transaction Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Transaction Type</div>
            <div class="card-value">{transaction_type}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Amount</div>
            <div class="card-value">₹{amount:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Fraud Probability</div>
            <div class="card-value {risk_class}">{probability:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Risk Level</div>
            <div class="card-value {risk_class}">{risk_label}</div>
        </div>
        """, unsafe_allow_html=True)

    # ------------------ FINAL DECISION ------------------
    st.divider()
    st.subheader("🧠 Prediction Result")

    if prediction == 1:
        st.error("⚠️ This transaction is **LIKELY FRAUDULENT**")
    else:
        st.success("✅ This transaction appears **LEGITIMATE**")

    # ------------------ EXPLANATION ------------------
    st.subheader("📌 Why this transaction was flagged")

    if reasons:
        for r in reasons:
            st.warning(f"• {r}")
    else:
        st.info("No suspicious patterns detected by rule-based analysis")
