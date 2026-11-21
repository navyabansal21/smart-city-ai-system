import matplotlib.pyplot as plt
import networkx as nx

from city.traffic_data import (
    get_vehicles,
    get_speed,
    get_confidence
)

from intelligence.fuzzy_logic import detect_congestion


def get_road_data(start, end):
    road = f"{start}-{end}"

    vehicles = get_vehicles(road)
    speed = get_speed(road)
    confidence = get_confidence(road)

    if vehicles == 0:
        road = f"{end}-{start}"

        vehicles = get_vehicles(road)
        speed = get_speed(road)
        confidence = get_confidence(road)

    return vehicles, speed, confidence


def get_junction_data(graph, node):
    neighbours = list(
        graph.neighbors(node)
    )

    vehicle_values = []
    speed_values = []

    for neighbour in neighbours:

        vehicles, speed, confidence = get_road_data(
            node,
            neighbour
        )

        if vehicles > 0:
            vehicle_values.append(vehicles)

        if speed > 0:
            speed_values.append(speed)

    if vehicle_values:
        vehicle_count = int(
            sum(vehicle_values) / len(vehicle_values)
        )
    else:
        vehicle_count = 0

    if speed_values:
        average_speed = int(
            sum(speed_values) / len(speed_values)
        )
    else:
        average_speed = 0

    congestion = detect_congestion(
        vehicle_count,
        average_speed
    )

    return {
        "vehicles": vehicle_count,
        "speed": average_speed,
        "congestion": congestion
    }


def get_signal_color(category):
    if category == "LOW":
        return "#20a85a"

    if category == "MEDIUM":
        return "#f2c94c"

    if category == "HIGH":
        return "#f2994a"

    if category == "VERY HIGH":
        return "#eb5757"

    return "#7f8c8d"


def get_signal_name(category):
    if category == "LOW":
        return "LOW"

    if category == "MEDIUM":
        return "MEDIUM"

    if category == "HIGH":
        return "HIGH"

    if category == "VERY HIGH":
        return "HIGH"

    return "UNKNOWN"


def draw_road(
    ax,
    start_position,
    end_position,
    is_route=False
):
    x1, y1 = start_position
    x2, y2 = end_position

    if is_route:

        ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=14,
            color="#ff6b6b",
            solid_capstyle="round",
            zorder=3
        )

        ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=6,
            color="#e63946",
            solid_capstyle="round",
            zorder=4
        )

    else:

        ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=14,
            color="#566573",
            solid_capstyle="round",
            zorder=1
        )

        ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=5,
            color="#dfe6e9",
            solid_capstyle="round",
            zorder=2
        )

        midpoint_x = (x1 + x2) / 2
        midpoint_y = (y1 + y2) / 2

        ax.scatter(
            midpoint_x,
            midpoint_y,
            s=25,
            color="white",
            zorder=5
        )


def draw_junction_card(
    ax,
    node,
    position,
    data,
    offset
):
    x, y = position

    signal_color = get_signal_color(
        data["congestion"]["category"]
    )

    category = get_signal_name(
        data["congestion"]["category"]
    )

    score = data["congestion"]["score"]

    if score is None:
        score_text = "N/A"
    else:
        score_text = f"{score:.0f}"

    card_text = (
        f"●  {node} Junction\n"
        f"Vehicles: {data['vehicles']}\n"
        f"Speed: {data['speed']} km/h\n"
        f"Congestion: {category}\n"
        f"Score: {score_text}"
    )

    ax.annotate(
        card_text,
        xy=(x, y),
        xytext=offset,
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
        color="#1f2933",
        ha="center",
        va="center",
        bbox=dict(
            boxstyle="round,pad=0.8",
            facecolor="white",
            edgecolor="#d6dce1",
            linewidth=1.2,
            alpha=0.97
        ),
        arrowprops=dict(
            arrowstyle="-",
            color="#aab4bd",
            linewidth=1
        ),
        zorder=10
    )

    ax.scatter(
        x,
        y,
        s=600,
        color="white",
        edgecolor=signal_color,
        linewidth=5,
        zorder=8
    )

    ax.scatter(
        x,
        y,
        s=260,
        color=signal_color,
        edgecolor="white",
        linewidth=3,
        zorder=9
    )

    ax.text(
        x,
        y,
        node,
        fontsize=12,
        fontweight="bold",
        color="white",
        ha="center",
        va="center",
        zorder=11
    )


