""" https://adventofcode.com/2022/day/21 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Node:
    def __init__(self) -> None:
        self.key: str = None
        self.val: int = None
        self.operator: str = None
        self.left = None
        self.right = None


class Solution:
    def __init__(self) -> None:
        self.tree: dict[str, Node] = {}

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                line = line.strip().split()
                monkey = line[0].rstrip(":")
                if monkey not in self.tree:
                    self.tree[monkey] = Node()
                    self.tree[monkey].key = monkey
                if len(line[1:]) == 1:
                    self.tree[monkey].val = int(line[1])
                else:
                    if line[1] not in self.tree:
                        self.tree[line[1]] = Node()
                        self.tree[line[1]].key = line[1]
                    if line[3] not in self.tree:
                        self.tree[line[3]] = Node()
                        self.tree[line[3]].key = line[3]
                    self.tree[monkey].operator = line[2]
                    self.tree[monkey].left = self.tree[line[1]]
                    self.tree[monkey].right = self.tree[line[3]]

    def evaluate(self, node: Node) -> int:
        if node.operator:
            left_num = self.evaluate(node.left)
            right_num = self.evaluate(node.right)
            if node.operator == "+":
                node.val = left_num + right_num
            elif node.operator == "-":
                node.val = left_num - right_num
            elif node.operator == "*":
                node.val = left_num * right_num
            else:
                node.val = int(left_num / right_num)
        return node.val

    def reverse_evaluate(self, node: Node, val: int) -> None:
        if node.key == "humn":
            node.val = val
            return
        # perform opposite operations to solve for the value of 'humn'
        # the operands for the oppsite operations are: `val` evaluated
        # upto this point, and the value of the subtree not containing
        # 'humn' below the current `node`
        if self.search(node.left, self.tree["humn"]):
            if node.operator == "/":
                return self.reverse_evaluate(node.left, val * self.evaluate(node.right))
            if node.operator == "+":
                return self.reverse_evaluate(node.left, val - self.evaluate(node.right))
            if node.operator == "-":
                return self.reverse_evaluate(node.left, val + self.evaluate(node.right))
            if node.operator == "*":
                return self.reverse_evaluate(
                    node.left, val // self.evaluate(node.right)
                )
        if node.operator == "/":
            return self.reverse_evaluate(node.right, self.evaluate(node.left) // val)
        if node.operator == "+":
            return self.reverse_evaluate(node.right, val - self.evaluate(node.left))
        if node.operator == "-":
            return self.reverse_evaluate(node.right, self.evaluate(node.left) - val)
        if node.operator == "*":
            return self.reverse_evaluate(node.right, val // self.evaluate(node.left))

    def search(self, node: Node, target: Node) -> bool:
        if not node:
            return False
        if node.key == target.key:
            return True
        return self.search(node.left, target) or self.search(node.right, target)

    def part1(self) -> None:
        root_num = self.evaluate(self.tree["root"])
        print(root_num)

    def part2(self) -> None:
        self.tree["humn"].val = 0
        self.tree["root"].operator = "="

        # calculate the value for the subtree not containing 'humn'
        # use the value to reverse evaluate the other subtree to
        # calculate the value yelled by 'humn' for the equality
        # condition at the 'root' to hold
        if self.search(self.tree["root"].left, self.tree["humn"]):
            one_half = self.evaluate(self.tree["root"].right)
            self.reverse_evaluate(self.tree["root"].left, one_half)
        else:
            one_half = self.evaluate(self.tree["root"].left)
            self.reverse_evaluate(self.tree["root"].right, one_half)

        print(self.tree["humn"].val)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
