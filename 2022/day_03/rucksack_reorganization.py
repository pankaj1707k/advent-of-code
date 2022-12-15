""" https://adventofcode.com/2022/day/3 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input() -> list[str]:
    rucksacks = []

    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            rucksacks.append(line.strip())

    return rucksacks


def part_1(data: list[str]) -> int:
    total_priority = 0

    for rucksack in data:
        first_comp_set = set(rucksack[: len(rucksack) // 2])
        for item in rucksack[len(rucksack) // 2 :]:
            if item in first_comp_set:
                if item.islower():
                    total_priority += ord(item) - ord("a") + 1
                else:
                    total_priority += ord(item) - ord("A") + 27
                break

    return total_priority


def part_2(data: list[str]) -> int:
    total_priority = 0

    for group_start in range(0, len(data), 3):
        badge_item = list(
            set(data[group_start])
            .intersection(data[group_start + 1])
            .intersection(data[group_start + 2])
        )[0]
        if badge_item.islower():
            total_priority += ord(badge_item) - ord("a") + 1
        else:
            total_priority += ord(badge_item) - ord("A") + 27

    return total_priority


if __name__ == "__main__":
    data = parse_input()
    print("Part 1:", part_1(data))  # output: 7785
    print("Part 2:", part_2(data))  # output: 2633
