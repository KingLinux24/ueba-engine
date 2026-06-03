import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import IsolationForest

DATA = Path("data/processed/user_features.csv")
MODEL_OUT = Path("src/models/ueba_iforest.joblib")

def main():
    df = pd.read_csv(DATA)

    feature_cols = [
        "login_count",
        "failed_login_ratio",
        "unique_hosts",
        "unique_countries",
        "off_hours_login",
        "sensitive_resource_access"
    ]

    X = df[feature_cols]

    model = IsolationForest(
        n_estimators=400,
        contamination=0.05,
        random_state=42
    )

    model.fit(X)

    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_OUT)

if __name__ == "__main__":
    main()
