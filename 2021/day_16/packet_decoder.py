""" https://adventofcode.com/2021/day/16 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


class Solution:
    def __init__(self) -> None:
        self.bits: str = ""
        self.hex_bin_map = {
            "0": "0000",
            "1": "0001",
            "2": "0010",
            "3": "0011",
            "4": "0100",
            "5": "0101",
            "6": "0110",
            "7": "0111",
            "8": "1000",
            "9": "1001",
            "A": "1010",
            "B": "1011",
            "C": "1100",
            "D": "1101",
            "E": "1110",
            "F": "1111",
        }

    def parse_input(self) -> None:
        with open(get_file_path("input.txt")) as infile:
            hexstring = infile.readline().strip()

        self.bits = ""
        for char in hexstring:
            self.bits += self.hex_bin_map[char]

    def evaluate(self, type_id: int, operands: list[int]) -> int:
        if type_id == 0:
            return sum(operands)
        elif type_id == 1:
            prod = 1
            for val in operands:
                prod *= val
            return prod
        elif type_id == 2:
            return min(operands)
        elif type_id == 3:
            return max(operands)
        elif type_id == 5:
            return 1 if operands[0] > operands[1] else 0
        elif type_id == 6:
            return 1 if operands[0] < operands[1] else 0
        elif type_id == 7:
            return 1 if operands[0] == operands[1] else 0

    def operator_packet(self, bpos: int, type_id: int) -> tuple[int, int, int]:
        """
        Parse an operator packet recursively. Return a tuple containing
        new iterator position, sum of version numbers and result of the operation.
        """
        if len(self.bits) - bpos < 5:
            return len(self.bits), 0, 0
        version_sum = 0
        values = []
        if self.bits[bpos] == "0":
            bpos += 1
            # 15-bit => length of sub-packets
            length = int(self.bits[bpos : bpos + 15], 2)
            bpos += 15
            while length > 0:
                initial = bpos
                # version number
                version_sum += int(self.bits[bpos : bpos + 3], 2)
                bpos += 3
                # type id
                _type_id = int(self.bits[bpos : bpos + 3], 2)
                bpos += 3
                if _type_id == 4:
                    bpos, value = self.literal_packet(bpos)
                else:
                    bpos, versions, value = self.operator_packet(bpos, _type_id)
                    version_sum += versions
                values.append(value)
                length -= bpos - initial
        else:
            bpos += 1
            # 11-bit => number of sub-packets
            packet_count = int(self.bits[bpos : bpos + 11], 2)
            bpos += 11
            while packet_count > 0:
                # version number
                version_sum += int(self.bits[bpos : bpos + 3], 2)
                bpos += 3
                # type id
                _type_id = int(self.bits[bpos : bpos + 3], 2)
                bpos += 3
                if _type_id == 4:
                    bpos, value = self.literal_packet(bpos)
                else:
                    bpos, versions, value = self.operator_packet(bpos, _type_id)
                    version_sum += versions
                values.append(value)
                packet_count -= 1

        result = self.evaluate(type_id, values)
        return bpos, version_sum, result

    def literal_packet(self, bpos: int) -> tuple[int, int]:
        """
        Parse a literal packet and return a tuple containing the starting
        position of the next packet and the integer value of the current packet
        """
        value_binary = ""
        while self.bits[bpos] == "1":
            value_binary += self.bits[bpos + 1 : bpos + 5]
            bpos += 5
        value_binary += self.bits[bpos + 1 : bpos + 5]
        return bpos + 5, int(value_binary, 2)

    def part1(self) -> None:
        bpos = version_total = 0
        # version number
        version_total += int(self.bits[bpos : bpos + 3], 2)
        bpos += 3
        # type id
        type_id = int(self.bits[bpos : bpos + 3], 2)
        bpos += 3

        if type_id == 4:
            bpos, _ = self.literal_packet(bpos)
        else:
            bpos, versions, _ = self.operator_packet(bpos, type_id)
            version_total += versions

        print(version_total)

    def part2(self) -> None:
        bpos = 0
        # version number
        bpos += 3
        # type id
        type_id = int(self.bits[bpos : bpos + 3], 2)
        bpos += 3

        if type_id == 4:
            bpos, result = self.literal_packet(bpos)
        else:
            bpos, _, result = self.operator_packet(bpos, type_id)

        print(result)


if __name__ == "__main__":
    solution = Solution()
    solution.parse_input()
    solution.part1()
    solution.part2()
