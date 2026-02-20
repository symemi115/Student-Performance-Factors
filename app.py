import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway
import os

# Page configuration
st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Student Performance Analysis")
st.markdown("### What Really Affects Exam Scores?")

# Load data function
@st.cache_data
def load_data():
    # Look for the data file in different possible locations
    possible_paths = [
        'Data/cleaned_student_data.csv',
        'Data/Cleaned/cleaned_student_data.csv',
        'Data/Raw/StudentPerformanceFactors.csv',
        'cleaned_student_data.csv',
        'StudentPerformanceFactors.csv'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            return df
    
    return None

# Load the data
df = load_data()

if df is not None:
    # Data preprocessing (from your notebook)
    df_clean = df.copy()
    
    # Convert categorical columns (from Step 2.4 in your notebook)
    categorical_columns = ['Gender', 'Parental_Involvement', 'Access_to_Resources', 
                           'Extracurricular_Activities', 'Motivation_Level',
                           'Internet_Access', 'Family_Income', 'Teacher_Quality',
                           'School_Type', 'Peer_Influence', 'Learning_Disabilities',
                           'Parental_Education_Level', 'Distance_from_Home']
    
    for col in categorical_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype('category')
    
    # Create Study_Sleep_Group (from Step 2.5 in your notebook)
    if 'Hours_Studied' in df_clean.columns and 'Sleep_Hours' in df_clean.columns:
        study_threshold = df_clean['Hours_Studied'].median()
        sleep_threshold = df_clean['Sleep_Hours'].median()
        
        def create_study_sleep_group(row):
            high_study = row['Hours_Studied'] > study_threshold
            high_sleep = row['Sleep_Hours'] > sleep_threshold
            
            if high_study and high_sleep:
                return 'High Both'
            elif high_study and not high_sleep:
                return 'High Study Only'
            elif not high_study and high_sleep:
                return 'High Sleep Only'
            else:
                return 'Low Both'
        
        df_clean['Study_Sleep_Group'] = df_clean.apply(create_study_sleep_group, axis=1)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to", 
        ["📋 Overview", "🔑 Key Findings", "📈 Visualizations", "📊 Data Explorer", "📝 About"]
    )
    
    if page == "📋 Overview":
        st.header("Project Overview")
        st.write("""
        This data analytics project investigates the factors that influence student academic performance,
        specifically examining which variables most strongly predict exam scores.
        """)
        
        # Dataset info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Students", len(df_clean))
        with col2:
            st.metric("Features", len(df_clean.columns))
        with col3:
            if 'Exam_Score' in df_clean.columns:
                st.metric("Avg Exam Score", f"{df_clean['Exam_Score'].mean():.2f}")
        
        # Data sample
        st.subheader("Data Sample")
        st.dataframe(df_clean.head(10))
        
        # Data info
        st.subheader("Dataset Info")
        buffer = []
        df_clean.info(buf=buffer)
        st.text('\n'.join(buffer))
        
        # Business Requirements
        st.subheader("🎯 Business Requirements")
        st.markdown("""
        - **BR1**: Identify key performance drivers
        - **BR2**: Quantify optimal study-sleep balance  
        - **BR3**: Develop predictive understanding
        - **BR4**: Generate actionable student profiles
        - **BR5**: Inform educational policy recommendations
        """)
        
        # Hypotheses
        st.subheader("🔬 Research Hypotheses")
        st.markdown("""
        - **H1**: Hours studied explains more variance than attendance or sleep
        - **H2**: Study hours + attendance together predict better than either alone
        - **H3**: Students with high study AND high sleep score significantly higher
        - **H4**: Hours studied has strongest correlation with exam scores
        """)
    
    elif page == "🔑 Key Findings":
        st.header("🔑 Key Findings")
        
        # Finding 1
        with st.expander("Finding 1: Study Hours Dominate Individual Predictors", expanded=True):
            st.write("""
            **What We Found**: Hours studied explained **19.8%** (R² = 0.198) of the variance in exam scores, 
            making it the only meaningful individual predictor. In contrast, attendance and sleep hours 
            alone showed virtually no predictive power.
            
            **Why It Matters**: When students ask "What's the most important thing I can do to improve my grades?" 
            — the data clearly points to **study time**.
            """)
            
            # Simple visualization
            fig, ax = plt.subplots(figsize=(8, 4))
            predictors = ['Hours Studied', 'Attendance', 'Sleep Hours']
            r2_values = [0.198, 0.00, 0.00]
            colors = ['#2E86AB', '#A23B72', '#A23B72']
            bars = ax.bar(predictors, r2_values, color=colors)
            ax.set_ylabel('R² Value')
            ax.set_title('Predictive Power of Individual Factors')
            ax.set_ylim(0, 0.25)
            for bar, val in zip(bars, r2_values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{val:.3f}', ha='center', va='bottom')
            st.pyplot(fig)
        
        # Finding 2
        with st.expander("Finding 2: Attendance Modifies Study Impact", expanded=True):
            st.write("""
            **What We Found**: While attendance alone doesn't predict scores, it plays a crucial **moderating role**. 
            The relationship between study hours and exam scores changes depending on attendance levels.
            
            **Why It Matters**: **Showing up to class amplifies the effectiveness of studying**. This means attendance 
            policies aren't just about being present—they directly impact how well study time translates to results.
            """)
        
        # Finding 3
        with st.expander("Finding 3: The 'Sweet Spot' for Student Success", expanded=True):
            st.write("**What We Found**: Students were grouped into four categories:")
            
            # Group data from your notebook
            group_data = pd.DataFrame({
                'Group': ['High Both', 'High Study Only', 'High Sleep Only', 'Low Both'],
                'Count': [1116, 1838, 1294, 2130],
                'Average Score': [68.74, 68.76, 65.88, 65.75],
                'vs Low Both': ['+2.73', '+2.75', '+0.13', '—']
            })
            st.dataframe(group_data)
            
            st.write("""
            **Statistical Significance**: 
            - ANOVA F-statistic = **308.39**, p < 0.001
            - Tukey HSD confirms High Study Only and High Both groups score significantly higher
            
            **Why It Matters**: **Study time drives success, not sleep alone**. Students who study a lot score ~3 points 
            higher regardless of whether they sleep a lot. However, the **High Both group is the largest**, suggesting 
            successful students tend to maintain both habits.
            """)
        
        # Finding 4
        with st.expander("Finding 4: What Predicts Success Most? (Ranked)", expanded=True):
            st.write("**What We Found**: When comparing all factors, here's how they rank:")
            
            rank_data = pd.DataFrame({
                'Rank': ['🥇', '🥈', '🥉', '4', '5', '6'],
                'Factor': ['Attendance', 'Hours Studied', 'Previous Scores', 
                          'Tutoring Sessions', 'Physical Activity', 'Sleep Hours'],
                'Correlation (r)': [0.58, 0.45, 0.16, 0.03, 0.02, -0.02],
                'Strength': ['Strong', 'Moderate', 'Weak', 'Very Weak', 'Very Weak', 'None']
            })
            st.dataframe(rank_data)
            
            st.write("""
            **Why It Matters**: This reveals something fascinating! While Hours Studied was the best individual predictor, 
            **Attendance actually has a stronger correlation** with exam scores (0.58 vs 0.45). This tells us that attendance 
            and study hours work together—students who attend class regularly also tend to study more.
            """)
    
    elif page == "📈 Visualizations":
        st.header("📈 Visualizations")
        
        tab1, tab2, tab3 = st.tabs(["Correlation Matrix", "Group Comparison", "Predictor Ranking"])
        
        with tab1:
            st.subheader("Correlation Matrix")
            # Select numerical columns only (like in your fixed code)
            numerical_df = df_clean.select_dtypes(include=[np.number])
            
            if len(numerical_df.columns) > 1:
                fig, ax = plt.subplots(figsize=(12, 8))
                corr_matrix = numerical_df.corr()
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', 
                           center=0, square=True, fmt='.2f', ax=ax)
                ax.set_title('Correlation Matrix of All Numerical Variables')
                st.pyplot(fig)
                
                # Show correlation with exam score
                if 'Exam_Score' in numerical_df.columns:
                    st.subheader("Correlations with Exam Score")
                    exam_corr = corr_matrix['Exam_Score'].drop('Exam_Score').sort_values(ascending=False)
                    st.dataframe(exam_corr)
            else:
                st.warning("Not enough numerical columns for correlation matrix.")
        
        with tab2:
            st.subheader("Exam Scores by Study-Sleep Group")
            if 'Study_Sleep_Group' in df_clean.columns and 'Exam_Score' in df_clean.columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.boxplot(data=df_clean, x='Study_Sleep_Group', y='Exam_Score', ax=ax)
                plt.xticks(rotation=45)
                ax.set_title('Exam Scores Across Different Study-Sleep Groups')
                st.pyplot(fig)
                
                # Show statistics
                st.subheader("Group Statistics")
                stats_df = df_clean.groupby('Study_Sleep_Group')['Exam_Score'].agg(['count', 'mean', 'std']).round(2)
                st.dataframe(stats_df)
            else:
                st.warning("Study_Sleep_Group or Exam_Score column not found.")
        
        with tab3:
            st.subheader("Predictor Ranking")
            
            # Data from your findings
            predictors = ['Attendance', 'Hours Studied', 'Previous Scores', 
                         'Tutoring Sessions', 'Physical Activity', 'Sleep Hours']
            correlations = [0.58, 0.45, 0.16, 0.03, 0.02, -0.02]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#2E86AB', '#2E86AB', '#A23B72', '#A23B72', '#A23B72', '#A23B72']
            bars = ax.bar(predictors, correlations, color=colors)
            
            # Add value labels
            for bar, val in zip(bars, correlations):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{val:.2f}', ha='center', va='bottom' if val > 0 else 'top')
            
            ax.set_title('Correlation of Variables with Exam Score', fontsize=14)
            ax.set_xlabel('Variables')
            ax.set_ylabel('Correlation Coefficient')
            ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            plt.xticks(rotation=45)
            ax.set_ylim(-0.1, 0.7)
            plt.tight_layout()
            st.pyplot(fig)
    
    elif page == "📊 Data Explorer":
        st.header("📊 Explore the Data")
        
        # Sidebar filters within the page
        st.sidebar.header("Filters")
        
        # Filter options
        filtered_df = df_clean.copy()
        
        # Numerical filters
        numerical_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
        for col in numerical_cols[:3]:  # Limit to first 3 numerical columns
            if col in filtered_df.columns:
                min_val = float(filtered_df[col].min())
                max_val = float(filtered_df[col].max())
                if min_val != max_val:
                    filter_range = st.sidebar.slider(
                        f"Filter {col}",
                        min_val, max_val,
                        (min_val, max_val)
                    )
                    filtered_df = filtered_df[
                        (filtered_df[col] >= filter_range[0]) & 
                        (filtered_df[col] <= filter_range[1])
                    ]
        
        # Categorical filters
        categorical_cols = filtered_df.select_dtypes(include=['category', 'object']).columns.tolist()
        for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
            if col in filtered_df.columns:
                unique_vals = filtered_df[col].unique().tolist()
                selected_vals = st.sidebar.multiselect(
                    f"Filter {col}",
                    unique_vals,
                    default=unique_vals
                )
                if selected_vals:
                    filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]
        
        st.subheader(f"Filtered Data ({len(filtered_df)} rows)")
        st.dataframe(filtered_df)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        st.dataframe(filtered_df.describe())
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )
    
    elif page == "📝 About":
        st.header("📝 About This Project")
        
        st.markdown("""
        ### Student Performance Analysis: What Really Affects Exam Scores?
        
        This data analytics project investigates the factors that influence student academic performance, 
        specifically examining which variables most strongly predict exam scores.
        
        **Dataset**: [Student Performance Factors](https://www.kaggle.com/datasets/lainguyn123/student-performance-factors) from Kaggle
        
        **Key Features**:
        - Hours Studied
        - Attendance Rate
        - Sleep Hours
        - Previous Scores
        - Extracurricular Activities
        - Exam Score (Target Variable)
        
        **Technologies Used**:
        - Python (Pandas, NumPy)
        - Matplotlib/Seaborn (Visualizations)
        - SciPy/StatsModels (Statistical Testing)
        - Scikit-learn (Regression)
        - Streamlit (Dashboard)
        
        **Author**: Sadiyah
        **GitHub**: [symemi115/Student-Performance-Factors](https://github.com/symemi115/Student-Performance-Factors)
        """)

else:
    st.error("""
    **Data file not found!**
    
    Please make sure your data file is in one of these locations:
    - `Data/cleaned_student_data.csv`
    - `Data/Raw/StudentPerformanceFactors.csv`
    - `cleaned_student_data.csv`
    
    Current directory: """ + os.getcwd()
    )
    
    # Show files in current directory for debugging
    st.write("Files in current directory:")
    files = os.listdir('.')
    st.write(files)