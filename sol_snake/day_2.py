from typing import TextIO

def find_differences(values: list[int]):
    diffs = []
    for i in range(len(values)-1):
        a,b = values[i], values[i+1]
        diff = abs(a - b)
        diffs.append(diff)
    return diffs

def is_descending(values: list[int]):
    for i in range(len(values)-1):
        if values[i] <= values[i+1]:
            return False
    return True

def is_ascending(values: list[int]):
    for i in range(len(values)-1):
        if values[i] >= values[i+1]:
            return False
    return True

def day_2(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    safe_part_1 = 0
    unsafe = 0

    fail_at_least_one_criteria : list[list[int]]= []
    for line in content:
        values = [int(i) for i in line.split(" ") if i != ""]

        ascending = is_ascending(values)
        descending = is_descending(values)
        differences = find_differences(values)

        differences_exceed_safe = [i for i in differences if not(1<= abs(i) <= 3)]
        differences_okay = (differences_exceed_safe == []
                            or (len(differences_exceed_safe) == 1 and differences_exceed_safe[0] == 0))

        match_both = differences_okay and (ascending ^ descending)

        if match_both:
            safe_part_1 += 1
        else:
            unsafe +=1
            fail_at_least_one_criteria.append(values)

    print(len(fail_at_least_one_criteria), unsafe)
    safe_part_2 = safe_part_1

    for to_check in fail_at_least_one_criteria:
        for i in range(len(to_check)):
            values = to_check[:]
            values.pop(i)
            ascending = is_ascending(values)
            descending = is_descending(values)
            differences = find_differences(values)

            differences_exceed_safe = [i for i in differences if not(1<= abs(i) <= 3)]
            differences_okay = (differences_exceed_safe == []
                                or (len(differences_exceed_safe) == 1 and differences_exceed_safe[0] == 0))

            match_both = differences_okay and (ascending ^ descending)
            if match_both:
                safe_part_2 += 1
                break

    return (safe_part_1, safe_part_2)