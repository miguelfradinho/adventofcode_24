from typing import TextIO
import itertools
from collections import deque
import time

# test_value, operator_places, numbers
type Equation = tuple[int, int, list[int]]

def do_operation(op: str, first: int, second: int) -> int:
    match op:
        case "+":
            return first + second
        case "*":
            return first * second
        case "||":
            return int(f"{first}{second}")
        case _:
            raise ValueError("Wrong operator!")

def can_be_solved(x: int, operators_combinations: list[tuple[str, ...]], numbers: list[int]) -> bool:
    for ops in operators_combinations:
        numbers_left = deque(numbers)
        ops_left = deque(ops)
        while len(numbers_left) > 1 and len(ops_left) > 0:
            first = numbers_left.popleft()
            second = numbers_left.popleft()
            operator = ops_left.popleft()

            # cachng the operation result would add enough overhead to make it 10-20 secs slower
            result = do_operation(operator, first, second)
            numbers_left.appendleft(result)
        if numbers_left[0] == x:
            return True
    return False

def parse_equations(content: TextIO) -> list[Equation]:
    result = []
    for line in content:
        line = line.strip()
        value, numbers = line.split(":")

        parsed_numbers = numbers.strip().split(" ")
        operator_places = len(parsed_numbers)-1
        equation = (int(value), operator_places, [int(i) for i in parsed_numbers])
        result.append(equation)
    return result

def day_7(content: TextIO, example: bool) -> tuple[int, int]:

    equations = parse_equations(content)

    #start = time.time()
    #print("Start", 0, start)
    operators_part_1 = ["*", "+"]
    results_part_1 = []

    to_check_part_2 = []

    for x, places, numbers in equations:
        possible_solutions = list(itertools.product(operators_part_1, repeat=places))

        if can_be_solved(x, possible_solutions, numbers):
            results_part_1.append(x)
        else:
            to_check_part_2.append((x, places, numbers))

    result_part_1 = sum(results_part_1)
    #part_1_time = time.time()
    #print("Part 1", part_1_time - start, part_1_time)
    #print("Part 1: ", result_part_1)

    #print("PART 2")
    operators_part_2 = ["*", "+", "||"]
    result_part_2 = []

    # caching the operations list actually makes it faster
    possible_solutions_cache_2 : dict[int, list[tuple[str,...]]] = dict()
    for x, places, numbers in to_check_part_2:
        possible_solutions = possible_solutions_cache_2.get(places, None)
        if possible_solutions is None:
            # We need to cast the result of iter tools to a list to consume the generator (?)
            # For whatever reason, if we try to cast it after, or use it as was, it'll just become None / empty list
            possible_solutions = list(itertools.product(operators_part_2, repeat=places))
            possible_solutions_cache_2[places] = possible_solutions

        if can_be_solved(x, possible_solutions, numbers):
            result_part_2.append(x)

    #part_2_time = time.time()
    #print("Part 2", part_2_time - start, part_2_time)

    return (result_part_1, result_part_1 + sum(result_part_2))