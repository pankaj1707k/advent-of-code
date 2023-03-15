""" https://adventofcode.com/2021/day/17 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1(ty_min: int) -> None:
    vy = abs(ty_min) - 1
    hmax = (vy * (vy + 1)) >> 1
    print(hmax)


def part2(tx_min: int, tx_max: int, ty_min: int, ty_max: int) -> None:
    def on_target(vx: int, vy: int) -> bool:
        xpos = ypos = 0
        while True:
            if tx_min <= xpos <= tx_max and ty_min <= ypos <= ty_max:
                return True
            if vx == 0 and not (tx_min <= xpos <= tx_max):
                return False
            if ypos < ty_min or xpos > tx_max:
                return False
            xpos += vx
            ypos += vy
            if vx > 0:
                vx -= 1
            elif vx < 0:
                vx += 1
            vy -= 1

    ymax = max(abs(ty_min), abs(ty_max))
    velocity_count = 0

    for ux in range(tx_max + 1):
        for uy in range(-ymax, ymax + 1):
            velocity_count += int(on_target(ux, uy))

    print(velocity_count)


def main() -> None:
    with open(get_file_path("input.txt")) as infile:
        _, _, xrange, yrange = infile.readline().strip().split()

    tx_min, tx_max = map(int, xrange.rstrip(",")[2:].split(".."))
    ty_min, ty_max = map(int, yrange[2:].split(".."))

    part1(ty_min)
    part2(tx_min, tx_max, ty_min, ty_max)


if __name__ == "__main__":
    main()
