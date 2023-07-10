""" https://adventofcode.com/2020/day/2 """

import os
import re


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1(passdb: list[tuple[int, int, str, str]]) -> None:
    valid = 0
    for min_freq, max_freq, char, passwd in passdb:
        valid += int(min_freq <= passwd.count(char) <= max_freq)
    print(valid)


def part2(passdb: list[tuple[int, int, str, str]]) -> None:
    valid = 0
    for first, second, char, passwd in passdb:
        valid += int((passwd[first - 1] == char) ^ (passwd[second - 1] == char))
    print(valid)


def main() -> None:
    with open(get_file_path("input.txt")) as fd:
        lines = fd.readlines()

    passdb = []
    pattern = re.compile(
        r"(?P<min>[0-9]+)\-(?P<max>[0-9]+)\s(?P<char>[a-z]):\s(?P<passwd>[a-z]+)"
    )
    for line in lines:
        _match = pattern.search(line)
        record = (
            int(_match.group("min")),
            int(_match.group("max")),
            _match.group("char"),
            _match.group("passwd"),
        )
        passdb.append(record)

    part1(passdb)
    part2(passdb)


if __name__ == "__main__":
    main()
