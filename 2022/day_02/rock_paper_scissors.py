""" https://adventofcode.com/2022/day/2 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input() -> list[list[int]]:
    data = []
    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            data.append(line.strip().split())
    return data


def part_1(data: list[list[int]]) -> int:
    SHAPE_SCORE = {"X": 1, "Y": 2, "Z": 3}
    OUTCOME_SCORE = {"L": 0, "D": 3, "W": 6}
    score = 0

    for opp, me in data:
        score += SHAPE_SCORE[me]
        outcome = ""
        if opp == "A":
            if me == "X":
                outcome = "D"
            elif me == "Y":
                outcome = "W"
            else:
                outcome = "L"
        elif opp == "B":
            if me == "X":
                outcome = "L"
            elif me == "Y":
                outcome = "D"
            else:
                outcome = "W"
        else:
            if me == "X":
                outcome = "W"
            elif me == "Y":
                outcome = "L"
            else:
                outcome = "D"
        score += OUTCOME_SCORE[outcome]

    return score


def part_2(data: list[list[int]]) -> int:
    SHAPE_SCORE = [1, 2, 3]
    OUTCOME_SCORE = {"X": 0, "Y": 3, "Z": 6}
    score = 0

    for opp, out in data:
        score += OUTCOME_SCORE[out]
        if out == "X":
            score += SHAPE_SCORE[ord(opp) - ord("A") - 1]
        elif out == "Y":
            score += SHAPE_SCORE[ord(opp) - ord("A")]
        else:
            score += SHAPE_SCORE[(ord(opp) - ord("A") + 1) % 3]

    return score


if __name__ == "__main__":
    data = parse_input()
    print("Part 1:", part_1(data))  # output: 8890
    print("Part 2:", part_2(data))  # output: 10238
