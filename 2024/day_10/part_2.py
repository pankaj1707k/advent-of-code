""" https://adventofcode.com/2024/day/10 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def search(row: int, col: int, grid: list[list[int]]) -> int:
    if grid[row][col] == 9:
        return 1
    score = 0
    for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        nr, nc = row + dr, col + dc
        if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[nr]):
            continue
        if grid[nr][nc] - grid[row][col] == 1:
            score += search(nr, nc, grid)
    return score


def main():
    grid: list[list[int]]

    with open(get_file_path("input.txt")) as fd:
        grid = [list(map(int, list(line.rstrip()))) for line in fd.readlines()]

    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                result += search(i, j, grid)

    print(result)


main()
