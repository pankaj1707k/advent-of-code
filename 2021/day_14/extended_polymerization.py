""" https://adventofcode.com/2021/day/14 """

import os
from collections import Counter, defaultdict


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.template: str = ""
        self.rules: dict[str, str] = defaultdict(lambda: "")

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            lines = [l.strip() for l in infile.readlines()]

        self.template = lines[0]
        for i in range(2, len(lines)):
            line = lines[i].split(" -> ")
            self.rules[line[0]] = line[1]

    def part1(self) -> None:
        polymer = self.template
        for _ in range(10):
            new_polymer = polymer[0]
            for i in range(1, len(polymer)):
                pair = polymer[i - 1] + polymer[i]
                new_polymer += self.rules[pair] + polymer[i]
            polymer = new_polymer

        char_counts = Counter(polymer)
        result = max(char_counts.values()) - min(char_counts.values())
        print(result)

    def part2(self) -> None:
        pair_counts = Counter()
        char_counts = Counter(self.template)
        # initialize with count of pairs in template
        for i in range(len(self.template) - 1):
            pair = self.template[i] + self.template[i + 1]
            pair_counts[pair] += 1

        for _ in range(40):
            pairs = pair_counts.copy()
            for pair, count in pairs.items():
                if count == 0:
                    continue
                char_counts[self.rules[pair]] += count
                pair_counts[pair[0] + self.rules[pair]] += count
                pair_counts[self.rules[pair] + pair[1]] += count
                pair_counts[pair] -= count

        result = max(char_counts.values()) - min(char_counts.values())
        print(result)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
