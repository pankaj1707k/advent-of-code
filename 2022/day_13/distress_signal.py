""" https://adventofcode.com/2022/day/13 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input():
    packets = []
    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            if line != "\n":
                packets.append(eval(line.rstrip()))
    return packets


def compare(first, second) -> int:
    if isinstance(first, int) and isinstance(second, int):
        return first - second
    elif isinstance(first, list) and isinstance(second, list):
        for index in range(min(len(first), len(second))):
            val = compare(first[index], second[index])
            if val != 0:
                return val
        return len(first) - len(second)
    elif isinstance(first, int):
        for index in range(min(1, len(second))):
            val = compare([first][index], second[index])
            if val != 0:
                return val
        return len([first]) - len(second)
    elif isinstance(second, int):
        for index in range(min(len(first), 1)):
            val = compare(first[index], [second][index])
            if val != 0:
                return val
        return len(first) - len([second])


def part_1():
    index_sum = 0
    for index in range(0, len(packets), 2):
        first = packets[index]
        second = packets[index + 1]
        val = compare(first, second)
        if val <= 0:
            index_sum += (index // 2) + 1
    print(index_sum)


class Comparator(list):
    def __lt__(self, __x: list) -> bool:
        return compare(self, __x) <= 0


def part_2():
    packets.extend([[[2]], [[6]]])
    packets.sort(key=Comparator)
    decoder_key = (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
    print(decoder_key)


if __name__ == "__main__":
    packets = parse_input()
    part_1()  # 5503
    part_2()  # 20952
