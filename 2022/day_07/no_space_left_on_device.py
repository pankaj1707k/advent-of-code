""" https://adventofcode.com/2022/day/7 """

import os
from functools import cache


class Node:
    def __init__(self) -> None:
        self.files = dict()
        self.dirs = dict()
        self.parent = None
        self.size = 0


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input():
    cwd = system = Node()
    system.dirs["/"] = Node()
    system.dirs["/"].parent = None

    with open(get_file_path("input.txt")) as infile:
        lines = [line.strip().split() for line in infile.readlines()]

    for line in lines:
        if line[0] == "$" and line[1] == "cd":
            if line[2] == "..":
                cwd = cwd.parent
            else:
                cwd = cwd.dirs[line[2]]
        elif line[0] == "dir":
            if line[1] not in cwd.dirs:
                cwd.dirs[line[1]] = Node()
                cwd.dirs[line[1]].parent = cwd
        elif line[0].isdigit():
            cwd.files[line[1]] = int(line[0])

    return system


@cache
def _dir_sizes(dir: Node) -> int:
    size = sum(s for _, s in dir.files.items())
    for subdir in dir.dirs.values():
        size += _dir_sizes(subdir)
    dir.size = size
    return size


def _get_sizesum(cwd: Node) -> int:
    sizesum = 0
    if cwd.size <= 100000:
        sizesum += cwd.size
    for subdir in cwd.dirs:
        sizesum += _get_sizesum(cwd.dirs[subdir])
    return sizesum


def part_1() -> int:
    _dir_sizes(system)
    return _get_sizesum(system)


def _removable_dirs(cwd: Node) -> list[int]:
    sizes = list()
    for subdir in cwd.dirs.values():
        sizes += _removable_dirs(subdir)
    if cwd.size + UNUSED >= REQ_SIZE:
        sizes.append(cwd.size)
    return sizes


def part_2():
    sizes = _removable_dirs(system)
    return min(sizes)


if __name__ == "__main__":
    system = parse_input()
    print(part_1())  # output: 1306611

    MAX_SIZE = 70_000_000
    UNUSED = MAX_SIZE - system.size
    REQ_SIZE = 30_000_000
    print(part_2())  # output: 13210366
