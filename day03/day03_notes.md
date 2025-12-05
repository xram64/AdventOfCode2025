## Key observation for Part 2
A direct solution for a 12-digit number can be found by first choosing the largest value in the line that's at least 12 digits from the end of the line (where it would be impossible to finish the number).
Next, choose the largest value in the remainder of the line starting one value after the first instance of the largest value found in the last step, and at least 11 digits from the end of the line.
Repeat until 11 digits have been chosen, then choose whatever the largest value is in the remaining part of the line for the 12th digit.

By always choosing the first instance of the largest value in the line, it isn't necessary to keep track of the positions of the selected digits. For the last digit, any instance of the largest value in the rest of the line would produce the same final number.

---

## Logic for `build_batt_sequence()` function
```py
# TEST
#                         0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
# (Original) bank_ints = [1, 9, 1, 5, 1, 1, 4, 4, 3, 3, 2, 2, 5, 5, 1, 1, 1, 1, 1, 1, 1]
#   
# >>Input
#   this_batt_slot  = 2
#   bank_ints       = [1, 1, 4, 4, 3, 3, 2, 2, 5, 5, 1, 1, 1, 1, 1, 1, 1]
#   bank_ints[:-9]  = [1, 1, 4, 4, 3, 3, 2, 2]
#   batt_sequence   = [9, 5]
#
#   next_max_batt = 4
#
# >>Output
#   this_batt_slot  = 3
#   bank_ints       = [4, 3, 3, 2, 2, 5, 5, 1, 1, 1, 1, 1, 1, 1]    (bank_ints[max_batt_index+1:])
#   bank_ints[:-8]  = [4, 3, 3, 2, 2, 5]
#   batt_sequence   = [9, 5, 4]
```

## Initial attempts at `Part2()`
```py
def Part2(input):
    battery_banks:list[str] = input
    max_joltage_in_each_bank:list[int] = []
    
    for i,bank in enumerate(battery_banks):
        print(f"|===| Bank {i+1}/{len(battery_banks)} |===|")
        max_joltage_in_bank = '0'*12
        combs = combinations(bank, 12)
        for comb in tqdm(combs, desc="Checking combinations", unit="comb", total=comb_n_r(len(bank), 12)):
            # :: Heuristics to lower computation costs ::
            # First digit test
            if int(max_joltage_in_bank[0]) > int(comb[0]):
                continue
            # Second digit test
            elif int(max_joltage_in_bank[0]) == int(comb[0]) and int(max_joltage_in_bank[1]) > int(comb[1]):
                continue
            
            # :: Compare this combination to the current max joltage sequence ::
            if int(max_joltage_in_bank) < int(''.join(comb)):
                max_joltage_in_bank = ''.join(comb)
```

```py    
    # Step 1: Gather candidates for the leading joltage digit.
    #   - Find the largest number at least 12 batteries from the end of the bank. This must be the leading digit.
    #   - All batteries with this largest value (at least 12 from the end) are possible leading digits.
    
    # Step 2: Test leading-digit candidates.
    #   - For each candidate, find the largest number that is at least 11 batteries from the end of the bank.
    #   - All batteries with this largest value (at least 11 from the end) are possible second digits for this first digit.

    for i,bank in enumerate(battery_banks):
        print(f"|===| Bank {i+1}/{len(battery_banks)} |===|")
        max_joltage_in_bank = '0'*12
        bank_ints = list(map(int, list(bank)))
        
        digits = [0]*12
        digits[0] = max(bank_ints[:-11])
        # Collect indices of candidates matching the largest battery found.
        batt_candidate_indices = [i for i,n in enumerate(bank_ints) if n == digits[0]]
        
        for candidate_index in batt_candidate_indices:
            # Find the largest battery after this candidate and at least 11 batteries from the end.
            max(bank_ints[candidate_index:-10])
```