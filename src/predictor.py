
import numpy as np
from sklearn.ensemble import RandomForestRegressor

SERVICE_CODES = {
    "Water": 0,
    "Energy": 1,
    "Waste": 2,
    "Air Quality": 3,
}

def train_predictor():
    rng = np.random.default_rng(42)
    n = 3000

    service_code = rng.integers(0, 4, n)
    value = rng.uniform(10, 120, n)
    hour = rng.integers(0, 24, n)

    # Synthetic next-reading behavior.
    rush = np.where((hour >= 7) & (hour <= 10), 1.0, 0.0)
    rush += np.where((hour >= 17) & (hour <= 20), 1.0, 0.0)

    change = (
        np.where(service_code == 0, -1.5, 0.0)
        + np.where(service_code == 1, rush * 5, 0.0)
        + np.where(service_code == 2, 2.0, 0.0)
        + np.where(service_code == 3, rush * 3, 0.0)
        + rng.normal(0, 3, n)
    )

    future_value = np.maximum(0, value + change)

    X = np.column_stack([service_code, value, hour])
    model = RandomForestRegressor(
        n_estimators=80,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X, future_value)
    return model

def predict_future(df, model):
    result = df.copy()
    predictions = []

    for _, row in result.iterrows():
        features = [[
            SERVICE_CODES[row["service"]],
            float(row["value"]),
            int(row["timestamp"].hour),
        ]]
        predictions.append(float(model.predict(features)[0]))

    result["predicted_value_15m"] = np.round(
        predictions, 2
    )
    return result
