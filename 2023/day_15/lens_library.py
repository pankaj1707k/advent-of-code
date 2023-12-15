""" https://adventofcode.com/2023/day/15 """

import os
from collections import defaultdict


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def hash_value(string: str) -> int:
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def get_lens_pos(box: list[tuple[str, int]], label: str) -> int:
    for pos, lens in enumerate(box):
        if lens[0] == label:
            return pos
    return -1


def part1() -> None:
    result = 0

    for string in seq:
        result += hash_value(string)

    print(result)


def part2() -> None:
    boxes = defaultdict(list)

    for instr in seq:
        if "-" in instr:
            label = instr[:-1]
            hval = hash_value(label)
            pos = get_lens_pos(boxes[hval], label)
            if pos != -1:
                boxes[hval].pop(pos)
        else:
            label = instr[:-2]
            focal_length = int(instr[-1])
            hval = hash_value(label)
            pos = get_lens_pos(boxes[hval], label)
            if pos == -1:
                boxes[hval].append((label, focal_length))
            else:
                boxes[hval][pos] = (label, focal_length)

    total_focus_power = 0
    for boxnum in boxes:
        for slot, (_, focal_length) in enumerate(boxes[boxnum], 1):
            total_focus_power += (boxnum + 1) * slot * focal_length

    print(total_focus_power)


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as infile:
        seq = infile.read().strip().split(",")

    part1()
    part2()
