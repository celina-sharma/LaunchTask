import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "final.csv"

def load_data():
    return pd.read_csv(DATA_PATH)


#FEATURE ENGINEERING
def create_family_features(df):
    df = df.copy()
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
    return df


def create_age_features(df):
    df = df.copy()

    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[0, 18, 40, 60, 100],
        labels=["Child", "Young", "Adult", "Senior"]
    )

    df["IsChild"] = (df["Age"] < 18).astype(int)
    df["IsElderly"] = (df["Age"] > 60).astype(int)
    return df


def create_fare_features(df):
    df = df.copy()
    df["Fare_Log"] = np.log1p(df["Fare"])
    df["Fare_Per_Person"] = df["Fare"] / df["FamilySize"]
    return df


def drop_unwanted_columns(df):
    return df.drop(
        columns=["PassengerId", "Name", "Ticket"],
        errors="ignore"
    )


def encode_categoricals(df):
    categorical_cols = ["Sex", "Embarked", "Age_Group"]
    return pd.get_dummies(df, columns=categorical_cols, drop_first=True)


#SPLIT & SCALE
def split_data(df):
    X = df.drop("Survived", axis=1)
    y = df["Survived"]

    return train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )


def scale_features(X_train, X_test):
    numeric_cols = X_train.select_dtypes(include=["int64", "float64"]).columns

    scaler = StandardScaler()
    X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

    return X_train, X_test


# ---------------- PIPELINE ----------------
def main():
    df = load_data()
    print("Initial shape:", df.shape)

    df = create_family_features(df)
    df = create_age_features(df)
    df = create_fare_features(df)
    df = drop_unwanted_columns(df)
    df = encode_categoricals(df)

    print("After feature engineering:", df.shape)

    X_train, X_test, y_train, y_test = split_data(df)
    X_train, X_test = scale_features(X_train, X_test)

    print("Train shape:", X_train.shape)
    print("Test shape :", X_test.shape)

    print("\nTarget distribution (train):")
    print(y_train.value_counts())

    print("\n Feature engineering completed")


if __name__ == "__main__":
    main()
