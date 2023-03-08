""" https://adventofcode.com/2021/day/12 """

import os
from collections import defaultdict


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.graph: defaultdict[str, set[str]] = defaultdict(set)

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                u, v = line.strip().split("-")
                self.graph[u].add(v)
                self.graph[v].add(u)

    def _dfs1(self, node: str, path: list[str]) -> int:
        if node == "end":
            # print(",".join(path))
            return 1
        path_count = 0
        for child in self.graph[node]:
            if child.isupper() or child not in path:
                path.append(child)
                path_count += self._dfs1(child, path)
                _ = path.pop()
        return path_count

    def part1(self) -> None:
        total_paths = self._dfs1("start", ["start"])
        print(total_paths)

    def _dfs2(self, node: str, path: dict[str, int]) -> int:
        if node == "end":
            return 1

        small_twice = False
        for v in path:
            if v.islower() and path[v] == 2:
                small_twice = True
                break

        path_count = 0
        for child in self.graph[node]:
            if child == "start":
                continue
            if child.isupper() or not small_twice or (small_twice and path[child] == 0):
                path[child] += 1
                path_count += self._dfs2(child, path)
                path[child] -= 1

        return path_count

    def part2(self) -> None:
        path = defaultdict(int)
        path["start"] = 1
        total_paths = self._dfs2("start", path)
        print(total_paths)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
