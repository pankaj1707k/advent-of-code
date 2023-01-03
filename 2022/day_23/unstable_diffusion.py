""" https://adventofcode.com/2022/day/23 """

import os
from collections import defaultdict, deque
from copy import deepcopy


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.elves: set[tuple[int, int]] = set()
        self.dirs = {
            "N": (-1, 0),
            "S": (1, 0),
            "W": (0, -1),
            "E": (0, 1),
            "NW": (-1, -1),
            "NE": (-1, 1),
            "SW": (1, -1),
            "SE": (1, 1),
        }

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            lines = [line.strip() for line in infile.readlines()]

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == "#":
                    self.elves.add((row, col))

    def part1(self) -> None:
        dirs_order = deque(
            [["N", "NE", "NW"], ["S", "SE", "SW"], ["W", "NW", "SW"], ["E", "NE", "SE"]]
        )
        elves = deepcopy(self.elves)
        minrow = min(elf[0] for elf in elves)
        maxrow = max(elf[0] for elf in elves)
        mincol = min(elf[1] for elf in elves)
        maxcol = max(elf[1] for elf in elves)
        pos_elf_map: dict[tuple[int, int], list] = defaultdict(list)

        for _ in range(10):

            for er, ec in elves:
                if all(
                    (er + dr, ec + dc) not in elves for dr, dc in self.dirs.values()
                ):
                    # all 8 directions are free, do not move
                    continue

                # check for movement in 4 directions ordered by `dirs_order`
                for dirset in dirs_order:
                    # if all 3 positions in a direction are free,
                    # consider the mid position as a possible next position
                    if all(
                        (er + dr, ec + dc) not in elves
                        for dr, dc in [self.dirs[d] for d in dirset]
                    ):
                        dr, dc = self.dirs[dirset[0]]
                        pos_elf_map[(er + dr, ec + dc)].append((er, ec))
                        break

            for pos, elfset in pos_elf_map.items():
                # if more than one elves propose to move to
                # the same position do not move any of them
                if len(elfset) > 1:
                    continue
                # remove old position and add new one to simulate movement
                elves.remove(elfset[0])
                elves.add(pos)

            # update boundary parameters
            minrow = min(elf[0] for elf in elves)
            maxrow = max(elf[0] for elf in elves)
            mincol = min(elf[1] for elf in elves)
            maxcol = max(elf[1] for elf in elves)

            # the first direction considered moves at the end
            dirs_order.append(dirs_order.popleft())
            pos_elf_map.clear()

        height = maxrow - minrow + 1
        width = maxcol - mincol + 1
        empty = height * width - len(elves)
        print(empty)

    def part2(self) -> None:
        dirs_order = deque(
            [["N", "NE", "NW"], ["S", "SE", "SW"], ["W", "NW", "SW"], ["E", "NE", "SE"]]
        )
        elves = deepcopy(self.elves)
        pos_elf_map: dict[tuple[int, int], list] = defaultdict(list)
        rounds = 0

        while True:
            elves_before = deepcopy(elves)

            for er, ec in elves:
                if all(
                    (er + dr, ec + dc) not in elves for dr, dc in self.dirs.values()
                ):
                    continue

                for dirset in dirs_order:
                    if all(
                        (er + dr, ec + dc) not in elves
                        for dr, dc in [self.dirs[d] for d in dirset]
                    ):
                        dr, dc = self.dirs[dirset[0]]
                        pos_elf_map[(er + dr, ec + dc)].append((er, ec))
                        break

            for pos, elfset in pos_elf_map.items():
                if len(elfset) > 1:
                    continue
                elves.remove(elfset[0])
                elves.add(pos)

            dirs_order.append(dirs_order.popleft())
            pos_elf_map.clear()
            rounds += 1

            if elves == elves_before:
                break

        print(rounds)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
