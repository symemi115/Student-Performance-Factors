# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# **Student Performance Analysis: What Really Affects Exam Scores?**

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=power%20bi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

##  **Live Dashboard**

## Project Overview
This data analytics project investigates the factors that influence student academic performance, specifically examining which variables most strongly predict exam scores. Using a comprehensive dataset of student attributes including study habits, attendance patterns, and lifestyle factors, this study tests four interconnected hypotheses about academic success.

## Research Questions & Hypotheses:
#### **H1: Individual Impact**
- Hours studied explains more variance in exam scores than attendance rate or sleep hours when analyzed separately.
Analytical Approach = Simple linear Regression

#### **H2: 2: Combined Effects**
- The combination of hours studied AND attendance rate predicts exam scores better than either variable alone.
Analyticial Approach = Multiple regression with interaction.

#### **H3: Threshold Success**
- Students who study more than 20 hours per week AND get more than 7 hours of sleep score significantly higher than those meeting only one or neither threshold.
Analytical Approach = ANOVA/ Group Comparison.

#### **H4: Variable Comparison**
- Hours studied has the strongest correlation with exam scores among all continuous variables in the dataset.
Analytical Approach = Correlation Matrix Analysis.

## **DataSet**
Source: Student Performance Factors (https://www.kaggle.com/datasets/lainguyn123/student-performance-factors) - Kaggle

**Decsription**:  This dataset contains information on student demographics, study habits, parental involvement, and academic performance metrics.

***Key Features:***
- Hours Studied
- Attendance Rate
- Sleep Hours
- Previous Scores
- Extracurricular Activities
- Exam Score (Target Variable)

## Methodology

1. ***Data Cleaning & Preprocessing***:
- Handle missing values
- Check for outliers
- Convert data types
- Feature engineering (creating threshold groups for H3)

2. ***Exploratory Data Analysis (EDA)***:
- Summary statistics
- Distribution visualizations
- Initial correlation exploration

3. ***Hypothesis Testing***:
- H1: Three simple linear regressions comparing R² values
- H2: Multiple regression with interaction term
- H3: Group comparisons using ANOVA/t-tests
- H4: Comprehensive correlation analysis with heatmap visualisation.

## Technologies Used
- Python (Recommended)
- Pandas (data manipulation)
- NumPy (numerical operations)
- Matplotlib/Seaborn (visualisations)
- SciPy/StatsModels (statistical testing)
- Scikit-learn (regression modeling)

## Expected Outcomes
This analysis will:
- Identify the strongest predictors of academic success
- Determine whether study hours alone matter more than combination factors
- Reveal if there's a "sweet spot" threshold for study and sleep
- Provide data-driven insights for students and educators

