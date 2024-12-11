from time import perf_counter_ns


def generate_module_name(YEAR, DAY):
    return f"{YEAR}.{DAY:02d}"


def read_data_from_filename(filename):
    with open(filename, "r") as file:
        data = file.read().splitlines()

    return data


def read_data(YEAR, DAY):
    filename_test = f"{YEAR}/data/{DAY:02d}_test.txt"
    filename_input = f"{YEAR}/data/{DAY:02d}_input.txt"

    data_test = read_data_from_filename(filename_test)
    data_input = read_data_from_filename(filename_input)

    return data_test, data_input


def convert_time(time_ns):
    orders_of_magnitude = [
        (10**3, "ns"),
        (10**6, "µs"),
        (10**9, "ms"),
        (10**12, "s"),
    ]
    for coef, unit in orders_of_magnitude:
        if time_ns < coef:
            time_ns_str = f"{(time_ns * 10**3) / coef:5.1f} {unit}"
            break

    return time_ns_str


def print_time(time_ns):
    time_ns_str = convert_time(time_ns)
    print("Total time: approx.", time_ns_str)


def pretty_print_table(table):
    """
                 +-------------------------------------------+
                 |        PART 1       |        PART 2       |
    +------------+----------+----------+----------+----------+
    | Data types |  Result  |   Time   |  Result  |   Time   |
    +------------+----------+----------+----------+----------+
    |    TEST    | XXXXXXXX | XXX.X ms | XXXXXXXX | XXX.X ms |
    +------------+----------+----------+----------+----------+
    |    INPUT   | XXXXXXXX | XXX.X ms | XXXXXXXX | XXX.X ms |
    +------------+----------+----------+----------+----------+
    """
    n_data_types = len(table)
    n_cols = len(table[0])
    n_parts = (n_cols - 1) // 2
    table = [["Data types"] + ["Result", "Time"] * n_parts] + table

    max_len = []
    for col in range(len(table[0])):
        max_len_col = max(len(table[i][col]) for i in range(n_data_types + 1))
        max_len.append(max_len_col)

    # Header
    len_parts = [sum(max_len[2 * i + 1 : 2 * i + 3]) for i in range(n_parts)]
    start_space = " " * (max_len[0] + 3)
    print(start_space, end="")
    print("+" + "-" * (sum(len_parts) + 6 * n_parts - 1) + "+")
    print(start_space, end="")
    for id_part, len_part in enumerate(len_parts, start=1):
        print("|" + f"{'PART ' + str(id_part):^{len_part + 5}}", end="")
    print("|")

    # Rows
    inter_rows = ["-" * (max_len[i] + 2) for i in range(len(table[0]))]
    print("+", end="")
    print(*inter_rows, sep="+", end="")
    print("+")
    for row in table:
        print("|", end="")
        vals = [f"{row[id_col]:^{max_len[id_col] + 2}}" for id_col in range(n_cols)]
        print(*vals, sep="|", end="")
        print("|")
        print("+", end="")
        print(*inter_rows, sep="+", end="")
        print("+")


def execute_part(code, data, data_type):
    print(f"Data {data_type}")

    start = perf_counter_ns()
    res_test = code(data)
    end = perf_counter_ns()

    output_data = [str(res_test), convert_time(end - start)]
    return output_data


def execute_parts(data, module, PART_1, PART_2, TEST, INPUT):
    output_data = []
    if TEST:
        output_data.append(["TEST"])
        if PART_1:
            output = execute_part(module.part1, data["TEST"], "TEST 1")
            output_data[-1].extend(output)
        if PART_2:
            output = execute_part(module.part2, data["TEST"], "TEST 2")
            output_data[-1].extend(output)
    if INPUT:
        output_data.append(["INPUT"])
        if PART_1:
            output = execute_part(module.part1, data["INPUT"], "INPUT 1")
            output_data[-1].extend(output)
        if PART_2:
            output = execute_part(module.part2, data["INPUT"], "INPUT 2")
            output_data[-1].extend(output)

    return output_data


if __name__ == "__main__":
    table = [
        ["TEST", "36", "194.3 µs", "81", "154.7 µs"],
        ["INPUT", "550", "6.2 ms", "1255", "4.8 ms"],
    ]

    pretty_print_table(table)
