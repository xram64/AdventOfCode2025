#│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day  1  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1: 1048            |            #
#            |  `-----------'   Part 2: 6498            |            #
#            `------------------------------------------'            #
#│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│#

from math import floor


def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]


class Dial():
    position = 0
    # To keep track of the number of times the dial rests on [0], we'll just record the counts for each number the dial rests on.
    rest_counts = {n: 0 for n in range(100)}
    # Keep track of the number of times the dial passes [0].
    zero_passes = 0
    
    def __init__(self, start_position=50):
        """`start_position`: Starting position of the dial."""
        self.position = start_position
    
    def turn(self, turn_code:str):
        """A 'turn code' is a letter `L` or `R` indicating a 'left' or 'right' turn, 
        followed by a 1- or 2-digit number of clicks in that direction. (e.g. `L5` or `R99`)"""
        direction = turn_code[0]
        clicks = int(turn_code[1:])
        
        # Count zero passes
        # - To count how many times we pass [0] in one turn, we check the raw un-modded value of `position + clicks`.
        # - If a turn lands the un-modded dial on a number in (1, 99), we couldn't have passed [0].
        # - If the dial lands on `position < 0`, we passed [0] at least once on a 'L' turn.
        # - If the dial lands on `position > 99`, we passed [0] at least once on a 'R' turn.
        dir_sign = 1 if direction == 'R' else -1
        raw_position = self.position + dir_sign*clicks
        
        self.zero_passes += abs(floor(raw_position/100))
        
        # A special case is when the dial lands exactly on [0] after a `L` turn.
        # The abs of the floor of the raw value will always be 1 too low in this case, so it must be incremented again.
        if direction == 'L' and raw_position % 100 == 0:
            self.zero_passes += 1
        
        # Another special case is when the dial turns left from starting on [0].
        # The pass count here will always be 1 too high, since we already counted the starting [0] when the last turn landed on it.
        if direction == 'L' and self.position == 0:
            self.zero_passes -= 1
        
        # [TEST]
        # print(f'{self.position:2} -({direction}{clicks:<3})-> {(raw_position) % 100:2} \t|floor({(raw_position)/100:5.02f})| = |{floor((raw_position)/100):2}| = {abs(floor((raw_position)/100))} \t[z_p = {self.zero_passes}]')
        
        # Turn dial
        if direction == 'R':
            self.position = (self.position + clicks) % 100  # Move dial to new position
            self.rest_counts[self.position] += 1            # Increment rest counter for this position
        elif direction == 'L':
            self.position = (self.position - clicks) % 100  # Move dial to new position
            self.rest_counts[self.position] += 1            # Increment rest counter for this position
    
    def get_rest_count(self, position:int):
        """Returns the number of times the dial has landed on the given `position`."""
        return self.rest_counts[position]
    
    def get_zero_passes(self):
        """Returns the number of times the dial has passed [0] during any turn."""
        return self.zero_passes
        

#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input):
    # Initial dial position: [50]
    dial = Dial(start_position=50)
    
    for turn_code in input:
        dial.turn(turn_code)
    
    return dial.get_rest_count(0)


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    # Initial dial position: [50]
    dial = Dial(start_position=50)
    
    for turn_code in input:
        dial.turn(turn_code)
    
    return dial.get_zero_passes()


if __name__ == "__main__":
    input = Setup('day01_input.txt')
    
    print(f"[Part 1] Number of times dial hit 0: {Part1(input)}")
    
    print(f"[Part 2] Number of times dial passed 0: {Part2(input)}")