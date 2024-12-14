""" https://adventofcode.com/2024/day/14 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def main():
    robots = []

    with open(get_file_path("input.txt")) as fd:
        for line in fd.read().splitlines():
            pos, vel = line.split(" ")
            robots.append(eval(pos[2:]) + eval(vel[2:]))

    X = 101
    Y = 103
    time = 100
    final = []
    for x, y, vx, vy in robots:
        nx = (x + ((time % X) * (vx % X)) % X + X) % X
        ny = (y + ((time % Y) * (vy % Y)) % Y + Y) % Y
        final.append((nx, ny))

    mx = X >> 1
    my = Y >> 1
    quad = [0] * 4
    for x, y in final:
        if x >= 0 and x < mx and y >= 0 and y < my:
            quad[0] += 1
        elif x > mx and x < X and y >= 0 and y < my:
            quad[1] += 1
        elif x > mx and x < X and y > my and y < Y:
            quad[2] += 1
        elif x >= 0 and x < mx and y > my and y < Y:
            quad[3] += 1

    print(quad[0] * quad[1] * quad[2] * quad[3])


main()
