import pandas as pd
import numpy as np
import json

df = pd.read_csv("/home/claude/project2/customer_data.csv", parse_dates=["Signup_Date"])
df["Churn_Date"] = pd.to_datetime(df["Churn_Date"], errors="coerce")
df["Signup_Month"] = df["Signup_Date"].dt.to_period("M").astype(str)
analysis_date = pd.Timestamp("2025-12-31")

# ---- KPIs ----
total_customers = len(df)
churned_customers = df["Churned"].sum()
active_customers = total_customers - churned_customers
churn_rate = churned_customers / total_customers * 100
retention_rate = 100 - churn_rate
avg_tenure = df["Tenure_Months"].mean()
mrr_active = df[~df["Churned"]]["Monthly_Revenue"].sum()
mrr_churned_lost = df[df["Churned"]]["Monthly_Revenue"].sum()
avg_mrr_per_customer = df["Monthly_Revenue"].mean()

print("=== KPIs ===")
print(f"Total customers: {total_customers}")
print(f"Churned: {churned_customers} ({churn_rate:.1f}%)")
print(f"Active: {active_customers} ({retention_rate:.1f}%)")
print(f"Avg tenure (months): {avg_tenure:.1f}")
print(f"Active MRR: {mrr_active:,.0f}")
print(f"MRR lost to churn (monthly): {mrr_churned_lost:,.0f}")

# ---- Churn by plan ----
plan_churn = df.groupby("Plan").agg(
    Customers=("Customer_ID","count"),
    Churned=("Churned","sum"),
).reset_index()
plan_churn["Churn_Rate"] = plan_churn["Churned"]/plan_churn["Customers"]*100
plan_churn = plan_churn.sort_values("Churn_Rate", ascending=False)
print("\n=== Churn by Plan ===")
print(plan_churn.to_string(index=False))

# ---- Churn by region ----
region_churn = df.groupby("Region").agg(
    Customers=("Customer_ID","count"),
    Churned=("Churned","sum"),
).reset_index()
region_churn["Churn_Rate"] = region_churn["Churned"]/region_churn["Customers"]*100
region_churn = region_churn.sort_values("Churn_Rate", ascending=False)
print("\n=== Churn by Region ===")
print(region_churn.to_string(index=False))

# ---- Churn by acquisition channel ----
acq_churn = df.groupby("Acquisition_Channel").agg(
    Customers=("Customer_ID","count"),
    Churned=("Churned","sum"),
).reset_index()
acq_churn["Churn_Rate"] = acq_churn["Churned"]/acq_churn["Customers"]*100
acq_churn = acq_churn.sort_values("Churn_Rate", ascending=False)
print("\n=== Churn by Acquisition Channel ===")
print(acq_churn.to_string(index=False))

# ---- Churn reasons ----
reasons = df[df["Churned"]]["Churn_Reason"].value_counts().reset_index()
reasons.columns = ["Reason","Count"]
reasons["Pct"] = reasons["Count"]/reasons["Count"].sum()*100
print("\n=== Churn Reasons ===")
print(reasons.to_string(index=False))

# ---- Tenure distribution (bucket) ----
bins = [0,3,6,12,18,24, 999]
labels = ["0-3 mo","4-6 mo","7-12 mo","13-18 mo","19-24 mo","24+ mo"]
df["Tenure_Bucket"] = pd.cut(df["Tenure_Months"], bins=bins, labels=labels, right=True, include_lowest=True)
tenure_dist = df.groupby("Tenure_Bucket", observed=True).agg(
    Customers=("Customer_ID","count"),
    Churned=("Churned","sum")
).reset_index()
tenure_dist["Churn_Rate"] = tenure_dist["Churned"]/tenure_dist["Customers"]*100
print("\n=== Tenure Distribution ===")
print(tenure_dist.to_string(index=False))

# ---- Usage score vs churn (buckets) ----
usage_bins = [0,25,50,75,100]
usage_labels = ["0-25 (Low)","26-50 (Med-Low)","51-75 (Med-High)","76-100 (High)"]
df["Usage_Bucket"] = pd.cut(df["Usage_Score"], bins=usage_bins, labels=usage_labels, include_lowest=True)
usage_churn = df.groupby("Usage_Bucket", observed=True).agg(
    Customers=("Customer_ID","count"),
    Churned=("Churned","sum")
).reset_index()
usage_churn["Churn_Rate"] = usage_churn["Churned"]/usage_churn["Customers"]*100
print("\n=== Churn by Usage Score Bucket ===")
print(usage_churn.to_string(index=False))

