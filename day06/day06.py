#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#
#   ______________________________________________________________   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   |  <<  <<  <>  <|   Advent  of  Code  2025   |>  <>  >>  >>  |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   | + ::|  Day  6  |:: + ::|  Jesse Williams  ∕  xram64  |:: + |   #
#   |~+~===~+==<>==+~===~+~===~+==<>==+~===~+~===~+==<>==+~===~+~|   #
#   '^^^^"^^^^'^^^^"^^^^'^^^^"^^^^||^^^^"^^^^'^^^^"^^^^'^^^^"^^^^'   #
#             __.-----------.___________________________             #
#            |  |  Answers  |   Part 1: 5381996914800   |            #
#            |  `-----------'   Part 2: 9627174150897   |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

from math import prod
from collections import namedtuple

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]

def Setup_Part2(filename):
    # For Part 2, don't strip whitespace from the front of the
    #  row strings, since this puts the first row out of sync.
    with open(filename) as f:
        input = f.readlines()
    return [line for line in input]

Problem = namedtuple('Problem', ['op', 'nums'])


#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input:list[str]):
    worksheet_rows = [line.split() for line in input]
    total_columns = max(map(len, worksheet_rows))
    
    # Gather number rows (first 4 rows)
    num_rows = worksheet_rows[:-1]
    # Gather operation row (last row)
    ops = worksheet_rows[-1]
    
    solutions:list[int] = []
    
    for col in range(total_columns):
        nums = [int(num_row[col]) for num_row in num_rows]
        if ops[col] == '+':
            solutions.append(sum(nums))
        elif ops[col] == '*':
            solutions.append(prod(nums))
    
    return sum(solutions)


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input:list[str]):
    worksheet_rows = input
    total_columns = max(map(len, worksheet_rows))
    
    # List to hold final solutions to each problem.
    solutions:list[int] = []
    
    # Buffer to hold the operation and numbers in each problem as columns are read.
    problem_buffer = Problem(op=None, nums=[])
    
    for col in range(total_columns):
        column:list[str] = [row[col] for row in worksheet_rows]
        column_digits, column_op = column[:-1], column[-1]
        
        # Skip empty columns.
        if len(''.join(column).strip()) == 0:
            continue
        
        # If the last entry in this column shows an operation (`+` or `*`), then this is the start of a
        #  new problem, so compute the solution for the last problem currently in the buffer and clear it.
        if column_op in ['+', '*']:
            # For the first iteration, the operation is set to `None` so it can be skipped.
            if problem_buffer.op:
                solutions.append(problem_buffer.op(problem_buffer.nums))
                
            problem_buffer = Problem(op=(sum if column_op == '+' else prod), nums=[])
        
        # Read the number down this column and add it to the buffer.
        problem_buffer.nums.append(int(''.join(column_digits)))
    
    # Compute the solution to the final problem left in the buffer at the end of the worksheet.
    solutions.append(problem_buffer.op(problem_buffer.nums))
    
    return sum(solutions)


if __name__ == "__main__":
    input = Setup('day06_input.txt')
    input_Part2 = Setup_Part2('day06_input.txt')
    
    print(f"[Part 1] Grand total of homework solutions: {Part1(input)}")
    
    print(f"[Part 2] Corrected grand total of homework solutions: {Part2(input_Part2)}")
