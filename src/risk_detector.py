
import pandas as pd

def detect_risks(df):
    results = []

    for _, row in df.iterrows():
        service = row["service"]
        value = float(row["value"])
        threshold = float(row["threshold"])

        if service == "Water":
            # Low pressure can indicate a supply problem.
            score = max(0, min(100, (threshold - value) / threshold * 100))
            if value < threshold:
                score = max(score, 65)

        elif service in ["Energy", "Waste", "Air Quality"]:
            score = max(0, min(100, value / threshold * 100))
            if value >= threshold:
                score = min(100, max(score, 65))

        else:
            score = 0

        if score >= 85:
            level = "CRITICAL"
        elif score >= 65:
            level = "HIGH"
        elif score >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"

        results.append({
            **row.to_dict(),
            "risk_score": round(score, 1),
            "risk_level": level,
            "risk_detected": score >= 65,
        })

    return pd.DataFrame(results)
