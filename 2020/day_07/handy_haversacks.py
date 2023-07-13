""" https://adventofcode.com/2020/day/7 """

import os
import re
from collections import defaultdict
from functools import cache


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    @cache
    def exists(node: str) -> bool:
        for child, _ in tree[node]:
            if child == "shiny gold":
                return True

        shiny_gold = False
        for child, _ in tree[node]:
            shiny_gold |= exists(child)

        return shiny_gold

    result = 0
    for node in tree:
        result += int(exists(node))
    print(result)


def part2() -> None:
    @cache
    def count_bags(node: str) -> int:
        bags = 0
        for child, count in tree[node]:
            bags += count * count_bags(child) + count
        return bags

    result = count_bags("shiny gold")
    print(result)


def parse_rule(rule: str) -> tuple[str, set[tuple[str, int]]]:
    components = re.split(r"\sbags\scontain\s|\sbags,\s|\sbag,\s|\sbags.|\sbag.", rule)
    key = components[0].strip()
    values = set()
    for component in components[1:]:
        if component:
            num, color = component.strip().split(maxsplit=1)
            if num != "no":
                values.add((color, int(num)))
    return [key, values]


def construct_tree(rules: list[str]) -> dict[str, set[tuple[str, int]]]:
    tree = defaultdict(set)

    for rule in rules:
        node, children = parse_rule(rule)
        tree[node] = children

    return tree


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as fd:
        rules = [line.strip() for line in fd.readlines()]

    tree = construct_tree(rules)
    part1()
    part2()
