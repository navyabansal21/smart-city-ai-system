import heapq

from city.traffic_data import (
    get_vehicles,
    get_speed,
    get_confidence
)
from city.knowledge_base import get_emergency_vehicles
from intelligence.ai_engine import run_smart_city_ai


def get_road_key(start, end):
    return f"{start}-{end}"


def get_reverse_road_key(start, end):
    return f"{end}-{start}"


def get_traffic_data(start, end):
    road = get_road_key(start, end)

    vehicles = get_vehicles(road)
    speed = get_speed(road)
    confidence = get_confidence(road)

    if vehicles == 0:
        road = get_reverse_road_key(start, end)

        vehicles = get_vehicles(road)
        speed = get_speed(road)
        confidence = get_confidence(road)

    return vehicles, speed, confidence


def analyze_road(start, end, emergency_vehicle=None):
    vehicles, speed, confidence = get_traffic_data(start, end)

    result = run_smart_city_ai(
        vehicle_count=vehicles,
        average_speed=speed,
        sensor_confidence=confidence,
        emergency_vehicle=emergency_vehicle
    )

    return result


def get_traffic_penalty(start, end):
    result = analyze_road(start, end)

    traffic = result["traffic_analysis"]

    if traffic["score"] is None:
        return 20

    return traffic["score"] / 10


def get_uncertainty_penalty(start, end):
    result = analyze_road(start, end)

    sensor_status = result["sensor_analysis"]["status"]

    if sensor_status == "INVALID":
        return 20

    if sensor_status == "UNCERTAIN":
        return 10

    return 0


def calculate_cost(graph, start, end):
    distance = graph[start][end]["weight"]

    traffic_penalty = get_traffic_penalty(
        start,
        end
    )

    uncertainty_penalty = get_uncertainty_penalty(
        start,
        end
    )

    return (
        distance
        + traffic_penalty
        + uncertainty_penalty
    )


def optimize_route(graph, start, goal):
    priority_queue = [
        (0, start, [start])
    ]

    visited = set()

    while priority_queue:

        cost, current, path = heapq.heappop(
            priority_queue
        )

        if current == goal:
            return path, round(cost, 2)

        if current in visited:
            continue

        visited.add(current)

        for neighbour in graph.neighbors(current):

            if neighbour in visited:
                continue

            road_cost = calculate_cost(
                graph,
                current,
                neighbour
            )

            heapq.heappush(
                priority_queue,
                (
                    cost + road_cost,
                    neighbour,
                    path + [neighbour]
                )
            )

    return None


def get_emergency_priority(vehicle_type):
    vehicles = get_emergency_vehicles()

    for vehicle, data in vehicles.items():

        if data["type"] == vehicle_type:
            return data["priority"]

    return 0


def get_emergency_name(vehicle_type):
    names = {
        "ambulance": "Ambulance",
        "fire_truck": "Fire Truck",
        "police": "Police"
    }

    return names.get(
        vehicle_type,
        vehicle_type
    )


def emergency_route(
    graph,
    vehicle_type,
    start,
    goal
):
    emergency_name = get_emergency_name(
        vehicle_type
    )

    priority = get_emergency_priority(
        vehicle_type
    )

    priority_queue = [
        (0, start, [start])
    ]

    visited = set()

    while priority_queue:

        cost, current, path = heapq.heappop(
            priority_queue
        )

        if current == goal:

            final_cost = round(cost, 2)

            ai_result = run_smart_city_ai(
                vehicle_count=0,
                average_speed=50,
                sensor_confidence=1.0,
                emergency_vehicle=emergency_name
            )

            return {
                "vehicle": emergency_name,
                "priority": priority,
                "route": path,
                "cost": final_cost,
                "decision": ai_result["decision"]["decision"],
                "action": ai_result["decision"]["action"],
                "priority_level": ai_result["decision"]["priority"],
                "explanation": ai_result["explanation"]
            }

        if current in visited:
            continue

        visited.add(current)

        for neighbour in graph.neighbors(current):

            if neighbour in visited:
                continue

            road_result = analyze_road(
                current,
                neighbour,
                emergency_name
            )

            traffic = road_result["traffic_analysis"]
            sensor = road_result["sensor_analysis"]

            distance = graph[current][neighbour]["weight"]

            if traffic["score"] is None:
                traffic_penalty = 20
            else:
                traffic_penalty = (
                    traffic["score"] / 10
                )

            if sensor["status"] == "INVALID":
                uncertainty_penalty = 20

            elif sensor["status"] == "UNCERTAIN":
                uncertainty_penalty = 10

            else:
                uncertainty_penalty = 0

            road_cost = (
                distance
                + traffic_penalty
                + uncertainty_penalty
            )

            heapq.heappush(
                priority_queue,
                (
                    cost + road_cost,
                    neighbour,
                    path + [neighbour]
                )
            )

    return None