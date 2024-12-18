from tqdm import tqdm


def parse_data(data):
    registers = list(map(int, [line.split()[-1] for line in data[:3]]))
    program = list(map(int, data[-1].split()[-1].split(",")))

    return registers, program


def combo(operand, registers):
    return operand if operand < 4 else registers[operand % 4]


def regdv(registers, operand, id_reg):
    num = registers[0]
    den = 2 ** combo(operand, registers)
    res = num // den
    registers[id_reg] = res


def adv(registers, operand):
    regdv(registers, operand, 0)


def bxl(registers, operand):
    registers[1] ^= operand


def bst(registers, operand):
    registers[1] = combo(operand, registers) % 8


def jnz(registers, operand):
    return -1 if registers[0] == 0 else operand


def bxc(registers, operand):
    registers[1] ^= registers[2]


def out(registers, operand):
    return combo(operand, registers) % 8


def bdv(registers, operand):
    regdv(registers, operand, 1)


def cdv(registers, operand):
    regdv(registers, operand, 2)


def run_program(registers, program, isPart2=False):
    instructions = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    output = []

    # print(f"{registers = }")
    # print(f"{program = }")
    id_inst = 0
    while id_inst < len(program):
        # print(f"{id_inst = }")
        inst = instructions[program[id_inst]]
        operand = program[id_inst + 1]
        # print(f"instruction = {inst.__name__}, {operand = }")
        if inst == jnz:
            res = inst(registers, operand)
            id_inst = id_inst if res == -1 else operand - 2
        elif inst == out:
            res = inst(registers, operand)
            output.append(res)
            print(registers)
            return output
            if isPart2 and (len(output) > len(program)):
                return output
            # print(f"{output = }")
        else:
            inst(registers, operand)
        id_inst += 2
        # print(f"{registers = }")
        # print(f"id_inst post cycle = {id_inst}")
        # print()

    return output


def part1(data):
    registers, program = parse_data(data)
    print(f"{program = }")
    print(f"{registers = }")

    output = run_program(registers, program)

    return ",".join(map(str, output))


def part2_brute_force(data):
    registers, program = parse_data(data)
    print(f"{program = }")
    print(f"{registers = }")
    print()

    found = False
    A = 0
    # while not found:
    # for A in tqdm(range(32, 1_000_000_000, 64)):
    for A in tqdm(range(32, 500, 64)):
        newRegisters = registers[:]
        newRegisters[0] = A
        print(A)
        output = run_program(newRegisters, program, isPart2=True)
        print(output)
        # print(newRegisters)
        print()
        if len(output) != len(program):
            continue
        elif output == program:
            found = True
            break
        A += 1

    return A


def part2(data):
    # --> (A % 8) XOR ((A // 2**((A % 8) XOR 3)) % 8) = out XOR 6
    # Test for all 8 possibilities A in [0, 1, 2, 3, 4, 5, 6, 7]
    registers, program = parse_data(data)
    A = 0
    for out in program[::-1]:
        for i in range(8):
            value = i ^ ((A // (2 ** (i ^ 3))) % 8)
            if value == (out ^ 6):
                A = A * 8 + i
                print(A)

    return A


if __name__ == "__main__":
    with open("2024/17/data/17_input.txt") as file:
        data = file.read().splitlines()

    res_p1 = part1(data)
    print(res_p1)

    res_p2 = part2(data)
    print(res_p2)


# program = 2,4,1,3,7,5,1,5,0,3,4,3,5,5,3,0
#  0: (2, 4) -> bst A %   8      to B
#  2: (1, 3) -> bxl B XOR 3      to B
#  4: (7, 5) -> cdv A //  (2**B) to C
#  6: (1, 5) -> bxl B XOR 5      to B
#  8: (0, 3) -> adv A //  (2**3) to A
# 10: (4, 3) -> bxc B XOR C      to B
# 12: (5, 5) -> out print(B % 8)
# 14: (3, 0) -> jnz if A != 0 : jump to 0

# A = 0b????????1000000

# It 0
#  0: (2, 4) -> bst A %   8      to B     [A0, A0%8, 0]
#  2: (1, 3) -> bxl B XOR 3      to B     [A0, (A0%8) XOR 3, 0]
#  4: (7, 5) -> cdv A //  (2**B) to C     [A0, B0, A0 // (2**B0)]
#  6: (1, 5) -> bxl B XOR 5      to B     [A0, B0 XOR 5, C0]
#  8: (0, 3) -> adv A //  (2**3) to A     [A0 // 8, B1, C0]
# 10: (4, 3) -> bxc B XOR C      to B     [A1, B1 XOR C0, C0]
# 12: (5, 5) -> out print(B % 8)          [A1, B2, C0]
# 14: (3, 0) -> jnz if A != 0 : jump to 0 [A1, B2, C0]

# 12: B2 % 8 == 2 --> B2 = K2 * 8 + 2
# 10: B2 = B1 XOR C0 --> (B1%8) XOR (C0%8) = 2, (B1//8) XOR (C0//8) = K2
#  8: A1 = A0 // 8
#  6: B1 = B0 XOR 0b101 -> B0 = B1 XOR 0b101
#  4: C0 = A0 // (2**B0)
#  2: B0 = 0 XOR 3 -> B0 = 3
#  4: C0 = A0 // 8 = 4 + 8K
#  6: B1 = 0b011 XOR 0b101 = 6
#  8: A1 = A0 // 8 = 4 + 8K
# 10: B2 = 0b110 XOR (C0%8) = 0b010 --> (A0//8)%8 = 0b010 XOR 0b110 = 0b100
# ===> A0 = (4 + 8K2) * 8 = 32 + 64K2
# END of round 1: [A1, B2, C0] = [4 + 8K, 2 + 8K, 4 + 8K]

# [4 + 8K1, 2 + 8K1, 4 + 8K1]
#  0: B = (4 + 8K1) // 8 = K1
#  2: B0 = K1 XOR 3 -> B0 =
#  4: C0 = A0 // (2**B0)
#  6: B1 = B0 XOR 0b101
#  8: A1 = A0 // 8 = K1
# 10: B2 = B1 XOR C0 = 0b010 --> (A0//8)%8 = 0b010 XOR 0b110 = 0b100
# ===> A0 = 32 + 64K
# END of round 2: [A1, B2, C0] = [4 + 8K, 2 + 8K, 4 + 8K]
