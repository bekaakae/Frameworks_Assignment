# 3_analysis_fixed.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

def create_all_visualizations(df):
    """Create all required visualizations for the assignment"""
    print("CREATING ALL VISUALIZATIONS...")
    
    # Create figures directory
    if not os.path.exists('figures'):
        os.makedirs('figures')
    
    # 1. Publications over time
    print("1. Creating publications over time plot...")
    plt.figure(figsize=(12, 6))
    yearly_counts = df['year'].value_counts().sort_index()
    plt.bar(yearly_counts.index, yearly_counts.values, color='skyblue', edgecolor='navy', alpha=0.8)
    plt.title('Number of COVID-19 Publications by Year', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figures/publications_by_year.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Top journals
    print("2. Creating top journals plot...")
    plt.figure(figsize=(12, 8))
    top_journals = df['journal'].value_counts().head(15)
    colors = plt.cm.Set3(np.linspace(0, 1, len(top_journals)))
    top_journals.sort_values().plot(kind='barh', color=colors)
    plt.title('Top 15 Journals Publishing COVID-19 Research', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Publications')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/top_journals.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. Word frequency analysis
    print("3. Creating word frequency plot...")
    all_titles = ' '.join(df['title'].dropna().astype(str))
    words = re.findall(r'\b[a-zA-Z]{4,}\b', all_titles.lower())
    
    stop_words = {
        'this', 'that', 'with', 'from', 'have', 'were', 'been', 'their', 
        'which', 'study', 'using', 'based', 'during', 'among', 'between',
        'analysis', 'research', 'paper', 'article', 'journal', 'results'
    }
    
    filtered_words = [word for word in words if word not in stop_words]
    word_freq = Counter(filtered_words)
    common_words = word_freq.most_common(20)
    
    words, counts = zip(*common_words)
    
    plt.figure(figsize=(12, 8))
    plt.barh(words, counts, color='lightgreen')
    plt.title('Most Frequent Words in Paper Titles', fontsize=14, fontweight='bold')
    plt.xlabel('Frequency')
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/common_words.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 4. Word cloud
    print("4. Creating word cloud...")
    plt.figure(figsize=(12, 6))
    wordcloud = WordCloud(width=800, height=400, background_color='white', 
                         max_words=100, colormap='viridis').generate(all_titles)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Paper Titles', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('figures/wordcloud.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 5. Abstract length distribution
    print("5. Creating abstract length distribution...")
    plt.figure(figsize=(12, 6))
    # Remove outliers for better visualization
    abstract_lengths = df[df['abstract_word_count'] <= 1000]['abstract_word_count']
    plt.hist(abstract_lengths, bins=50, color='orange', edgecolor='black', alpha=0.7)
    plt.title('Distribution of Abstract Word Count', fontsize=14, fontweight='bold')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.axvline(abstract_lengths.mean(), color='red', linestyle='--', 
                label=f'Mean: {abstract_lengths.mean():.1f} words')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/abstract_length.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
    return {
        'yearly_counts': yearly_counts,
        'top_journals': top_journals,
        'common_words': common_words,
        'avg_abstract_length': abstract_lengths.mean()
    }

def main():
    # Load cleaned data
    try:
        df = pd.read_csv('cleaned_metadata.csv')
        print(f"Loaded {len(df)} rows for analysis")
    except FileNotFoundError:
        print("ERROR: cleaned_metadata.csv not found! Run cleaning script first.")
        return
    
    # Create all visualizations
    stats = create_all_visualizations(df)
    
    # Generate report
    with open('analysis_report.txt', 'w') as f:
        f.write("CORD-19 ANALYSIS REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total papers analyzed: {len(df)}\n")
        f.write(f"Publication range: {int(df['year'].min())}-{int(df['year'].max())}\n")
        f.write(f"Peak publication year: {stats['yearly_counts'].idxmax()} "
                f"({stats['yearly_counts'].max()} papers)\n")
        f.write(f"Top journal: {stats['top_journals'].index[0]} "
                f"({stats['top_journals'].iloc[0]} papers)\n")
        f.write(f"Most common word: '{stats['common_words'][0][0]}' "
                f"({stats['common_words'][0][1]} appearances)\n")
        f.write(f"Average abstract length: {stats['avg_abstract_length']:.1f} words\n")
    
    print("✅ ANALYSIS COMPLETE! Check the 'figures' folder for all visualizations.")

if __name__ == "__main__":
    main()