# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2e86ab;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2e86ab;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load the cleaned dataset"""
    try:
        df = pd.read_csv('cleaned_metadata.csv')
        return df
    except FileNotFoundError:
        # If cleaned data doesn't exist, create a sample
        st.warning("Creating sample data for demonstration...")
        return create_sample_data()

def create_sample_data():
    """Create sample data if cleaned_metadata.csv doesn't exist"""
    sample_data = {
        'title': [
            'Clinical characteristics of COVID-19 patients',
            'A novel coronavirus from patients with pneumonia',
            'First case of 2019 novel coronavirus in the United States',
            'The epidemiology and pathogenesis of coronavirus',
            'Remdesivir for the treatment of COVID-19',
            'Effectiveness of masks in preventing COVID-19',
            'Vaccine development for SARS-CoV-2',
            'Mental health during the COVID-19 pandemic',
            'Economic impact of COVID-19 lockdowns',
            'Treatment strategies for severe COVID-19 cases'
        ],
        'abstract': [
            'This study examines the clinical features of hospitalized COVID-19 patients...',
            'In December 2019, a cluster of patients with pneumonia was identified...',
            'The first case of 2019 novel coronavirus was identified in the US...',
            'Coronaviruses are enveloped RNA viruses that cause respiratory illnesses...',
            'Remdesivir showed clinical improvement in patients with severe COVID-19...',
            'Face masks are effective in reducing transmission of COVID-19...',
            'Multiple vaccine candidates are in development for SARS-CoV-2...',
            'The pandemic has significant effects on global mental health...',
            'Economic consequences of lockdown measures are substantial...',
            'Various treatment approaches for severe COVID-19 are being investigated...'
        ],
        'publish_time': [
            '2020-03-15', '2020-01-24', '2020-01-31', '2020-02-10',
            '2020-04-10', '2020-03-20', '2020-05-15', '2020-04-05',
            '2020-06-01', '2020-03-25'
        ],
        'journal': [
            'JAMA', 'New England Journal of Medicine', 'The Lancet', 'Nature',
            'Science', 'BMJ', 'Nature Medicine', 'JAMA Psychiatry',
            'The Economist', 'Intensive Care Medicine'
        ],
        'authors': [
            'Wang D, Hu B, Hu C', 'Zhu N, Zhang D, Wang W', 
            'Holshue ML, DeBolt C', 'Cui J, Li F', 'Beigel JH, Tomashek KM',
            'Chu DK, Akl EA', 'Lurie N, Saville M', 'Pfefferbaum B, North CS',
            'Baldwin R, Weder di Mauro B', 'Wu Z, McGoogan JM'
        ]
    }
    
    df = pd.DataFrame(sample_data)
    df['publish_time'] = pd.to_datetime(df['publish_time'])
    df['year'] = df['publish_time'].dt.year
    df['abstract_word_count'] = df['abstract'].str.split().str.len()
    df['title_word_count'] = df['title'].str.split().str.len()
    
    return df

