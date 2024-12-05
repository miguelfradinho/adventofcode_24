from typing import TextIO
from datatypes import Direction, Coordinate
import utils
type WordSearchPoint = tuple[Coordinate, set[Direction]]


def part_1(word_search):
    n_rows = len(word_search)
    m_cols = len(word_search[0])
    word_to_find = "XMAS"
    start_char = word_to_find[0]

    result_part_1 = 0

    possible_starts : list[WordSearchPoint] = list()
    for n in range(n_rows):
        #print(n, word_search[n])
        for m in range(m_cols):
            curr_char = word_search[n][m]
            if curr_char == start_char:
                # edge cases, borders
                directions_to_exclude = set()
                # upwards
                if n == 0:
                    directions_to_exclude.add(Direction.GetUpwardsDirections)
                elif n == n_rows-1:
                    directions_to_exclude.add(Direction.GetDownwardsDirections)
                # left
                if m == 0:
                    directions_to_exclude.add(Direction.GetLeftwardsDirections)
                elif m == m_cols - 1:
                    directions_to_exclude.add(Direction.GetRightwardsDirections)
                directions_to_check = set([i for i in Direction if i not in directions_to_exclude])
                possible_starts.append(((n,m), directions_to_check))

    #print("\n".join(word_search))
    # TODO: we could optimize this by inverting the order
    # e.g. Exclude all Xs that don't have a neighbouring M
    # Then all M's that don't have a neighbouring A, etc
    # but that would require a bit of shift in the way we're storing
    for start_coords, directions in possible_starts:
        directions_to_check = list(directions)
        for i in directions_to_check:
            curr_y, curr_x = start_coords
            try:
                #print("Checking ", word_search[curr_y][curr_x], start_coords, i.__repr__())
                checked = ""
                for j in word_to_find[1:]:
                    next_y, next_x = utils.get_corner_coordinates(curr_x, curr_y, i)
                    # because lists are cyclical
                    if next_x < 0 or next_y < 0:
                        raise IndexError
                    next_char = word_search[next_y][next_x]
                    checked += next_char
                    if next_char != j:
                        break
                    curr_x = next_x
                    curr_y = next_y
                else: # only if the previous did not break
                    # we found a match, so let's include
                    result_part_1 += 1
                #print("checked:", checked)
            except IndexError: # we reached a boundary, so let's skip this direction
                #print("skipped", i)
                continue
    return result_part_1


def part_2(word_search):
    n_rows = len(word_search)
    m_cols = len(word_search[0])
    start_char = "A"

    possible_starts : list[WordSearchPoint] = list()
    for n in range(n_rows):
        for m in range(m_cols):
            curr_char = word_search[n][m]
            if curr_char == start_char:
                directions_to_exclude = set()
                directions_to_include = [
                    Direction.DiagonalLeftDown,
                    Direction.DiagonalLeftUp,
                    Direction.DiagonalRightDown,
                    Direction.DiagonalRightUp
                ]
                # upwards
                if n == 0:
                    directions_to_exclude.add(Direction.GetUpwardsDirections)
                elif n == n_rows-1:
                    directions_to_exclude.add(Direction.GetDownwardsDirections)
                # left
                if m == 0:
                    directions_to_exclude.add(Direction.GetLeftwardsDirections)
                elif m == m_cols - 1:
                    directions_to_exclude.add(Direction.GetRightwardsDirections)
                directions_to_check = set([i for i in directions_to_include if i not in directions_to_exclude])
                directions = directions_to_check
                # sorting just to avoid non-deterministic behaviour
                #directions = sorted(directions_to_check, key=lambda x: x.value)
                possible_starts.append(((n,m), directions))

    found = set()

    # This depends on whatever the Direction enumm defines as values but alas
    # Order is: Top right, bottom right, bottom left, top left
    # so the only invalid cases are when both diagonals are the same
    # In which case, our valid inputs are whenever we see 2 occurences of either SS or MM
    # In whichever we visited
    # SSMM, SMMS, MMSS, MSSM
    valid_cases = ["SSMM", "SMMS", "MMSS", "MSSM"]
    for start_coords, directions in possible_starts:
        directions_to_check = list(directions)
        directions_to_check.sort(key=lambda x: x.value)
        checked = ""
        try:
            for i in directions_to_check:
                curr_y, curr_x = start_coords
                #print("Checking from", start_coords, i.__repr__())

                next_y, next_x = utils.get_corner_coordinates(curr_x, curr_y, i)
                # because lists are cyclical
                if next_x < 0 or next_y < 0:
                    #print("skipping", next_y, next_x)
                    raise IndexError
                next_char = word_search[next_y][next_x]
                #print(next_char)
                checked += next_char

                curr_x = next_x
                curr_y = next_y
            #print("finished checking with", checked)
        except IndexError: # we reached a boundary, so this shouldn't count
            #print("skipped", i)
            continue
        if checked in valid_cases:
            #print("Found", start_coords)
            found.add(start_coords)

    final_result = [list(i) for i in word_search]
    for f in found:
        y,x = f
        final_result[y][x] = "F"

    #print("\n".join("".join(i) for i in final_result))

    return len(found)

def day_4(content: TextIO, example: bool) -> tuple[int, int]:

    word_search = [i.strip() for i in content.readlines()]

    result_part_1 = part_1(word_search[:])

    print("PART 2")
    result_part_2 = part_2(word_search[:])

    return (result_part_1, result_part_2)