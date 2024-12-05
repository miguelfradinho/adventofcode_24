import typing
import os
import requests
from dotenv import dotenv_values

auth_cookie = dotenv_values(".env").get("AOC_COOKIE", None)
if auth_cookie is None:
    raise RuntimeError("Could not load the 'AOC_COOKIE' for downloading inputs")

FILES_FOLDER : str = "data"
INPUT_FORMAT = "{0}_input"

def setup_directories():
    if not os.path.exists(FILES_FOLDER):
        print(f"'{FILES_FOLDER}' folder doesn't exist, creating...")
        os.mkdir(FILES_FOLDER)

def full_path_to_file(file_name: str, extension: str) -> str:
    return os.path.join(os.getcwd(), FILES_FOLDER, f"{file_name}.{extension}")


def get_file(file_path : str) -> typing.TextIO:
    #print(os.getcwd())
    #print(os.path.abspath(os.path.dirname(__file__)))
    return open(file_path, "r", encoding="utf-8")

def get_exercise_file(day: int, year: int) -> typing.TextIO:
    assert day > 0
    file_path = full_path_to_file(file_name=INPUT_FORMAT.format(day), extension="txt")
    try:
        return get_file(file_path)
    except FileNotFoundError:
        print(f"Didn't find input for 'day {day}', fetching...")
        with open(file_path, mode="w", encoding="utf-8") as f:
            input_text = download_input(day=day, year=year)
            print(f"Writing to '{file_path}'")
            f.write(input_text)
        return get_file(file_path)


def get_example_file(day: int, part: int = 1) -> typing.TextIO:
    assert day > 0

    part_prefix = ""
    if part > 1:
        part_prefix = f"_{part}"

    example_format = f"{day}_example{part_prefix}"
    file_path = full_path_to_file(file_name=example_format, extension="txt")

    return get_file(file_path)

def download_input(day : int, year: int) -> str:
    """Downloads the input for Advent of Code. Caches the download separately from the data folder, as to avoid repeting the downloads in case the user decides to change the storage directory

    Parameters
    ----------
    day : int
    year : int

    Returns
    -------
    requests.Response
        Returns the input response

    Raises
    ------
    RuntimeError
        If any error occurred (HTTP Status code != OK)
    """

    cached_file_name = f"{year}_{day}_input.cache"
    cached_folder = os.path.join(os.getcwd(),".aoc_input_cache")
    cached_file_path = os.path.join(cached_folder, cached_file_name)

    # sanity check creating the folder in case it doesn't exist
    if not os.path.exists(cached_folder):
        os.mkdir(cached_folder)

    # Checking if we have it cached and return it
    elif os.path.exists(cached_file_path):
        print(f"Skipping download, found cached input for 'day {day} - {year}'")
        content : str
        with open(cached_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content

    # Otherwise, we need to download and cache it

    headers = {
        "User-Agent" : "github.com/miguelfradinho/adventofcode_24 by miguel.fradinho"
    }
    cookies = {
        "session": auth_cookie
    }

    endpoint = f"https://adventofcode.com/{year}/day/{day}/input"

    print(f"Fetching from '{endpoint}'...")

    r = requests.get(endpoint, headers=headers, cookies=cookies) # type: ignore
    if r.status_code != 200:
        raise RuntimeError(f"Request failed with '{r.status_code}' and {r.json()}")

    print("Download succesful, caching it")
    with open(cached_file_path, "w", encoding="utf-8") as caching:
        print(f"Caching 'day {day} - {year}'")
        caching.write(r.text)

    return r.text