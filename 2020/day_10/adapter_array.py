""" https://adventofcode.com/2020/day/10 """

import os
from functools import cache


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    diff_counts = {1: 0, 2: 0, 3: 1}
    curr = 0
    maxval = max(ratings)
    while curr != maxval:
        if curr + 1 in ratings:
            diff_counts[1] += 1
            curr += 1
        elif curr + 2 in ratings:
            diff_counts[2] += 1
            curr += 2
        elif curr + 3 in ratings:
            diff_counts[3] += 1
            curr += 3
    print(diff_counts[1] * diff_counts[3])


@cache
def count_arrangements(rating: int) -> int:
    """Return the number of arrangements ending with `rating`"""
    if rating == 0:
        return 1
    if rating < 0 or rating not in ratings:
        return 0
    return (
        count_arrangements(rating - 1)
        + count_arrangements(rating - 2)
        + count_arrangements(rating - 3)
    )


def part2() -> None:
    max_rating = max(ratings)
    arrangements = count_arrangements(max_rating)
    print(arrangements)


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as fd:
        ratings = set(int(n.strip()) for n in fd.readlines())

    part1()
    part2()
