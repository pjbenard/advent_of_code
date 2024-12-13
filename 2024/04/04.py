import numpy as np


def parse_data(data):
    grid = np.array([list(line) for line in data])
    return grid


def test_XMAS(array, idx, idy):
    return "".join(array[idx, idy]) == "XMAS"


def part1(data):
    grid = parse_data(data)
    n, m = grid.shape

    id_hor_1_x, id_hor_1_y = np.array([0, 0, 0, 0]), np.array([0, 1, 2, 3])
    id_hor_2_x, id_hor_2_y = np.array([0, 0, 0, 0]), np.array([3, 2, 1, 0])

    id_ver_1_x, id_ver_1_y = np.array([0, 1, 2, 3]), np.array([0, 0, 0, 0])
    id_ver_2_x, id_ver_2_y = np.array([3, 2, 1, 0]), np.array([0, 0, 0, 0])

    id_dia_1_x, id_dia_1_y = np.array([0, 1, 2, 3]), np.array([0, 1, 2, 3])
    id_dia_2_x, id_dia_2_y = np.array([3, 2, 1, 0]), np.array([3, 2, 1, 0])
    id_dia_3_x, id_dia_3_y = np.array([0, 1, 2, 3]), np.array([3, 2, 1, 0])
    id_dia_4_x, id_dia_4_y = np.array([3, 2, 1, 0]), np.array([0, 1, 2, 3])

    nXMAS = 0
    for i in range(0, n):
        for j in range(0, m - 3):
            nXMAS += test_XMAS(grid, id_hor_1_x + i, id_hor_1_y + j)
            nXMAS += test_XMAS(grid, id_hor_2_x + i, id_hor_2_y + j)

    for i in range(0, n - 3):
        for j in range(0, m):
            nXMAS += test_XMAS(grid, id_ver_1_x + i, id_ver_1_y + j)
            nXMAS += test_XMAS(grid, id_ver_2_x + i, id_ver_2_y + j)

    for i in range(0, n - 3):
        for j in range(0, m - 3):
            nXMAS += test_XMAS(grid, id_dia_1_x + i, id_dia_1_y + j)
            nXMAS += test_XMAS(grid, id_dia_2_x + i, id_dia_2_y + j)
            nXMAS += test_XMAS(grid, id_dia_3_x + i, id_dia_3_y + j)
            nXMAS += test_XMAS(grid, id_dia_4_x + i, id_dia_4_y + j)

    return nXMAS


def part2(data):
    grid = parse_data(data)
    n, m = grid.shape

    pattern_x = np.array([0, 0, 1, 2, 2])
    pattern_y = np.array([0, 2, 1, 0, 2])

    strings = ["MMASS", "SMASM", "MSAMS", "SSAMM"]
    nXMAS = 0
    for i in range(0, n - 2):
        for j in range(0, m - 2):
            nXMAS += "".join(grid[pattern_x + i, pattern_y + j]) in strings

    return nXMAS


if __name__ == "__main__":
    with open("2024/data/04_test.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
