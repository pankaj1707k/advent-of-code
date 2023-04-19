""" https://adventofcode.com/2021/day/23 """

import math
import os
from collections import defaultdict, deque
from copy import deepcopy
from queue import PriorityQueue


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


AMPHIPODS = {"A": 0, "B": 1, "C": 2, "D": 3}
ENTRANCE = (2, 4, 6, 8)
ENERGY = (1, 10, 100, 1000)


class State:
    def __init__(self) -> None:
        self.hallway: list[int | None] = [None] * 11
        self.rooms: list[list[int | None]] = [[None] * 2 for _ in range(4)]

    def __eq__(self, other: "State") -> bool:
        return self.hallway == other.hallway and self.rooms == other.rooms

    def __lt__(self, other: "State") -> bool:
        return hash(self) < hash(other)

    def __lte__(self, other: "State") -> bool:
        return hash(self) <= hash(other)

    def __hash__(self) -> int:
        # Encode the state in a 57-bit integer
        # Each cell occupies exactly 3 bits
        hash_value = bit_counter = 0

        for x in self.hallway:
            hash_value |= 7 if x == None else (x << bit_counter)
            bit_counter += 3

        for room in self.rooms:
            for value in room:
                hash_value |= 7 if value == None else (value << bit_counter)
                bit_counter += 3

        return hash_value

    def __str__(self) -> str:
        _s = [
            "#" * 13,
            "#" + "".join("." if not h else str(h) for h in self.hallway) + "#",
            "###" + "#".join(map(str, [r for r, _ in self.rooms])) + "###",
            "  #" + "#".join(map(str, [r for _, r in self.rooms])) + "#",
            "  " + "#" * 9,
        ]
        return "\n".join(_s)

    def __repr__(self) -> str:
        return self.__str__()

    def _get_empty_pos(self, pos: int) -> list[int]:
        """
        Return empty positions in the hallway that can be visited
        from `pos` (room entrance). The list does not include positions
        that form a room entrance.
        """
        empty_pos = deque()
        _p = pos - 1
        # move as far left as possible until a non-empty cell
        # or end of hallway is encountered
        while _p >= 0 and self.hallway[_p] == None:
            if _p not in ENTRANCE:
                empty_pos.appendleft(_p)
            _p -= 1
        _p = pos + 1
        # move as far right as possible
        while _p < len(self.hallway) and self.hallway[_p] == None:
            if _p not in ENTRANCE:
                empty_pos.append(_p)
            _p += 1
        return list(empty_pos)

    def _can_enter_room(self, room_index: int) -> bool:
        """Check if room can be entered by its host amphipod"""
        room = self.rooms[room_index]
        return all(amphipod in {None, room_index} for amphipod in room)

    def _is_room_exitable(self, room_index: int) -> bool:
        """Check if there is any amphipod that does not belong to the room"""
        return not self._can_enter_room(room_index)

    def _get_bottom_most(self, room_index: int) -> int:
        """Return the bottom most empty slot in the room"""
        pos = 0
        room = self.rooms[room_index]
        while pos < len(room) and room[pos] == None:
            pos += 1
        return pos - 1

    def _first_amphipod_in_room(self, room_index: int) -> tuple[int, int]:
        """Return the first amphipod and its depth in the room"""
        room = self.rooms[room_index]
        for depth, amphipod in enumerate(room):
            if amphipod != None:
                return (amphipod, depth)

    def _is_hallway_clear(self, curr_pos: int, target_pos: int) -> bool:
        """Check if phallway is clear from `curr_pos` to `target_pos`"""
        left, right = (
            (curr_pos, target_pos) if curr_pos < target_pos else (target_pos, curr_pos)
        )
        return all(x == None for x in self.hallway[left + 1 : right])

    def get_neighbors(self) -> list[tuple["State", int]]:
        """
        Return neighboring states coupled with the energy cost of the movements.
        """
        neighbors = []

        # generate states by considering movement from room to hallway
        for room_index, _ in enumerate(self.rooms):
            if not self._is_room_exitable(room_index):
                continue
            amphipod, depth = self._first_amphipod_in_room(room_index)
            for target_pos in self._get_empty_pos(ENTRANCE[room_index]):
                new_config = deepcopy(self)
                new_config.hallway[target_pos] = amphipod
                new_config.rooms[room_index][depth] = None
                steps = depth + 1 + abs(target_pos - ENTRANCE[room_index])
                energy_used = steps * ENERGY[amphipod]
                neighbors.append((new_config, energy_used))

        # generate states by considering movement from hallway to room
        for pos, amphipod in enumerate(self.hallway):
            if (
                amphipod == None
                or not self._can_enter_room(amphipod)
                or not self._is_hallway_clear(pos, ENTRANCE[amphipod])
            ):
                continue
            # target depth of amphipod in its room
            depth = self._get_bottom_most(amphipod)
            new_config = deepcopy(self)
            new_config.hallway[pos] = None
            new_config.rooms[amphipod][depth] = amphipod
            steps = depth + 1 + abs(pos - ENTRANCE[amphipod])
            energy_used = steps * ENERGY[amphipod]
            neighbors.append((new_config, energy_used))

        return neighbors

    def h_score(self) -> int:
        """
        Heuristic function for the A* search algorithm.

        Return the heuristic score of the current state as the sum of:
        - Moving each amphipod from its current room to its target room.
        - Moving an amphipod (which is already in its target room) into
          the hallway and back to the room.
        """
        cost = 0
        # Add costs of every amphipod into its target room. Use the top most slot
        # in the target room because we only require a rough estimate of the cost
        # such that the heuristic is admissible.
        for room_index, room in enumerate(self.rooms):
            for depth, amphipod in enumerate(room):
                if amphipod == room_index:
                    # Already in the target room. However, it may still need to move
                    # to allow other amphipods to exit the room.
                    if any(
                        room[d] != None and room[d] != amphipod
                        for d in range(depth + 1, len(room))
                    ):
                        # (depth + 1) steps to move into the hallway and 2 steps to
                        # move back in the room (top most slot)
                        cost += (depth + 4) * ENERGY[amphipod]
                elif amphipod != None:
                    steps = depth + abs(ENTRANCE[room_index] - ENTRANCE[amphipod]) + 2
                    cost += steps * ENERGY[amphipod]

        return cost


