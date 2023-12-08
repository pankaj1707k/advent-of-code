""" https://adventofcode.com/2023/day/8 """

import os
import math


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    d_idx = steps = 0
    node = "AAA"

    while node != "ZZZ":
        node = network[node][0 if dirs[d_idx] == "L" else 1]
        steps += 1
        d_idx = (d_idx + 1) % len(dirs)

    print(steps)


def part2() -> None:
    srcs = [node for node in network.keys() if node[-1] == "A"]
    overall_steps = 1

    for src in srcs:
        node = src
        d_idx = steps = 0
        while node[-1] != "Z":
            node = network[node][0 if dirs[d_idx] == "L" else 1]
            steps += 1
            d_idx = (d_idx + 1) % len(dirs)
        overall_steps = math.lcm(overall_steps, steps)

    print(overall_steps)


if __name__ == "__main__":
    network: dict[str, tuple[str, str]] = {}

    with open(get_file_path("input.txt")) as infile:
        dirs, _network = infile.read().split("\n\n")

        for line in _network.splitlines():
            _parts = line.split(" = ")
            _left = _parts[1][1:4]
            _right = _parts[1][6:9]
            network[_parts[0]] = (_left, _right)

    part1()
    part2()
