import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io  # Added for the Dataset Info buffer
from pathlib import Path
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
    # Look for the data file in your actual folder structure
    cwd = Path(__file__).parent
    possible_paths = [
        cwd / 'Data' / 'Cleaned' / 'cleaned_student_data.csv',
        cwd / 'Data' / 'cleaned_student_data.csv',
        cwd / 'cleaned_student_data.csv',
        cwd / 'Data' / 'Raw' / 'StudentPerformanceFactors.csv'
    ]
    for p in possible_paths:
        if p.exists():
            try:
                df = pd.read_csv(p)
                return df
            except Exception as e:
                st.error(f"Failed to read {p}: {e}")
                return None
    return None


# Load the data
df = load_data()

if df is not None:
    # Data preprocessing
    df_clean = df.copy()

    # Normalize column names: strip and replace spaces with underscores
    # for consistency
    df_clean.columns = [c.strip().replace(' ', '_') for c in df_clean.columns]

    # Convert categorical columns
    categorical_columns = [
        'Gender', 'Parental_Involvement', 'Access_to_Resources',
        'Extracurricular_Activities', 'Motivation_Level',
        'Internet_Access', 'Family_Income', 'Teacher_Quality',
        'School_Type', 'Peer_Influence', 'Learning_Disabilities',
        'Parental_Education_Level', 'Distance_from_Home'
    ]
for col in categorical_columns:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].astype('category')

# Create Study_Sleep_Group
    if ('Hours_Studied' in df_clean.columns and
            'Sleep_Hours' in df_clean.columns):
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

    df_clean['Study_Sleep_Group'] = df_clean.apply(
        create_study_sleep_group, axis=1)

# --- Initialize Sidebar Filters ---
st.sidebar.header("Filter Data Here")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
        "Go to",
        [
            "📋 Overview",
            "🔑 Key Findings",
            "📈 Visualizations",
            "📊 Data Explorer",
            "📝 About"
        ]
    )

if page == "📋 Overview":
    st.header("Project Overview")
    st.write("""
    This data analytics project investigates the factors that
    influence student academic performance, specifically examining
    which variables most strongly predict exam scores.
    """)

    # Dataset metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", len(df_clean))
    with col2:
        st.metric("Features", len(df_clean.columns))
    with col3:
        if 'Exam_Score' in df_clean.columns:
            avg_score = df_clean['Exam_Score'].mean()
            if pd.isna(avg_score):
                st.metric("Avg Exam Score", "N/A")
            else:
                st.metric("Avg Exam Score", f"{avg_score:.2f}")

    # Data sample
    st.subheader("Data Sample")
    st.dataframe(df_clean.head(10))

    # FIXED DATA INFO SECTION
    st.subheader("Dataset Info")
    buffer = io.StringIO()
    df_clean.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    # Business Requirements & Hypotheses
    st.subheader("🎯 Business Requirements")
    st.markdown(
        "- **BR1**: Identify key performance drivers\n"
        "- **BR2**: Quantify optimal study-sleep balance"
    )

    st.subheader("🔬 Research Hypotheses")
    st.markdown(
        "- **H1**: Hours studied explains more variance than "
        "attendance or sleep\n"
        "- **H3**: High study AND high sleep score higher"
    )

elif page == "🔑 Key Findings":
    st.header("🔑 Key Findings")

    with st.expander(
        "Finding 1: Study Hours Dominate Predictors",
        expanded=True
    ):
        st.write(
            "**What We Found**: Hours studied explained "
            "**19.8%** of the variance."
        )
        fig, ax = plt.subplots(figsize=(8, 4))
        # Display-friendly predictor names
        # (these may differ from column names)
        predictors = ['Hours Studied', 'Attendance', 'Sleep Hours']
        r2_values = [0.198, 0.00, 0.00]
        colors = ['#2E86AB', '#A23B72', '#A23B72']
        ax.bar(predictors, r2_values, color=colors)
        st.pyplot(fig)

elif page == "📈 Visualizations":
    st.header("📈 Visualizations")
    tab1, tab2 = st.tabs(["Correlation Matrix", "Group Comparison"])

    with tab1:
        numerical_df = df_clean.select_dtypes(include=[np.number])
        if len(numerical_df.columns) > 1:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(
                numerical_df.corr(),
                annot=True,
                cmap='coolwarm',
                ax=ax
            )
            st.pyplot(fig)

    with tab2:
        if 'Study_Sleep_Group' in df_clean.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(
                data=df_clean,
                x='Study_Sleep_Group',
                y='Exam_Score',
                ax=ax
            )
            st.pyplot(fig)

elif page == "📊 Data Explorer":
    st.header("📊 Explore the Data")

    # Simple Filter
    if 'Gender' in df_clean.columns:
        gender_options = df_clean['Gender'].unique()
        gender_filter = st.multiselect(
            "Filter by Gender",
            options=gender_options,
            default=gender_options
        )
        df_filtered = df_clean[df_clean['Gender'].isin(gender_filter)]
        st.dataframe(df_filtered)

    # BONUS: Score Predictor (Based on your Correlation of 0.45)
    # Streamlit divider may not exist in older versions
    if hasattr(st, 'divider'):
        st.divider()
    else:
        st.markdown('---')
    st.subheader("🔮 Simple Score Predictor")
    st.write("Based on the data, how might your hours affect your score?")
    user_hours = st.number_input(
        "Enter Study Hours Per Week",
        min_value=0,
        max_value=100,
        value=20
    )
    # Simplified linear approximation based on your findings
    base_score = 55
    predicted = base_score + (user_hours * 0.5)
    st.success(f"Estimated Predicted Score: {min(predicted, 100.0):.1f}")

elif page == "📝 About":
    st.header("📝 About This Project")
    st.write("Author: Sadiyah")
    st.write("Dataset: Student Performance Factors (Kaggle)")
else:
    st.error("Data file not found! Check your file paths in the repository.")
    data_dir = Path(__file__).parent / 'Data'
    if data_dir.exists():
        st.write("Files in Data folder:", os.listdir(data_dir))
    else:
        st.write("Current Directory Files:", os.listdir('.'))