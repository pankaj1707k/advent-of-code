""" https://adventofcode.com/2023/day/14 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def tilt_north(grid: list[list[str]]) -> None:
    for c in range(len(grid[0])):
        for r in range(len(grid)):
            if grid[r][c] == "O":
                nr = r - 1
                while nr >= 0 and grid[nr][c] == ".":
                    nr -= 1
                if nr + 1 >= 0:
                    grid[nr + 1][c] = "O"
                if nr + 1 != r:
                    grid[r][c] = "."


def tilt_west(grid: list[list[str]]) -> None:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "O":
                nc = c - 1
                while nc >= 0 and grid[r][nc] == ".":
                    nc -= 1
                if nc + 1 >= 0:
                    grid[r][nc + 1] = "O"
                if nc + 1 != c:
                    grid[r][c] = "."


def tilt_south(grid: list[list[str]]) -> None:
    for c in range(len(grid[0])):
        for r in range(len(grid) - 1, -1, -1):
            if grid[r][c] == "O":
                nr = r + 1
                while nr < len(grid) and grid[nr][c] == ".":
                    nr += 1
                if nr - 1 < len(grid):
                    grid[nr - 1][c] = "O"
                if nr - 1 != r:
                    grid[r][c] = "."


def tilt_east(grid: list[list[str]]) -> None:
    for r in range(len(grid)):
        for c in range(len(grid[0]) - 1, -1, -1):
            if grid[r][c] == "O":
                nc = c + 1
                while nc < len(grid[0]) and grid[r][nc] == ".":
                    nc += 1
                if nc - 1 < len(grid[0]):
                    grid[r][nc - 1] = "O"
                if nc - 1 != c:
                    grid[r][c] = "."


def cycle(grid: list[list[str]]) -> None:
    tilt_north(grid)
    tilt_west(grid)
    tilt_south(grid)
    tilt_east(grid)


def part1() -> None:
    grid = [[c for c in row] for row in platform]
    m = len(grid)
    result = 0
    tilt_north(grid)
    for r in range(m):
        rocks = grid[r].count("O")
        result += rocks * (m - r)
    print(result)


def key(grid: list[list[str]]) -> str:
    return "".join("".join(row) for row in grid)


def part2() -> None:
    cycle_count = 0
    MAX_COUNT = 10**9
    grid = [[c for c in row] for row in platform]
    seen = {}

    while True:
        cycle(grid)
        cycle_count += 1
        gkey = key(grid)
        if gkey in seen:
            sub = seen[gkey]
            break
        seen[gkey] = cycle_count

    for _ in range((MAX_COUNT - sub) % (cycle_count - sub)):
        cycle(grid)

    load = 0
    for r in range(len(grid)):
        rocks = grid[r].count("O")
        load += rocks * (len(grid) - r)

    print(load)


if __name__ == "__main__":
    platform: list[list[str]] = list()

    with open(get_file_path("input.txt")) as infile:
        for line in infile.read().splitlines():
            platform.append(list(line))

    part1()
    part2()
