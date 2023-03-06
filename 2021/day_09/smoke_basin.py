""" https://adventofcode.com/2021/day/9 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.hmap: list[list[int]] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                self.hmap.append(list(map(int, list(line.strip()))))

    def get_lowest_points(self) -> list[tuple[int, int]]:
        lowest_points = []
        m, n = len(self.hmap), len(self.hmap[0])
        for r in range(m):
            for c in range(n):
                if (
                    (r == 0 or self.hmap[r - 1][c] > self.hmap[r][c])
                    and (c == 0 or self.hmap[r][c - 1] > self.hmap[r][c])
                    and (r == m - 1 or self.hmap[r + 1][c] > self.hmap[r][c])
                    and (c == n - 1 or self.hmap[r][c + 1] > self.hmap[r][c])
                ):
                    lowest_points.append((r, c))
        return lowest_points

    def in_bounds(self, row: int, col: int) -> bool:
        m, n = len(self.hmap), len(self.hmap[0])
        return row >= 0 and col >= 0 and row < m and col < n

    def dfs(self, row: int, col: int, visited: set[tuple[int, int]]) -> int:
        visited.add((row, col))
        count = 1
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nrow, ncol = row + dr, col + dc
            if (
                self.in_bounds(nrow, ncol)
                and self.hmap[nrow][ncol] > self.hmap[row][col]
                and (nrow, ncol) not in visited
                and self.hmap[nrow][ncol] != 9
            ):
                count += self.dfs(nrow, ncol, visited)
        return count

    def part1(self) -> None:
        lowest_points = self.get_lowest_points()
        risk_sum = sum([self.hmap[r][c] for r, c in lowest_points]) + len(lowest_points)
        print(risk_sum)

    def part2(self) -> None:
        lowest_points = self.get_lowest_points()
        visited = set()
        basin_lengths = []
        for sr, sc in lowest_points:
            basin_lengths.append(self.dfs(sr, sc, visited))
        basin_lengths.sort(reverse=True)
        print(basin_lengths[0] * basin_lengths[1] * basin_lengths[2])


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
