from typing import TextIO

def day_1(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    # first part
    l1 = []
    l2 = []

    # second part
    l2_times = {}

    for i in content:
        first, second = i.split("   ")
        first, second = int(first), int(second)
        l1.append(first)
        l2.append(second)

        times_appeared = l2_times.get(second, 0)
        l2_times[second] = times_appeared +1

    l1.sort()
    l2.sort()

    pairs = set(zip(l1,l2))
    results_part_1 = [first-second  if first > second else second-first for first,second in pairs]

    results_part_2 = [i * l2_times.get(i, 0) for i in l1]

    return sum(results_part_1), sum(results_part_2)