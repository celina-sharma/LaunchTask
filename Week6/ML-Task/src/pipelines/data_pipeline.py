import pandas as pd
from pathlib import Path
import logging

base = Path(__file__).resolve().parents[1]
raw_data = base / "data" / "raw" / "titanic.csv"
processed_data = base / "data" / "processed" / "final.csv"

logs_dir = base / "logs"
logs_dir.mkdir(exist_ok=True)

log_file = logs_dir / "pipeline.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_data(path):
    logging.info("Loading raw Titanic dataset")
    return pd.read_csv(path)

def clean_data(df):
    logging.info("Starting data cleaning")
    df = df.copy()

    # 1. Handle missing values
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

    # Drop Cabin (too many missing values)
    if "Cabin" in df.columns:
        df = df.drop(columns=["Cabin"])

    # 2. Remove duplicates
    df = df.drop_duplicates()

    # 3. Handle outliers using IQR
    Q1 = df["Fare"].quantile(0.25)
    Q3 = df["Fare"].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df = df[(df["Fare"] >= lower_bound) & (df["Fare"] <= upper_bound)]

    logging.info("Data cleaning completed")
    return df

def save_data(df, path):
    logging.info("Saving cleaned dataset to data/processed/final.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

def main():
    logging.info("Data pipeline started")

    df = load_data(raw_data)
    logging.info(f"Raw data shape: {df.shape}")

    cleaned_df = clean_data(df)
    logging.info(f"Cleaned data shape: {cleaned_df.shape}")

    save_data(cleaned_df, processed_data)

    logging.info("Data pipeline completed successfully")

if __name__ == "__main__":
    main()

