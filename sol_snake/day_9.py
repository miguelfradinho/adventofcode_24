from typing import TextIO
from collections import deque
from pprint import pprint

def print_filesystem(filesystem, free_spaces):
    filesystem_map = ""
    spaces_index = 0
    for k,v in filesystem.items():

        for file in v:
            filesystem_map += str(file)

        # because there might be n+1 file blocks for n space blocks
        try:
            space = free_spaces[spaces_index]
            for j in range(space):
                filesystem_map += "."
            spaces_index += 1
        except IndexError:
            pass

    print(filesystem_map)



def defragment_part1(file_system_list, free_spaces):
    FREE_BLOCK =  deque()

    free_spaces_indexes = deque([i for i, v in enumerate(file_system_list) if v == FREE_BLOCK])
    files_indexes = [i for i, v in enumerate(file_system_list) if v != FREE_BLOCK]

    # find the next available block
    next_free_i = free_spaces_indexes.popleft()
    # Get the amount we have available here
    amount_free = free_spaces.popleft()
    while True:
        #print(f"Starting - Free [{next_free_i}]={amount_free}")
        file_to_move_i = files_indexes.pop()
        # find the right most file
        curr_file  = file_system_list[file_to_move_i]
        #print("Moving:", curr_file)
        # we ran out of continuous space,
        if next_free_i >= file_to_move_i:
            #print("Oopsie, no space", curr_file, file_to_move_i, next_free_i)
            break
        # until we moved it all
        while len(curr_file) > 0:
            # we ran out of space, so we need to find the next one
            if amount_free == 0:
                next_free_i = free_spaces_indexes.popleft()
                # edge case: If we're trying to move the file but we'd exceed or stop condition, just use this space, aka, break the loop
                if next_free_i > file_to_move_i:
                    free_spaces_indexes.appendleft(next_free_i)
                    break
                # Get the amount we have available here
                else:
                    amount_free = free_spaces.popleft()
                #print(f"Ran out of space, using  [{next_free_i}]={amount_free}")

            # move the block
            available_space = file_system_list[next_free_i]
            available_space.append(curr_file.pop())
            amount_free -= 1
        else:
            # after we moved, we now have space, so let's include that
            free_spaces_indexes.append(file_to_move_i)

        #print(f"Finished moving - Free [{next_free_i}]={amount_free}")
        #pprint(file_system_list)
    return file_system_list

def defragment_part2(file_system_list, free_spaces: deque):
    FREE_BLOCK =  deque()

    free_spaces_indexes = [i for i, v in enumerate(file_system_list) if v == FREE_BLOCK]
    files_indexes = [i for i, v in enumerate(file_system_list) if v != FREE_BLOCK]

    # find the next available block
    next_free_i = free_spaces_indexes.pop(0)
    # Get the amount we have available here
    free_spaces_list = list(free_spaces)
    free_space_i = 0
    amount_free = free_spaces_list[free_space_i]

    print("STARTING\n")
    while len(files_indexes) != 0:
        #print(f"Starting - Free [{next_free_i}]={amount_free}")
        file_to_move_i = files_indexes.pop()
        # find the right most file
        curr_file  = file_system_list[file_to_move_i]
        #print("Moving:", curr_file)
        # we ran out of continuous space,

        print("Moving", curr_file, files_indexes)
        print("Free", free_spaces_list, free_spaces_indexes)
        # we don't have enough space for this file, so let's try to find the next available space
        if amount_free < len(curr_file):
            suitable_amounts = [(i,v) for i,v in enumerate(free_spaces_list) if len(curr_file) <= v]
            print(suitable_amounts)
            # we found it, so we need to use that
            if any(suitable_amounts):
                free_space_i, val = suitable_amounts[0]
                # pop it from the list of free spaces
                popped = free_spaces_list.pop(free_space_i)
                # very minor sanity check
                assert val == popped
                amount_free = val

                # pop our free index
                next_free_i = free_spaces_indexes.pop(free_space_i)
                print(f"Ran out of space, using  [{next_free_i}]={amount_free}")
                print("State is now", free_spaces_list, free_spaces_indexes)
            # we couldn't find any spot for this, so just leave the file where it is
            else:
                print("No space found for", curr_file)
                continue

        # happy path, we can move it all
        if len(curr_file) <= amount_free:
            # until we moved it all
            while len(curr_file) > 0:
                # move the block
                available_space = file_system_list[next_free_i]
                available_space.append(curr_file.pop())
                amount_free -= 1
            # after we moved, we now have space, so let's include that
            #free_spaces_indexes.append(file_to_move_i)
            print("Finished moving, space left:", amount_free, free_spaces_indexes)

            if amount_free > 0:
                # restore the amount free
                free_spaces_list[free_space_i] = amount_free
                copy_indexes = deque(free_spaces_indexes)
                copy_indexes.appendleft(next_free_i)
                free_spaces_indexes = list(copy_indexes)

        # unhappy path, we can't and that's okay

        print(f"Finished moving - Free [{next_free_i}]={amount_free}")
        pprint(file_system_list)


def day_9(content: TextIO, example: bool) -> tuple[int, int]:
    # single line input
    disk_map = content.read()

    results_part_1 = 0

    file_block_id = 0
    # Alternate between file and free space
    reading_file = True

    filesystem : dict[int, deque] = dict()
    file_system_list: list[deque[int]] = []

    free_spaces = deque()

    # just to avoid instancing multiple empty deques

    for next_free_i in disk_map:
        mapping = int(next_free_i)
        if reading_file:
            file = deque(file_block_id for _ in range(mapping))
            filesystem[file_block_id] = file
            file_system_list.append(file)

            reading_file = False
            file_block_id += 1
        # free space
        elif not reading_file:
            if mapping > 0:
                free_spaces.append(mapping)
                file_system_list.append(deque())
            reading_file = True

    #print(list(free_spaces_indexes)[:20])

    #print("STARTING", free_spaces_indexes)
    #print(free_spaces, len(free_spaces))
    #pprint(file_system_list)

    # deep copying
    part_1_copy = [deque(i) for i in file_system_list]
    #defragment_part1(part_1_copy, free_spaces.copy())

    final_blocks_part_1 = []
    for i in part_1_copy:
        final_blocks_part_1.extend([j for j in i])

    results_part_1 = [i*v for i,v in enumerate(final_blocks_part_1)]
    #pprint([(i,v) for i,v in enumerate(part_1_copy[:100])])

    # deep copying

    part_2_copy = [deque(i) for i in file_system_list]
    defragment_part2(part_2_copy, free_spaces.copy())
    pprint([(i,v) for i,v in enumerate(part_2_copy[:100])])

    final_blocks_part_2 = []
    for i in part_2_copy:
        final_blocks_part_2.extend([j for j in i])

    results_part_2 = [i*v for i,v in enumerate(final_blocks_part_2)]

    #print("PART 2")
    return (sum(results_part_1), sum(results_part_2))