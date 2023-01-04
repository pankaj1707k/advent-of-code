""" https://adventofcode.com/2022/day/24 """

import math
import os
from collections import defaultdict, deque


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.billiards: dict[str, set[tuple[int, int]]] = defaultdict(set)
        self.start: tuple[int, int] = (-1, 0)
        self.end: tuple[int, int] = None
        self.billiard_moves = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            lines = [line.strip() for line in infile.readlines()]

        for row, line in enumerate(lines, start=-1):
            for col, char in enumerate(line, start=-1):
                if char in {"<", ">", "^", "v"}:
                    self.billiards[char].add((row, col))

        self.end = (len(lines) - 2, len(lines[0]) - 3)

    def get_min_time(
        self, start: tuple[int, int], end: tuple[int, int], start_time: int
    ) -> int:
        que = deque()  # (row, col, time)
        visited = set()  # (row, col, time % lcm)
        moves = ((1, 0), (0, 1), (-1, 0), (0, -1), (0, 0))
        min_time = None

        rowend, colend = self.end[0], self.end[1] + 1
        lcm = (rowend * colend) // math.gcd(rowend, colend)
        que.append((*start, start_time))

        while que:
            r, c, time = que.popleft()
            time += 1

            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                # mission successful :)
                if (nr, nc) == end:
                    min_time = time
                    que.clear()
                    break
                # out of bounds check
                if (nr, nc) != start and (
                    nr < 0 or nr >= rowend or nc < 0 or nc >= colend
                ):
                    continue

                collision = False
                if (nr, nc) != start:
                    # check for collision with any of the billiards
                    for char, (br, bc) in self.billiard_moves.items():
                        # instead of predicting position of each billiard
                        # and comparing it with curr position,
                        # apply reverse movement on curr position and
                        # check if there is any billiard at that location
                        mr, mc = (nr - br * time) % rowend, (nc - bc * time) % colend
                        if (mr, mc) in self.billiards[char]:
                            collision = True
                            break

                if collision:
                    continue

                key = (nr, nc, time % lcm)
                if key in visited:
                    continue
                visited.add(key)
                que.append((nr, nc, time))

        return min_time

    def part1(self) -> None:
        min_time = self.get_min_time(self.start, self.end, 0)
        print(min_time)

    def part2(self) -> None:
        first_trip = self.get_min_time(self.start, self.end, 0)
        second_trip = self.get_min_time(self.end, self.start, first_trip)
        final_trip = self.get_min_time(self.start, self.end, second_trip)
        print(final_trip)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
