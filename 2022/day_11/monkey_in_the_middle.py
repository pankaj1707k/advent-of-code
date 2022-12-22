""" https://adventofcode.com/2022/day/11 """

import os
from collections import deque


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Monkey:
    def __init__(self) -> None:
        self.items: deque = deque()
        self.operator: str = None
        self.const_operand: int = None
        self.test_num: int = None
        self.true_monkey: int = None
        self.false_monkey: int = None
        self.inspections: int = 0

    def compute_worry(self, old_worry: int) -> int:
        operand = self.const_operand if self.const_operand else old_worry
        if self.operator == "*":
            return old_worry * operand
        if self.operator == "+":
            return old_worry + operand


class Solution:
    def parse_input(self):
        self.monkeys: list[Monkey] = list()
        with open(get_file_path("input.txt")) as infile:
            lines = [line.strip().split() for line in infile.readlines()]
        for index, line in enumerate(lines):
            if index % 7 == 0:
                self.monkeys.append(Monkey())
            elif index % 7 == 1:
                self.monkeys[-1].items = deque(eval("".join(line[2:]) + ","))
            elif index % 7 == 2:
                self.monkeys[-1].operator = line[-2]
                if line[-1].isdigit():
                    self.monkeys[-1].const_operand = int(line[-1])
            elif index % 7 == 3:
                self.monkeys[-1].test_num = int(line[-1])
            elif index % 7 == 4:
                self.monkeys[-1].true_monkey = int(line[-1])
            elif index % 7 == 5:
                self.monkeys[-1].false_monkey = int(line[-1])

    def print_monkeys(self):
        for monkey in self.monkeys:
            print(*monkey.items)
            print(monkey.operator)
            print(monkey.const_operand)
            print(monkey.test_num)
            print(monkey.true_monkey)
            print(monkey.false_monkey)
            print(monkey.inspections)
            print()

    def _compute_monkey_business(self, rounds: int, part: int):
        test_num_prod = 1
        for monkey in self.monkeys:
            test_num_prod *= monkey.test_num

        for _ in range(rounds):
            for monkey in self.monkeys:
                while monkey.items:
                    item_worry = monkey.items.popleft()
                    item_worry = monkey.compute_worry(item_worry)
                    if part == 1:
                        item_worry //= 3
                    else:
                        item_worry %= test_num_prod
                    if item_worry % monkey.test_num == 0:
                        index = monkey.true_monkey
                    else:
                        index = monkey.false_monkey
                    self.monkeys[index].items.append(item_worry)
                    monkey.inspections += 1

        _monkeys = sorted(self.monkeys, key=lambda m: m.inspections, reverse=True)
        monkey_business = _monkeys[0].inspections * _monkeys[1].inspections
        print(monkey_business)

    def part_1(self):
        self._compute_monkey_business(20, 1)

    def part_2(self):
        self._compute_monkey_business(10000, 2)


if __name__ == "__main__":
    soln = Solution()
    soln.parse_input()
    soln.part_1()
    soln.parse_input()
    soln.part_2()
