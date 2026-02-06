# 🎵 Worship Analytics Dashboard

> An End-to-End Data Engineering and Analysis project for music repertoire management.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)
![Status](https://img.shields.io/badge/Status-Finished-success)

## 🎯 The Problem
Managing a music ministry's repertoire often generates scattered data (execution history vs. total inventory). The challenge was to answer critical business questions such as:
- *"Which songs are we overplaying?"*
- *"Which songs from our library are currently forgotten (backlog)?"*
- *"What is the balance between Upbeat and Slow songs?"*

## 💡 The Solution
I developed a complete data pipeline and an interactive web application that merges execution history with the total inventory, generating strategic KPIs for leadership decision-making.

---

## 🏗️ Project Architecture

The project is structured in two distinct phases, from data extraction to visualization:

### 🧪 Phase 1: ETL & Data Engineering
**File:** [`ETL_ADOLESCENTES.ipynb`](ETL_ADOLESCENTES.ipynb)

This Jupyter Notebook contains the raw engineering logic. It acts as the "Laboratory" where data is processed before reaching the dashboard.
- **Ingestion:** Reading multiple raw CSV files (Executions, Songs database).
- **Data Cleaning:** Handling trailing spaces (`strip`), standardizing string cases (`upper`), and managing null values.
- **Transformation:** Using `pd.merge` (Left Join) to cross-reference Execution IDs with Song Metadata.
- **Output:** Generates the refined dataset `DADOS_DASHBOARD_FINAL.csv`.

### 🏭 Phase 2: Web Application & Visualization
**File:** `app.py`

The production-ready dashboard built with **Streamlit** that consumes the processed data.
- **Performance:** Implementation of Cache (`@st.cache_data`) to optimize loading times.
- **Business Logic:** Implementation of Set Theory algorithms to identify the "Backlog" (Difference between Total Inventory and Played Songs).
- **Visualization:** Interactive charts using **Plotly Express**.

---

## 📊 Dashboard Features

1.  **Real-Time KPIs:** Total executions, Repertoire Turnover Rate, and Backlog Size.
2.  **Demand Analysis (Executions):** Ranking of most played songs and artists.
3.  **Supply Analysis (Inventory):** Overview of what is available in the database vs. what is actually used.
4.  **Backlog X-Ray (Opportunities):**
    - Identifies songs that have **never been played** within the selected filter.
    - "Green Light" charts to suggest new songs for rehearsals.
5.  **Dynamic Filters:** Global filtering by Musical Style (Upbeat/Slow) that recalculates all metrics, including the backlog.

## 🛠️ Tech Stack

* **Language:** Python
* **Data Manipulation:** Pandas (ETL, Merges, Cleaning)
* **Visualization:** Plotly Express
* **Web Framework:** Streamlit
* **IDE:** VS Code / Google Colab

## 🚀 How to run locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/REPO_NAME.git](https://github.com/YOUR_USERNAME/REPO_NAME.git)

2. Create a virtual enviroment
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install dependencies
    pip install -r requirements.txt

4. Run Tthe Dashboard 
    streamlit run app.py

📈 Key Learnings
During development, I deepened my knowledge in:

**ETL Processes:** The importance of cleaning data (handling trailing spaces that caused duplicate records) inside Jupyter Notebooks.

**Data Engineering:** Building a robust pipeline to ensure data integrity before visualization.

**Streamlit:** Managing application state and layout (Tabs, Columns, Sidebar).

**Business Intelligence:** Differentiating between "Stock" (Inventory) vs. "Flow" (Execution) metrics.

Developed by [Matheus] 👨‍💻