""" https://adventofcode.com/2020/day/3 """

import os


def get_file_path(filename: str) -> str:
    dir_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(dir_path, filename)


def part1(batch_file: list[str]) -> None:
    mandatory = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    index = valid_count = 0

    while index < len(batch_file):
        passport = ""
        # combine all password info into a single string
        while index < len(batch_file) and batch_file[index] != "":
            passport += batch_file[index] + " "
            index += 1
        # check passport validity
        valid = True
        for field in mandatory:
            if field not in passport:
                valid = False
                break
        valid_count += int(valid)
        index += 1

    print(valid_count)


def part2(batch_file: list[str]) -> None:
    mandatory_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    ecl_values = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
    index = valid_count = 0

    while index < len(batch_file):
        info = []
        while index < len(batch_file) and batch_file[index] != "":
            info.extend(batch_file[index].split())
            index += 1

        valid = True
        # check if all mandatory fields are present
        info_str = " ".join(info)
        for field_name in mandatory_fields:
            valid = valid and field_name in info_str

        if not valid:
            index += 1
            continue

        # check if fields have correct data
        for field in info:
            field_name, value = field.split(":")
            if field_name == "byr":
                valid = valid and 1920 <= int(value) <= 2002
            elif field_name == "iyr":
                valid = valid and 2010 <= int(value) <= 2020
            elif field_name == "eyr":
                valid = valid and 2020 <= int(value) <= 2030
            elif field_name == "hgt":
                height, unit = value[:-2], value[-2:]
                valid = (
                    valid
                    and height.isdigit()
                    and (
                        (unit == "cm" and 150 <= int(height) <= 193)
                        or (unit == "in" and 59 <= int(height) <= 76)
                    )
                )
            elif field_name == "hcl":
                valid = (
                    valid
                    and len(value) == 7
                    and value[0] == "#"
                    and all(char.isdigit() or char in "abcdef" for char in value[1:])
                )
            elif field_name == "ecl":
                valid = valid and value in ecl_values
            elif field_name == "pid":
                valid = valid and len(value) == 9 and value.isdigit()

        valid_count += int(valid)
        index += 1

    print(valid_count)


def main() -> None:
    with open(get_file_path("input.txt")) as fd:
        lines = [line.strip() for line in fd.readlines()]

    part1(lines)
    part2(lines)


if __name__ == "__main__":
    main()
