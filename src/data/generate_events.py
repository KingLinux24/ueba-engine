import json
import random
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path("data/raw/events.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

USERS = ["alice", "bob", "carol"]
HOSTS = ["wkst-01", "wkst-02", "srv-fin-01"]
COUNTRIES = ["US", "US", "US", "CA", "DE"]
IPS = ["10.0.1.10", "10.0.1.11", "10.0.2.20"]

def ts(base, minutes):
    return (base + timedelta(minutes=minutes)).isoformat() + "Z"

def main():
    base = datetime.utcnow() - timedelta(days=2)
    rows = []

    # Normal behavior
    for i in range(1200):
        user = random.choice(USERS)
        rows.append({
            "timestamp": ts(base, i),
            "user_id": user,
            "host": random.choice(HOSTS),
            "event_type": random.choice(["login", "file_access"]),
            "src_ip": random.choice(IPS),
            "geo_country": random.choice(COUNTRIES),
            "success": True,
            "resource": random.choice(["shareA", "shareB", "crm", "email"]),
            "label": 0
        })

    # Anomalous user behavior (possible compromise)
    for i in range(60):
        rows.append({
            "timestamp": ts(base, 1500 + i),
            "user_id": "alice",
            "host": "srv-fin-01",
            "event_type": "login",
            "src_ip": "203.0.113.99",
            "geo_country": "RU",
            "success": i > 5,
            "resource": "finance-db",
            "label": 1
        })

    random.shuffle(rows)

    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    main()
