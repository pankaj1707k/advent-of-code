""" https://adventofcode.com/2022/day/8 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def parse_input() -> list[list[int]]:
    grid = []
    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            grid.append(list(map(int, line.strip())))
    return grid


def check_visibility(row: int, col: int) -> bool:
    # top
    for r in range(row - 1, -1, -1):
        if grid[r][col] >= grid[row][col]:
            break
    else:
        return True

    # bottom
    for r in range(row + 1, M):
        if grid[r][col] >= grid[row][col]:
            break
    else:
        return True

    # left
    for c in range(col - 1, -1, -1):
        if grid[row][c] >= grid[row][col]:
            break
    else:
        return True

    # right
    for c in range(col + 1, N):
        if grid[row][c] >= grid[row][col]:
            break
    else:
        return True

    return False


def part_1() -> int:
    count = 0
    for row in range(M):
        for col in range(N):
            count += int(check_visibility(row, col))
    return count


def scenic_score(row: int, col: int) -> int:
    score = 1

    # top
    for r in range(row - 1, -1, -1):
        if grid[r][col] >= grid[row][col]:
            score *= row - r
            break
    else:
        score *= row

    # bottom
    for r in range(row + 1, M):
        if grid[r][col] >= grid[row][col]:
            score *= r - row
            break
    else:
        score *= M - row - 1

    # left
    for c in range(col - 1, -1, -1):
        if grid[row][c] >= grid[row][col]:
            score *= col - c
            break
    else:
        score *= col

    # right
    for c in range(col + 1, N):
        if grid[row][c] >= grid[row][col]:
            score *= c - col
            break
    else:
        score *= N - col - 1

    return score


def part_2() -> int:
    max_score = 0
    for row in range(1, M - 1):
        for col in range(1, N - 1):
            max_score = max(max_score, scenic_score(row, col))
    return max_score


if __name__ == "__main__":
    grid = parse_input()
    M, N = len(grid), len(grid[0])
    print(part_1())  # output: 1807
    print(part_2())  # output: 480000
