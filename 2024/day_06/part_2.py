""" https://adventofcode.com/2024/day/6 """

from collections import defaultdict
import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def is_edge(grid: list[list[str]], row: int, col: int) -> bool:
    return row == 0 or row == len(grid) - 1 or col == 0 or col == len(grid[0]) - 1


def does_loop(grid: list[list[str]], row: int, col: int) -> bool:
    dr, dc = -1, 0
    pos_with_dirs: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    while not is_edge(grid, row, col):
        if (dr, dc) in pos_with_dirs[(row, col)]:
            return True
        pos_with_dirs[(row, col)].add((dr, dc))
        if grid[row + dr][col + dc] == "#":
            dr, dc = dc, -dr
        # after turning once, there could be another obstacle in the new direction
        if grid[row + dr][col + dc] == "#":
            dr, dc = dc, -dr
        row += dr
        col += dc
    return False


def main():
    grid: list[list[str]] = []
    srow, scol = -1, -1

    with open(get_file_path("input.txt")) as fd:
        grid = [list(l) for l in fd.readlines()]

    # find start pos
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "^":
                srow, scol = i, j
                break

    # brute force simulation by adding obstacles at all empty positions
    result = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] != ".":
                continue
            grid[r][c] = "#"
            if does_loop(grid, srow, scol):
                result += 1
            grid[r][c] = "."

    print(result)


main()
