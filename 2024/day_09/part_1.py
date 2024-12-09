""" https://adventofcode.com/2024/day/9 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def main():
    disk_map = ""

    with open(get_file_path("input.txt")) as fd:
        disk_map = fd.readline().rstrip()

    blocks: list[int] = []
    id = 0
    file = True
    for char in disk_map:
        count = int(char)
        if file:
            blocks.extend([id] * count)
            id += 1
        else:
            blocks.extend([-1] * count)
        file = not file

    front, rear = 0, len(blocks) - 1
    while front < rear:
        if blocks[front] == -1 and blocks[rear] != -1:
            blocks[front] = blocks[rear]
            blocks[rear] = -1
            front += 1
            rear -= 1
        elif blocks[front] == -1:
            rear -= 1
        else:
            front += 1

    checksum = sum(pos * id if id != -1 else 0 for pos, id in enumerate(blocks))
    print(checksum)


main()
