""" https://adventofcode.com/2021/day/1 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.depths: list[int] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                self.depths.append(int(line.strip()))

    def part1(self) -> None:
        increments = 0
        for i in range(1, len(self.depths)):
            if self.depths[i] > self.depths[i - 1]:
                increments += 1

        print(increments)

    def part2(self) -> None:
        increments = 0
        for i in range(3, len(self.depths)):
            if self.depths[i] > self.depths[i - 3]:
                increments += 1

        print(increments)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
