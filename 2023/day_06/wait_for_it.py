""" https://adventofcode.com/2023/day/6 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    result = 1
    races = len(race_time)

    for r in range(races):
        ways = 0
        for hold_time in range(1, race_time[r]):
            move_time = race_time[r] - hold_time
            distance = move_time * hold_time
            ways += int(distance > max_distance[r])
        result *= ways

    print(result)


def part2() -> None:
    total_time = int("".join(map(str, race_time)))
    record_distance = int("".join(map(str, max_distance)))
    ways = 0
    for hold_time in range(1, total_time):
        distance = (total_time - hold_time) * hold_time
        ways += int(distance > record_distance)
    print(ways)


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as infile:
        time_line, distance_line = infile.read().splitlines()
        race_time = list(map(int, time_line.split()[1:]))
        max_distance = list(map(int, distance_line.split()[1:]))

    part1()
    part2()
