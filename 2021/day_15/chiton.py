""" https://adventofcode.com/2021/day/15 """

import os
from heapq import heappop, heappush


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.grid: list[list[int]] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                self.grid.append(list(map(int, list(line.strip()))))

    def get_min_risk(self, tile_count: int) -> int:
        # Using dijkstra's algorithm
        # risk === distance
        que = [(0, 0, 0)]  # (cost, row, col)
        N = len(self.grid)  # reference grid dimension
        M = tile_count * N  # extended grid dimension
        cost = [[None] * M for _ in range(M)]

        while que:
            curr_cost, row, col = heappop(que)
            # check if out of bounds
            if row < 0 or col < 0 or row >= M or col >= M:
                continue
            risk = self.grid[row % N][col % N] + row // N + col // N
            # perform wrap around for values greater than 9
            while risk > 9:
                risk -= 9
            if cost[row][col] != None and cost[row][col] <= curr_cost + risk:
                continue
            cost[row][col] = curr_cost + risk
            # exit if we have reached the end
            if row == M - 1 and col == M - 1:
                break
            # add neighbors to queue
            for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nr, nc = row + dr, col + dc
                heappush(que, (cost[row][col], nr, nc))

        return cost[M - 1][M - 1] - self.grid[0][0]

    def part1(self) -> None:
        print(self.get_min_risk(1))

    def part2(self) -> None:
        print(self.get_min_risk(5))


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
