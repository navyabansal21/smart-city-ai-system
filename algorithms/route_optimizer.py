import heapq
from city.traffic_data import get_vehicles, get_speed
from city.knowledge_base import get_emergency_vehicles


def get_road_key(start, end):
    return f"{start}-{end}"


def get_reverse_road_key(start, end):
    return f"{end}-{start}"


def get_traffic_penalty(start, end):
    road = get_road_key(start, end)
    vehicles = get_vehicles(road)

    if vehicles == 0:
        road = get_reverse_road_key(start, end)
        vehicles = get_vehicles(road)

    return vehicles / 10


def calculate_cost(graph, start, end):
    distance = graph[start][end]["weight"]
    traffic_penalty = get_traffic_penalty(start, end)

    return distance + traffic_penalty


def optimize_route(graph, start, goal):
    priority_queue = [(0, start, [start])]
    visited = set()

    while priority_queue:
        cost, current, path = heapq.heappop(priority_queue)

        if current == goal:
            return path, cost

        if current in visited:
            continue

        visited.add(current)

        for neighbour in graph.neighbors(current):
            if neighbour not in visited:
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


def emergency_route(graph, vehicle_type, start, goal):
    priority = get_emergency_priority(vehicle_type)

    result = optimize_route(graph, start, goal)

    if result is None:
        return None

    path, cost = result

    emergency_bonus = priority * 0.5
    emergency_cost = max(0, cost - emergency_bonus)

    return {
        "vehicle": vehicle_type,
        "priority": priority,
        "route": path,
        "cost": emergency_cost,
        "reasons": [
            "Lower traffic cost",
            "Traffic-aware route selected",
            "Emergency priority applied"
        ]
    }