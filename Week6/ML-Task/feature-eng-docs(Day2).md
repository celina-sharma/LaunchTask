# Feature Engineering – Titanic Dataset

## Overview
This document describes the complete **Day 2 feature engineering and feature selection pipeline** for the Titanic Survival Prediction project. The goal of this stage is to transform the cleaned dataset into a structured, informative, and model-ready format that improves predictive performance.

---

## Objective
The primary objectives of the feature engineering phase are to:
- Generate meaningful new features from raw data
- Encode categorical variables into numerical form
- Normalize numerical features where required
- Reduce redundancy using feature selection techniques
- Identify the most relevant predictors for survival

This step ensures the dataset is well-prepared for model training in the next phase.

---

## Input Dataset
- **Source:** `data/processed/final.csv`
- **Target Variable:** `Survived`
  - `0` → Did not survive  
  - `1` → Survived  

---

## Feature Engineering

Feature engineering involved creating new features, transforming existing ones, and encoding categorical variables to enhance the dataset.

### Family-Based Features
- **FamilySize**  
  Total number of family members traveling together, calculated as:  
  `SibSp + Parch + 1`
- **IsAlone**  
  Binary feature indicating whether a passenger traveled alone (1) or with family (0)

These features capture social and family context, which has a known impact on survival chances.

---

### Fare-Based Features
- **Fare_Log**  
  Log-transformed version of the Fare column to reduce skewness and stabilize variance

This transformation helps the model better learn from fare distribution differences.

---

### Categorical Encoding
Categorical variables were converted into numerical format using **one-hot encoding**:
- `Sex` → `Sex_male`
- `Embarked` → `Embarked_S`, `Embarked_Q`

The first category was dropped to avoid multicollinearity.

---

### Numerical Features Retained
The following original numerical features were retained due to their strong relevance:
- `Age`
- `Fare`
- `Pclass`
- `SibSp`
- `Parch`

---

### Summary of Feature Generation
Through feature creation, transformation, and encoding, **more than 10 features were generated** during this phase. This satisfies the feature generation requirement of the Day 2 task.

---

## Feature Selection

Feature selection was performed to reduce noise and retain only the most informative features.

### Correlation Thresholding
- A correlation threshold of **0.85** was applied.
- Highly correlated feature pairs were identified.
- One feature from each highly correlated pair was removed to reduce redundancy and multicollinearity.

---

### Mutual Information
- **Mutual Information (MI)** was used to measure the dependency between individual features and the target variable (`Survived`).
- Features with an MI score greater than **0.01** were retained.
- MI was chosen because it can capture both linear and non-linear relationships.

---

### Final Selected Features
After feature selection, the following **8 features** were identified as the most relevant:

- `Sex_male`
- `Fare`
- `Embarked_S`
- `IsAlone`
- `Age`
- `SibSp`
- `Pclass`
- `Embarked_Q`

These features collectively capture demographic, socioeconomic, and family-based survival patterns.

---

## Feature Importance Visualization
- A feature importance plot based on Mutual Information scores was generated.
- The visualization highlights the relative importance of each selected feature.
- Output saved to:

