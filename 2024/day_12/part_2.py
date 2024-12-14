""" https://adventofcode.com/2024/day/12 """

from collections import deque
import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def main():
    farm: list[str] = []

    with open(get_file_path("input.txt")) as fd:
        farm = fd.read().splitlines()

    total_cost = 0
    rows = len(farm)
    cols = len(farm[0])
    dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    seen = set()
    for sr in range(rows):
        for sc in range(cols):
            if (sr, sc) in seen:
                continue
            que = deque([(sr, sc)])
            plant = farm[sr][sc]
            edges = set()  # (r, c, dr, dc)
            region = set()
            while que:
                r, c = que.popleft()
                if (r, c) in region:
                    continue
                region.add((r, c))
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if (
                        nr < 0
                        or nc < 0
                        or nr >= rows
                        or nc >= cols
                        or farm[nr][nc] != plant
                    ):
                        edges.add((r, c, dr, dc))
                        continue
                    que.append((nr, nc))

            used_edges = set()
            sides = 0
            for er, ec, dr, dc in edges:
                if (er, ec, dr, dc) in used_edges:
                    continue
                used_edges.add((er, ec, dr, dc))
                sides += 1
                r, c = er, ec
                while (r + dc, c - dr, dr, dc) in edges:
                    used_edges.add((r + dc, c - dr, dr, dc))
                    r, c = r + dc, c - dr
                r, c = er, ec
                while (r - dc, c + dr, dr, dc) in edges:
                    used_edges.add((r - dc, c + dr, dr, dc))
                    r, c = r - dc, c + dr

            total_cost += len(region) * sides

            seen |= region

    print(total_cost)


main()
