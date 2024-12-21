import heapq as hq


def inbound(pX, pY, n, m):
    return (1 <= pX < n - 1) and (1 <= pY < m - 1)


def parse_data(data):
    n, m = len(data), len(data[0])
    print(f"{n = }, {m = }")

    track = dict()
    for pX in range(1, n - 1):
        for pY in range(1, m - 1):
            node = (pX, pY)
            element = data[pX][pY]
            if element == "#":
                continue
            elif element == "S":
                startTrack = node
            elif element == "E":
                endTrack = node

            track[node] = []
            for diffX, diffY in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighX, neighY = pX + diffX, pY + diffY
                neigh = (neighX, neighY)
                element_neigh = data[neighX][neighY]
                if element_neigh != "#":
                    track[node].append((neigh, 1))

    thinWalls = dict()
    for pX in range(1, n - 1):
        for pY in range(1, m - 1):
            node = (pX, pY)
            element = data[pX][pY]
            if element != "#":
                continue
            thinWalls[node] = []
            for diffX, diffY in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighX, neighY = pX + diffX, pY + diffY
                neigh = (neighX, neighY)
                element_neigh = data[neighX][neighY]
                if element_neigh != "#":
                    thinWalls[node].append(neigh)

            if len(thinWalls[node]) != 2:
                del thinWalls[node]
                continue

            node1, node2 = thinWalls[node]
            diffX = abs(node1[0] - node2[0])
            diffY = abs(node1[1] - node2[1])
            if (diffX, diffY) not in [(2, 0), (0, 2)]:
                del thinWalls[node]

    return track, thinWalls, startTrack, endTrack


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
    track, thinWalls, startTrack, endTrack = parse_data(data)
    distances = dijkstra(track, startTrack)

    print(f"{len(distances) = }")

    cheats = dict()
    for wall in thinWalls:
        node1, node2 = thinWalls[wall]
        dist_gained = abs(distances[node1] - distances[node2]) - 2
        cheats[dist_gained] = cheats.get(dist_gained, 0) + 1

    # print(cheats)
    return sum(nCheats for dist, nCheats in cheats.items() if dist >= 100)


def part2(data):
    track, thinWalls, startTrack, endTrack = parse_data(data)
    distances = dijkstra(track, startTrack)
    order = [0] * len(distances)
    for node, dist in distances.items():
        order[dist] = node
    print(order)
    return


if __name__ == "__main__":
    YEAR, DAY = 2024, 20
    with open(f"{YEAR}/{DAY}/data/{DAY}_test.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
