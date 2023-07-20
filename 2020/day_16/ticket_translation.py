""" https://adventofcode.com/2020/day/16 """

import os
import re
from collections import defaultdict


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> set[int]:
    invalid_sum = 0
    invalid_tickets = set()
    for index, ticket in enumerate(nearby_tickets):
        for value in ticket:
            valid = False
            for fint, sint in field_values.values():
                valid |= fint[0] <= value <= fint[1]
                valid |= sint[0] <= value <= sint[1]
            if not valid:
                invalid_sum += value
                invalid_tickets.add(index)
    print(invalid_sum)
    return invalid_tickets


def part2() -> None:
    field_pos = defaultdict(set)

    # for each `pos` check which fields are valid for it
    # store the findings as set of valid positions for each field
    for pos in range(len(field_values)):
        for field, intervals in field_values.items():
            valid = True
            for index, ticket in enumerate(nearby_tickets):
                if index in invalid:
                    continue
                valid &= (
                    intervals[0][0] <= ticket[pos] <= intervals[0][1]
                    or intervals[1][0] <= ticket[pos] <= intervals[1][1]
                )
            if valid:
                field_pos[field].add(pos)

    # process each field in sorted order of number of valid positions
    # this ensures that each field gets a unique valid position
    field_pos_items = list(field_pos.items())
    field_pos_items.sort(key=lambda p: len(p[1]))

    used = set()
    result = 1

    for field, pos_set in field_pos_items:
        for pos in pos_set:
            if pos not in used:
                used.add(pos)
                if "departure" in field:
                    result *= my_ticket[pos]

    print(result)


if __name__ == "__main__":
    with open(get_file_path("field_rules.txt")) as fd:
        _rules = [line.strip() for line in fd.readlines()]

    with open(get_file_path("my_ticket.txt")) as fd:
        my_ticket = fd.readline().strip().split(",")

    with open(get_file_path("nearby_tickets.txt")) as fd:
        nearby_tickets = [line.strip().split(",") for line in fd.readlines()]

    field_values = {}
    for index, rule in enumerate(_rules):
        _field, _first_interval, _second_interval = re.split(r":\s|\sor\s", rule)
        _first_interval = list(map(int, _first_interval.split("-")))
        _second_interval = list(map(int, _second_interval.split("-")))
        field_values[_field] = [_first_interval, _second_interval]

    del _rules

    my_ticket = list(map(int, my_ticket))

    for index, ticket in enumerate(nearby_tickets):
        ticket = list(map(int, ticket))
        nearby_tickets[index] = ticket

    invalid = part1()
    part2()
