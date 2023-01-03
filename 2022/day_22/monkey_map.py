""" https://adventofcode.com/2022/day/22 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.map: list[list[str]] = []
        self.path: list[str | int] = []
        self.cstart: list[int] = []
        self.cend: list[int] = []
        self.rstart: list[int] = []
        self.rend: list[int] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            lines = [line.rstrip() for line in infile.readlines()]

        i = 0
        while lines[i]:
            self.map.append(list(lines[i]))
            i += 1

        max_col = max(map(len, self.map))

        for i in range(len(self.map)):
            self.map[i] += [" " for _ in range(max_col - len(self.map[i]))]

        pathstr = lines[-1]
        i = 0
        while i < len(pathstr):
            num = ""
            while i < len(pathstr) and pathstr[i].isdigit():
                num += pathstr[i]
                i += 1
            if num:
                self.path.append(int(num))
            if i < len(pathstr) and pathstr[i].isalpha():
                self.path.append(pathstr[i])
            i += 1

        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if not self.map[i][j].isspace():
                    self.rstart.append(j)
                    break
            for j in range(len(self.map[i]) - 1, -1, -1):
                if not self.map[i][j].isspace():
                    self.rend.append(j)
                    break

        for j in range(max(map(len, self.map))):
            for i in range(len(self.map)):
                if not self.map[i][j].isspace():
                    self.cstart.append(i)
                    break
            for i in range(len(self.map) - 1, -1, -1):
                if not self.map[i][j].isspace():
                    self.cend.append(i)
                    break

    def part1(self) -> None:
        start = None
        for j in range(len(self.map[0])):
            if self.map[0][j] == ".":
                start = [0, j]
                break

        d = 0  # direction: 0->right, 1->down, 2->left, 3->up
        i, j = start

        for x in self.path:
            if isinstance(x, int):
                if d == 0:
                    for _ in range(x):
                        if j + 1 <= self.rend[i] and self.map[i][j + 1] == ".":
                            j += 1
                        elif j == self.rend[i] and self.map[i][self.rstart[i]] == ".":
                            j = self.rstart[i]
                elif d == 1:
                    for _ in range(x):
                        if i + 1 <= self.cend[j] and self.map[i + 1][j] == ".":
                            i += 1
                        elif i == self.cend[j] and self.map[self.cstart[j]][j] == ".":
                            i = self.cstart[j]
                elif d == 2:
                    for _ in range(x):
                        if j - 1 >= self.rstart[i] and self.map[i][j - 1] == ".":
                            j -= 1
                        elif j == self.rstart[i] and self.map[i][self.rend[i]] == ".":
                            j = self.rend[i]
                else:
                    for _ in range(x):
                        if i - 1 >= self.cstart[j] and self.map[i - 1][j] == ".":
                            i -= 1
                        elif i == self.cstart[j] and self.map[self.cend[j]][j] == ".":
                            i = self.cend[j]
            else:
                if d == 0:
                    if x == "L":
                        d = 3
                    else:
                        d = 1
                elif d == 1:
                    if x == "L":
                        d = 0
                    else:
                        d = 2
                elif d == 2:
                    if x == "L":
                        d = 1
                    else:
                        d = 3
                else:
                    if x == "L":
                        d = 2
                    else:
                        d = 0

        password = 1000 * (i + 1) + 4 * (j + 1) + d
        print(password)

    def part2(self) -> None:
        start = None
        for j in range(len(self.map[0])):
            if self.map[0][j] == ".":
                start = [0, j]
                break

        d = 0  # direction: 0->right, 1->down, 2->left, 3->up
        r, c = start
        dirs = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}

        for x in self.path:
            if x == "L" or x == "R":
                if d == 0:
                    if x == "L":
                        d = 3
                    else:
                        d = 1
                elif d == 1:
                    if x == "L":
                        d = 0
                    else:
                        d = 2
                elif d == 2:
                    if x == "L":
                        d = 1
                    else:
                        d = 3
                else:
                    if x == "L":
                        d = 2
                    else:
                        d = 0
            else:
                for _ in range(x):
                    cd = d
                    dr, dc = dirs[d]
                    nr, nc = r + dr, c + dc

                    if 0 <= nr < 50 and nc == 150 and d == 0:
                        d = 2
                        nr, nc = 149 - nr, 99
                    elif 0 <= nr < 50 and nc == 49 and d == 2:
                        d = 0
                        nr, nc = 149 - nr, 0
                    elif 50 <= nc < 100 and nr < 0 and d == 3:
                        d = 0
                        nr, nc = nc + 100, 0
                    elif 100 <= nc < 150 and nr < 0 and d == 3:
                        nr, nc = 199, nc - 100
                    elif 100 <= nc < 150 and nr == 50 and d == 1:
                        d = 2
                        nr, nc = nc - 50, 99
                    elif 50 <= nr < 100 and nc == 49 and d == 2:
                        d = 1
                        nr, nc = 100, nr - 50
                    elif 50 <= nr < 100 and nc == 100 and d == 0:
                        d = 3
                        nr, nc = 49, nr + 50
                    elif 100 <= nr < 150 and nc == 100 and d == 0:
                        d = 2
                        nr, nc = 149 - nr, 149
                    elif 50 <= nc < 100 and nr == 150 and d == 1:
                        d = 2
                        nr, nc = nc + 100, 49
                    elif 0 <= nc < 50 and nr == 99 and d == 3:
                        d = 0
                        nr, nc = nc + 50, 50
                    elif 100 <= nr < 150 and nc < 0 and d == 2:
                        d = 0
                        nr, nc = 149 - nr, 50
                    elif 150 <= nr < 200 and nc < 0 and d == 2:
                        d = 1
                        nr, nc = 0, nr - 100
                    elif 150 <= nr < 200 and nc == 50 and d == 0:
                        d = 3
                        nr, nc = 149, nr - 100
                    elif 0 <= nc < 50 and nr == 200 and d == 1:
                        nr, nc = 0, nc + 100

                    if self.map[nr][nc] == "#":
                        d = cd
                        break

                    r, c = nr, nc

        password = 1000 * (r + 1) + 4 * (c + 1) + d
        print(password)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
