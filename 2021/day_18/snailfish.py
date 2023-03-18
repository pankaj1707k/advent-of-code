""" https://adventofcode.com/2021/day/18 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def explode(num: list) -> tuple[bool, list]:
    # convert to list of parts
    # each character the is an element and consecutive digits
    # are converted to integer and added as an element
    numstr = str(num).replace(" ", "")
    num_parts = []
    index = 0
    while index < len(numstr):
        if numstr[index] in {"[", ",", "]"}:
            num_parts.append(numstr[index])
            index += 1
        else:
            integer = ""
            while index < len(numstr) and numstr[index].isdigit():
                integer += numstr[index]
                index += 1
            num_parts.append(int(integer))

    depth = index = 0
    for index in range(len(num_parts)):
        if num_parts[index] == "[":
            depth += 1
            if depth == 5:
                left_num = num_parts[index + 1]
                right_num = num_parts[index + 3]  # (index + 2) => ','
                left_index = index - 1
                while left_index >= 0:
                    if isinstance(num_parts[left_index], int):
                        num_parts[left_index] += left_num
                        break
                    left_index -= 1
                right_index = index + 5
                while right_index < len(num_parts):
                    if isinstance(num_parts[right_index], int):
                        num_parts[right_index] += right_num
                        break
                    right_index += 1
                num_parts = num_parts[:index] + [0] + num_parts[index + 5 :]
                return True, eval("".join(map(str, num_parts)))
        elif num_parts[index] == "]":
            depth -= 1

    return False, num


def split(num: list | int) -> tuple[bool, list]:
    if isinstance(num, int):
        if num > 9:
            return True, [num >> 1, (num + 1) >> 1]
        return False, num
    did_split, left_split = split(num[0])
    if did_split:
        return True, [left_split, num[1]]
    did_split, right_split = split(num[1])
    return did_split, [left_split, right_split]


def reduce(num: list) -> list:
    exploded, after_explosion = explode(num)
    if exploded:
        return reduce(after_explosion)
    did_split, after_split = split(num)
    if did_split:
        return reduce(after_split)
    return num


def add(m: list, n: list) -> list:
    s = [m, n]
    return reduce(s)


def magnitude(num: list | int) -> int:
    if isinstance(num, int):
        return num
    return 3 * magnitude(num[0]) + 2 * magnitude(num[1])


def part1(nums: list) -> None:
    result = nums[0]
    for i in range(1, len(nums)):
        result = add(result, nums[i])

    print(magnitude(result))


def part2(nums: list) -> None:
    max_magnitude = 0
    for x in nums:
        for y in nums:
            if x != y:
                result = add(x, y)
                max_magnitude = max(max_magnitude, magnitude(result))

    print(max_magnitude)


def main() -> None:
    nums = []
    with open(get_file_path("input.txt")) as infile:
        for line in infile.readlines():
            nums.append(eval(line.strip()))

    part1(nums)
    part2(nums)


if __name__ == "__main__":
    main()
