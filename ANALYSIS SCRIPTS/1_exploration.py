# 1_exploration.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def basic_exploration():
    print("=== STARTING BASIC DATA EXPLORATION ===")
    print("=" * 50)
    
    # Load data with specific dtype to handle mixed types
    try:
        df = pd.read_csv('metadata.csv', low_memory=False)
        print("SUCCESS: Dataset loaded successfully!")
    except FileNotFoundError:
        print("ERROR: metadata.csv not found!")
        print("Please download the dataset from Kaggle and place it in this folder")
        return None
    
    # Basic information
    print(f"\nDATASET SHAPE: {df.shape}")
    print(f"Number of rows: {df.shape[0]:,}")
    print(f"Number of columns: {df.shape[1]}")
    
    # Display first few rows
    print("\nFIRST 3 ROWS:")
    print(df.head(3))
    
    # Column information
    print("\nCOLUMN INFORMATION:")
    print(df.info())
    
    # Data types
    print("\nDATA TYPES:")
    print(df.dtypes.value_counts())
    print("\nDetailed dtypes:")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype}")
    
    # Missing values analysis
    print("\nMISSING VALUES ANALYSIS:")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': missing_data,
        'Missing_Percentage': missing_percent
    }).sort_values('Missing_Count', ascending=False)
    
    print(missing_df.head(15))  # Show top 15 columns with most missing values
    
    # Basic statistics for numerical columns
    print("\nBASIC STATISTICS:")
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) > 0:
        print(df[numerical_cols].describe())
    else:
        print("No numerical columns found")
    
    # Check important columns
    important_cols = ['title', 'abstract', 'publish_time', 'journal', 'authors']
    print(f"\nIMPORTANT COLUMNS STATUS:")
    for col in important_cols:
        if col in df.columns:
            non_null = df[col].notnull().sum()
            percentage = (non_null / len(df)) * 100
            sample_val = df[col].iloc[0] if non_null > 0 else "N/A"
            print(f"  {col}: {non_null:,} non-null ({percentage:.1f}%)")
            print(f"    Sample: {str(sample_val)[:80]}...")
        else:
            print(f"  {col}: COLUMN NOT FOUND")
    
    # Check for any date-like columns
    print(f"\nDATE-LIKE COLUMNS:")
    date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    for col in date_cols:
        if col in df.columns:
            non_null = df[col].notnull().sum()
            print(f"  {col}: {non_null:,} non-null")
            if non_null > 0:
                sample = df[col].iloc[0]
                print(f"    Sample value: {sample}")
    
    return df

if __name__ == "__main__":
    df = basic_exploration()
    
    # Save exploration results
    if df is not None:
        with open('exploration_results.txt', 'w', encoding='utf-8') as f:
            f.write("CORD-19 Dataset Exploration Results\n")
            f.write("=" * 40 + "\n")
            f.write(f"Dataset shape: {df.shape}\n")
            f.write(f"Columns: {list(df.columns)}\n")
            f.write("\nMissing values:\n")
            f.write(str(df.isnull().sum()))
        print("\nEXPLORATION RESULTS saved to 'exploration_results.txt'")