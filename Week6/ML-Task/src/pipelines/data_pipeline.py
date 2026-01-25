import pandas as pd
from pathlib import Path
import logging


base_dir = Path(__file__).resolve().parents[1]
raw_path = base_dir / "data" / "raw" / "hospital_admissions_dirty.csv"
processed_path = base_dir / "data" / "processed" / "final.csv"

logs_dir = base_dir / "logs"
logs_dir.mkdir(exist_ok=True)


LOG_FILE = logs_dir / "pipeline.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_data(path):
    logging.info(f"Loading raw data: data/raw/hospital_admission_dirty.csv")
    df = pd.read_csv(path)
    logging.info(f"Raw data shape: {df.shape}")
    return df


def clean_data(df):
    logging.info("Starting data cleaning")
    df = df.copy()

    if "Age" in df.columns:
        df["Age"] = df["Age"].fillna(df["Age"].median())

    if "Insurance_Provider" in df.columns:
        df["Insurance_Provider"] = df["Insurance_Provider"].fillna("Unknown")

    if "Room_Number" in df.columns:
        df["Room_Number"] = df["Room_Number"].fillna(-1)

   #Remove duplicates
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    logging.info(f"Duplicates removed: {before - after}")

    #Fixing Inconsistence categories
    if "Gender" in df.columns:
        df["Gender"] = df["Gender"].replace({
            "M": "Male",
            "F": "Female"
        })

    if "Billing_Amount" in df.columns:
        df["Billing_Amount"] = (
            df["Billing_Amount"]
            .replace(r"[$,]", "", regex=True)
            .astype(float)
        )

    #handling outliers
    if "Age" in df.columns:
        df = df[(df["Age"] >= 0) & (df["Age"] <= 120)]

    # Billing Amount: cap extreme values
    if "Billing_Amount" in df.columns:
        lower = df["Billing_Amount"].quantile(0.01)
        upper = df["Billing_Amount"].quantile(0.99)
        df["Billing_Amount"] = df["Billing_Amount"].clip(lower, upper)

    logging.info("Data cleaning completed")
    logging.info(f"Cleaned data shape: {df.shape}")

    return df


def save_data(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logging.info(f"Processed data saved at: data/processed/final.csv")


#pipeline execution
def main():
    logging.info("Data pipeline started")

    df = load_data(raw_path)
    cleaned_df = clean_data(df)
    save_data(cleaned_df, processed_path)

    logging.info("Data pipeline completed successfully")


if __name__ == "__main__":
    main()