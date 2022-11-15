# encodings for 4x4 sudoku to DIMACS --> to 9x9 sudoku

from util import parse_cnf

def encode(filename):
    for line in open(filename, "r"):
        clauses = encode_line(line[:-1], 9)
        print(clauses)
                

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
        rules = parse_cnf("sudoku-rules-9x9.txt")
        return rules


def convert_to_dimacs(dimacs_filename, clauses, size):
    print(clauses)
    dimacs_file = open(f"{dimacs_filename}.cnf", "w+")
    dimacs_file.write(f"p cnf {size ** 3} {len(clauses)}\n")

    for clause in clauses:
        dimacs_clause = f"{clause[0]} "
        for literal in clause[1:]:
            dimacs_clause += f" {literal} "
        dimacs_clause += "0\n"
        dimacs_file.write(dimacs_clause)

    dimacs_file.close()
    return dimacs_file

line = ".94...13..............76..2.8..1......32........2...6.....5.4.......8..7..63.4..8"
givens = encode_line(line, 9)
rules = get_sudoku_rules(9)


for given in givens:
    rules.insert(0, [given])

dimacs = convert_to_dimacs("dimacs_9x9", rules, 9)
print(dimacs)
#print(givens)

#encode("data/raw/1000_sudokus.txt")

