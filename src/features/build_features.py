import json
import pandas as pd
from pathlib import Path

IN = Path("data/raw/events.jsonl")
OUT = Path("data/processed/user_features.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

def main():
    rows = []
    with IN.open("r") as f:
        for line in f:
            rows.append(json.loads(line))

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.floor("1h")

    df["is_login"] = (df["event_type"] == "login").astype(int)
    df["is_failed"] = ((df["event_type"] == "login") & (~df["success"])).astype(int)
    df["is_sensitive"] = df["resource"].isin(["finance-db"]).astype(int)
    df["off_hours"] = ~df["timestamp"].dt.hour.between(8, 18)

    grouped = df.groupby(["user_id", "hour"]).agg(
        login_count=("is_login", "sum"),
        failed_login_ratio=("is_failed", "mean"),
        unique_hosts=("host", "nunique"),
        unique_countries=("geo_country", "nunique"),
        off_hours_login=("off_hours", "max"),
        sensitive_resource_access=("is_sensitive", "max"),
        anomaly_label=("label", "max")
    ).reset_index()

    grouped.to_csv(OUT, index=False)

if __name__ == "__main__":
    main()
