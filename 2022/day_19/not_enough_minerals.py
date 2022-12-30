""" https://adventofcode.com/2022/day/19 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Cost:
    def __init__(self) -> None:
        self.ore: int = 0
        self.clay: int = 0
        self.obsidian: int = 0

    def __repr__(self) -> str:
        return str({"ore": self.ore, "clay": self.clay, "obsidian": self.obsidian})


class Blueprint:
    def __init__(self) -> None:
        self.ore = Cost()
        self.clay = Cost()
        self.obsidian = Cost()
        self.geode = Cost()

        self.useful = {}

    def set_useful(self) -> None:
        self.useful = {
            "ore": max(self.ore.ore, self.clay.ore, self.obsidian.ore, self.geode.ore),
            "clay": self.obsidian.clay,
            "obsidian": self.geode.obsidian,
        }

    def __repr__(self) -> str:
        return str(
            {
                "ore": self.ore,
                "clay": self.clay,
                "obsidian": self.obsidian,
                "geode": self.geode,
            }
        )


class Solution:
    def __init__(self) -> None:
        self.blueprints: dict[int, Blueprint] = {}

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            lines = [line.strip().split() for line in infile.readlines()]

        for line in lines:
            id = int(line[1].rstrip(":"))
            self.blueprints[id] = Blueprint()
            self.blueprints[id].ore.ore = int(line[6])
            self.blueprints[id].clay.ore = int(line[12])
            self.blueprints[id].obsidian.ore = int(line[18])
            self.blueprints[id].obsidian.clay = int(line[21])
            self.blueprints[id].geode.ore = int(line[27])
            self.blueprints[id].geode.obsidian = int(line[30])
            self.blueprints[id].set_useful()

    def dfs(
        self, blueprint: Blueprint, state: tuple[int, ...], cache: dict[tuple, int]
    ) -> int:
        ore, clay, obsidian, geode, orebot, claybot, obsbot, geobot, time = state

        if time == 0:
            return geode

        # discard extra minerals and robots
        # this allows more frequent repetition of states
        if orebot >= blueprint.useful["ore"]:
            orebot = blueprint.useful["ore"]
        if claybot >= blueprint.useful["clay"]:
            claybot = blueprint.useful["clay"]
        if obsbot >= blueprint.useful["obsidian"]:
            obsbot = blueprint.useful["obsidian"]

        # if the amount of mineral that will be collected at the end with the given
        # number of mineral bots and the amount already collected exceeds the max
        # expenditure of that mineral, then discard the extra amount by reducing
        # it in the current state
        if ore + orebot * (time - 1) >= blueprint.useful["ore"] * time:
            ore = blueprint.useful["ore"] * time - orebot * (time - 1)
        if clay + claybot * (time - 1) >= blueprint.useful["clay"] * time:
            clay = blueprint.useful["clay"] * time - claybot * (time - 1)
        if obsidian + obsbot * (time - 1) >= blueprint.useful["obsidian"] * time:
            obsidian = blueprint.useful["obsidian"] * time - obsbot * (time - 1)

        state = (ore, clay, obsidian, geode, orebot, claybot, obsbot, geobot, time)

        if state in cache:
            return cache[state]

        state_common = [
            ore + orebot,
            clay + claybot,
            obsidian + obsbot,
            geode + geobot,
            orebot,
            claybot,
            obsbot,
            geobot,
            time - 1,
        ]

        new_state = state_common.copy()
        max_geode = self.dfs(blueprint, tuple(new_state), cache)

        # orebot
        if ore >= blueprint.ore.ore:
            new_state = state_common.copy()
            new_state[0] -= blueprint.ore.ore
            new_state[4] += 1
            max_geode = max(max_geode, self.dfs(blueprint, tuple(new_state), cache))

        # claybot
        if ore >= blueprint.clay.ore:
            new_state = state_common.copy()
            new_state[0] -= blueprint.clay.ore
            new_state[5] += 1
            max_geode = max(max_geode, self.dfs(blueprint, tuple(new_state), cache))

        # obsidian bot
        if ore >= blueprint.obsidian.ore and clay >= blueprint.obsidian.clay:
            new_state = state_common.copy()
            new_state[0] -= blueprint.obsidian.ore
            new_state[1] -= blueprint.obsidian.clay
            new_state[6] += 1
            max_geode = max(max_geode, self.dfs(blueprint, tuple(new_state), cache))

        # geode bot
        if ore >= blueprint.geode.ore and obsidian >= blueprint.geode.obsidian:
            new_state = state_common.copy()
            new_state[0] -= blueprint.geode.ore
            new_state[2] -= blueprint.geode.obsidian
            new_state[7] += 1
            max_geode = max(max_geode, self.dfs(blueprint, tuple(new_state), cache))

        cache[state] = max_geode
        return max_geode

    def part1(self) -> None:
        total_quality = 0
        for id, bp in self.blueprints.items():
            init_state = (0, 0, 0, 0, 1, 0, 0, 0, 24)
            total_quality += id * self.dfs(bp, init_state, {})
        print(total_quality)

    def part2(self) -> None:
        product = 1
        for id in range(1, 4):
            init_state = (0, 0, 0, 0, 1, 0, 0, 0, 32)
            product *= self.dfs(self.blueprints[id], init_state, {})
        print(product)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()  # 1725
    solution.part2()  # 15510
