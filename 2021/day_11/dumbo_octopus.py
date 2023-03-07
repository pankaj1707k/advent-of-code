""" https://adventofcode.com/2021/day/11 """

import os
from collections import deque


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.grid: list[list[int]] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                self.grid.append(list(map(int, list(line.strip()))))

    def get_flash_count(self, grid: list[list[int]]) -> int:
        n = len(grid)

        # increment energies of all octopuses
        for i in range(n):
            for j in range(n):
                grid[i][j] += 1

        # identify which will flash and start a multi-source BFS
        que = deque()
        flashed = set()
        for i in range(n):
            for j in range(n):
                if grid[i][j] > 9:
                    que.append((i, j))
        dirs = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        while que:
            r, c = que.popleft()
            if (r, c) in flashed:
                continue
            flashed.add((r, c))
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if nr >= 0 and nc >= 0 and nr < n and nc < n:
                    grid[nr][nc] += 1
                    if grid[nr][nc] > 9:
                        que.append((nr, nc))

        # reset energy of flashed octopuses to 0
        for i, j in flashed:
            grid[i][j] = 0

        return len(flashed)

    def part1(self) -> None:
        total_flashes = 0
        n = len(self.grid)
        grid = [[self.grid[i][j] for j in range(n)] for i in range(n)]
        for _ in range(100):
            total_flashes += self.get_flash_count(grid)
        print(total_flashes)

    def part2(self) -> None:
        n = len(self.grid)
        grid = [[self.grid[i][j] for j in range(n)] for i in range(n)]
        steps = 0
        while True:
            flashes = self.get_flash_count(grid)
            steps += 1
            if flashes == n * n:
                break
        print(steps)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
