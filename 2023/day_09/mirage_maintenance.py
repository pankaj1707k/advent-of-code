""" https://adventofcode.com/2023/day/9 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def get_diffs(seq: list[int]) -> list[list[int]]:
    subseqs = [seq.copy()]

    while not all(num == seq[0] for num in seq):
        diff = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
        subseqs.append(diff)
        seq = diff

    return subseqs


def generate_next_value(seq: list[int]) -> int:
    subseqs = get_diffs(seq)
    subseqs[-1].append(subseqs[-1][-1])

    for sidx in range(len(subseqs) - 2, -1, -1):
        subseqs[sidx].append(subseqs[sidx + 1][-1] + subseqs[sidx][-1])

    return subseqs[0][-1]


def generate_prev_value(seq: list[int]) -> int:
    subseqs = get_diffs(seq)
    subseqs[-1] = [subseqs[-1][0]] + subseqs[-1]

    for sidx in range(len(subseqs) - 2, -1, -1):
        subseqs[sidx] = [subseqs[sidx][0] - subseqs[sidx + 1][0]] + subseqs[sidx]

    return subseqs[0][0]


def part1() -> None:
    result = 0
    for seq in seqs:
        result += generate_next_value(seq)
    print(result)


def part2() -> None:
    result = 0
    for seq in seqs:
        result += generate_prev_value(seq)
    print(result)


if __name__ == "__main__":
    seqs = list()

    with open(get_file_path("input.txt")) as infile:
        for line in infile.read().splitlines():
            seqs.append(list(map(int, line.split())))

    part1()
    part2()
