import re
from tqdm import tqdm
from functools import cache


def parse_data(data):
    pattern = re.compile(r"[rgubw]+")
    towels = set(re.findall(pattern, data[0]))
    designs = data[2:]

    return towels, designs


@cache
def design_doable_p1(design, max_len):
    if len(design) == 0:
        return True

    doable = False
    # print(" " * it + f"{max_len = }")
    for len_prefix in range(1, max_len + 1):
        if design[:len_prefix] in towels:
            # print(" " * it + f"{design[:len_prefix]}, {design[len_prefix:]}")
            doable = design_doable_p1(
                design=design[len_prefix:],
                max_len=min(max_len, len(design[len_prefix:])),
            )
            # print(" " * it + f"{suffix = }")
        if doable:
            break

    # print(f"{suffix_tot = }")

    return doable


@cache
def design_doable_p2(design, max_len):
    if len(design) == 0:
        return 1

    suffix_tot = 0
    # print(" " * it + f"{max_len = }")
    for len_prefix in range(1, max_len + 1):
        if design[:len_prefix] in towels:
            # print(" " * it + f"{design[:len_prefix]}, {design[len_prefix:]}")
            suffix = design_doable_p2(
                design=design[len_prefix:],
                max_len=min(max_len, len(design[len_prefix:])),
            )
            # print(" " * it + f"{suffix = }")
            suffix_tot += suffix

    # print(f"{suffix_tot = }")

    return suffix_tot


def part1(data):
    global towels
    towels, designs = parse_data(data)
    # print(f"{towels = }")
    # print(f"{designs = }")
    max_len = max(len(towel) for towel in towels)

    TOTAL = 0
    for design in designs:
        # print(design)
        doable = design_doable_p1(design, max_len)
        if doable:
            TOTAL += 1
        # print("POSSIBLE") if doable else print("IMPOSSIBLE")
        # print()

    return TOTAL


def part2(data):
    global towels
    towels, designs = parse_data(data)
    # print(f"{towels = }")
    # print(f"{designs = }")
    max_len = max(len(towel) for towel in towels)

    TOTAL = 0
    for design in tqdm(designs):
        # print(design)
        doable = design_doable_p2(design, max_len)
        TOTAL += doable
        # print("POSSIBLE") if doable else print("IMPOSSIBLE")
        # print()

    return TOTAL
    return


if __name__ == "__main__":
    YEAR, DAY = 2024, 19
    with open(f"{YEAR}/{DAY}/data/{DAY}_test.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)


# rrbgbr
# It1:
#   r = It2(d[1:])
#   return r

# It2:
#   r = It3(d[1:])
#   It3:
#       b = It4(d[1:])
#       It4:
#           g = It5(d[1:])
#           It5:
#               b = It6(d[1:])
#               It6:
#                   r = It6(d[1:])
#                   It7:
#                       return 1
#                   return r
#               return b
#           gb = It5(d[2:])
#           It5:
#               r = It6(d[1:])
#               It7:
#                   return 1
#               return r

#   rb = It3(d[2:])
#   return r + rb
