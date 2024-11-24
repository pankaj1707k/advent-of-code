""" https://adventofcode.com/2023/day/24 """

import os
from itertools import combinations


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Hailstone:
    def __init__(self, pos: tuple[int, ...], vel: tuple[int, ...]) -> None:
        self.pos = pos
        self.vel = vel


def part1() -> None:
    MIN = 200000000000000
    MAX = 400000000000000

    result = 0

    for h1, h2 in combinations(hailstones, 2):
        if h1.vel[0] and h2.vel[0]:
            m1 = h1.vel[1] / h1.vel[0]
            m2 = h2.vel[1] / h2.vel[0]
            c1 = h1.pos[1] - m1 * h1.pos[0]
            c2 = h2.pos[1] - m2 * h2.pos[0]
            if abs(m1 - m2) < 1e-7:
                continue
            x = (c2 - c1) / (m1 - m2)
            y = (m1 * c2 - m2 * c1) / (m1 - m2)
        elif h1.vel[0]:
            x = h2.pos[0]
            m1 = h1.vel[1] / h1.vel[0]
            y = m1 * x + h1.pos[1] - m1 * h1.pos[0]
        elif h2.vel[0]:
            x = h1.pos[0]
            m2 = h2.vel[1] / h2.vel[0]
            y = m2 * x + h2.pos[1] - m2 * h2.pos[0]
        else:
            continue
        if (
            (x - h1.pos[0]) * h1.vel[0] >= 0
            and (y - h1.pos[1]) * h1.vel[1] >= 0
            and (x - h2.pos[0]) * h2.vel[0] >= 0
            and (y - h2.pos[1]) * h2.vel[1] >= 0
            and MIN <= x <= MAX
            and MIN <= y <= MAX
        ):
            result += 1

    print(result)


def part2() -> None:
    pass


if __name__ == "__main__":
    hailstones: list[Hailstone] = list()

    make_tuple = lambda string: tuple(map(int, string.split(", ")))

    with open(get_file_path("input.txt")) as infile:
        for line in infile.read().splitlines():
            pos, vel = line.strip().split(" @ ")
            hailstones.append(Hailstone(make_tuple(pos), make_tuple(vel)))

    part1()
    part2()
