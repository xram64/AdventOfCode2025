#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day  7  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   '^^^^"^^^^'^^^^"^^^^'^^^^"^^^^||^^^^"^^^^'^^^^"^^^^'^^^^"^^^^'   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1: 1703            |            #
#            |  `-----------'   Part 2:                 |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

import numpy as np
from numpy.typing import NDArray

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]


def step_forward(current_row:int, splitters:NDArray, beams:NDArray) -> int:
    """
    Takes a matrix of splitter positions and a matrix of beam paths and moves the beams one step down the grid,
    and returns the number of new splits that occur.
    """
    grid_bounds = (0, splitters.shape[1]-1)
    
    # Compare the current row of beams with the next row of splitters to detect new splits.
    # If a beam on one row coincides with a splitter on the next row, a split will happen on the next step.
    splits = (splitters[current_row + 1] & beams[current_row])
    
    # Continue all active beams downward, unless they would overlap a splitter.
    splitter_mask = (splitters[current_row + 1] == False)
    beams[current_row + 1][splitter_mask] = beams[current_row][splitter_mask]
    
    # Collect indices to the left and right of each split (filtered to within grid bounds), and update the beam state.
    split_indices = np.hstack((np.flatnonzero(splits) - 1, np.flatnonzero(splits) + 1))
    split_indices = split_indices[(split_indices >= grid_bounds[0]) & (split_indices <= grid_bounds[1])]
    np.put(beams[current_row+1], split_indices, True)
    
    # Count and return the number of splits that occured on this step.
    return sum(splits)

def render_diagram(splitters:NDArray, beams:NDArray, start_column:int, current_row:int|None = None):
    """Prints the combined current state of the splitter grid and beam paths."""
    char_start = 'S'
    char_beam = '|'
    char_splitter = '^'
    char_blank = '.'
    
    # Convert bool matrices into string matrices.
    str_splitters = np.where(splitters, char_splitter, char_blank)
    str_beams = np.where(beams, char_beam, char_blank)
    
    # Merge the two matrices, overwriting empty cells in the splitters matrix with beams.
    merge_mask = (str_beams == char_beam)
    str_splitters[merge_mask] = str_beams[merge_mask]
    
    # Insert the start symbol.
    str_splitters[0, start_column] = char_start
    
    print_rows = [''.join(row) for row in str_splitters]
    
    # Highlight current row.
    if current_row:
        print_rows[current_row] += f'  <------ [{current_row}]'
    
    print('_'*splitters.shape[1])
    print("\n".join(print_rows))


#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input:list[str]):
    height = len(input)
    width = len(input[0])
    
    # Locate the start position in the first row.
    start_col = input[0].find('S')
    
    # Format the input diagram into a matrix of bools representing splitter positions.
    diagram = np.array([list(line) for line in input])
    splitters = (diagram == '^')
    
    # Initialize a bool matrix to track beam paths.
    active_beams = np.full((height, width), False)
    
    # Generate the first beam below the start position.
    active_beams[1, start_col] = True
    
    split_count = 0

    for row in range(1, height-1):
        render_diagram(splitters, active_beams, start_col, row)
        split_count += step_forward(row, splitters, active_beams)   # `active_beams` will be modified by the function

    return(split_count)


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    ...


if __name__ == "__main__":
    input = Setup('day07_input.txt')
    
    print(f"[Part 1] Total number of splits: {Part1(input)}")
    
    # print(f"[Part 2] : {Part2(input)}")
