import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime
import matplotlib.pyplot as plt

# ------------------ CONFIG ------------------
LOG_FILE = "transaction_logs.csv"

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
st.caption("AI-powered transaction analysis using ML + Rule Engine")
st.divider()

# ------------------ INPUT FORM ------------------
st.subheader("🧾 Transaction Details")

col1, col2 = st.columns(2)

with col1:
    transaction_type = st.selectbox(
        "Transaction Type",
        ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"]
    )
    amount = st.number_input("Transaction Amount (₹)", min_value=0.0, value=1000.0)
    oldbalanceOrg = st.number_input("Sender Old Balance (₹)", min_value=0.0, value=10000.0)

with col2:
    newbalanceOrig = st.number_input("Sender New Balance (₹)", min_value=0.0, value=9000.0)
    oldbalanceDest = st.number_input("Receiver Old Balance (₹)", min_value=0.0, value=0.0)
    newbalanceDest = st.number_input("Receiver New Balance (₹)", min_value=0.0, value=0.0)

st.divider()

# ------------------ PREDICTION ------------------
if st.button("Predict Fraud Risk", use_container_width=True):

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
        risk_label = "High Risk"
        risk_class = "high-risk"
    elif probability >= 40:
        risk_label = "Medium Risk"
        risk_class = "medium-risk"
    else:
        risk_label = "Low Risk"
        risk_class = "low-risk"

    # ------------------ RULE-BASED EXPLANATION ------------------
    reasons = []

    if amount > 200000:
        reasons.append("Unusually high transaction amount")

    if oldbalanceOrg > 0 and newbalanceOrig == 0:
        reasons.append("Sender balance completely drained")

    if oldbalanceDest == 0 and newbalanceDest > 0:
        reasons.append("Receiver had zero balance before transaction")

    if transaction_type in ["TRANSFER", "CASH_OUT"] and amount > 100000:
        reasons.append("High-risk transaction type with large amount")

    if abs((oldbalanceOrg - newbalanceOrig) - amount) > 1:
        reasons.append("Inconsistent balance change detected")

    # ------------------ STEP 5: HYBRID DECISION ENGINE ------------------
    if amount > 500000:
        final_decision = "Fraud (Rule Override: Very High Amount)"
    elif oldbalanceOrg > 0 and newbalanceOrig == 0:
        final_decision = "Fraud (Rule Override: Balance Drained)"
    elif abs((oldbalanceOrg - newbalanceOrig) - amount) > 1:
        final_decision = "Fraud (Rule Override: Balance Mismatch)"
    elif probability >= 75:
        final_decision = "Fraud (ML Prediction)"
    elif 40 <= probability < 75:
        final_decision = "Suspicious (Manual Review Required)"
    else:
        final_decision = "Safe"

    # ------------------ TRANSACTION LOGGING ------------------
    log_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Transaction Type": transaction_type,
        "Amount": amount,
        "Old Balance Sender": oldbalanceOrg,
        "New Balance Sender": newbalanceOrig,
        "Old Balance Receiver": oldbalanceDest,
        "New Balance Receiver": newbalanceDest,
        "Fraud Probability (%)": round(probability, 2),
        "Risk Level": risk_label,
        "ML Prediction": "Fraud" if prediction == 1 else "Not Fraud",
        "Final Decision": final_decision
    }

    log_df = pd.DataFrame([log_data])
    if os.path.exists(LOG_FILE):
        log_df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        log_df.to_csv(LOG_FILE, index=False)

    st.info("📄 Transaction logged successfully (Audit Trail)")

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
    st.subheader("🧠 Final Decision (Hybrid Engine)")

    if "Fraud" in final_decision:
        st.error(f"🚨 {final_decision}")
    elif "Suspicious" in final_decision:
        st.warning(f"🧐 {final_decision}")
    else:
        st.success("✅ Transaction Approved")

    # ------------------ EXPLANATION ------------------
    st.subheader("📌 Why this transaction was flagged")

    if reasons:
        for r in reasons:
            st.warning(f"• {r}")
    else:
        st.info("No suspicious patterns detected by rule-based analysis")


st.divider()
st.subheader("🧑‍💼 Admin Dashboard – Transaction Monitoring")
if os.path.exists(LOG_FILE):
    logs_df = pd.read_csv(LOG_FILE)
else:
    st.warning("No transaction logs found yet.")
    logs_df = None

if logs_df is not None:

    col1, col2 = st.columns(2)

    with col1:
        decision_filter = st.selectbox(
            "Filter by Final Decision",
            ["All", "Fraud", "Suspicious", "Safe"]
        )

    with col2:
        min_prob = st.slider(
            "Minimum Fraud Probability (%)",
            0, 100, 40
        )

    filtered_df = logs_df.copy()

    if decision_filter != "All":
        filtered_df = filtered_df[
            filtered_df["Final Decision"].str.contains(decision_filter, case=False)
        ]

    filtered_df = filtered_df[
        filtered_df["Fraud Probability (%)"] >= min_prob
    ]

    st.markdown("### 📋 Flagged Transactions")

    st.dataframe(
        filtered_df.sort_values("Fraud Probability (%)", ascending=False),
        use_container_width=True
    )

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Report",
        data=csv,
        file_name="fraud_monitoring_report.csv",
        mime="text/csv"
    )
st.divider()
st.subheader("📈 Fraud Trend Analytics")

if logs_df is not None and not logs_df.empty:

    # ---------- PREPROCESS ----------
    logs_df["Timestamp"] = pd.to_datetime(logs_df["Timestamp"])
    logs_df["Date"] = logs_df["Timestamp"].dt.date
    logs_df["Month"] = logs_df["Timestamp"].dt.to_period("M").astype(str)

    fraud_df = logs_df[
        logs_df["Final Decision"].str.contains("Fraud", case=False)
    ]

    # ========= SINGLE COLUMN =========
    # ========= SINGLE ROW (3 GRAPHS SIDE BY SIDE) =========
    col1, col2, col3 = st.columns(3)

# ---------- DAILY FRAUD ----------
    with col1:
        st.markdown("### 📅 Daily Fraud Trend")

        daily_fraud = fraud_df.groupby("Date").size()

        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.plot(daily_fraud.index, daily_fraud.values, marker="o")
        ax1.set_ylabel("Count")
        ax1.grid(alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig1)

# ---------- MONTHLY FRAUD ----------
    with col2:
        st.markdown("### 📆 Monthly Fraud Trend")

        monthly_fraud = fraud_df.groupby("Month").size()

        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.bar(monthly_fraud.index, monthly_fraud.values)
        ax2.set_ylabel("Count")
        ax2.grid(axis="y", alpha=0.3)
        st.pyplot(fig2)

# ---------- FRAUD VS SAFE ----------
    with col3:
        st.markdown("### 📊 Fraud vs Safe")

        decision_counts = logs_df["Final Decision"].apply(
        lambda x: "Fraud" if "Fraud" in x else "Safe"
        ).value_counts()

        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.bar(decision_counts.index, decision_counts.values)
        ax3.set_ylabel("Count")
        ax3.grid(axis="y", alpha=0.3)
        st.pyplot(fig3)


else:
    st.info("Not enough transaction data available for analytics.")
