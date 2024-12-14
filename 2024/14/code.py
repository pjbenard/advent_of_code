import re
import numpy as np
from PIL import Image
from tqdm import tqdm


def parse_data(data):
    shape_grid = list(map(int, data[0].split(",")))

    position = []
    velocity = []

    pattern = re.compile(r"-?\d+")
    for line in data[1:]:
        px, py, vx, vy = list(map(int, re.findall(pattern, line)))
        position.append([px, py])
        velocity.append([vx, vy])

    return np.array(shape_grid), np.array(position), np.array(velocity)


def create_grid(shape_grid, position):
    grid = np.zeros(shape_grid, dtype=int)
    for px, py in position:
        grid[px, py] += 1
    return grid


def create_bin_grid(shape_grid, position):
    grid = np.zeros(shape_grid, dtype=bool)
    pX, pY = position[:, 0], position[:, 1]
    grid[pX, pY] = True
    return grid


def debug(grid):
    n, m = grid.shape
    for j in range(m):
        for i in range(n):
            print(grid[i, j], end="") if grid[i, j] > 0 else print(".", end="")
        print()
    print()


def part1(data):
    shape_grid, position, velocity = parse_data(data)
    print(f"{shape_grid = }")
    # print(f"{position = }")
    # print(f"{velocity = }")

    # grid = create_grid(shape_grid, position)
    # debug(grid)

    nSeconds = 100

    # Update positions
    position += velocity * nSeconds
    position %= shape_grid

    # grid = create_grid(shape_grid, position)
    # debug(grid)

    # Split in quadrants
    midX, midY = shape_grid // 2
    grid = create_grid(shape_grid, position)
    quadrant_NW = grid[:midX, :midY]
    quadrant_SW = grid[:midX, midY + 1 :]
    quadrant_NE = grid[midX + 1 :, :midY]
    quadrant_SE = grid[midX + 1 :, midY + 1 :]

    # print("Quadrant NW")
    # debug(quadrant_NW)
    # print("Quadrant SW")
    # debug(quadrant_SW)
    # print("Quadrant NE")
    # debug(quadrant_NE)
    # print("Quadrant SE")
    # debug(quadrant_SE)

    safety_factor = 1
    for quadrant in [quadrant_NW, quadrant_SW, quadrant_NE, quadrant_SE]:
        safety_factor *= np.sum(quadrant)

    return safety_factor


def part2_old(data):
    # Saving positions as pictures and finding manually the tree
    shape_grid, position, velocity = parse_data(data)
    dir_name = "2024/14/imgs"
    # 53 ++ 103
    # base_it, update_it = 53, 103
    base_it, update_it = 0, 1
    it = base_it

    # Update positions
    position += velocity * update_it
    position %= shape_grid

    while it < 10_000:
        bin_grid = create_bin_grid(shape_grid, position)
        image = Image.fromarray(bin_grid)
        image.save(f"{dir_name}/{it:04d}.png")

        it += update_it
        # Update positions
        position += velocity * update_it
        position %= shape_grid


def part2(data):
    # Using the chinese remainder theorem
    shape_grid, position, velocity = parse_data(data)
    n, m = list(map(int, shape_grid))
    varX, varY = np.zeros(n), np.zeros(m)
    newPosition = np.zeros_like(position, dtype=int)

    for it in range(max(n, m)):
        # Update positions
        newPosition = (position + velocity * it) % shape_grid
        variance_it = np.var(newPosition, axis=0)
        varX[it % n] = variance_it[0]
        varY[it % m] = variance_it[1]

    aX = int(np.argmin(varX))
    aY = int(np.argmin(varY))

    vX = pow(m, -1, n)
    vY = pow(n, -1, m)

    eX = vX * m
    eY = vY * n

    it_easter_egg = (aX * eX + aY * eY) % (m * n)

    # print(f"{aX = }, {aY = }")
    # print(f"{vX = }, {vY = }")
    # print(f"{eX = }, {eY = }")

    return it_easter_egg


if __name__ == "__main__":
    with open("2024/14/data/14_input.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
