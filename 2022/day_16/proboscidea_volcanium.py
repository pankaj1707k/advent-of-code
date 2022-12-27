""" https://adventofcode.com/2022/day/16 """

import os
from collections import deque
from functools import cache


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.tunnels = dict()
        self.valves = dict()
        self.distances = dict()
        self.nonzero_valves = list()
        self.valve_index = dict()

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                line = line.strip().split()
                curr_valve = line[1]
                rate = int(line[4][5:].rstrip(";"))
                neighbors = set(map(lambda s: s.rstrip(","), line[9:]))
                self.valves[curr_valve] = rate
                self.tunnels[curr_valve] = neighbors
                if rate != 0:
                    self.nonzero_valves.append(curr_valve)

        for index, valve in enumerate(self.nonzero_valves):
            self.valve_index[valve] = index

    def shortest_distances(self) -> None:
        for start in self.valves:
            # consider only valves with non-zero flow rate except "AA"
            # because it is the starting point
            if start != "AA" and self.valves[start] == 0:
                continue

            self.distances[start] = {start: 0, "AA": 0}

            # calculate distance from `start` to all nodes
            # with non-zero flow rates
            que = deque()
            que.append((start, 0))
            visited = set()
            visited.add(start)

            while que:
                valve, distance = que.popleft()
                for neighbor in self.tunnels[valve]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        # consider updating distance only if flow rate is non-zero
                        if self.valves[neighbor]:
                            self.distances[start][neighbor] = distance + 1
                        que.append((neighbor, distance + 1))

            del self.distances[start][start]
            if start != "AA":
                del self.distances[start]["AA"]

    @cache
    def dfs(self, valve: str, time_left: int, open_valves: int) -> int:
        # open_valves -> bitmask of ordered valves: bit 1 means valve is open
        max_pressure = 0
        for neighbor in self.distances[valve]:
            # lookup in distances instead of tunnels because
            # we only want neighbors with non-zero flow rates
            neighbor_mask = 1 << self.valve_index[neighbor]  # set neighbor as open
            if open_valves & neighbor_mask:  # neighbor is already open
                continue
            # deduct travel time
            reduced_time_left = time_left - self.distances[valve][neighbor]
            # deduct valve opening time
            reduced_time_left -= 1
            if reduced_time_left <= 0:  # can't reach or no time left after opening
                continue
            pressure_released = self.valves[neighbor] * reduced_time_left
            neighbor_open = open_valves | neighbor_mask
            pressure_released += self.dfs(neighbor, reduced_time_left, neighbor_open)
            # maximize pressure released
            max_pressure = max(max_pressure, pressure_released)

        return max_pressure

    def part1(self) -> None:
        max_pressure = self.dfs(valve="AA", time_left=30, open_valves=0)
        print(max_pressure)

    def part2(self) -> None:
        max_pressure = 0
        n = len(self.nonzero_valves)
        open_valve_states = (1 << n) - 1  # total number of masks for open_valves
        # for each partition of openable valves among human and elephant
        # find max pressure independently and add them together
        for open_valves in range(open_valve_states):
            max_pressure = max(
                max_pressure,
                self.dfs("AA", 26, open_valves)
                + self.dfs("AA", 26, open_valves ^ open_valve_states),
            )
        print(max_pressure)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.shortest_distances()
    solution.part1()
    solution.part2()
