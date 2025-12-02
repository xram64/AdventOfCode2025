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
#            |  `-----------'   Part 2:                 |            #
#            `------------------------------------------'            #
#│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│#


def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]


class Dial():
    position = 0
    # To keep track of the number of times the dial rests on [0], we'll just record the counts for each number the dial rests on.
    rest_counts = {n: 0 for n in range(100)}
    
    def __init__(self, start_position=50):
        """`start_position`: Starting position of the dial."""
        self.position = start_position
    
    def turn(self, turn_code:str):
        """A 'turn code' is a letter `L` or `R` indicating a 'left' or 'right' turn, 
        followed by a 1- or 2-digit number of clicks in that direction. (e.g. `L5` or `R99`)"""
        direction = turn_code[0]
        clicks = int(turn_code[1:])
        
        if direction == 'R':
            self.position = (self.position + clicks) % 100  # Move dial to new position
            self.rest_counts[self.position] += 1            # Increment rest counter for this position
        elif direction == 'L':
            self.position = (self.position - clicks) % 100  # Move dial to new position
            self.rest_counts[self.position] += 1            # Increment rest counter for this position
    
    def get_rest_count(self, position:int):
        """Returns the number of times the dial has landed on the given `position`."""
        return self.rest_counts[position]
        

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
    ...


if __name__ == "__main__":
    input = Setup('day01_input.txt')
    
    print(f"[Part 1] Number of times dial hit 0: {Part1(input)}")
    
    # print(f"[Part 2] : {Part2(input)}")