from typing import TextIO
import re
import utils

valid_antennas = re.compile(r"[a-zA-Z\d]")

def print_map(antennas_map, antinodes_positions):
    _, map_cols = len(antennas_map), len(antennas_map[0])
    print("   " + "".join([f"{i:3d}" for i in range(map_cols)]))

    for y, row in enumerate(antennas_map):
        line = f"{y:3d} "
        for x, val in enumerate(row):
            if (y,x) in antinodes_positions:
                line += f"{'#':^3}"
            else:
                line += f"{val:^3}"
        print(line)

def is_within_bounds(x:int, y:int, rows : int, cols:int) -> bool:
    return (0 <= y < rows) and (0 <= x < cols)


def find_unit_vector_between(a, b) -> tuple[tuple[int,int], float]:
    """Calculates the vector between 2 points (assumes (y,x))

    Parameters
    ----------
    a : tuple[int,int]
        (y1, x1)
    b : tuple[int,int]
        (y2, x2)

    Returns
    -------
    tuple[tuple[int,int]]
        Returns the unit vector + the distance between the 2 points
    """
    y1, x1 = a
    y2, x2 = b
    # Find the vector between the 2 points
    diff = (y2-y1, x2-x1)
    # Distance between the two points (length of the vector)
    dist = utils.euclidean_distance(a, b)
    # normalized vector
    unit_vector = diff[0]/dist, diff[1]/dist

    return (unit_vector, dist)



def day_8(content: TextIO, example: bool) -> tuple[int, int]:

    antennas_map = [i.strip() for i in content.readlines()]
    map_rows, map_cols = len(antennas_map), len(antennas_map[0])

    antenna_positions : dict = {}

    for y, row in enumerate(antennas_map):
        for x, val in enumerate(row):
            if re.match(valid_antennas, val):
                positions = antenna_positions.get(val,None)
                if positions is None:
                    antenna_positions[val] = [(y,x)]
                else:
                    positions.append((y,x))

    antinodes_positions = set()
    for frequency, positions in antenna_positions.items():
        for i, pos in enumerate(positions):
            y, x = pos
            for next_pos in positions[i+1:]:
                y2, x2 = next_pos
                (u_y, u_x), dist = find_unit_vector_between(pos, next_pos)

                anti_node_behind = (y-dist*u_y, x-dist*u_x)
                if is_within_bounds(anti_node_behind[1], anti_node_behind[0], map_rows, map_cols):
                    antinodes_positions.add(anti_node_behind)

                anti_node_forward = (y2+dist*u_y, x2+dist*u_x)
                if is_within_bounds(anti_node_forward[1], anti_node_forward[0], map_rows, map_cols):
                    antinodes_positions.add(anti_node_forward)
    results_part_1 = len(antinodes_positions)
    #print_map(antennas_map, antinodes_positions)

    antinodes_positions_2 = set()
    for frequency, positions in antenna_positions.items():
        for i, pos in enumerate(positions):
            y, x = pos
            for next_pos in positions[i+1:]:
                y2, x2 = next_pos
                (u_y, u_x), dist = find_unit_vector_between(pos, next_pos)

                # we're probably overshooting a little bit (since we could limit based on how many distances we could fit the grid), but this is easier and helps us avoid rounding errors
                for j in range(map_cols):
                    anti_node_behind = (round(y-j*dist*u_y), round(x-j*dist*u_x))
                    if is_within_bounds(anti_node_behind[1], anti_node_behind[0], map_rows, map_cols):
                        antinodes_positions_2.add(anti_node_behind)

                    anti_node_forward = (round(y2+j*dist*u_y), round(x2+j*dist*u_x))
                    if is_within_bounds(anti_node_forward[1], anti_node_forward[0], map_rows, map_cols):
                        antinodes_positions_2.add(anti_node_forward)


    #print("PART 2")
    result_part_2 = len(antinodes_positions_2)
    #print_map(antennas_map, antinodes_positions_2)
    return (results_part_1, result_part_2)