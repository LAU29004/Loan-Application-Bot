import streamlit as st
import pandas as pd
import plotly.express as px

from db import insert_application, fetch_applications, insert_feedback
from models import estimate_credit_score, check_eligibility, calculate_emi
from chatbot import ask_loan_bot
from scaledown_service import compress_rules

# =====================================================
# PAGE CONFIG (DO NOT SET initial_sidebar_state)
# =====================================================
st.set_page_config(
    page_title="LoanSense - AI-Powered Lending Platform",
    layout="wide"
)

# =====================================================
# SIDEBAR (MUST BE FIRST UI ELEMENT)
# =====================================================
with st.sidebar:
    st.markdown("## 🏦 LoanSense")
    st.caption("AI-Powered Lending Platform")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Home",
            "AI Advisor",
            "Pre-Qualification",
            "EMI Calculator",
            "My Applications",
            "Admin Dashboard",
            "Feedback",
        ],
        index=0
    )

# Normalize page value
page = page.lower().replace(" ", "_")

# =====================================================
# BASIC CSS (AFTER SIDEBAR)
# =====================================================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# HOME
# =====================================================
if page == "home":
    st.title("Smart Lending, Instant Decisions")
    st.caption("Get pre-qualified for loans in under 2 minutes")

    c1, c2, c3 = st.columns(3)
    c1.metric("Avg Decision Time", "2 min")
    c2.metric("Approval Automation", "50%")
    c3.metric("Doc Reduction", "80%")

    st.markdown("### Choose a Loan")
    cols = st.columns(3)
    cols[0].info("🏠 **Mortgage**\n\nLow rates, long tenure")
    cols[1].info("🚗 **Auto Loan**\n\nQuick vehicle financing")
    cols[2].info("💳 **Personal Loan**\n\nFlexible usage")

# =====================================================
# AI ADVISOR
# =====================================================
elif page == "ai_advisor":
    st.title("💬 AI Loan Advisor")

    if "chat" not in st.session_state:
        st.session_state.chat = [
            {
                "role": "assistant",
                "content": "Hi! I can help you with loan eligibility, EMIs, and next steps."
            }
        ]

    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).markdown(msg["content"])

    question = st.chat_input("Ask me anything about loans…")
    if question:
        st.session_state.chat.append({"role": "user", "content": question})
        answer = ask_loan_bot(question)
        st.session_state.chat.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.button("🧹 Clear Chat"):
        st.session_state.chat = st.session_state.chat[:1]
        st.rerun()

# =====================================================
# PRE-QUALIFICATION
# =====================================================
elif page == "pre-qualification":
    st.title("📋 Pre-Qualification")

    col1, col2 = st.columns([2, 1])

    with col1:
        name = st.text_input("Full Name")
        loan_type = st.selectbox("Loan Type", ["Mortgage", "Auto", "Personal"])
        income = st.number_input("Annual Income (₹)", 0, 1_000_000, 60000, step=1000)
        debt = st.number_input("Annual Debt (₹)", 0, 500_000, 15000, step=1000)
        history = st.slider("Credit History (Years)", 0, 30, 6)

    with col2:
        score = estimate_credit_score(income, debt, history)
        eligible = check_eligibility(loan_type, score, income, debt)

        st.metric("Estimated Credit Score", score)

        if eligible:
            st.success("✅ Eligible for Loan")
        else:
            st.warning("⚠️ Manual Review Required")

        if st.button("Submit Application"):
            if not name:
                st.error("Name required")
            else:
                insert_application((
                    name,
                    loan_type,
                    income,
                    debt,
                    score,
                    eligible,
                    "Pre-Qualified" if eligible else "Manual Review"
                ))
                st.success("Application submitted successfully")

# =====================================================
# EMI CALCULATOR
# =====================================================
elif page == "emi_calculator":
    st.title("💰 EMI Calculator")

    with st.form("emi_form"):
        amount = st.number_input("Loan Amount (₹)", 1_000, 500_000, 50_000, step=1_000)
        rate = st.number_input("Interest Rate (%)", 1.0, 20.0, 7.0, step=0.1)
        years = st.number_input("Tenure (Years)", 1, 30, 5)
        submitted = st.form_submit_button("Calculate EMI")

    if submitted:
        emi = calculate_emi(amount, rate, years)
        total = emi * years * 12

        c1, c2, c3 = st.columns(3)
        c1.metric("Monthly EMI", f"₹{emi:,.2f}")
        c2.metric("Total Payment", f"₹{total:,.2f}")
        c3.metric("Interest Paid", f"₹{total - amount:,.2f}")

# =====================================================
# MY APPLICATIONS
# =====================================================
elif page == "my_applications":
    st.title("📊 My Applications")

    apps = fetch_applications()
    if not apps:
        st.info("No applications yet")
    else:
        df = pd.DataFrame(apps)
        df["Status"] = df["eligibility"].map({1: "Pre-Qualified", 0: "Manual Review"})

        display = df[
            ["id", "applicant_name", "loan_type", "income",
             "estimated_credit_score", "Status", "created_at"]
        ]

        display.columns = [
            "ID", "Applicant", "Loan Type", "Income",
            "Credit Score", "Status", "Date"
        ]

        st.dataframe(display, use_container_width=True)

# =====================================================
# ADMIN DASHBOARD
# =====================================================
elif page == "admin_dashboard":
    st.title("📈 Admin Dashboard")
    st.caption("Compression powered by ScaleDown.ai (with local fallback)")
    st.info("Admin access only (authentication omitted for demo)")

    apps = fetch_applications()
    if not apps:
        st.info("No data available")
    else:
        df = pd.DataFrame(apps)

        total = len(df)
        approved = len(df[df["eligibility"] == 1])
        avg_score = df["estimated_credit_score"].mean()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Applications", total)
        c2.metric("Approval Rate", f"{approved / total * 100:.1f}%")
        c3.metric("Avg Credit Score", f"{avg_score:.0f}")

        fig = px.bar(
            df["loan_type"].value_counts(),
            labels={"index": "Loan Type", "value": "Applications"}
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("## ⚡ ScaleDown.ai – Rule Compression Engine")
        sd = compress_rules()

        col1, col2 = st.columns(2)
        with col1:
            st.code(sd["original_text"])
            st.metric("Original Size", sd["original_size"])
        with col2:
            st.code(sd["compressed_text"])
            st.metric("Compressed Size", sd["compressed_size"])

        c1, c2, c3 = st.columns(3)
        c1.metric("Compression Achieved", f"{sd['compression_ratio']}%")
        c2.metric("Decision Time", "2 min", delta="-2 days")
        c3.metric("Underwriter Load", "↓ 50%")

# =====================================================
# FEEDBACK
# =====================================================
elif page == "feedback":
    st.title("⭐ Feedback")

    apps = fetch_applications()
    if not apps:
        st.info("Submit an application first")
    else:
        app_ids = [a["id"] for a in apps]
        selected = st.selectbox("Application ID", app_ids)
        rating = st.slider("Rating", 1, 5, 5)
        comments = st.text_area("Comments")

        if st.button("Submit Feedback"):
            insert_feedback(selected, rating, comments)
            st.success("Thanks for your feedback!")
