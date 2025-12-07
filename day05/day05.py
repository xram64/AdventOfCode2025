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
#            |  `-----------'   Part 2: 361615643045059 |            #
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
    # Build a list of the ID ranges as tuples, in the format: `[(11, 21), (99, 109), ...]`
    fresh_id_ranges = [tuple(map(int, line.split('-'))) for line in input if re.match(r'^\d+-\d+$', line)]
    
    # Iterate through all ranges in the original list to check for overlaps.
    for this_range_index in range(len(fresh_id_ranges)):
        this_range = fresh_id_ranges[this_range_index]
        
        # If any subsequent `compare_range` overlaps fully or partially with `this_range`, merge the two ranges into one
        #  and replace the `compare_range` with the merged range.
        for compare_range_index in range(this_range_index+1, len(fresh_id_ranges)):
            compare_range = fresh_id_ranges[compare_range_index]
            
            if (
                this_range[0] <= compare_range[0] <= this_range[1] <= compare_range[1] or   # Partial overlap:  ⯊⯊⏺⏺⏺⏺⏺⏺⯋⯋⯋⯋
                compare_range[0] <= this_range[0] <= compare_range[1] <= this_range[1] or   # Partial overlap:  ⯋⯋⯋⯋⏺⏺⏺⏺⏺⏺⯊⯊
                this_range[0] <= compare_range[0] <= compare_range[1] <= this_range[1] or   # Full overlap:     ⯊⯊⏺⏺⏺⏺⏺⏺⯊⯊⯊⯊
                compare_range[0] <= this_range[0] <= this_range[1] <= compare_range[1]      # Full overlap:     ⯋⯋⯋⯋⏺⏺⏺⏺⏺⏺⯋⯋
            ):
                # Replace `compare_range` with the merged range.
                merged_range = (min(this_range[0], compare_range[0]), max(this_range[1], compare_range[1]))
                fresh_id_ranges[compare_range_index] = merged_range
                
                # Remove `this_range` from the final list by setting it to (0, 0).
                fresh_id_ranges[this_range_index] = (0, 0)
                
                break
    
    # Determine the length of each remaining disjoint ID range and return the sum.
    id_range_lengths:dict[tuple, int] = dict()
    for disjoint_range in [rng for rng in fresh_id_ranges if rng != (0, 0)]:
        id_range_lengths[disjoint_range] = disjoint_range[1] - disjoint_range[0] + 1
    
    return sum(id_range_lengths.values())


if __name__ == "__main__":
    input = Setup('day05_input.txt')
    
    print(f"[Part 1] Number of available fresh ingredient IDs: {Part1(input)}")
    
    print(f"[Part 2] Total number of fresh ingredient IDs from ranges: {Part2(input)}")
