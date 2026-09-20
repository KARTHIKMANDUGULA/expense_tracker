import streamlit as st

class bank:
    def __init__(self, acc, balance):
        self.acc = acc
        self.__balance = balance
        self.history = []
    
    def credit(self, amount):
        if amount > 0:
            self.__balance += amount
            msg = f"Amount of Rs. {amount} credited to acc {self.acc}.\nRemaining balance: Rs. {self.__balance}"
            self.history.append(f"credit,+{amount},balance,{self.__balance}\n")
            return msg, True
        return "Please enter a valid positive amount.", False

    def debit(self, amount):
        if amount > 0:
            if amount <= self.__balance:
                self.__balance -= amount
                msg = f"Amount of Rs. {amount} debited from acc {self.acc}.\nRemaining balance: Rs. {self.__balance}"
                self.history.append(f"debit,-{amount},balance,{self.__balance}\n")
                return msg, True
            return "Insufficient funds in the bank. Kindly enter a lower amount.", False
        return "Please enter a valid positive amount.", False

    def get_balance(self):
        return self.__balance

    def save(self):
        if self.history:
            with open("save_to_file.csv", "a") as f:
                f.writelines(self.history)
            self.history = []


st.set_page_config(page_title="Vault Bank", page_icon="🏦", layout="centered")

# Track entry portal state: "landing", "new_portal", "old_portal"
if "portal_state" not in st.session_state:
    st.session_state.portal_state = "landing"

# Track dashboard screen: "menu", "add", "debit", "history"
if "current_view" not in st.session_state:
    st.session_state.current_view = "menu"


# ============================================================
# 1. INITIAL ENTRY: ONLY TWO PORTAL BOXES
# ============================================================
if "acc1" not in st.session_state and st.session_state.portal_state == "landing":
    st.title("🏦 Welcome to Banking Portal")
    st.write("Please choose your portal to continue:")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🆕 New Customer")
            st.write("Open an account, make an initial deposit, and join.")
            if st.button("Enter New Customer Portal ➡️", use_container_width=True):
                st.session_state.portal_state = "new_portal"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("👤 Existing Customer")
            st.write("Access your existing balance and manage transactions.")
            if st.button("Enter Existing Customer Portal ➡️", use_container_width=True):
                st.session_state.portal_state = "old_portal"
                st.rerun()


# ============================================================
# 2. NEW CUSTOMER DEDICATED PORTAL
# ============================================================
elif "acc1" not in st.session_state and st.session_state.portal_state == "new_portal":
    with st.container(border=True):
        st.subheader("🆕 New Customer Registration")
        
        acc_new = st.number_input("Enter Desired Account Number:", min_value=1, step=1, value=101)
        bal_new = st.number_input("Enter Initial Deposit (Rs.):", min_value=0.0, step=100.0, value=500.0)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Open Account & Login", use_container_width=True):
                if bal_new < 0:
                    st.error("Amount should not be negative.")
                else:
                    new_acc_obj = bank(acc_new, bal_new)
                    new_acc_obj.history.append(f"credit,+{bal_new},balance,{bal_new}\n")
                    new_acc_obj.save()
                    st.session_state.acc1 = new_acc_obj
                    st.session_state.current_view = "menu"
                    st.rerun()

        with btn_col2:
            if st.button("⬅️ Back to Portals", use_container_width=True):
                st.session_state.portal_state = "landing"
                st.rerun()


# ============================================================
# 3. EXISTING CUSTOMER DEDICATED PORTAL
# ============================================================
elif "acc1" not in st.session_state and st.session_state.portal_state == "old_portal":
    with st.container(border=True):
        st.subheader("👤 Existing Customer Login")
        
        acc_old = st.number_input("Enter Your Account Number:", min_value=1, step=1, value=101)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Verify & Login", use_container_width=True):
                try:
                    with open("save_to_file.csv", "r") as f:
                        hist = f.readlines()
                except FileNotFoundError:
                    hist = []

                if not hist:
                    st.warning("No records found in the ledger. Please register as a New Customer.")
                else:
                    recent_history = hist[-1].strip().split(",")
                    saved_bal = float(recent_history[3])
                    st.session_state.acc1 = bank(acc_old, saved_bal)
                    st.session_state.current_view = "menu"
                    st.rerun()

        with btn_col2:
            if st.button("⬅️ Back to Portals", use_container_width=True):
                st.session_state.portal_state = "landing"
                st.rerun()


# ============================================================
# 4. MAIN OPERATIONS DASHBOARD
# ============================================================
else:
    acc1 = st.session_state.acc1

    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.title("Banking Dashboard")
        st.write(f"Active Account: **`{acc1.acc}`**")
    with header_col2:
        st.write("")
        if st.button("🚪 Logout", use_container_width=True):
            acc1.save()
            del st.session_state.acc1
            st.session_state.portal_state = "landing"
            st.session_state.current_view = "menu"
            st.rerun()

    st.divider()

    # Dashboard Hub (4 cards)
    if st.session_state.current_view == "menu":
        col_a, col_b = st.columns(2)

        with col_a:
            with st.container(border=True):
                st.subheader("💰 Balance")
                st.metric(label="Current Available Balance", value=f"Rs. {acc1.get_balance()}")

        with col_b:
            with st.container(border=True):
                st.subheader("📜 Ledger History")
                st.write("View all transactions recorded in your CSV file.")
                if st.button("View Ledger ➡️", use_container_width=True):
                    st.session_state.current_view = "history"
                    st.rerun()

        col_c, col_d = st.columns(2)

        with col_c:
            with st.container(border=True):
                st.subheader("➕ Credit")
                st.write("Add funds directly to your account balance.")
                if st.button("Go to Credit ➡️", use_container_width=True):
                    st.session_state.current_view = "add"
                    st.rerun()

        with col_d:
            with st.container(border=True):
                st.subheader("➖ Debit")
                st.write("Withdraw funds from your available balance.")
                if st.button("Go to Debit ➡️", use_container_width=True):
                    st.session_state.current_view = "debit"
                    st.rerun()

    # Credit (Add) Screen
    elif st.session_state.current_view == "add":
        with st.container(border=True):
            st.subheader("➕ Credit Funds")
            add_amt = st.number_input("Enter amount to add:", min_value=0.0, step=50.0, value=100.0)
            
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Submit Credit", use_container_width=True):
                    msg, success = acc1.credit(add_amt)
                    acc1.save()
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
            with b2:
                if st.button("⬅️ Back to Menu", use_container_width=True):
                    st.session_state.current_view = "menu"
                    st.rerun()

    # Debit Screen
    elif st.session_state.current_view == "debit":
        with st.container(border=True):
            st.subheader("➖ Debit Funds")
            deb_amt = st.number_input("Enter amount to withdraw:", min_value=0.0, step=50.0, value=100.0)
            
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Submit Debit", use_container_width=True):
                    msg, success = acc1.debit(deb_amt)
                    acc1.save()
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
            with b2:
                if st.button("⬅️ Back to Menu", use_container_width=True):
                    st.session_state.current_view = "menu"
                    st.rerun()

    # History View Screen
    elif st.session_state.current_view == "history":
        with st.container(border=True):
            st.subheader("📜 Transaction Ledger")
            try:
                with open("save_to_file.csv", "r") as f:
                    lines = f.readlines()
                if lines:
                    st.text("".join(lines))
                else:
                    st.info("The ledger file is currently empty.")
            except FileNotFoundError:
                st.info("No ledger file found yet.")

            st.write("")
            if st.button("⬅️ Back to Menu", use_container_width=True):
                st.session_state.current_view = "menu"
                st.rerun()