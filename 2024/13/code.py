import re


def parse_data(data):
    nGames = (len(data) + 1) // 4
    games = []
    pattern = re.compile(r"\d+")
    for id_game in range(nGames):
        game = {}
        for id_line, line in enumerate(["A", "B", "prize"]):
            matches = re.findall(pattern, data[id_game * 4 + id_line])
            game[line] = list(map(int, matches))
        games.append(game)

    return games


def compute_inv_determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def cofactors_matrix(matrix):
    co_matrix = [[matrix[1][1], -matrix[1][0]], [-matrix[0][1], matrix[0][0]]]
    return co_matrix


def play(game):
    matrix = [game["A"], game["B"]]
    prize = game["prize"]

    det = compute_inv_determinant(matrix)
    if det == 0:
        return 0

    co_matrix = cofactors_matrix(matrix)
    # print(f'{co_matrix = }, {det = }')

    tokens = [
        prize[0] * co_matrix[0][0] + prize[1] * co_matrix[0][1],
        prize[0] * co_matrix[1][0] + prize[1] * co_matrix[1][1],
    ]

    # print(f'{tokens = }, {[tokens[0] % det, tokens[1] % det]}')
    # print(f'{tokens[0] / det, tokens[1] / det}')
    if (tokens[0] % det != 0) or (tokens[1] % det != 0):
        return 0

    return (3 * tokens[0] // det) + (tokens[1] // det)


def part1(data):
    """
    (Ax Bx) (nA) = (totX) <=> M * N = TOT
    (Ay By) (nB)   (totY)
    So N = M**-1 * TOT
    with N a 2-vector of integers
    """
    games = parse_data(data)

    TOT = 0
    for game in games:
        # print(game)
        nTokens = play(game)
        # print(nTokens)
        TOT += nTokens

    return TOT


def part2(data):
    games = parse_data(data)
    offset = 10_000_000_000_000
    TOT = 0
    for game in games:
        # print(game)
        game["prize"] = [
            game["prize"][0] + offset,
            game["prize"][1] + offset,
        ]
        nTokens = play(game)
        # print(nTokens)
        TOT += nTokens

    return TOT


if __name__ == "__main__":
    with open("2024/13/data/13_test.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
