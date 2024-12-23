directional_keypad = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}
numerical_keypad = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}


def parse_data(data):
    numeric_part = [int(line[:-1]) for line in data]
    return data, numeric_part


def create_d_k2k():
    d_k2k = {}
    for key1 in directional_keypad:
        pos1X, pos1Y = directional_keypad[key1]
        for key2 in directional_keypad:
            pos2X, pos2Y = directional_keypad[key2]
            if key1 == key2:
                d_k2k[(key1, key2)] = ""
                continue

            diffX, diffY = pos2X - pos1X, pos2Y - pos1Y

            sensH = ">" if diffY > 0 else "<"
            dirs = sensH * abs(diffY)

            sensV = "v" if diffX > 0 else "^"
            dirs += sensV * abs(diffX)
            if diffX > 0:
                dirs = dirs[::-1]

            d_k2k[(key1, key2)] = dirs

    return d_k2k


def create_d_n2k():
    d_n2k = {}
    for key1 in numerical_keypad:
        pos1X, pos1Y = numerical_keypad[key1]
        for key2 in numerical_keypad:
            pos2X, pos2Y = numerical_keypad[key2]
            if key1 == key2:
                d_n2k[(key1, key2)] = ""
                continue

            diffX, diffY = pos2X - pos1X, pos2Y - pos1Y

            sensH = ">" if diffY > 0 else "<"
            dirs = sensH * abs(diffY)

            sensV = "v" if diffX > 0 else "^"
            dirs += sensV * abs(diffX)
            if diffX < 0:
                dirs = dirs[::-1]

            d_n2k[(key1, key2)] = dirs

    return d_n2k


d_k2k = create_d_k2k()
d_n2k = create_d_n2k()


def compute_sequence(code, it=0):
    if it == 3:
        return code

    next_code = ""

    if it == 0:
        d_in = d_n2k
    else:
        d_in = d_k2k

    current_pos = "A"
    for next_pos in code:
        next_code += d_in[(current_pos, next_pos)]
        next_code += "A"
        current_pos = next_pos

    print(next_code)
    return compute_sequence(next_code, it + 1)


def part1(data):
    codes, numeric_parts = parse_data(data)
    print(f"{codes = }")
    print(f"{numeric_parts = }")

    SUM = 0
    for idx, code_in in enumerate(codes):
        code = compute_sequence(code_in)
        print(len(code), numeric_parts[idx])
        SUM += len(code) * numeric_parts[idx]
    # print(f"{d_k2k = }")
    # print(f"{d_k2n = }")

    return SUM


def part2(data):
    return


if __name__ == "__main__":
    YEAR, DAY = 2024, 21
    with open(f"{YEAR}/{DAY}/data/{DAY}_input.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

# <Av<AA>>^A<AAvA^Av<AAA
#  ^  <<   A ^^ >AvvvA>A
#          1    8   0 A
