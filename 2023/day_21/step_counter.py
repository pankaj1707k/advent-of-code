""" https://adventofcode.com/2023/day/21 """

import os
from collections import deque


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def get_start_pos() -> tuple[int, int]:
    for rownum, row in enumerate(plotmap):
        if "S" in row:
            return (rownum, row.index("S"))


def part1() -> None:
    que = deque()
    que.append((*get_start_pos(), 0))
    visited = set()
    result = 0

    while que:
        row, col, steps = que.popleft()
        if steps > 64:
            continue
        if (row, col) in visited:
            continue
        visited.add((row, col))
        if steps % 2 == 0:
            result += 1
        for dr, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nr, nc = row + dr, col + dc
            if nr >= 0 and nc >= 0 and nr < N and nc < N and plotmap[nr][nc] == ".":
                que.append((nr, nc, steps + 1))

    print(result)


def part2() -> None:
    que = deque()
    que.append((*get_start_pos(), 0))
    visited = set()
    sample_values = {65: 0, 65 + 131: 0, 65 + 2 * 131: 0}

    while que:
        row, col, steps = que.popleft()
        if steps > 65 + 2 * 131:
            continue
        if (row, col) in visited:
            continue
        visited.add((row, col))
        sample_values[65 + 131] += int(steps <= 65 + 131 and steps % 2 == 0)
        sample_values[65] += int(steps <= 65 and steps % 2 == 1)
        sample_values[65 + 2 * 131] += int(steps <= 65 + 2 * 131 and steps % 2 == 1)
        for dr, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nr, nc = row + dr, col + dc
            if plotmap[nr % N][nc % N] != "#":
                que.append((nr, nc, steps + 1))

    print(sample_values)

    # Computed using:
    # Let f(x) = ax^2 + bx + c; we have f(0), f(1), f(2)
    extrapol_func = lambda x: 14655 * x * x + 14775 * x + 3720

    xval = 26501365 // 131
    result = extrapol_func(xval)
    print(result)


if __name__ == "__main__":
    plotmap: list[str] = list()

    with open(get_file_path("input.txt")) as infile:
        plotmap = infile.read().strip().splitlines()

    N = len(plotmap)

    part1()
    part2()
