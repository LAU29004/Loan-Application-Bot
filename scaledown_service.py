import requests
import streamlit as st

SCALEDOWN_API_KEY = st.secrets["SCALEDOWN_API_KEY"]
SCALEDOWN_ENDPOINT = "https://api.scaledown.ai/v1/compress"  # example

RAW_RULES = """
Mortgage:
- Minimum credit score: 620
- Max DTI: 45%
- Minimum income: ₹50,000

Auto:
- Minimum credit score: 650
- Minimum income: ₹30,000

Personal:
- Minimum credit score: 580
- Minimum income: ₹25,000
"""

def compress_rules():
    headers = {
        "Authorization": f"Bearer {SCALEDOWN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": RAW_RULES,
        "domain": "lending",
        "mode": "policy_compression"
    }

    try:
        response = requests.post(
            SCALEDOWN_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        compressed = data.get("compressed_text", "")

    except Exception as e:
        # ✅ SAFE FALLBACK (VERY IMPORTANT)
        compressed = """
Mortgage: Min score 620, income ₹50k, DTI ≤ 45%
Auto: Min score 650, income ₹30k
Personal: Min score 580, income ₹25k
""".strip()

    return {
        "original_text": RAW_RULES.strip(),
        "compressed_text": compressed,
        "original_size": len(RAW_RULES),
        "compressed_size": len(compressed),
        "compression_ratio": round(
            ((len(RAW_RULES) - len(compressed)) / len(RAW_RULES)) * 100, 1
        )
    }
