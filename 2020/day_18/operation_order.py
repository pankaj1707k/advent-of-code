""" https://adventofcode.com/2020/day/18 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def operate(x: int, op: str, y: int) -> int:
    return (x + y) if op == "+" else (x * y)


def evaluate(expr: str, start: int) -> int | tuple[int, int]:
    index = start
    num = result = 0
    op = "+"
    while index < len(expr):
        if expr[index].isdigit():
            num = num * 10 + int(expr[index])
        elif expr[index] in "+*":
            result = operate(result, op, num)
            op = expr[index]
            num = 0
        elif expr[index] == "(":
            num, end_index = evaluate(expr, index + 1)
            index = end_index
        elif expr[index] == ")":
            return operate(result, op, num), index
        index += 1
    return operate(result, op, num)


def evaluate2(expr: list[str]) -> int:
    # expr in this function is guaranteed to not contain any bracketed groups
    add_count = expr.count("+")
    while add_count > 0:
        for i, s in enumerate(expr):
            if s == "+":
                value = int(expr[i - 1]) + int(expr[i + 1])
                expr = expr[: i - 1] + [str(value)] + expr[i + 2 :]
                add_count -= 1
                break

    ans = 1
    for s in expr:
        if s.isdigit():
            ans *= int(s)

    return ans


def part1() -> None:
    total = 0
    for expr in exprs:
        total += evaluate(expr, 0)
    print(total)


def part2() -> None:
    total = 0
    for expr in exprs:
        expr = expr.replace("(", "( ").replace(")", " )")
        expr = expr.split()
        bracket_groups = expr.count("(")
        while bracket_groups > 0:
            start = end = 0
            for index, part in enumerate(expr):
                if part == "(":
                    start = index
                elif part == ")":
                    end = index
                    ans = evaluate2(expr[start + 1 : end])
                    expr = expr[:start] + [str(ans)] + expr[end + 1 :]
                    bracket_groups -= 1
                    break
        total += evaluate2(expr)

    print(total)


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as fd:
        exprs = [line.strip() for line in fd.readlines()]

    part1()
    part2()
