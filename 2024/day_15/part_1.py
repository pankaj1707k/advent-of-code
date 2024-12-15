""" https://adventofcode.com/2024/day/15 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def main():
    grid: list[list[str]] = []
    moves: str = ""

    with open(get_file_path("input.txt")) as fd:
        top, bottom = fd.read().split("\n\n")
        grid = [list(line) for line in top.split("\n")]
        moves = "".join(bottom.split("\n"))

    n = len(grid)
    r = c = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == "@":
                r, c = i, j
                break

    DIRS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    for move in moves:
        dr, dc = DIRS[move]
        nr, nc = r + dr, c + dc
        is_movable = True
        while True:
            if grid[nr][nc] == 'O':
                nr += dr
                nc += dc
            elif grid[nr][nc] == '#':
                is_movable = False
                break
            else: break
        if is_movable:
            grid[nr][nc] = 'O'
            grid[r + dr][c + dc] = '@'
            grid[r][c] = '.'
            r += dr
            c += dc

    print('\n'.join([''.join(line) for line in grid]))

    result = sum(100 * i + j if grid[i][j] == 'O' else 0 for i in range(n) for j in range(n))
    print(result)


main()
