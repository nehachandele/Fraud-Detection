# 💳 Fraud Detection Prediction System

A Machine Learning–powered Fraud Detection System with a real-time **Streamlit dashboard** that combines **ML probability**, **rule-based decision logic**, and **interactive analytics** to help financial teams identify fraudulent transactions efficiently.

---

## 🚀 Features

- 🔍 Real-time fraud prediction  
- 🤖 ML-based fraud probability estimation  
- 🧠 Hybrid decision engine (ML + business rules)  
- 📊 Admin dashboard for monitoring & analytics  
- 📈 Daily and monthly fraud trend analysis  
- 📱 Mobile-responsive Streamlit UI  
- 🧾 Automatic transaction logging for audit purposes  

---

## 🧠 System Overview

1. User inputs transaction details  
2. ML model predicts fraud probability  
3. Rule engine applies domain-based conditions  
4. Final decision is generated: **Fraud / Suspicious / Safe**  
5. Transaction is logged for analytics and monitoring  
6. Admin panel visualizes fraud trends and distributions  

> This system combines ML-based fraud probability, a rule-based explanation engine, and a user-friendly dashboard to help financial teams take faster decisions.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **Machine Learning:** Scikit-learn  
- **Data Processing:** Pandas, NumPy  
- **Visualization:** Matplotlib  
- **Model Serialization:** Joblib  

---

## 📂 Project Structure

```
Fraud_Detection/
│
├── AIML Dataset.csv
├── analysis_model.ipynb
├── fraud_detection_pipeline.pkl
├── fraud_detection.py
├── transaction_logs.csv
├── README.md
├── .gitignore
```

---

## 📊 Dataset

The dataset is **not included** in this repository due to GitHub file size limitations.

Download from:  
https://www.kaggle.com/datasets/amanalisiddiqui/fraud-detection-dataset  

After downloading, place the dataset file in the **project root directory**.

---

## ⚙️ Installation & Setup

### Clone the Repository
```bash
git clone https://github.com/your-username/Fraud_Detection.git
cd Fraud_Detection
```

### Install Dependencies
```bash
pip install streamlit pandas numpy scikit-learn matplotlib joblib
```

### Run the Application
```bash
streamlit run fraud_detection.py
```

The application will run at:  
http://localhost:8501

---

## 📈 Analytics Dashboard

The admin dashboard provides:
- Daily fraud trend analysis  
- Monthly fraud statistics  
- Decision-wise transaction distribution  
- Filters by fraud probability and decision type  

All charts are responsive and optimized for mobile screens.

---

## 🧪 Fraud Decision Logic

| Condition                         | Final Decision |
|----------------------------------|----------------|
| Amount > ₹5,00,000               | Fraud          |
| Sender balance becomes zero      | Fraud          |
| ML probability ≥ 75%             | Fraud          |
| ML probability ≥ 40%             | Suspicious     |
| Otherwise                        | Safe           |

---

## 🎯 Use Cases

- Banking transaction monitoring  
- Financial fraud prevention systems  
- Risk assessment dashboards  
- ML + business rule integration demos  

---

## 📌 Note

This project is designed for **academic, demo, and portfolio purposes** and demonstrates how machine learning models can be combined with business rules for real-world fraud detection systems.
