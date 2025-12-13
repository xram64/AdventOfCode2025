#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day  8  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   '^^^^"^^^^'^^^^"^^^^'^^^^"^^^^||^^^^"^^^^'^^^^"^^^^'^^^^"^^^^'   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1:                 |            #
#            |  `-----------'   Part 2:                 |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

from math import prod, dist as distance
from itertools import combinations

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]

ACTUAL_CONNECTIONS_MADE = 0 # TEST

def _connect(box_pair:tuple[tuple,tuple], circuits:list[set], INDEX):
    """Connect two boxes in a new circuit, or add them to an existing circuit. Modifies `circuits` list in place."""
    # Check if one or both of these boxes already exist in other circuits.
    circuit_index_per_box = [-1, -1]
    
    # if INDEX == 82 or INDEX in range(282,386): print('-'*100 + f'\n{INDEX} === {box_pair}')    # TEST
    # if INDEX == 386: print('-'*100 + f'\n{INDEX} === {box_pair}')    # TEST
    
    for circuit_index, circuit in enumerate(circuits):
        # If either box is found in this circuit, associate the box with the circuit's index.
        if box_pair[0] in circuit:
            circuit_index_per_box[0] = circuit_index
        if box_pair[1] in circuit:
            circuit_index_per_box[1] = circuit_index
        # if INDEX == 82 or INDEX in range(282,386): print(f'{circuit_index} :: {circuit}')
        # if INDEX == 386: print(f'{circuit_index} :: {circuit}')
    
    if INDEX in [377,378]: print('CIRCUITS BEFORE' + '~!'*50) ; print(circuits)
    if INDEX in [377,378,379]: print(f'==== [ {INDEX} ] ' + '='*110 + f'\n> Pair: {box_pair}  |  Indices: {circuit_index_per_box}')
    
            
    # global ACTUAL_CONNECTIONS_MADE  # TEST
    
    # Case 1: Neither box is already in a circuit.
    if (circuit_index_per_box[0] == -1) and (circuit_index_per_box[1] == -1):
        if INDEX in [377,378,379]: print('-'*120 + f'<[ # Circuits: {len(circuits)} ]')  # TEST
        if INDEX in [377,378,379]: print(f'| [Case 1] |----------------<|| Box 1: {box_pair[0]} (@ {circuit_index_per_box[0]}) || Box 2: {box_pair[1]} (@ {circuit_index_per_box[1]})')   # TEST
        circuits.append({box_pair[0], box_pair[1]})
        if INDEX in [377,378,379]: print(f'| ~~~~~~~~ | NEW circuit = {circuits[-1]}')  # TEST
        # ACTUAL_CONNECTIONS_MADE += 1 # TEST
        if INDEX in [377,378,379]: print(f'{INDEX:4} | [Case 1] \t{box_pair}')   # TEST
    
    # Case 2: Only one box is already in a circuit, or both boxes are already in the *same* circuit.
    elif (
        (circuit_index_per_box[0] >= 0 and circuit_index_per_box[1] == -1) or
        (circuit_index_per_box[0] == -1 and circuit_index_per_box[1] >= 0) or
        (circuit_index_per_box[0] >= 0 and circuit_index_per_box[1] >= 0 and circuit_index_per_box[0] == circuit_index_per_box[1])
    ):
        if INDEX in [377,378,379]: print('-'*120 + f'<[ # Circuits: {len(circuits)} ]')  # TEST
        if INDEX in [377,378,379]: print(f'| [Case 2] |----------------<|| Box 1: {box_pair[0]} (@ {circuit_index_per_box[0]}) || Box 2: {box_pair[1]} (@ {circuit_index_per_box[1]})')   # TEST
        if circuit_index_per_box[0] >= 0:   # TEST
            if INDEX in [377,378,379]: print(f'|          | circuit[{circuit_index_per_box[0]}] = {circuits[circuit_index_per_box[0]]}')    # TEST
        if circuit_index_per_box[1] >= 0:   # TEST
            if INDEX in [377,378,379]: print(f'|          | circuit[{circuit_index_per_box[1]}] = {circuits[circuit_index_per_box[1]]}')    # TEST
        # Determine the circuit both boxes should be in and add them.
        common_circuit_index = circuit_index_per_box[0] if (circuit_index_per_box[0] >= 0) else circuit_index_per_box[1]
        circuits[common_circuit_index].update({box_pair[0], box_pair[1]})
        if INDEX in [377,378,379]: print(f'{INDEX:4} | [Case 222] \t{box_pair}')   # TEST
        if INDEX in [377,378,379]: print(f'| ~~~~~~~~ | COMMON circuit = {circuits[common_circuit_index]}')    # TEST
        # if not (circuit_index_per_box[0] == circuit_index_per_box[1]): ACTUAL_CONNECTIONS_MADE += 1 # TEST
        
    
    # Case 3: Each box is already in a *separate* circuit.
    else:
        if INDEX in [377,378,379]: print('-'*120 + f'<[ # Circuits: {len(circuits)} ]')  # TEST
        if INDEX in [377,378,379]: print(f'| [Case 3] |----------------<|| Box 1: {box_pair[0]} (@ {circuit_index_per_box[0]}) || Box 2: {box_pair[1]} (@ {circuit_index_per_box[1]})')   # TEST
        if INDEX in [377,378,379]: print(f'|          | circuit[{circuit_index_per_box[0]}] = {circuits[circuit_index_per_box[0]]}')    # TEST
        if INDEX in [377,378,379]: print(f'|          | circuit[{circuit_index_per_box[1]}] = {circuits[circuit_index_per_box[1]]}')    # TEST
        
        # Merge the two circuits into one along with both boxes and add the new circuit to the list.
        merged_circuit = circuits[circuit_index_per_box[0]].union(circuits[circuit_index_per_box[1]], {box_pair[0], box_pair[1]})
        circuits.append(merged_circuit)
        
        if INDEX in [377,378,379]: print(f'| ~~~~~~~~ | MERGED circuit = {circuits[-1]}')    # TEST
        if INDEX in [377,378,379]: print(f'| xxxxxxxx | REMOVED circuit = {circuits[circuit_index_per_box[0]]}')    # TEST
        if INDEX in [377,378,379]: print(f'| xxxxxxxx | REMOVED circuit = {circuits[circuit_index_per_box[1]]}')    # TEST
        
        # Delete the two original circuits.
        circuits.remove(circuits[circuit_index_per_box[0]])     ## <-------------------------------------------------------------- THE PROBLEM
        circuits.remove(circuits[circuit_index_per_box[1]])     ## <-------------------------------------------------------------- THE PROBLEM
        
        # print(f'{INDEX:4} | [Case 33333] \t{box_pair}')   # TEST
        # ACTUAL_CONNECTIONS_MADE += 1 # TEST

