""" https://adventofcode.com/2023/day/4 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> None:
    total_worth = 0

    for winning, have in cards.values():
        common_count = len(winning & have)
        total_worth += (1 << (common_count - 1)) if common_count else 0

    print(total_worth)


def part2() -> None:
    card_counter = {card_num: 1 for card_num in cards.keys()}

    for card_num in range(1, len(cards) + 1):
        winning, have = cards[card_num]
        common = len(winning & have)
        curr_card_freq = card_counter[card_num]
        for copy_card_num in range(card_num + 1, card_num + common + 1):
            card_counter[copy_card_num] += curr_card_freq

    total_cards = sum(card_counter.values())
    print(total_cards)


if __name__ == "__main__":
    cards: dict[int, tuple[set[int], set[int]]] = {}

    with open(get_file_path("input.txt")) as infile:
        for card in infile.readlines():
            header, desc = card.strip().split(": ")
            card_num = int(header.split()[1])
            winning, have = desc.split(" | ")
            winning = set(map(int, winning.split()))
            have = set(map(int, have.split()))
            cards[card_num] = (winning, have)

    part1()
    part2()
