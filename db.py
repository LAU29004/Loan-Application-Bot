import mysql.connector
from config import DB_CONFIG

conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor(dictionary=True)

def insert_application(data):
    cur.execute("""
        INSERT INTO loan_applications
        (applicant_name, loan_type, income, debt,
         estimated_credit_score, eligibility, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, data)
    conn.commit()

def fetch_applications():
    cur.execute("""
        SELECT * FROM loan_applications
        ORDER BY created_at DESC
    """)
    return cur.fetchall()

def insert_feedback(application_id, rating, comments):
    cur.execute("""
        INSERT INTO borrower_feedback
        (application_id, rating, comments)
        VALUES (%s, %s, %s)
    """, (application_id, rating, comments))
    conn.commit()

def insert_feedback(application_id, rating, comments):
    cur.execute("""
        INSERT INTO borrower_feedback
        (application_id, rating, comments)
        VALUES (%s, %s, %s)
    """, (application_id, rating, comments))
    conn.commit()
