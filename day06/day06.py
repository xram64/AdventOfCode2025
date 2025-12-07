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
#            |  `-----------'   Part 2:                 |            #
#            `------------------------------------------'            #
#│∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷▶◀∷∷∷∷∷∷∷∷∷∷∷∷∷∷∷│#

from math import prod

def Setup(filename):
    with open(filename) as f:
        input = f.readlines()
    return [line.strip() for line in input]


#╷----------.
#│  Part 1  │
#╵----------'
def Part1(input:list[str]):
    worksheet_rows = [line.split() for line in input]
    
    # Gather number rows (first 4 rows)
    num_rows = worksheet_rows[:-1]
    # Gather operation row (last row)
    ops = worksheet_rows[-1]
    
    solutions:list[int] = []
    
    for col in range(len(worksheet_rows[0])):
        nums = [int(num_row[col]) for num_row in num_rows]
        if ops[col] == '+':
            solutions.append(sum(nums))
        elif ops[col] == '*':
            solutions.append(prod(nums))
    
    return sum(solutions)


#╷----------.
#│  Part 2  │
#╵----------'
def Part2(input):
    ...


if __name__ == "__main__":
    input = Setup('day06_input.txt')
    
    print(f"[Part 1] Grand total of homework solutions: {Part1(input)}")
    
    # print(f"[Part 2] : {Part2(input)}")
