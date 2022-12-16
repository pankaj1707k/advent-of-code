""" https://adventofcode.com/2022/day/5 """

import os
from collections import defaultdict, deque
from copy import deepcopy


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input():
    stacks = defaultdict(deque)
    operations = list()

    with open(get_file_path("input.txt")) as infile:
        rstream = infile.readlines()
        line_index = 0

        for line in rstream:
            if line[1].isdigit():
                break
            for i in range(1, len(line), 4):
                stack_num = (i // 4) + 1
                if line[i].isalpha():
                    stacks[stack_num].appendleft(line[i])
            line_index += 1

        for line in rstream[line_index + 2 :]:
            _as_list = line.strip().split()
            operation = {
                "count": int(_as_list[1]),
                "src": int(_as_list[3]),
                "dest": int(_as_list[5]),
            }
            operations.append(operation)

    return stacks, operations


def part_1(stacks: dict[int, deque[str]], operations: list[dict[str, int]]) -> str:
    for op in operations:
        for _ in range(op["count"]):
            stacks[op["dest"]].append(stacks[op["src"]].pop())

    return "".join(stacks[i][-1] for i in range(1, len(stacks) + 1))


def part_2(stacks: dict[int, deque[str]], operations: list[dict[str, int]]) -> str:
    for op in operations:
        intermediate = [stacks[op["src"]].pop() for _ in range(op["count"])]
        intermediate.reverse()
        stacks[op["dest"]].extend(intermediate)

    return "".join(stacks[i][-1] for i in range(1, len(stacks) + 1))


if __name__ == "__main__":
    stacks, operations = parse_input()

    print("Part 1:", part_1(deepcopy(stacks), deepcopy(operations)))
    # output: DHBJQJCCW

    print("Part 2:", part_2(deepcopy(stacks), deepcopy(operations)))
    # output: WJVRLSJJT
