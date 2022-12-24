""" https://adventofcode.com/2022/day/15 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input() -> tuple[list, list]:
    sensors = list()
    beacons = list()
    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            line = line.strip().split()
            sensor = (int(line[2][2:].rstrip(",")), int(line[3][2:].rstrip(":")))
            sensors.append(sensor)
            beacon = (int(line[8][2:].rstrip(",")), int(line[9][2:].rstrip(":")))
            beacons.append(beacon)
    return sensors, beacons


def manhattan_distance(p: tuple[int, int], q: tuple[int, int]) -> int:
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def get_exclusion_zones(target_row: int) -> list[list[int]]:
    excluded_zones = list()

    for i in range(len(sensors)):
        k = manhattan_distance(sensors[i], beacons[i]) - abs(target_row - sensors[i][1])
        if k < 0:
            continue
        excluded_zones.append([sensors[i][0] - k, sensors[i][0] + k])

    # merge overlapping intervals
    excluded_zones.sort()
    disjoint_zones = list()
    start, end = excluded_zones[0]
    for zone in excluded_zones:
        if max(start, zone[0]) > min(end, zone[1]):
            disjoint_zones.append([start, end])
            start, end = zone
        else:
            start = min(start, zone[0])
            end = max(end, zone[1])
    disjoint_zones.append([start, end])

    return disjoint_zones


def part_1():
    exclusion_zones = get_exclusion_zones(target_row=2000000)

    # count number of positions
    excluded_positions = 0
    for zone in exclusion_zones:
        excluded_positions += zone[1] - zone[0]

    print(excluded_positions)


def get_distress_beacon_x(zones: list[list[int]], maxpos: int) -> int:
    if len(zones) == 2 and zones[1][0] - zones[0][1] == 2:
        return zones[0][1] + 1
    if len(zones) == 1 and zones[0] == [0, maxpos - 1]:
        return maxpos
    if len(zones) == 1 and zones[0] == [1, maxpos]:
        return 0
    return -1  # either no location or multiple locations


def part_2():
    MAX_POS = 4000000
    distress_beacon_pos = None
    for ypos in range(MAX_POS):
        zones = get_exclusion_zones(ypos)
        xpos = get_distress_beacon_x(zones, MAX_POS)
        if xpos > 0:
            distress_beacon_pos = [xpos, ypos]
            break
    xpos, ypos = distress_beacon_pos
    tuning_freq = xpos * MAX_POS + ypos
    print(tuning_freq)


if __name__ == "__main__":
    sensors, beacons = parse_input()
    part_1()
    part_2()
