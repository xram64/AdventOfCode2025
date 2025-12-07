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
#            |  `-----------'   Part 2: 8437            |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

#|•...| Notes |...•|#
# • Part 2 is equivalent to a cellular automata with the ruleset `45678//2`:
#     - A cell lives if it has 4 or more neighbors.
#     - A cell dies if it has less than 4 neighbors.
#     - Dead cells cannot become alive.

from enum import Enum
import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageColor, ImageDraw

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]

# Define characters in layout.
class Tile(Enum):
    EMPTY = '.'
    ROLL = '@'


def find_adjacent_coords(center_coords:tuple[int,int], layout:NDArray) -> list[tuple[int,int]]:
    """
    Given a `coords` tuple and the `layout` of the room, returns a list of adjacent coord tuples.
    This function only determines valid adjacent coords for a position and does not check what's in them.
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
    For a list of `adjacent_coords` tuples representing all valid adjacent positions to the center coords, and
    the `layout` of paper rolls in the room, this function returns a sub-list of the adjacent coord tuples that
    contain paper rolls (`@`).
    """
    roll_coords:list[tuple[int,int]] = []
    
    for adj in adjacent_coords:
        if str(layout[adj]) == Tile.ROLL.value:
            roll_coords.append(adj)
    
    return roll_coords

def get_adjacent_live_cells(adjacent_cells:list[tuple[int,int]], state:NDArray) -> list[tuple[int,int]]:
    """
    For a list of `adjacent_cells` tuples representing all valid adjacent positions to a cell, and the
    `state` of a grid, this function returns a sub-list of only the live adjacent cells (`True` cells).
    """
    adjacent_live_cells:list[tuple[int,int]] = []
    
    for adj in adjacent_cells:
        if state[adj] == True:
            adjacent_live_cells.append(adj)
    
    return adjacent_live_cells

def _anim_draw_frame(state:NDArray, last_state:NDArray, anim_options:dict) -> Image.Image:
    """Renders and returns single frames given a state matrix and options dict."""
    # Get defined options or use defaults.
    opt_scale = anim_options.get('scale', 2)    # length/width of square representing each cell, in pixels
    opt_background_color = anim_options.get('background_color', '#333333')
    opt_live_cell_fill_color = anim_options.get('live_cell_fill_color', '#f3831b')
    opt_live_cell_outline_color = anim_options.get('live_cell_outline_color', '#f19035')
    opt_dying_cell_fill_color = anim_options.get('dying_cell_fill_color', '#c24526')
    opt_dying_cell_outline_color = anim_options.get('dying_cell_outline_color', '#c55f45')
    
    # Get width/heigh of frames from state matrix.
    anim_width = int(opt_scale*state.shape[1])
    anim_height = int(opt_scale*state.shape[0])
    
    # Initialize frame.
    anim_frame = Image.new('RGBA', (anim_width, anim_height), ImageColor.getrgb(opt_background_color))
    
    # Draw cells.
    for (row, col), cell in np.ndenumerate(state):
        # Live cell
        if cell == True:
            ImageDraw.Draw(anim_frame).rounded_rectangle(
                [
                    (opt_scale*col, opt_scale*row),
                    (opt_scale*col+(opt_scale-1), opt_scale*row+(opt_scale-1))
                ],
                radius=8,
                fill=ImageColor.getrgb(opt_live_cell_fill_color),
                outline=ImageColor.getrgb(opt_live_cell_outline_color),
            )
        
        # Dying cell (dead but live on last state)
        elif cell == False and last_state[(row, col)] == True:
            ImageDraw.Draw(anim_frame).rounded_rectangle(
                [
                    (opt_scale*col, opt_scale*row),
                    (opt_scale*col+(opt_scale-1), opt_scale*row+(opt_scale-1))
                ],
                radius=8,
                fill=ImageColor.getrgb(opt_dying_cell_fill_color),
                outline=ImageColor.getrgb(opt_dying_cell_outline_color),
            )
            
        # Dead cell
        else:
            pass
    
    return anim_frame

