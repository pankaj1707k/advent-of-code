""" https://adventofcode.com/2020/day/20 """

import math
import os
from functools import cached_property


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Tile:
    def __init__(self, tile_id: int, rows: list[str]) -> None:
        self.id = tile_id
        self.rows = rows

    def __eq__(self, __value: "Tile") -> bool:
        return self.id == __value.id

    def __hash__(self) -> int:
        return self.id

    @cached_property
    def edges(self) -> list[str]:
        # clockwise order
        return [
            self.rows[0],
            "".join(row[-1] for row in self.rows),
            self.rows[-1],
            "".join(row[0] for row in self.rows),
        ]

    @cached_property
    def all_edges(self) -> set[str]:
        return set(self.edges) | set(edge[::-1] for edge in self.edges)

    def shared_edges(self, tile: "Tile") -> set[str]:
        return self.all_edges & tile.all_edges

    def is_neighbor(self, tile: "Tile") -> bool:
        return bool(self != tile and self.shared_edges(tile))

    def rotate_edges_90(self, edges: list[str]) -> list[str]:
        return [edges[3][::-1], edges[0], edges[1][::-1], edges[2]]

    def flip_edges(self, edges: list[str]) -> list[str]:
        return [edges[0][::-1], edges[3], edges[2][::-1], edges[1]]


def part1() -> None:
    result = 1
    for tile in tiles:
        neighbors = [candidate for candidate in tiles if candidate.is_neighbor(tile)]
        if len(neighbors) == 2:
            result *= tile.id
    print(result)


def fill_corners_and_edges(
    image: list[list[Tile]], corner_tiles: list[Tile], edge_tiles: list[Tile]
) -> None:
    side_length = len(image)
    used_edge_tiles = set()

    # top left corner
    image[0][0] = corner_tiles[0]

    # top edge
    for col in range(1, side_length - 1):
        for tile in edge_tiles:
            if tile not in used_edge_tiles and tile.is_neighbor(image[0][col - 1]):
                # use the correct orientation
                pass


def part2() -> None:
    corners, edges, internals = [list() for _ in range(3)]
    for tile in tiles:
        neighbors = [candidate for candidate in tiles if candidate.is_neighbor(tile)]
        if len(neighbors) == 2:
            corners.append(tile)
        elif len(neighbors) == 3:
            edges.append(tile)
        else:
            internals.append(tile)

    side_length = round(math.sqrt(len(tiles)))
    image = [[Tile(0, [])] * side_length for _ in range(side_length)]
    fill_corners_and_edges(image, corners, edges)


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as fd:
        lines = fd.readlines()

    tiles: set[Tile] = set()
    SIZE = 10

    for index in range(0, len(lines), SIZE + 2):
        tile_id = int(lines[index].split()[1][:-1])
        tile_rows = [lines[index + delta].strip() for delta in range(1, SIZE + 1)]
        tiles.add(Tile(tile_id, tile_rows))

    # part1()
    # part2()
