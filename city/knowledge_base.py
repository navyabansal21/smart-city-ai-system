CITY_DATA = {
    "intersections": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F"
    ],

    "roads": {
        "A": {
            "B": 4,
            "C": 2
        },
        "B": {
            "A": 4,
            "D": 5,
            "E": 10
        },
        "C": {
            "A": 2,
            "D": 3,
            "E": 8
        },
        "D": {
            "B": 5,
            "C": 3,
            "E": 2,
            "F": 6
        },
        "E": {
            "B": 10,
            "C": 8,
            "D": 2,
            "F": 3
        },
        "F": {
            "D": 6,
            "E": 3
        }
    },

    "hospitals": {
        "H1": {
            "location": "F",
            "name": "City General Hospital"
        }
    },

    "emergency_vehicles": {
        "ambulance_1": {
            "type": "ambulance",
            "location": "A",
            "priority": 2
        },
        "fire_truck_1": {
            "type": "fire_truck",
            "location": "B",
            "priority": 3
        },
        "police_1": {
            "type": "police",
            "location": "C",
            "priority": 1
        }
    },

    "traffic": {
        "A-B": {
            "vehicles": 40,
            "speed": 35,
            "confidence": 0.95
        },
        "A-C": {
            "vehicles": 20,
            "speed": 45,
            "confidence": 0.90
        },
        "B-D": {
            "vehicles": 70,
            "speed": 20,
            "confidence": 0.85
        },
        "B-E": {
            "vehicles": 80,
            "speed": 15,
            "confidence": 0.80
        },
        "C-D": {
            "vehicles": 30,
            "speed": 40,
            "confidence": 0.95
        },
        "C-E": {
            "vehicles": 50,
            "speed": 30,
            "confidence": 0.90
        },
        "D-E": {
            "vehicles": 25,
            "speed": 45,
            "confidence": 0.95
        },
        "D-F": {
            "vehicles": 60,
            "speed": 25,
            "confidence": 0.85
        },
        "E-F": {
            "vehicles": 20,
            "speed": 40,
            "confidence": 0.90
        }
    }
}


def get_city_data():
    return CITY_DATA


def get_intersections():
    return CITY_DATA["intersections"]


def get_roads():
    return CITY_DATA["roads"]


def get_hospitals():
    return CITY_DATA["hospitals"]


def get_emergency_vehicles():
    return CITY_DATA["emergency_vehicles"]


def get_traffic_data():
    return CITY_DATA["traffic"]