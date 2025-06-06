# ==============================
# Personal Finance Dashboard (CSV Storage Version)
# ==============================

import streamlit as st
import pandas as pd
import bcrypt
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
import plotly.express as px

# ==============================
# File paths
# ==============================
USERS_CSV = "users.csv"
TRANSACTIONS_CSV = "transactions.csv"
TMP_USERS_CSV = "/tmp/users.csv"
TMP_TRANSACTIONS_CSV = "/tmp/transactions.csv"

# ==============================
# Initialize session state keys
# ==============================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'rerun_flag' not in st.session_state:
    st.session_state['rerun_flag'] = False

# ==============================
# Rerun helper function
# ==============================
def rerun():
    st.session_state['rerun_flag'] = not st.session_state['rerun_flag']

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")

# ==============================
# CUSTOM PAGE STYLE (improved UI)
# ==============================
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(to right, #F0F4FD, #E0F7FA, #F1F8E9);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #B2EBF2, #81D4FA);
        }
        h1, h2, h3 {
            background: linear-gradient(to right, #42A5F5, #478ED1);
            color: white;
            padding: 8px;
            border-radius: 8px;
        }
        div.stButton > button:first-child {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-size: 16px;
        }
        div.stButton > button:hover {
            background-color: #45A049;
            color: white;
        }
        button[kind="secondary"] {
            background-color: #F44336 !important;
            color: white !important;
            border-radius: 8px;
        }
        button[kind="secondary"]:hover {
            background-color: #D32F2F !important;
            color: white !important;
        }
        div[data-testid="stDownloadButton"] > button {
            background-color: #03A9F4;
            color: white;
            border-radius: 8px;
            font-weight: bold;
        }
        div[data-testid="stDownloadButton"] > button:hover {
            background-color: #0288D1;
            color: white;
        }
        /* New transaction card styles */
        .transaction-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: box-shadow 0.3s ease;
        }
        .transaction-card:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        .transaction-info {
            display: flex;
            justify-content: space-between;
            font-weight: 500;
            flex-wrap: wrap;
            gap: 15px;
        }
        .transaction-info > div {
            flex: 1 1 120px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# CSV File Load/Save Helpers
# ==============================
def load_users():
    path = TMP_USERS_CSV if os.path.exists(TMP_USERS_CSV) else USERS_CSV
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame(columns=["user_id", "name", "email", "password_hash"])

def save_users(df):
    df.to_csv(TMP_USERS_CSV, index=False)

def load_transactions():
    path = TMP_TRANSACTIONS_CSV if os.path.exists(TMP_TRANSACTIONS_CSV) else TRANSACTIONS_CSV
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame(columns=["transaction_id", "user_id", "category", "amount", "type", "transaction_date"])

def save_transactions(df):
    df.to_csv(TMP_TRANSACTIONS_CSV, index=False)

# ==============================
# Password hashing
# ==============================
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

# ==============================
# User management functions
# ==============================
def register_user(name, email, password):
    users = load_users()
    if email in users['email'].values:
        return "User already exists!"
    hashed_password = hash_password(password)
    new_id = users['user_id'].max() + 1 if not users.empty else 1
    new_user = pd.DataFrame([{
        "user_id": new_id,
        "name": name,
        "email": email,
        "password_hash": hashed_password
    }])
    users = pd.concat([users, new_user], ignore_index=True)
    save_users(users)
    return "User registered successfully!"

def login_user(email, password):
    users = load_users()
    user = users[users['email'] == email]
    if user.empty:
        return False
    stored_hash = user.iloc[0]['password_hash'].encode()
    if bcrypt.checkpw(password.encode(), stored_hash):
        st.session_state["user_id"] = int(user.iloc[0]['user_id'])
        st.session_state["logged_in"] = True
        return True
    return False

# ==============================
# Transaction functions
# ==============================
def fetch_transactions(user_id):
    transactions = load_transactions()
    user_transactions = transactions[transactions['user_id'] == user_id]
    if not user_transactions.empty:
        user_transactions['transaction_date'] = pd.to_datetime(user_transactions['transaction_date'])
    return user_transactions.sort_values(by='transaction_date', ascending=False)

def add_transaction(user_id, category, amount, transaction_type, transaction_date):
    transactions = load_transactions()
    new_id = transactions['transaction_id'].max() + 1 if not transactions.empty else 1
    new_transaction = pd.DataFrame([{
        "transaction_id": new_id,
        "user_id": user_id,
        "category": category,
        "amount": amount,
        "type": transaction_type,
        "transaction_date": transaction_date.strftime("%Y-%m-%d")
    }])
    transactions = pd.concat([transactions, new_transaction], ignore_index=True)
    save_transactions(transactions)

def delete_transaction(transaction_id):
    transactions = load_transactions()
    transactions = transactions[transactions['transaction_id'] != transaction_id]
    save_transactions(transactions)

# ==============================
# Prediction function
# ==============================
def predict_next_month(df):
    if df.empty:
        return 0
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['month'] = df['transaction_date'].dt.to_period('M')
    monthly_expense = df[df['type'] == 'Expense'].groupby('month')['amount'].sum().reset_index()
    if len(monthly_expense) < 2:
        return monthly_expense['amount'].sum()
    monthly_expense['month_num'] = range(len(monthly_expense))
    X = np.array(monthly_expense['month_num']).reshape(-1, 1)
    y = np.array(monthly_expense['amount'])
    model = LinearRegression()
    model.fit(X, y)
    next_month = np.array([[monthly_expense['month_num'].max() + 1]])
    return model.predict(next_month)[0]

# ==============================
# Email alert (unchanged)
# ==============================
def send_email_alert(email, message):
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    msg = MIMEText(message)
    msg['Subject'] = "Budget Overage Alert"
    msg['From'] = sender_email
    msg['To'] = email
    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

# ==============================
# Streamlit UI Code
# ==============================
st.sidebar.title("📌 Navigation")

if not st.session_state["logged_in"]:
    page = st.sidebar.radio("Go to", ["Login", "Register"])
    st.title("Welcome to the Personal Finance Dashboard")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if page == "Register":
        name = st.text_input("Full Name")
        if st.button("Register"):
            st.success(register_user(name, email, password))

    if page == "Login" and st.button("Login"):
        if login_user(email, password):
            rerun()
        else:
            st.error("Invalid credentials. Please try again.")

else:
    page = st.sidebar.radio("Go to", ["📊 Dashboard", "💰 Transactions", "📈 Budget & Predictions", "⚙️ Settings"])

    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        rerun()

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("User ID not found. Please log in again.")
    else:
        if page == "📊 Dashboard":
            st.title("📊 Personal Finance Dashboard")
            df = fetch_transactions(user_id)
            if not df.empty:
                st.dataframe(df)
                fig = px.pie(df[df['type'] == 'Expense'], names='category', values='amount', title='Expense by Category')
                st.plotly_chart(fig)
            else:
                st.write("No transactions found.")

        elif page == "💰 Transactions":
            st.title("💰 Transactions")
            category = st.text_input("Category")
            amount = st.number_input("Amount", min_value=0.01, step=0.01)
            transaction_type = st.selectbox("Type", ["Expense", "Income"])
            transaction_date = st.date_input("Date", datetime.today())
            if st.button("➕ Add Transaction"):
                add_transaction(user_id, category, amount, transaction_type, transaction_date)
                st.success("Transaction added successfully!")
                rerun()

            df = fetch_transactions(user_id)
            if not df.empty:
                st.write("Your Transactions:")
                for index, row in df.iterrows():
                    st.markdown(
                        f"""
                        <div class="transaction-card">
                            <div class="transaction-info">
                                <div><b>Date:</b> {row['transaction_date'].date()}</div>
                                <div><b>Category:</b> {row['category']}</div>
                                <div><b>Amount:</b> ${float(row['amount']):.2f}</div>
                                <div><b>Type:</b> {row['type']}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if st.button("🗑️ Delete", key=f"del_{row['transaction_id']}"):
                        delete_transaction(row['transaction_id'])
                        st.success("Transaction deleted.")
                        rerun()
            else:
                st.write("No transactions to display.")

        elif page == "📈 Budget & Predictions":
            st.title("📈 Budget & Predictions")
            df = fetch_transactions(user_id)
            predicted_expense = predict_next_month(df)
            predicted_expense = float(predicted_expense)

            if not df.empty:
                total_expense = float(df[df['type'] == 'Expense']['amount'].sum())
            else:
                total_expense = 0.0

            st.metric("Predicted Expense for Next Month", f"${predicted_expense:.2f}")

            if predicted_expense > total_expense * 1.2:
                st.warning("⚠️ You are likely to exceed your budget next month!")
                if st.button("📧 Send Budget Alert Email"):
                    result = send_email_alert("user_email@example.com", "You are likely to exceed your budget!")
                    st.info(result)

        elif page == "⚙️ Settings":
            st.title("⚙️ Settings")
            df = fetch_transactions(user_id)
            def export_to_csv(dataframe):
                return dataframe.to_csv(index=False).encode("utf-8")

            if not df.empty:
                st.download_button("📥 Download Transactions as CSV", export_to_csv(df), "transactions.csv", "text/csv")
            else:
                st.info("No transactions available to download.")

            predicted_expense = predict_next_month(df)
            predicted_expense = float(predicted_expense)

            if not df.empty:
                total_expense = float(df[df['type'] == 'Expense']['amount'].sum())
            else:
                total_expense = 0.0

            st.subheader("Budget Prediction")
            st.write(f"Predicted Expense for Next Month: **${predicted_expense:.2f}**")

            if predicted_expense > total_expense * 1.2:
                st.warning("⚠️ You are likely to exceed your budget next month. Consider reviewing your expenses.")
