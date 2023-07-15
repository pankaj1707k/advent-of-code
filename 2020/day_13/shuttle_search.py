""" https://adventofcode.com/2020/day/13 """

import math
import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    min_wt = math.inf
    target_bus_id = None

    for id in bus_ids:
        if id == "x":
            continue
        _id = int(id)
        wt = _id - (time % _id)
        if wt < min_wt:
            min_wt = wt
            target_bus_id = _id

    print(target_bus_id * min_wt)


def part2() -> None:
    # solved using linear algebra

    # Equations:
    # 19 x0 - 37 x1 = -13,
    # 19 x0 - 523 x2 = -19,
    # 19 x0 - 13 x3 = -37,
    # 19 x0 - 23 x4 = -42,
    # 19 x0 - 29 x5 = -48,
    # 19 x0 - 547 x6 = -50,
    # 19 x0 - 41 x7 = -60,
    # 19 x0 - 17 x8 = -67

    # general integer solution is of the form:
    # x0 = 63972408763939 n + 17226365795791,
    # x1 = 32850696392293 n + 8845971624866,
    # x2 = 2324045442667 n + 625814436176,
    # x3 = 93498135885757 n + 25176996163082,
    # x4 = 52846772457167 n + 14230476092177,
    # x5 = 41912957466029 n + 11286239659313,
    # x6 = 2222076355603 n + 598356398757,
    # x7 = 29645750402801 n + 7982950002929,
    # x8 = 71498574500873 n + 19252997065888,
    # n is a positive integer.

    # Earliest value of x0 occurs at n = 0
    # Earliest timestamp is: 19 * (x0 at n = 0) = 19 * 17226365795791
    # = 327300950120029
    pass


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as fd:
        time = int(fd.readline().strip())
        bus_ids = fd.readline().strip().split(",")

    part1()
    part2()
