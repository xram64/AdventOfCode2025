#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day  4  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   '^^^^"^^^^'^^^^"^^^^'^^^^"^^^^||^^^^"^^^^'^^^^"^^^^'^^^^"^^^^'   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1: 1370            |            #
#            |  `-----------'   Part 2:                 |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

import numpy as np
from numpy.typing import NDArray

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]


# Define characters in layout.
TILE_EMPTY = '.'
TILE_ROLL  = '@'

def find_adjacent_coords(center_coords:tuple[int,int], layout:NDArray) -> list[tuple[int,int]]:
    """
    Given a `coords` tuple and the `layout` of the room, returns a list of adjacent coord tuples.
    This function only finds valid adjacents coords and does not check what's in them.
    The `layout` is only needed to determine boundaries. All coord tuples are kept in (row, col) format.
    """
    adj_coords:list[tuple[int,int]] = []
    
    # Convert center coords into a (row, col) vector.
    center_vec = np.array(center_coords, dtype=int)
    
    # Construct a set of coordinate offset masks for generating adjacent coord pairs.
    masks = [np.array((i,j)) for i in [-1,0,1] for j in [-1,0,1] if (i,j) != (0,0)]
    
    # Apply each mask to the current coords.
    for mask in masks:
        adj_vec = center_vec + mask
        # Check that masked coords are within matrix bounds.
        if 0 <= adj_vec[0] < layout.shape[0] and 0 <= adj_vec[1] < layout.shape[1]:
            adj_coords.append((adj_vec[0], adj_vec[1]))
    
    return adj_coords


def get_adjacent_rolls(adjacent_coords:list[tuple[int,int]], layout:NDArray) -> list[tuple[int,int]]:
    """
    Given a list of `adjacent_coords` tuples representing all valid adjacent positions to the center coords
    and the `layout` of paper rolls in the room, this function returns a sub-list of the adjacent coord tuples
    that contain paper rolls (`@`).
    """
    roll_coords:list[tuple[int,int]] = []
    
    for adj in adjacent_coords:
        if str(layout[adj]) == TILE_ROLL:
            roll_coords.append(adj)
    
    return roll_coords


#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input):
    # Convert each line into a list of characters, making each a row in the room `layout` matrix.
    layout = np.array([list(line) for line in input])
    
    # forklift_accessible_rolls:dict[tuple[int,int], bool] = dict()
    roll_counts:NDArray = np.empty(layout.shape)
    
    # For each position in the room, count the number of adjacent coords occupied by paper rolls.
    for row in range(layout.shape[0]):
        for col in range(layout.shape[1]):
            center = (row, col)
            
            adjacent_coords = find_adjacent_coords(center, layout)
            adjacent_rolls = get_adjacent_rolls(adjacent_coords, layout)
            
            # Build a new matrix parallel to the layout matrix that holds the number of rolls adjacent to each position.
            roll_counts[center] = len(adjacent_rolls)
    
    # Forklifts can only access a roll if there are fewer than 4 rolls in adjacent positions.
    # Count the total number of forklift-accessible paper rolls, filtering the `roll_counts` matrix
    #  for counts less than 4 which also coincide with an '@' (roll) in the `layout`` matrix.
    forklift_accessible_rolls = np.sum((roll_counts < 4) & (layout == TILE_ROLL))
    
    return forklift_accessible_rolls


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    ...


if __name__ == "__main__":
    input = Setup('day04_input.txt')
    
    print(f"[Part 1] Total number of accessible paper rolls: {Part1(input)}")
    
    # print(f"[Part 2] : {Part2(input)}")