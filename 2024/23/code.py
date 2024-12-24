import numpy as np


def parse_data(data):
    graph = {}
    for line in data:
        node1, node2 = line.split("-")
        if node1 not in graph:
            graph[node1] = set()
        graph[node1].add(node2)

        if node2 not in graph:
            graph[node2] = set()
        graph[node2].add(node1)

    return graph


def part1(data):
    graph = parse_data(data)
    nodes = graph.keys()
    print(len(nodes))
    # print(graph)

    triangles = set()

    for n1 in nodes:
        for n2 in graph[n1]:
            for n3 in graph[n2]:
                if n1 == n3:
                    continue
                for n4 in graph[n3]:
                    if n1 == n4:
                        triangle = tuple(sorted([n1, n2, n3]))
                        triangles.add(triangle)

    # print(len(triangles), triangles)
    triangles_with_t = list(
        triangle
        for triangle in triangles
        if any(node.startswith("t") for node in triangle)
    )
    return len(triangles_with_t)


def part2(data):
    return


if __name__ == "__main__":
    YEAR, DAY = 2024, 23
    with open(f"{YEAR}/{DAY}/data/{DAY}_input.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
