import matplotlib.pyplot as plt
import networkx as nx


def draw_city_map(graph, route=None):
    position = {
        "A": (0, 2),
        "B": (2, 3),
        "C": (2, 1),
        "D": (4, 2),
        "E": (5, 0),
        "F": (7, 1)
    }

    plt.figure(figsize=(10, 7))

    nx.draw_networkx_nodes(
        graph,
        position,
        node_size=1800,
        node_color="lightblue"
    )

    nx.draw_networkx_edges(
        graph,
        position,
        width=2,
        edge_color="gray"
    )

    nx.draw_networkx_labels(
        graph,
        position,
        font_size=14,
        font_weight="bold"
    )

    edge_labels = nx.get_edge_attributes(
        graph,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        graph,
        position,
        edge_labels=edge_labels,
        font_size=11
    )

    if route:
        route_edges = list(zip(route, route[1:]))

        nx.draw_networkx_edges(
            graph,
            position,
            edgelist=route_edges,
            width=4,
            edge_color="red"
        )

    plt.title("Smart City Traffic Route")
    plt.axis("off")
    plt.tight_layout()
    plt.show()