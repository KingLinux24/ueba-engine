from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="UEBA Engine", version="1.0")

@app.get("/alerts")
def alerts():
    df = pd.read_csv("data/processed/alerts.csv")
    return df.to_dict(orient="records")
