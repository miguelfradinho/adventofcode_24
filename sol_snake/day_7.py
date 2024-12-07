from typing import TextIO
import itertools
from collections import deque
import multiprocessing

# test_value, operator_places, numbers
type Equation = tuple[int, int, list[int]]
type OperatorCombinations = list[tuple[str, ...]]

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

def can_be_solved(x: int, operators_combinations: OperatorCombinations, numbers: list[int]) -> bool:
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

def equations_iterator(to_solve: list[Equation], operators, amount_to_take):
    pos = 0  # store our current position
    batch = to_solve[:]
    while pos < len(batch):
        yield [(x, list(itertools.product(operators, repeat=places)), numbers) for x, places, numbers in batch[pos:pos+amount_to_take]]
        pos += amount_to_take

def can_be_solved_multiple(chunk: list[tuple[int, OperatorCombinations, list[int]]]):
    return [x for x, possible_solutions, numbers in chunk if can_be_solved(x, possible_solutions, numbers)]

def day_7(content: TextIO, example: bool) -> tuple[int, int]:

    equations = parse_equations(content)

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

    #print("PART 2")
    operators_part_2 = ["*", "+", "||"]
    result_part_2 = []

    # ensure at least one process
    cores = max(multiprocessing.cpu_count() - 1, 1)
    pool = multiprocessing.Pool(processes=cores)

    # doing in chunks of 50 is around 15 secs at 2.5 GHz on a 7940HS
    # Doing in chunks of 1 is 12 secs, so meh
    for result in pool.imap_unordered(func=can_be_solved_multiple, iterable=equations_iterator(to_check_part_2, operators_part_2, 50)):
        result_part_2.extend(result)

    return (result_part_1, result_part_1 + sum(result_part_2))