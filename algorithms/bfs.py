from collections import deque


def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbour in graph.neighbors(current):
            if neighbour not in visited:
                queue.append(
                    (neighbour, path + [neighbour])
                )

    return None