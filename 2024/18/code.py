import heapq as hq


def parse_data(data):
    positions = [tuple(map(int, line.split(","))) for line in data]
    n = max(positions, key=lambda pos: pos[0])[0] + 1
    m = max(positions, key=lambda pos: pos[1])[1] + 1
    return positions, n, m


def inbound(pX, pY, n, m):
    return (0 <= pX < n) and (0 <= pY < m)


def create_graph(n, m, obstacles):
    graph = dict()
    for pX in range(0, n):
        for pY in range(0, m):
            node = (pX, pY)
            graph[node] = []
            for diffX, diffY in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighX, neighY = pX + diffX, pY + diffY
                neigh = (neighX, neighY)
                if (not inbound(neighX, neighY, n, m)) or (neigh in obstacles):
                    continue

                graph[node].append((neigh, 1))

    return graph


# Thanks to https://stackoverflow.com/a/71666688
def dijkstra(graph, start):
    distances = {}
    heap = [(0, start)]

    while heap:
        dist, node = hq.heappop(heap)
        if node in distances:
            continue
        distances[node] = dist
        # print(f"{node = }, {dist = }")
        # print(f"{graph[node] = }")
        for neighbor, weight in graph[node]:
            # print(neighbor, weight)
            if neighbor not in distances:
                hq.heappush(heap, (dist + weight, neighbor))
        # print(heap)
        # print()

    return distances


def part1(data):
    positions, n, m = parse_data(data)
    print(f"{(n, m) = }")
    print(f"{len(positions) = }")
    # print(positions[:10])
    if n == 7:
        falling_bytes = 12
    else:
        falling_bytes = 1024

    obstacles = set(positions[:falling_bytes])
    print(f"{len(obstacles) = }")
    # print(f"{obstacles = }")

    # Construct graph
    graph = create_graph(n, m, obstacles)
    # print(graph)

    distances = dijkstra(graph, start=(0, 0))
    # print(distances)
    return distances[(n - 1, m - 1)]


def part2(data):
    positions, n, m = parse_data(data)
    print(f"{(n, m) = }")
    print(f"{len(positions) = }")

    min_obst, max_obst = 0, len(positions)

    while min_obst < max_obst:
        # print(min_obst, max_obst)
        falling_bytes = (min_obst + max_obst) // 2
        obstacles = positions[:falling_bytes]
        graph = create_graph(n, m, obstacles)
        distances = dijkstra(graph, start=(0, 0))
        if (n - 1, m - 1) not in distances:
            max_obst = falling_bytes
        else:
            min_obst = falling_bytes + 1

    # print(min_obst, falling_bytes, max_obst)
    return positions[falling_bytes]


if __name__ == "__main__":
    with open("2024/18/data/18_test.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
