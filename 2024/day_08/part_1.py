""" https://adventofcode.com/2024/day/8 """

from collections import defaultdict
import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def main():
    grid: list[str] = []

    with open(get_file_path("input.txt")) as fd:
        grid = list(map(lambda l: l.strip(), fd.readlines()))

    antennas: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != ".":
                antennas[grid[i][j]].append((i, j))

    antinodes: set[tuple[int, int]] = set()
    for same_freq in antennas.values():
        for i in range(len(same_freq) - 1):
            for j in range(i + 1, len(same_freq)):
                x0, y0 = same_freq[i]
                x1, y1 = same_freq[j]
                for x in range(len(grid)):
                    for y in range(len(grid[x])):
                        if (x == x0 and y == y0) or (x == x1 and y == y1):
                            continue
                        if (y - y0) * (x - x1) != (y - y1) * (x - x0):
                            continue
                        if abs(x - x0) + abs(y - y0) == 2 * (
                            abs(x - x1) + abs(y - y1)
                        ) or abs(x - x1) + abs(y - y1) == 2 * (
                            abs(x - x0) + abs(y - y0)
                        ):
                            antinodes.add((x, y))

    print(len(antinodes))


main()