# ---- Support tickets vs churn ----
supp_bins = [-1,0,2,4,999]
supp_labels = ["0 tickets","1-2 tickets","3-4 tickets","5+ tickets"]
df["Support_Bucket"] = pd.cut(df["Support_Tickets"], bins=supp_bins, labels=supp_labels)
supp_churn = df.groupby("Support_Bucket", observed=True).agg(
    Customers=("Customer_ID","count"),
    Churned=("Churned","sum")
).reset_index()
supp_churn["Churn_Rate"] = supp_churn["Churned"]/supp_churn["Customers"]*100
print("\n=== Churn by Support Ticket Bucket ===")
print(supp_churn.to_string(index=False))

# ---- Cohort retention matrix (monthly cohorts by signup month, retention % over months since signup) ----
cohort_months = sorted(df["Signup_Month"].unique())[:12]  # first 12 cohorts for a clean matrix
cohort_matrix = []
for cm in cohort_months:
    cohort_df = df[df["Signup_Month"] == cm]
    cohort_size = len(cohort_df)
    row = {"Cohort": cm, "Size": cohort_size}
    for m_offset in range(0, 12):
        # active at month m_offset means tenure >= m_offset OR (churned and tenure >= m_offset)
        still_active_count = (cohort_df["Tenure_Months"] >= m_offset).sum()
        row[f"M{m_offset}"] = round(still_active_count/cohort_size*100,1) if cohort_size>0 else None
    cohort_matrix.append(row)
cohort_df_out = pd.DataFrame(cohort_matrix)
print("\n=== Cohort Retention Matrix (first 12 cohorts) ===")
print(cohort_df_out.to_string(index=False))

# ---- Monthly new signups & churn trend ----
df["Churn_Month"] = df["Churn_Date"].dt.to_period("M").astype(str)
signup_trend = df.groupby("Signup_Month").size().reset_index(name="New_Signups")
churn_trend = df[df["Churned"]].groupby("Churn_Month").size().reset_index(name="Churned_Customers")
trend = pd.merge(signup_trend, churn_trend, left_on="Signup_Month", right_on="Churn_Month", how="outer")
trend["Month"] = trend["Signup_Month"].combine_first(trend["Churn_Month"])
trend = trend[["Month","New_Signups","Churned_Customers"]].fillna(0).sort_values("Month")
trend = trend[trend["Month"] <= "2025-12"]
print("\n=== Monthly Signup vs Churn Trend ===")
print(trend.to_string(index=False))

export = {
    "kpis": {
        "total_customers": int(total_customers),
        "churned_customers": int(churned_customers),
        "active_customers": int(active_customers),
        "churn_rate": round(churn_rate,2),
        "retention_rate": round(retention_rate,2),
        "avg_tenure": round(avg_tenure,2),
        "mrr_active": round(float(mrr_active),2),
        "mrr_churned_lost": round(float(mrr_churned_lost),2),
        "avg_mrr_per_customer": round(float(avg_mrr_per_customer),2)
    },
    "plan_churn": plan_churn.to_dict(orient="records"),
    "region_churn": region_churn.to_dict(orient="records"),
    "acq_churn": acq_churn.to_dict(orient="records"),
    "reasons": reasons.to_dict(orient="records"),
    "tenure_dist": tenure_dist.astype({"Tenure_Bucket":"str"}).to_dict(orient="records"),
    "usage_churn": usage_churn.astype({"Usage_Bucket":"str"}).to_dict(orient="records"),
    "supp_churn": supp_churn.astype({"Support_Bucket":"str"}).to_dict(orient="records"),
    "cohort_matrix": cohort_df_out.to_dict(orient="records"),
    "trend": trend.to_dict(orient="records")
}
with open("/home/claude/project2/dashboard_data.json","w") as f:
    json.dump(export, f, indent=2, default=str)
print("\nSaved dashboard_data.json")
