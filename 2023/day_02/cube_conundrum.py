""" https://adventofcode.com/2023/day/2 """

import os
from collections import defaultdict


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    max_cubes = {"red": 12, "green": 13, "blue": 14}
    id_sum = 0

    for game_id, desc in games.items():
        valid = True
        for sub_game in desc:
            for color, max_count in max_cubes.items():
                if sub_game[color] > max_count:
                    valid = False
                    break
        id_sum += game_id if valid else 0

    print(id_sum)


def part2() -> None:
    total_power = 0

    for desc in games.values():
        min_cubes = {}
        for sub_game in desc:
            for color in sub_game:
                min_cubes[color] = max(min_cubes.get(color, 0), sub_game[color])
        power = 1
        for count in min_cubes.values():
            power *= count
        total_power += power

    print(total_power)


if __name__ == "__main__":
    games = defaultdict(list)

    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            header, desc = line.strip().split(": ")
            game_id = int(header.split()[1])
            parts = desc.split("; ")
            for part in parts:
                counts = defaultdict(int)
                for color_desc in part.split(", "):
                    count, color = color_desc.split()
                    counts[color] = int(count)
                games[game_id].append(counts)

    part1()
    part2()
