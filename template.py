""" https://adventofcode.com/{year}/day/{daynum} """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    pass


def part2() -> None:
    pass


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as infile:
        pass

    part1()
    part2()
