# Smart City AI System
# Fairness Analysis Module

def calculate_fairness(green_times, traffic_demand, waiting_times=None):
    """
    Evaluates fairness in traffic signal allocation.

    Parameters:
        green_times: Green signal time allocated to each road
        traffic_demand: Traffic demand for each road
        waiting_times: Optional waiting time for each road

    Returns:
        Fairness analysis report
    """

    if len(green_times) != len(traffic_demand):
        raise ValueError(
            "Green times and traffic demand must have equal length."
        )

    if any(time < 0 for time in green_times):
        raise ValueError("Green times cannot be negative.")

    if any(demand <= 0 for demand in traffic_demand):
        raise ValueError("Traffic demand must be greater than zero.")

    # Calculate green time received per unit of traffic demand
    service_ratios = []

    for green_time, demand in zip(
        green_times,
        traffic_demand
    ):

        ratio = green_time / demand

        service_ratios.append(ratio)

    # Jain's Fairness Index
    numerator = sum(service_ratios) ** 2

    denominator = (
        len(service_ratios)
        * sum(ratio ** 2 for ratio in service_ratios)
    )

    fairness_index = numerator / denominator

    # Fairness classification
    if fairness_index >= 0.90:

        fairness_level = "HIGH"

    elif fairness_index >= 0.75:

        fairness_level = "MODERATE"

    else:

        fairness_level = "LOW"

    # Identify roads receiving comparatively less service
    average_service = sum(service_ratios) / len(service_ratios)

    underserved_roads = []

    for index, ratio in enumerate(service_ratios):

        if ratio < average_service * 0.75:

            underserved_roads.append(index)

    # Waiting time analysis
    waiting_analysis = None

    if waiting_times is not None:

        if len(waiting_times) != len(green_times):

            raise ValueError(
                "Waiting times must match the number of roads."
            )

        maximum_wait = max(waiting_times)

        minimum_wait = min(waiting_times)

        average_wait = sum(waiting_times) / len(waiting_times)

        waiting_analysis = {
            "maximum_wait": maximum_wait,
            "minimum_wait": minimum_wait,
            "average_wait": round(average_wait, 2),
            "wait_difference": maximum_wait - minimum_wait
        }

    # Generate recommendation
    if fairness_level == "LOW":

        recommendation = (
            "Signal allocation is unfair. "
            "Consider redistributing green time."
        )

    elif fairness_level == "MODERATE":

        recommendation = (
            "Fairness is acceptable but could be improved."
        )

    else:

        recommendation = (
            "Signal allocation is reasonably fair."
        )

    return {
        "fairness_index": round(fairness_index, 3),
        "fairness_level": fairness_level,
        "service_ratios": service_ratios,
        "underserved_roads": underserved_roads,
        "waiting_analysis": waiting_analysis,
        "recommendation": recommendation
    }


# ------------------------------------------
# TESTING
# ------------------------------------------

if __name__ == "__main__":

    roads = ["North", "South", "East", "West"]

    # Scenario 1: Fair allocation
    print("\nSCENARIO 1: FAIR ALLOCATION")
    print("=" * 50)

    result = calculate_fairness(
        green_times=[25, 25, 25, 25],
        traffic_demand=[50, 50, 50, 50],
        waiting_times=[30, 32, 28, 31]
    )

    print(f"Fairness Index: {result['fairness_index']}")
    print(f"Fairness Level: {result['fairness_level']}")
    print(f"Recommendation: {result['recommendation']}")

    # Scenario 2: Unequal allocation
    print("\nSCENARIO 2: UNEQUAL ALLOCATION")
    print("=" * 50)

    result = calculate_fairness(
        green_times=[40, 30, 20, 10],
        traffic_demand=[50, 50, 50, 50],
        waiting_times=[15, 30, 50, 80]
    )

    print(f"Fairness Index: {result['fairness_index']}")
    print(f"Fairness Level: {result['fairness_level']}")

    print("\nUnderserved Roads:")

    for road_index in result["underserved_roads"]:

        print(f"- {roads[road_index]}")

    print("\nWaiting Time Analysis:")

    print(result["waiting_analysis"])

    print(f"\nRecommendation: {result['recommendation']}")

    # Scenario 3: Different traffic demands
    print("\nSCENARIO 3: DEMAND-BASED ALLOCATION")
    print("=" * 50)

    result = calculate_fairness(
        green_times=[40, 30, 20, 10],
        traffic_demand=[100, 75, 50, 25],
        waiting_times=[20, 25, 30, 35]
    )

    print(f"Fairness Index: {result['fairness_index']}")
    print(f"Fairness Level: {result['fairness_level']}")
    print(f"Recommendation: {result['recommendation']}")