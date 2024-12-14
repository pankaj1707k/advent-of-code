""" https://adventofcode.com/2024/day/12 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def floodfill(
    row: int, col: int, farm: list[str], visited: set[tuple[int, int]]
) -> int:
    if (row, col) in visited:
        return 0
    visited.add((row, col))
    peri = 0
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if (
            nr < 0
            or nr == len(farm)
            or nc < 0
            or nc == len(farm[0])
            or farm[nr][nc] != farm[row][col]
        ):
            peri += 1
            continue
        peri += floodfill(nr, nc, farm, visited)
    return peri


def main():
    farm: list[str] = []

    with open(get_file_path("input.txt")) as fd:
        farm = fd.read().splitlines()

    price = 0
    visited: set[tuple[int, int]] = set()
    for i in range(len(farm)):
        for j in range(len(farm[i])):
            if (i, j) in visited:
                continue
            before = len(visited)
            perimeter = floodfill(i, j, farm, visited)
            area = len(visited) - before
            price += perimeter * area

    print(price)


main()