def make_connections(box_pairs_by_distance:dict[float, set[tuple[tuple,tuple]]], max_connections:int) -> list[set]:
    """Returns a list of circuits (sets of boxes) made by connecting each closeset pair of boxes."""
    # Maintain a list of circuit sets made by connecting boxes.
    circuits:list[set] = []
    
    # Loop through a sorted list of distances, starting from the lowest, and make connections, keeping track of circuits.
    connections_made = 0
    INDEX = 0   # TEST
    for dist in sorted(box_pairs_by_distance.keys()):
        # In most cases, the next loop should only run once, but if there are multiple pairs with the same distance
        #  between them, they will each be processed here.
        for box_pair in box_pairs_by_distance[dist]:
            # Connect these two boxes by putting them in the same circuit.
            _connect(box_pair, circuits, INDEX)##TEST   # `circuits` will be modified by the function
            INDEX += 1  # TEST
            
            # After each pair is processed, increment counter and exit as soon as the max number of connections is reached.
            connections_made += 1
            if connections_made == max_connections:
                return circuits
    return circuits
            

#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input:list[str]):
    max_connections = 1000
    # max_connections = 10 # TEST
    
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
    
    # for c in circuits: print('-'*80 + f'\n{c}') # [TEST]
    
    # Get the 3 largest circuits and multiply their sizes.
    # print('------ COUNTS --------')     # TEST
    # print(sorted([len(c) for c in circuits], reverse=True))   # TEST
    # print(sorted([len(c) for c in circuits], reverse=True)[:3])   # TEST
    # print(ACTUAL_CONNECTIONS_MADE)  #TEST
    return prod(sorted([len(c) for c in circuits], reverse=True)[:3])


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    ...


