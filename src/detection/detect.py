import pandas as pd
import joblib
from pathlib import Path

DATA = Path("data/processed/user_features.csv")
MODEL = Path("src/models/ueba_iforest.joblib")
OUT = Path("data/processed/alerts.csv")

def main():
    df = pd.read_csv(DATA)
    model = joblib.load(MODEL)

    feature_cols = [
        "login_count",
        "failed_login_ratio",
        "unique_hosts",
        "unique_countries",
        "off_hours_login",
        "sensitive_resource_access"
    ]

    scores = model.decision_function(df[feature_cols])
    preds = model.predict(df[feature_cols])

    df["risk_score"] = (-scores - (-scores).min()) / ((-scores).max() - (-scores).min())
    df["is_anomalous"] = preds == -1

    alerts = df[df["is_anomalous"]].sort_values("risk_score", ascending=False)
    alerts.to_csv(OUT, index=False)

if __name__ == "__main__":
    main()
