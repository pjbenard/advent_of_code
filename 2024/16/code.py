def parse_data(data):
    n, m = len(data), len(data[0])
    nodes = set()
    edges = {}

    for pX in range(1, n - 1):
        for pY in range(1, m - 1):
            element = data[pX][pY]
            if element == "#":
                continue
            elif element == "S":
                startNode = (pX, pY)
            elif element == "E":
                endNode = (pX, pY)

            nodes.add((pX, pY))
            edges[(pX, pY)] = set()
            for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nX, nY = pX + dX, pY + dY
                if data[nX][nY] == "#":
                    continue

                edges[(pX, pY)].add((nX, nY))

    return nodes, edges, startNode, endNode


def argmin(d, keys):
    min_key = list(keys)[0]
    min_val = d[min_key]
    for key in keys:
        val = d[key]
        if val < min_val:
            min_key = key
            min_val = val
    return min_key, min_val


def compute_cost_moving(newNode, prevNode):
    diffX = newNode[0] - prevNode[0]
    diffY = newNode[1] - prevNode[1]
    if (diffX, diffY) in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
        return 1
    else:
        return 1001
    # return 1001 if (diffX != 0) and (diffY != 0) else 1


def debug(prev, startNode, endNode, data):
    path = set()
    node = endNode
    while node != startNode:
        path.add(node)
        node = prev[node]
    path.remove(endNode)

    n, m = len(data), len(data[0])
    for i in range(n):
        for j in range(m):
            if (i, j) in path:
                print("+", end="")
            else:
                print(data[i][j], end="")
        print()
    print()


def djikstra(nodes, edges, startNode, endNode):
    queue_nodes = set()
    dist = dict()
    prev = dict()

    for node in nodes:
        dist[node] = 1_000_000_000
        prev[node] = None
        queue_nodes.add(node)
    dist[startNode] = 0
    prev[startNode] = (startNode[0], startNode[1] - 1)

    while len(queue_nodes) > 0:
        node, node_dist = argmin(dist, queue_nodes)
        queue_nodes.remove(node)
        # if node == endNode:
        #     break

        for neigh_node in edges[node]:
            if neigh_node not in queue_nodes:
                continue

            cost_move = compute_cost_moving(neigh_node, prev[node])
            alt_dist = node_dist + cost_move
            if alt_dist < dist[neigh_node]:
                dist[neigh_node] = alt_dist
                prev[neigh_node] = node

    return dist, prev


def compute_total_score(prev, startNode, endNode):
    path = []
    node = endNode
    while node != startNode:
        path.insert(0, node)
        node = prev[node]
    path.insert(0, startNode)
    print(f"{len(path) = }")

    total_score = 0
    prevprev_node = (startNode[0], startNode[1] - 1)
    all_diffs = set()
    straight_path = {(2, 0), (-2, 0), (0, 2), (0, -2)}
    bent_path = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
    nBends = 0
    for node in path[1:]:
        prev_node = prev[node]
        diffX = node[0] - prevprev_node[0]
        diffY = node[1] - prevprev_node[1]
        all_diffs.add((diffX, diffY))
        if (diffX, diffY) in straight_path:
            total_score += 1
        else:
            total_score += 1001
            nBends += 1

        prevprev_node = prev_node

    print(f"{nBends = }")

    print(all_diffs)

    return total_score


def part1(data):
    nodes, edges, startNode, endNode = parse_data(data)
    # print(f"{nodes = }")
    # print(f"{edges = }")
    print(f"{startNode = }")
    print(f"{endNode = }")

    dist, prev = djikstra(nodes, edges, startNode, endNode)
    # debug(prev, startNode, endNode, data)
    total_score = compute_total_score(prev, startNode, endNode)
    print(f"{dist[endNode] = }")
    return total_score


def part2(data):
    return


if __name__ == "__main__":
    with open("2024/16/data/16_test1.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)

# 133596 < x < 134596
