# ultra_fast_simple.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

def main():
    print("ULTRA-FAST CORD-19 ANALYSIS")
    print("=" * 40)
    start_time = time.time()
    
    # Step 1: Load minimal data
    print("1. Loading data...")
    try:
        df = pd.read_csv('metadata.csv', 
                        nrows=2000,  # Small sample
                        usecols=['title', 'abstract', 'publish_time', 'journal'],
                        low_memory=False)
        print(f"   Loaded {len(df)} rows")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Step 2: Quick cleaning
    print("2. Quick cleaning...")
    df_clean = df[df['title'].notna()].copy()
    df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')
    df_clean['year'] = df_clean['publish_time'].dt.year
    df_clean['abstract'] = df_clean['abstract'].fillna('')
    df_clean['journal'] = df_clean['journal'].fillna('Unknown')
    df_clean['abstract_length'] = df_clean['abstract'].str.split().str.len()
    
    print(f"   Cleaned {len(df_clean)} rows")
    
    # Step 3: Fast analysis
    print("3. Fast analysis...")
    year_counts = df_clean['year'].value_counts().sort_index()
    journal_counts = df_clean['journal'].value_counts().head(6)
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Publications by year
    ax1.bar(year_counts.index, year_counts.values, color='lightblue', alpha=0.8)
    ax1.set_title('Publications by Year', fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Papers')
    ax1.grid(axis='y', alpha=0.3)
    
    # Plot 2: Top journals
    ax2.barh(list(journal_counts.index), journal_counts.values, color='lightcoral', alpha=0.8)
    ax2.set_title('Top Journals', fontweight='bold')
    ax2.set_xlabel('Number of Papers')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fast_analysis_results.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Step 4: Results
    total_time = time.time() - start_time
    print("\n" + "=" * 40)
    print("ANALYSIS COMPLETE!")
    print(f"Time: {total_time:.1f} seconds")
    print(f"Publications by year: {dict(year_counts)}")
    print(f"Top 3 journals: {dict(journal_counts.head(3))}")
    print(f"Average abstract length: {df_clean['abstract_length'].mean():.1f} words")
    print(f"Results saved to: fast_analysis_results.png")
    
    # Save cleaned data for future use
    df_clean.to_csv('cleaned_data_fast.csv', index=False)
    print(f"Cleaned data saved to: cleaned_data_fast.csv")

if __name__ == "__main__":
    main()