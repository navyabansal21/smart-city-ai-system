import heapq


def ucs(graph, start, goal):
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
                distance = graph[current][neighbour]["weight"]
                heapq.heappush(
                    priority_queue,
                    (cost + distance, neighbour, path + [neighbour])
                )

    return None