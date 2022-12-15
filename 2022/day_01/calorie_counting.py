""" https://adventofcode.com/2022/day/1 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input() -> list[list[int]]:
    data = []
    with open(get_file_path("input.txt")) as infile:
        elf_calories = []
        for line in infile.readlines():
            if line == "\n":
                data.append(elf_calories.copy())
                elf_calories.clear()
            else:
                elf_calories.append(int(line.strip()))
    return data


def part_1(data: list[list[int]]) -> int:
    max_calories = 0
    for elf_calories in data:
        max_calories = max(max_calories, sum(elf_calories))


def part_2(data: list[list[int]]) -> int:
    calorie_sums = []
    for elf_calories in data:
        calorie_sums.append(sum(elf_calories))

    calorie_sums.sort(reverse=True)
    return sum(calorie_sums[:3])


if __name__ == "__main__":
    data = parse_input()
    print("Part 1:", part_1(data))  # output: 67633
    print("Part 2:", part_2(data))  # output: 199628
