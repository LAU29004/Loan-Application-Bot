def estimate_credit_score(income, debt, history_years):
    if income <= 0:
        return 300

    dti = debt / income

    score = (
        500                              # base score
        + (income / 1000) * 1.5          # income impact
        - (dti * 150)                    # DTI penalty
        + (history_years * 20)           # credit history
    )

    return int(max(300, min(850, score)))



def check_eligibility(loan_type, score, income, debt):
    rules = {
        "Mortgage": (620, 50000, 0.45),
        "Auto": (650, 30000, 0.50),
        "Personal": (580, 25000, 0.40),
    }

    min_score, min_income, max_dti = rules[loan_type]
    dti = debt / income if income else 1
    return score >= min_score and income >= min_income and dti <= max_dti

def calculate_emi(amount, rate, years):
    r = rate / 12 / 100
    n = years * 12
    if r == 0:
        return amount / n
    return amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