#### TEST COMPARISON || Source: https://github.com/nitekat1124/advent-of-code-2025
def OTHER_PART1(data):
    boxes = [list(map(int, line.split(","))) for line in data]

    pairs = {}
    pairs_boxes = {}    # TEST
    for i, box1 in enumerate(boxes):
        for j, box2 in enumerate(boxes[i + 1 :], i + 1):
            # zip is slower but more readable, so I keep it here
            pairs[(i, j)] = sum((a - b) ** 2 for a, b in zip(box1, box2))
            pairs_boxes[(tuple(box1), tuple(box2))] = sum((a - b) ** 2 for a, b in zip(box1, box2)) # TEST

    pairs = sorted(pairs.items(), key=lambda x: x[1])
    pairs_boxes = sorted(pairs_boxes.items(), key=lambda x: x[1])   # TEST

    # nums = 10 if it's test data
    nums = 10 if len(boxes) == 20 else 1000
    pairs = pairs[:nums]

    circuits: list[set] = []

    INDEX = 0
    for (i, j), d in pairs:
        
        circuit_index_per_box_i = -1
        circuit_index_per_box_j = -1

        for circuit_index, circuit in enumerate(circuits):
            if i in circuit:
                circuit_index_per_box_i = circuit_index
            if j in circuit:
                circuit_index_per_box_j = circuit_index

        match (circuit_index_per_box_i > -1, circuit_index_per_box_j > -1):
            case (False, False):
                circuits.append(set([i, j]))
                # print(circuits[-1])
                print(f'{INDEX:4} | [Case 1] \t{pairs_boxes[INDEX][0]}')   # TEST
            case (True, False):
                circuits[circuit_index_per_box_i].add(j)
                print(f'{INDEX:4} | [Case 222] \t{pairs_boxes[INDEX][0]}')   # TEST
            case (False, True):
                circuits[circuit_index_per_box_j].add(i)
                print(f'{INDEX:4} | [Case 222] \t{pairs_boxes[INDEX][0]}')   # TEST
            case (True, True) if circuit_index_per_box_i != circuit_index_per_box_j:
                circuits[circuit_index_per_box_i] |= circuits[circuit_index_per_box_j]
                del circuits[circuit_index_per_box_j]
                print(f'{INDEX:4} | [Case 33333] \t{pairs_boxes[INDEX][0]}')   # TEST
                
            case (True, True) if circuit_index_per_box_i == circuit_index_per_box_j:    # TEST
                print(f'{INDEX:4} | [Case 222] \t{pairs_boxes[INDEX][0]}\t(Skipped)')   # TEST
                
        # print(f'Pair: {pairs_boxes[INDEX]} | Pair indices: {(i, j)} | Dist: {d}')   # TEST
        INDEX += 1

    _lens = sorted([len(s) for s in circuits], reverse=True)
    
    # for c in circuits: print('-'*80 + f'\n{c}') # [TEST]
    
    # print('------ COUNTS --------')     # TEST
    # print(sorted([len(s) for s in circuits], reverse=True))   # TEST
    # print(sorted([len(s) for s in circuits], reverse=True)[:3])   # TEST
    
    
    return _lens[0] * _lens[1] * _lens[2]


if __name__ == "__main__":
    input = Setup('day08_input.txt')
    # input = Setup('day08_test_input.txt')   # [TEST]
    
    
    print(f"[Part 1] Product of the three largest circuits: {Part1(input)}")
    
    # print('='*100)
    # print(OTHER_PART1(input))  # TEST
    
    # print(f"[Part 2] : {Part2(input)}")