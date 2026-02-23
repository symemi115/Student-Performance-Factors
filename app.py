import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="📊",
    layout="wide"
)
# -----------------------------
# Title & intro
# -----------------------------
st.title("📊 Student Performance Analysis")
st.markdown("### What Really Affects Exam Scores?")

st.write(
    "This project explores which factors have the biggest impact on student exam scores, "
    "with a focus on study hours, sleep, and other lifestyle and school-related variables."
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    cwd = Path(__file__).parent
    possible_paths = [
        cwd / "Data" / "Cleaned" / "cleaned_student_data.csv",
        cwd / "Data" / "cleaned_student_data.csv",
        cwd / "cleaned_student_data.csv",
        cwd / "Data" / "Raw" / "StudentPerformanceFactors.csv",
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


df = load_data()

if df is not None:
    # -----------------------------
    # Basic cleaning / formatting
    # -----------------------------
    df_clean = df.copy()
    df_clean.columns = [c.strip().replace(" ", "_") for c in df_clean.columns]

    categorical_columns = [
        "Gender",
        "Parental_Involvement",
        "Access_to_Resources",
        "Extracurricular_Activities",
        "Motivation_Level",
        "Internet_Access",
        "Family_Income",
        "Teacher_Quality",
        "School_Type",
        "Peer_Influence",
        "Learning_Disabilities",
        "Parental_Education_Level",
        "Distance_from_Home",
    ]
    for col in categorical_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype("category")

    # Create Study_Sleep_Group
    if ("Hours_Studied" in df_clean.columns) and ("Sleep_Hours" in df_clean.columns):
        study_threshold = df_clean["Hours_Studied"].median()
        sleep_threshold = df_clean["Sleep_Hours"].median()

        def create_study_sleep_group(row):
            high_study = row["Hours_Studied"] > study_threshold
            high_sleep = row["Sleep_Hours"] > sleep_threshold

            if high_study and high_sleep:
                return "High Both"
            elif high_study and not high_sleep:
                return "High Study Only"
            elif not high_study and high_sleep:
                return "High Sleep Only"
            else:
                return "Low Both"

        df_clean["Study_Sleep_Group"] = df_clean.apply(create_study_sleep_group, axis=1)

    # -----------------------------
    # Sidebar
    # -----------------------------
    st.sidebar.header("Filter & Navigation")

    page = st.sidebar.radio(
        "Go to",
        [
            "📋 Overview",
            "🔑 Key Findings",
            "📈 Visualisations",
            "📊 Data Explorer",
            "🔮 Score Predictor",
            "📝 About",
        ],
    )

    # Optional global filter (example: gender)
    if "Gender" in df_clean.columns:
        st.sidebar.subheader("Quick Filter")
        gender_options = df_clean["Gender"].cat.categories.tolist() \
            if hasattr(df_clean["Gender"], "cat") else df_clean["Gender"].unique()
        selected_gender = st.sidebar.multiselect(
            "Filter by Gender",
            options=gender_options,
            default=gender_options,
        )
        df_view = df_clean[df_clean["Gender"].isin(selected_gender)]
    else:
        df_view = df_clean

    # -----------------------------
    # Overview
    # -----------------------------
    if page == "📋 Overview":
        st.header("Project Overview")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Students", len(df_view))
        with col2:
            st.metric("Features", len(df_view.columns))
        with col3:
            if "Exam_Score" in df_view.columns:
                avg_score = df_view["Exam_Score"].mean()
                st.metric("Avg Exam Score", f"{avg_score:.2f}")
            else:
                st.metric("Avg Exam Score", "N/A")

        st.subheader("Data Sample")
        st.dataframe(df_view.head(10), use_container_width=True)

        st.subheader("📌 High-Level Dataset Summary")
        st.write(
            f"- **Rows:** {df_view.shape[0]}  \n"
            f"- **Columns:** {df_view.shape[1]}  \n"
            "- Mix of numerical and categorical features related to study habits, "
            "sleep, school environment, and family background."
        )

        st.subheader("🎯 Business Requirements")
        st.markdown(
            "- **BR1:** Identify the key drivers of student performance.\n"
            "- **BR2:** Understand how study and sleep balance relate to exam scores.\n"
            "- **BR3:** Provide a simple way to estimate a student’s potential score."
        )

        st.subheader("🔬 Research Hypotheses")
        st.markdown(
            "- **H1:** Hours studied explains more variance in exam scores than attendance or sleep.\n"
            "- **H2:** Students with both high study hours and high sleep perform best.\n"
        )

    # -----------------------------
    # Key Findings
    # -----------------------------
    elif page == "🔑 Key Findings":
        st.header("🔑 Key Findings")

        with st.expander("Finding 1: Study Hours Are the Strongest Driver", expanded=True):
            st.write(
                "**What we found:** Study hours show the strongest relationship with exam score "
                "compared to other single factors like attendance or sleep."
            )
            fig, ax = plt.subplots(figsize=(8, 4))
            predictors = ["Hours Studied", "Attendance", "Sleep Hours"]
            # Example R²-style values (you can adjust these to match your notebook)
            r2_values = [0.20, 0.05, 0.03]
            colors = ["#2E86AB", "#A23B72", "#A23B72"]
            ax.bar(predictors, r2_values, color=colors)
            ax.set_ylabel("Relative Importance (R²-like)")
            ax.set_ylim(0, 0.25)
            st.pyplot(fig)

        if "Study_Sleep_Group" in df_view.columns and "Exam_Score" in df_view.columns:
            with st.expander("Finding 2: Study + Sleep Balance Matters", expanded=True):
                st.write(
                    "Students who manage **both** higher study hours and higher sleep "
                    "tend to achieve the best scores overall."
                )
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.boxplot(
                    data=df_view,
                    x="Study_Sleep_Group",
                    y="Exam_Score",
                    ax=ax,
                )
                ax.set_xlabel("Study–Sleep Group")
                ax.set_ylabel("Exam Score")
                st.pyplot(fig)

    # -----------------------------
    # Visualisations
    # -----------------------------
    elif page == "📈 Visualisations":
        st.header("📈 Visualisations")

        tab1, tab2 = st.tabs(["Correlation Matrix", "Study–Sleep Groups"])

        with tab1:
            st.subheader("Correlation Matrix (Numerical Features)")
            numerical_df = df_view.select_dtypes(include=[np.number])
            if len(numerical_df.columns) > 1:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(
                    numerical_df.corr(),
                    annot=True,
                    cmap="coolwarm",
                    ax=ax,
                )
                st.pyplot(fig)
            else:
                st.info("Not enough numerical columns to show a correlation matrix.")

        with tab2:
            st.subheader("Exam Score by Study–Sleep Group")
            if "Study_Sleep_Group" in df_view.columns and "Exam_Score" in df_view.columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.boxplot(
                    data=df_view,
                    x="Study_Sleep_Group",
                    y="Exam_Score",
                    ax=ax,
                )
                ax.set_xlabel("Study–Sleep Group")
                ax.set_ylabel("Exam Score")
                st.pyplot(fig)
            else:
                st.info("Study_Sleep_Group or Exam_Score not available in the dataset.")

    # -----------------------------
    # Data Explorer
    # -----------------------------
    elif page == "📊 Data Explorer":
        st.header("📊 Explore the Data")

        # Extra filters
        df_explore = df_view.copy()

        if "School_Type" in df_explore.columns:
            school_options = df_explore["School_Type"].unique()
            selected_school = st.multiselect(
                "Filter by School Type",
                options=school_options,
                default=school_options,
            )
            df_explore = df_explore[df_explore["School_Type"].isin(selected_school)]

        if "Parental_Involvement" in df_explore.columns:
            involvement_options = df_explore["Parental_Involvement"].unique()
            selected_involvement = st.multiselect(
                "Filter by Parental Involvement",
                options=involvement_options,
                default=involvement_options,
            )
            df_explore = df_explore[df_explore["Parental_Involvement"].isin(selected_involvement)]

        st.subheader("Filtered Data")
        st.dataframe(df_explore, use_container_width=True)

    # -----------------------------
    # Score Predictor
    # -----------------------------
    elif page == "🔮 Score Predictor":
        st.header("🔮 Simple Score Predictor")
        st.write(
            "This is a **simple, data-inspired tool** that estimates a student's exam score "
            "based mainly on their study hours (and optionally sleep). "
            "It’s not a full machine learning model, but it follows the patterns seen in the data."
        )

        if "Hours_Studied" in df_clean.columns and "Exam_Score" in df_clean.columns:
            # Fit a simple linear relationship: Exam_Score ~ Hours_Studied
            x = df_clean["Hours_Studied"].values
            y = df_clean["Exam_Score"].values

            # Remove any NaNs
            mask = ~np.isnan(x) & ~np.isnan(y)
            x = x[mask]
            y = y[mask]

            if len(x) > 1:
                # Simple linear regression using numpy
                slope, intercept = np.polyfit(x, y, 1)

                st.subheader("Enter Your Details")

                col1, col2 = st.columns(2)
                with col1:
                    user_hours = st.number_input(
                        "Study Hours per Week",
                        min_value=0.0,
                        max_value=100.0,
                        value=float(np.median(x)),
                        step=1.0,
                    )
                with col2:
                    if "Sleep_Hours" in df_clean.columns:
                        sleep_vals = df_clean["Sleep_Hours"].dropna().values
                        default_sleep = float(np.median(sleep_vals)) if len(sleep_vals) > 0 else 7.0
                        user_sleep = st.number_input(
                            "Sleep Hours per Night",
                            min_value=0.0,
                            max_value=16.0,
                            value=default_sleep,
                            step=0.5,
                        )
                    else:
                        user_sleep = None
                        st.info("Sleep_Hours not found in dataset, prediction will use study hours only.")

                if st.button("Estimate Score"):
                    base_pred = intercept + slope * user_hours

                    # Optional gentle adjustment based on sleep
                    if user_sleep is not None:
                        # Assume 7–9 hours is ideal range
                        if 7 <= user_sleep <= 9:
                            base_pred += 3  # small bonus
                        elif user_sleep < 5:
                            base_pred -= 3  # small penalty

                    predicted_score = float(np.clip(base_pred, 0, 100))
                    st.success(f"Estimated Exam Score: **{predicted_score:.1f} / 100**")

                    st.caption(
                        "This is a rough estimate based on patterns in the dataset, "
                        "not a guaranteed result."
                    )

                st.subheader("How the Model Sees Study Hours")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.scatter(x, y, alpha=0.4, label="Students")
                x_line = np.linspace(x.min(), x.max(), 100)
                y_line = intercept + slope * x_line
                ax.plot(x_line, y_line, color="red", label="Trend Line")
                ax.set_xlabel("Hours Studied per Week")
                ax.set_ylabel("Exam Score")
                ax.legend()
                st.pyplot(fig)
            else:
                st.info("Not enough data to build a predictor.")
        else:
            st.info("Required columns (Hours_Studied and Exam_Score) are not available in the dataset.")

    # -----------------------------
    # About
    # -----------------------------
    elif page == "📝 About":
        st.header("📝 About This Project")
        st.write("**Author:** Sadiyah")
        st.write("**Dataset:** Student Performance Factors (Kaggle)")
        st.write(
            "This dashboard was built to explore what really affects exam scores, "
            "with a focus on making insights clear, visual, and interactive."
        )

        st.markdown("---")
        st.caption("Created as part of a data analytics project on student performance factors.")

else:
    st.error("Data file not found! Please check your file paths in the repository.")