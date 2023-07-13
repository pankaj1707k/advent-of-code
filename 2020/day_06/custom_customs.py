""" https://adventofcode.com/2020/day/6 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1(answers: list[str]) -> None:
    index = total = 0
    while index < len(answers):
        union = 0
        while index < len(answers) and answers[index] != "":
            # bit mask the characters
            mask = 0
            for char in answers[index]:
                mask |= 1 << (ord(char) - ord("a"))
            # for "anyone", compute OR
            union |= mask
            index += 1
        total += union.bit_count()
        index += 1
    print(total)


def part2(answers: list[str]) -> None:
    index = total = 0
    while index < len(answers):
        common = (1 << 26) - 1
        while index < len(answers) and answers[index] != "":
            # bit mask the characters
            mask = 0
            for char in answers[index]:
                mask |= 1 << (ord(char) - ord("a"))
            # for "everyone", compute AND
            common &= mask
            index += 1
        total += common.bit_count()
        index += 1
    print(total)


def main() -> None:
    with open(get_file_path("input.txt")) as fd:
        lines = [line.strip() for line in fd.readlines()]

    part1(lines)
    part2(lines)


if __name__ == "__main__":
    main()
