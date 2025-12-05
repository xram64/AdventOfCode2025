#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day  3  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   '^^^^"^^^^'^^^^"^^^^'^^^^"^^^^||^^^^"^^^^'^^^^"^^^^'^^^^"^^^^'   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1: 17095           |            #
#            |  `-----------'   Part 2: 168794698570517 |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#


def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]


class BatteryPair():
    left:str = '0'
    right:str = '0'
    def __init__(self, left_batt:str='0', right_batt:str='0'):
        self.left = left_batt
        self.right = right_batt
    def get_joltage(self):
        """Return the joltage of the current battery pair."""
        return int(self.left + self.right)
    def update_batts(self, left_batt:str, right_batt:str):
        """Tests whether the input battery pair has a higher joltage than the current pair, and updates the current pair if so."""
        if self.get_joltage() < int(left_batt + right_batt):
            self.left = left_batt
            self.right = right_batt


def build_batt_sequence(bank_ints: list[int], this_batt_slot:int, batt_sequence:list[int]) -> list[int]:
    """
    Given a battery slot (0-11) and a partial battery sequence, this recursive function will find
    the next battery value in the sequence by finding the largest value in the `bank_ints` list
    following the last value added to the sequence, eventually returning the largest possible
    sequence of battery values in the original bank.
    """
    
    # If this is the final iteration, just find the largest battery
    #  value in the rest of the bank (since its index doesn't matter).
    if this_batt_slot == 11:
        next_max_batt = max(bank_ints)
        batt_sequence.append(next_max_batt)
        return batt_sequence
    
    # Find the largest battery value in the rest of the bank and
    #  record the first index of that value seen in `bank_ints`.
    next_max_batt = max(bank_ints[:(this_batt_slot+1)-12])
    next_max_batt_index = bank_ints.index(next_max_batt)
    
    batt_sequence.append(next_max_batt)
    
    # Recurse to find the next battery in the sequence.
    return build_batt_sequence(bank_ints[next_max_batt_index+1:], this_batt_slot+1, batt_sequence)


#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input):
    battery_banks:list[str] = input
    max_joltage_in_each_bank:list[int] = []
    
    for bank in battery_banks:
        max_joltage_batts = BatteryPair()
        for first_batt_index, first_batt in enumerate(bank):
            # If this battery is smaller than the current left battery, skip testing it.
            if int(first_batt) < int(max_joltage_batts.left):
                continue
            
            # If this battery matches the current left battery, only test if
            #  the second battery is larger than the current right battery.
            elif int(first_batt) == int(max_joltage_batts.left):
                for second_batt in bank[first_batt_index+1:]:
                    if int(second_batt) > int(max_joltage_batts.right):
                        max_joltage_batts.update_batts(first_batt, second_batt)
                    
            # Otherwise, test all subsequent second batteries.
            else:
                for second_batt in bank[first_batt_index+1:]:
                    max_joltage_batts.update_batts(first_batt, second_batt)
        max_joltage_in_each_bank.append(max_joltage_batts.get_joltage())
        
    return sum(max_joltage_in_each_bank)


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    battery_banks:list[str] = input
    max_joltage_in_each_bank:list[int] = []
    
    for bank in battery_banks:
        bank_ints = list(map(int, list(bank)))
        
        max_joltage_batt_sequence = build_batt_sequence(bank_ints, 0, [])
        max_joltage_in_each_bank.append(int(''.join(map(str, max_joltage_batt_sequence))))
    
    return sum(max_joltage_in_each_bank)


if __name__ == "__main__":
    input = Setup('day03_input.txt')
    
    print(f"[Part 1] Sum of maximum joltage pairs from each bank: {Part1(input)}")
    
    print(f"[Part 2] Sum of maximum joltage sequences from each bank: {Part2(input)}")