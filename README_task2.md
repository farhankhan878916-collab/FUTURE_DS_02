# 🔁 Customer Retention & Churn Analysis
**Future Interns — Data Science & Analytics Task 2 (2026)**

An end-to-end retention analytics project: cohort analysis, churn segmentation, and an interactive client-ready dashboard with a formal report and prioritized recommendations.

---

## 🖥️ Dashboard Preview

**Overview & Churn Gauge**
![Dashboard Overview](screenshot_1_overview.png)

**Cohort Retention Curve & Churn Reasons**
![Cohort & Reasons](screenshot_2_cohort.png)

**Churn Drivers: Plan, Usage & Support**
![Churn Drivers](screenshot_3_drivers.png)

Open `dashboard.html` in any browser to explore it live — no installation needed.

---

## 🧩 Problem Statement
A subscription SaaS business (**Orbit SaaS** — simulated, anonymized data representing a realistic multi-plan subscription product) needed to understand:
- Why customers leave the platform
- Which customer segments are most likely to churn
- How long customers typically stay active (cohort retention)
- What actions can improve retention

## 🗂️ Dataset
- **File:** [`Customer_Data.xlsx`](./Customer_Data.xlsx) / [`customer_data.csv`](./customer_data.csv)
- **Size:** 4,636 customers | signups Jan 2024 – Oct 2025, observed through Dec 2025
- **Fields:** Customer ID, Signup Date, Plan, Region, Acquisition Channel, Monthly Revenue, Support Tickets, Usage Score, Satisfaction Score, Tenure (months), Churned (Y/N), Churn Date, Churn Reason
- Simulated data built to mirror a real SaaS subscription business across 3 plans (Basic/Pro/Enterprise), 4 regions, and 5 acquisition channels, with churn probability realistically driven by plan tier, product usage, and support ticket volume.

## 🛠️ Tools Used
- **Python (pandas)** — data generation, cohort construction, churn segmentation
- **HTML / CSS / JavaScript (Chart.js)** — interactive retention dashboard
- **Microsoft Word (docx)** — client-ready analysis report

## 📈 What Was Analyzed
- Overall churn rate & retention rate, active vs. lost MRR
- Monthly cohort retention curves (first 12 months since signup)
- Churn rate by subscription plan, region, and acquisition channel
- Churn rate by product usage score and support ticket volume
- Stated churn reasons (exit survey style breakdown)
- Monthly new signups vs. churned customers trend

## 🔑 Key Insights
1. Overall churn is **32.2%**, with the sharpest drop-off in the **first 3 months** after signup.
2. **Basic plan** customers churn at **36.9%**, nearly double the **Enterprise** rate of **24.0%**.
3. **Missing features** and **pricing** together account for **over 40%** of stated churn reasons — more than support issues.
4. Customers in the **lowest usage bracket churn ~37%** vs. **27%** for highly engaged users — usage is a leading indicator.
5. Customers with **5+ support tickets churn 36.6%** of the time vs. **28.3%** for zero-ticket customers.
6. **Partnership-acquired** customers churn least (26.1%); **Social Media-acquired** customers churn most (35.4%).

## ✅ Recommendations
- Build a structured 90-day onboarding flow — most churn happens before month 3.
- Re-position the Basic plan: enrich its feature set or nudge engaged users toward Pro.
- Prioritize product roadmap items around the top stated "missing features" churn reason.
- Trigger proactive outreach when a customer's usage score drops below 50.
- Treat support ticket count as an early-warning churn signal and tighten SLAs.
- Reallocate marketing spend toward Partnership and Organic channels, which retain best.

## 📁 Repository Contents
| File | Description |
|---|---|
| `customer_data.csv` / `Customer_Data.xlsx` | Cleaned raw dataset |
| `dashboard.html` | Interactive client-ready retention & churn dashboard |
| `Retention_Churn_Report.docx` | Full analysis report with insights & recommendations |
| `generate_data.py` | Script used to simulate the customer/subscription dataset |
| `analyze.py` | Python script for churn, cohort, and segmentation analysis |
| `screenshot_1_overview.png`, `screenshot_2_cohort.png`, `screenshot_3_drivers.png` | Dashboard preview images |

## 🎓 About This Task
Completed as part of the **Future Interns – Data Science & Analytics Task 2 (2026)**: *Customer Retention & Churn Analysis.*
[Future Interns on LinkedIn](https://www.linkedin.com/company/future-interns/)
