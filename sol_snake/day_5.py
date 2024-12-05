from typing import TextIO

type Rule = tuple[int, int]
type Pages = list[int]
type PageUpdates = list[Pages]

def day_5(content: TextIO, example: bool) -> tuple[int, int]:
    order_rules : list[Rule] = []
    page_updates : PageUpdates = []

    reading_ordering = True
    for line in content:
        line = line.strip()
        if line == "":
            reading_ordering = False
            continue
        if reading_ordering:
            before, after = line.split("|")
            order = (int(before), int(after))
            order_rules.append(order)
        else:
            pages_to_update = line.split(",")
            page_updates.append([int(i) for i in pages_to_update if i != ""])

    order_rules.sort(key=lambda x: x[0])

    correctly_ordered : PageUpdates = []
    incorrectly_ordered : list[tuple[Pages, list[Rule]]] = []

    for pages in page_updates:
        valid = True
        rules_to_check = []

        for rule in order_rules:
            before, after = rule
            both_in_update = before in pages and after in pages
            if both_in_update:
                rules_to_check.append(rule)
                if pages.index(before) >= pages.index(after):
                    valid = False
        if valid:
            correctly_ordered.append(pages)
        else:
            incorrectly_ordered.append((pages, rules_to_check))

    result_part_1 = sum([i[len(i)//2] for i in correctly_ordered])

    print("PART 2")

    middle_points = []
    # There's probably an ordering/sorting alternative, but we don't really need to find or build a list
    # As this is essentially a problem that relies on finding the median number
    # Since our updates need to follow the rules, then something that is "correctly" ordered needs to follow all the rules...
    # So, our middle point will be... the one that appears the median number of times in the "after" rules :^)
    for pages, rules in incorrectly_ordered:
        before_rules = [i[0] for i in rules]
        after_rules = [i[1] for i in rules]
        middle_point = len(pages) // 2

        middle_number : int = 0
        for i in set(before_rules):
            if after_rules.count(i) == middle_point:
                middle_number = i

        middle_points.append(middle_number)
    result_part_2 = sum(middle_points)

    return (result_part_1, result_part_2)