DEBUG = False


def verbose_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def parse_data(data):
    grid = [list(map(int, list(line))) for line in data]
    return grid


def shape(array):
    n, m = len(array), len(array[0])
    return n, m


def find_val_idxs(array, val):
    posX, posY = [], []
    n, m = len(array), len(array[0])
    for i in range(n):
        for j in range(m):
            if array[i][j] == val:
                posX.append(i)
                posY.append(j)
    return posX, posY


def sum2d(grid):
    return sum(sum(grid[i]) for i in range(len(grid)))


def init_path_set(grid):
    n, m = shape(grid)
    path = [[set() for j in range(m)] for i in range(n)]
    startPos = find_val_idxs(grid, 9)
    for idx_trailhead, (posX, posY) in enumerate(zip(*startPos)):
        path[posX][posY] = {idx_trailhead}
    return path


def init_path_int(grid):
    n, m = shape(grid)
    path = [[0 for j in range(m)] for i in range(n)]
    startPos = find_val_idxs(grid, 9)
    for idx_trailhead, (posX, posY) in enumerate(zip(*startPos)):
        path[posX][posY] = 1
    return path


def count_paths_set(path, grid):
    n, m = shape(path)
    nPaths = []
    for i in range(n):
        nPaths.append([])
        for j in range(m):
            nPaths[i].append(len(path[i][j]) if grid[i][j] == 0 else 0)

    return nPaths


def count_paths_int(path, grid):
    n, m = shape(path)
    nPaths = []
    for i in range(n):
        nPaths.append([])
        for j in range(m):
            nPaths[i].append(path[i][j] if grid[i][j] == 0 else 0)

    return nPaths


def inbound(posX, posY, n, m):
    return (0 <= posX < n) and (0 <= posY < m)


def adjacent_positions(posX, posY, n, m):
    diffsX, diffsY = [-1, 0, 1, 0], [0, 1, 0, -1]
    adj_posX, adj_posY = [], []
    for diffX, diffY in zip(diffsX, diffsY):
        newPosX = posX + diffX
        newPosY = posY + diffY
        if inbound(newPosX, newPosY, n, m):
            adj_posX.append(newPosX)
            adj_posY.append(newPosY)
    return adj_posX, adj_posY


def part1(data):
    grid = parse_data(data)
    n, m = shape(grid)
    path = init_path_set(grid)
    for level in range(9, 0, -1):
        level_pos = find_val_idxs(grid, level)
        for posX, posY in zip(*level_pos):
            adj_pos = adjacent_positions(posX, posY, n, m)
            for adj_posX, adj_posY in zip(*adj_pos):
                if (grid[adj_posX][adj_posY] - grid[posX][posY]) == -1:
                    path[adj_posX][adj_posY].update(path[posX][posY])

    nPaths = count_paths_set(path, grid)
    verbose_print(nPaths)
    return sum2d(nPaths)


def part2(data):
    grid = parse_data(data)
    n, m = shape(grid)
    path = init_path_int(grid)
    for level in range(9, 0, -1):
        level_pos = find_val_idxs(grid, level)
        for posX, posY in zip(*level_pos):
            adj_pos = adjacent_positions(posX, posY, n, m)
            for adj_posX, adj_posY in zip(*adj_pos):
                if (grid[adj_posX][adj_posY] - grid[posX][posY]) == -1:
                    path[adj_posX][adj_posY] += path[posX][posY]

    nPaths = count_paths_int(path, grid)
    verbose_print(nPaths)
    return sum2d(nPaths)


if __name__ == "__main__":
    with open("2024/10/data/10_test.txt") as file:
        data = file.read().splitlines()

    DEBUG = True

    res_part1 = part1(data)
    print(res_part1)

    res_part2 = part2(data)
    print(res_part2)
