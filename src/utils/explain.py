def explain(row):
    reasons = []

    if row["unique_countries"] > 1:
        reasons.append("Login activity from multiple countries")
    if row["failed_login_ratio"] > 0.3:
        reasons.append("High rate of failed login attempts")
    if row["off_hours_login"]:
        reasons.append("Login during unusual hours")
    if row["sensitive_resource_access"]:
        reasons.append("Access to sensitive resources")

    if not reasons:
        reasons.append("Behavior deviates from established baseline")

    return reasons
