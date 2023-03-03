""" https://adventofcode.com/2021/day/2 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.moves: list[tuple[str, int]] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            moves = infile.readlines()

        for move in moves:
            move = move.strip().split()
            self.moves.append((move[0], int(move[1])))

    def part1(self) -> None:
        xpos = ypos = 0
        for direction, steps in self.moves:
            if direction == "forward":
                xpos += steps
            elif direction == "down":
                ypos += steps
            else:
                ypos -= steps

        result = xpos * ypos
        print(result)

    def part2(self) -> None:
        xpos = ypos = aim = 0
        for direction, steps in self.moves:
            if direction == "forward":
                xpos += steps
                ypos += aim * steps
            elif direction == "down":
                aim += steps
            else:
                aim -= steps

        result = xpos * ypos
        print(result)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
