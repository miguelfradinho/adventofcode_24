import re
from datatypes import Coordinate, Direction
import math

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

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
        return [int(i) for i in re.findall(r"[-+]?\d+", seq)]
    # Assuming it's a list of strings
    elif isinstance(seq, list):
        return [int(i) for i in seq if i.isdecimal()]
    return []

def get_cartesian_coordinates(coord: Coordinate, direction: Direction) -> Coordinate:
    x, y = coord

    match direction:
        case Direction.Up:
            return x, y + 1

        case Direction.DiagonalRightUp:
            return x + 1, y + 1

        case Direction.Right:
            return x + 1, y

        case Direction.DiagonalRightDown:
            return x + 1, y - 1

        case Direction.Down:
            return x, y - 1

        case Direction.DiagonalLeftDown:
            return x - 1, y - 1

        case Direction.Left:
            return x - 1, y

        case Direction.DiagonalLeftUp:
            return x - 1, y + 1

        case other:
            raise ValueError("Wrong parsing", other)

def get_corner_coordinates(x:int, y:int, direction: Direction) -> Coordinate:
    """
    This assumes the top left corner as (0,0) and the coordinates as (y,x)
    Returns
    -------
    (y,x) : tuple[int, int]
        Returns the (y,x) coordinates relative to the top left  corner
    """

    match direction:
        case Direction.Up:
            return y-1, x

        case Direction.DiagonalRightUp:
            return y-1, x+1

        case Direction.Right:
            return y, x+1

        case Direction.DiagonalRightDown:
            return y+1, x+1

        case Direction.Down:
            return y + 1, x

        case Direction.DiagonalLeftDown:
            return y+1, x-1

        case Direction.Left:
            return y, x-1

        case Direction.DiagonalLeftUp:
            return y-1, x-1

        case other:
            raise ValueError("Wrong parsing", other)