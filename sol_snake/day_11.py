from typing import TextIO
from utils import parse_ints
import math


def apply_rules(stones):
    new_stones = []
    for i in stones:
        #print("New Iteration", new_stones, i)
        if i == 0:
            new_stones.append(1)
            continue

        number_of_digits = int(math.log10(i)+1)
        if number_of_digits % 2 == 0:
            divider =  (10**(number_of_digits//2))
            first_half = i // divider
            second_half = i % divider
            new_stones.append(first_half)
            new_stones.append(second_half)
        else:
            new_stones.append(i*2024)
    return new_stones

def day_11(content: TextIO, example: bool) -> tuple[int, int]:
    stones = parse_ints(content.readline())
    part_1_stones = stones[:]

    for _ in range(25):
        part_1_stones = apply_rules(part_1_stones)
    results_part_1 = len(part_1_stones)

    results_part_2 = 0

    return (results_part_1, 0)