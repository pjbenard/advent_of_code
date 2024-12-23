import numpy as np


def parse_data(data):
    numbers = list(map(int, data))
    return numbers


def evolve(n0):
    mod = 16777216  # 1 << 24 = 2**24
    n1 = ((n0 << 6) ^ n0) % mod
    n2 = ((n1 >> 5) ^ n1) % mod
    n3 = ((n2 << 11) ^ n2) % mod

    return n3


def part1(data):
    numbers = parse_data(data)
    # print(numbers)

    SUM = 0
    for number in numbers:
        for it in range(2000):
            number = evolve(number)
        # print(number)
        SUM += number

    return SUM


def part2(data):
    numbers = parse_data(data)
    prices = np.zeros((len(numbers), 2001), dtype=int)
    prices[:, 0] = numbers
    for idx, number in enumerate(numbers):
        for it in range(1, 2001):
            number = evolve(number)
            prices[idx, it] = number

    # print(prices)
    prices %= 10
    # print(prices)
    diffs = prices[:, 1:] - prices[:, :-1]
    # print(diffs)
    changes = set()
    for monkey in diffs:
        for idx in range(0, len(monkey) - 3):
            sequence = tuple(monkey[idx : idx + 4].tolist())
            changes.add(sequence)

    print(len(changes))
    return


if __name__ == "__main__":
    YEAR, DAY = 2024, 22
    with open(f"{YEAR}/{DAY}/data/{DAY}_input.txt") as file:
        data = file.read().splitlines()

    # res_p1 = part1(data)
    # print(res_p1)

    res_p2 = part2(data)
    print(res_p2)

# mod = 16777216  # 1 << 24 = 2**24
# n1 = ((n0 << 6) ^ n0) % mod
# n2 = ((n1 >> 5) ^ n1) % mod
# n3 = ((n2 << 11) ^ n2) % mod
