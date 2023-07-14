""" https://adventofcode.com/2020/day/9 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1() -> int:
    window = set(nums[:25])
    for index in range(25, len(nums)):
        curr = nums[index]
        valid = False
        for prev in window:
            valid = valid or (curr - prev != prev and curr - prev in window)
        if not valid:
            print(curr)
            return curr
        window.remove(nums[index - 25])
        window.add(curr)


def part2(target: int) -> None:
    left = window_sum = 0
    for right in range(len(nums)):
        window_sum += nums[right]
        while left < right and window_sum > target:
            window_sum -= nums[left]
            left += 1
        if window_sum == target and left < right:
            window = nums[left : right + 1]
            print(max(window) + min(window))
            break


if __name__ == "__main__":
    with open(get_file_path("input.txt")) as fd:
        nums = [int(l.strip()) for l in fd.readlines()]

    invalid_num = part1()
    part2(invalid_num)
