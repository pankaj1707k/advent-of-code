""" https://adventofcode.com/2020/day/12 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    xpos = ypos = 0
    # E, S, W, N
    # fnum - 1 => turn left 90 deg, fnum + 1 => turn right 90 deg
    faces = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    fnum = 0  # initial facing direction is east

    for ins in nav:
        action, value = ins[0], int(ins[1:])
        if action == "N":
            ypos += value
        elif action == "S":
            ypos -= value
        elif action == "E":
            xpos += value
        elif action == "W":
            xpos -= value
        elif action == "F":
            xpos += faces[fnum][0] * value
            ypos += faces[fnum][1] * value
        elif action == "L":
            fnum = (fnum - (value // 90) + 4) % 4
        else:
            fnum = (fnum + (value // 90)) % 4

    distance = abs(xpos) + abs(ypos)
    print(distance)


def part2() -> None:
    shx = shy = 0  # ship pos
    wpx, wpy = 10, 1  # waypoint pos relative to ship

    for ins in nav:
        action, value = ins[0], int(ins[1:])
        if action == "N":
            wpy += value
        elif action == "S":
            wpy -= value
        elif action == "E":
            wpx += value
        elif action == "W":
            wpx -= value
        elif action == "F":
            dx, dy = wpx * value, wpy * value
            shx += dx
            shy += dy
        elif action == "L":
            if value == 90:
                wpx, wpy = -wpy, wpx
            elif value == 180:
                wpx, wpy = -wpx, -wpy
            elif value == 270:
                wpx, wpy = wpy, -wpx
        elif action == "R":
            if value == 90:
                wpx, wpy = wpy, -wpx
            elif value == 180:
                wpx, wpy = -wpx, -wpy
            elif value == 270:
                wpx, wpy = -wpy, wpx

    distance = abs(shx) + abs(shy)
    print(distance)


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as fd:
        nav = [line.strip() for line in fd.readlines()]

    part1()
    part2()