def draw_city_map(graph, route=None):
    position = {
        "A": (1.5, 6.5),
        "B": (4.5, 7.0),
        "C": (4.0, 3.5),
        "D": (7.0, 5.5),
        "E": (8.5, 2.0),
        "F": (11.0, 3.5)
    }

    fig, ax = plt.subplots(
        figsize=(15, 9)
    )

    fig.patch.set_facecolor(
        "#f4f7f9"
    )

    ax.set_facecolor(
        "#eef2f5"
    )

    route_edges = set()

    if route:

        for start, end in zip(
            route,
            route[1:]
        ):
            route_edges.add(
                tuple(sorted((start, end)))
            )

    for start, end in graph.edges():

        edge = tuple(
            sorted((start, end))
        )

        draw_road(
            ax,
            position[start],
            position[end],
            edge in route_edges
        )

    for start, end in graph.edges():

        vehicles, speed, confidence = get_road_data(
            start,
            end
        )

        x1, y1 = position[start]
        x2, y2 = position[end]

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        label = (
            f"{vehicles} cars  |  "
            f"{speed} km/h"
        )

        ax.text(
            x,
            y + 0.25,
            label,
            fontsize=7.5,
            color="#34495e",
            ha="center",
            va="center",
            bbox=dict(
                boxstyle="round,pad=0.25",
                facecolor="white",
                edgecolor="#d5dadd",
                alpha=0.9
            ),
            zorder=6
        )

    junction_data = {}

    for node in graph.nodes():

        junction_data[node] = get_junction_data(
            graph,
            node
        )

    offsets = {
        "A": (0, 85),
        "B": (0, 85),
        "C": (-85, -65),
        "D": (0, 85),
        "E": (-15, -90),
        "F": (80, 10)
    }

    for node in graph.nodes():

        draw_junction_card(
            ax,
            node,
            position[node],
            junction_data[node],
            offsets.get(node, (0, 70))
        )

    ax.text(
        6,
        8.8,
        "SMART CITY TRAFFIC MAP",
        fontsize=24,
        fontweight="bold",
        color="#17202a",
        ha="center"
    )

    ax.text(
        6,
        8.35,
        "Real-Time Traffic Monitoring & Route Optimization",
        fontsize=11,
        color="#6b7785",
        ha="center"
    )

    if route:

        route_text = (
            "OPTIMIZED ROUTE: "
            + " → ".join(route)
        )

        ax.text(
            6,
            0.15,
            route_text,
            fontsize=12,
            fontweight="bold",
            color="#c0392b",
            ha="center",
            bbox=dict(
                boxstyle="round,pad=0.5",
                facecolor="white",
                edgecolor="#e74c3c",
                linewidth=1.5
            )
        )

    legend_items = [
        ("LOW", "#20a85a"),
        ("MEDIUM", "#f2c94c"),
        ("HIGH", "#eb5757"),
        ("OPTIMIZED ROUTE", "#e63946")
    ]

    legend_x = 0.4
    legend_y = 0.8

    ax.text(
        legend_x,
        legend_y + 0.75,
        "TRAFFIC LEGEND",
        fontsize=10,
        fontweight="bold",
        color="#34495e"
    )

    for index, (label, color) in enumerate(
        legend_items
    ):

        y = legend_y - (
            index * 0.35
        )

        ax.scatter(
            legend_x,
            y,
            s=90,
            color=color,
            edgecolor="white",
            linewidth=1.5,
            zorder=20
        )

        ax.text(
            legend_x + 0.25,
            y,
            label,
            fontsize=8.5,
            color="#34495e",
            va="center"
        )

    total_vehicles = sum(
        data["vehicles"]
        for data in junction_data.values()
    )

    average_speed = int(
        sum(
            data["speed"]
            for data in junction_data.values()
        )
        / len(junction_data)
    )

    very_high = sum(
        1
        for data in junction_data.values()
        if data["congestion"]["category"]
        == "VERY HIGH"
    )

    ax.text(
        10.1,
        8.0,
        "TRAFFIC OVERVIEW",
        fontsize=11,
        fontweight="bold",
        color="#34495e"
    )

    ax.text(
        10.1,
        7.55,
        f"Vehicles: {total_vehicles}",
        fontsize=10,
        color="#34495e"
    )

    ax.text(
        10.1,
        7.15,
        f"Avg Speed: {average_speed} km/h",
        fontsize=10,
        color="#34495e"
    )

    ax.text(
        10.1,
        6.75,
        f"High Congestion: {very_high}",
        fontsize=10,
        color="#34495e"
    )

    ax.set_xlim(
        0,
        12.5
    )

    ax.set_ylim(
        -0.4,
        9.3
    )

    ax.axis("off")

    plt.tight_layout(
        rect=(0, 0, 1, 0.98)
    )

    plt.show()