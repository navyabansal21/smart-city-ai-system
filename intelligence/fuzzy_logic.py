# Smart City AI System
# Fuzzy Logic Based Traffic Congestion Detection

def triangular_membership(value, left, peak, right):
    """
    Calculates the membership degree of a value
    in a triangular fuzzy set.
    Returns a value between 0 and 1.
    """

    if value <= left or value >= right:
        return 0.0

    if value == peak:
        return 1.0

    if value < peak:
        return (value - left) / (peak - left)

    return (right - value) / (right - peak)


def get_vehicle_memberships(vehicle_count):
    """
    Determines how strongly vehicle count belongs
    to Low, Medium, High, and Very High categories.
    """

    return {
        "low": triangular_membership(vehicle_count, 0, 20, 40),
        "medium": triangular_membership(vehicle_count, 20, 50, 80),
        "high": triangular_membership(vehicle_count, 60, 85, 110),
        "very_high": triangular_membership(vehicle_count, 90, 120, 150),
    }


def get_speed_memberships(speed):
    """
    Determines how strongly traffic speed belongs
    to Low, Medium, and High categories.
    """

    return {
        "low": triangular_membership(speed, 0, 10, 25),
        "medium": triangular_membership(speed, 15, 35, 55),
        "high": triangular_membership(speed, 40, 60, 80),
    }


def detect_congestion(vehicle_count, average_speed):
    """
    Uses fuzzy rules to calculate traffic congestion.

    Inputs:
        vehicle_count: Number of vehicles detected
        average_speed: Average speed in km/h

    Output:
        Congestion score and congestion category
    """

    vehicles = get_vehicle_memberships(vehicle_count)
    speed = get_speed_memberships(average_speed)

    # Fuzzy rule base
    rules = [
        # Rule: High traffic + low speed = very high congestion
        (min(vehicles["high"], speed["low"]), 95),

        # Rule: Very high traffic + low speed = very high congestion
        (min(vehicles["very_high"], speed["low"]), 100),

        # Rule: Medium traffic + low speed = high congestion
        (min(vehicles["medium"], speed["low"]), 75),

        # Rule: High traffic + medium speed = high congestion
        (min(vehicles["high"], speed["medium"]), 70),

        # Rule: Medium traffic + medium speed = medium congestion
        (min(vehicles["medium"], speed["medium"]), 50),

        # Rule: Low traffic + low speed = medium congestion
        (min(vehicles["low"], speed["low"]), 45),

        # Rule: Low traffic + high speed = low congestion
        (min(vehicles["low"], speed["high"]), 15),

        # Rule: Medium traffic + high speed = low congestion
        (min(vehicles["medium"], speed["high"]), 25),

        # Rule: High traffic + high speed = medium congestion
        (min(vehicles["high"], speed["high"]), 40),
    ]

    total_activation = sum(strength for strength, _ in rules)

    # Avoid division by zero
    if total_activation == 0:
        congestion_score = 0

    else:
        weighted_sum = sum(
            strength * output
            for strength, output in rules
        )

        congestion_score = weighted_sum / total_activation

    # Determine congestion category
    if congestion_score < 30:
        category = "LOW"

    elif congestion_score < 50:
        category = "MEDIUM"

    elif congestion_score < 75:
        category = "HIGH"

    else:
        category = "VERY HIGH"

    return {
        "score": round(congestion_score, 2),
        "category": category,
        "vehicle_count": vehicle_count,
        "average_speed": average_speed,
    }


# Test the system
if __name__ == "__main__":

    result = detect_congestion(
        vehicle_count=90,
        average_speed=10
    )

    print("SMART CITY TRAFFIC ANALYSIS")
    print("---------------------------")
    print(f"Vehicles detected: {result['vehicle_count']}")
    print(f"Average speed: {result['average_speed']} km/h")
    print(f"Congestion score: {result['score']}/100")
    print(f"Congestion level: {result['category']}")