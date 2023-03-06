""" https://adventofcode.com/2021/day/10 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.file: list[str] = []
        self.opening_chars = {"(", "[", "{", "<"}
        self.closing_chars = {")", "]", "}", ">"}
        self.corrupt_points = {")": 3, "]": 57, "}": 1197, ">": 25137}
        self.incomplete_points = {")": 1, "]": 2, "}": 3, ">": 4}
        self.matching_pairs = {
            ")": "(",
            "]": "[",
            "}": "{",
            ">": "<",
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">",
        }

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            self.file = [line.strip() for line in infile.readlines()]

    def part1(self) -> None:
        points = 0
        for line in self.file:
            stack = []
            for char in line:
                if char in self.opening_chars:
                    stack.append(char)
                elif not stack or self.matching_pairs[char] != stack[-1]:
                    points += self.corrupt_points[char]
                    break
                else:
                    stack.pop()

        print(points)

    def part2(self) -> None:
        scores = []
        for line in self.file:
            stack = []
            for char in line:
                if char in self.opening_chars:
                    stack.append(char)
                elif not stack or self.matching_pairs[char] != stack[-1]:
                    stack.clear()
                    break
                else:
                    stack.pop()
            score = 0
            while stack:
                closing_char = self.matching_pairs[stack.pop()]
                score *= 5
                score += self.incomplete_points[closing_char]
            if score > 0:
                scores.append(score)

        scores.sort()
        print(scores[len(scores) >> 1])


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
