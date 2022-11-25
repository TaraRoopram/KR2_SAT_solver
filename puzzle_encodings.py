# encodings for input Sudoku to DIMACS 

from util import parse_cnf

def encode(filename):
    file_num = 1
    path = "data/dimacs/sudoku/9x9"
    file = open(filename, "r")
    for line in file:
        print(file_num)
        givens = encode_line(line, 9)
        rules = get_sudoku_rules(9)
        for given in givens:
            rules.insert(0, [given])
        dimacs = convert_to_dimacs(f"{path}/dimacs_9x9_{file_num}", rules, size=9)
        file_num += 1

    file.close()

def encode_line(line, size):
    clauses = []
    for i in range(0, size):
        for j in range(0, size):
            character = line[(i * size) + j]
            if character != ".":
                clause = f"{i+1}{j+1}{character}"
                clauses.append(clause)

    return clauses


def get_sudoku_rules(size):
    if size == 9:
        rules = parse_cnf("data/dimacs/sudoku_rules/sudoku-rules-9x9.txt")
        return rules


def convert_to_dimacs(dimacs_filename, clauses, size):
    dimacs_file = open(f"{dimacs_filename}.cnf", "w+")
    dimacs_file.write(f"p cnf {size ** 3} {len(clauses)}\n")

    for clause in clauses:
        dimacs_clause = f"{clause[0]} "
        for literal in clause[1:]:
            dimacs_clause += f"{literal} "
        dimacs_clause += "0\n"
        dimacs_file.write(dimacs_clause)

    dimacs_file.close()
    return dimacs_file


# encode("data/raw/1000_sudokus.txt")
