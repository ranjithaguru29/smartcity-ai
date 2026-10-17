
import os
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.data_generator import generate_city_data
from src.risk_detector import detect_risks
from src.predictor import train_predictor, predict_future
from src.recommendation_engine import recommend_actions

st.set_page_config(
    page_title="SmartCity AI",
    page_icon="🏙️",
    layout="wide",
)

st_autorefresh(interval=5000, key="city_refresh")

st.title("🏙️ SmartCity AI")
st.caption(
    "Real-time urban monitoring, risk prediction "
    "and prioritized decision support"
)
st.info(
    "DEMO MODE: All sensor readings are simulated. "
    "Forecasts and recommendations require real-world "
    "validation before operational use."
)

@st.cache_resource
def load_model():
    return train_predictor()

model = load_model()

# Keep a history of readings for trend visualization.
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame()

live = generate_city_data()
live = detect_risks(live)
live = predict_future(live, model)
live = recommend_actions(live)

# Add one new observation for each service to the history.
snapshot = live[
    ["timestamp", "service", "location", "value"]
].copy()

st.session_state.history = pd.concat(
    [st.session_state.history, snapshot],
    ignore_index=True,
).tail(500)

# Save the current readings locally.
os.makedirs("data", exist_ok=True)
live.to_csv("data/city_data.csv", index=False)

critical = int((live["risk_level"] == "CRITICAL").sum())
high = int((live["risk_level"] == "HIGH").sum())
medium = int((live["risk_level"] == "MEDIUM").sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Services monitored", live["service"].nunique())
c2.metric("Critical risks", critical)
c3.metric("High risks", high)
c4.metric("Medium risks", medium)

st.subheader("Live city service overview")

left, right = st.columns(2)

with left:
    fig = px.bar(
        live,
        x="service",
        y="value",
        color="risk_level",
        hover_data=["location", "unit", "threshold"],
        title="Current sensor readings",
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.bar(
        live,
        x="service",
        y="predicted_value_15m",
        color="risk_level",
        hover_data=["location", "threshold"],
        title="Predicted readings in 15 minutes",
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Prioritized alerts and actions")

columns = [
    "risk_level",
    "risk_score",
    "service",
    "location",
    "value",
    "unit",
    "predicted_value_15m",
    "decision_maker",
    "recommended_action",
]

st.dataframe(
    live[columns].rename(columns={
        "risk_level": "Risk",
        "risk_score": "Risk score",
        "service": "City service",
        "location": "Location",
        "value": "Current reading",
        "unit": "Unit",
        "predicted_value_15m": "Forecast (15 min)",
        "decision_maker": "Responsible department",
        "recommended_action": "Recommended action",
    }),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Explainable AI risk analysis")

selected = st.selectbox(
    "Select a city service",
    live["service"].tolist(),
)

row = live[live["service"] == selected].iloc[0]

a, b = st.columns(2)
with a:
    st.write(f"**Service:** {row['service']}")
    st.write(f"**Location:** {row['location']}")
    st.write(f"**Risk level:** {row['risk_level']}")
    st.write(f"**Risk score:** {row['risk_score']}/100")

with b:
    st.write(f"**Current reading:** {row['value']} {row['unit']}")
    st.write(f"**Configured threshold:** {row['threshold']}")
    st.write(
        f"**Predicted reading:** "
        f"{row['predicted_value_15m']} {row['unit']}"
    )

st.write("**Why was this action recommended?**")
st.write(row["explanation"])
st.write("**Suggested next action:**")
st.write(row["recommended_action"])
st.write("**Responsible department:**", row["decision_maker"])

st.subheader("Sensor trends")

history = st.session_state.history
if not history.empty:
    selected_history = history[
        history["service"] == selected
    ]
    fig = px.line(
        selected_history,
        x="timestamp",
        y="value",
        markers=True,
        title=f"{selected} sensor readings over time",
    )
    st.plotly_chart(fig, use_container_width=True)

st.download_button(
    "Download current city data (CSV)",
    data=live.to_csv(index=False).encode("utf-8"),
    file_name="smartcity_current_data.csv",
    mime="text/csv",
)

st.caption(
    "Prototype: human verification is required. "
    "Synthetic-data performance is not real-city validation."
)
