""" https://adventofcode.com/2023/day/3 """

import os
from collections import defaultdict


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    part_nums = list()
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

    for ln, line in enumerate(schematic):
        not_symbols = set(".0123456789")
        is_part = False
        num = 0

        for idx, char in enumerate(line):
            if not char.isdigit():
                if num > 0 and is_part:
                    part_nums.append(num)
                num = 0
                is_part = False
                continue
            for dr, dc in directions:
                rn, cn = ln + dr, idx + dc
                is_part |= (
                    0 <= rn < len(schematic)
                    and 0 <= cn < len(line)
                    and schematic[rn][cn] not in not_symbols
                )
            num = num * 10 + int(char)

        if num > 0 and is_part:
            part_nums.append(num)

    result = sum(part_nums)
    print(result)


def check_walls(
    ln: int, start: int, end: int, gears: dict[tuple[int, int], list[int]], num: int
) -> None:
    # check upper row
    if ln > 0:
        for cn in range(start, end + 1):
            if schematic[ln - 1][cn] == "*":
                gears[(ln - 1, cn)].append(num)
    # check lower row
    if ln < len(schematic) - 1:
        for cn in range(start, end + 1):
            if schematic[ln + 1][cn] == "*":
                gears[(ln + 1, cn)].append(num)
    # check remaining surrounding cells
    for dr, dc in [(0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]:
        rn, cn = ln + dr, (start if dc == -1 else end) + dc
        if (
            0 <= rn < len(schematic)
            and 0 <= cn < len(line)
            and schematic[rn][cn] == "*"
        ):
            gears[(rn, cn)].append(num)


def part2() -> None:
    gears = defaultdict(list)

    for ln, line in enumerate(schematic):
        num = 0
        start, end = -1, 0
        for idx, char in enumerate(line):
            if char.isdigit():
                num = num * 10 + int(char)
                if start == -1:
                    start = idx
                end = idx
                continue
            if num == 0:
                continue
            check_walls(ln, start, end, gears, num)
            # reset
            num = 0
            start = end = -1
        if num > 0:
            check_walls(ln, start, end, gears, num)

    result = 0
    for nums in gears.values():
        if len(nums) == 2:
            result += nums[0] * nums[1]

    print(result)


if __name__ == "__main__":
    schematic: list[str] = list()

    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            schematic.append(line.strip())

    part1()
    part2()