def search_Astar(init_state: State, goal_state: State) -> int:
    """
    Search the most optimal path using A-star algorithm.
    Return the least cost of reaching the `goal_state` from `init_state`.
    """
    # nodes that are open for exploration: (fscore, state)
    open_nodes = PriorityQueue()
    open_nodes.put((init_state.h_score(), init_state))
    # g_score[s]: lowest cost recorded so far to reach `s` from `init_state`
    g_score = defaultdict(lambda: math.inf)
    g_score[init_state] = 0
    # f_score[s] = g_score[s] + s.h_score()
    f_score = defaultdict(lambda: math.inf)
    f_score[init_state] = init_state.h_score()

    while open_nodes:
        _, curr_state = open_nodes.get()
        if curr_state == goal_state:
            return g_score[curr_state]
        for next_state, transition_energy in curr_state.get_neighbors():
            tentative_g_score = g_score[curr_state] + transition_energy
            if tentative_g_score < g_score[next_state]:
                # lower cost path is found
                g_score[next_state] = tentative_g_score
                f_score[next_state] = tentative_g_score + next_state.h_score()
                open_nodes.put((f_score[next_state], next_state))


# Slower than A* search
def search_dikjstra(init_state: State, goal_state: State) -> int:
    """
    Search the most optimal path using Dijkstra's shortest path algorithm.
    Return the least cost of reaching the `goal_state` from `init_state`.
    """
    energy_cost = defaultdict(lambda: math.inf)
    energy_cost[init_state] = 0
    visited = set()
    pq = PriorityQueue()
    pq.put((0, init_state))

    while not pq.empty():
        cost, curr_state = pq.get()
        if curr_state in visited:
            continue
        visited.add(curr_state)
        for next_state, transition_energy in curr_state.get_neighbors():
            if cost + transition_energy < energy_cost[next_state]:
                energy_cost[next_state] = cost + transition_energy
                pq.put((energy_cost[next_state], next_state))

    return energy_cost[goal_state]


def part1(init_state: State, goal_state: State) -> None:
    least_energy = search_Astar(init_state, goal_state)
    print(least_energy)


def part2(init_state: State, goal_state: State) -> None:
    # update `init_state` to include two additional rows provided (DD, CB, BA, AC)
    additional_rows = [[3, 3], [2, 1], [1, 0], [0, 2]]
    for room_index, room in enumerate(init_state.rooms):
        init_state.rooms[room_index] = (
            [room[0]] + additional_rows[room_index] + [room[1]]
        )

    # update `goal_state`
    for room_index, room in enumerate(goal_state.rooms):
        goal_state.rooms[room_index] = room * 2

    least_energy = search_Astar(init_state, goal_state)
    print(least_energy)


def main() -> None:
    with open(get_file_path("input.txt")) as infile:
        lines = list(map(lambda l: l.strip(), infile.readlines()))

    cell_0 = lines[2].strip("#").split("#")
    cell_1 = lines[3].strip().strip("#").split("#")
    init_state = State()

    for i in range(4):
        init_state.rooms[i][0] = AMPHIPODS[cell_0[i]]
        init_state.rooms[i][1] = AMPHIPODS[cell_1[i]]

    goal_state = State()
    for i in range(4):
        goal_state.rooms[i] = [i, i]

    part1(init_state, goal_state)
    part2(init_state, goal_state)


if __name__ == "__main__":
    main()
