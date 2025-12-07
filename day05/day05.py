#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day  9  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   '^^^^"^^^^'^^^^"^^^^'^^^^"^^^^||^^^^"^^^^'^^^^"^^^^'^^^^"^^^^'   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1: 707             |            #
#            |  `-----------'   Part 2:                 |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

import re

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]


#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input):
    # Build a list of the ID ranges as tuples, in the format: `[(11, 21), (99, 109), ...]`
    fresh_id_ranges = [tuple(map(int, line.split('-'))) for line in input if re.match(r'^\d+-\d+$', line)]
    
    # Build a list of the available ingredient IDs in the format: `[10, 12, 14, ...]`
    ingredient_ids = [int(line) for line in input if re.match(r'^\d+$', line, )]

    # Scan through ingredient IDs and count how many are fresh.
    fresh_ingredient_ids = []
    for id in ingredient_ids:
        for fresh_range in fresh_id_ranges:
            if fresh_range[0] <= id <= fresh_range[1]:
                fresh_ingredient_ids.append(id)
                break
    
    return len(fresh_ingredient_ids)


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    ...


if __name__ == "__main__":
    input = Setup('day05_input.txt')
    
    print(f"[Part 1] Number of fresh ingredient IDs: {Part1(input)}")
    
    # print(f"[Part 2] : {Part2(input)}")