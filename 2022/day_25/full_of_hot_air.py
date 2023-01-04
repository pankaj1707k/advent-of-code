""" https://adventofcode.com/2022/day/25 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.snafu: list[str] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            self.snafu = [line.strip() for line in infile.readlines()]

    def part1(self) -> None:
        decimal_sum = 0
        for num in self.snafu:
            decimal = 0
            for p, digit in enumerate(num[::-1]):
                if digit == "-":
                    decimal += -1 * (5**p)
                elif digit == "=":
                    decimal += -2 * (5**p)
                else:
                    decimal += int(digit) * (5**p)
            decimal_sum += decimal

        snafu_sum = ""
        while decimal_sum:
            rem = decimal_sum % 5
            decimal_sum //= 5

            if rem <= 2:
                snafu_sum = f"{rem}" + snafu_sum
            elif rem == 3:
                snafu_sum = "=" + snafu_sum
                decimal_sum += 1
            else:
                snafu_sum = "-" + snafu_sum
                decimal_sum += 1

        print(snafu_sum)

    def part2(self) -> None:
        """
        Started the blender to make the smoothie and the expedition is over!
        """


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
