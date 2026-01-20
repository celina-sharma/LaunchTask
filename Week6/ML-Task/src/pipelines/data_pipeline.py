import pandas as pd
from pathlib import Path


base = Path(__file__).resolve().parents[1]
raw_data = base / "data" / "raw" / "titanic.csv"
processed_data = base / "data" / "processed" / "final.csv"


def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    df = df.copy()

    # 1. Handle missing values
    df["Age"].fillna(df["Age"].median(), inplace=True)
    df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

    # 2. Remove duplicates
    df.drop_duplicates(inplace=True)

    # 3. Handle outliers using IQR on Fare
    Q1 = df["Fare"].quantile(0.25)
    Q3 = df["Fare"].quantile(0.75)
    IQR = Q3 - Q1

    lb = Q1 - 1.5 * IQR
    up = Q3 + 1.5 * IQR

    df = df[(df["Fare"] >= lb) & (df["Fare"] <= up)]

    return df

def save_data(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

def main():
    print("Loading raw data")
    df = load_data(raw_data)

    print("Cleaning data")
    cleaned_df = clean_data(df)

    print("Saving processed data")
    save_data(cleaned_df, processed_data)

    print("Data pipeline completed successfully.")


if __name__ == "__main__":
    main()
