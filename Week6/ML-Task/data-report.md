📄 Data Analysis Report – Hospital Admissions Dataset


1. ### Dataset Overview
The Hospital Admissions dataset contains records related to patient admissions, including demographic details, hospital logistics, insurance information, and billing data.
The dataset is intended to analyze patient admission patterns and prepare clean data for downstream machine learning tasks.
Raw dataset: hospital_admissions_dirty.csv
Processed dataset: final.csv
Domain: Healthcare / Hospital Management
The raw dataset contains several data quality issues such as missing values, inconsistent entries, invalid values, and extreme observations, which were addressed through exploratory data analysis and a structured data pipeline.

2. ### Missing Values Analysis
EDA revealed missing values in several columns:
- Age contains missing values.
- Insurance_Provider contains missing values for some patients.
- Room_Number has missing entries.

# Based on data characteristics 
- Missing Age values were imputed using the median.
- Missing Insurance_Provider values were filled with "Unknown".
- Missing Room_Number values were assigned a placeholder value to preserve records.



3. ### Duplicate Records Analysis
The dataset was checked for duplicate rows to ensure data integrity.
Exact duplicate records were identified during EDA.
Duplicate entries can lead to biased statistics and incorrect model learning.
All exact duplicate rows were removed during data preprocessing to ensure each admission record is unique.

4. ### Outlier Analysis
Outlier analysis was conducted only on meaningful numerical features.
Key observations:

- Age contains invalid values (negative values and values exceeding reasonable biological limits).
- Billing_Amount contains extreme values and is heavily right-skewed.


Handling strategy:

Invalid Age values were removed based on domain constraints (0–120 years).
Extreme Billing_Amount values were capped using percentile-based thresholds to avoid data loss while limiting the impact of extreme cases.
Identifier-like numeric columns were excluded from outlier treatment.

5. ### Data Inconsistencies and Type Issues
EDA identified several inconsistencies and formatting issues:
Gender values were inconsistently labeled (e.g., M, F, Male, Female).
Billing_Amount was stored as a string containing currency symbols and commas.


Corrections applied:
Gender values were standardized to consistent categories.
Billing amounts were converted to numeric format after removing non-numeric characters.
These steps ensure uniform representation and improve downstream compatibility.

6. ### Feature Scale and Standardization Considerations
EDA showed that numerical features exist on significantly different scales (e.g., Age vs Billing Amount).
No scaling or standardization was applied at this stage, as such transformations are model-dependent and are better handled during the training phase rather than during raw data preprocessing.

7. ### Data Cleaning Summary
Based on insights from EDA, the data pipeline performed the following actions:

Handled missing values using statistically and domain-appropriate methods.
Removed duplicate records.
Corrected inconsistent categorical values.
Converted incorrectly typed numerical fields.
Applied domain-aware outlier handling.
Preserved raw data and generated a clean processed dataset.
The cleaned dataset was saved as final.csv in the data/processed directory.

8. ### Conclusion
The hospital admissions dataset has been successfully analyzed and cleaned using a reproducible data pipeline informed by exploratory data analysis.


