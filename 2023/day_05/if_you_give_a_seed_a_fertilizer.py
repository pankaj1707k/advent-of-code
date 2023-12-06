""" https://adventofcode.com/2023/day/5 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def convert(source: int, conversion_map: list[tuple[int, int, int]]) -> int:
    for dest_start, src_start, length in conversion_map:
        src_end = src_start + length - 1
        if src_start <= source <= src_end:
            return dest_start + source - src_start
    return source


def part1() -> None:
    min_loc = 1 << 63

    for seed in seeds:
        value = seed
        for range_map in range_maps:
            value = convert(value, range_map)
        min_loc = min(min_loc, value)

    print(min_loc)


def part2() -> None:
    intervals = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]

    for range_map in range_maps:
        new_intervals = []

        while intervals:
            start, end = intervals.pop()
            for dst_start, src_start, length in range_map:
                overlap_start = max(start, src_start)
                overlap_end = min(end, src_start + length)
                if overlap_start < overlap_end:
                    new_intervals.append(
                        (
                            dst_start + overlap_start - src_start,
                            dst_start + overlap_end - src_start,
                        )
                    )
                    if start < overlap_start:
                        intervals.append((start, overlap_start))
                    if overlap_end < end:
                        intervals.append((overlap_end, end))
                    break
            else:
                new_intervals.append((start, end))

        intervals = new_intervals

    min_loc = min(interval[0] for interval in intervals)
    print(min_loc)


if __name__ == "__main__":
    seeds: list[int] = list()
    range_maps: list[list[tuple[int, int, int]]] = [[] for _ in range(7)]

    with open(get_file_path("input.txt")) as infile:
        seeds_line, *range_blocks = infile.read().split("\n\n")
        seeds = list(map(int, seeds_line.split()[1:]))
        for idx, block in enumerate(range_blocks):
            triplets = block.splitlines()[1:]
            for triplet in triplets:
                range_maps[idx].append(tuple(map(int, triplet.split())))

    part1()
    part2()
