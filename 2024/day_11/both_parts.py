""" https://adventofcode.com/2024/day/11 """

from functools import cache
import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


@cache
def transform(num, count):
    if count == 0:
        return 1
    count -= 1
    if num == 0:
        return transform(1, count)
    snum = str(num)
    if len(snum) & 1 == 0:
        half = len(snum) >> 1
        return transform(int(snum[:half]), count) + transform(int(snum[half:]), count)
    return transform(num * 2024, count)


def compute(arr: list[int], count: int):
    result = 0
    for n in arr:
        result += transform(n, count)

    print(result)


def main():
    arr: list[int] = []

    with open(get_file_path("input.txt")) as fd:
        arr = list(map(int, fd.readline().rstrip().split()))

    compute(arr, 25)  # part 1
    compute(arr, 75)  # part 2


main()
