""" https://adventofcode.com/2022/day/4 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input() -> list[list[tuple[int, int]]]:
    data = []

    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            data.append([tuple(map(int, p.split("-"))) for p in line.split(",")])

    return data


def part_1(data: list[list[tuple[int, int]]]) -> int:
    overlaps = 0

    for elf_pair in data:
        start = min(elf_pair[0][0], elf_pair[1][0])
        end = max(elf_pair[0][1], elf_pair[1][1])
        if (start, end) in elf_pair:
            overlaps += 1

    return overlaps


def part_2(data: list[list[tuple[int, int]]]) -> int:
    overlaps = 0

    for elf_pair in data:
        start = max(elf_pair[0][0], elf_pair[1][0])
        end = min(elf_pair[0][1], elf_pair[1][1])
        if start <= end:
            overlaps += 1

    return overlaps


if __name__ == "__main__":
    data = parse_input()
    print("Part 1:", part_1(data))  # output: 562
    print("Part 2:", part_2(data))  # output: 924
