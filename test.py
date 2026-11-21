from visualization.city_map import draw_city_map
from city.city_graph import create_city_graph
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.astar import astar
from algorithms.route_optimizer import optimize_route, emergency_route


graph = create_city_graph()

start = "A"
goal = "F"

print("City Graph:")
print(list(graph.edges(data=True)))

print("\nBFS:")
print(bfs(graph, start, goal))

print("\nDFS:")
print(dfs(graph, start, goal))

print("\nUCS:")
print(ucs(graph, start, goal))

print("\nA*:")
print(astar(graph, start, goal))

print("\nTraffic-Aware Route:")
print(optimize_route(graph, start, goal))

print("\nEmergency Vehicle Route:")
print(emergency_route(graph, "ambulance", "A", "F"))

route_result = optimize_route(graph, start, goal)

if route_result:
    route, cost = route_result
    draw_city_map(graph, route)