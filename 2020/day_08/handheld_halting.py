""" https://adventofcode.com/2020/day/8 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    result = index = 0
    executed = set()
    while index < len(prog) and index not in executed:
        if prog[index][0] == "acc":
            result += prog[index][1]
        executed.add(index)
        index += prog[index][1] if prog[index][0] == "jmp" else 1
    print(result)


def check() -> int | None:
    result = index = 0
    executed = set()
    while index < len(prog) and index not in executed:
        if prog[index][0] == "acc":
            result += prog[index][1]
        executed.add(index)
        index += prog[index][1] if prog[index][0] == "jmp" else 1
    return result if index == len(prog) else None


def part2() -> None:
    result = 0
    for i in range(len(prog)):
        if prog[i][0] == "acc":
            continue
        prog[i][0] = "nop" if prog[i][0] == "jmp" else "jmp"
        value = check()
        if value != None:
            result = value
            break
        prog[i][0] = "nop" if prog[i][0] == "jmp" else "jmp"
    print(result)


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as fd:
        prog = [line.strip() for line in fd.readlines()]

    for i in range(len(prog)):
        op, arg = prog[i].split()
        prog[i] = [op, int(arg)]

    part1()
    part2()
