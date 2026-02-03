import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# ================= CONFIG =================
LOG_FILE = "transaction_logs.csv"

st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="💳",
    layout="wide"
)

# ================= LOAD MODEL =================
model = joblib.load("fraud_detection_pipeline.pkl")

# ================= STYLING =================
st.markdown("""
<style>
.card {
    background-color: #ffffff;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    text-align: center;
}
.card-title {
    font-size: 13px;
    color: #6b7280;
}
.card-value {
    font-size: 24px;
    font-weight: 700;
}
.high-risk { color: #dc2626; }
.medium-risk { color: #f59e0b; }
.low-risk { color: #16a34a; }
.admin-box {
    background:#f9fafb;
    padding:18px;
    border-radius:14px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("💳 Fraud Detection Prediction System")
st.caption("ML + Rule Engine · Real-Time Risk Analysis")
st.divider()

# ================= INPUT =================
st.subheader("🧾 Transaction Details")

c1, c2 = st.columns(2)

with c1:
    transaction_type = st.selectbox(
        "Transaction Type",
        ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"]
    )
    amount = st.number_input("Amount (₹)", min_value=0.0, value=1000.0)
    oldbalanceOrg = st.number_input("Sender Old Balance (₹)", min_value=0.0, value=10000.0)

with c2:
    newbalanceOrig = st.number_input("Sender New Balance (₹)", min_value=0.0, value=9000.0)
    oldbalanceDest = st.number_input("Receiver Old Balance (₹)", min_value=0.0)
    newbalanceDest = st.number_input("Receiver New Balance (₹)", min_value=0.0)

st.divider()

# ================= PREDICTION =================
if st.button("🔍 Analyze Transaction", use_container_width=True):

    input_df = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1] * 100

    # Risk Label
    if probability >= 80:
        risk, cls = "High Risk", "high-risk"
    elif probability >= 40:
        risk, cls = "Medium Risk", "medium-risk"
    else:
        risk, cls = "Low Risk", "low-risk"

    # Hybrid Decision Engine
    if amount > 500000:
        final_decision = "Fraud"
    elif oldbalanceOrg > 0 and newbalanceOrig == 0:
        final_decision = "Fraud"
    elif probability >= 75:
        final_decision = "Fraud"
    elif probability >= 40:
        final_decision = "Suspicious"
    else:
        final_decision = "Safe"

    # Log Transaction
    log = pd.DataFrame([{
        "Timestamp": datetime.now(),
        "Transaction Type": transaction_type,
        "Amount": amount,
        "Old Balance Sender": oldbalanceOrg,
        "New Balance Sender": newbalanceOrig,
        "Old Balance Receiver": oldbalanceDest,
        "New Balance Receiver": newbalanceDest,
        "Fraud Probability (%)": round(probability, 2),
        "Risk Level": risk,
        "ML Prediction": "Fraud" if prediction == 1 else "Safe",
        "Final Decision": final_decision
    }])

    log.to_csv(LOG_FILE, mode="a", header=not os.path.exists(LOG_FILE), index=False)

    # ================= SUMMARY =================
    st.subheader("📊 Transaction Summary")

    s1, s2, s3, s4 = st.columns(4)

    s1.markdown(f"<div class='card'><div class='card-title'>Type</div><div class='card-value'>{transaction_type}</div></div>", unsafe_allow_html=True)
    s2.markdown(f"<div class='card'><div class='card-title'>Amount</div><div class='card-value'>₹{amount:,.0f}</div></div>", unsafe_allow_html=True)
    s3.markdown(f"<div class='card'><div class='card-title'>Probability</div><div class='card-value {cls}'>{probability:.1f}%</div></div>", unsafe_allow_html=True)
    s4.markdown(f"<div class='card'><div class='card-title'>Risk</div><div class='card-value {cls}'>{risk}</div></div>", unsafe_allow_html=True)

    if final_decision == "Fraud":
        st.error("🚨 Fraud Detected")
    elif final_decision == "Suspicious":
        st.warning("🧐 Suspicious Transaction")
    else:
        st.success("✅ Transaction Approved")

# ================= ADMIN PANEL =================
st.divider()
st.markdown("## 🛡️ Admin Console")
st.caption("Monitoring · Audit · Analytics")

# Load logs for admin panel
if os.path.exists(LOG_FILE):
    logs_df = pd.read_csv(LOG_FILE)
    logs_df["Timestamp"] = pd.to_datetime(logs_df["Timestamp"], errors="coerce")
    logs_df["Final Decision"] = logs_df["Final Decision"].str.strip()
else:
    logs_df = pd.DataFrame()

if not logs_df.empty:
    with st.container():
        st.markdown("<div class='admin-box'>", unsafe_allow_html=True)

        f1, f2, f3 = st.columns([2,2,1])

        with f1:
            decision_filter = st.selectbox(
                "Filter by Decision",
                ["All", "Fraud", "Suspicious", "Safe"]
            )

        with f2:
            min_prob = st.slider("Minimum Fraud Probability (%)", 0, 100, 40)

        with f3:
            st.metric("Total Records", len(logs_df))

        df = logs_df.copy()
        if decision_filter != "All":
            df = df[df["Final Decision"] == decision_filter]

        df = df[df["Fraud Probability (%)"] >= min_prob]

        st.caption(f"Showing {len(df)} records")
        st.dataframe(df, use_container_width=True, height=260)

        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("📌 No transaction logs available yet.")

# ================= ANALYTICS =================
st.divider()
st.subheader("📈 Fraud Trend Analytics")

# Always read full logs from CSV for analytics
if os.path.exists(LOG_FILE):
    full_logs_df = pd.read_csv(LOG_FILE)
    full_logs_df["Timestamp"] = pd.to_datetime(full_logs_df["Timestamp"], errors="coerce")
    full_logs_df["Final Decision"] = full_logs_df["Final Decision"].str.strip()
    full_logs_df["Date"] = full_logs_df["Timestamp"].dt.date
    full_logs_df["Month"] = full_logs_df["Timestamp"].dt.to_period("M").astype(str)
    fraud_df = full_logs_df[full_logs_df["Final Decision"].str.contains("Fraud", na=False)]
else:
    full_logs_df = pd.DataFrame()
    fraud_df = pd.DataFrame()

# Responsive columns: stacked on small screens
if st.runtime.exists():
    # Detect width (Streamlit doesn't provide exact screen width)
    # We'll just use a simple 3-column layout for desktop, stacked on mobile automatically
    g1, g2, g3 = st.columns([1,1,1], gap="medium")

    # Daily Fraud
    with g1:
        st.caption("📅 Daily Fraud")
        if not fraud_df.empty:
            # Ensure Date is datetime
            fraud_df["Date"] = pd.to_datetime(fraud_df["Date"])
    
            daily = fraud_df.groupby("Date").size().sort_index()

            # Create figure
            fig, ax = plt.subplots(figsize=(5,4))
            ax.plot(daily.index, daily.values, marker="o", color="#ef4444", linewidth=2)

    # Titles and labels
            ax.set_title("Daily Fraud Count", fontsize=12)
            ax.set_xlabel("Date", fontsize=10)
            ax.set_ylabel("Count", fontsize=10)

    # Format x-axis
            ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
            plt.xticks(rotation=0, ha="right", fontsize=8)
            plt.yticks(fontsize=8)
    
            plt.grid(True, linestyle='--', alpha=0.5)  # optional grid
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("No fraud data available")



    # Monthly Fraud
    with g2:
        st.caption("📆 Monthly Fraud")
        if not fraud_df.empty:
            monthly = fraud_df.groupby("Month").size()
            fig, ax = plt.subplots(figsize=(5,4))
            ax.bar(monthly.index, monthly.values, color="#f59e0b")
            ax.set_title("Monthly Fraud Count", fontsize=10)
            ax.set_xlabel("Month", fontsize=8)
            ax.set_ylabel("Count", fontsize=8)
            plt.xticks(rotation=0, fontsize=8)
            plt.yticks(fontsize=8)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("No fraud data available")

    # Decision Distribution
    with g3:
        st.caption("📊 Decision Distribution")
        if not full_logs_df.empty:
            dist = full_logs_df["Final Decision"].value_counts()
            fig, ax = plt.subplots(figsize=(5,4))
            ax.bar(dist.index, dist.values, color="#16a34a")
            ax.set_title("Decision Distribution", fontsize=10)
            ax.set_xlabel("Decision", fontsize=8)
            ax.set_ylabel("Count", fontsize=8)
            plt.xticks(rotation=0, fontsize=8)
            plt.yticks(fontsize=8)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("No transaction data available")
