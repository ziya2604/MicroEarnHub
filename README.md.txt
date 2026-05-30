# MicroEarnHub — Student Micro-Skill Marketplace + Analytics System

> A student freelance marketplace with AI-powered skill matching, backed by a Data Warehouse and Data Mining analytics system built on student survey responses.

---

## Project Overview

MicroEarn Hub bridges the gap between students who have marketable micro-skills and those who need them — within the same campus community. The project has two integrated components:

| Component | Description |
|---|---|
| Web Application | Full-stack Flask app for gig posting, student browsing, and skill recommendations |
| Analytics and Prediction System | Data warehouse + data mining + ML models built on student survey responses |

By: Ziya Parween (23FE10ITE00350) & Aashi Singh (23FE10ITE00073)

---

## Part 1 — Web Application

A full-stack web app where students can offer skills as freelancers and hirers can post gigs.

### Features
- Student & Hirer registration and login
- Browse gigs with skill and budget filters
- Browse student profiles by skill, experience, and rating
- AI-powered skill recommendation engine (`/api/recommend`)
- Student and hirer dashboards
- Profile management

### Tech Stack
`Python` · `Flask` · `Jinja2` · `HTML/CSS`

### How to Run
```bash
cd webapp
pip install flask
python app.py
```
Open http://127.0.0.1:5000 in your browser.

---

## Part 2 — Data Warehouse & Data Mining Analytics

### Dataset
| Attribute | Value |
|---|---|
| Total Responses | 245 |
| Real Data | 45 |
| Synthetic Data | 200 |
| Schema | Star Schema (1 Fact + 4 Dimensions) |

### OLAP Operations
| Operation | Description |
|---|---|
| Data Cube | Academic Level × Experience → Avg Price |
| Slice | 3rd Year Undergrads |
| Dice | Exp + Freelancer + Price ≥ ₹1500 |
| Roll-Up | Dept → Group → Total |
| Drill-Down | Dept → Skill |
| Pivot | Experience × Skill → Earning |

### EDA Insights
| Metric | Value |
|---|---|
| Largest Segment | 3rd Year Undergrad (76 students) |
| Top Skill | Web/App Development |
| Avg Price | ₹2,082/task |
| Avg Monthly Earning | ₹12,017 |
| Adoption Rate | 74% |

### Data Mining
**Association Rule Mining (Apriori)**
- 49 frequent itemsets, 31 association rules
- Strongest rule: Data Analysis ↔ Excel (Lift: 10.21, Confidence: 100%)
- Tutoring + Academic Support co-occur with 100% confidence

**K-Means Clustering — 4 Student Segments**
| Cluster | Segment | Avg Price (₹) | Avg Hours/Week |
|---|---|---|---|
| 0 | High-Earner Pro | 2,414 | 13.3 |
| 1 | Beginner | 2,250 | 15.6 |
| 2 | Active Freelancer + Hirer | 1,720 | 11.6 |
| 3 | Platform Adopter (New) | 2,127 | 7.2 |

**Price Gap Analysis**
| Metric | Value |
|---|---|
| Avg Freelancer Rate | ₹2,082/task |
| Avg Hirer Budget | ₹1,543/task |
| Price Gap | ₹+539 (freelancers charge more) |

---

## Machine Learning Models

| Model | Task | Algorithm | Result |
|---|---|---|---|
| M1: Pay Prediction | Regression | Random Forest (Leakage Fixed) | MAE: ₹6,415 · R²: 0.10 |
| M2: Income Classification | Binary Classification | Random Forest | Accuracy: 77% |
| M3: Hiring Prediction | Classification | Logistic Regression | Accuracy: 83% · Precision: 1.00 · Recall: 0.11 |
| M4: Recommendation System | Similarity-Based | KNN | Distance-based (lower = more similar) |

> Note: M3 recall is low due to class imbalance — improvement planned.

---

## Key Business Insights
1. Majority of students are likely to adopt the platform
2. Web Development + experience → highest earning potential
3. 3rd Year UG students are the most active segment
4. Users frequently act as both freelancers and hirers
5. Hiring prediction is affected by class imbalance — needs addressing
6. Price gap of ₹539 between freelancer rates and hirer budgets requires a negotiation or dynamic pricing feature

---

## Full Tech Stack
| Layer | Tools |
|---|---|
| Web Framework | Python, Flask |
| Frontend | HTML, CSS |
| Data Processing | pandas, numpy |
| Visualisation | matplotlib, seaborn, plotly |
| Machine Learning | scikit-learn, XGBoost |
| Data Mining | mlxtend (Apriori, TransactionEncoder) |
| Notebook Environment | Google Colab / Jupyter |
| Data Source | Google Form Survey — 245 responses |

---

## Repository Structure
```
MicroEarnHub/
│
├── webapp/
│   ├── app.py
│   ├── templates/
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
├── data_mining/
│   └── MicroEarnHub_DataMining.ipynb
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### Web App
```bash
cd webapp
pip install flask
python app.py
# Open http://127.0.0.1:5000
```

### Data Mining Notebook
Open `data_mining/MicroEarnHub_DataMining.ipynb` in Google Colab or Jupyter Notebook.

```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn xgboost mlxtend openpyxl
```
