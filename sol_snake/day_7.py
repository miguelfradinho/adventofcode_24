from typing import TextIO
import itertools


# test_value, operator_places, numbers
type Equation = tuple[int, int, list[int]]


def do_operation(op: str, first: int, second: int) -> int:
    match op:
        case "+":
            return first + second
        case "*":
            return first * second
        case _:
            raise ValueError("Wrong operator!")

def can_be_solved(x: int, operators_combinations: list[tuple[str, ...]], numbers: list[int]) -> bool:
    solutions = []
    for ops in operators_combinations:
        numbers_left = numbers[:]
        ops_left = list(ops)
        while len(numbers_left) > 1 and len(ops_left) > 0:
            first = numbers_left.pop(0)
            second = numbers_left.pop(0)
            operator = ops_left.pop(0)
            result = do_operation(operator, first, second)
            numbers_left.insert(0, result)
        if numbers_left[0] == x:
            solutions.append(operators_combinations)
    return len(solutions) > 0



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

    operators = ["*", "+"]

    result_part_1 = []
    for x, places, numbers in equations:
        possible_solutions = list(itertools.product(operators, repeat=places))
        if can_be_solved(x, possible_solutions, numbers):
            result_part_1.append(x)



    print("PART 2")

    result_part_2 = 0

    return (sum(result_part_1), result_part_2)