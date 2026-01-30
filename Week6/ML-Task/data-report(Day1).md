# Titanic Dataset – Exploratory Data Analysis (EDA) Report

## 1. Introduction
This report presents the Exploratory Data Analysis (EDA) performed on the Titanic dataset as part of the machine learning data pipeline. The objective of this stage is to understand the structure, quality, and characteristics of the data before applying preprocessing and model training techniques.

---

## 2. Dataset Overview
The Titanic dataset contains passenger-level information including travel class, fare paid, family relationships, and survival outcome. Each row represents an individual passenger.

**Dataset Objectives:**
- Understand feature distributions and relationships
- Identify data quality issues
- Prepare the dataset for preprocessing and modeling

---

## 3. Target Variable
The target variable for this dataset is **`Survived`**, where:
- `0` indicates the passenger did not survive
- `1` indicates the passenger survived

The target distribution shows a mild class imbalance, with more non-survivors than survivors. This observation suggests that model evaluation should rely on metrics such as **ROC-AUC, precision, and recall**, rather than accuracy alone.

---

## 4. Missing Value Analysis
Missing values were identified in the following columns:

- **Age**: Missing values were imputed using the **median**, as the feature shows skewness and contains outliers.
- **Embarked**: Missing values were imputed using the **mode**, as it is a categorical feature.
- **Cabin**: This column was dropped due to a very high proportion of missing values, making reliable imputation impractical.

A **missing values heatmap** was generated to visually inspect the pattern of missing data, confirming that missingness was limited and not structurally dependent.

---

## 5. Duplicate Records
The dataset was checked for duplicate rows using pandas utilities.  
No duplicate records were found, as each passenger entry represents a unique observation.

---

## 6. Outlier Analysis
Outlier analysis was primarily conducted on numerical features.

- Significant outliers were observed in the **Fare** column due to a small number of passengers paying exceptionally high fares.
- Outliers were detected and handled using the **Interquartile Range (IQR)** method.
- Mild outliers were also observed in **Age**, **SibSp**, and **Parch**, which represent realistic passenger scenarios and were not aggressively modified.

This approach helped reduce skewness while preserving meaningful data.

---

## 7. Feature Distributions
Exploratory visualizations revealed the following insights:

- **Age** and **Fare** exhibit right-skewed distributions.
- **Male passengers** outnumbered female passengers in the dataset.

These distributions provided useful context for understanding passenger demographics and data imbalance.

---

## 8. Feature Relationships
Several important relationships were identified during EDA:

- Female passengers showed a significantly higher survival rate than males.
- Passengers in **first class** had a higher probability of survival compared to those in second and third classes.
- Correlation analysis revealed:
  - A positive relationship between **Fare** and **Survived**
  - A negative relationship between **Passenger Class (Pclass)** and **Survived**

---

## 9. Conclusion
The exploratory data analysis provided a clear understanding of data quality, feature behavior, and key relationships within the Titanic dataset. Based on these findings, the dataset was successfully cleaned and saved as a processed version for further preprocessing and model training. This EDA phase forms a strong foundation for the subsequent stages of the machine learning pipeline.
