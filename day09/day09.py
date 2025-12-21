#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day  9  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   '^^^^"^^^^'^^^^"^^^^'^^^^"^^^^||^^^^"^^^^'^^^^"^^^^'^^^^"^^^^'   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1: 4741451444      |            #
#            |  `-----------'   Part 2:                 |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

from itertools import combinations

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]


def calculate_area(coord_pair:tuple[tuple,tuple]) -> int:
    """Calculate the area of the rectangle made using the two coords in the `coord_pair`
    as the corners of the rectangle."""
    first_tile, second_tile = coord_pair
    h = abs(second_tile[0] - first_tile[0]) + 1
    w = abs(second_tile[1] - first_tile[1]) + 1
    return h * w

#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input):
    # Collect coordinates of red tiles.
    red_tile_coords:list[tuple] = []
    for line in input:
        coords = tuple(map(int, line.split(',')))
        red_tile_coords.append(coords)
    
    # Compare all coord pairs to find the combination with the largest rectangle area.
    largest_rectangle_area:int = 0
    for red_tile_pair in combinations(red_tile_coords, 2):
        if (area := calculate_area(red_tile_pair)) > largest_rectangle_area:
            largest_rectangle_area = area
    
    return largest_rectangle_area

#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    ...


if __name__ == "__main__":
    input = Setup('day09_input.txt')
    
    print(f"[Part 1] Area of the largest rectangle made by two tiles: {Part1(input)}")
    
    # print(f"[Part 2] : {Part2(input)}")