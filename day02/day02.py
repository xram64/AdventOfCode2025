#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day  2  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   '^^^^"^^^^'^^^^"^^^^'^^^^"^^^^||^^^^"^^^^'^^^^"^^^^'^^^^"^^^^'   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1: 38158151648     |            #
#            |  `-----------'   Part 2: 45283684555     |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#


def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]


def is_invalid_part1(id:int):
    """Returns `True` for any ID that consists of a sequence of digits repeated exactly twice."""
    id_len = len(str(id))
    # Ignore any odd-length IDs, since only even-length IDs can have a double sequence.
    if id_len % 2 == 1:
        return False
    # Otherwise, check if the first half of the ID matches the second half.
    elif str(id)[:int(id_len/2)] == str(id)[int(id_len/2):]:
        return True
    else:
        return False

def is_invalid_part2(id:int):
    """Returns `True` for any ID that consists of any sequence of digits repeated any number of times."""
    id_len = len(str(id))
    
    # For each length `n` up to half the length of the full ID, test whether those `n` digits repeat.
    for div in range(1, int(id_len/2)+1):
        # Skip this divisor if it is not the divisor of the ID length.
        if not id_len % (div) == 0:
            continue
        
        # For each divisor `div`, take slices of the digits in the ID to check if every `div`th digit is the same.
        invalid = True
        for offset in range(div):
            if not len(set(str(id)[offset::div])) == 1:  # len == 1 if all digits in this slice are identical
                invalid = False 
                break
        
        # If the last `div` showed a repeated sequence, the ID is invalid.
        if invalid:
            return True
        # Otherwise, continue to the next `div`.
    
    # If no `div` showed an invalid sequence, the ID is valid.
    return False


#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input):
    id_ranges = [tuple(map(int, r.split('-'))) for r in input[0].split(',')]

    invalid_ids = []
    for id_range in id_ranges:
        for id in range(id_range[0], id_range[1]+1):
            if is_invalid_part1(id):
                invalid_ids.append(id)
    return sum(invalid_ids)

#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    id_ranges = [tuple(map(int, r.split('-'))) for r in input[0].split(',')]

    invalid_ids = []
    for id_range in id_ranges:
        for id in range(id_range[0], id_range[1]+1):
            if is_invalid_part2(id):
                invalid_ids.append(id)
    return sum(invalid_ids)


if __name__ == "__main__":
    input = Setup('day02_input.txt')
    
    print(f"[Part 1] Sum of invalid IDs: {Part1(input)}")
    
    print(f"[Part 2] Sum of invalid IDs: {Part2(input)}")