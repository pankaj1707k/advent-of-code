""" https://adventofcode.com/2023/day/1 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    total = 0

    for line in content:
        first = last = -1
        for char in line:
            if char.isdigit():
                last = int(char)
                if first == -1:
                    first = int(char)
        total += first * 10 + last

    print(total)


def part2() -> None:
    digits = tuple("123456789")
    dwords = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    search_content = digits + dwords
    total = 0

    for line in content:
        first = last = -1
        first_pos, last_pos = len(line), -1
        for digit in search_content:
            pos = line.find(digit)
            if pos != -1 and pos < first_pos:
                first_pos = pos
                first = int(digit) if digit.isdigit() else (dwords.index(digit) + 1)
            pos = line.rfind(digit)
            if pos != -1 and pos > last_pos:
                last_pos = pos
                last = int(digit) if digit.isdigit() else (dwords.index(digit) + 1)
        total += first * 10 + last

    print(total)


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as infile:
        content = [line.strip() for line in infile.readlines()]

    part1()
    part2()