def create_visualizations(df, year_range, selected_journals):
    """Create all required visualizations"""
    
    # Filter data based on selections
    filtered_df = df.copy()
    
    if year_range:
        filtered_df = filtered_df[
            (filtered_df['year'] >= year_range[0]) & 
            (filtered_df['year'] <= year_range[1])
        ]
    
    if selected_journals:
        filtered_df = filtered_df[filtered_df['journal'].isin(selected_journals)]
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Publications by Year
    if 'year' in filtered_df.columns and not filtered_df.empty:
        yearly_counts = filtered_df['year'].value_counts().sort_index()
        axes[0, 0].bar(yearly_counts.index, yearly_counts.values, color='skyblue', alpha=0.8)
        axes[0, 0].set_title('Publications by Year', fontweight='bold', fontsize=14)
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Number of Papers')
        axes[0, 0].grid(axis='y', alpha=0.3)
    else:
        axes[0, 0].text(0.5, 0.5, 'No year data available', 
                       ha='center', va='center', transform=axes[0, 0].transAxes)
        axes[0, 0].set_title('Publications by Year', fontweight='bold')
    
    # 2. Top Journals
    if 'journal' in filtered_df.columns and not filtered_df.empty:
        top_journals = filtered_df['journal'].value_counts().head(10)
        colors = plt.cm.Set3(np.linspace(0, 1, len(top_journals)))
        top_journals.plot(kind='bar', ax=axes[0, 1], color=colors, alpha=0.8)
        axes[0, 1].set_title('Top Publishing Journals', fontweight='bold', fontsize=14)
        axes[0, 1].set_xlabel('Journal')
        axes[0, 1].set_ylabel('Number of Papers')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(axis='y', alpha=0.3)
    else:
        axes[0, 1].text(0.5, 0.5, 'No journal data available', 
                       ha='center', va='center', transform=axes[0, 1].transAxes)
        axes[0, 1].set_title('Top Publishing Journals', fontweight='bold')
    
    # 3. Word Frequency in Titles
    if 'title' in filtered_df.columns and not filtered_df.empty:
        all_titles = ' '.join(filtered_df['title'].dropna().astype(str))
        words = re.findall(r'\b[a-zA-Z]{4,}\b', all_titles.lower())
        
        # Custom stop words
        stop_words = {
            'this', 'that', 'with', 'from', 'have', 'were', 'been', 'their',
            'which', 'study', 'using', 'based', 'during', 'among', 'between'
        }
        
        filtered_words = [word for word in words if word not in stop_words]
        
        if filtered_words:
            word_freq = Counter(filtered_words)
            common_words = word_freq.most_common(10)
            words, counts = zip(*common_words)
            
            axes[1, 0].barh(words, counts, color='lightgreen', alpha=0.8)
            axes[1, 0].set_title('Most Frequent Words in Titles', fontweight='bold', fontsize=14)
            axes[1, 0].set_xlabel('Frequency')
            axes[1, 0].invert_yaxis()
            axes[1, 0].grid(axis='x', alpha=0.3)
        else:
            axes[1, 0].text(0.5, 0.5, 'No title data for analysis', 
                           ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('Most Frequent Words in Titles', fontweight='bold')
    else:
        axes[1, 0].text(0.5, 0.5, 'No title data available', 
                       ha='center', va='center', transform=axes[1, 0].transAxes)
        axes[1, 0].set_title('Most Frequent Words in Titles', fontweight='bold')
    
    # 4. Abstract Length Distribution
    if 'abstract_word_count' in filtered_df.columns and not filtered_df.empty:
        abstract_lengths = filtered_df['abstract_word_count']
        axes[1, 1].hist(abstract_lengths, bins=20, color='orange', alpha=0.7, edgecolor='black')
        axes[1, 1].set_title('Abstract Length Distribution', fontweight='bold', fontsize=14)
        axes[1, 1].set_xlabel('Word Count')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].axvline(abstract_lengths.mean(), color='red', linestyle='--', 
                          label=f'Mean: {abstract_lengths.mean():.1f} words')
        axes[1, 1].legend()
        axes[1, 1].grid(alpha=0.3)
    else:
        axes[1, 1].text(0.5, 0.5, 'No abstract length data available', 
                       ha='center', va='center', transform=axes[1, 1].transAxes)
        axes[1, 1].set_title('Abstract Length Distribution', fontweight='bold')
    
    plt.tight_layout()
    return fig, filtered_df

