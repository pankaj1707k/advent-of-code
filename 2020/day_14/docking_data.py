""" https://adventofcode.com/2020/day/14 """

import os
import re


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    memory = {}
    mask = None

    for ins in init_prog:
        if len(ins) == 1:
            mask = ins[0]
            continue
        loc, value = ins
        for b in range(36):
            if mask[-b - 1] == "0":
                value &= ~(1 << b)
            elif mask[-b - 1] == "1":
                value |= 1 << b
        memory[loc] = value

    result = sum(memory.values())
    print(result)


def part2() -> None:
    memory = {}
    mask = None

    for ins in init_prog:
        if len(ins) == 1:
            mask = ins[0]
            continue

        loc, value = ins
        floating = []
        for b in range(36):
            if mask[-b - 1] == "X":
                floating.append(b)
            elif mask[-b - 1] == "1":
                loc |= 1 << b

        for com in range(1 << len(floating)):
            float_loc = loc
            for i, p in enumerate(floating):
                if com & (1 << i) == 0:
                    float_loc &= ~(1 << p)
                else:
                    float_loc |= 1 << p
            memory[float_loc] = value

    result = sum(memory.values())
    print(result)


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as fd:
        init_prog = [line.strip() for line in fd.readlines()]

    for index, line in enumerate(init_prog):
        _comps = re.split(r"mask\s=\s|mem\[|\]\s=\s", line)[1:]
        if len(_comps) == 2:
            _comps = list(map(int, _comps))
        init_prog[index] = _comps

    part1()
    part2()
