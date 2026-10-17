
def recommend_actions(df):
    actions = {
        "Water": (
            "Water Operations Team",
            "Verify pressure sensors and inspect the affected supply zone."
        ),
        "Energy": (
            "Energy Control Team",
            "Verify load readings and review safe load-balancing options."
        ),
        "Waste": (
            "Municipal Waste Team",
            "Prioritize collection for bins nearing their capacity limit."
        ),
        "Air Quality": (
            "Environmental Monitoring Team",
            "Validate sensor readings and investigate the pollution source."
        ),
    }

    priorities = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    output = df.copy()
    owners, recommendations, explanations = [], [], []

    for _, row in output.iterrows():
        owner, action = actions[row["service"]]
        owners.append(owner)
        recommendations.append(action)

        explanations.append(
            f"Current reading: {row['value']} {row['unit']}; "
            f"threshold: {row['threshold']}; "
            f"predicted reading in 15 min: "
            f"{row['predicted_value_15m']}."
        )

    output["decision_maker"] = owners
    output["recommended_action"] = recommendations
    output["explanation"] = explanations
    output["priority"] = output["risk_level"].map(priorities)

    return output.sort_values(
        ["priority", "risk_score"],
        ascending=[True, False]
    )
