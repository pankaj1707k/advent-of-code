""" https://adventofcode.com/2021/day/24 """

import os
from functools import cache


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


@cache
def search(index: int, wval: int, xval: int, yval: int, zval: int) -> tuple[bool, str]:
    """
    Try all possible values. Cache results for each combination of index
    and variable values.
    """
    # if zval exceeds 10**7 then it cannot be reduced to 0
    # This is because the ALU multiplies by 26 atmost 4 times
    # without reducing the value. 26**4 is of the order 10**6
    # so 10**7 as a cap is a valid rough estimate
    if zval > 10**7:
        return False, ""

    if index == len(alu):
        return (zval == 0, "")

    values = {"w": wval, "x": xval, "y": yval, "z": zval}

    if alu[index][0] == "inp":
        # start trying digits from maximum to minimum if we need to find
        # the largest number accepted by the monad
        seq = range(9, 0, -1) if maxnum else range(1, 10)
        for d in seq:
            # try `d` as input for `w`, reset x, y and pass z unchanged
            result = search(index + 1, d, 0, 0, zval)
            if result[0]:
                return True, str(d) + result[1]
        return False, ""

    op, first, second = alu[index]
    second = values[second] if second in values else int(second)

    if op == "add":
        values[first] += second
    elif op == "mul":
        values[first] *= second
    elif op == "div":
        if second == 0:
            return False, ""
        values[first] //= second
    elif op == "mod":
        if second == 0:
            return False, ""
        values[first] %= second
    else:
        values[first] = int(values[first] == second)

    return search(index + 1, values["w"], values["x"], values["y"], values["z"])


def part1() -> None:
    global maxnum
    maxnum = True
    result = search(0, 0, 0, 0, 0)
    print(*result)


def part2() -> None:
    global maxnum
    maxnum = False
    result = search(0, 0, 0, 0, 0)
    print(*result)


def main() -> None:
    with open(get_file_path("input.txt")) as infile:
        lines = list(map(lambda l: l.strip(), infile.readlines()))

    global alu
    alu = [line.split() for line in lines]

    global maxnum  # bool to identify if we need to find max number

    # do not run both in a single instance
    part1()
    # part2()


if __name__ == "__main__":
    main()

# Inspired from `https://www.youtube.com/watch?v=uNSO3y4WdVQ`
