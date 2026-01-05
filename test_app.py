import streamlit as st
import pandas as pd
import io

# ==============================================
# PAGE CONFIG & PROFESSIONAL THEMING
# ==============================================
st.set_page_config(
    page_title="Taxiva",
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
        font-size: 1.05em !important;
    }
    /* Hover effect on primary buttons */
    button[kind="primary"]:hover,
    .stButton > button:hover {
        background-color: #1B5E20 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
    }
    /* Delete (X) button - small round red */
    .delete-btn button {
        background-color: #c62828 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 30px !important;
        height: 30px !important;
        padding: 0 !important;
        font-size: 1.3em !important;
        line-height: 30px !important;
        border: none !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
        cursor: pointer !important;
        margin-top: 8px !important;
    }
    .delete-btn button:hover {
        background-color: #b71c1c !important;
        transform: scale(1.1);
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    /* Hide default footer & hamburger menu */
    footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    /* Better spacing & cards */
    .stMetric {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Extremely tight expense spacing */
    .expense-row {
        margin: 2px 0 !important;
        padding: 2px 0 !important;
        border-bottom: 1px solid #E5E7EB !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .expense-row:last-child {
        border-bottom: none !important;
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    .expense-row .description {
        font-size: 0.85em;
        color: #64748B;
        margin-left: 8px;
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
        <h1 style='color: #2E7D32; margin: 0; font-size: 2.8em;'>Taxiva</h1>
        <p style='color: #64748B; font-size: 1.3em; margin: 10px 0 0;'>
            Easy tax set-aside tool for UK freelancers & sole traders
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ==============================================
# SESSION STATE
# ==============================================
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'receipts' not in st.session_state:
    st.session_state.receipts = []

with st.sidebar:
    st.markdown("### Settings")
    if st.button("Clear All Data"):
        st.session_state.expenses = []
        st.session_state.receipts = []
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

    if st.button("➕ Add Expense", type="primary"):
        if exp_amount > 0:
            st.session_state.expenses.append({
                "Amount": exp_amount,
                "Category": exp_category,
                "Description": exp_description if exp_description else ""
            })
            st.success(f"Added £{exp_amount:.2f} - {exp_category}")
            st.rerun()
        else:
            st.warning("Amount must be greater than 0")

    st.subheader("Upload Receipts")
    uploaded_files = st.file_uploader("Upload receipt photos/PDFs", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in [r["name"] for r in st.session_state.receipts]:
                st.session_state.receipts.append({"name": file.name, "size": file.size})
                st.success(f"Uploaded: {file.name}")
        st.rerun()

with col2:
    st.subheader("Summary & Tax Pot")

    # Tax rate slider
    tax_rate = st.slider(
        "Suggested tax set-aside %",
        min_value=10,
        max_value=50,
        value=25,
        step=5,
        help="Percentage of your net profit (after expenses) to set aside for tax"
    )

    # Calculations
    total_income = monthly_income
    total_expenses = sum(exp["Amount"] for exp in st.session_state.expenses) if st.session_state.expenses else 0.0
    net_cash = total_income - total_expenses

    if net_cash > 0:
        tax_pot = net_cash * (tax_rate / 100)
        tax_pot_display = f"£{tax_pot:,.2f}"
        tax_delta = None
    else:
        tax_pot = 0.0
        tax_pot_display = "£0.00 (no profit)"
        tax_delta = "⚠️ Expenses exceed income!"

    st.metric("Monthly Income", f"£{total_income:,.2f}")
    st.metric("Total Expenses", f"£{total_expenses:,.2f}", delta=f"-£{total_expenses:,.2f}")
    st.metric("Net Cash (Profit)", f"£{net_cash:,.2f}", delta_color="normal")
    st.metric(
        "Suggested Tax Pot to Set Aside",
        tax_pot_display,
        delta=tax_delta,
        help=f"Based on {tax_rate}% of your net cash/profit after expenses."
    )

    # CSV Export
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Expenses as CSV",
            data=csv,
            file_name="expenses_summary.csv",
            mime="text/csv",
            type="primary"
        )

    # Expenses list with remove X
    if st.session_state.expenses:
        st.markdown("### Added Expenses")
        for i, expense in enumerate(st.session_state.expenses):
            cols = st.columns([5, 1, 0.4])
            with cols[0]:
                desc = expense['Description']
                if desc:
                    content = f"**£{expense['Amount']:.2f}** – {expense['Category']} <span class='description'>{desc}</span>"
                else:
                    content = f"**£{expense['Amount']:.2f}** – {expense['Category']}"
                st.markdown(
                    f"<div class='expense-row'>{content}</div>",
                    unsafe_allow_html=True
                )
            with cols[2]:
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                if st.button("✕", key=f"remove_{i}", type="secondary"):
                    st.session_state.expenses.pop(i)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No expenses added yet.")

    # Uploaded receipts list
    if st.session_state.receipts:
        st.markdown("### Uploaded Receipts")
        for receipt in st.session_state.receipts:
            st.write(f"📄 {receipt['name']} ({receipt['size']/1024:.1f} KB)")

# ==============================================
# FOOTER DISCLAIMER
# ==============================================
st.markdown("---")
st.caption(
    "Taxiva MVP — Estimates only. Not official financial or tax advice. "
    "Always check with HMRC or your accountant. Built by a UK accountant student."
)
