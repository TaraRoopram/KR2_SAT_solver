# Helpful links
# https://github.com/muneeb706/sudoku-solver/blob/master/basic_sudoku_solver/sudoku-solver.py
# https://users.aalto.fi/~tjunttil/2020-DP-AUT/notes-sat/solving.html
# https://github.com/mxklabs/mxklabs-python/tree/master/mxklabs/dimacs

# read the file into string
def read_input_file(filename):
    file = open(filename)
    content = file.readlines()
    parsed_content = ""
    for line in content:
        # since we are dealing with only single digits
        # we can remove spaces in the middle of the numbers
        # to ease iteration in future
        parsed_content += ''.join(line.split())
    return parsed_content


# convert string into matrix to represent input of the puzzle
def generate_matrix(string):
    matrix = [[0 for x in range(9)] for x in range(9)]
    for i in range(9):
        for j in range(9):
            matrix[i][j] = string[i * 9 + j]
    return matrix
