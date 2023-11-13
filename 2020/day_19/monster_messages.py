""" https://adventofcode.com/2020/day/19 """

import os
import re


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


# good enough for part 1
def get_strings(rule: str | int, possible_strings: dict[int, set[str]]) -> set[str]:
    if isinstance(rule, str):
        return {rule}
    if rule in possible_strings:
        return possible_strings[rule]

    strings = set()
    for subrule in rules[rule]:
        if len(subrule) == 1:
            strings |= get_strings(subrule[0], possible_strings)
        else:
            left, right = get_strings(subrule[0], possible_strings), get_strings(
                subrule[1], possible_strings
            )
            for s in left:
                for r in right:
                    strings.add(s + r)

    possible_strings[rule] = strings
    return strings


def check_message(
    message: str, start_indexes: tuple[int, ...], rule: str
) -> tuple[int, ...]:
    rule_desc = rules[rule]
    overall_valid_starts = tuple()

    for start_index in start_indexes:
        # message fully checked
        if start_index >= len(message):
            continue
        # current rule is leaf node
        if rule_desc[0][0].isalpha():
            # match single character and add add next index as a start point
            if rule_desc[0][0] == message[start_index]:
                overall_valid_starts += (start_index + 1,)
            continue

        for option in rule_desc:
            starts = (start_index,)
            invalid = False
            # recursively (in DFS order) check if the message is valid for all
            # rules for the current option (path).
            for next_rule in option:
                local_valid_starts = check_message(message, starts, next_rule)
                # if no valid start points are found, then the message cannot
                # be constructed from the current option. Thus, move to the
                # next option skipping all remaining rules in the current one.
                if not local_valid_starts:
                    invalid = True
                    break
                starts = local_valid_starts
            if not invalid:
                overall_valid_starts += starts

    return overall_valid_starts


def part1() -> None:
    result = 0

    for message in messages:
        pivots = check_message(message, (0,), "0")
        if pivots and len(message) in pivots:
            result += 1

    print(result)


def part2() -> None:
    rules["8"] = [["42"], ["42", "8"]]
    rules["11"] = [["42", "31"], ["42", "11", "31"]]
    result = 0

    for message in messages:
        pivots = check_message(message, (0,), "0")
        if pivots and len(message) in pivots:
            result += 1

    print(result)


if __name__ == "__main__":
    with open(get_file_path("rules.txt")) as fd:
        rules_raw = [line.strip() for line in fd.readlines()]

    with open(get_file_path("messages.txt")) as fd:
        messages = [line.strip() for line in fd.readlines()]

    rules: dict[str, list[list[str]]] = {}

    for rule in rules_raw:
        parts: list[str] = re.split(r":\s|\s", rule)
        key = parts[0]
        value = []
        subrule = []
        for p in parts[1:]:
            if p == "|":
                value.append(subrule.copy())
                subrule.clear()
            elif p.isdigit():
                subrule.append(p)
            else:
                subrule.append(p.strip('"'))
        if subrule:
            value.append(subrule.copy())
        rules[key] = value

    part1()
    part2()
