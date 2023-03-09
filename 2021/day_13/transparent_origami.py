""" https://adventofcode.com/2021/day/13 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.points: set[tuple[int, int]] = set()
        self.fold_lines: list[tuple[str, int]] = list()

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            lines = list(map(lambda l: l.strip(), infile.readlines()))

        line_index = 0
        while lines[line_index]:
            self.points.add(tuple(map(int, lines[line_index].split(","))))
            line_index += 1

        line_index += 1
        while line_index < len(lines):
            line = lines[line_index].split()[-1]
            line = line.split("=")
            line[1] = int(line[1])
            self.fold_lines.append(tuple(line))
            line_index += 1

    def get_points_after_fold(
        self, points: set[tuple[int, int]], fold: tuple[str, int]
    ) -> set[tuple[int, int]]:
        after_fold = set()
        for x, y in points:
            if fold[0] == "y" and y > fold[1]:
                after_fold.add((x, 2 * fold[1] - y))
            elif fold[0] == "x" and x > fold[1]:
                after_fold.add((2 * fold[1] - x, y))
            else:
                after_fold.add((x, y))
        return after_fold

    def part1(self) -> None:
        points = self.get_points_after_fold(self.points.copy(), self.fold_lines[0])
        print(len(points))

    def part2(self) -> None:
        points = self.points.copy()
        for fold in self.fold_lines:
            points = self.get_points_after_fold(points, fold)

        # output points in the form of grid
        max_x = max(x for x, _ in points)
        max_y = max(y for _, y in points)
        grid = [["."] * (max_x + 1) for _ in range(max_y + 1)]
        for x, y in points:
            grid[y][x] = "#"

        for row in grid:
            print(" ".join(row))


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
