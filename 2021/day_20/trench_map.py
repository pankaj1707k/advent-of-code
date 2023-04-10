""" https://adventofcode.com/2021/day/20 """

import os
from collections import deque


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def enhance_image(input_img: list[str], enhancer: str, bg: str) -> list[str]:
    # add extra rows and columns to accomodate for
    # addition of light pixels in darker region
    img = deque(input_img)
    img.extendleft([bg * len(img[0]) for _ in range(2)])
    img.extend([bg * len(img[0]) for _ in range(2)])
    for i in range(len(img)):
        img[i] = bg * 2 + img[i] + bg * 2

    # apply image enhancement
    output_img = [[bg for __ in range(len(img[0]))] for _ in range(len(img))]
    for i in range(1, len(img) - 1):
        for j in range(1, len(img[0]) - 1):
            encoded = ""
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    encoded += "0" if img[r][c] == "." else "1"
            index = int(encoded, 2)
            output_img[i][j] = enhancer[index]

    # convert to list of strings
    output_img = deque(["".join(row) for row in output_img])
    # truncate border containing all `bg` pixels
    while all(p == bg for p in output_img[0]):
        _ = output_img.popleft()
    while all(p == bg for p in output_img[-1]):
        _ = output_img.pop()
    while all(output_img[i][0] == bg for i in range(len(output_img))):
        for i in range(len(output_img)):
            output_img[i] = output_img[i][1:]
    while all(output_img[i][-1] == bg for i in range(len(output_img))):
        for i in range(len(output_img)):
            output_img[i] = output_img[i][:-1]

    return output_img


def count_light_pixels(img: list[str]) -> int:
    result = 0
    for row in img:
        for pixel in row:
            result += int(pixel == "#")
    return result


def part1(input_img: list[str], enhancer: str) -> None:
    if enhancer[0] == "#" and enhancer[-1] == ".":
        # background color is inverted after each enhancement
        output_img = enhance_image(input_img, enhancer, ".")
        output_img = enhance_image(output_img, enhancer, "#")
    else:
        output_img = enhance_image(input_img, enhancer, ".")
        output_img = enhance_image(output_img, enhancer, ".")

    print(count_light_pixels(output_img))


def part2(input_img: list[str], enhancer: str) -> None:
    img = input_img
    for i in range(50):
        if enhancer[0] == "#" and enhancer[-1] == ".":
            bg = "." if i & 1 == 0 else "#"
        else:
            bg = "."
        img = enhance_image(img, enhancer, bg)
    print(count_light_pixels(img))


def main() -> None:
    with open(get_file_path("input.txt")) as infile:
        lines = list(map(lambda l: l.strip(), infile.readlines()))

    enhancer = lines[0]
    image = lines[2:]

    part1(image, enhancer)
    part2(image, enhancer)


if __name__ == "__main__":
    main()
