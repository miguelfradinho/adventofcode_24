from typing import TextIO
from datatypes import Coordinate, Direction
import utils

# ("symbol", coordinates)
type MapPosition = tuple[str, Coordinate]


# Converting the set to a list just for consistent behaviour
valid_directions : list = sorted(list(Direction.GetCardinalDirections()), key= lambda x: x.value)

def find_guard(map) -> Coordinate:
    # assuming each row has the same columns
    rows = len(map)
    cols = len(map[0])

    for row in range(rows):
        for col in range(cols):

            symbol = map[row][col]
            # guard
            if symbol == "^":
                return (row, col)
    raise ValueError("Unable to find the guard!")

def get_next_move(direction : Direction) -> Direction:
    assert direction in valid_directions
    # Turns 90 degrees towards the right
    match direction:
        case Direction.Up:
            return Direction.Right
        case Direction.Right:
            return Direction.Down
        case Direction.Down:
            return Direction.Left
        case Direction.Left:
            return Direction.Up
        case _:
            raise ValueError(f"Movement not possible! {direction}")


def day_6(content: TextIO, example: bool) -> tuple[int, int]:

    positions_map = [i.strip() for i in content.readlines()]

    guard_start_pos : Coordinate = find_guard(positions_map)
    visited_positions : set[Coordinate] = set()
    visited_positions.add(guard_start_pos)

    curr_pos = guard_start_pos
    moving_direction = Direction.Up

    try:
        while True:
            y, x = curr_pos
            next_y, next_x = utils.get_corner_coordinates(x, y , moving_direction)
            # because python lists are cyclical
            if next_y < 0 or next_x < 0:
                raise IndexError

            # obstacle found, so let's switch
            elif positions_map[next_y][next_x] == "#":
                moving_direction = get_next_move(moving_direction)
                continue
            # obstacle not found, so lets update
            else :
                next_pos = (next_y, next_x)
                visited_positions.add(next_pos)
                curr_pos = next_pos

    except IndexError:
        # We exited, so hurray!
        pass


    result_part_1 = len(visited_positions)

    print("PART 2")

    result_part_2 = 0

    return (result_part_1, result_part_2)