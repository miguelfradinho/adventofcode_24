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

    equations_vector = np.array([[a_x, b_x], [a_y, b_y]], dtype=np.int64)
    solution_vector = np.array([int(i) for i in re.findall(parse_ints, prize)], dtype=np.int64)

    return (equations_vector,solution_vector)

def is_close_to_integer(num: float):
    return math.isclose(num, round(num), rel_tol=0, abs_tol=1e-4)

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
    results_part_2 = 0

    part_2_factor = 10000000000000
    for i in equations:
        equation, solutions = i
        a_amount_part_1, b_amount_part_1 = np.linalg.solve(equation, solutions)

        # part 1:
        if is_close_to_integer(a_amount_part_1) and is_close_to_integer(b_amount_part_1):
            if a_amount_part_1 <= 100 and b_amount_part_1 <= 100:
                results_part_1 += (a_amount_part_1 * 3 + b_amount_part_1 * 1)

        # part 2
        solutions_part_2 = solutions + part_2_factor
        a_amount_part_2, b_amount_part_2 = np.linalg.solve(equation, solutions_part_2)
        if is_close_to_integer(a_amount_part_2) and is_close_to_integer(b_amount_part_2):
            results_part_2 += (a_amount_part_2 * 3 + b_amount_part_2 * 1)

    return (int(results_part_1), int(results_part_2))