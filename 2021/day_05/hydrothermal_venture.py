""" https://adventofcode.com/2021/day/5 """

import os
from collections import Counter


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.lines: list[tuple[tuple[int, int], ...]] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                line = line.split(" -> ")
                line = tuple(tuple(map(int, point.split(","))) for point in line)
                self.lines.append(line)

    def get_overlap_count(self, ignore_diagonals: bool) -> int:
        points = Counter()
        for (x1, y1), (x2, y2) in self.lines:
            if ignore_diagonals and x1 != x2 and y1 != y2:
                continue
            x, y = x1, y1
            dx = 0 if x2 == x1 else (1 if x2 > x1 else -1)
            dy = 0 if y2 == y1 else (1 if y2 > y1 else -1)
            while True:
                points[(x, y)] += 1
                if x == x2 and y == y2:
                    break
                x += dx
                y += dy

        non_overlap_points = list(points.values()).count(1)
        overlap_points = len(points) - non_overlap_points
        return overlap_points

    def part1(self) -> None:
        print(self.get_overlap_count(ignore_diagonals=True))

    def part2(self) -> None:
        print(self.get_overlap_count(ignore_diagonals=False))


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
