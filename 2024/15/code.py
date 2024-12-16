from tqdm import tqdm


def shape(grid):
    n, m = len(grid), len(grid[0])
    return n, m


def parse_data(data):
    id_split = data.index("")
    grid = [list(line) for line in data[:id_split]]
    moves = "".join(data[id_split + 1 :])

    n, m = shape(grid)
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if grid[i][j] == "@":
                posRobot = [i, j]

    return grid, moves, posRobot


def inbound(pX, pY, n, m):
    return (1 <= pX < n - 1) and (1 <= pY < m - 1)


def swap(grid, dX, dY, newDX, newDY):
    grid[dX][dY], grid[newDX][newDY] = grid[newDX][newDY], grid[dX][dY]


def debug(grid):
    for line in grid:
        print("".join(line))
    print()


def GPS_boxes(grid):
    n, m = shape(grid)
    TOT = 0
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if grid[i][j] == "O":
                TOT += 100 * i + j
    return TOT


def part1(data):
    grid, moves, posRobot = parse_data(data)
    # print(grid)
    # print(f"{moves = }")
    # print(f"{posRobot = }")

    n, m = shape(grid)
    dirs = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}

    for move in tqdm(moves):
        # print(move)
        dX, dY = dirs[move]
        nextPosX, nextPosY = posRobot[0] + dX, posRobot[1] + dY
        elementsPos = []
        movable = False
        while inbound(nextPosX, nextPosY, n, m):
            if grid[nextPosX][nextPosY] == "#":
                break
            elif grid[nextPosX][nextPosY] == ".":
                movable = True
                break

            elementsPos.append((nextPosX, nextPosY))
            nextPosX += dX
            nextPosY += dY

        # print(movable, posRobot, elementsPos)

        if movable:
            if len(elementsPos) > 0:
                swap(
                    grid,
                    posRobot[0] + dX,
                    posRobot[1] + dY,
                    elementsPos[-1][0] + dX,
                    elementsPos[-1][1] + dY,
                )

            swap(
                grid,
                posRobot[0],
                posRobot[1],
                posRobot[0] + dX,
                posRobot[1] + dY,
            )
            posRobot[0] += dX
            posRobot[1] += dY

        # debug(grid)

    return GPS_boxes(grid)


def part2(data):
    return


if __name__ == "__main__":
    with open("2024/15/data/15_test2.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
