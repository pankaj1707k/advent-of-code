""" https://adventofcode.com/2023/day/19 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def run_workflows(part: dict[str, int]) -> str:
    wf = "in"
    while wf not in "AR":
        for rule in workflows[wf]:
            if len(rule) == 1:
                wf = rule[0]
                break
            if eval(f"{part[rule[0][0]]}{rule[0][1:]}"):
                wf = rule[1]
                break
    return wf


def part1() -> None:
    result = 0
    for part in parts:
        if run_workflows(part) == "A":
            result += sum(part.values())
    print(result)


def count_accepted(
    wf: str,
    x: tuple[int, int],
    m: tuple[int, int],
    a: tuple[int, int],
    s: tuple[int, int],
) -> int:
    if wf == "R":
        return 0
    if wf == "A":
        return (
            (x[1] - x[0] + 1)
            * (m[1] - m[0] + 1)
            * (a[1] - a[0] + 1)
            * (s[1] - s[0] + 1)
        )
    total = 0
    for rule in workflows[wf]:
        if rule[0].startswith("x>"):
            total += count_accepted(rule[1], (int(rule[0][2:]) + 1, x[1]), m, a, s)
            x = (x[0], int(rule[0][2:]))
        elif rule[0].startswith("x<"):
            total += count_accepted(rule[1], (x[0], int(rule[0][2:]) - 1), m, a, s)
            x = (int(rule[0][2:]), x[1])
        elif rule[0].startswith("m>"):
            total += count_accepted(rule[1], x, (int(rule[0][2:]) + 1, m[1]), a, s)
            m = (m[0], int(rule[0][2:]))
        elif rule[0].startswith("m<"):
            total += count_accepted(rule[1], x, (m[0], int(rule[0][2:]) - 1), a, s)
            m = (int(rule[0][2:]), m[1])
        elif rule[0].startswith("a>"):
            total += count_accepted(rule[1], x, m, (int(rule[0][2:]) + 1, a[1]), s)
            a = (a[0], int(rule[0][2:]))
        elif rule[0].startswith("a<"):
            total += count_accepted(rule[1], x, m, (a[0], int(rule[0][2:]) - 1), s)
            a = (int(rule[0][2:]), a[1])
        elif rule[0].startswith("s>"):
            total += count_accepted(rule[1], x, m, a, (int(rule[0][2:]) + 1, s[1]))
            s = (s[0], int(rule[0][2:]))
        elif rule[0].startswith("s<"):
            total += count_accepted(rule[1], x, m, a, (s[0], int(rule[0][2:]) - 1))
            s = (int(rule[0][2:]), s[1])
        else:
            total += count_accepted(rule[0], x, m, a, s)
    return total


def part2() -> None:
    result = count_accepted("in", *[(1, 4000) for _ in range(4)])
    print(result)


if __name__ == "__main__":
    workflows: dict[str, list[tuple[str, ...]]] = {}
    parts: list[dict[str, int]] = []

    with open(get_file_path("input.txt")) as infile:
        _flows, _parts = infile.read().strip().split("\n\n")
        for wf in _flows.splitlines():
            name, desc = wf.split("{")
            workflows[name] = [tuple(rule.split(":")) for rule in desc[:-1].split(",")]
        for part in _parts.splitlines():
            part_entry = {}
            for rule in part[1:-1].split(","):
                category, value = rule.split("=")
                part_entry[category] = int(value)
            parts.append(part_entry)

    part1()
    part2()
