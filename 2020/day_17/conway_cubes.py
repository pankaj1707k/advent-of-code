""" https://adventofcode.com/2020/day/17 """

import os
from collections import defaultdict


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    active = set()
    count = defaultdict(int)  # count of neighboring active cells

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "#":
                active.add((x, y, 0))

    # for each active cell, increment the count of active neighbors
    # for all its neighbors
    for x, y, z in active:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    npos = (x + dx, y + dy, z + dz)
                    if npos != (x, y, z):
                        count[npos] += 1

    for _ in range(6):
        new_active = set()

        for pos, active_count in count.items():
            if pos in active and active_count in {2, 3}:
                new_active.add(pos)
            elif pos not in active and active_count == 3:
                new_active.add(pos)

        active = new_active
        count.clear()

        # update the count of actives for each cell
        for x, y, z in active:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    for dz in range(-1, 2):
                        npos = (x + dx, y + dy, z + dz)
                        if npos != (x, y, z):
                            count[npos] += 1

    print(len(active))


def part2() -> None:
    active = set()
    count = defaultdict(int)  # count of neighboring active cells

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "#":
                active.add((x, y, 0, 0))

    # for each active cell, increment the count of active neighbors
    # for all its neighbors
    for x, y, z, w in active:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    for dw in range(-1, 2):
                        npos = (x + dx, y + dy, z + dz, w + dw)
                        if npos != (x, y, z, w):
                            count[npos] += 1

    for _ in range(6):
        new_active = set()

        for pos, active_count in count.items():
            if pos in active and active_count in {2, 3}:
                new_active.add(pos)
            elif pos not in active and active_count == 3:
                new_active.add(pos)

        active = new_active
        count.clear()

        # update the count of actives for each cell
        for x, y, z, w in active:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    for dz in range(-1, 2):
                        for dw in range(-1, 2):
                            npos = (x + dx, y + dy, z + dz, w + dw)
                            if npos != (x, y, z, w):
                                count[npos] += 1

    print(len(active))


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as fd:
        grid = [line.strip() for line in fd.readlines()]

    part1()
    part2()
