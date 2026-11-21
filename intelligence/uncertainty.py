# Smart City AI System
# Sensor Uncertainty Handling Module

def validate_sensor_data(vehicle_count, average_speed, confidence):
    """
    Validates traffic sensor data and evaluates its reliability.

    Parameters:
        vehicle_count: Number of detected vehicles
        average_speed: Average speed in km/h
        confidence: Sensor confidence between 0 and 1

    Returns:
        Dictionary containing validation results.
    """

    issues = []

    # Check vehicle count
    if vehicle_count < 0:
        issues.append("Invalid vehicle count")

    # Check speed
    if average_speed < 0 or average_speed > 120:
        issues.append("Invalid speed reading")

    # Check confidence
    if confidence < 0 or confidence > 1:
        issues.append("Invalid confidence value")

    # Determine sensor reliability
    if confidence >= 0.8:
        reliability = "HIGH"

    elif confidence >= 0.6:
        reliability = "MEDIUM"

    else:
        reliability = "LOW"

    # Determine whether the reading should be trusted
    if issues:
        status = "INVALID"

    elif confidence < 0.6:
        status = "UNCERTAIN"

    else:
        status = "RELIABLE"

    return {
        "vehicle_count": vehicle_count,
        "average_speed": average_speed,
        "confidence": confidence,
        "reliability": reliability,
        "status": status,
        "issues": issues
    }


def handle_uncertainty(sensor_data):
    """
    Handles uncertain sensor readings.

    Low-confidence readings are flagged instead of
    being blindly accepted by the AI system.
    """

    result = validate_sensor_data(
        vehicle_count=sensor_data["vehicle_count"],
        average_speed=sensor_data["average_speed"],
        confidence=sensor_data["confidence"]
    )

    if result["status"] == "INVALID":

        result["decision"] = "REJECT SENSOR DATA"

    elif result["status"] == "UNCERTAIN":

        result["decision"] = "USE WITH CAUTION"

    else:

        result["decision"] = "ACCEPT SENSOR DATA"

    return result


# Testing the module
if __name__ == "__main__":

    test_sensors = [
        {
            "vehicle_count": 45,
            "average_speed": 35,
            "confidence": 0.95
        },

        {
            "vehicle_count": 90,
            "average_speed": 10,
            "confidence": 0.45
        },

        {
            "vehicle_count": 30,
            "average_speed": 50,
            "confidence": 0.70
        },

        {
            "vehicle_count": -5,
            "average_speed": 30,
            "confidence": 0.90
        }
    ]

    for index, sensor in enumerate(test_sensors, start=1):

        result = handle_uncertainty(sensor)

        print(f"\nSENSOR TEST {index}")
        print("------------------")
        print(f"Vehicles: {result['vehicle_count']}")
        print(f"Speed: {result['average_speed']} km/h")
        print(f"Confidence: {result['confidence']}")
        print(f"Reliability: {result['reliability']}")
        print(f"Status: {result['status']}")
        print(f"Decision: {result['decision']}")

        if result["issues"]:
            print(f"Issues: {result['issues']}")