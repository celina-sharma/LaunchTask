# Data Analysis Report – Titanic Dataset

## 1. Dataset Overview
The Titanic dataset contains information about passengers aboard the Titanic,ticket information, and survival status.  
The dataset is used to understand patterns related to passenger survival.

- Total rows: 891
- Target column: Survived (0 = Not Survived, 1 = Survived)

---

## 2. Missing Values Analysis
An analysis of missing values revealed the following:
- The **Age** column contains missing values.
- The **Embarked** column contains a small number of missing values.
- The **Cabin** column has a large proportion of missing data.

A missing values heatmap was generated to visually inspect the distribution of missing data across features.

---

## 3. Target Distribution
The target variable **Survived** shows an imbalanced distribution:
- A higher number of passengers did not survive compared to those who survived.

This imbalance was visualized using a count plot of the target variable.

---

## 4. Feature Distributions
Feature-wise distributions were analyzed to understand the spread and behavior of individual variables:
- The **Age** distribution shows that most passengers were between 20 and 40 years old.
- The **Sex** distribution indicates that there were more male passengers than female passengers.

Histograms and count plots were used to visualize these distributions.

---

## 5. Correlation Analysis
A correlation matrix was generated using only numerical features to study the relationship between variables:
- **Fare** shows a positive correlation with survival.
- **Passenger class (Pclass)** shows a negative correlation with survival.
- **Age** has a weaker correlation with survival.

This analysis helps identify features that may be important for future model development.

---

## 6. Data Cleaning Summary
Based on the EDA:
- Missing values in **Age** were filled using the median.
- Missing values in **Embarked** were filled using the mode.
- Duplicate records were removed.
- Outliers in the **Fare** column were handled using the IQR method.
- A cleaned dataset was saved as `final.csv` in the processed data directory.

---

## 7. Conclusion
The dataset has been successfully analyzed and cleaned.  
The processed dataset is now ready for feature engineering and machine learning model development in subsequent stages.
