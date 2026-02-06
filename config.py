import os
import streamlit as st
# DATABASE CONFIG
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Nox@123456789",
    "database": "lending_db",
    "port": 3306,
}

# API KEYS
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]


# AI MODEL
MODEL_NAME = "models/gemini-flash-latest"

# LOAN RULES (INPUT TO SCALEDOWN)
RAW_LOAN_RULES = """
Mortgage:
- Minimum credit score: 620
- Max DTI: 45%
- Minimum income: $50,000

Auto:
- Minimum credit score: 650
- Minimum income: $30,000

Personal:
- Minimum credit score: 580
- Minimum income: $25,000
"""
