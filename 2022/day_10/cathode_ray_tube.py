""" https://adventofcode.com/2022/day/10 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input() -> list[list[str | int]]:
    instructions = list()
    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            instructions.append(line.strip().split())
            if len(instructions[-1]) == 2:
                instructions[-1][1] = int(instructions[-1][1])
    return instructions


def part_1():
    cycle = 1
    xval = 1
    signal_sum = 0
    pivots = {20, 60, 100, 140, 180, 220}
    for instruction in instructions:
        if cycle > 220:
            break
        if cycle in pivots:
            signal_sum += xval * cycle
        elif cycle + 1 in pivots and instruction[0] == "addx":
            signal_sum += xval * (cycle + 1)
        if instruction[0] == "noop":
            cycle += 1
        else:
            xval += instruction[1]
            cycle += 2
    return signal_sum


def part_2():
    xval, cycle = 1, 0
    rows = [["." for __ in range(40)] for _ in range(6)]

    for instruction in instructions:
        if instruction[0] == "noop":
            cycle += 1
            if (cycle - 1) % 40 in {xval - 1, xval, xval + 1}:
                rows[(cycle - 1) // 40][(cycle - 1) % 40] = "#"
        else:
            cycle += 1
            if (cycle - 1) % 40 in {xval - 1, xval, xval + 1}:
                rows[(cycle - 1) // 40][(cycle - 1) % 40] = "#"
            cycle += 1
            if (cycle - 1) % 40 in {xval - 1, xval, xval + 1}:
                rows[(cycle - 1) // 40][(cycle - 1) % 40] = "#"
            xval += instruction[1]

    for row in rows:
        print("".join(row))


if __name__ == "__main__":
    instructions = parse_input()
    print(part_1())  # output: 17020
    part_2()  # RLEZFLGE
