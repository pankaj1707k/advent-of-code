""" https://adventofcode.com/2024/day/10 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def search(
    row: int, col: int, grid: list[list[int]], visited: set[tuple[int, int]]
) -> int:
    if (row, col) in visited:
        return 0
    visited.add((row, col))
    if grid[row][col] == 9:
        return 1
    score = 0
    for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        nr, nc = row + dr, col + dc
        if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[nr]):
            continue
        if grid[nr][nc] - grid[row][col] == 1:
            score += search(nr, nc, grid, visited)
    return score


def main():
    grid: list[list[int]]

    with open(get_file_path("input.txt")) as fd:
        grid = [list(map(int, list(line.rstrip()))) for line in fd.readlines()]

    result = 0
    visited: set[tuple[int, int]] = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                visited.clear()
                result += search(i, j, grid, visited)

    print(result)


main()
