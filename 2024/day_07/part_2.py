""" https://adventofcode.com/2024/day/7 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def is_valid(
    equation: tuple[int, ...], curr_index: int, result: int, expected: int
) -> bool:
    if curr_index == len(equation):
        return result == expected
    if result > expected:
        return False
    return (
        is_valid(equation, curr_index + 1, result + equation[curr_index], expected)
        or is_valid(equation, curr_index + 1, result * equation[curr_index], expected)
        or is_valid(
            equation, curr_index + 1, int(f"{result}{equation[curr_index]}"), expected
        )
    )


def main():
    equations: list[tuple[int, ...]] = []

    with open(get_file_path("input.txt")) as fd:
        for line in fd.readlines():
            res, exp = line.split(":")
            equations.append((int(res),) + tuple(map(int, exp.split())))

    result = 0
    for equation in equations:
        expected = equation[0]
        if is_valid(equation, 2, equation[1], expected):
            result += expected

    print(result)


main()
