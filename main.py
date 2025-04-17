import streamlit as st
import pandas as pd

# 1. Functions
def calculate_monthly_payment(P, annual_rate, years):
    r = (annual_rate / 100) / 12
    n = years * 12
    if r == 0:
        return P / n
    M = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return M

def generate_payment_schedule(P, annual_rate, years):
    monthly_payment = calculate_monthly_payment(P, annual_rate, years)
    r = (annual_rate / 100) / 12
    n = years * 12
    balance = P

    schedule = []
    for month in range(1, n + 1):
        interest = balance * r
        principal = monthly_payment - interest
        balance -= principal
        balance = max(balance, 0)  # Avoid negative balance
        schedule.append({
            "Month": month,
            "Payment (₦)": f"{monthly_payment:,.2f}",
            "Principal (₦)": f"{principal:,.2f}",
            "Interest (₦)": f"{interest:,.2f}",
            "Remaining Balance (₦)": f"{balance:,.2f}"
        })
    return pd.DataFrame(schedule)

# 2. Streamlit UI
st.title("📈 Loan Repayment Calculator")

st.sidebar.header("Enter Loan Details")

loan_amount = st.sidebar.number_input("Loan Amount (₦)", value=1000000, step=10000, format="%d")
interest_rate = st.sidebar.number_input("Annual Interest Rate (%)", value=15.0, step=0.1)
loan_term = st.sidebar.number_input("Loan Term (Years)", value=5, step=1)

if st.sidebar.button("Calculate"):
    monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    payment_schedule = generate_payment_schedule(loan_amount, interest_rate, loan_term)

    st.subheader(f"📋 Monthly Payment: ₦{monthly_payment:,.2f}")
    
    total_payment = monthly_payment * loan_term * 12
    total_interest = total_payment - loan_amount

    st.write(f"✅ Total Payment: ₦{total_payment:,.2f}")
    st.write(f"✅ Total Interest Paid: ₦{total_interest:,.2f}")

    st.subheader("📅 Payment Schedule")
    st.dataframe(payment_schedule, use_container_width=True)

    # Optional: Download button
    csv = payment_schedule.to_csv(index=False).encode('utf-8')
    st.download_button("Download Schedule as CSV", data=csv, file_name="payment_schedule.csv", mime='text/csv')
