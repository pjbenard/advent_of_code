import numpy as np


def parse_data(data):
    grid = np.array([list(line) for line in data])
    return grid


def extract_frequencies_and_pos(grid):
    frequencies = np.unique(grid)

    distinct_antennas = {}
    for frequency in frequencies:
        distinct_antennas[str(frequency)] = np.where(grid == frequency)

    del distinct_antennas["."]
    return distinct_antennas


def extract_frequencies_and_pos_np(grid):
    frequencies = np.unique(grid)

    distinct_antennas = {}
    for frequency in frequencies:
        antennas_pos = np.array(np.where(grid == frequency)).T
        distinct_antennas[str(frequency)] = antennas_pos

    del distinct_antennas["."]
    return distinct_antennas


def inbound(posX, posY, n, m):
    return (0 <= posX < n) and (0 <= posY < m)


def inbound_np(pos, shape):
    return all(np.zeros_like(pos) <= pos) and all(pos < shape)


def debug(grid, antinodes):
    n, m = grid.shape
    for i in range(n):
        for j in range(m):
            if grid[i, j] != ".":
                print(grid[i, j], end="")
            elif antinodes[i, j]:
                print("#", end="")
            else:
                print(grid[i, j], end="")
        print()


def part1(data):
    grid = parse_data(data)
    shape = grid.shape

    distinct_antennas = extract_frequencies_and_pos_np(grid)
    antinodes = np.zeros_like(grid, dtype=bool)

    for frequency in distinct_antennas:
        antennas_pos = distinct_antennas[frequency]
        for id_antenna1, pos1 in enumerate(antennas_pos):
            for id_antenna2, pos2 in enumerate(antennas_pos):
                if id_antenna1 == id_antenna2:
                    continue

                antinode = 2 * pos1 - pos2
                if inbound_np(antinode, shape):
                    antinodes[antinode[0], antinode[1]] = True

    n_antinodes = np.count_nonzero(antinodes)
    return n_antinodes


def part2(data):
    grid = parse_data(data)
    shape = grid.shape

    distinct_antennas = extract_frequencies_and_pos_np(grid)
    antinodes = np.zeros_like(grid, dtype=bool)

    for frequency in distinct_antennas:
        antennas_pos = distinct_antennas[frequency]
        for id_antenna1, pos1 in enumerate(antennas_pos):
            for id_antenna2, pos2 in enumerate(antennas_pos):
                if id_antenna1 == id_antenna2:
                    continue

                diff_antennas = pos1 - pos2
                antinode = pos1.copy()

                while inbound_np(antinode, shape):
                    antinodes[antinode[0], antinode[1]] = True
                    antinode += diff_antennas

    n_antinodes = np.count_nonzero(antinodes)
    return n_antinodes


if __name__ == "__main__":
    with open("2024/08/data/08_test.txt") as file:
        data = file.read().splitlines()

    grid = parse_data(data)
    shape = grid.shape
    # print(grid, n, m)

    distinct_antennas = extract_frequencies_and_pos_np(grid)
    antinodes = np.zeros_like(grid, dtype=bool)

    for frequency, antennas_pos in distinct_antennas.items():
        n_antennas = antennas_pos.shape[0]
        for id_antenna1, pos1 in enumerate(antennas_pos):
            for id_antenna2, pos2 in enumerate(antennas_pos):
                if id_antenna1 == id_antenna2:
                    continue

                diff_antennas = pos1 - pos2
                antinode = pos1.copy()

                while inbound_np(antinode, shape):
                    print(antinode)
                    antinodes[antinode[0], antinode[1]] = True
                    antinode += diff_antennas

    debug(grid, antinodes)
    print(np.count_nonzero(antinodes))
