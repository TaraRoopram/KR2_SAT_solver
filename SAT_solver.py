#!/usr/bin/python3
'''
  SAT solver based on basic DPLL
  Knowledge representation
'''

import sys
from util import *


# Helpful links
# https://github.com/muneeb706/sudoku-solver/blob/master/basic_sudoku_solver/sudoku-solver.py
# https://users.aalto.fi/~tjunttil/2020-DP-AUT/notes-sat/solving.html
# https://github.com/DRTooley/PythonSatSolver --> implements three different algorithms incl. dpll
# https://github.com/marcmelis/dpll-sat/blob/master/solvers/base_sat.py

# three different strategies: the DPLL algorithm without any further heuristics and two different heuristics

# 1: Read DIMACS input
def parse_cnf(filename):
    '''
    Input: file with all clauses in DIMACS format
    Output: array with clauses, number of variables
    '''
    clauses = []
    for line in open(filename):
        if line.startswith("c"):
            continue
        if line.startswith("p"):
            num_vars = line.split()[2]
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauses.append(clause)
    return clauses, num_vars


# 2: Encode Sudoku rules as clauses in DIMACS
# reads sudoku-rules-4x4.txt; to print add print() statement
# read_dimacs_input("sudoku-rules-4x4.txt")

# 3: Encode a given puzzle in DIMACS
# reads sudoku1.cnf; to print add print() statement
# read_dimacs_input("sudoku1.cnf")

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


def check_empty_clauses(clauses):
    """ Checks whether set of clauses is empty; (sat + empty of DP procedure) """
    for clause in clauses:
        if len(clause) == 0:
            return "unsat"  # True
    return "sat"  # False


c = parse_cnf("sudoku1.cnf")
if check_empty_clauses(c) == "sat":
    print("continue with DP procedure")
else:
    print("terminate DP procedure")


def propagate_unit_clauses(clauses):
    unit_clauses = util.find_unit_clauses(clauses)

    for unit_clause in unit_clauses:
        clauses = list(
            filter(lambda c: unit_clause not in c or len(c) == 1, clauses))
        clauses = util.remove_literal_all_clauses(
            util.negate(unit_clause), clauses)

    return clauses


def eliminate_pure_literals(clauses):
    pure_literals = util.find_pure_literals(clauses)
    print(len(pure_literals))

    for pure_literal in pure_literals:
        clauses = util.remove_clauses_containing_literal(pure_literal, clauses)
        clauses.append([pure_literal])

    return clauses

# Alternatieve implementatie


def resolve_formula_for_literal(current_formula, literal):
    '''
        Input: formula and a (true) literal
        Output: formula that is resolved 
        Body:
            -assume given unit to be true
            - remove clause if unit is in it (entire clause is true because of 'or')
            - modify clauses that contain the negation of unit, by removing the negation of the unit ('or' makes literal reduntant as clause needs to evaluate to true)
    '''
    result_formula = []
    for clause in current_formula:
        if literal in clause:
            continue
        if negate(literal) in clause:
            modified_clause = [x for x in clause if x != negate(literal)]
            # Empty clause = False. Thus continue on alternative branch.
            if not modified_clause:
                return -1
            result_formula.append(modified_clause)
        else:
            result_formula.append(clause)
    return result_formula


def handle_pure_literals(clauses):
    literal_count = count_literals(clauses)
    pure_clauses = get_pures(literal_count)
    pure_assignment = []
    for pure_clause in pure_clauses:
        clauses = resolve_formula_for_literal(clauses, pure_clause)
    pure_assignment = pure_clauses
    return clauses, pure_assignment

# def main():
#     clauses, num_vars = read_dimacs_input(sys.argv[1])
#     print(clauses)
#     print(num_vars)
#
#
# if __name__ == '__main__':
#     main()
