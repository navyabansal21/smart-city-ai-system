def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbour in graph.neighbors(current):
            if neighbour not in visited:
                stack.append(
                    (neighbour, path + [neighbour])
                )

    return None