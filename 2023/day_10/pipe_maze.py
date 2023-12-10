""" https://adventofcode.com/2023/day/10 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    steps = 0
    loop.add((srow, scol))
    pipes = pipe_ends[maze[srow][scol]](srow, scol)

    while not all(pipe in loop for pipe in pipes):
        steps += 1
        for pipe in pipes:
            loop.add(pipe)
        next_pipes = []
        for row, col in pipes:
            for nrow, ncol in pipe_ends[maze[row][col]](row, col):
                if (nrow, ncol) not in loop:
                    next_pipes.append((nrow, ncol))
        pipes = next_pipes

    print(steps)


def part2() -> None:
    pillars = {"FJ", "L7", "|"}
    enclosed_tiles = 0
    m, n = len(maze), len(maze[0])

    for row in range(m):
        parity = 0
        pillar = ""
        for col in range(n):
            if (row, col) not in loop:
                enclosed_tiles += parity
            else:
                if maze[row][col] in "FL":
                    pillar = maze[row][col]
                elif maze[row][col] in "J7|":
                    pillar += maze[row][col]
                    if pillar in pillars:
                        parity = 1 - parity
                    pillar = ""

    print(enclosed_tiles)


if __name__ == "__main__":
    pipe_ends = {
        "|": lambda r, c: [(r - 1, c), (r + 1, c)],
        "-": lambda r, c: [(r, c - 1), (r, c + 1)],
        "L": lambda r, c: [(r - 1, c), (r, c + 1)],
        "J": lambda r, c: [(r - 1, c), (r, c - 1)],
        "7": lambda r, c: [(r + 1, c), (r, c - 1)],
        "F": lambda r, c: [(r + 1, c), (r, c + 1)],
    }
    maze: list[list[str]] = list()
    loop: set[tuple[int, int]] = set()
    srow, scol = 0, 0

    with open(get_file_path("input.txt")) as infile:
        for ln, line in enumerate(infile.read().splitlines()):
            maze.append(list(line))
            if "S" in line:
                srow, scol = ln, line.index("S")

    if (
        srow > 0
        and srow < len(maze) - 1
        and maze[srow - 1][scol] in "7F|"
        and maze[srow + 1][scol] in "LJ|"
    ):
        # north - south
        maze[srow][scol] == "|"
    elif (
        scol > 0
        and scol < len(maze[0]) - 1
        and maze[srow][scol - 1] in "FL-"
        and maze[srow][scol + 1] in "7J-"
    ):
        # east - west
        maze[srow][scol] == "-"
    elif (
        srow > 0
        and scol < len(maze[0]) - 1
        and maze[srow - 1][scol] in "7F|"
        and maze[srow][scol + 1] in "7J-"
    ):
        # north - east
        maze[srow][scol] = "L"
    elif (
        srow > 0
        and scol > 0
        and maze[srow - 1][scol] in "7F|"
        and maze[srow][scol - 1] in "FL-"
    ):
        # north - west
        maze[srow][scol] = "J"
    elif (
        srow < len(maze) - 1
        and scol > 0
        and maze[srow + 1][scol] in "LJ|"
        and maze[srow][scol - 1] in "FL-"
    ):
        # south - west
        maze[srow][scol] = "7"
    elif (
        srow < len(maze) - 1
        and scol < len(maze[0]) - 1
        and maze[srow + 1][scol] in "LJ|"
        and maze[srow][scol + 1] in "7J-"
    ):
        # south - east
        maze[srow][scol] = "F"

    part1()
    part2()
