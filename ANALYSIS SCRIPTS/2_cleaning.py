# 2_cleaning.py
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def clean_data(df):
    print("=== STARTING DATA CLEANING PROCESS ===")
    print("=" * 50)
    
    # Create a copy
    df_clean = df.copy()
    original_size = len(df_clean)
    
    print(f"Original dataset size: {original_size:,} rows")
    print(f"Original columns: {list(df_clean.columns)}")
    
    # 1. Handle missing titles (essential column)
    print("\n1. Handling missing titles...")
    missing_titles = df_clean['title'].isnull().sum()
    print(f"   Removing {missing_titles} rows with missing titles")
    df_clean = df_clean[df_clean['title'].notna()]
    
    # 2. Handle abstract column
    print("\n2. Handling abstract column...")
    df_clean['abstract'] = df_clean['abstract'].fillna('No abstract available')
    empty_abstracts = (df_clean['abstract'] == 'No abstract available').sum()
    print(f"   Empty abstracts: {empty_abstracts}")
    
    # 3. Convert publish_time to datetime - handle various formats
    print("\n3. Converting publish_time to datetime...")
    
    # First, check what the publish_time format looks like
    sample_times = df_clean['publish_time'].dropna().head(5)
    print(f"   Sample publish_time values: {list(sample_times)}")
    
    # Try to convert to datetime
    df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce', utc=True)
    
    # Check conversion results
    valid_dates = df_clean['publish_time'].notnull().sum()
    invalid_dates = df_clean['publish_time'].isnull().sum()
    print(f"   Successfully converted: {valid_dates} dates")
    print(f"   Failed to convert: {invalid_dates} dates")
    
    # 4. Extract year and month from valid dates only
    df_clean['year'] = df_clean['publish_time'].dt.year
    df_clean['month'] = df_clean['publish_time'].dt.month
    
    # For invalid dates, we'll keep them as NaN for now
    print(f"   Years extracted: {df_clean['year'].notnull().sum()}")
    
    # 5. Handle journal column
    print("\n4. Handling journal column...")
    df_clean['journal'] = df_clean['journal'].fillna('Unknown Journal')
    unknown_journals = (df_clean['journal'] == 'Unknown Journal').sum()
    print(f"   Unknown journals: {unknown_journals}")
    
    # 6. Create new features
    print("\n5. Creating new features...")
    
    # Abstract word count
    df_clean['abstract_word_count'] = df_clean['abstract'].apply(
        lambda x: len(str(x).split()) if pd.notnull(x) and x != 'No abstract available' else 0
    )
    
    # Title word count
    df_clean['title_word_count'] = df_clean['title'].apply(
        lambda x: len(str(x).split()) if pd.notnull(x) else 0
    )
    
    # Has abstract flag
    df_clean['has_abstract'] = df_clean['abstract'] != 'No abstract available'
    
    # Paper ID (create if doesn't exist)
    if 'cord_uid' in df_clean.columns:
        df_clean['paper_id'] = df_clean['cord_uid']
    else:
        df_clean['paper_id'] = range(len(df_clean))
    
    # 7. Remove duplicates based on title
    print("\n6. Removing duplicate titles...")
    initial_count = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=['title'])
    duplicates_removed = initial_count - len(df_clean)
    print(f"   Removed {duplicates_removed} duplicate titles")
    
    # Final report
    final_size = len(df_clean)
    retention_rate = (final_size / original_size) * 100
    
    print(f"\nCLEANING SUMMARY:")
    print(f"   Original size: {original_size:,} rows")
    print(f"   Final size: {final_size:,} rows")
    print(f"   Retention rate: {retention_rate:.1f}%")
    print(f"   Columns in cleaned data: {len(df_clean.columns)}")
    
    return df_clean

def analyze_cleaned_data(df_clean):
    print("\nANALYZING CLEANED DATA")
    print("=" * 30)
    
    # Year distribution
    valid_years = df_clean['year'].notnull()
    if valid_years.any():
        year_counts = df_clean[valid_years]['year'].value_counts().sort_index()
        print("\nPUBLICATION YEARS:")
        for year, count in year_counts.head(10).items():  # Show top 10 years
            if pd.notnull(year):
                print(f"   {int(year)}: {count:,} papers")
    else:
        print("No valid years found")
    
    # Journal statistics
    top_journals = df_clean['journal'].value_counts().head(10)
    print(f"\nTOP 10 JOURNALS:")
    for journal, count in top_journals.items():
        print(f"   {journal}: {count:,} papers")
    
    # Abstract statistics
    avg_words = df_clean['abstract_word_count'].mean()
    has_abstract_count = df_clean['has_abstract'].sum()
    print(f"\nABSTRACT STATISTICS:")
    print(f"   Average abstract length: {avg_words:.1f} words")
    print(f"   Papers with abstracts: {has_abstract_count:,}")
    print(f"   Papers without abstracts: {len(df_clean) - has_abstract_count:,}")
    
    return {
        'year_counts': year_counts if valid_years.any() else pd.Series(),
        'top_journals': top_journals,
        'avg_abstract_length': avg_words
    }

if __name__ == "__main__":
    try:
        # Load data with specific settings for mixed types
        print("Loading metadata.csv...")
        df = pd.read_csv('metadata.csv', low_memory=False)
        print(f"Loaded {len(df):,} rows")
        
        # Clean data
        df_clean = clean_data(df)
        
        # Analyze cleaned data
        stats = analyze_cleaned_data(df_clean)
        
        # Save cleaned data
        output_file = 'cleaned_metadata.csv'
        df_clean.to_csv(output_file, index=False)
        print(f"\nCLEANED DATA saved to '{output_file}'")
        
        # Save cleaning report
        with open('cleaning_report.txt', 'w', encoding='utf-8') as f:
            f.write("CORD-19 Data Cleaning Report\n")
            f.write("=" * 40 + "\n")
            f.write(f"Final dataset size: {len(df_clean):,} rows\n")
            f.write(f"Columns: {len(df_clean.columns)}\n")
            f.write(f"Average abstract length: {stats['avg_abstract_length']:.1f} words\n")
            f.write(f"Papers with abstracts: {df_clean['has_abstract'].sum():,}\n")
            
        print("CLEANING REPORT saved to 'cleaning_report.txt'")
        
    except Exception as e:
        print(f"ERROR during cleaning: {e}")
        import traceback
        traceback.print_exc()