from typing import TextIO
import re

multiply_instructions = r"mul\((\d+,\d+)\)"
enable_instruction = r"(do\(\))"
disable_instruction = r"(don\'t\(\))"
valid_instructions_part_1 = re.compile(multiply_instructions)
valid_instructions_part_2 = re.compile(f"{enable_instruction}|{disable_instruction}|{multiply_instructions}")

def day_3(content: TextIO, is_example: bool) -> tuple[int, int]:

    lines = content.read()
    instructions_part_1 = re.findall(valid_instructions_part_1, lines)

    result_part_1 = 0
    for i in instructions_part_1:
        first,second = i.split(",")
        result = int(first) * int(second)
        result_part_1 += result
    
    print("PART 2")
    result_part_2 = 0
    mul_enabled = True 
    for i in re.finditer(valid_instructions_part_2, lines):
        enable, disable, mul = i.groups()

        if enable is not None:
            mul_enabled = True 
        elif disable is not None:
            mul_enabled = False
        # (implicit) and mul is not None
        elif mul_enabled:
            first,second = mul.split(",")
            result = int(first) * int(second)
            result_part_2 += result

    return (result_part_1, result_part_2)