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
#            |  `-----------'   Part 2: 1562459680      |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

#|•...| Notes |...•|#
# • Runtime for `floodfill` operation: 2h 12m
# • Unoptimized runtime for Part 2: 28h 33m
# • Final runtime for Part 2: 17m 14s

from itertools import combinations
import numpy as np
from scipy import sparse
from PIL import Image, ImageColor, ImageDraw, ImageChops
from math import comb
from pathlib import Path
from tqdm import tqdm

# Override pixel limit on PIL images to prevent DecompressionBombError when cropping huge images.
Image.MAX_IMAGE_PIXELS = 10_000_000_000

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]

def _visualize_floor(all_coords:list[tuple], red_coords:list[tuple]) -> Image.Image:
    SCALE = 100
    UNSCALED_DIMS = (100_000, 100_100)
    C_BG = ImageColor.getrgb('#080808')
    C_RED = ImageColor.getrgb('#ff6666')
    C_GREEN = ImageColor.getrgb('#006622')
    C_GREEN_FILL = ImageColor.getrgb('#001003')

    scaled_dims = (int(UNSCALED_DIMS[0]/SCALE), int(UNSCALED_DIMS[1]/SCALE))
    
    img = Image.new('RGB', scaled_dims, C_BG)
    
    # Draw green pixels from full matrix.
    for green_coord in all_coords:
        scaled_coord = (int(green_coord[0]/SCALE), int(green_coord[1]/SCALE))
        img.putpixel(scaled_coord, C_GREEN)
    
    # Draw red pixels for red tiles (overwriting green pixels).
    for red_coord in red_coords:
        scaled_coord = (int(red_coord[0]/SCALE), int(red_coord[1]/SCALE))
        img.putpixel(scaled_coord, C_RED)
    
    # Fill green tiles within the loop.
    point_within_loop = (int(30_000/SCALE), int(30_000/SCALE))
    ImageDraw.floodfill(img, point_within_loop, C_GREEN_FILL)
    
    img.save('test_image.png')
    return img

def determine_matrix_bounds(coord_list:list[tuple]) -> tuple:
    """Scans a list of coordinates to find the largest coord used along each axis.
    Returns the tuple `(n+1, m+1)`, where `n` is the largest row coord and `m` is the largest column coord."""
    max_row, max_col = 0, 0
    for coord in coord_list:
        if coord[0] > max_row:
            max_row = coord[0]
        if coord[1] > max_col:
            max_col = coord[1]
    return (max_row+1, max_col+1)

def calculate_area(coord_pair:tuple[tuple,tuple]) -> int:
    """Calculate the area of the rectangle made using the two coords in the `coord_pair`
    as the corners of the rectangle."""
    first_tile, second_tile = coord_pair
    h = abs(second_tile[0] - first_tile[0]) + 1
    w = abs(second_tile[1] - first_tile[1]) + 1
    return h * w

def draw_filled_floor_img(floor_matrix:sparse.dok_array, matrix_bounds:tuple) -> Image.Image:
    """Returns a 1-bit image object representing the floor grid with green tiles filled into an existing
    loop of red and green tiles, leveraging the `floodfill` method on the image representation."""
    # Initialize 1-bit image (1 bit per pixel).
    floor_img = Image.new('1', matrix_bounds, 0)
    
    # Draw all red/green tiles.
    for coord in list(floor_matrix.keys()):
        floor_img.putpixel(coord, 1)  # type: ignore
    
    # Define a point on the inside of the loop as a seed, and apply a floodfill to fill the inside of the loop.
    seed_point_inside_loop = (30_000, 30_000)  # point chosen by inspection
    ImageDraw.floodfill(floor_img, seed_point_inside_loop, 1)
    
    return floor_img


