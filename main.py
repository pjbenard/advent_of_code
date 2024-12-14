import importlib

import AOC_utils as AOC

YEAR, DAY = 2024, 14

TEST = True
INPUT = True

PART_1 = True
PART_2 = True

if __name__ == "__main__":
    import_name = AOC.generate_module_name(YEAR, DAY)
    module = importlib.import_module(import_name)

    data_test, data_input = AOC.read_data(YEAR, DAY)
    data = {"TEST": data_test if TEST else [], "INPUT": data_input if INPUT else []}

    output = AOC.execute_parts(data, module, PART_1, PART_2)
    AOC.pretty_print_table(output)
