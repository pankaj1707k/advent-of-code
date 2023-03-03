""" https://adventofcode.com/2021/day/6 """

import os
from collections import Counter


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.fish: list[int] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            self.fish = list(map(int, infile.readline().strip().split(",")))

    def count_fish(self, days: int) -> int:
        counts = Counter(self.fish)
        for _ in range(days):
            zero_initial = counts[0]
            for t in range(8):
                counts[t] = counts[t + 1]
            counts[6] += zero_initial
            counts[8] = zero_initial

        return counts.total()

    def part1(self) -> None:
        print(self.count_fish(80))

    def part2(self) -> None:
        print(self.count_fish(256))


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
