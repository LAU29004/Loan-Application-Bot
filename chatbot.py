from google import genai
from config import MODEL_NAME, GEMINI_API_KEY, RAW_LOAN_RULES

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_loan_bot(question):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"""
You are a professional AI lending assistant for the Indian market.

IMPORTANT RULES:
- Always use Indian Rupees (₹), never dollars.
- Assume income values are annual and expressed in INR.
- Use Indian lending context and terminology.
- Do not mention USD or foreign banking systems.

Personal Loan Rules:
- Minimum income: ₹25,000 per year
- Minimum credit score: 580


Loan Rules:
{RAW_LOAN_RULES}

User Question:
{question}
"""
    )
    return response.text
