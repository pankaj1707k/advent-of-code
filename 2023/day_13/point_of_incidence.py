""" https://adventofcode.com/2023/day/13 """

import os
from typing import Callable


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def check_column_divider(pattern: list[str], col: int, tolerance: int) -> bool:
    m = len(pattern)
    n = len(pattern[0])
    l, r = col, col + 1
    errors = 0
    while l >= 0 and r < n:
        errors += sum(int(pattern[i][l] != pattern[i][r]) for i in range(m))
        if errors > tolerance:
            return False
        l -= 1
        r += 1
    return errors == tolerance


def check_row_divider(pattern: list[str], row: int, tolerance: int) -> bool:
    m, n = len(pattern), len(pattern[0])
    l, r = row, row + 1
    errors = 0
    while l >= 0 and r < m:
        errors += sum(int(pattern[l][j] != pattern[r][j]) for j in range(n))
        if errors > tolerance:
            return False
        l -= 1
        r += 1
    return errors == tolerance


def summary(pattern: list[str], smudge: int) -> int:
    m = len(pattern)
    n = len(pattern[0])

    for c in range(n - 1):
        if check_column_divider(pattern, c, smudge):
            return c + 1

    for r in range(m - 1):
        if check_row_divider(pattern, r, smudge):
            return 100 * (r + 1)


def part1() -> None:
    result = 0

    for pattern in patterns:
        result += summary(pattern, 0)

    print(result)


def part2() -> None:
    result = 0

    for pattern in patterns:
        result += summary(pattern, 1)

    print(result)


if __name__ == "__main__":
    patterns: list[list[str]] = []

    with open(get_file_path("input.txt")) as infile:
        for pattern in infile.read().split("\n\n"):
            patterns.append(pattern.splitlines())

    part1()
    part2()
