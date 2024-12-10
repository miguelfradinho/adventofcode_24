from typing import TextIO
from utils import Coordinate, get_corner_coordinates
from datatypes import Direction
from collections import deque

type HikingPosition = tuple[Coordinate, int]

# hoping there's no loops
def yet_another_simple_pathfinding(y_x_grid, starting_position: HikingPosition, end_value : int) -> int:
    rows, cols  = len(y_x_grid), len(y_x_grid[0])

    def is_within_bounds(pos) -> bool:
        y, x = pos
        # sanity check because cyclical lists and out of bounds
        if (y < 0 or y >= rows) or (x < 0 or x >= cols):
            return False
        return True

    visited_nodes = set()
    positions_to_check = deque()
    positions_to_check.appendleft(starting_position)

    trail_heads = 0

    EMPTY_DEQUE = deque()
    while positions_to_check != EMPTY_DEQUE:
        curr_pos = positions_to_check.popleft()
        (y,x), slope = curr_pos
        visited_nodes.add(curr_pos)
        # we found the end, hurray
        if slope == end_value:
            trail_heads += 1
            continue

        # we didn't find the end, so let's search everything else
        for i in Direction.GetCardinalDirections():
            next_y, next_x = get_corner_coordinates(x, y, i)
            if not is_within_bounds((next_y, next_x)):
                continue
            next_pos = y_x_grid[next_y][next_x]
            # we can do this because the positions match their indexes, since it's easier
            (_), next_slope = next_pos
            if (next_slope - slope == 1) and next_pos not in visited_nodes:
                positions_to_check.appendleft(next_pos)
    return trail_heads

def day_10(content: TextIO, example: bool) -> tuple[int, int]:
    # yet another y,x grid

    hiking_input = [i.strip() for i in content.readlines()]
    starting_positions : list[HikingPosition]= []
    hiking_map : list[list[HikingPosition]] = []
    for y, row in enumerate(hiking_input):
        hiking_row = []
        for x, val in enumerate(row):
            slope = int(val)
            position = (y,x), slope
            hiking_row.append(position)
            if slope == 0:
                starting_positions.append(position)
        hiking_map.append(hiking_row)

    results_part_1 = [yet_another_simple_pathfinding(hiking_map, i, 9) for i in starting_positions]


    results_part_2 = 0

    #print("PART 2")
    return (sum(results_part_1), results_part_2)