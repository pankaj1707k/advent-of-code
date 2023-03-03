""" https://adventofcode.com/2021/day/4 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Board:
    def __init__(self) -> None:
        self.grid: list[list[int]] = []
        # number of elements already "marked" in each row and column
        self.row_marked: list[int] = [0] * 5
        self.col_marked: list[int] = [0] * 5
        self.done: bool = False


class Solution:
    def __init__(self) -> None:
        self.sequence: list[int] = []
        self.boards: list[Board] = []

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            self.sequence = list(map(int, infile.readline().strip().split(",")))
            for line in infile.readlines():
                if line == "\n":
                    self.boards.append(Board())
                    continue
                self.boards[-1].grid.append(list(map(int, line.split())))

    def get_score(self, board: Board, num: int) -> int:
        unmarked_sum = sum(n for row in board.grid for n in row if n != -1)
        return unmarked_sum * num

    def part1(self) -> None:
        win = False
        win_board = None
        win_num = None
        for num in self.sequence:
            for board in self.boards:
                for row in range(5):
                    for col in range(5):
                        if board.grid[row][col] == num:
                            board.grid[row][col] = -1
                            board.row_marked[row] += 1
                            board.col_marked[col] += 1
                        if board.row_marked[row] == 5 or board.col_marked[col] == 5:
                            win = True
                            break
                    if win:
                        break
                if win:
                    win_board = board
                    break
            if win:
                win_num = num
                break

        print(self.get_score(win_board, win_num))

    def part2(self) -> None:
        win_count = 0
        last_board = None
        last_num = None
        for num in self.sequence:
            for board in self.boards:
                if board.done:
                    continue
                for row in range(5):
                    for col in range(5):
                        if board.grid[row][col] == num:
                            board.grid[row][col] = -1
                            board.row_marked[row] += 1
                            board.col_marked[col] += 1
                        if board.row_marked[row] == 5 or board.col_marked[col] == 5:
                            win_count += 1
                            board.done = True
                            break
                    if board.done:
                        break
                if win_count == len(self.boards):
                    last_board = board
                    break
            if win_count == len(self.boards):
                last_num = num
                break

        print(self.get_score(last_board, last_num))


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
