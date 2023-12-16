""" https://adventofcode.com/2023/day/16 """

import os
import sys
from collections import defaultdict

sys.setrecursionlimit(1000000)


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def dfs(
    row: int,
    col: int,
    drow: int,
    dcol: int,
    visited: dict[tuple[int, int], set[tuple[int, int]]],
) -> None:
    if row < 0 or col < 0 or row >= N or col >= N:
        return
    if (row, col) in visited and (drow, dcol) in visited[(row, col)]:
        return
    visited[(row, col)].add((drow, dcol))
    if grid[row][col] == ".":
        dfs(row + drow, col + dcol, drow, dcol, visited)
    elif grid[row][col] == "\\":
        if drow == 0 and dcol == 1:
            dfs(row + 1, col, 1, 0, visited)
        elif drow == -1 and dcol == 0:
            dfs(row, col - 1, 0, -1, visited)
        elif drow == 1 and dcol == 0:
            dfs(row, col + 1, 0, 1, visited)
        else:
            dfs(row - 1, col, -1, 0, visited)
    elif grid[row][col] == "/":
        if drow == 0 and dcol == 1:
            dfs(row - 1, col, -1, 0, visited)
        elif drow == -1 and dcol == 0:
            dfs(row, col + 1, 0, 1, visited)
        elif drow == 1 and dcol == 0:
            dfs(row, col - 1, 0, -1, visited)
        else:
            dfs(row + 1, col, 1, 0, visited)
    elif grid[row][col] == "|":
        if (drow, dcol) in {(1, 0), (-1, 0)}:
            dfs(row + drow, col, drow, dcol, visited)
        else:
            dfs(row - 1, col, -1, 0, visited)
            dfs(row + 1, col, 1, 0, visited)
    else:
        if (drow, dcol) in {(0, 1), (0, -1)}:
            dfs(row, col + dcol, drow, dcol, visited)
        else:
            dfs(row, col - 1, 0, -1, visited)
            dfs(row, col + 1, 0, 1, visited)


def part1() -> None:
    visited = defaultdict(set)
    dfs(0, 0, 0, 1, visited)
    print(len(visited))


def part2() -> None:
    visited = defaultdict(set)
    max_tiles = 0

    # top row
    for col in range(N):
        dfs(0, col, 1, 0, visited)
        max_tiles = max(max_tiles, len(visited))
        visited.clear()

    # bottom row
    for col in range(N):
        dfs(N - 1, col, -1, 0, visited)
        max_tiles = max(max_tiles, len(visited))
        visited.clear()

    # left column
    for row in range(N):
        dfs(row, 0, 0, 1, visited)
        max_tiles = max(max_tiles, len(visited))
        visited.clear()

    # right column
    for row in range(N):
        dfs(row, N - 1, 0, -1, visited)
        max_tiles = max(max_tiles, len(visited))
        visited.clear()

    print(max_tiles)


if __name__ == "__main__":
    grid: list[str] = list()

    with open(get_file_path("input.txt")) as infile:
        grid = infile.read().strip().splitlines()

    N = len(grid)

    part1()
    part2()
