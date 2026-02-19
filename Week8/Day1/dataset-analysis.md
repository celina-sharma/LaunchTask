# Dataset Analysis Report
## Week 8 — Day 1 | LLM Architecture and Data Prep for fine-tuning

---

## 1. Overview

This report documents the preparation and analysis of an instruction tuning dataset
built for the purpose of fine-tuning a Large Language Model (LLM).

---

## 2. Dataset Source

| Property        | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| Name            | CodeAlpaca                                                              |
| Source          | Hugging Face                                                            |
| Link            | https://huggingface.co/datasets/thisisanshgupta/CodeAlpaca              |
| Domain          | Coding (Python, JavaScript, SQL, C++, Java and more)                   |
| Total Available | 20,022 samples                                                          |
| Selected        | 1,200 samples (400 per type)                                            |
                                                        

---

## 3. Dataset Format

Every sample follows the standard instruction tuning JSONL format:
```json
{"instruction": "...", "input": "...", "output": "..."}
```

| Field       | Description                                              |
|-------------|----------------------------------------------------------|
| instruction | The task or question given to the model                  |
| input       | Additional context or code snippet (can be empty)        |
| output      | The expected response or solution from the model         |

---

## 4. Sample Types

The dataset is divided into 3 carefully labeled types based on the nature
of the instruction:

| Type       | Count | Description                                                        |
|------------|-------|--------------------------------------------------------------------|
| QA         | 400   | Direct coding questions with clear and concise answers             |
| Reasoning  | 400   | Debugging, analyzing, explaining and fixing code step by step      |
| Extraction | 400   | Extracting specific information or patterns from given code        |
| **Total**  | **1,200** | Balanced across all 3 types                                   |

### Why these 3 types?
- **QA** trains the model to answer direct questions confidently
- **Reasoning** trains the model to think step by step and debug
- **Extraction** trains the model to identify and pull out specific information

---

## 5. Data Cleaning Pipeline

All cleaning was performed using `utils/data_cleaner.py`

### Cleaning Steps Applied:

| Step | Operation                        | Reason                                          |
|------|----------------------------------|-------------------------------------------------|
| 1    | Remove empty outputs             | Empty outputs provide no learning signal        |
| 2    | Remove duplicate instructions    | Duplicates cause overfitting                    |
| 3    | Remove short outputs (<3 words)  | Too short to be meaningful for training         |

### Cleaning Results:

| Split | Before Cleaning | After Cleaning | Removed |
|-------|----------------|----------------|---------|
| Train | 1,080          | 1,023          | 57      |
| Val   | 120            | 116            | 4       |

---

## 6. Train / Validation Split

| Split      | Samples | Percentage |
|------------|---------|------------|
| Train      | 1,080   | 90%        |
| Validation | 120     | 10%        |
| **Total**  | **1,200** | **100%** |

The dataset was split using a fixed random seed of `42` to ensure
reproducibility across runs.

---

## 7. Token Length Analysis

Token lengths were estimated using the formula:
 **tokens ≈ total characters / 4**

### Train Set:

| Metric          | Value |
|-----------------|-------|
| Total Samples   | 1,080 |
| Mean Tokens     | 74.3  |
| Median Tokens   | 60.0  |
| Min Tokens      | 9     |
| Max Tokens      | 431   |
| Outliers (>512) | 0   |

### Validation Set:

| Metric          | Value |
|-----------------|-------|
| Total Samples   | 120   |
| Mean Tokens     | 73.0  |
| Median Tokens   | 58.5  |
| Min Tokens      | 16    |
| Max Tokens      | 297   |
| Outliers (>512) | 0     |

### Key Observations:
- Average token length is **~74 tokens** — well within fine-tuning limits
- Maximum token length is **431** — safely under the 512 token threshold
- **No outliers** were found in either split
- Both train and val sets have **similar distributions** — good consistency

---

## 8. Distribution Graphs

### Token Length Distribution
Shows how token lengths are spread across train and val sets.

### Sample Type Distribution
Shows the balance between QA, Reasoning and Extraction types.


### Key Observations:
- All 3 sample types are **equally distributed** (~360 each after cleaning)
- Token lengths follow a **right skewed distribution**
- The dataset is **clean, balanced and ready** for fine-tuning 

---

## 9. Final Deliverables

| File                      | Description                              |
|---------------------------|------------------------------------------|
| `data/train.jsonl`        | 1,023 clean training samples             |
| `data/val.jsonl`          | 116 clean validation samples             |
| `utils/data_cleaner.py`   | Cleaning pipeline script                 |
| `token_distribution.png`  | Token length distribution graph          |
| `type_distribution.png`   | Sample type distribution graph           |
| `DATASET-ANALYSIS.md`     | This report                              |

---

## 10. Conclusion

The dataset has been successfully prepared for LLM instruction fine-tuning.
It is clean, balanced across 3 task types, well within token length limits,
and follows the standard JSONL format required for fine-tuning pipelines.