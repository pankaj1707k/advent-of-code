""" https://adventofcode.com/2021/day/7 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        # horizontal positions of crabs
        self.crabs: list[int] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            self.crabs = list(map(int, infile.readline().strip().split(",")))

    def get_const_fuel_req(self, crabs: list[int], pos: int) -> int:
        return sum(abs(crab_pos - pos) for crab_pos in crabs)

    def get_var_fuel_req(self, crabs: list[int], pos: int) -> int:
        fuel = 0
        for crab in crabs:
            n = abs(crab - pos)
            fuel += n * (n + 1) // 2
        return fuel

    def part1(self) -> None:
        # optimal fuel cost is achieved at the median
        # time: O(nlogn) [dominated by sorting]
        sorted_crabs = sorted(self.crabs)
        total_crabs = len(self.crabs)
        mid = total_crabs >> 1
        if total_crabs & 1:
            optimal_pos = sorted_crabs[mid]
            fuel_req = self.get_const_fuel_req(sorted_crabs, optimal_pos)
            print(fuel_req)
        else:
            fuel_req_1 = self.get_const_fuel_req(sorted_crabs, sorted_crabs[mid])
            fuel_req_2 = self.get_const_fuel_req(sorted_crabs, sorted_crabs[mid - 1])
            print(min(fuel_req_1, fuel_req_2))

    def part2(self) -> None:
        # try every position from min to max
        # Time: O(n**2) [array size and (max-min) is order of 1000]
        min_fuel = float("inf")
        for pos in range(min(self.crabs), max(self.crabs) + 1):
            fuel_req = self.get_var_fuel_req(self.crabs, pos)
            min_fuel = min(min_fuel, fuel_req)

        print(min_fuel)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
