from collections import Counter


def parse_data(data):
    l1, l2 = [], []
    for line in data:
        i1, i2 = list(map(int, line.split()))
        l1.append(i1)
        l2.append(i2)
    return l1, l2


def part1(data):
    l1, l2 = parse_data(data)

    SUM = sum(abs(i1 - i2) for (i1, i2) in zip(sorted(l1), sorted(l2)))
    return SUM


def part2(data):
    l1, l2 = parse_data(data)
    count_l2 = Counter(l2)

    SUM = sum(i1 * count_l2[i1] for i1 in l1)
    return SUM
