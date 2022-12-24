""" https://adventofcode.com/2022/day/14 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input():
    lines = list()
    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            line = list(map(list, map(eval, line.strip().split(" -> "))))
            lines.append(line)
    return lines


def find_min_xy() -> tuple[int, int]:
    min_x = min_y = 1000
    for scan in scans:
        for x, y in scan:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
    return min_x - 1, min_y - 1


def find_max_xy() -> tuple[int, int]:
    max_x = max_y = 0
    for scan in scans:
        for x, y in scan:
            max_x = max(max_x, x)
            max_y = max(max_y, y)
    return max_x, max_y


def reduce_coordinates(min_x: int):
    for scan in scans:
        for point in scan:
            point[0] -= min_x


def mark_paths(grid: list[list[str]]):
    for scan in scans:
        for i in range(len(scan) - 1):
            if scan[i][0] == scan[i + 1][0]:
                diff = -1 if scan[i + 1][1] < scan[i][1] else 1
                for y in range(scan[i][1], scan[i + 1][1] + diff, diff):
                    grid[y][scan[i][0]] = "#"
            if scan[i][1] == scan[i + 1][1]:
                diff = -1 if scan[i + 1][0] < scan[i][0] else 1
                for x in range(scan[i][0], scan[i + 1][0] + diff, diff):
                    grid[scan[i][1]][x] = "#"


def print_grid(grid: list[list[str]]):
    for row in grid:
        print("".join(row))
    print()


def part_1():
    min_x, _ = find_min_xy()
    reduce_coordinates(min_x)
    max_x, max_y = find_max_xy()
    grid = [["." for __ in range(max_x + 2)] for _ in range(max_y + 1)]
    grid[0][500 - min_x] = "+"  # mark sand source
    mark_paths(grid)
    print_grid(grid)

    while True:
        grain = [0, 500 - min_x]
        while grain[0] < len(grid) - 1 and grain[1] < len(grid[0]) - 1:
            if grid[grain[0] + 1][grain[1]] == ".":
                grain[0] += 1
            elif grid[grain[0] + 1][grain[1] - 1] == ".":
                grain[0] += 1
                grain[1] -= 1
            elif grid[grain[0] + 1][grain[1] + 1] == ".":
                grain[0] += 1
                grain[1] += 1
            else:
                break
        if grain[0] >= len(grid) - 1 or grain[1] >= len(grid[0]) - 1:
            break
        grid[grain[0]][grain[1]] = "o"

    rest_units = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            rest_units += int(grid[i][j] == "o")

    print(rest_units)


def part_2():
    min_x, _ = find_min_xy()
    reduce_coordinates(min_x)
    _, max_y = find_max_xy()
    grid = [["." for __ in range(2 * max_y + 7)] for _ in range(max_y + 3)]
    right_shift = min_x + max_y - 497
    reduce_coordinates(-right_shift)
    grid[0][500 - min_x + right_shift] = "+"  # mark sand source
    mark_paths(grid)
    # mark floor
    for j in range(len(grid[0])):
        grid[-1][j] = "#"
    print_grid(grid)

    while True:
        grain = [0, 500 - min_x + right_shift]
        while grain[0] < len(grid) - 1:
            if grid[grain[0] + 1][grain[1]] == ".":
                grain[0] += 1
            elif grid[grain[0] + 1][grain[1] - 1] == ".":
                grain[0] += 1
                grain[1] -= 1
            elif grid[grain[0] + 1][grain[1] + 1] == ".":
                grain[0] += 1
                grain[1] += 1
            else:
                break
        grid[grain[0]][grain[1]] = "o"
        if grain == [0, 500 - min_x + right_shift]:
            break

    print_grid(grid)

    rest_units = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            rest_units += int(grid[i][j] == "o")

    print(rest_units)


if __name__ == "__main__":
    scans = parse_input()
    part_1()
    part_2()
