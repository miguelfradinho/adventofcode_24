import typing
from typing import Callable, TextIO

import sol_snake
from utils import get_example_file, get_exercise_file
import argparse

type Solution = Callable[[TextIO, bool], typing.Any]

SOLUTION_PREFIX = "day_"
RUN_EXAMPLES : bool
RUN_EXERCISE : bool
DAYS = range(1, 25 + 1)
SKIP_DAYS : list[int] = []
STOP_BEFORE = 6

def get_solution(day: int) -> Solution:
    fnc_name = f"{SOLUTION_PREFIX}{day}"
    return getattr(sol_snake, fnc_name)

def print_day_separator():
    print("="*30)
def print_content_separator():
    print("-"*30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="AdventOfCode - 2024"
    )

    parser.add_argument("-m", "--exercises", help="Run the exercises", action='store_true')
    parser.add_argument("-e", "--examples", help="Run the examples", action='store_true')

    args = parser.parse_args()
    RUN_EXAMPLES = args.examples
    RUN_EXERCISE = args.exercises

    solution_prefix = "day_"
    for day in DAYS:
        if day in SKIP_DAYS:
            continue
        if day >= STOP_BEFORE:
            break
        print_day_separator()
        print((f"Day [{day}] - "*4).removesuffix(" - "))
        print_content_separator()
        try:
            solution = get_solution(day)
        except AttributeError:
            print("Solution not found, skipping...")
            continue
        if RUN_EXAMPLES:
            print("EXAMPLE")
            example = get_example_file(day)
            example_result = solution(example, True)
            print(example_result)
            print_content_separator()
        if RUN_EXERCISE:
            print("EXERCISE")
            exercise = get_exercise_file(day)
            result = solution(exercise, False)
            print(result)