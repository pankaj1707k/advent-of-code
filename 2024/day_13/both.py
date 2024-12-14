""" https://adventofcode.com/2024/day/13 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Machine:
    def __init__(
        self, a: tuple[int, int], b: tuple[int, int], p: tuple[int, int]
    ) -> None:
        self.a = a
        self.b = b
        self.p = p


def parse_button(text: str) -> tuple[int, int]:
    _, xy = text.split(": ")
    x, y = xy.split(", ")
    return (int(x[2:]), int(y[2:]))


def compute_tokens(machines: list[Machine], base_shift: int) -> int:
    total_tokens = 0
    for m in machines:
        at_num = m.b[0] * (m.p[1] + base_shift) - (m.p[0] + base_shift) * m.b[1]
        at_den = m.b[0] * m.a[1] - m.a[0] * m.b[1]
        if at_num % at_den != 0:
            continue
        at = at_num // at_den
        if at < 0:
            continue
        bt_num = (m.p[0] + base_shift) - at * m.a[0]
        if bt_num % m.b[0] != 0:
            continue
        bt = bt_num // m.b[0]
        if bt < 0:
            continue
        total_tokens += 3 * at + bt

    return total_tokens


def main():
    machines: list[Machine] = []

    with open(get_file_path("input.txt")) as fd:
        lines = fd.read().splitlines()
        for ln in range(0, len(lines), 4):
            button_a, button_b, prize = lines[ln : ln + 3]
            px, py = prize.split(", ")
            px = int(px[9:])
            py = int(py[2:])
            machines.append(
                Machine(parse_button(button_a), parse_button(button_b), (px, py))
            )

    print(compute_tokens(machines, 0))  # part 1
    print(compute_tokens(machines, 10000000000000))  # part 2


main()
