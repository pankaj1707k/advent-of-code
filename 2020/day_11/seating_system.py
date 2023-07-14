""" https://adventofcode.com/2020/day/11 """

import os
from typing import Callable


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def is_valid(row: int, col: int) -> bool:
    return row >= 0 and col >= 0 and row < M and col < N


def can_occupy(row: int, col: int, state: list[list[int]]) -> bool:
    """
    Check if `state[row][col]` can be occupied
    """
    return state[row][col] == 0 and all(
        state[row + dr][col + dc] in {-1, 0}
        for dr, dc in DIRS
        if is_valid(row + dr, col + dc)
    )


def can_occupy_ext(row: int, col: int, state: list[list[int]]) -> bool:
    """
    Check if `state[row][col]` can be occupied with extended visibility
    """
    if state[row][col] != 0:
        return False
    status = True
    for dr, dc in DIRS:
        nr, nc = row + dr, col + dc
        while is_valid(nr, nc) and state[nr][nc] == -1:
            nr += dr
            nc += dc
        if is_valid(nr, nc):
            status = status and state[nr][nc] == 0
    return status


def must_leave(row: int, col: int, state: list[list[int]]) -> bool:
    """
    Check if `state[row][col]` needs to be emptied
    """
    return (
        state[row][col] == 1
        and sum(
            int(state[row + dr][col + dc] == 1)
            for dr, dc in DIRS
            if is_valid(row + dr, col + dc)
        )
        >= 4
    )


def must_leave_ext(row: int, col: int, state: list[list[int]]) -> bool:
    """
    Check if `state[row][col]` needs to be emptied, with extended visibility
    """
    if state[row][col] != 1:
        return False
    occupied = 0
    for dr, dc in DIRS:
        nr, nc = row + dr, col + dc
        while is_valid(nr, nc) and state[nr][nc] == -1:
            nr += dr
            nc += dc
        if is_valid(nr, nc):
            occupied += state[nr][nc]
    return occupied >= 5


def solve(empty_rule: Callable, occupied_rule: Callable) -> int:
    """
    Generic solver for both parts of the problem.
    `empty_rule` refers to a function to check the rule for an empty seat.
    `occupied_rule` refers to a function to check the rule for an occupied seat.
    """
    curr_state = grid

    while True:
        next_state = [[curr_state[i][j] for j in range(N)] for i in range(M)]
        changed = False

        for i in range(M):
            for j in range(N):
                if empty_rule(i, j, curr_state):
                    next_state[i][j] = 1
                    changed = True
                elif occupied_rule(i, j, curr_state):
                    next_state[i][j] = 0
                    changed = True

        curr_state = next_state
        if not changed:
            break

    occupied = 0

    for i in range(M):
        for j in range(N):
            occupied += int(curr_state[i][j] == 1)

    return occupied


def part1() -> None:
    result = solve(can_occupy, must_leave)
    print(result)


def part2() -> None:
    result = solve(can_occupy_ext, must_leave_ext)
    print(result)


if __name__ == "__main__":
    # encode the state with integer grid
    # floor (.) = -1; empty seat (L) = 0; occupied seat (#) = 1
    # initial state does not have any occupied seat
    encoder = lambda char: -1 if char == "." else 0

    # directions
    DIRS = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

    with open(get_file_path("input.txt")) as fd:
        grid = [list(map(encoder, line.strip())) for line in fd.readlines()]

    # grid dimensions
    M, N = len(grid), len(grid[0])

    part1()
    part2()
