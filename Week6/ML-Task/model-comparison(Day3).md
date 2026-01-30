# Day 3 – Model Training & Evaluation  
## Titanic Survival Prediction

---

## Overview
This document describes the **Day 3 model training, evaluation, and model selection pipeline** for the Titanic Survival Prediction project. In this stage, multiple machine learning models are trained on the feature-engineered dataset and compared using standardized evaluation metrics to identify the best-performing model.

---

## Objective
The objectives of Day 3 are to:
- Train multiple classification models on the processed dataset
- Evaluate models using consistent performance metrics
- Apply cross-validation to ensure reliable results
- Select the best model based on a defined criterion
- Save the trained model and evaluation artifacts for reproducibility

---

## Input Dataset
- **Target Variable:** `Survived`
  - `0` → Did not survive  
  - `1` → Survived
- **Features:** Selected and engineered features from Day 2

The dataset is fully numeric and ready for model training.

---

## Data Splitting Strategy
- **Train–Test Split:**  
  - 80% training data  
  - 20% testing data
- **Stratified Sampling:**  
  - Ensures class balance is preserved across splits

This strategy prevents class imbalance bias during model evaluation.

---

## Models Trained
The following machine learning models were implemented:

### Logistic Regression
- Baseline linear classification model
- Provides interpretability and simplicity

### Random Forest Classifier
- Ensemble-based model using multiple decision trees
- Captures non-linear feature interactions

### XGBoost Classifier
- Gradient-boosted decision tree model
- Performs well on structured/tabular datasets
- Handles complex feature relationships effectively

### Neural Network (MLPClassifier)
- Feedforward neural network
- Used to compare traditional ML models with neural approaches

---

## Evaluation Methodology
- **Cross-Validation:**  
  - 5-fold cross-validation applied during evaluation
- **Evaluation Metrics Used:**
  - Accuracy
  - Precision
  - Recall
  - F1-score
  - ROC-AUC
- **Primary Model Selection Metric:**  
  - **ROC-AUC**, as it balances true positive and false positive rates

---

## Model Performance Comparison

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|------|----------|-----------|--------|----------|---------|
| Logistic Regression | 0.785 | 0.699 | 0.643 | 0.670 | 0.816 |
| Random Forest | 0.805 | 0.726 | 0.681 | 0.703 | 0.838 |
| **XGBoost** | **0.821** | **0.765** | **0.681** | **0.720** | **0.840** |
| Neural Network | 0.802 | 0.743 | 0.633 | 0.684 | 0.818 |

---

## Best Model Selection
The **XGBoost Classifier** was selected as the final model because:
- It achieved the **highest ROC-AUC score**
- It delivered the **best F1-score**, indicating a strong balance between precision and recall
- It showed better generalization across validation folds
- It outperformed other models on overall predictive capability

---

## Evaluation Artifacts
The following artifacts were generated during this stage:

- **Best Trained Model:**  
  `models/best_model.pkl`

- **Model Performance Metrics:**  
  `evaluation/metrics.json`

- **Confusion Matrix Visualization:**  
  `evaluation/confusion_matrix.png`

These artifacts support transparency, analysis, and reproducibility.

---

## Observations
- Logistic Regression provided a strong baseline but was limited to linear decision boundaries.
- Random Forest improved performance through ensemble learning.
- Neural Network achieved competitive results but raised convergence warnings due to minimal hyperparameter tuning.
- XGBoost consistently achieved the best performance across all major metrics.

---

## Conclusion
Day 3 successfully completed the **model training and evaluation phase** of the pipeline. After training and comparing four different classification models using cross-validation and multiple evaluation metrics, **XGBoost emerged as the best-performing model** for predicting passenger survival on the Titanic dataset. This model will be used in the next stage for final evaluation or deployment.

---