def anim_render_state(state:NDArray, last_state:NDArray, anim_options:dict) -> list[Image.Image]:
    """Render a single state of the grid as multiple frames."""
    new_frames:list[Image.Image] = []
    
    render_options = anim_options.copy()
    
    # Generate 6 frames for each dying cell:
    dying_frames = [
        {'dying_cell_fill_color': '#f3461b', 'dying_cell_outline_color': '#f19035'},
        {'dying_cell_fill_color': '#c24020', 'dying_cell_outline_color': '#c56048'},
        {'dying_cell_fill_color': '#a2381c', 'dying_cell_outline_color': '#c05840'},
        {'dying_cell_fill_color': '#703018', 'dying_cell_outline_color': '#90402c'},
        {'dying_cell_fill_color': '#301c0d', 'dying_cell_outline_color': '#602010'},
        {'dying_cell_fill_color': '#000000', 'dying_cell_outline_color': '#000000'},
    ]
    
    for opts in dying_frames:
        render_options.update(opts)
        new_frames.append(_anim_draw_frame(state, last_state, render_options))
    
    return new_frames

def anim_finalize(frames:list[Image.Image], fps:int = 20) -> None:
    """Save all rendered frames as an APNG."""
    frames[0].save(
        f'anim/day04_part2_{fps}fps.png',
        save_all=True,
        append_images=frames,
        default_image=True,
        disposal=0,
        blend=0,
        duration=int((1/fps)*1000),
        loop=1,
    )


#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input):
    # Convert each line into a list of characters, making each a row in the room `layout` matrix.
    layout = np.array([list(line) for line in input])
    
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
    forklift_accessible_rolls = np.sum((roll_counts < 4) & (layout == Tile.ROLL.value))
    
    return forklift_accessible_rolls


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    # Load the initial room layout as the initial "state" of cells in the grid.
    initial_state_str = np.array([list(line) for line in input])
    # Convert the string state matrix to a bool matrix where `@`="live"=True and `.`="dead"=False.
    initial_state = (initial_state_str == Tile.ROLL.value)
    
    # Set up working state matrices for loop.
    last_state:NDArray = np.empty(initial_state.shape)
    next_state:NDArray = np.copy(initial_state)
    
    # Start list of animation frames and add a frame for the initial state.
    anim_options = {'scale': 8}
    anim_frames:list[Image.Image] = []
    anim_frames += anim_render_state(initial_state, initial_state, anim_options)
    
    # For each timestep, apply the ruleset to transform the state (layout), and render frames for the new layout.
    total_dead_cells = 0
    while not np.array_equal(last_state, next_state):
        # Update the last state to match the result of the last timestep.
        last_state = np.copy(next_state)
        
        # Initialize a matrix to hold the neighbor counts for each cell.
        live_neighbors = np.empty(next_state.shape)
        
        # For each cell (position) in the state (room), count the number of adjacent living cells (paper rolls).
        # By the rule, any cell with less than 4 neighbors will die on the next timestep.
        for row in range(next_state.shape[0]):
            for col in range(next_state.shape[1]):
                center = (row, col)
                
                adjacent_cells = find_adjacent_coords(center, last_state)
                adjacent_live_cells = get_adjacent_live_cells(adjacent_cells, last_state)
                
                live_neighbors[center] = len(adjacent_live_cells)
        
        # Create a bool mask for the state matrix where cells with less than 4 neighbors are set False and cells
        #  with 4 or more are set True, to indicate whether a living cell should live or die in the next timestep.
        state_update_mask = (live_neighbors >= 4)
        
        # Apply the mask to "kill" overcrowded cells (set to False) and keep the rest alive (leave True).
        # Any already dead cells (empty `.` positions) will be unaffected by the `&` operation.
        next_state = (next_state & state_update_mask)
        
        # Count the differences between the last and next state matrices to detect the number of cells that
        #  died on this timestep (i.e. the number of paper rolls that were removed).
        total_dead_cells += np.sum(last_state != next_state)
        
        # Render an animation frame for the newly updated state.
        anim_frames += anim_render_state(next_state, last_state, anim_options)
    
    anim_finalize(anim_frames)
    
    return total_dead_cells


if __name__ == "__main__":
    input = Setup('day04_input.txt')
    
    print(f"[Part 1] Total number of accessible paper rolls: {Part1(input)}")
    
    print(f"[Part 2] Total number of removed paper rolls: {Part2(input)}")
    