""" https://adventofcode.com/2020/day/5 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def decode(boarding_pass: str) -> tuple[int, int, int]:
    """Decode the boarding pass and return its row, column and seat id"""

    # first 7 characters are for rows
    low, high = 0, 127
    for i in range(7):
        mid = (low + high) >> 1
        if boarding_pass[i] == "F":
            high = mid
        else:
            low = mid + 1

    row = high

    # last 3 characters are for columns
    low, high = 0, 7
    for i in range(7, 10):
        mid = (low + high) >> 1
        if boarding_pass[i] == "L":
            high = mid
        else:
            low = mid + 1

    col = high
    seat_id = row * 8 + col
    return row, col, seat_id


def part1(boarding_passes: list[str]) -> None:
    max_seat_id = 0
    for boarding_pass in boarding_passes:
        _, _, seat_id = decode(boarding_pass)
        max_seat_id = max(max_seat_id, seat_id)
    print(max_seat_id)


def part2(boarding_passes: list[str]) -> None:
    seat_ids = set()

    for boarding_pass in boarding_passes:
        _, _, seat_id = decode(boarding_pass)
        seat_ids.add(seat_id)

    for row in range(128):
        for col in range(8):
            seat_id = row * 8 + col
            if row == 0 or row == 127:
                continue
            if (
                seat_id not in seat_ids
                and seat_id + 1 in seat_ids
                and seat_id - 1 in seat_ids
            ):
                print(seat_id)


def main() -> None:
    with open(get_file_path("input.txt")) as fd:
        lines = [line.strip() for line in fd.readlines()]

    part1(lines)
    part2(lines)


if __name__ == "__main__":
    main()
