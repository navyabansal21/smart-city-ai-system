# Smart City AI System
# Rule-Based Expert System for Traffic Signal Decisions


def make_decision(
    congestion_level,
    emergency_vehicle=None,
    sensor_status="RELIABLE"
):
    """
    Makes traffic signal decisions using predefined AI rules.

    Parameters:
        congestion_level: LOW, MEDIUM, HIGH, VERY HIGH
        emergency_vehicle: None, Ambulance, Fire Truck, Police
        sensor_status: RELIABLE, UNCERTAIN, INVALID

    Returns:
        Decision, signal action, and explanation.
    """

    # Rule 1: Invalid sensor data
    if sensor_status == "INVALID":

        return {
            "decision": "NORMAL SIGNAL OPERATION",
            "action": "Maintain safe default signal timing",
            "priority": "NONE",
            "explanation": (
                "Sensor data is invalid. "
                "The system avoids making decisions using unreliable data."
            )
        }

    # Rule 2: Emergency vehicle priority
    if emergency_vehicle is not None:

        emergency_priorities = {
            "Fire Truck": 1,
            "Ambulance": 2,
            "Police": 3
        }

        if emergency_vehicle not in emergency_priorities:

            return {
                "decision": "NORMAL SIGNAL OPERATION",
                "action": "Maintain normal signal timing",
                "priority": "NONE",
                "explanation": "Unknown emergency vehicle type."
            }

        priority = emergency_priorities[emergency_vehicle]

        # Higher priority emergency
        if priority == 1:

            return {
                "decision": "EMERGENCY PRIORITY",
                "action": "GREEN SIGNAL FOR FIRE TRUCK",
                "priority": "HIGH",
                "explanation": (
                    "Fire trucks receive the highest priority "
                    "to reduce emergency response time."
                )
            }

        elif priority == 2:

            return {
                "decision": "EMERGENCY PRIORITY",
                "action": "GREEN SIGNAL FOR AMBULANCE",
                "priority": "HIGH",
                "explanation": (
                    "An ambulance is detected. "
                    "The signal is adjusted to provide a clear route."
                )
            }

        elif priority == 3:

            return {
                "decision": "EMERGENCY PRIORITY",
                "action": "GREEN SIGNAL FOR POLICE",
                "priority": "MEDIUM",
                "explanation": (
                    "Police vehicles receive emergency signal priority."
                )
            }

    # Rule 3: Uncertain sensor data
    if sensor_status == "UNCERTAIN":

        return {
            "decision": "CAUTIOUS OPERATION",
            "action": "Use conservative signal timing",
            "priority": "LOW",
            "explanation": (
                "Sensor confidence is low. "
                "The system avoids aggressive signal adjustments."
            )
        }

    # Rule 4: Very high congestion
    if congestion_level == "VERY HIGH":

        return {
            "decision": "CONGESTION CONTROL",
            "action": "Increase green time for congested road",
            "priority": "HIGH",
            "explanation": (
                "Very high congestion detected. "
                "Green signal duration is increased to reduce traffic buildup."
            )
        }

    # Rule 5: High congestion
    elif congestion_level == "HIGH":

        return {
            "decision": "CONGESTION CONTROL",
            "action": "Moderately increase green signal duration",
            "priority": "MEDIUM",
            "explanation": (
                "High congestion detected. "
                "The signal timing is adjusted to improve traffic flow."
            )
        }

    # Rule 6: Medium congestion
    elif congestion_level == "MEDIUM":

        return {
            "decision": "NORMAL TRAFFIC MANAGEMENT",
            "action": "Maintain balanced signal timing",
            "priority": "NORMAL",
            "explanation": (
                "Moderate traffic is detected. "
                "Balanced signal timing is maintained."
            )
        }

    # Rule 7: Low congestion
    elif congestion_level == "LOW":

        return {
            "decision": "NORMAL TRAFFIC MANAGEMENT",
            "action": "Maintain normal signal timing",
            "priority": "LOW",
            "explanation": (
                "Traffic flow is smooth. "
                "Normal signal timing is sufficient."
            )
        }

    # Rule 8: Unknown congestion category
    else:

        return {
            "decision": "SAFE DEFAULT",
            "action": "Maintain normal signal timing",
            "priority": "LOW",
            "explanation": "Unknown congestion level."
        }


# Testing the Expert System
if __name__ == "__main__":

    test_cases = [

        {
            "congestion_level": "VERY HIGH",
            "emergency_vehicle": None,
            "sensor_status": "RELIABLE"
        },

        {
            "congestion_level": "HIGH",
            "emergency_vehicle": "Ambulance",
            "sensor_status": "RELIABLE"
        },

        {
            "congestion_level": "MEDIUM",
            "emergency_vehicle": "Fire Truck",
            "sensor_status": "RELIABLE"
        },

        {
            "congestion_level": "LOW",
            "emergency_vehicle": None,
            "sensor_status": "UNCERTAIN"
        },

        {
            "congestion_level": "HIGH",
            "emergency_vehicle": None,
            "sensor_status": "INVALID"
        },

        {
            "congestion_level": "LOW",
            "emergency_vehicle": "Police",
            "sensor_status": "RELIABLE"
        }
    ]

    for index, test in enumerate(test_cases, start=1):

        result = make_decision(**test)

        print(f"\nTEST CASE {index}")
        print("=" * 40)

        print(f"Congestion: {test['congestion_level']}")
        print(f"Emergency: {test['emergency_vehicle']}")
        print(f"Sensor: {test['sensor_status']}")

        print(f"\nDecision: {result['decision']}")
        print(f"Action: {result['action']}")
        print(f"Priority: {result['priority']}")
        print(f"Explanation: {result['explanation']}")