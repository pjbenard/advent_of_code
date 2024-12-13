from collections import defaultdict


def parse_data(data):
    id_split = data.index("")
    rules = data[:id_split]
    updates = data[id_split + 1 :]

    d_above = defaultdict(set)

    for rule in rules:
        p1, p2 = list(map(int, rule.split("|")))
        d_above[p2].add(p1)

    return d_above, updates


def class_updates(d_above, updates):
    correct_updates = []
    incorrect_updates = []

    for update in updates:
        pages = list(map(int, update.split(",")))
        for id_page, page in enumerate(pages[:-1]):
            pages_after = set(pages[id_page + 1 :])
            if pages_after.intersection(d_above[page]):
                incorrect_updates.append(update)
                break
        else:
            correct_updates.append(update)

    return correct_updates, incorrect_updates


def part1(data):
    d_above, updates = parse_data(data)

    MID_PAGE_SUM = 0
    correct_updates, _ = class_updates(d_above, updates)

    for update in correct_updates:
        pages = list(map(int, update.split(",")))
        MID_PAGE_SUM += pages[(len(pages) - 1) // 2]

    return MID_PAGE_SUM


def part2(data):
    d_above, updates = parse_data(data)

    MID_PAGE_SUM = 0
    _, incorrect_updates = class_updates(d_above, updates)

    for update in incorrect_updates:
        pages = list(map(int, update.split(",")))
        id_page = 0

        while id_page < len(pages):
            pages_after = set(pages[id_page + 1 :])
            incorrectly_ordered_pages = pages_after & d_above[pages[id_page]]
            if incorrectly_ordered_pages:
                p1 = list(incorrectly_ordered_pages)[0]
                id_page_inc = pages.index(p1)
                # swap
                temp = pages[id_page]
                pages[id_page] = pages[id_page_inc]
                pages[id_page_inc] = temp
            else:
                id_page += 1

        MID_PAGE_SUM += pages[(len(pages) - 1) // 2]

    return MID_PAGE_SUM


if __name__ == "__main__":
    with open("2024/05/data/05_test.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
