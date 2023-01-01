""" https://adventofcode.com/2022/day/20 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Node:
    """Doubly linked list node"""

    def __init__(self, val: int) -> None:
        self.val = val
        self.prev = None
        self.next = None


class Solution:
    def __init__(self) -> None:
        self.file: list[int] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                val = int(line.strip())
                self.file.append(val)

    def mix(self, enc_file: list[Node]) -> Node:
        """Mix enc_file once and return node with value 0"""
        mod = len(enc_file) - 1

        for curr in enc_file:
            if curr.val == 0:
                zero_node = curr
                continue
            node = curr
            if curr.val > 0:
                for _ in range(curr.val % mod):
                    node = node.next
                if node == curr:
                    continue
                curr.next.prev = curr.prev
                curr.prev.next = curr.next
                curr.next = node.next
                curr.prev = node
                node.next = curr
                curr.next.prev = curr
            else:
                for _ in range(-curr.val % mod):
                    node = node.prev
                if node == curr:
                    continue
                curr.next.prev = curr.prev
                curr.prev.next = curr.next
                curr.prev = node.prev
                curr.next = node
                node.prev = curr
                curr.prev.next = curr

        return zero_node

    def part1(self) -> None:
        # construct doubly linked list
        enc_file = [Node(val) for val in self.file]
        for index, node in enumerate(enc_file):
            node.prev = enc_file[(index - 1) % len(enc_file)]
            node.next = enc_file[(index + 1) % len(enc_file)]

        zero_node = self.mix(enc_file)

        total = 0
        for _ in range(3):
            for __ in range(1000):
                zero_node = zero_node.next
            total += zero_node.val

        print(total)

    def part2(self) -> None:
        enc_key = 811589153
        mix_count = 10

        enc_file = [Node(val * enc_key) for val in self.file]
        for index, node in enumerate(enc_file):
            node.prev = enc_file[(index - 1) % len(enc_file)]
            node.next = enc_file[(index + 1) % len(enc_file)]

        for _ in range(mix_count):
            zero_node = self.mix(enc_file)

        total = 0
        for _ in range(3):
            for __ in range(1000):
                zero_node = zero_node.next
            total += zero_node.val

        print(total)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
