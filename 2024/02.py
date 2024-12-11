import numpy as np


def parse_data(data):
    reports = [np.array(list(map(int, line.split())), dtype=int) for line in data]

    return reports


def is_safe(report):
    diffs = report[1:] - report[:-1]
    sign = np.sign(diffs[0])
    return all(0 < diff * sign < 4 for diff in diffs)


def part1(data):
    reports = parse_data(data)
    SUM = sum(is_safe(report) for report in reports)
    return SUM


def part2(data):
    reports = parse_data(data)
    SUM = 0
    for report in reports:
        size = report.size
        arange = np.arange(size)
        SUM += any(is_safe(report[np.delete(arange, i)]) for i in range(size))

    return SUM
