""" https://adventofcode.com/2021/day/19 """

import os
from itertools import combinations

import numpy


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Point(tuple):
    def __add__(self, __x: "Point") -> "Point":
        return Point((self[0] + __x[0], self[1] + __x[1], self[2] + __x[2]))

    def __sub__(self, __x: "Point") -> "Point":
        return Point((self[0] - __x[0], self[1] - __x[1], self[2] - __x[2]))

    def __pow__(self, __x: int) -> "Point":
        return Point((self[0] ** __x, self[1] ** __x, self[2] ** __x))


class Scanner:
    def __init__(self, beacons: list[Point]) -> None:
        self.beacons: list[Point] = beacons
        self.location: Point = None
        self.rotation: numpy.ndarray = None
        self.beacon_distances: set[int] = set()
        self.dist_beacon_map: dict[int, tuple[Point, Point]] = {}

        self._set_beacon_distances()

    def _set_beacon_distances(self) -> None:
        for beacon1, beacon2 in combinations(self.beacons, 2):
            dist_sq = sum((beacon1 - beacon2) ** 2)
            self.beacon_distances.add(dist_sq)
            self.dist_beacon_map[dist_sq] = (beacon1, beacon2)


def overlapping_scanners(scanners: list[Scanner]) -> dict[tuple[int, int], list[int]]:
    """
    Iterate through all pairs of scanners and find the overlapping pairs having
    at least `PAIR_COMBINATIONS` common pairs of beacon distances. Return a dictionary
    of the form `{tuple_of_scanner_indices: list_of_common_beacon_distances}`.
    """
    result = {}
    for (i, sa), (j, sb) in combinations(enumerate(scanners), 2):
        common_distances = sa.beacon_distances & sb.beacon_distances
        if len(common_distances) >= PAIR_COMBINATIONS:
            result[(i, j)] = list(common_distances)
    return result


def get_scanner_location(
    beacon_pair1: tuple[Point, Point], beacon_pair2: tuple[Point, Point]
) -> Point | None:
    """
    Return the location of a scanner.
    `beacon_pair1`: Pair of beacons belonging to scanner 1
    `beacon_pair2`: Pair of beacons belonging to scanner 2
    Both the beacon pairs have the same euclidean distance, i.e.,
    they belong to the overlapping region of the two scanners.
    This function figures out which beacon belongs to which end of the line.
    """
    pos1 = beacon_pair1[0] - beacon_pair2[0]
    pos2 = beacon_pair1[1] - beacon_pair2[1]
    if pos1 == pos2:
        return pos1

    pos1 = beacon_pair1[0] - beacon_pair2[1]
    pos2 = beacon_pair1[1] - beacon_pair2[0]
    if pos1 == pos2:
        return pos1

    return None


def get_all_beacons(scanners: list[Scanner]) -> list[Point]:
    """
    Return locations for all beacons in the given space relative to the first scanner.
    """
    overlaps = overlapping_scanners(scanners)
    all_beacons = set(scanners[0].beacons)
    scanners_processed = 1

    while scanners_processed < len(scanners):
        for (i, j), common_distances in overlaps.items():
            # "exactly" one of the scanners must be processed already
            if not ((scanners[i].location == None) ^ (scanners[j].location == None)):
                continue

            # make sure `scanner[i]` is the reference scanner (already processed)
            if scanners[i].location is None:
                i, j = j, i

            # take out one pair of beacons each from both scanners to compute
            # the position of `scanner[j]` relative to `scanner[i]`.
            beacon_pair1 = scanners[i].dist_beacon_map[common_distances[0]]
            beacon_pair2 = scanners[j].dist_beacon_map[common_distances[0]]

            pair1_rotated = (
                Point(numpy.matmul(scanners[i].rotation, numpy.array(beacon_pair1[0]))),
                Point(numpy.matmul(scanners[i].rotation, numpy.array(beacon_pair1[1]))),
            )

            for rotation in ROTATIONS:
                pair2_rotated = (
                    Point(numpy.matmul(rotation, numpy.array(beacon_pair2[0]))),
                    Point(numpy.matmul(rotation, numpy.array(beacon_pair2[1]))),
                )
                location = get_scanner_location(pair1_rotated, pair2_rotated)

                if location:
                    # found the correct orientation for `scanners[j]`
                    # perform translation using already computed location
                    # of `scanners[i]`
                    location += scanners[i].location
                    scanners[j].location = location
                    scanners[j].rotation = rotation

                    # apply the same rotation and translation on every beacon
                    # of `scanners[j]` and insert into `all_beacons`
                    for beacon in scanners[j].beacons:
                        beacon = Point(numpy.matmul(rotation, numpy.array(beacon)))
                        beacon += location
                        all_beacons.add(beacon)

                    scanners_processed += 1
                    break

    return all_beacons


def manhattan_distance(x: Point, y: Point) -> int:
    return sum(map(abs, x - y))


def part1(scanners: list[Scanner]) -> None:
    beacon_count = len(get_all_beacons(scanners))
    print(beacon_count)


def part2(scanners: list[Scanner]) -> None:
    max_distance = max(
        manhattan_distance(s.location, r.location) for s in scanners for r in scanners
    )
    print(max_distance)


def main() -> None:
    scanners: list[Scanner] = []
    with open(get_file_path("input.txt")) as infile:
        lines = infile.readlines()

    scanner_beacons = []
    for line in lines:
        line = line.strip()
        if line.startswith("---"):
            continue
        if not line:
            scanners.append(Scanner(scanner_beacons))
            scanner_beacons = []
            continue
        scanner_beacons.append(Point(map(int, line.split(","))))
    scanners.append(Scanner(scanner_beacons))

    scanners[0].location = Point((0, 0, 0))
    scanners[0].rotation = ROTATIONS[0]

    part1(scanners)
    part2(scanners)


if __name__ == "__main__":
    MIN_OVERLAPS = 12
    PAIR_COMBINATIONS = MIN_OVERLAPS * (MIN_OVERLAPS - 1) // 2

    ROTATIONS = [
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
        [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
        [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
        [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
        [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
        [[0, 1, 0], [1, 0, 0], [0, 0, -1]],
        [[0, 0, -1], [1, 0, 0], [0, -1, 0]],
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
        [[-1, 0, 0], [0, 0, -1], [0, -1, 0]],
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
        [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],
        [[0, 1, 0], [-1, 0, 0], [0, 0, 1]],
        [[0, 0, 1], [-1, 0, 0], [0, -1, 0]],
        [[0, -1, 0], [-1, 0, 0], [0, 0, -1]],
        [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],
        [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
        [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
        [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
        [[0, -1, 0], [0, 0, -1], [1, 0, 0]],
        [[0, 0, -1], [0, -1, 0], [-1, 0, 0]],
        [[0, -1, 0], [0, 0, 1], [-1, 0, 0]],
        [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
        [[0, 1, 0], [0, 0, -1], [-1, 0, 0]],
    ]
    ROTATIONS = list(map(numpy.array, ROTATIONS))

    main()
