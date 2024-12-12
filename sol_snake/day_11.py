from typing import TextIO, Generator
from utils import parse_ints
import math

# Made a generator because we have to tackle the splitting
def rules(stone: int) -> Generator[int]:
    if stone == 0:
        yield 1
        return # to prevent falling through

    number_of_digits = int(math.log10(stone)+1)
    if number_of_digits % 2 == 0:
        divider =  (10**(number_of_digits//2))
        yield stone // divider
        yield stone % divider
    else:
        yield stone * 2024

def apply_rules(stone_counts : dict[int,int]):
    # Using a list would be quite taxing, so instead,
    # use a dict with the counts being the number of elements of that number the list would contain
    results = dict()
    for stone,count in stone_counts.items():
        for new_stone in rules(stone):
            # e.g. if the previous "list" has "0" 24  times, then we'd need to put 1 24 times
            results[new_stone] = results.get(new_stone, 0) + count
    return results

def day_11(content: TextIO, example: bool) -> tuple[int, int]:
    stones = parse_ints(content.readline())

    part_1_blinks = 25
    part_1_counts = {i: 1 for i in stones}
    for _ in range(part_1_blinks):
        part_1_counts = apply_rules(part_1_counts)

    results_part_1 = sum(part_1_counts.values())

    part_2_blinks = 75
    # we can pick up where part 1 left off
    part_2_counts = part_1_counts.copy()
    for _ in range(part_2_blinks-part_1_blinks):
        part_2_counts = apply_rules(part_2_counts)

    results_part_2 = sum(part_2_counts.values())

    return (results_part_1, results_part_2)