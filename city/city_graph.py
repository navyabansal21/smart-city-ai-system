import networkx as nx
from city.knowledge_base import get_roads


def create_city_graph():
    graph = nx.Graph()
    roads = get_roads()

    for start, destinations in roads.items():
        for end, distance in destinations.items():
            graph.add_edge(start, end, weight=distance)

    return graph


def get_neighbors(graph, intersection):
    return list(graph.neighbors(intersection))


def get_distance(graph, start, end):
    return graph[start][end]["weight"]


def display_graph(graph):
    print("City Graph:")
    for node in graph.nodes:
        print(f"{node}: {get_neighbors(graph, node)}")