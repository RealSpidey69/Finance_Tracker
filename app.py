import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Finance Tracker", page_icon="💸", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0f0f0f; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
    }
    .stMetric { background: #1a1a2e; border-radius: 10px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("💸 Finance Tracker")
st.caption("Know where every rupee goes")

# Session state
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Sidebar
st.sidebar.header("➕ Add Expense")
category = st.sidebar.selectbox("Category", 
    ["🍕 Food", "🚗 Transport", "🛍️ Shopping", "🎬 Entertainment", "📚 Study", "💊 Health", "🏠 Rent", "⚡ Other"])
description = st.sidebar.text_input("Description")
amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=10.0)
expense_date = st.sidebar.date_input("Date", value=date.today())
budget = st.sidebar.number_input("Monthly Budget (₹)", min_value=0.0, step=500.0, value=5000.0)
add_btn = st.sidebar.button("Add Expense ✅", use_container_width=True)

if add_btn and description and amount > 0:
    st.session_state.expenses.append({
        "Category": category,
        "Description": description,
        "Amount": amount,
        "Date": str(expense_date)
    })
    st.sidebar.success("Added!")

if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    total = df["Amount"].sum()
    top_category = df.groupby("Category")["Amount"].sum().idxmax()

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Spent", f"₹{total:,.0f}")
    col2.metric("🎯 Budget Left", f"₹{budget - total:,.0f}", delta=f"-₹{total:,.0f}")
    col3.metric("🔥 Top Category", top_category.split()[1])
    col4.metric("📝 Transactions", len(df))

    st.markdown("---")

    # Budget progress bar
    progress = min(total / budget, 1.0) if budget > 0 else 0
    st.subheader("📊 Budget Usage")
    st.progress(progress)
    if progress >= 0.9:
        st.error("⚠️ You've almost hit your budget!")
    elif progress >= 0.7:
        st.warning("🟡 You're at 70% of your budget")
    else:
        st.success("✅ You're doing great!")

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Spending by Category")
        pie = px.pie(df, names="Category", values="Amount",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    hole=0.4)
        pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(pie, use_container_width=True)

    with col2:
        st.subheader("Spending Over Time")
        line = px.bar(df, x="Date", y="Amount", color="Category",
                     color_discrete_sequence=px.colors.sequential.Purples_r)
        line.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(line, use_container_width=True)

    st.markdown("---")

    # Expense table
    st.subheader("🧾 All Expenses")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Download
    csv = df.to_csv(index=False)
    st.download_button("📥 Download as CSV", csv, "expenses.csv", "text/csv")

else:
    st.info("👈 Add your first expense from the sidebar to get started!")
    