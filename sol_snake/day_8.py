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
                # Vectorization time
                difference = (y2-y, x2-x) # Find the vector between the 2 points
                # Distance between the two points (length of the vector)
                dist = utils.euclidean_distance(pos, next_pos)
                # normalized vector
                u_y, u_x = difference[0]/dist, difference[1]/dist

                anti_node_behind = (y-dist*u_y, x-dist*u_x)
                if is_within_bounds(anti_node_behind[1], anti_node_behind[0], map_rows, map_cols):
                    antinodes_positions.add(anti_node_behind)

                anti_node_forward = (y2+dist*u_y, x2+dist*u_x)
                if is_within_bounds(anti_node_forward[1], anti_node_forward[0], map_rows, map_cols):
                    antinodes_positions.add(anti_node_forward)
    results_part_1 = len(antinodes_positions)
    #print_map(antennas_map, antinodes_positions)


    #print("PART 2")
    result_part_2 = 0
    return (results_part_1, result_part_2)