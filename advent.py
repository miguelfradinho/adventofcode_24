import typing
from typing import Callable, TextIO

import sol_snake
import utils_files
from utils_files import get_example_file, get_exercise_file
import argparse

type Solution = Callable[[TextIO, bool], typing.Any]

SKIP_DAYS : list[int] = [1,2,3,4,5, 6]
STOP_BEFORE = 8
AOC_YEAR = 2024

def print_day_separator():
    print("="*30)
def print_content_separator():
    print("-"*30)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=f"AdventOfCode - {AOC_YEAR}"
    )

    parser.add_argument("-m", "--exercises", help="Run the exercises", action='store_true')
    parser.add_argument("-e", "--examples", help="Run the examples", action='store_true')

    return parser.parse_args()

def main(args: argparse.Namespace):
    run_examples = args.examples
    run_exercise = args.exercises

    utils_files.setup_directories()

    for day in range(1, 25 + 1):
        if day in SKIP_DAYS:
            continue
        if day >= STOP_BEFORE:
            break
        print_day_separator()
        print((f"Day [{day}] - "*4).removesuffix(" - "))
        print_content_separator()

        try:
            fnc_name = f"day_{day}"
            solution : Solution = getattr(sol_snake, fnc_name)
        except AttributeError:
            print("Solution not found, skipping...")
            continue

        if run_examples:
            print("EXAMPLE")
            example = get_example_file(day)
            example_result = solution(example, True)
            print(example_result)
            print_content_separator()
        if run_exercise:
            print("EXERCISE")
            exercise = get_exercise_file(day, year=AOC_YEAR)
            result = solution(exercise, False)
            print(result)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)