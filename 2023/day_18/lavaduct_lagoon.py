""" https://adventofcode.com/2023/day/18 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def find_area(vertices: list[tuple[int, int]], border_length: int) -> int:
    n = len(vertices)
    area = abs(
        sum(
            (vertices[(i + 1) % n][1] + vertices[i][1])
            * (vertices[(i + 1) % n][0] - vertices[i][0])
            for i in range(n)
        )
    )
    area //= 2
    area += border_length // 2 + 1
    return area


def part1() -> None:
    pos = (0, 0)
    boundary = 0
    vertices = []
    dirs = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}

    for dir, steps, _ in plan:
        dr, dc = dirs[dir]
        vertices.append(pos)
        for _ in range(steps):
            pos = (pos[0] + dr, pos[1] + dc)
            boundary += 1

    result = find_area(vertices, boundary)
    print(result)


def part2() -> None:
    pos = (0, 0)
    boundary = 0
    vertices = []

    dirs = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}

    for _, _, hexcode in plan:
        steps, dir = int(hexcode[1:-1], 16), int(hexcode[-1])
        dr, dc = dirs[dir]
        vertices.append(pos)
        pos = (pos[0] + steps * dr, pos[1] + steps * dc)
        boundary += steps * abs(dr + dc)

    result = find_area(vertices, boundary)
    print(result)


if __name__ == "__main__":
    plan: list[tuple[str, int, str]] = list()

    with open(get_file_path("input.txt")) as infile:
        for line in infile.read().strip().splitlines():
            _dir, _steps, _color = line.split()
            plan.append((_dir, int(_steps), _color[1:-1]))

    part1()
    part2()
