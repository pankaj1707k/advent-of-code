""" https://adventofcode.com/2022/day/12 """

import os
from queue import PriorityQueue


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input() -> list[str]:
    grid: list[str] = list()
    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            grid.append(line.strip())
    return grid


def get_height(row: int, col: int) -> int:
    if grid[row][col] == "S":
        return 0
    if grid[row][col] == "E":
        return 25
    return ord(grid[row][col]) - ord("a")


def min_steps(start: tuple[int, int], end: tuple[int, int]) -> int:
    M, N = len(grid), len(grid[0])
    visited = set()
    pq = PriorityQueue()
    pq.put((0, start))
    while not pq.empty():
        steps, (row, col) = pq.get()
        if (row, col) in visited:
            continue
        visited.add((row, col))
        if (row, col) == end:
            return steps
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            new_row, new_col = row + dr, col + dc
            if new_row >= 0 and new_row < M and new_col >= 0 and new_col < N:
                if get_height(new_row, new_col) - get_height(row, col) <= 1:
                    pq.put((steps + 1, (new_row, new_col)))

    return 1000000009


def part_1():
    start = end = None
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S":
                start = (row, col)
            elif grid[row][col] == "E":
                end = (row, col)
        if start and end:
            break

    print(min_steps(start, end))


def part_2():
    end = None
    starts = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "E":
                end = (row, col)
            elif grid[row][col] in {"S", "a"}:
                starts.append((row, col))

    result = 1000000009
    for start in starts:
        result = min(result, min_steps(start, end))

    print(result)


if __name__ == "__main__":
    grid = parse_input()
    part_1()  # 330
    part_2()  # 321
