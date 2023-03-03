""" https://adventofcode.com/2021/day/3 """

import os
from collections import Counter


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.bins: list[str] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                self.bins.append(line.strip())

    def part1(self) -> None:
        bit_counts = [[0, 0] for _ in range(len(self.bins[0]))]
        gamma_rate = epsilon_rate = ""

        for b in self.bins:
            for i, x in enumerate(b):
                bit_counts[i][int(x)] += 1

        for zero, one in bit_counts:
            if zero > one:
                gamma_rate += "0"
                epsilon_rate += "1"
            else:
                gamma_rate += "1"
                epsilon_rate += "0"

        gamma_rate = int(gamma_rate, 2)
        epsilon_rate = int(epsilon_rate, 2)
        power_consumption = gamma_rate * epsilon_rate
        print(power_consumption)

    def part2(self) -> None:
        # oxygen generator rating
        bins = self.bins
        bitpos = 0
        while len(bins) > 1:
            counter = Counter([bstring[bitpos] for bstring in bins])
            if counter["0"] == counter["1"]:
                most_common = "1"
            else:
                most_common = "1" if counter["1"] > counter["0"] else "0"
            bins = [bstring for bstring in bins if bstring[bitpos] == most_common]
            bitpos += 1
        oxygen_generator_rating = int(bins[0], 2)

        # CO2 scrubber rating
        bins = self.bins
        bitpos = 0
        while len(bins) > 1:
            counter = Counter([bstring[bitpos] for bstring in bins])
            if counter["0"] == counter["1"]:
                least_common = "0"
            else:
                least_common = "1" if counter["1"] < counter["0"] else "0"
            bins = [bstring for bstring in bins if bstring[bitpos] == least_common]
            bitpos += 1
        co2_scrubber_rating = int(bins[0], 2)

        life_support_rating = oxygen_generator_rating * co2_scrubber_rating
        print(life_support_rating)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
