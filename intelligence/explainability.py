# Smart City AI System
# Explainable AI (XAI) Module


def explain_ai_decision(result):
    """
    Converts AI decisions into human-readable explanations.
    """

    sensor = result["sensor_analysis"]
    traffic = result["traffic_analysis"]
    decision = result["decision"]

    explanations = []

    # Explain sensor reliability
    if sensor["status"] == "RELIABLE":

        explanations.append(
            "The sensor readings are considered reliable "
            "because their confidence level is sufficient."
        )

    elif sensor["status"] == "UNCERTAIN":

        explanations.append(
            "The sensor readings have low confidence. "
            "Therefore, the system operates cautiously."
        )

    elif sensor["status"] == "INVALID":

        explanations.append(
            "The sensor data contains invalid readings. "
            "The system avoids relying on this data."
        )

    # Explain congestion
    
    if sensor["status"] == "INVALID":
        explanations.append(
        "Congestion could not be reliably determined "
        "because the sensor data is invalid."
    )
    elif sensor["status"] == "UNCERTAIN":
        
        explanations.append(
        f"The sensor readings suggest {traffic['category']} congestion, "
        "but this estimate has low confidence and should not be "
        "treated as fully reliable."
    )
    else:
        
        if traffic["category"] == "LOW":
            explanations.append(
            "Traffic congestion is low, indicating "
            "relatively smooth traffic flow."
        )
        
        elif traffic["category"] == "MEDIUM":
            
            explanations.append(
            "Moderate congestion is detected. "
            "Balanced traffic signal timings are appropriate."
        )
        
        elif traffic["category"] == "HIGH":
            
            explanations.append(
            "High congestion is detected. "
            "The system recommends increasing green time "
            "for the affected road."
        )
        
        elif traffic["category"] == "VERY HIGH":
            
            explanations.append(
            "Very high congestion is detected. "
            "The system recommends prioritizing "
            "the congested road."
        )
        
        elif traffic["category"] == "UNKNOWN":
            
            explanations.append(
            "Congestion could not be reliably determined."
        )
    # Explain emergency priority
    emergency = result["system_summary"]["emergency_vehicle"]

    if emergency:

        explanations.append(
            f"{emergency} was detected. "
            "Emergency vehicle priority rules were applied."
        )

    # Explain final action
    explanations.append(
        f"Final system action: {decision['action']}."
    )

        # Explain signal optimization
    signal_optimization = result.get("signal_optimization")

    if signal_optimization is not None:

        timings = signal_optimization["signal_timings"]

        explanations.append(
            "Optimized traffic signal timings were calculated "
            "using the Genetic Algorithm: "
            f"North {timings['North']} seconds, "
            f"South {timings['South']} seconds, "
            f"East {timings['East']} seconds, and "
            f"West {timings['West']} seconds."
        )

        explanations.append(
            f"The signal optimization achieved a fitness score "
            f"of {signal_optimization['fitness_score']:.4f}."
        )

    # Explain fairness analysis
    fairness_analysis = result.get("fairness_analysis")

    if fairness_analysis is not None:

        explanations.append(
            f"The signal allocation has a fairness index of "
            f"{fairness_analysis['fairness_index']}, "
            f"classified as {fairness_analysis['fairness_level']}."
        )

        if fairness_analysis["underserved_roads"]:

            road_names = ["North", "South", "East", "West"]

            underserved = [
                road_names[index]
                for index in fairness_analysis["underserved_roads"]
            ]

            explanations.append(
                "The following roads were identified as "
                "comparatively underserved: "
                + ", ".join(underserved)
                + "."
            )

        explanations.append(
            fairness_analysis["recommendation"]
        )

    return explanations


def display_explanation(result):

    explanations = explain_ai_decision(result)

    print("\nEXPLAINABLE AI ANALYSIS")
    print("=" * 50)

    for index, explanation in enumerate(
        explanations,
        start=1
    ):

        print(f"{index}. {explanation}")


# ------------------------------------------
# TESTING
# ------------------------------------------

if __name__ == "__main__":

    from ai_engine import run_smart_city_ai

    scenarios = [

        {
            "name": "Heavy Congestion",
            "vehicle_count": 100,
            "average_speed": 10,
            "sensor_confidence": 0.95,
            "emergency_vehicle": None
        },

        {
            "name": "Ambulance Emergency",
            "vehicle_count": 80,
            "average_speed": 15,
            "sensor_confidence": 0.95,
            "emergency_vehicle": "Ambulance"
        },

        {
            "name": "Unreliable Sensor",
            "vehicle_count": 90,
            "average_speed": 10,
            "sensor_confidence": 0.40,
            "emergency_vehicle": None
        }
    ]

    for scenario in scenarios:

        print("\n" + "#" * 60)

        print(f"SCENARIO: {scenario['name']}")

        print("#" * 60)

        result = run_smart_city_ai(
            vehicle_count=scenario["vehicle_count"],
            average_speed=scenario["average_speed"],
            sensor_confidence=scenario["sensor_confidence"],
            emergency_vehicle=scenario["emergency_vehicle"]
        )

        display_explanation(result)