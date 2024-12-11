def parse_data(data):
    line = list(map(int, data[0].split()))
    return line


def update_stones(stones, newStones, stone, count):
    newCount = count
    # newCount += stones.get(stone, 0)
    newCount += newStones.get(stone, 0)
    newStones[stone] = newCount


def part(data, n_blinks=25):
    line = parse_data(data)
    print(f"Starting {line = }")
    stones = dict()
    for stone in line:
        stones[stone] = stones.get(stone, 0) + 1

    # print(stones)
    for blink in range(n_blinks):
        # print('blink', blink + 1)
        newStones = dict()
        for stone, count in stones.items():
            if stone == 0:
                update_stones(stones, newStones, 1, count)
            elif len(stone_str := str(stone)) % 2 == 0:
                len_stone = len(stone_str)
                s1 = int(stone_str[: len_stone // 2])
                s2 = int(stone_str[len_stone // 2 :])
                update_stones(stones, newStones, s1, count)
                update_stones(stones, newStones, s2, count)
            else:
                newStone = stone * 2024
                update_stones(stones, newStones, newStone, count)
        stones = newStones
        # print(stones)
        # print(sum(stones.values()))

    print(f"Number of differents stones = {len(stones.keys())}")
    return sum(stones.values())


def part1(data):
    return part(data, n_blinks=25)


def part2(data):
    return part(data, n_blinks=75)


if __name__ == "__main__":
    with open("2024/data/11_test.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
