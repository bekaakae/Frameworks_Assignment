# Frameworks_Assignment
 CORD-19 COVID-19 Research Analysis

# CORD-19 COVID-19 Research Analysis

This project provides a comprehensive analysis of the CORD-19 dataset and an interactive web application to explore COVID-19 research trends.

## Project Structure
Frameworks_Assignment/
│
├── 📄 **ANALYSIS SCRIPTS** (Part 1-3)
│   ├── 1_exploration.py
│   ├── 2_cleaning.py
│   ├── 3_analysis.py
│   └── run_all.py (or run_analysis.py)
│
├── 🌐 **STREAMLIT APP** (Part 4)
│   ├── app.py
│   └── requirements.txt
│
├── 📊 **GENERATED VISUALIZATIONS** (Part 3)
│   ├── figures/
│   │   ├── publications_by_year.png
│   │   ├── top_journals.png
│   │   ├── common_words.png
│   │   ├── wordcloud.png
│   │   └── abstract_length.png
│
├── 📁 **DATA FILES**
│   ├── metadata.csv (original - from Kaggle)
│   ├── cleaned_metadata.csv
│
├── 📝 **REPORTS & DOCUMENTATION** (Part 5)
│   ├── exploration_results.txt
│   ├── cleaning_report.txt
│   ├── analysis_report.txt
│
└── ⚙️ **CONFIGURATION FILES**
    ├── .gitignore
## Installation

1. Clone this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
Download metadata.csv from the CORD-19 dataset on Kaggle and place it in the project directory.

Usage
Run Complete Analysis
bash
python main.py
Run Individual Components
Data exploration:

bash
python exploration.py
Data cleaning:

bash
python cleaning.py
Data analysis:

bash
python analysis.py
Streamlit app:

bash
streamlit run app.py
Features
Data Exploration: Basic statistics and missing value analysis

Data Cleaning: Handling missing values and data type conversion

Visualizations:

Publications over time

Top publishing journals

Word frequency analysis

Word clouds

Interactive Dashboard: Filter data by year and journal

Key Findings
[Add your specific findings here after running the analysis]

Challenges and Learnings
[Document your experience with the project]

License
This project is for educational purposes as part of the Frameworks assignment.

text

## How to Run the Project

1. **Setup**:
   ```bash
   pip install -r requirements.txt
Download data: Get metadata.csv from Kaggle and place in project directory

Run analysis:

bash
python main.py
Launch app:

bash
streamlit run app.py
This complete solution covers all the requirements and provides a professional-grade analysis pipeline with an interactive web application. The code is well-commented, modular, and follows best practices for data analysis projects.
