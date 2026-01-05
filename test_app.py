import streamlit as st
import pandas as pd

# Set page config for nicer look
st.set_page_config(page_title="Tax Pot Tracker MVP", layout="wide")

# Title and intro
st.title("Tax Pot Tracker - MVP 🚀")
st.markdown("Simple tool to help track income, expenses and set aside tax. For UK sole traders/freelancers.")

# Initialize session state for expenses
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    tax_rate = st.slider("Suggested tax set-aside %", 10, 50, 25, step=5)
    st.markdown("---")
    if st.button("Clear All Data"):
        st.session_state.expenses = []
        st.success("All data cleared!")
        st.rerun()

# Main content - two columns
col1, col2 = st.columns([1, 1.3])

with col1:
    st.subheader("Add Income")
    monthly_income = st.number_input(
        "Monthly Gross Income (£)",
        min_value=0.0,
        value=2000.0,
        step=100.0,
        format="%.2f"
    )

    st.subheader("Add Expense")
    exp_amount = st.number_input("Expense Amount (£)", min_value=0.01, value=50.0, step=10.0)
    exp_category = st.selectbox(
        "Category",
        ["Travel/Mileage", "Home Office", "Equipment", "Subscriptions", "Marketing", "Other"]
    )
    exp_description = st.text_input("Description (optional)")

    if st.button("➕ Add Expense"):
        if exp_amount > 0:
            st.session_state.expenses.append({
                "Amount": exp_amount,
                "Category": exp_category,
                "Description": exp_description if exp_description else "-"
            })
            st.success(f"Added £{exp_amount:.2f} - {exp_category}")
        else:
            st.warning("Amount must be greater than 0")

with col2:
    st.subheader("Summary & Tax Pot")

    # Calculations
    total_income = monthly_income
    total_expenses = sum(exp["Amount"] for exp in st.session_state.expenses) if st.session_state.expenses else 0.0
    net_cash = total_income - total_expenses

    # New tax pot logic: based on net cash (profit), not gross income
    if net_cash > 0:
        tax_pot = net_cash * (tax_rate / 100)
        tax_pot_display = f"£{tax_pot:,.2f}"
        tax_delta = None
    else:
        tax_pot = 0.0
        tax_pot_display = "£0.00 (no profit)"
        tax_delta = "⚠️ Expenses exceed income!"

    # Display metrics
    st.metric("Monthly Income", f"£{total_income:,.2f}")
    st.metric("Total Expenses", f"£{total_expenses:,.2f}", delta=f"-£{total_expenses:,.2f}")
    st.metric("Net Cash (Profit)", f"£{net_cash:,.2f}", delta_color="normal")
    st.metric(
        "Suggested Tax Pot to Set Aside",
        tax_pot_display,
        delta=tax_delta,
        help=f"Calculated as {tax_rate}% of your net cash/profit after expenses (more realistic for cash flow). Adjust rate in sidebar."
    )

    # Show expenses table
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df.style.format({"Amount": "£{:,.2f}"}), use_container_width=True)
    else:
        st.info("No expenses added yet.")

# Footer disclaimer
st.markdown("---")
st.caption("This is a basic MVP tool — estimates only. Not official financial/tax advice. Always check with HMRC or your accountant.")