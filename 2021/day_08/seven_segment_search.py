""" https://adventofcode.com/2021/day/8 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.puzzle_input: list[dict[str, list[str]]] = []
        self.digit_segments = {2: 1, 3: 7, 4: 4, 7: 8, 5: {2, 3, 5}, 6: {0, 6, 9}}
        self.singles = {2, 3, 4, 7}

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            for line in infile.readlines():
                uniques, output = line.strip().split(" | ")
                uniques = ["".join(sorted(p)) for p in uniques.split()]
                output = ["".join(sorted(p)) for p in output.split()]
                self.puzzle_input.append({"uniques": uniques, "output": output})

    def part1(self) -> None:
        singles_count = 0
        for output in [p["output"] for p in self.puzzle_input]:
            for pattern in output:
                if len(pattern) in self.singles:
                    singles_count += 1

        print(singles_count)

    def part2(self) -> None:
        output_total = 0
        for pattern in self.puzzle_input:
            uniques = pattern["uniques"]
            output = pattern["output"]
            decoded = {x: None for x in range(10)}
            # decode singles
            for p in uniques:
                if len(p) in self.singles:
                    decoded[self.digit_segments[len(p)]] = p

            # decode 6-length patterns
            six_length = [p for p in uniques if len(p) == 6]
            # identify pattern for 9
            for p in six_length:
                if set(decoded[4]).issubset(set(p)):
                    decoded[9] = p
                    break
            # identify pattern for 6 and 0
            for p in six_length:
                if p == decoded[9]:
                    continue
                if set(decoded[7]).issubset(set(p)):
                    decoded[0] = p
                else:
                    decoded[6] = p

            # decode 5-length patterns
            five_length = [p for p in uniques if len(p) == 5]
            # identify pattern for 5
            for p in five_length:
                if set(p).issubset(set(decoded[6])):
                    decoded[5] = p
                    break
            # identify pattern for 2 and 3
            for p in five_length:
                if len(set(p) & set(decoded[5])) == 3:
                    decoded[2] = p
                elif p != decoded[5]:
                    decoded[3] = p

            # find the output number
            num = 0
            for p in output:
                for digit in decoded:
                    if decoded[digit] == p:
                        num *= 10
                        num += digit
                        break

            output_total += num

        print(output_total)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
