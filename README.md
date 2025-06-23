# 💼 Personal Finance Dashboard

A clean, modern, and interactive web app to manage your **income, expenses, and financial goals** — all powered by Python, Streamlit, and machine learning. Ideal for users who want **simple CSV-based financial tracking** without the need for a database.

🔗 **[🌐 Live Demo](https://personal-finance-dashboard-gtimex2cf9wmq7dadqdxdc.streamlit.app/)**  
🎦 **https://github.com/user-attachments/assets/5d8ff6d4-cc0b-44d3-b201-0b039ee44730**

---

## 📘 Overview

Managing money shouldn't be complicated.  
**Personal Finance Dashboard** provides a lightweight yet powerful solution for:

- Tracking income and spending
- Visualizing where your money goes
- Predicting future expenses
- Making smarter financial decisions

All without needing a backend database—just a CSV file and some Python magic!

---

## ⚡ Highlights

✨ **Why you'll love it**:

- 🔐 **Secure Login System** – Uses bcrypt to hash user passwords.
- 📝 **Intuitive Transaction Input** – Quickly add income or expense entries.
- 📁 **CSV-Based Storage** – No database headaches. Just simple files.
- 📊 **Dynamic Dashboard** – Filter by category, type, or time range.
- 📈 **AI-Powered Predictions** – Estimate future expenses using linear regression.
- 📉 **Smart Spending Insights** – Identify patterns and reduce waste.

---

## 🖼️ Screenshots

| Dashboard View | Transaction Form |
|----------------|------------------|
| ![Dashboard Screenshot](screenshots/dashboard.png) | ![Transaction Form](screenshots/form.png) |

---

## 🧠 Tech Stack

- 🐍 **Python 3**
- 🎨 **Streamlit** – Beautiful & reactive frontend
- 📊 **Pandas** – Data handling and manipulation
- 🔐 **bcrypt** – Password security
- 🧠 **scikit-learn** – For machine learning predictions

---

## 🛠️ Installation Guide

To run this project locally, follow these steps:

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/personal-finance-dashboard.git
cd personal-finance-dashboard
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the App

```bash
streamlit run app.py
```

---

## 💡 Project Structure 

```
personal-finance-dashboard/
│
├── app.py                  # Main Streamlit app
├── auth.py                 # Login & password handling
├── data.csv                # CSV file storing all transactions
├── utils.py                # Utility functions
├── requirements.txt        # Dependencies
├── screenshots/            # UI screenshots
└── README.md               # You’re reading it!
```

---

## 🧪 Sample Transactions

If you want to test, here are a few dummy entries to paste into your `data.csv`:

```csv
Date,Type,Category,Amount,Description
2024-12-10,Income,Salary,50000,Monthly salary
2024-12-15,Expense,Groceries,3000,Big Bazaar
2024-12-18,Expense,Utilities,1200,Electric bill
```

---

## 🤝 Contributing

Got ideas? Spotted a bug?  
We’d love your help! Feel free to:

- 🌟 Star the repo
- 🐛 Open issues
- 📥 Submit pull requests

---

## 📄 License

Licensed under the **Apache License 2.0**.  
See the [LICENSE](LICENSE) file for full details.

---


