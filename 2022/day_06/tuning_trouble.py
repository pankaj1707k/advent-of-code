""" https://adventofcode.com/2022/day/6 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input() -> str:
    with open(get_file_path("input.txt")) as infile:
        stream = infile.readline()
    return stream.strip()


def _get_start_point(stream: str, winsize: int) -> int:
    window = dict()

    for k in range(winsize):
        window[stream[k]] = window.get(stream[k], 0) + 1

    index = winsize
    while len(window) != winsize:
        window[stream[index - winsize]] -= 1
        if window[stream[index - winsize]] == 0:
            window.pop(stream[index - winsize])
        window[stream[index]] = window.get(stream[index], 0) + 1
        index += 1

    return index


def part_1(stream: str) -> int:
    return _get_start_point(stream, 4)


def part_2(stream: str) -> int:
    return _get_start_point(stream, 14)


if __name__ == "__main__":
    stream = parse_input()
    print("Part 1:", part_1(stream))  # output: 1544
    print("Part 2:", part_2(stream))  # output: 2145
