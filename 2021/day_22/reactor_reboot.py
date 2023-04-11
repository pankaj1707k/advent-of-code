""" https://adventofcode.com/2021/day/22 """

import os
from collections import Counter, defaultdict


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Step:
    def __init__(
        self,
        toggle: bool = False,
        x_range: tuple[int, int] = None,
        y_range: tuple[int, int] = None,
        z_range: tuple[int, int] = None,
    ) -> None:
        self.toggle: bool = toggle
        self.x_range: tuple[int, int] = x_range
        self.y_range: tuple[int, int] = y_range
        self.z_range: tuple[int, int] = z_range

    def __repr__(self) -> str:
        return f"Step(toggle={self.toggle}, x_range={self.x_range}, y_range={self.y_range}, z_range={self.z_range})"


def part1(steps: list[Step]) -> None:
    cubes = defaultdict(lambda: False)
    for step in steps:
        for x in range(max(step.x_range[0], -50), min(step.x_range[1], 50) + 1):
            for y in range(max(step.y_range[0], -50), min(step.y_range[1], 50) + 1):
                for z in range(max(step.z_range[0], -50), min(step.z_range[1], 50) + 1):
                    cubes[(x, y, z)] = step.toggle

    cubes_on = 0
    for x in range(-50, 51):
        for y in range(-50, 51):
            for z in range(-50, 51):
                cubes_on += int(cubes[(x, y, z)])

    print(cubes_on)


def part2(steps: list[Step]) -> None:
    cubes = Counter()
    for step in steps:
        curr_sign = 1 if step.toggle else -1
        cxs, cxe, cys, cye, czs, cze = *step.x_range, *step.y_range, *step.z_range
        update = Counter()
        for (xs, xe, ys, ye, zs, ze), sign in cubes.items():
            # find intersection of current cuboid and existing cuboid
            # this is also a cuboid!
            ixs, ixe = max(cxs, xs), min(cxe, xe)
            iys, iye = max(cys, ys), min(cye, ye)
            izs, ize = max(czs, zs), min(cze, ze)
            # if intersection exists, zero out its contribution from the set
            if ixs <= ixe and iys <= iye and izs <= ize:
                update[(ixs, ixe, iys, iye, izs, ize)] -= sign

        # add the current cuboid to the set only if it needs to be turned on
        if curr_sign == 1:
            update[(cxs, cxe, cys, cye, czs, cze)] += curr_sign
        cubes.update(update)

    cubes_on = 0
    # since all cubes correspond to values +1 for ON
    # volume of the cuboid gives the number of cubes in the ON state
    for (xs, xe, ys, ye, zs, ze), sign in cubes.items():
        cubes_on += (xe - xs + 1) * (ye - ys + 1) * (ze - zs + 1) * sign

    print(cubes_on)


def main() -> None:
    with open(get_file_path("input.txt")) as infile:
        lines = list(map(lambda l: l.strip(), infile.readlines()))

    steps = []

    for line in lines:
        line = line.split()
        toggle = True if line[0] == "on" else False
        ranges = line[1].split(",")
        for i in range(3):
            r = ranges[i][2:].split("..")
            ranges[i] = tuple(map(int, r))
        steps.append(Step(toggle, *ranges))

    part1(steps)
    part2(steps)


if __name__ == "__main__":
    main()
