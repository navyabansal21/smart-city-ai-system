# Smart City AI System
# Integrated AI Decision Engine

from intelligence.fuzzy_logic import detect_congestion
from intelligence.uncertainty import handle_uncertainty
from intelligence.expert_system import make_decision
from intelligence.genetic_algorithm import optimize_traffic_signals
from intelligence.fairness import calculate_fairness
from intelligence.explainability import explain_ai_decision

def run_smart_city_ai(
    vehicle_count,
    average_speed,
    sensor_confidence,
    emergency_vehicle=None,
    traffic_demand=None
):
    """
    Integrates all AI intelligence modules.

    Pipeline:
    1. Sensor validation
    2. Uncertainty handling
    3. Fuzzy congestion detection
    4. Expert system decision-making
    5. Explainable AI output
    """

    # --------------------------------
    # STEP 1: Validate sensor readings
    # --------------------------------

    sensor_data = {
        "vehicle_count": vehicle_count,
        "average_speed": average_speed,
        "confidence": sensor_confidence
    }

    sensor_result = handle_uncertainty(sensor_data)

    sensor_status = sensor_result["status"]

    # --------------------------------
    # STEP 2: Detect congestion
    # --------------------------------

    if sensor_status == "INVALID":

        congestion_result = {
            "score": None,
            "category": "UNKNOWN"
        }

    else:

        congestion_result = detect_congestion(
            vehicle_count=vehicle_count,
            average_speed=average_speed
        )

    congestion_level = congestion_result["category"]

    # --------------------------------
    # STEP 3: Expert system decision
    # --------------------------------

    decision_result = make_decision(
        congestion_level=congestion_level,
        emergency_vehicle=emergency_vehicle,
        sensor_status=sensor_status
    )
    # --------------------------------
    # STEP 4: Optimize traffic signal timings
    # --------------------------------

    signal_optimization = None
    fairness_analysis = None

    if traffic_demand is not None:

        # Genetic Algorithm
        best_solution, best_fitness = optimize_traffic_signals(
            traffic_demand
        )

        signal_optimization = {
            "signal_timings": {
                "North": best_solution[0],
                "South": best_solution[1],
                "East": best_solution[2],
                "West": best_solution[3]
            },
            "fitness_score": best_fitness
        }

        # Fairness Analysis
        fairness_analysis = calculate_fairness(
            green_times=best_solution,
            traffic_demand=traffic_demand
        )

    # --------------------------------
    # STEP 5: Generate Explainable AI output
    # --------------------------------

    explanation = explain_ai_decision({
        "sensor_analysis": sensor_result,
        "traffic_analysis": congestion_result,
        "decision": decision_result,
        "signal_optimization": signal_optimization,
        "fairness_analysis": fairness_analysis,
        "system_summary": {
            "emergency_vehicle": emergency_vehicle
        }
    })

    # --------------------------------
    # STEP 6: Generate final AI output
    # --------------------------------

    return {
        "sensor_analysis": sensor_result,

        "traffic_analysis": congestion_result,

        "decision": decision_result,

        "signal_optimization": signal_optimization,

        "fairness_analysis": fairness_analysis,

        "explanation": explanation,

        "system_summary": {
            "congestion": congestion_level,
            "emergency_vehicle": emergency_vehicle,
            "sensor_reliability": sensor_result["reliability"],
            "final_action": decision_result["action"]
        }
    }


# --------------------------------
# TESTING THE INTEGRATED AI SYSTEM
# --------------------------------

if __name__ == "__main__":

    scenarios = [

        {
            "name": "Normal Traffic",
            "vehicle_count": 25,
            "average_speed": 50,
            "sensor_confidence": 0.95,
            "emergency_vehicle": None
        },

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
        },

        {
            "name": "Invalid Sensor Reading",
            "vehicle_count": -5,
            "average_speed": 20,
            "sensor_confidence": 0.95,
            "emergency_vehicle": None
        },

        {
            "name": "Signal Optimization",
            "vehicle_count": 80,
            "average_speed": 15,
            "sensor_confidence": 0.95,
            "emergency_vehicle": None,
            "traffic_demand": [80, 60, 100, 40]
        }
    ]

    for scenario in scenarios:

        print("\n" + "=" * 60)
        print(f"SCENARIO: {scenario['name']}")
        print("=" * 60)

        result = run_smart_city_ai(
            vehicle_count=scenario["vehicle_count"],
            average_speed=scenario["average_speed"],
            sensor_confidence=scenario["sensor_confidence"],
            emergency_vehicle=scenario["emergency_vehicle"],
            traffic_demand=scenario.get("traffic_demand")
        )

        print("\nSENSOR ANALYSIS")
        print("-" * 30)

        print(
            f"Reliability: "
            f"{result['sensor_analysis']['reliability']}"
        )

        print(
            f"Status: "
            f"{result['sensor_analysis']['status']}"
        )

        print("\nTRAFFIC ANALYSIS")
        print("-" * 30)

        print(
            f"Congestion Score: "
            f"{result['traffic_analysis']['score']}"
        )

        print(
            f"Congestion Level: "
            f"{result['traffic_analysis']['category']}"
        )

        print("\nAI DECISION")
        print("-" * 30)

        print(
            f"Decision: "
            f"{result['decision']['decision']}"
        )

        print(
            f"Action: "
            f"{result['decision']['action']}"
        )

        print(
            f"Priority: "
            f"{result['decision']['priority']}"
        )

        print(
            f"Explanation: "
            f"{result['decision']['explanation']}"
        )

        if result["signal_optimization"] is not None:

            print("\nSIGNAL OPTIMIZATION")
            print("-" * 30)

            timings = result["signal_optimization"]["signal_timings"]

            print(f"North: {timings['North']} seconds")
            print(f"South: {timings['South']} seconds")
            print(f"East: {timings['East']} seconds")
            print(f"West: {timings['West']} seconds")

            print(
                f"Fitness Score: "
                f"{result['signal_optimization']['fitness_score']:.4f}"
            )

        if result["fairness_analysis"] is not None:

            print("\nFAIRNESS ANALYSIS")
            print("-" * 30)

            fairness = result["fairness_analysis"]

            print(
                f"Fairness Index: "
                f"{fairness['fairness_index']}"
            )

            print(
                f"Fairness Level: "
                f"{fairness['fairness_level']}"
            )

            print(
                f"Underserved Roads: "
                f"{fairness['underserved_roads']}"
            )

            print(
                f"Recommendation: "
                f"{fairness['recommendation']}"
            )

        print("\nEXPLAINABLE AI ANALYSIS")
        print("-" * 30)

        for index, explanation in enumerate(
            result["explanation"],
            start=1
        ):
            print(f"{index}. {explanation}")