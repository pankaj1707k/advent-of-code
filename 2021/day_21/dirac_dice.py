""" https://adventofcode.com/2021/day/21 """

import os
from collections import namedtuple
from functools import cache


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Player:
    def __init__(self) -> None:
        self.start_pos: int = None
        self.curr_pos: int = None
        self.score: int = 0


Pawn = namedtuple("Pawn", ["pos", "score"], defaults=[None, 0])


def part1(players: list[Player]) -> None:
    rolls = turn = 0
    die_num = 1
    while all(p.score < 1000 for p in players):
        roll_sum = (
            die_num
            + (die_num % 100 + 1)
            + (die_num + 2 if die_num < 99 else (die_num + 2) % 100)
        )
        players[turn].curr_pos = (players[turn].curr_pos + roll_sum) % 10
        players[turn].score += players[turn].curr_pos + 1
        rolls += 3
        turn = 1 - turn
        die_num = die_num + 3 if die_num < 98 else (die_num + 3) % 100

    # `turn` represents the index of the loser after the loop ends
    result = players[turn].score * rolls
    print(result)


@cache
def play(turn: int, player_1: Pawn, player_2: Pawn) -> tuple[int, int]:
    """
    Simulate all possibilities and return the win counts of both players
    """
    if player_1.score >= 21:
        return (1, 0)
    if player_2.score >= 21:
        return (0, 1)
    win_counts = (0, 0, 0)
    for x in {1, 2, 3}:
        for y in {1, 2, 3}:
            for z in {1, 2, 3}:
                die_sum = x + y + z
                if turn == 0:
                    new_pos = (player_1.pos + die_sum) % 10
                    new_player_1 = Pawn(pos=new_pos, score=player_1.score + new_pos + 1)
                    new_player_2 = Pawn(pos=player_2.pos, score=player_2.score)
                else:
                    new_pos = (player_2.pos + die_sum) % 10
                    new_player_2 = Pawn(pos=new_pos, score=player_2.score + new_pos + 1)
                    new_player_1 = Pawn(pos=player_1.pos, score=player_1.score)
                # produce universe for this possibility
                u_wins = play(1 - turn, new_player_1, new_player_2)
                win_counts = tuple(u_wins[i] + win_counts[i] for i in range(2))
    return win_counts


def part2(players: list[Player]) -> None:
    player_1 = Pawn(pos=players[0].start_pos, score=0)
    player_2 = Pawn(pos=players[1].start_pos, score=0)
    win_counts = play(0, player_1, player_2)
    print(max(win_counts))


def main() -> None:
    players = [Player(), Player()]

    with open(get_file_path("input.txt")) as infile:
        # make positions on track 0-based for modular arithmetic to work
        for i in range(2):
            players[i].start_pos = int(infile.readline().strip().split()[-1]) - 1
            players[i].curr_pos = players[i].start_pos

    part1(players)

    # reset player attributes
    for i in range(2):
        players[i].score = 0
        players[i].curr_pos = players[i].start_pos

    part2(players)


if __name__ == "__main__":
    main()
