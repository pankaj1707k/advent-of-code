""" https://adventofcode.com/2024/day/15 """

from collections import deque
import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


DIRS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

def move_horizontal(grid, sr, sc, move) -> tuple[int, int]:
    _, d = DIRS[move]
    c = sc
    while grid[sr][c] not in '.#':
        c += d
    if grid[sr][c] == '#':
        return sr, sc
    while grid[sr][c] != '@':
        grid[sr][c] = grid[sr][c - d]
        c -= d
    grid[sr][c] = '.'
    return sr, sc + d


def move_vertical(grid, sr, sc, move):
    d, _ = DIRS[move]
    boxes = {(sr, sc)}
    que = deque([(sr, sc)])
    movable = True
    while que:
        r, c = que.popleft()
        if (r + d, c) in boxes: continue
        if grid[r + d][c] == '#':
            movable = False
            break
        if grid[r + d][c] == '[':
            que.append((r + d, c))
            que.append((r + d, c + 1))
            boxes.add((r + d, c))
            boxes.add((r + d, c + 1))
        elif grid[r + d][c] == ']':
            que.append((r + d, c))
            que.append((r + d, c - 1))
            boxes.add((r + d, c))
            boxes.add((r + d, c - 1))
    if not movable: return sr, sc
    copy = [list(row) for row in grid]
    grid[sr][sc] = '.'
    grid[sr + d][sc] = '@'
    for r, c in boxes:
        grid[r][c] = '.'
    for r, c in boxes:
        grid[r + d][c] = copy[r][c]
    return sr + d, sc


def main():
    grid: list[list[str]] = []
    moves: str = ''

    with open(get_file_path('input.txt')) as fd:
        top, bottom = fd.read().split('\n\n')
        moves = ''.join(bottom.splitlines())
        for line in top.splitlines():
            row = []
            for char in line:
                if char == 'O':
                    row.append('[')
                    row.append(']')
                elif char == '.':
                    row.append('.')
                    row.append('.')
                elif char == '#':
                    row.append('#')
                    row.append('#')
                else:
                    row.append('@')
                    row.append('.')
            grid.append(row)

    R = len(grid)
    C = len(grid[0])

    r = c = 0
    for i in range(R):
        for j in range(C):
            if grid[i][j] == '@':
                r, c = i, j
                break

    for i, move in enumerate(moves):
        if move in '<>':
            r, c = move_horizontal(grid, r, c, move)
        else:
            r, c = move_vertical(grid, r, c, move)


    result = sum(100 * i + j if grid[i][j] == '[' else 0 for i in range(R) for j in range(C))
    print(result)


main()
