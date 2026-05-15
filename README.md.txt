# 🎓 MicroEarnHub — Student Micro-Skill Marketplace + Analytics System

> A student freelance marketplace with AI-powered skill matching, backed by a full Data Warehouse and Data Mining analytics system built on 245 real student survey responses from Manipal University Jaipur.

---

## 📌 Project Overview

MicroEarn Hub bridges the gap between students who have marketable micro-skills and those who need them — within the same campus community. The project has two integrated components:

| Component | Description |
|---|---|
| 🌐 **Web Application** | Full-stack Flask app for gig posting, student browsing, and skill recommendations |
| 📊 **Analytics System** | Data warehouse + data mining + 5 ML models built on 245 student survey responses |

**By:** Ziya Parween (23FE10ITE00350) & Aashi Singh (23FE10ITE00073)  
**Degree:** B.Tech Information Technology — Manipal University Jaipur, 2025–2026  
**Guidance:** Mrs. Shweta Sharma (Analytics) | Mr. Venkatesh G. Shankar (Web App)

---

## 🌐 Part 1 — Web Application (Flask)

A full-stack web app where students can offer skills as freelancers and hirers can post gigs.

### Features
- Student & Hirer registration and login
- Browse gigs with skill and budget filters
- Browse student profiles by skill, experience, and rating
- AI-powered skill recommendation engine (`/api/recommend`)
- Student and hirer dashboards
- Profile management

### Tech Stack
`Python` · `Flask` · `HTML/CSS` · `Jinja2`

### How to Run
```bash
cd webapp
pip install flask
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

---

## 📊 Part 2 — Data Warehouse & Data Mining Analytics

A complete analytics system built on a Google Form survey of **245 Manipal University Jaipur students** (collected Feb–Mar 2026).

### Dataset
| Attribute | Value |
|---|---|
| Total Responses | 245 |
| Raw Columns | 24 |
| Columns After Feature Engineering | 27 |
| Date Range | 12 Feb 2026 – 02 Mar 2026 |
| Dataset Completeness | 92.9% |

### 🏗️ Data Warehouse — Star Schema
A Star Schema was designed with 1 fact table and 4 dimension tables:

| Table | Type | Description |
|---|---|---|
| `fact_survey` | Fact | Price, earnings, adoption, hiring metrics |
| `dim_student` | Dimension | Academic level, department, experience, role |
| `dim_skill` | Dimension | Primary skill, multi-skill flag, skill count |
| `dim_time` | Dimension | Year, month, week, day of week |
| `dim_platform` | Dimension | Trust, challenges, hiring intent |

### 🔲 OLAP Operations
Six OLAP operations performed — Data Cube, Slice, Dice, Roll-Up, Drill-Down, and Pivot.

Key finding: CS/IT students average **Rs. 10,048/month**; Data Science averages **Rs. 14,104/month**.

### ⛏️ Data Mining

**Association Rule Mining (Apriori)**
- 49 frequent itemsets and 31 association rules discovered
- Strongest rule: Students hiring for Data Analysis also need Excel (Lift: **10.21**, Confidence: **100%**)
- Tutoring + Academic Support co-occur with 100% confidence

**K-Means Clustering — 4 Student Segments**

| Cluster | Segment | Avg Price (Rs.) | Avg Hours/Week |
|---|---|---|---|
| 0 | High-Earner Pro | 2,414 | 13.3 |
| 1 | Beginner | 2,250 | 15.6 |
| 2 | Active Freelancer + Hirer | 1,720 | 11.6 |
| 3 | Platform Adopter (New) | 2,127 | 7.2 |

**Price Gap Analysis**
| Metric | Value |
|---|---|
| Avg Freelancer Rate | Rs. 2,082/task |
| Avg Hirer Budget | Rs. 1,543/task |
| Price Gap | **Rs. +539** (freelancers charge more) |

### 🤖 Machine Learning Models (5 Models)

| Model | Task | Best Algorithm | Result |
|---|---|---|---|
| M1: Platform Adoption | Binary Classification | Logistic Regression | **72.3% accuracy** |
| M2: Price Range Prediction | Multiclass Classification | Random Forest | 34.0% accuracy |
| M3: Monthly Earning Potential | Regression | Random Forest Regressor | **R² = 1.000, MAE = Rs. 37** |
| M4: Hiring Likelihood | Binary Classification | Logistic Regression | **76.6% accuracy** |
| M5: Earning Tier Classifier | 3-class Classification | Random Forest | **89.36% accuracy** |

### 💡 Key Business Insights
- **72%** of students are predicted to adopt the platform — strong market viability
- Experienced Web/App Development students can earn up to **Rs. 24,750/month**
- All major skills show **supply exceeding demand** — focus should be on matchmaking quality, not supply expansion
- **Rs. 539 price gap** between freelancers and hirers requires a negotiation or dynamic pricing feature
- **3rd Year UG students** are the most active group on both supply and demand sides
- **Payment security** and client discovery are the top adoption barriers

---

## 📁 Repository Structure

```
MicroEarnHub/
│
├── webapp/                        # Flask web application
│   ├── app.py                     # Main Flask app
│   ├── templates/                 # HTML pages
│   │   ├── landing.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── student_dashboard.html
│   │   ├── hirer_dashboard.html
│   │   ├── browse_gigs.html
│   │   ├── browse_students.html
│   │   ├── profile.html
│   │   ├── post_gig.html
│   │   └── tools.html
│   └── static/
│       └── css/
│           └── style.css
│
├── data_mining/                   # Jupyter notebook
│   └── MicroEarnHub_DataMining.ipynb
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Full Tech Stack

| Layer | Tools |
|---|---|
| Web Framework | Flask, Jinja2 |
| Data Processing | pandas, numpy |
| Visualisation | matplotlib, seaborn, plotly |
| Machine Learning | scikit-learn, XGBoost |
| Data Mining | mlxtend (Apriori, TransactionEncoder) |
| Notebook Environment | Google Colab / Jupyter |
| Data Source | Google Form Survey — 245 responses |

---

## 🚀 Getting Started

### Web App
```bash
cd webapp
pip install flask
python app.py
# Open http://127.0.0.1:5000
```

### Data Mining Notebook
Open `data_mining/MicroEarnHub_DataMining.ipynb` in **Google Colab** or **Jupyter Notebook**

Install dependencies:
```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn xgboost mlxtend openpyxl
```