import streamlit as st
import pandas as pd

# ==============================================
# PAGE CONFIG & PROFESSIONAL THEMING
# ==============================================
st.set_page_config(
    page_title="TaxPot Tracker",
    page_icon="💰",
    layout="wide"
)

# Professional finance-themed styling (inline CSS override)
st.markdown(
    """
    <style>
    /* Main app background & text */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    /* Primary buttons & accents */
    button[kind="primary"],
    .stButton > button {
        background-color: #2E7D32 !important;
        color: white !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
    }
    /* Hover effect on buttons */
    button[kind="primary"]:hover,
    .stButton > button:hover {
        background-color: #1B5E20 !important;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    /* Hide default footer & hamburger menu for cleaner look */
    footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    /* Better spacing & cards */
    .stMetric {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================
# HEADER & BRANDING
# ==============================================
st.markdown(
    """
    <div style='text-align: center; padding: 30px 0 20px;'>
        <h1 style='color: #2E7D32; margin: 0; font-size: 2.8em;'>TaxPot Tracker</h1>
        <p style='color: #64748B; font-size: 1.3em; margin: 10px 0 0;'>
            Easy tax set-aside tool for UK freelancers & sole traders
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ==============================================
# SESSION STATE & SIDEBAR
# ==============================================
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

with st.sidebar:
    st.markdown("### Settings")
    tax_rate = st.slider(
        "Suggested tax set-aside %",
        min_value=10,
        max_value=50,
        value=25,
        step=5,
        help="Percentage of your net profit (after expenses) to set aside for tax"
    )
    st.markdown("---")
    if st.button("Clear All Data"):
        st.session_state.expenses = []
        st.success("All data cleared!")
        st.rerun()

# ==============================================
# MAIN CONTENT - TWO COLUMNS
# ==============================================
col1, col2 = st.columns([1, 1.3])

with col1:
    st.subheader("Add Income")
    monthly_income = st.number_input(
        "Monthly Gross Income (£)",
        min_value=0.0,
        value=2000.0,
        step=100.0,
        format="%.2f",
        key="income_input"
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

    # Tax pot based on net cash (profit)
    if net_cash > 0:
        tax_pot = net_cash * (tax_rate / 100)
        tax_pot_display = f"£{tax_pot:,.2f}"
        tax_delta = None
    else:
        tax_pot = 0.0
        tax_pot_display = "£0.00 (no profit)"
        tax_delta = "⚠️ Expenses exceed income!"

    # Display key metrics
    st.metric("Monthly Income", f"£{total_income:,.2f}")
    st.metric("Total Expenses", f"£{total_expenses:,.2f}", delta=f"-£{total_expenses:,.2f}")
    st.metric("Net Cash (Profit)", f"£{net_cash:,.2f}", delta_color="normal")
    st.metric(
        "Suggested Tax Pot to Set Aside",
        tax_pot_display,
        delta=tax_delta,
        help=f"Based on {tax_rate}% of your net cash/profit after expenses (recommended for realistic cash flow)."
    )

    # Expenses table
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(
            df.style.format({"Amount": "£{:,.2f}"}),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No expenses added yet. Start adding above!")

# ==============================================
# FOOTER DISCLAIMER
# ==============================================
st.markdown("---")
st.caption(
    "TaxPot Tracker MVP — Estimates only. Not official financial or tax advice. "
    "Always check with HMRC or your accountant. Built by a UK accountant student."
)
