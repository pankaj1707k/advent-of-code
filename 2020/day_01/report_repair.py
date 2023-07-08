""" https://adventofcode.com/2020/day/1 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1(report: list[int]) -> None:
    length = len(report)
    result = None
    for i in range(length - 1):
        for j in range(i + 1, length):
            if report[i] + report[j] == 2020:
                result = report[i] * report[j]
                break
        if result:
            break

    print(result)


def part2(report: list[int]) -> None:
    length = len(report)
    result = None

    for i in range(length - 2):
        for j in range(i + 1, length - 1):
            for k in range(j + 1, length):
                if report[i] + report[j] + report[k] == 2020:
                    result = report[i] * report[j] * report[k]
                    break
            if result:
                break
        if result:
            break

    print(result)


def main() -> None:
    with open(get_file_path("input.txt")) as fd:
        report = [int(line.rstrip()) for line in fd.readlines()]

    part1(report)
    part2(report)


if __name__ == "__main__":
    main()
