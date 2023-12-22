""" https://adventofcode.com/2023/day/22 """

import os
from collections import defaultdict, deque


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def overlap(a: list[int], b: list[int]) -> bool:
    # ignore z-coordinate for both bricks (top view)
    return max(a[0], b[0]) <= min(a[3], b[3]) and max(a[1], b[1]) <= min(a[4], b[4])


def stabilize() -> None:
    # sort wrt z-coordinates of start points
    bricks.sort(key=lambda b: b[2])

    # stabilize bricks
    for i in range(len(bricks)):
        # evaluate highest z-coordinate to which the current brick can fall
        highest_z = 1
        for j in range(i):
            if overlap(bricks[i], bricks[j]):
                highest_z = max(highest_z, bricks[j][5] + 1)
        # drop the brick to the stable height
        diff = bricks[i][5] - bricks[i][2]
        bricks[i][2] = highest_z
        bricks[i][5] = bricks[i][2] + diff

    # sort again
    bricks.sort(key=lambda b: b[2])


def part1() -> None:
    result = 0
    for i in range(len(bricks)):
        if all(len(supports[j]) >= 2 for j in supported_by[i]):
            result += 1

    print(result)


def part2() -> None:
    result = 0

    for i in range(len(bricks)):
        que = deque([j for j in supported_by[i] if len(supports[j]) == 1])
        fall = set(que)
        fall.add(i)

        while que:
            j = que.popleft()
            for k in supported_by[j] - fall:
                if supports[k].issubset(fall):
                    que.append(k)
                    fall.add(k)

        result += len(fall) - 1

    print(result)


if __name__ == "__main__":
    bricks: list[list[int]] = list()

    with open(get_file_path("input.txt")) as infile:
        for line in infile.read().splitlines():
            bricks.append(list(map(int, line.replace("~", ",").split(","))))

    stabilize()

    supports = defaultdict(set)
    supported_by = defaultdict(set)

    for i in range(len(bricks)):
        for j in range(i):
            if overlap(bricks[i], bricks[j]) and bricks[i][2] - bricks[j][5] == 1:
                supports[i].add(j)
                supported_by[j].add(i)

    part1()
    part2()
