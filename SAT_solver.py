#!/usr/bin/python3
'''
  SAT solver based on basic DPLL
  Knowledge representation
'''

import sys


# Helpful links
# https://github.com/muneeb706/sudoku-solver/blob/master/basic_sudoku_solver/sudoku-solver.py
# https://users.aalto.fi/~tjunttil/2020-DP-AUT/notes-sat/solving.html
# https://github.com/DRTooley/PythonSatSolver --> implements three different algorithms incl. dpll
# https://github.com/marcmelis/dpll-sat/blob/master/solvers/base_sat.py

# three different strategies: the DPLL algorithm without any further heuristics and two different heuristics

# 1: Read DIMACS input
def read_dimacs_input(filename):
    clauses = []
    with open(filename, 'r') as file:
        next(file)  # skips first row in file
        for line in file:
            data = line.split()
            clause = [int(x) for x in line[:-2].split()]
            clauses.append(clause)
        return clauses  # prints clauses as list of lists


# 2: Encode Sudoku rules as clauses in DIMACS
# reads sudoku-rules-4x4.txt; to print add print() statement
read_dimacs_input("sudoku-rules-4x4.txt")

# 3: Encode a given puzzle in DIMACS
# reads sudoku1.cnf; to print add print() statement
read_dimacs_input("sudoku1.cnf")

# 4: Give (2)+(3) as input to (1) and return the solution to the given puzzle

# Pseudocode DPLL --> https://github.com/safwankdb/SAT-Solver-using-DPLL
# solve_dpll(cnf):
#     while(cnf has a unit clause {X}):
#         delete clauses contatining {X}
#         delete {!X} from all clauses
#     if null clause exists:
#         return False
#     if CNF is null:
#         return True
#     select a literal {X}
#     cnf1 = cnf + {X}
#     cnf2 = cnf + {!X}
#     return solve_dpll(cnf1)+solve_dpll(cnf2)

def propagate_unit_clauses(clauses):
    unit_clauses = util.find_unit_clauses(clauses)

    for unit_clause in unit_clauses:
        clauses = list(filter(lambda c: unit_clause not in c or len(c) == 1, clauses))
        clauses = util.remove_literal_all_clauses(util.negate(unit_clause), clauses)

    return clauses


def eliminate_pure_literals(clauses):
    pure_literals = util.find_pure_literals(clauses)
    print(len(pure_literals))

    for pure_literal in pure_literals:
        clauses = util.remove_clauses_containing_literal(pure_literal, clauses)
        clauses.append([pure_literal])

    return clauses


def main():
    clauses, num_vars = parse_cnf(sys.argv[1])
    print(clauses)
    print(num_vars)


if __name__ == '__main__':
    main()
