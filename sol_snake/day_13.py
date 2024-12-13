from typing import TextIO
import numpy as np
import numpy.typing as nptypes
import re
import utils
import math

parse_ints = r"(\d+)"

def parse_machine(lines: list[str])-> tuple[nptypes.NDArray, nptypes.NDArray]:
    button_a = lines[0]
    button_b = lines[1]
    prize = lines[2]

    a_x, a_y = utils.parse_ints(button_a)
    b_x, b_y = utils.parse_ints(button_b)

    equations_vector = np.array([[a_x, b_x], [a_y, b_y]], dtype=np.int32)
    solution_vector = np.array([int(i) for i in re.findall(parse_ints, prize)], dtype=np.int32)

    return (equations_vector,solution_vector)

def solution_is_valid(num: float):
    if num > 100:
        return False
    elif not math.isclose(num, round(num)):
        return False
    return True


def day_13(content: TextIO, example: bool) -> tuple[int, int]:

    equations : list[tuple[nptypes.NDArray, nptypes.NDArray]] = []

    lines_to_parse = []
    for line in content:
        line = line.strip()
        if line == "":
            equation = parse_machine(lines_to_parse)
            equations.append(equation)
            lines_to_parse = []
        else:
            lines_to_parse.append(line)
    equation = parse_machine(lines_to_parse)
    equations.append(equation)

    results_part_1 = 0
    for i in equations:
        equation, solutions = i
        a_amount, b_amount = np.linalg.solve(equation, solutions)

        if not solution_is_valid(a_amount):
            #print(equation, solutions, a_amount, b_amount)
            #print("Oofie, A isn't valid, skipping")
            continue
        elif not solution_is_valid(b_amount):
            #print(equation, solutions, a_amount, b_amount)
            #print("Oofie, B isn't valid, skipping")
            continue
        else:
            #print(equation, solutions, a_amount, b_amount)
            #print(a_amount, b_amount)
            results_part_1 += (a_amount * 3 + b_amount * 1)

    results_part_2 = 0
    return (int(results_part_1), results_part_2)