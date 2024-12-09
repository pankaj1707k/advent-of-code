""" https://adventofcode.com/2024/day/9 """

import os
from typing import Optional


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Node:
    def __init__(self, id: int, count: int) -> None:
        self.id: int = id
        self.count: int = count
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


def main():
    disk_map = ""

    with open(get_file_path("input.txt")) as fd:
        disk_map = fd.readline().rstrip()

    head = Node(-2, 0)
    tail = head
    id = 0
    file = True
    for char in disk_map:
        count = int(char)
        if count == 0:
            file = not file
            continue
        if file:
            tail.next = Node(id, count)
            tail.next.prev = tail
            id += 1
        else:
            tail.next = Node(-1, count)
            tail.next.prev = tail
        tail = tail.next
        file = not file

    moved: set[int] = set()
    rear = tail
    while rear != head:
        if rear.id == -1 or rear.id in moved:
            rear = rear.prev
            continue
        front = head.next
        while front != rear:
            if front.id == -1 and front.count >= rear.count:
                break
            front = front.next
        if front == rear:
            rear = rear.prev
            continue

        front.id = rear.id
        rem = front.count - rear.count
        front.count = rear.count
        rear.id = -1
        if rem == 0:
            rear = rear.prev
            continue

        new = Node(-1, rem)
        new.prev = front
        new.next = front.next
        front.next = new
        new.next.prev = new

        moved.add(rear.id)
        rear = rear.prev

    checksum = 0
    pos = 0
    curr = head.next
    while curr:
        if curr.id != -1:
            checksum += sum(p * curr.id for p in range(pos, pos + curr.count))
        pos += curr.count
        curr = curr.next

    print(checksum)


main()
