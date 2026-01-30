import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif

# Paths
base = Path(__file__).resolve().parents[1]
data_file = base / "data" / "processed" / "final.csv"
json_file = base / "features" / "feature_list.json"
plot_file = base / "evaluation" / "feature_importance.png"

base.joinpath("features").mkdir(exist_ok=True)
base.joinpath("evaluation").mkdir(exist_ok=True)


def main():
    # Load data
    df = pd.read_csv(data_file)

    #Basic feature creation
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
    df["Fare_Log"] = np.log1p(df["Fare"])

    df = pd.get_dummies(df, columns=["Sex", "Embarked"], drop_first=True)

    X = df.drop(["Survived", "PassengerId", "Name", "Ticket"], axis=1, errors="ignore")
    y = df["Survived"]

    #Correlation threshold
    corr = X.corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))

    remove_cols = [c for c in upper.columns if any(upper[c] > 0.85)]
    X = X.drop(columns=remove_cols)

    #Mutual Information
    mi = mutual_info_classif(X, y, random_state=42)

    mi_df = pd.DataFrame({
        "feature": X.columns,
        "score": mi
    }).sort_values(by="score", ascending=False)

    selected = mi_df[mi_df["score"] > 0.01]["feature"].tolist()

    #Save results
    with open(json_file, "w") as f:
        json.dump(selected, f, indent=4)

    plt.figure(figsize=(8, 5))
    plt.barh(mi_df.head(10)["feature"], mi_df.head(10)["score"])
    plt.xlabel("MI Score")
    plt.title("Feature Importance")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()

    print(f"Selected {len(selected)} features")


if __name__ == "__main__":
    main()
