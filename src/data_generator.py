
import numpy as np
import pandas as pd
from datetime import datetime

def generate_city_data():
    rng = np.random.default_rng()
    now = datetime.now()

    services = [
        {
            "service": "Water",
            "location": "Central District",
            "value": rng.uniform(20, 100),
            "unit": "% pressure",
            "threshold": 35,
        },
        {
            "service": "Energy",
            "location": "Power Grid Zone A",
            "value": rng.uniform(40, 110),
            "unit": "% load",
            "threshold": 90,
        },
        {
            "service": "Waste",
            "location": "Residential Zone B",
            "value": rng.uniform(20, 110),
            "unit": "% bin capacity",
            "threshold": 85,
        },
        {
            "service": "Air Quality",
            "location": "Industrial Zone C",
            "value": rng.uniform(20, 180),
            "unit": "AQI",
            "threshold": 100,
        },
    ]

    rows = []

    for item in services:
        rows.append({
            "timestamp": now,
            "service": item["service"],
            "location": item["location"],
            "value": round(float(item["value"]), 2),
            "unit": item["unit"],
            "threshold": item["threshold"],
        })

    return pd.DataFrame(rows)
