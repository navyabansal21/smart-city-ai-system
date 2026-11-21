# SMART CITY AI SYSTEM - INTEGRATED DEMO

from city.city_graph import create_city_graph
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.astar import astar
from algorithms.route_optimizer import optimize_route, emergency_route
from visualization.city_map import draw_city_map

from intelligence.ai_engine import run_smart_city_ai


def show_route_planning():
    print("\n" + "=" * 60)
    print("SMART CITY - ROUTE PLANNING")
    print("=" * 60)

    graph = create_city_graph()
    start = "A"
    goal = "F"

    print(f"\nRoute: {start} -> {goal}")

    print("\nBFS:", bfs(graph, start, goal))
    print("DFS:", dfs(graph, start, goal))
    print("UCS:", ucs(graph, start, goal))
    print("A*:", astar(graph, start, goal))

    result = optimize_route(graph, start, goal)

    print("\nTRAFFIC-AWARE ROUTE")

    if result:
        route, cost = result
        print("Route:", " -> ".join(route))
        print("Total Cost:", round(cost, 2))

    print("\nEMERGENCY VEHICLE ROUTE")

    emergency = emergency_route(
        graph,
        "ambulance",
        start,
        goal
    )

    if emergency:
        print("Vehicle:", emergency["vehicle"])
        print("Route:", " -> ".join(emergency["route"]))
        print("Priority:", emergency["priority"])
        print("Cost:", emergency["cost"])

    print("\nDisplaying City Map...")
    draw_city_map(graph, route if result else None)


def show_ai_scenario(name, vehicle_count, speed, confidence,
                     emergency=None, demand=None):

    print("\n" + "=" * 60)
    print(f"AI SCENARIO: {name}")
    print("=" * 60)

    result = run_smart_city_ai(
        vehicle_count=vehicle_count,
        average_speed=speed,
        sensor_confidence=confidence,
        emergency_vehicle=emergency,
        traffic_demand=demand
    )

    print("\nSENSOR STATUS:",
          result["sensor_analysis"]["status"])

    print("SENSOR RELIABILITY:",
          result["sensor_analysis"]["reliability"])

    print("\nCONGESTION:",
          result["traffic_analysis"]["category"])

    print("CONGESTION SCORE:",
          result["traffic_analysis"]["score"])

    print("\nAI DECISION:",
          result["decision"]["decision"])

    print("ACTION:",
          result["decision"]["action"])

    print("PRIORITY:",
          result["decision"]["priority"])

    if result["signal_optimization"]:

        print("\nOPTIMIZED SIGNAL TIMINGS")

        for road, timing in result["signal_optimization"]["signal_timings"].items():
            print(f"{road}: {timing} seconds")

        print("Fitness Score:",
              round(result["signal_optimization"]["fitness_score"], 4))

    if result["fairness_analysis"]:

        print("\nFAIRNESS INDEX:",
              result["fairness_analysis"]["fairness_index"])

        print("FAIRNESS LEVEL:",
              result["fairness_analysis"]["fairness_level"])

        print("RECOMMENDATION:",
              result["fairness_analysis"]["recommendation"])

    print("\nEXPLAINABLE AI:")

    for explanation in result["explanation"]:
        print("-", explanation)


def main():

    print("\n")
    print("*" * 60)
    print("       SMART CITY AI SYSTEM")
    print("*" * 60)

    # PART 1: ROUTE PLANNING
    show_route_planning()

    # PART 2: AI INTELLIGENCE
    show_ai_scenario(
        name="Normal Traffic",
        vehicle_count=25,
        speed=50,
        confidence=0.95
    )

    show_ai_scenario(
        name="Heavy Congestion",
        vehicle_count=100,
        speed=10,
        confidence=0.95
    )

    show_ai_scenario(
        name="Ambulance Emergency",
        vehicle_count=80,
        speed=15,
        confidence=0.95,
        emergency="Ambulance"
    )

    show_ai_scenario(
        name="Signal Optimization",
        vehicle_count=80,
        speed=15,
        confidence=0.95,
        demand=[80, 60, 100, 40]
    )

    print("\n" + "*" * 60)
    print("       SMART CITY AI DEMO COMPLETED")
    print("*" * 60)


if __name__ == "__main__":
    main()