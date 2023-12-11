""" https://adventofcode.com/2023/day/11 """

import os
from itertools import combinations


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def get_empty_rows() -> set[int]:
    row_nums = set()
    m = len(universe[0])
    for rn in range(len(universe)):
        if universe[rn] == "." * m:
            row_nums.add(rn)
    return row_nums


def get_empty_cols() -> set[int]:
    col_nums = set()
    n = len(universe)
    for cn in range(len(universe[0])):
        if all(universe[rn][cn] == "." for rn in range(n)):
            col_nums.add(cn)
    return col_nums


def get_galaxy_pos() -> list[tuple[int, int]]:
    pos = []
    for rn, row in enumerate(universe):
        for cn, char in enumerate(row):
            if char == "#":
                pos.append((rn, cn))
    return pos


def eval_total_distance(expansion_factor: int) -> int:
    empty_rows = get_empty_rows()
    empty_cols = get_empty_cols()
    galaxies = get_galaxy_pos()
    total_dist = 0

    for g0, g1 in combinations(galaxies, 2):
        drow = abs(g0[0] - g1[0])
        dcol = abs(g0[1] - g1[1])
        dist = drow + dcol
        for irow in range(min(g0[0], g1[0]), max(g0[0], g1[0])):
            if irow in empty_rows:
                dist += expansion_factor - 1
        for icol in range(min(g0[1], g1[1]), max(g0[1], g1[1])):
            if icol in empty_cols:
                dist += expansion_factor - 1
        total_dist += dist

    return total_dist


def part1() -> None:
    total_dist = eval_total_distance(2)
    print(total_dist)


def part2() -> None:
    total_dist = eval_total_distance(1000000)
    print(total_dist)


if __name__ == "__main__":
    universe: list[str] = list()

    with open(get_file_path("input.txt")) as infile:
        for line in infile.read().splitlines():
            universe.append(line)

    part1()
    part2()
