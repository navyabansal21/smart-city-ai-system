import heapq


def heuristic(graph, current, goal):
    return 0


def astar(graph, start, goal):
    priority_queue = [(0, 0, start, [start])]
    visited = set()

    while priority_queue:
        f_cost, g_cost, current, path = heapq.heappop(priority_queue)

        if current == goal:
            return path, g_cost

        if current in visited:
            continue

        visited.add(current)

        for neighbour in graph.neighbors(current):
            if neighbour in visited:
                continue

            distance = graph[current][neighbour]["weight"]
            new_g_cost = g_cost + distance
            h_cost = heuristic(graph, neighbour, goal)
            new_f_cost = new_g_cost + h_cost

            heapq.heappush(
                priority_queue,
                (new_f_cost, new_g_cost, neighbour, path + [neighbour])
            )

    return None