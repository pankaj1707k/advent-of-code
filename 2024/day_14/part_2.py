""" https://adventofcode.com/2024/day/14 """

from collections import deque
import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


X = 101
Y = 103


def get_final_positions(
    robots: list[tuple[int, ...]], time: int
) -> set[tuple[int, int]]:
    final = set()
    for x, y, vx, vy in robots:
        nx = (x + ((time % X) * (vx % X)) % X + X) % X
        ny = (y + ((time % Y) * (vy % Y)) % Y + Y) % Y
        final.add((nx, ny))
    return final


def is_tree_possible(positions: set[tuple[int, int]]) -> bool:
    global_seen = set()
    for p in positions:
        if p in global_seen:
            continue
        que = deque([p])
        seen = set()
        while que:
            x, y = que.popleft()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in positions:
                    que.append((nx, ny))
        # a sufficiently large region is found by floodfill
        # could form a tree
        if len(seen) > 50:
            return True
        global_seen |= seen
    return False


def main():
    robots = []

    with open(get_file_path("input.txt")) as fd:
        for line in fd.read().splitlines():
            pos, vel = line.split(" ")
            robots.append(eval(pos[2:]) + eval(vel[2:]))

    for t in range(1, 10000):
        final = get_final_positions(robots, t)
        if is_tree_possible(final):
            with open(get_file_path(f"{t}.txt"), "w") as out:
                for i in range(Y):
                    for j in range(X):
                        if (i, j) in final:
                            out.write("#")
                        else:
                            out.write(".")
                    out.write("\n")
            break


main()
