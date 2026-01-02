#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day 10  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   '^^^^"^^^^'^^^^"^^^^'^^^^"^^^^||^^^^"^^^^'^^^^"^^^^'^^^^"^^^^'   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1: 385             |            #
#            |  `-----------'   Part 2:                 |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

import re
from itertools import combinations

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]


class IndicatorRow():
    # Represents indicator light rows as binary lists:
    #  [.##.] = [0,1,1.0]
    #  [#..#.##] = [1,0,0,1,0,1,1]
    lights: list[int]
    def __init__(self, initial_state:str):
        """
        Create a row of indicator lights, set according to `initial_state`.
        
        :param initial_state: String representation of an indicator light row (i.e. `"[.##.#]"`)
        """
        self.lights = [0 if (c == '.') else 1 for c in list(initial_state.strip('[]'))]
    
    def press(self, buttons:list[tuple]) -> bool:
        """
        Press a list of `buttons` in order, and test the effect of pressing these buttons on the initial state of `lights` (the initial state is not modified).
        Returns `True` if this combination of button presses returned the light row to a blank state (i.e. `"[.....]"`), which is equivalent to starting from a blank state and achieving the `lights` state after the button presses.
        """
        test_lights = self.lights.copy()
        blank_lights = [0]*len(test_lights)
        
        for button in buttons:
            for light_index in button:
                # Toggle each light that this button affects.
                test_lights[light_index] = 1 if test_lights[light_index] == 0 else 0
        return (test_lights == blank_lights)

def button_pattern(n_buttons:int):
    """
    Generator to produce bit patterns for button combinations, ordering them to minimize the sum of 1's.
    
    :param n: Number of buttons
    """
    
    # For n buttons, 2^n combinations will be generated.
    
    # Generate all combinations with 1,2,3,... non-zero digits.
    for digits in range(1, n_buttons+1):
        # Generate combinations of indices to set those indices to 1 in button combos.
        index_combs = combinations(range(n_buttons), digits)
        # Form a button pattern, setting a given combination of indices to `1`.
        for index_comb in index_combs:
            button_combo = [0]*n_buttons
            for index in index_comb:
                button_combo[index] = 1
        
            yield tuple(button_combo)

#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input):
    machines:dict[IndicatorRow, list[tuple]] = dict()
    
    for line in input:
        # Extract indicator light row and buttons from the line.
        parts = re.split(r"^(\[.+\]) (.+) (\{.+\})$", line)
        indicator_light_row = IndicatorRow(parts[1])
        
        button_strings = re.findall(r"(\(.+?\))", parts[2])
        buttons_set:list[tuple] = [tuple(map(int, s.strip('()').split(','))) for s in button_strings]
        
        # Map each indicator light row to its set of available buttons.
        machines[indicator_light_row] = buttons_set
    
    # For each machine, determine the minimum number of button presses needed to achieve the target light row.
    num_button_presses_needed_for_machine:dict[IndicatorRow, int] = dict()
    for target_light_row in machines.keys():
        available_buttons = machines[target_light_row]
        
        # Starting with the least number of button presses, generate combinations of buttons to press for this test.
        for pattern in button_pattern(len(available_buttons)):
            test_buttons = [b for i,b in enumerate(available_buttons) if pattern[i] == 1]
            
            # Press the buttons and check the final state of the indicator lights.
            if target_light_row.press(test_buttons):
                num_button_presses_needed_for_machine[target_light_row] = len(test_buttons)
                break
    
    return sum(num_button_presses_needed_for_machine.values())


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    ...


if __name__ == "__main__":
    input = Setup('day10_input.txt')
    
    print(f"[Part 1] Minimum number of button presses to correctly configure all machines: {Part1(input)}")
    
    # print(f"[Part 2] : {Part2(input)}")