# Shadiyana Insights Dashboard

A Streamlit-based interactive dashboard to extract actionable insights from Shadiyana’s customer and vendor data.

## 📌 Objectives

- Analyze customer behavior, seasonal demand, and vendor distribution.
- Enable data-driven decisions for marketing, sales, and product strategy.

## 🛠 Tech Stack

- Python, Pandas, Streamlit
- Seaborn & Matplotlib for visualization
- Excel (.xlsx) as data source

## 📁 Structure

```
shadiyana-insights-dashboard/
├── Data-Analytics-Case-Study.xlsx                   # Excel file with customer & vendor sheets
├── app.py
└── README.md
```

## 🚀 Getting Started

```bash
git clone https://github.com/your-username/shadiyana-insights-dashboard.git
cd shadiyana-insights-dashboard
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
streamlit run shadiyana_dashboard.py
```

## 📊 Features

- Visualize query patterns by month, venue, guest count
- Analyze vendor presence by sub-area and budget
- Interactive filters and clean UI for exploration

## 📄 Deliverables

- `app.py` – Streamlit app
- `shadiyana_insights.pdf` – PDF insights summary
- `Data-Analytics-Case-Study.xlsx` – Input data

## 📂 Dependencies

Make sure you have the following Python packages installed:

- `pandas`
- `matplotlib`
- `seaborn`
- `openpyxl`
- `streamlit`

### 💻 Install via pip:

```bash
pip install pandas matplotlib seaborn openpyxl streamlit
```
