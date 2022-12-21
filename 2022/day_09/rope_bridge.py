""" https://adventofcode.com/2022/day/9 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input():
    moves = []
    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            moves.append(line.strip().split())
            moves[-1][1] = int(moves[-1][1])
    return moves


def part_1():
    visited = set()
    trow = tcol = hrow = hcol = 0
    visited.add((trow, tcol))
    for direction, steps in moves:
        drow = dcol = 0
        if direction == "R":
            dcol = 1
        elif direction == "D":
            drow = -1
        elif direction == "L":
            dcol = -1
        else:
            drow = 1
        for _ in range(steps):
            hrow += drow
            hcol += dcol
            if abs(hrow - trow) > 1 or abs(hcol - tcol) > 1:
                if hrow == trow or hcol == tcol:
                    # up, down, right, left chase
                    trow += drow
                    tcol += dcol
                else:
                    # diagonal chase
                    trow += -1 if hrow < trow else 1
                    tcol += -1 if hcol < tcol else 1
                visited.add((trow, tcol))
    return len(visited)


def part_2():
    visited = set()
    # index 0 -> head, -1 -> tail
    rows = [0] * 10
    cols = [0] * 10
    visited.add((rows[0], cols[0]))

    for direction, steps in moves:
        drow = dcol = 0
        if direction == "R":
            dcol = 1
        elif direction == "D":
            drow = -1
        elif direction == "L":
            dcol = -1
        else:
            drow = 1

        for _ in range(steps):
            rows[0] += drow
            cols[0] += dcol
            for i in range(1, 10):
                dist = max(abs(rows[i - 1] - rows[i]), abs(cols[i - 1] - cols[i]))
                if dist > 1:
                    if rows[i - 1] != rows[i] and cols[i - 1] != cols[i]:
                        if rows[i - 1] > rows[i] and cols[i - 1] > cols[i]:
                            rows[i] += 1
                            cols[i] += 1
                        elif rows[i - 1] > rows[i] and cols[i - 1] < cols[i]:
                            rows[i] += 1
                            cols[i] -= 1
                        elif rows[i - 1] < rows[i] and cols[i - 1] > cols[i]:
                            rows[i] -= 1
                            cols[i] += 1
                        elif rows[i - 1] < rows[i] and cols[i - 1] < cols[i]:
                            rows[i] -= 1
                            cols[i] -= 1
                    elif rows[i - 1] != rows[i] or cols[i - 1] != cols[i]:
                        if rows[i - 1] > rows[i]:
                            rows[i] += 1
                        elif rows[i - 1] < rows[i]:
                            rows[i] -= 1
                        elif cols[i - 1] > cols[i]:
                            cols[i] += 1
                        elif cols[i - 1] < cols[i]:
                            cols[i] -= 1

            visited.add((rows[-1], cols[-1]))

    return len(visited)


if __name__ == "__main__":
    moves = parse_input()
    print(part_1())  # output: 6337
    print(part_2())  # output: 2455
