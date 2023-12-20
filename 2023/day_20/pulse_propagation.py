""" https://adventofcode.com/2023/day/20 """

import math
import os
from collections import deque
from copy import deepcopy


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Module:
    def __init__(self, name: str, type: str, dst_mods: list[str]) -> None:
        self.name = name
        self.type = type
        self.dst_mods = dst_mods
        self.state = 0 if type == "%" else {}


def part1() -> None:
    modules = deepcopy(modules_original)
    low = high = 0
    for _ in range(1000):
        low += 1
        que = deque([("broadcaster", dst, 0) for dst in broadcast])
        while que:
            src, dst, pulse = que.popleft()
            if pulse == 0:
                low += 1
            else:
                high += 1
            if dst not in modules:
                continue
            module = modules[dst]
            if module.type == "%":
                if pulse == 0:
                    module.state = 1 - module.state
                    que.extend([(dst, nxt, module.state) for nxt in module.dst_mods])
            else:
                module.state[src] = pulse
                npulse = 0 if all(module.state.values()) else 1
                que.extend([(dst, nxt, npulse) for nxt in module.dst_mods])

    print(low * high)


def part2() -> None:
    modules = deepcopy(modules_original)
    rx_input = "cs"
    # Modules which act as inputs to `rx_input`
    rx_subinputs = {}
    for name, module in modules.items():
        if rx_input in module.dst_mods:
            rx_subinputs[name] = False
    # For each input of the 'cs' module, store the min number of button
    # presses required to make the input module send a high pulse
    counts = {}
    button_press = 0

    while True:
        button_press += 1
        que = deque([("broadcaster", dst, 0) for dst in broadcast])
        all_covered = False

        while que:
            src, dst, pulse = que.popleft()
            if dst not in modules:
                continue
            module = modules[dst]

            if module.name == rx_input and pulse == 1:
                rx_subinputs[src] = True
                if src not in counts:
                    counts[src] = button_press
                if all(rx_subinputs.values()):
                    all_covered = True
                    break

            if module.type == "%":
                if pulse == 0:
                    module.state = 1 - module.state
                    que.extend([(dst, nxt, module.state) for nxt in module.dst_mods])
            else:
                module.state[src] = pulse
                npulse = 0 if all(module.state.values()) else 1
                que.extend([(dst, nxt, npulse) for nxt in module.dst_mods])

        if all_covered:
            break

    print(math.lcm(*counts.values()))


if __name__ == "__main__":
    modules_original: dict[str, Module] = {}
    broadcast: list[str] = list()

    with open(get_file_path("input.txt")) as infile:
        for line in infile.read().splitlines():
            src, dst = line.split(" -> ")
            if src == "broadcaster":
                broadcast = dst.split(", ")
            else:
                type, name = src[0], src[1:]
                modules_original[name] = Module(name, type, dst.split(", "))

    for name, module in modules_original.items():
        for nxt in module.dst_mods:
            if nxt in modules_original and modules_original[nxt].type == "&":
                modules_original[nxt].state[name] = 0

    part1()
    part2()
