""" https://adventofcode.com/2021/day/25 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def simulate(grid: list[list[str]]) -> None:
    rows, cols = len(grid), len(grid[0])
    east, south = set(), set()

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == ">":
                east.add((row, col))
            elif grid[row][col] == "v":
                south.add((row, col))

    steps = 0
    while True:
        moved = False

        # east herd movement
        east_new = set()
        for row, col in east:
            ncol = (col + 1) % cols
            if (row, ncol) not in east and (row, ncol) not in south:
                east_new.add((row, ncol))
                moved = True
            else:
                east_new.add((row, col))
        east = east_new

        # south herd movement
        south_new = set()
        for row, col in south:
            nrow = (row + 1) % rows
            if (nrow, col) not in east and (nrow, col) not in south:
                south_new.add((nrow, col))
                moved = True
            else:
                south_new.add((row, col))
        south = south_new

        steps += 1

        if not moved:
            break

    print(steps)


def main() -> None:
    with open(get_file_path("input.txt")) as fd:
        grid = [list(line.rstrip()) for line in fd.readlines()]

    simulate(grid)


if __name__ == "__main__":
    main()
