""" https://adventofcode.com/2023/day/12 """

import os
from functools import cache


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def count_ways(record: str, key: tuple[int, ...], unfold: bool) -> int:
    if unfold:
        record = "?".join([record] * 5)
        key *= 5

    @cache
    def func(ridx: int, kidx: int, count: int) -> int:
        if ridx < 0:
            if kidx < 0 and count == 0:
                return 1
            if kidx == 0 and count == key[0]:
                return 1
            return 0
        if record[ridx] == "#":
            return func(ridx - 1, kidx, count + 1)
        if record[ridx] == ".":
            if count == 0:
                return func(ridx - 1, kidx, 0)
            if count and kidx >= 0 and key[kidx] == count:
                return func(ridx - 1, kidx - 1, 0)
            return 0
        value = 0
        if count == 0:
            value += func(ridx - 1, kidx, 0)
        elif kidx >= 0 and key[kidx] == count:
            value += func(ridx - 1, kidx - 1, 0)
        value += func(ridx - 1, kidx, count + 1)
        return value

    return func(len(record) - 1, len(key) - 1, 0)


def part1() -> None:
    result = 0
    for record, key in records:
        result += count_ways(record, key, False)
    print(result)


def part2() -> None:
    result = 0
    for record, key in records:
        result += count_ways(record, key, True)
    print(result)


if __name__ == "__main__":
    records: list[tuple[str, tuple[int, ...]]] = list()

    with open(get_file_path("input.txt")) as infile:
        for line in infile.read().splitlines():
            record, key = line.split()
            key = tuple(map(int, key.split(",")))
            records.append((record, key))

    part1()
    part2()
