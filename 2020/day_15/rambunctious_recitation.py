""" https://adventofcode.com/2020/day/15 """


def num_spoken(target_turn: int) -> None:
    cache = {num: [t + 1] for t, num in enumerate(init_nums)}
    turn = len(init_nums) + 1
    prev_num = init_nums[-1]

    while True:
        if len(cache[prev_num]) == 1:
            curr_num = 0
        else:
            curr_num = cache[prev_num][1] - cache[prev_num][0]

        if turn == target_turn:
            break

        if curr_num not in cache:
            cache[curr_num] = [turn]
        elif len(cache[curr_num]) == 1:
            cache[curr_num].append(turn)
        else:
            cache[curr_num].pop(0)
            cache[curr_num].append(turn)

        prev_num = curr_num
        turn += 1

    print(curr_num)


if __name__ == "__main__":
    init_nums = [5, 1, 9, 18, 13, 8, 0]
    num_spoken(2020)
    num_spoken(30000000)
