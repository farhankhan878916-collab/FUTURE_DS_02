import pandas as pd
import numpy as np

np.random.seed(7)

# ---- Setup ----
N = 4700
plans = ["Basic", "Pro", "Enterprise"]
plan_weights = [0.5, 0.35, 0.15]
plan_price = {"Basic": 499, "Pro": 1499, "Enterprise": 4999}
regions = ["North", "South", "East", "West"]
region_weights = [0.27, 0.25, 0.26, 0.22]
acquisition = ["Organic Search", "Paid Ads", "Referral", "Social Media", "Partnership"]
acq_weights = [0.30, 0.26, 0.20, 0.16, 0.08]
churn_reasons = ["Too expensive", "Missing features", "Poor support experience",
                  "Switched to competitor", "No longer needed", "Low product usage"]

signup_start = pd.Timestamp("2024-01-01")
signup_end = pd.Timestamp("2025-10-31")
analysis_date = pd.Timestamp("2025-12-31")

rows = []
cust_id = 5000

# signup volume grows slightly over time (business growing)
all_days = pd.date_range(signup_start, signup_end, freq="D")
for d in all_days:
    days_since_start = (d - signup_start).days
    growth = 1 + days_since_start / 500  # gradual growth
    n_signups = np.random.poisson(4.2 * growth)
    for _ in range(n_signups):
        plan = np.random.choice(plans, p=plan_weights)
        region = np.random.choice(regions, p=region_weights)
        acq = np.random.choice(acquisition, p=acq_weights)
        support_tickets = np.random.poisson(2.5)
        # usage score 0-100 (product engagement)
        usage_score = np.clip(np.random.normal(62, 20), 5, 100)
        # NPS-like satisfaction
        satisfaction = np.clip(np.random.normal(7, 2), 1, 10)

        # churn probability depends on plan, usage, support tickets, satisfaction
        base_hazard = {"Basic": 0.022, "Pro": 0.013, "Enterprise": 0.007}[plan]
        usage_factor = (100 - usage_score) / 100 * 0.020
        support_factor = min(support_tickets, 8) * 0.0022
        satisfaction_factor = (10 - satisfaction) / 10 * 0.014
        monthly_hazard = base_hazard + usage_factor + support_factor + satisfaction_factor
        monthly_hazard = np.clip(monthly_hazard, 0.005, 0.35)

        # simulate month-by-month survival until analysis_date or churn
        tenure_months = 0
        churned = False
        max_possible_months = int((analysis_date - d).days / 30.44)
        for m in range(max_possible_months + 1):
            tenure_months = m
            if np.random.random() < monthly_hazard:
                churned = True
                break
        churn_date = d + pd.Timedelta(days=int(tenure_months * 30.44)) if churned else pd.NaT
        reason = np.random.choice(churn_reasons, p=[0.22, 0.20, 0.18, 0.16, 0.14, 0.10]) if churned else None

        mrr = plan_price[plan]

        rows.append({
            "Customer_ID": f"CUST-{cust_id}",
            "Signup_Date": d.strftime("%Y-%m-%d"),
            "Plan": plan,
            "Region": region,
            "Acquisition_Channel": acq,
            "Monthly_Revenue": mrr,
            "Support_Tickets": support_tickets,
            "Usage_Score": round(usage_score, 1),
            "Satisfaction_Score": round(satisfaction, 1),
            "Tenure_Months": tenure_months,
            "Churned": churned,
            "Churn_Date": churn_date.strftime("%Y-%m-%d") if churned else "",
            "Churn_Reason": reason if reason else ""
        })
        cust_id += 1
        if cust_id - 5000 >= N:
            break
    if cust_id - 5000 >= N:
        break

df = pd.DataFrame(rows)
df.to_csv("/home/claude/project2/customer_data.csv", index=False)
print(df.shape)
print(df.head())
print("Churn rate:", df["Churned"].mean())
print(df["Plan"].value_counts())
