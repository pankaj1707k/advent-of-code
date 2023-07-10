""" https://adventofcode.com/2020/day/3 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def count_trees(grid: list[str], right: int, down: int) -> int:
    m = len(grid)
    n = len(grid[0])
    trees = col = 0
    for row in range(down, m, down):
        col = (col + right) % n
        trees += int(grid[row][col] == "#")
    return trees


def part1(grid: list[str]) -> None:
    trees = count_trees(grid, 3, 1)
    print(trees)


def part2(grid: list[str]) -> None:
    slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
    result = 1
    for right, down in slopes:
        result *= count_trees(grid, right, down)
    print(result)


def main() -> None:
    with open(get_file_path("input.txt")) as fd:
        grid = [line.rstrip() for line in fd.readlines()]

    part1(grid)
    part2(grid)


if __name__ == "__main__":
    main()
