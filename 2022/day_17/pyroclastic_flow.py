""" https://adventofcode.com/2022/day/16 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        # relative structure coordinates for each rock
        self.rocks = [
            [(0, 0), (1, 0), (2, 0), (3, 0)],  # -
            [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],  # +
            [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # _|
            [(0, 0), (0, 1), (0, 2), (0, 3)],  # |
            [(0, 0), (0, 1), (1, 0), (1, 1)],  # []
        ]
        # horizontal movement parameters
        self.hmoves = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            line = infile.readline().strip()
        self.hmoves = [1 if char == ">" else -1 for char in line]

    def get_config(self, fixed: set[tuple[int, int]]) -> tuple[int]:
        config = [-30] * 7  # look for pattern in upto 30 rows below
        for x, y in fixed:
            config[x] = max(config[x], y)
        max_y = max(config)
        return tuple(max_y - y for y in config)

    def get_tower_height(self, max_rocks: int) -> int:
        height = rock_count = rock_index = 0
        # set of positions that have reached a steady state
        fixed = {(x, -1) for x in range(7)}
        rock = {(x + 2, y + height + 3) for x, y in self.rocks[rock_index]}
        skipped = 0
        seen = {}  # pattern of horizontal move, rock and top rows config

        while rock_count < max_rocks:
            for index, hmove in enumerate(self.hmoves):
                # horizontal movement
                new_pos = {(x + hmove, y) for x, y in rock}
                # check if position after movement does not overlap with the
                # walls and the steady structure formed till now
                if all(0 <= x < 7 for x, _ in new_pos) and not (new_pos & fixed):
                    rock = new_pos
                # vertical movement
                new_pos = {(x, y - 1) for x, y in rock}
                # overlap with steady structure
                if new_pos & fixed:
                    # include current rock in the steady structure
                    fixed |= rock
                    height = max(height - 1, max(y for _, y in rock)) + 1
                    rock_count += 1
                    if rock_count == max_rocks:
                        break
                    rock_index = (rock_index + 1) % 5
                    rock = {(x + 2, y + height + 3) for x, y in self.rocks[rock_index]}
                    # skip ahead by taking into account the height increments
                    # for the repeating pattern in one go
                    pattern = (index, rock_index, self.get_config(fixed))
                    if pattern in seen:
                        prev_rock_count, prev_height = seen[pattern]
                        # number of rocks yet to fall
                        rem_rocks = max_rocks - rock_count
                        # length of the repeated pattern in terms of rock count
                        pattern_length = rock_count - prev_rock_count
                        repetitions = rem_rocks // pattern_length
                        height_diff = height - prev_height
                        # total height gained in all repetitions of the pattern
                        skipped = height_diff * repetitions
                        rock_count += repetitions * pattern_length
                        # clear the pattern from cache so that it does not
                        # get considered multiple times
                        seen.clear()
                    # record the current pattern
                    seen[pattern] = (rock_count, height)
                else:
                    rock = new_pos

        return height + skipped

    def part1(self) -> None:
        print(self.get_tower_height(2022))

    def part2(self) -> None:
        print(self.get_tower_height(1000000000000))


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
