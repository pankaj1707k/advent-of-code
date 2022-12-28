""" https://adventofcode.com/2022/day/18 """

import os
from collections import defaultdict, deque


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.graph = defaultdict(set)
        self.cubes = set()

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                position = tuple(map(int, line.split(",")))
                self.cubes.add(position)

        for cube in self.cubes:
            for neighbor in self.cubes:
                if (
                    (
                        cube[0] == neighbor[0]
                        and cube[1] == neighbor[1]
                        and abs(cube[2] - neighbor[2]) == 1
                    )
                    or (
                        cube[0] == neighbor[0]
                        and cube[2] == neighbor[2]
                        and abs(cube[1] - neighbor[1]) == 1
                    )
                    or (
                        cube[2] == neighbor[2]
                        and cube[1] == neighbor[1]
                        and abs(cube[0] - neighbor[0]) == 1
                    )
                ):
                    self.graph[cube].add(neighbor)

    def part1(self) -> None:
        surface_area = 0
        for cube in self.cubes:
            surface_area += 6 - len(self.graph[cube])
        print(surface_area)

    def part2(self) -> None:
        # find lower and upper bounds of x, y, z coordinates
        lowers = [100] * 3
        uppers = [0] * 3
        for cube in self.cubes:
            for i in range(3):
                lowers[i] = min(lowers[i], cube[i])
                uppers[i] = max(uppers[i], cube[i])

        for i in range(3):
            lowers[i] -= 1
            uppers[i] += 1

        # assuming the given coordinates correspond to the center of the cube applying
        # the following shifts represent the coordinates of the center of each face
        shifts = [
            (0, 0, 0.5),
            (0, 0.5, 0),
            (0.5, 0, 0),
            (0, 0, -0.5),
            (0, -0.5, 0),
            (-0.5, 0, 0),
        ]
        # set of coordinates of the faces
        faces = set()

        # coordinate set for all faces
        for x, y, z in self.cubes:
            for dx, dy, dz in shifts:
                faces.add((x + dx, y + dy, z + dz))

        exposed = set()
        exposed.add((lowers[0], lowers[1], lowers[2]))
        que = deque()
        que.append((lowers[0], lowers[1], lowers[2]))

        # BFS over all integer coordinates in the 3d grid
        # bounded by `lowers` and `uppers` for each component
        while que:
            x, y, z = que.popleft()
            for dx, dy, dz in shifts:
                newx, newy, newz = (
                    round(x + 2 * dx),
                    round(y + 2 * dy),
                    round(z + 2 * dz),
                )
                newpos = (newx, newy, newz)
                if not (
                    lowers[0] <= newx <= uppers[0]
                    and lowers[1] <= newy <= uppers[1]
                    and lowers[2] <= newz <= uppers[2]
                ):
                    continue
                if newpos in self.cubes or newpos in exposed:
                    continue
                exposed.add(newpos)
                que.append(newpos)

        # set of coordinates for faces that are exposed
        open_faces = set()
        for x, y, z in exposed:
            for dx, dy, dz in shifts:
                open_faces.add((x + dx, y + dy, z + dz))

        # intersection with `faces` ensures that faces that do not belong
        # to an actual cube are not considered for the surface area
        outer_surface_area = len(faces & open_faces)
        print(outer_surface_area)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
