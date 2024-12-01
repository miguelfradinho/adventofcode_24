import os
import re
import typing
from os import path

FILES_FOLDER : str = "data"

def get_file(file_name : str, ext : str ="txt"):
    file_with_ext = f"{file_name}.{ext}"
    #print(os.getcwd())
    #print(os.path.abspath(os.path.dirname(__file__)))

    path_to_file = path.join(os.getcwd(), FILES_FOLDER, file_with_ext)
    return open(path_to_file, "r", encoding="utf-8")

def get_exercise_file(day: int) -> typing.TextIO:
    exercise_format = f"{day}_input"
    return get_file(exercise_format)


def get_example_file(day: int, part: int = 1) -> typing.TextIO:
    part_prefix = ""
    if part > 1:
        part_prefix = f"_{part}"

    example_format = f"{day}_example{part_prefix}"
    return get_file(example_format)

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def parse_ints(seq : str | list[str]) -> list[int]:
    """Utility function to parse a sequence of integers, just to avoid having type same thing over and over again.

    Parameters
    ----------
    seq : str | list[str]
        Sequence of integers, currently only supported for list or strings, returns an empty list otherwise

    Returns
    -------
    numbers : list[int]
        The numbers but now as ints

    """
    if isinstance(seq, str):
        return [int(i) for i in seq.strip().split(" ") if re.match(r"[-+]?\d+", i)]
    # Assuming it's a list of strings
    elif isinstance(seq, list):
        return [int(i) for i in seq if i.isdecimal()]
    return []