#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input):
    # Collect coordinates of red tiles.
    red_tile_coords:list[tuple] = []
    for line in input:
        coords = tuple(map(int, line.split(',')))
        red_tile_coords.append(coords)
    
    # Compare all red tile coord pairs to find the combination with the largest rectangle area.
    largest_rectangle_area:int = 0
    for red_tile_pair in combinations(red_tile_coords, 2):
        if (area := calculate_area(red_tile_pair)) > largest_rectangle_area:
            largest_rectangle_area = area
    
    return largest_rectangle_area


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    # Collect coordinates of red tiles.
    red_tile_coords:list[tuple] = []
    for line in input:
        coords = tuple(map(int, line.split(',')))
        red_tile_coords.append(coords)
    
    matrix_bounds = determine_matrix_bounds(red_tile_coords)
    
    # Initialize and populate a sparse boolean matrix to represent the grid of floor tiles.
    # Red and green tiles in the matrix are set True, all other tiles False.
    floor_matrix = sparse.dok_array(matrix_bounds, dtype=np.bool_)
    
    # (Red tiles)
    for tile in red_tile_coords:
        floor_matrix[tile] = True
    
    # (Green tiles)
    # For every consecutive pair of red tiles in the coord list, fill the entries
    #  in between with True values to represent green tiles.
    for i in range(len(red_tile_coords) - 1):
        # Determine whether this line of green tiles is along a row or a column.
        row_dist = abs(red_tile_coords[i+1][0] - red_tile_coords[i][0])
        col_dist = abs(red_tile_coords[i+1][1] - red_tile_coords[i][1])

        if row_dist > 0:    # tiles along row
            for tile_row in range(min(red_tile_coords[i][0], red_tile_coords[i+1][0]) + 1, max(red_tile_coords[i][0], red_tile_coords[i+1][0])):
                floor_matrix[tile_row, red_tile_coords[i][1]] = True
        
        elif col_dist > 0:  # tiles along column
            for tile_col in range(min(red_tile_coords[i][1], red_tile_coords[i+1][1]) + 1, max(red_tile_coords[i][1], red_tile_coords[i+1][1])):
                floor_matrix[red_tile_coords[i][0], tile_col] = True
        
        else:
            print(f"Error: Coordinates {red_tile_coords[i]} & {red_tile_coords[i+1]} do not lie in the same row or column.")
    
    # Handle wraparound from last to first coords in the list as a special case.
    first_coord, second_coord = red_tile_coords[0], red_tile_coords[-1]
    row_dist = abs(second_coord[0] - first_coord[0])
    col_dist = abs(second_coord[1] - first_coord[1])

    if row_dist > 0:    # tiles along row
        for tile_row in range(min(first_coord[0], second_coord[0]) + 1, max(first_coord[0], second_coord[0])):
            floor_matrix[tile_row, first_coord[1]] = True
    
    elif col_dist > 0:  # tiles along column
        for tile_col in range(min(first_coord[1], second_coord[1]) + 1, max(first_coord[1], second_coord[1])):
            floor_matrix[first_coord[0], tile_col] = True

    # Create an image object and fill the loop with green tiles, to act as a reference when checking for valid rectangles.
    if Path('save/floor.png').exists():
        # Load the image from an existing file.
        floor_filled_img = Image.open('save/floor.png')
    else:
        # Generate a new 1-bit image (1 bit per pixel) and save it to a file.
        floor_filled_img = draw_filled_floor_img(floor_matrix, matrix_bounds)
        floor_filled_img.save('save/floor.png')
    
    # Invert image so that 1's represent invalid tiles and 0's represent red/green tiles (for easier logic).
    floor_filled_img_inverted = ImageChops.invert(floor_filled_img)
    
    largest_rectangle_area:int = 0
    floor_width, floor_height = floor_filled_img.size
    stats = {'No area': 0, 'Invalid corners': 0}
    
    # Compare all red tile coord pairs to find the combination with the largest rectangle area that only includes red/green tiles.
    for red_tile_pair in tqdm(combinations(red_tile_coords, 2), total=comb(len(red_tile_coords), 2), unit='comb', smoothing=0.1):
        first_coord, second_coord = red_tile_pair
        
        # Determine inclusive bounds of this rectangle.
        rectangle_bounds = (
            min(first_coord[0], second_coord[0]),   # left
            min(first_coord[1], second_coord[1]),   # top/upper
            max(first_coord[0], second_coord[0]),   # right
            max(first_coord[1], second_coord[1]),   # bottom/lower
        )
        
        # [Heuristic] Skip rectangles with no area.
        if rectangle_bounds[0] == rectangle_bounds[2] or rectangle_bounds[1] == rectangle_bounds[3]:
            stats['No area'] += 1
            continue
        
        # [Heuristic] Skip rectangles with invalid tiles immediately inside any of the corners.
        corner_pixels = [
            (rectangle_bounds[0] + 1, rectangle_bounds[1] + 1),
            (rectangle_bounds[2] - 1, rectangle_bounds[1] + 1),
            (rectangle_bounds[0] + 1, rectangle_bounds[3] - 1),
            (rectangle_bounds[2] - 1, rectangle_bounds[3] - 1),
        ]
        if 0 in [floor_filled_img.getpixel(p) for p in corner_pixels if (0 < p[0] < floor_width and 0 < p[1] < floor_height)]:
            stats['Invalid corners'] += 1
            continue
        
        # Since all red/green tiles are 0 in the inverted image, this method will detect
        #  whether any 1's (invalid tiles) exist within the cropped rectangle.
        if floor_filled_img_inverted.crop(rectangle_bounds).getbbox() == None:
            # This is a valid rectangle, so check its size.
            if (area := calculate_area(red_tile_pair)) > largest_rectangle_area:
                largest_rectangle_area = area
        else:
            continue
    
    print(f'| ---- [Part 2 Stats] -------------------------------------- |')
    print(f'| Rectangles eliminated for no area: {stats['No area']} ({round((stats['No area']/comb(len(red_tile_coords), 2))*100, 2)}%)')
    print(f'| Rectangles eliminated for invalid corners: {stats['Invalid corners']} ({round((stats['Invalid corners']/comb(len(red_tile_coords), 2))*100, 2)}%)')
    
    return largest_rectangle_area
    

if __name__ == "__main__":
    input = Setup('day09_input.txt')
    
    print(f"[Part 1] Area of the largest rectangle made by two tiles: {Part1(input)}")
    
    print(f"[Part 2] Area of the largest rectangle made by two red tiles only containing green tiles: {Part2(input)}")
