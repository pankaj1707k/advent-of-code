""" https://adventofcode.com/2023/day/7 """

import os
from collections import Counter


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Hand:
    def __init__(self, cards: str, bid: int) -> None:
        self.cards = cards
        self.bid = bid
        self.type = sorted(Counter(cards).values(), reverse=True)
        self.card_order = "23456789TJQKA"

    def __lt__(self, __other: "Hand") -> bool:
        if self.type < __other.type:
            return True
        if self.type > __other.type:
            return False
        for idx in range(5):
            if self.card_order.index(self.cards[idx]) < self.card_order.index(
                __other.cards[idx]
            ):
                return True
            if self.card_order.index(self.cards[idx]) > self.card_order.index(
                __other.cards[idx]
            ):
                return False
        return False

    def __repr__(self) -> str:
        return self.cards


class JokerHand(Hand):
    def __init__(self, cards: str, bid: int) -> None:
        super().__init__(cards, bid)
        self.card_order = "J23456789TQKA"

        joker_freq = cards.count("J")
        if 0 < joker_freq < 5:
            self.type.remove(joker_freq)
            self.type[0] += joker_freq


def part1() -> None:
    ranked_hands = sorted(hands)

    total_winnings = 0
    for rank, hand in enumerate(ranked_hands, 1):
        total_winnings += rank * hand.bid

    print(total_winnings)


def part2() -> None:
    joker_hands = [JokerHand(hand.cards, hand.bid) for hand in hands]
    ranked_hands = sorted(joker_hands)
    total_winnings = 0

    for rank, hand in enumerate(ranked_hands, 1):
        total_winnings += rank * hand.bid

    print(total_winnings)


if __name__ == "__main__":
    hands: list[Hand] = list()

    with open(get_file_path("input.txt")) as infile:
        for line in infile.read().splitlines():
            cards, bid = line.split()
            bid = int(bid)
            hands.append(Hand(cards, bid))

    part1()
    part2()
