#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day  8  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   '^^^^"^^^^'^^^^"^^^^'^^^^"^^^^||^^^^"^^^^'^^^^"^^^^'^^^^"^^^^'   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1: 75582           |            #
#            |  `-----------'   Part 2: 59039696        |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

from math import prod, dist as distance
from itertools import combinations

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]

def _connect(box_pair:tuple[tuple,tuple], circuits:list[set]) -> bool:
    """Connect two boxes in a new circuit, or add them to an existing circuit. Modifies `circuits` list in place.
    Returns True if a connection was made between these boxes."""
    connection_made = False
    
    # Check if one or both of these boxes already exist in other circuits.
    circuit_index_per_box = [-1, -1]
    for circuit_index, circuit in enumerate(circuits):
        # If either box is found in this circuit, associate the box with the circuit's index.
        if box_pair[0] in circuit:
            circuit_index_per_box[0] = circuit_index
        if box_pair[1] in circuit:
            circuit_index_per_box[1] = circuit_index
    
    # Case 1: Neither box is already in a circuit.
    if (circuit_index_per_box[0] == -1) and (circuit_index_per_box[1] == -1):
        circuits.append({box_pair[0], box_pair[1]})
        connection_made = True
    
    # Case 2: Only one box is already in a circuit, or both boxes are already in the *same* circuit.
    elif (
        (circuit_index_per_box[0] >= 0 and circuit_index_per_box[1] == -1) or
        (circuit_index_per_box[0] == -1 and circuit_index_per_box[1] >= 0) or
        (circuit_index_per_box[0] >= 0 and circuit_index_per_box[1] >= 0 and circuit_index_per_box[0] == circuit_index_per_box[1])
    ):
        # Determine the circuit both boxes should be in and add them.
        common_circuit_index = circuit_index_per_box[0] if (circuit_index_per_box[0] >= 0) else circuit_index_per_box[1]
        circuits[common_circuit_index].update({box_pair[0], box_pair[1]})
        
        if not (circuit_index_per_box[0] == circuit_index_per_box[1]):
            connection_made = True
    
    # Case 3: Each box is already in a *separate* circuit.
    else:
        # Merge the two circuits into one along with both boxes and add the new circuit to the list.
        merged_circuit = circuits[circuit_index_per_box[0]].union(circuits[circuit_index_per_box[1]], {box_pair[0], box_pair[1]})
        circuits.append(merged_circuit)

        # Record the frozen contents of the circuits that should be deleted, to prevent indices from shifting after the first is removed.
        delete_circuit_0 = circuits[circuit_index_per_box[0]]
        delete_circuit_1 = circuits[circuit_index_per_box[1]]
        
        # Delete the two original circuits.
        circuits.remove(delete_circuit_0)
        circuits.remove(delete_circuit_1)
        
        connection_made = True
    
    return connection_made

def make_connections(box_pairs_by_distance:dict[float, set[tuple[tuple,tuple]]], max_connections:int) -> list[set]:
    """Returns a list of circuits (sets of boxes) made by connecting each closeset pair of boxes."""
    # Maintain a list of circuit sets made by connecting boxes.
    circuits:list[set] = []
    
    # Loop through a sorted list of distances, starting from the lowest, and make connections, keeping track of circuits.
    connections_made = 0
    for dist in sorted(box_pairs_by_distance.keys()):
        # In most cases, the next loop should only run once, but if there are multiple pairs with the same distance
        #  between them, they will each be processed here.
        for box_pair in box_pairs_by_distance[dist]:
            # Connect these two boxes by putting them in the same circuit.
            _connect(box_pair, circuits)  # `circuits` will be modified by the function
            
            # After each pair is processed, increment counter and exit as soon as the max number of connections is reached.
            connections_made += 1
            if connections_made == max_connections:
                return circuits
    return circuits

def make_all_connections(box_pairs_by_distance:dict[float, set[tuple[tuple,tuple]]]) -> tuple[tuple,tuple]:
    """Returns a list of circuits (sets of boxes) made by connecting each closeset pair of boxes until all boxes
    are connected in one circuit."""
    # Maintain a list of circuit sets made by connecting boxes.
    circuits:list[set] = []
    
    # Track the last two boxes connected.
    last_two_boxes_connected:tuple[tuple,tuple]
    
    # Loop through a sorted list of distances, starting from the lowest, and make connections, keeping track of circuits.
    for dist in sorted(box_pairs_by_distance.keys()):
        # In most cases, the next loop should only run once, but if there are multiple pairs with the same distance
        #  between them, they will each be processed here.
        for box_pair in box_pairs_by_distance[dist]:
            # Connect these two boxes by putting them in the same circuit.
            connection_made = _connect(box_pair, circuits)  # `circuits` will be modified by the function
            # Push this pair of boxes onto the queue if they were connected.
            if connection_made:
                last_two_boxes_connected = box_pair
    return last_two_boxes_connected


#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input:list[str]):
    max_connections = 1000
    
    # Format a list of all 3-tuples of box coords.
    boxes = [tuple(map(int, coords.split(','))) for coords in input]
    
    # Populate a dict, mapping a distance to a set of pairs of boxes separated by that distance.
    box_pairs_by_distance:dict[float, set[tuple[tuple,tuple]]] = {}
    for box_A, box_B in combinations(boxes, 2):
        pair_dist = distance(box_A, box_B)
        if pair_dist not in box_pairs_by_distance.keys():
            box_pairs_by_distance[pair_dist] = {(box_A, box_B)}
        else:
            box_pairs_by_distance[pair_dist].add((box_A, box_B))

    # Generate a list of circuits made by the closest boxes.
    circuits = make_connections(box_pairs_by_distance, max_connections)
    
    # Get the 3 largest circuits and multiply their sizes.
    return prod(sorted([len(c) for c in circuits], reverse=True)[:3])


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    # Format a list of all 3-tuples of box coords.
    boxes = [tuple(map(int, coords.split(','))) for coords in input]
    
    # Populate a dict, mapping a distance to a set of pairs of boxes separated by that distance.
    box_pairs_by_distance:dict[float, set[tuple[tuple,tuple]]] = {}
    for box_A, box_B in combinations(boxes, 2):
        pair_dist = distance(box_A, box_B)
        if pair_dist not in box_pairs_by_distance.keys():
            box_pairs_by_distance[pair_dist] = {(box_A, box_B)}
        else:
            box_pairs_by_distance[pair_dist].add((box_A, box_B))

    # Generate a list of circuits made by the closest boxes.
    last_two_boxes_connected = make_all_connections(box_pairs_by_distance)
    
    # Multiply the x-coordinates of the last two boxes connected.
    return (last_two_boxes_connected[0][0] * last_two_boxes_connected[1][0])


if __name__ == "__main__":
    input = Setup('day08_input.txt')
    
    print(f"[Part 1] Product of the three largest circuits: {Part1(input)}")

    print(f"[Part 2] Product of the x-coordinates of the last two boxes connected: {Part2(input)}")