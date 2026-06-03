# User & Entity Behavior Analytics (UEBA) Engine

## Overview
This repository contains a User and Entity Behavior Analytics (UEBA) system designed to learn normal baseline behaviors for users and entities, subsequently flagging deviations that may indicate compromised accounts, insider threats, or policy violations. 

This engine is built on **identity-centric security** principles. It relies entirely on synthetic, privacy-aware telemetry—meaning no actual surveillance or private data is utilized.

## What is UEBA and Why It Matters
Traditional rule-based security often fails to catch sophisticated attacks that use legitimate, compromised credentials. UEBA shifts the focus from static rules to dynamic behavioral baselines. By understanding what "normal" looks like for a specific user (e.g., standard working hours, typical host machines, standard geo-locations), the engine can identify subtle anomalies that indicate an account has been taken over or an insider is abusing their access.

## Behavioral Features & Rationale
The engine aggregates raw event telemetry into time-windowed (hourly) behavioral features per user:
* **`login_count`**: High frequency can indicate brute-force or automated script activity.
* **`failed_login_ratio`**: A high ratio is a strong indicator of credential stuffing or guessing.
* **`unique_hosts` & `unique_countries`**: Accessing resources from unusual or multiple locations/devices in a short window signals potential compromise (impossible travel).
* **`off_hours_login`**: Activity outside of normal business hours often warrants lower trust.
* **`sensitive_resource_access`**: Anomalous access to high-value assets (like a finance database) acts as a strong multiplier for risk.

## Risk Scoring vs. Binary Detection
Unlike standard detection rules that simply output "Malicious" or "Benign," UEBA embraces the grey area. It generates a **Risk Score** (normalized between 0 and 1) based on the anomaly score from an Isolation Forest model. 
* **Binary detection** creates alert fatigue when weak signals trigger false positives. 
* **Risk scoring** allows Security Operations Center (SOC) analysts to set thresholds and prioritize investigations based on the accumulation of multiple weak signals over time.

## Example Alerts with Explanations
To prevent "black box" machine learning, alerts are enriched with explainable reasons. 
* **Scenario A:** User logs in from a new country and fails multiple times.
    * *Explanation Output:* `["Login activity from multiple countries", "High rate of failed login attempts"]`
* **Scenario B:** User accesses the finance database at 2:00 AM on a Sunday.
    * *Explanation Output:* `["Login during unusual hours", "Access to sensitive resources"]`

## Mapping to Use Cases
1.  **Account Compromise:** Detected via geographic anomalies, unfamiliar hosts, and sudden spikes in failed logins followed by success.
2.  **Insider Threat:** Detected via off-hours access to sensitive resources that the user normally does not interact with, or massive spikes in generic file access.

## Privacy and Ethical Considerations
This engine evaluates telemetry and system access logs, not personal communications or private content. In a production environment, UEBA must be deployed in accordance with local privacy laws (e.g., GDPR, CCPA). Best practices include pseudonymizing user IDs during model training and strict role-based access control (RBAC) to the alert outputs. 

## Limitations and Tuning Guidance
* **Cold Start Problem:** Unsupervised models like Isolation Forest require a sufficient baseline of normal data. New users will likely trigger false positives until their baseline is established.
* **Contamination Parameter:** The `contamination` hyperparameter in `train.py` is currently set to `0.05` (assuming 5% of data is anomalous). Adjust this based on your organization's true anomaly rate and SOC capacity.

---

## Getting Started

### 1. End-to-End Execution
Run the following commands in order to generate data, build features, train the model, detect anomalies, and start the API:

```bash
python src/data/generate_events.py
python src/features/build_features.py
python src/models/train.py
python src/detection/detect.py
uvicorn src.api.app:app --reload --port 8000
```

### 2. Using the API
Once Uvicorn is running, the API will be hosted locally on port 8000.

* Important: Navigating to the base URL (http://127.0.0.1:8000/) will result in a 404 Not Found error unless you have explicitly coded a root route.

View Alerts: To see the JSON output of the anomalous alerts, navigate directly to the /alerts endpoint:

* http://127.0.0.1:8000/alerts

Interactive API Docs: FastAPI automatically generates a Swagger UI where you can explore and test your endpoints interactively. Visit:

* http://127.0.0.1:8000/docs
 --- 
<img width="1906" height="746" alt="Screenshot 2026-06-03 092303" src="https://github.com/user-attachments/assets/b1c3bf70-46e1-4905-9d15-f34df4d38b1a" />

