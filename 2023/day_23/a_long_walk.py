""" https://adventofcode.com/2023/day/23 """

import os
import sys

sys.setrecursionlimit(100000000)


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def dfs(row: int, col: int, steps: int, visited: set[tuple[int, int]]) -> int:
    if row == len(grid) - 1 and col == len(grid[0]) - 2:
        return steps
    if (row, col) in visited:
        return 0
    visited.add((row, col))
    steps += 1
    max_steps = 0
    if grid[row][col] == ">":
        max_steps = max(max_steps, dfs(row, col + 1, steps, visited))
    elif grid[row][col] == "v":
        max_steps = max(max_steps, dfs(row + 1, col, steps, visited))
    elif grid[row][col] == "<":
        max_steps = max(max_steps, dfs(row, col - 1, steps, visited))
    elif grid[row][col] == "^":
        max_steps = max(max_steps, dfs(row - 1, col, steps, visited))
    else:
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if (
                nr >= 0
                and nc >= 0
                and nr < len(grid)
                and nc < len(grid)
                and grid[nr][nc] != "#"
            ):
                max_steps = max(max_steps, dfs(nr, nc, steps, visited))
    visited.discard((row, col))
    return max_steps


def part1() -> None:
    print(dfs(0, 1, 0, set()))


def part2() -> None:
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    nodes = {(0, 1), (len(grid) - 1, len(grid[0]) - 2)}

    for row in range(1, len(grid)):
        for col in range(1, len(grid)):
            if grid[row][col] == "#":
                continue
            # count number of path options that could be taken from (row, col)
            options = 0
            for dr, dc in dirs:
                nr, nc = row + dr, col + dc
                if (
                    nr >= 0
                    and nc >= 0
                    and nr < len(grid)
                    and nc < len(grid)
                    and grid[nr][nc] != "#"
                ):
                    options += 1
            if options >= 3:
                nodes.add((row, col))

    graph = {node: {} for node in nodes}

    for sr, sc in nodes:
        stack: list[tuple[int, int, int]] = [(0, sr, sc)]  # (distance, row, col)
        visited: set[tuple[int, int]] = {(sr, sc)}

        while stack:
            dist, row, col = stack.pop()
            if dist > 0 and (row, col) in nodes:
                graph[(sr, sc)][(row, col)] = dist
                continue
            for dr, dc in dirs:
                nr, nc = row + dr, col + dc
                if (
                    nr >= 0
                    and nc >= 0
                    and nr < len(grid)
                    and nc < len(grid)
                    and grid[nr][nc] != "#"
                    and (nr, nc) not in visited
                ):
                    stack.append((dist + 1, nr, nc))
                    visited.add((nr, nc))


    def _dfs(node: tuple[int, int], visited: set[tuple[int, int]]) -> int:
        if node == (len(grid) - 1, len(grid[0]) - 2):
            return 0
        max_dist = -(1 << 32)
        visited.add(node)
        for other in graph[node]:
            if other not in visited:
                max_dist = max(max_dist, graph[node][other] + _dfs(other, visited))
        visited.remove(node)
        return max_dist

    result = _dfs((0, 1), set())
    print(result)


if __name__ == "__main__":
    grid: list[str] = list()

    with open(get_file_path("input.txt")) as infile:
        grid = infile.read().strip().splitlines()

    part1()
    part2()
