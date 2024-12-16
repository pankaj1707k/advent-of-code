""" https://adventofcode.com/2024/day/16 """

from heapq import heappush, heappop
import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def main():
    maze: list[str] = []

    with open(get_file_path('input.txt')) as fd:
        maze = fd.read().splitlines()

    N = len(maze)
    INF = 10 ** 9
    min_score = [[INF] * N for _ in range(N)]
    pq = [(0, N - 2, 1, 0, 1)]  # score, row, col, dr, dc
    visited = set()
    while pq:
        score, row, col, dr, dc = heappop(pq)
        if maze[row][col] == '#': continue
        if (row, col, dr, dc) in visited or (row, col, -dr, -dc) in visited:
            continue
        visited.add((row, col, dr, dc))
        if score + 1 < min_score[row + dr][col + dc]:
            min_score[row + dr][col + dc] = score + 1
            heappush(pq, (score + 1, row + dr, col + dc, dr, dc))
        if score + 1001 < min_score[row + dc][col - dr]:  # clockwise turn
            min_score[row + dc][col - dr] = score + 1001
            heappush(pq, (score + 1001, row + dc, col - dr, dc, -dr))
        if score + 1001 < min_score[row - dc][col + dr]:  # anti-clockwise turn
            min_score[row - dc][col + dr] = score + 1001
            heappush(pq, (score + 1001, row - dc, col + dr, -dc, dr))

    print(min_score[1][N - 2])


main()