def main():
    # Header
    st.markdown('<h1 class="main-header">🔬 CORD-19 COVID-19 Research Explorer</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Welcome to the CORD-19 Research Explorer! This interactive dashboard allows you to explore 
    COVID-19 research papers and discover publication trends, key journals, and research focus areas.
    
    **Use the filters in the sidebar to customize your analysis.**
    """)
    
    # Load data
    df = load_data()
    
    # Sidebar - Filters and Controls
    st.sidebar.markdown('<div class="section-header">🔍 Filters & Controls</div>', 
                       unsafe_allow_html=True)
    
    # Year range filter
    if 'year' in df.columns:
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())
        year_range = st.sidebar.slider(
            "Select Publication Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
    else:
        year_range = (2020, 2022)
        st.sidebar.warning("Using default year range")
    
    # Journal filter
    if 'journal' in df.columns:
        available_journals = sorted(df['journal'].unique())
        selected_journals = st.sidebar.multiselect(
            "Select Journals to Include",
            options=available_journals,
            default=available_journals[:3] if len(available_journals) > 3 else available_journals
        )
    else:
        selected_journals = []
        st.sidebar.info("No journal data available")
    
    # Abstract length filter
    if 'abstract_word_count' in df.columns:
        min_abstract, max_abstract = st.sidebar.slider(
            "Abstract Word Count Range",
            min_value=0,
            max_value=int(df['abstract_word_count'].max()) if not df.empty else 500,
            value=(0, 300)
        )
    else:
        min_abstract, max_abstract = (0, 300)
    
    # Apply abstract length filter
    filtered_df_abstract = df.copy()
    if 'abstract_word_count' in df.columns:
        filtered_df_abstract = filtered_df_abstract[
            (filtered_df_abstract['abstract_word_count'] >= min_abstract) &
            (filtered_df_abstract['abstract_word_count'] <= max_abstract)
        ]
    
    # Sidebar metrics
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Dataset Overview")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Total Papers", len(df))
    with col2:
        st.metric("Filtered Papers", len(filtered_df_abstract))
    
    if 'year' in df.columns:
        st.sidebar.metric("Date Range", f"{int(df['year'].min())}-{int(df['year'].max())}")
    
    # Main content area
    if df.empty:
        st.error("No data available for analysis.")
        return
    
    # Key Metrics
    st.markdown('<div class="section-header">📈 Key Metrics</div>', unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        total_papers = len(filtered_df_abstract)
        st.metric("Total Research Papers", f"{total_papers:,}")
    
    with metric_col2:
        if 'journal' in filtered_df_abstract.columns:
            unique_journals = filtered_df_abstract['journal'].nunique()
            st.metric("Unique Journals", unique_journals)
        else:
            st.metric("Unique Journals", "N/A")
    
    with metric_col3:
        if 'abstract_word_count' in filtered_df_abstract.columns:
            avg_abstract = filtered_df_abstract['abstract_word_count'].mean()
            st.metric("Avg Abstract Length", f"{avg_abstract:.1f} words")
        else:
            st.metric("Avg Abstract Length", "N/A")
    
    with metric_col4:
        if 'year' in filtered_df_abstract.columns:
            years_covered = filtered_df_abstract['year'].nunique()
            st.metric("Years Covered", years_covered)
        else:
            st.metric("Years Covered", "N/A")
    
    # Visualizations
    st.markdown('<div class="section-header">📊 Research Visualizations</div>', 
                unsafe_allow_html=True)
    
    # Create and display visualizations
    fig, final_filtered_df = create_visualizations(filtered_df_abstract, year_range, selected_journals)
    st.pyplot(fig)
    
    # Data Sample Section
    st.markdown('<div class="section-header">📋 Research Papers Sample</div>', 
                unsafe_allow_html=True)
    
    # Select columns to display
    display_columns = []
    for col in ['title', 'journal', 'year', 'authors']:
        if col in final_filtered_df.columns:
            display_columns.append(col)
    
    if display_columns and not final_filtered_df.empty:
        st.dataframe(
            final_filtered_df[display_columns].head(10),
            use_container_width=True,
            height=400
        )
        
        # Show sample count
        st.info(f"Showing {min(10, len(final_filtered_df))} of {len(final_filtered_df)} papers")
    else:
        st.warning("No data available to display with current filters")
    
    # Download Section
    st.markdown('<div class="section-header">📥 Export Data</div>', 
                unsafe_allow_html=True)
    
    if not final_filtered_df.empty:
        csv_data = final_filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="cord19_filtered_data.csv",
            mime="text/csv",
            help="Download the currently filtered dataset"
        )
    else:
        st.info("No data available for download with current filters")
    
    # Insights Section
    st.markdown('<div class="section-header">💡 Key Insights</div>', 
                unsafe_allow_html=True)
    
    if not final_filtered_df.empty:
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.subheader("Publication Trends")
            if 'year' in final_filtered_df.columns:
                yearly_stats = final_filtered_df['year'].value_counts()
                if not yearly_stats.empty:
                    peak_year = yearly_stats.idxmax()
                    peak_count = yearly_stats.max()
                    st.write(f"• **Peak publication year**: {int(peak_year)} ({peak_count} papers)")
            
            if 'journal' in final_filtered_df.columns:
                journal_stats = final_filtered_df['journal'].value_counts()
                if not journal_stats.empty:
                    top_journal = journal_stats.index[0]
                    top_count = journal_stats.iloc[0]
                    st.write(f"• **Top journal**: {top_journal} ({top_count} papers)")
        
        with insights_col2:
            st.subheader("Content Analysis")
            if 'abstract_word_count' in final_filtered_df.columns:
                avg_words = final_filtered_df['abstract_word_count'].mean()
                st.write(f"• **Average abstract length**: {avg_words:.1f} words")
            
            if 'title' in final_filtered_df.columns:
                all_titles = ' '.join(final_filtered_df['title'].dropna().astype(str))
                words = re.findall(r'\b[a-zA-Z]{4,}\b', all_titles.lower())
                if words:
                    common_word = Counter(words).most_common(1)[0]
                    st.write(f"• **Most common word**: '{common_word[0]}' ({common_word[1]} times)")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**CORD-19 Data Explorer** | Built with Streamlit | "
        "Data Source: [CORD-19 Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)"
    )

if __name__ == "__main__":
    main()