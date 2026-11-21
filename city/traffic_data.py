from city.knowledge_base import get_traffic_data


def get_road_traffic(road):
    traffic_data = get_traffic_data()
    return traffic_data.get(road, {})


def get_vehicles(road):
    data = get_road_traffic(road)
    return data.get("vehicles", 0)


def get_speed(road):
    data = get_road_traffic(road)
    return data.get("speed", 0)


def get_confidence(road):
    data = get_road_traffic(road)
    return data.get("confidence", 0)


def display_traffic_data():
    traffic_data = get_traffic_data()

    for road, data in traffic_data.items():
        print(
            f"{road}: "
            f"Vehicles={data['vehicles']}, "
            f"Speed={data['speed']}, "
            f"Confidence={data['confidence']}"
        )