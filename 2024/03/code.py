import re
import operator as op


def parse_data(data):
    return data


def part1(data):
    lines = parse_data(data)
    # print(line)
    pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)")

    TOTAL = 0
    for line in lines:
        for match in re.findall(pattern, line):
            i1, i2 = list(map(int, match[4:-1].split(",")))
            TOTAL += op.mul(i1, i2)

    return TOTAL


def part2(data):
    lines = parse_data(data)
    # print(line)
    pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)")

    TOTAL = 0
    do_mul = True

    for line in lines:
        for match in re.findall(pattern, line):
            if match == r"don't()":
                do_mul = False
            elif match == r"do()":
                do_mul = True
            elif do_mul:
                i1, i2 = list(map(int, match[4:-1].split(",")))
                TOTAL += op.mul(i1, i2)

    return TOTAL


if __name__ == "__main__":
    with open("2024/03/data/03_test.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
