def OR(x, y):
    return x | y


def AND(x, y):
    return x & y


def XOR(x, y):
    return x ^ y


d_operators = {"OR": OR, "AND": AND, "XOR": XOR}


def parse_data(data):
    idx_split = data.index("")
    inputs = {}
    for line in data[:idx_split]:
        name = line[:3]
        val = True if line[-1:] == "1" else False
        inputs[name] = val

    operations = []
    for line in data[idx_split + 1 :]:
        op1, operator, op2, _, res = line.split()
        operations.append(((op1, op2), d_operators[operator], res))

    return inputs, operations


def extract_number_z(inputs):
    inputs_z = [
        (name, int(val)) for name, val in inputs.items() if name.startswith("z")
    ]
    sorted_z = sorted(inputs_z, key=lambda i: i[0], reverse=True)
    # print(sorted_z)
    z_string = "0b" + "".join(list(map(str, [val for name, val in sorted_z])))
    # print(z_string)
    return int(z_string, base=2)


def part1(data):
    inputs, operations = parse_data(data)
    # print(inputs)

    idx_operation = 0
    while operations:
        (op1, op2), operator, res = operations[idx_operation]
        if (op1 in inputs) and (op2 in inputs):
            # print(op1, op2, res)
            res_val = operator(inputs[op1], inputs[op2])
            # print(res_val)
            inputs[res] = res_val
            operations.pop(idx_operation)

        idx_operation += 1
        idx_operation %= len(operations) if len(operations) else 1

    z_val = extract_number_z(inputs)
    return z_val


def part2(data):
    return


if __name__ == "__main__":
    YEAR, DAY = 2024, 24
    with open(f"{YEAR}/{DAY}/data/{DAY}_test2.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)
