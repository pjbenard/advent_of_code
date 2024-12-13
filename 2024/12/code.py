from itertools import groupby


def parse_data(data):
    grid = [list(line) for line in data]
    return grid


def shape(grid):
    n, m = len(grid), len(grid[0])
    return n, m


def inbound(posX, posY, n, m):
    return (0 <= posX < n) and (0 <= posY < m)


def debug(grid, graph, region):
    n, m = shape(grid)
    for i in range(n):
        for j in range(m):
            if (i, j) in graph[region]:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def find_neighbours(grid, n, m):
    neighbours = dict()
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for posX in range(0, n):
        for posY in range(0, m):
            neighbours[(posX, posY)] = set()
            for dX, dY in dirs:
                if inbound(posX + dX, posY + dY, n, m):
                    if grid[posX][posY] == grid[posX + dX][posY + dY]:
                        neighbours[(posX, posY)].add((posX + dX, posY + dY))

    return neighbours


def create_regions(neighbours, n, m):
    graph = dict()
    nRegions = 0
    for posX in range(0, n):
        for posY in range(0, m):
            pos = (posX, posY)
            if any(pos in graph[region] for region in graph):
                continue
            graph[nRegions] = {pos}
            neighbours_to_add = neighbours[pos].difference(graph[nRegions])
            while len(neighbours_to_add):
                newNeighbours_to_add = set()
                for neighbour in neighbours_to_add:
                    graph[nRegions].add(neighbour)
                    newNeighbours_to_add.update(neighbours[neighbour])
                neighbours_to_add = newNeighbours_to_add.difference(graph[nRegions])

            nRegions += 1

    return graph


def count_distinct_sides(scan):
    return sum(abs(k) for (k, g) in groupby(scan) if k != 0)


def identify_sides(region, n, m):
    sides = 0
    # print(region)
    for posX in range(n + 1):
        scan_change = [False] * m
        for posY in range(m):
            pos = (min(posX, n - 1), posY)
            scan_change[posY] = int(pos in region)
            if 0 < posX < n:
                prevPos = (posX - 1, posY)
                scan_change[posY] -= int(prevPos in region)
        # print(scan_change)
        sides += count_distinct_sides(scan_change)

    for posY in range(m + 1):
        scan_change = [0] * n
        for posX in range(n):
            pos = (posX, min(posY, m - 1))
            scan_change[posX] = int(pos in region)
            if 0 < posY < m:
                prevPos = (posX, posY - 1)
                scan_change[posX] -= int(prevPos in region)
        # print(scan_change)
        sides += count_distinct_sides(scan_change)

    return sides


def part1(data):
    grid = parse_data(data)
    # print(grid)
    n, m = shape(grid)

    # Step 1: get graph of each region
    neighbours = find_neighbours(grid, n, m)
    # print(neighbours)

    graph = create_regions(neighbours, n, m)
    # print(graph)

    # for region in graph:
    #     debug(grid, graph, region)

    # Step 2: for each region/graph, count area and perimeter
    area = {region: len(elements) for region, elements in graph.items()}
    perimeter = {region: 0 for region in graph}

    for region, elements in graph.items():
        for element in elements:
            perimeter[region] += 4 - len(neighbours[element])

    # print(area)
    # print(perimeter)
    price = sum(area[region] * perimeter[region] for region in graph)

    return price


def part2(data):
    grid = parse_data(data)
    # print(grid)
    n, m = shape(grid)

    # Step 1: get graph of each region
    neighbours = find_neighbours(grid, n, m)
    # print(neighbours)

    graph = create_regions(neighbours, n, m)
    # print(graph)

    # for region in graph:
    #     debug(grid, graph, region)

    # Step 2: for each region/graph, count area and perimeter
    area = {region: len(elements) for region, elements in graph.items()}
    sides = {region: identify_sides(graph[region], n, m) for region in graph}

    # print(f'{area = }')
    # print(f'{sides = }')
    price = sum(area[region] * sides[region] for region in graph)

    return price


if __name__ == "__main__":
    with open("2024/12/data/12_test5.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
