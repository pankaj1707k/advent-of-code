""" https://adventofcode.com/2023/day/17 """

import heapq
import os
from collections import defaultdict


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def min_heat_loss(min_blocks: int, max_blocks: int) -> int:
    heats = defaultdict(lambda: 1 << 31)
    que = list()
    que.append((0, 0, 0, 0, 0))
    heats[(0, 0, 0, 1)] = 0
    heats[(0, 0, 1, 0)] = 0

    while que:
        heat, row, col, pdr, pdc = heapq.heappop(que)
        if (row, col) == (N - 1, N - 1):
            return heat
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if (dr, dc) == (-pdr, -pdc) or (dr, dc) == (pdr, pdc):
                continue
            nh = heat
            for d in range(1, max_blocks + 1):
                nr, nc = row + d * dr, col + d * dc
                if nr < 0 or nc < 0 or nr >= N or nc >= N:
                    continue
                nh += grid[nr][nc]
                key = (nr, nc, dr, dc)
                if d >= min_blocks and nh < heats[key]:
                    heats[key] = nh
                    heapq.heappush(
                        que,
                        (nh, nr, nc, dr, dc),
                    )


def part1() -> None:
    result = min_heat_loss(1, 3)
    print(result)


def part2() -> None:
    result = min_heat_loss(4, 10)
    print(result)


if __name__ == "__main__":
    grid: list[list[int]] = list()

    with open(get_file_path("input.txt")) as infile:
        for line in infile.read().splitlines():
            grid.append(list(map(int, list(line))))

    N = len(grid)

    part1()
    part2()
