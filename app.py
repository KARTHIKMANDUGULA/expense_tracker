import os
import streamlit as st
import pandas as pd

# ----------------- Class Definition -----------------
class Bank:
    def __init__(self, acc, balance):
        self.acc = acc
        self.__balance = balance
        self.history = []

    def credit(self, amount):
        if amount > 0:
            self.__balance += amount
            self.history.append({
                "Action": "Credit",
                "Amount": amount,
                "Remaining Balance": self.__balance
            })
            return True, f"Rs. {amount:,.2f} credited to Acc. {self.acc}. Current Balance: Rs. {self.__balance:,.2f}"
        return False, "Please enter a valid positive amount."

    def debit(self, amount):
        if amount > 0:
            if amount <= self.__balance:
                self.__balance -= amount
                self.history.append({
                    "Action": "Debit",
                    "Amount": -amount,
                    "Remaining Balance": self.__balance
                })
                return True, f"Rs. {amount:,.2f} debited from Acc. {self.acc}. Current Balance: Rs. {self.__balance:,.2f}"
            return False, "Insufficient funds in the account."
        return False, "Please enter a valid positive amount."

    def get_balance(self):
        return self.__balance

    def save(self, filename="save_to_file.csv"):
        if not self.history:
            return False
        df = pd.DataFrame(self.history)
        file_exists = os.path.isfile(filename)
        df.to_csv(filename, mode="a", index=False, header=not file_exists)
        return True

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="Simple Bank App", layout="wide")
st.title("🏦 Banking System")

# Initialize bank account in session_state
if "account" not in st.session_state:
    st.session_state.account = None

# Step 1: Account Creation
if st.session_state.account is None:
    st.subheader("Open an Account")
    with st.form("open_account_form"):
        acc_no = st.number_input("Enter Account Number", min_value=1, step=1)
        initial_bal = st.number_input("Initial Deposit Amount (Rs.)", min_value=0.0, step=100.0, format="%.2f")
        submit = st.form_submit_button("Create Account")

        if submit:
            st.session_state.account = Bank(acc_no, initial_bal)
            st.success(f"Account {acc_no} created successfully!")
            st.rerun()

# Step 2: Account Operations
else:
    acc = st.session_state.account

    st.sidebar.header(f"Account: #{acc.acc}")
    st.sidebar.metric("Current Balance", f"Rs. {acc.get_balance():,.2f}")

    if st.sidebar.button("Save Transactions & Logout"):
        acc.save()
        st.session_state.account = None
        st.success("Session saved to CSV. Logged out.")
        st.rerun()

    tab_credit, tab_debit, tab_history = st.tabs(["Add Money", "Debit Money", "Transaction History"])

    # Credit Tab
    with tab_credit:
        st.subheader("Credit Funds")
        credit_amt = st.number_input("Amount to Add (Rs.)", min_value=0.0, step=50.0, key="credit_val")
        if st.button("Deposit"):
            success, msg = acc.credit(credit_amt)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    # Debit Tab
    with tab_debit:
        st.subheader("Debit Funds")
        debit_amt = st.number_input("Amount to Debit (Rs.)", min_value=0.0, step=50.0, key="debit_val")
        if st.button("Withdraw"):
            success, msg = acc.debit(debit_amt)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    # History Tab
    with tab_history:
        st.subheader("Recent Activity")
        if acc.history:
            df_history = pd.DataFrame(acc.history)
            st.dataframe(df_history, use_container_width=True)
            
            if st.button("Save History to CSV"):
                acc.save()
                st.success("Saved to `save_to_file.csv`!")
        else:
            st.info("No transactions recorded yet in this session.")
            