#!/usr/bin/python3
'''
  SAT solver based on basic DPLL
  Knowledge representation
'''

import sys
import util


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

def check_empty_clauses(clauses):
    """ Checks whether set of clauses is empty; (sat + empty of DP procedure) """
    for clause in clauses:
        if len(clause) == 0:
            return "unsat"  # True
    return "sat"  # False


# nog niet af
# def propagate_unit_clauses(clauses):
#     unit_clauses = util.find_unit_clauses(clauses)

#     for unit_clause in unit_clauses:
#         clauses = list(
#             filter(lambda c: unit_clause not in c or len(c) == 1, clauses))
#         clauses = util.remove_literal_all_clauses(
#             util.negate(unit_clause), clauses)

#     return clauses


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
            - assume given unit to be true
            - remove clause if unit is in it (entire clause is true because of 'or')
            - modify clauses that contain the negation of unit, by removing the negation of the unit ('or' makes literal reduntant as clause needs to evaluate to true)
    '''
    result_formula = []
    for clause in current_formula:
        if literal in clause:
            print(f"continue: {literal}")
            continue
        if util.negate(literal) in clause:
            modified_clause = [x for x in clause if x != util.negate(literal)]
            # Empty clause = False. Thus continue on alternative branch.
            if not modified_clause:
                return -1
            result_formula.append(modified_clause)
        else:
            result_formula.append(clause)
    return result_formula


def handle_pure_literals(clauses):
    literal_count = util.count_literals(clauses)
    pure_clauses = util.get_pures(literal_count)
    pure_assignment = []
    for pure_clause in pure_clauses:
        clauses = resolve_formula_for_literal(clauses, pure_clause)
    pure_assignment += pure_clauses
    return clauses, pure_clauses


# print(handle_pure_literals(c))
# clauses, num_var = parse_cnf("sudoku1.cnf")
# print(handle_pure_literals(clauses))

# print(propagate_unit_clauses(clauses))
# print(eliminate_pure_literals(clauses))

# def main():
#     clauses, num_vars = read_dimacs_input(sys.argv[1])
#     print(clauses)
#     print(num_vars)
#
#
# if __name__ == '__main__':
#     main()

# print(resolve_formula_for_literal(clauses, 141))


def unit_propagation(clauses):
    assignment = []
    unit_clauses = [c for c in clauses if len(c) == 1]
    while len(unit_clauses) > 0:
        unit = unit_clauses[0]
        clauses = resolve_formula_for_literal(clauses, unit[0])
        assignment += [unit[0]]
        if clauses == -1:
            return -1, []
        if not clauses:
            return clauses, assignment
        unit_clauses = [c for c in clauses if len(c) == 1]
    return clauses, assignment


def dpll(clauses, literal):
    clauses = resolve_formula_for_literal(clauses, literal)
    if len(clauses) == 0:
        return True

    for clause in clauses:
        if len(clause) == 0:
            return False

    literal = util.find_unit_clauses(clauses)
    if len(literal) > 0:
        return dpll(clauses, abs(literal[0]))
    # if (F contains pure L)
    #   return ...

    p = literal[0]
    if dpll(clauses, util.negate(p)):
        return True

    return dpll(clauses, abs(p))


# literal = util.find_unit_clauses(clauses)[0]
# print(dpll(parse_cnf("sudoku1.cnf"), literal))

# Pseudocode DPLL --> https://github.com/safwankdb/SAT-Solver-using-DPLL
# solve_dpll(cnf):
#     while(cnf has a unit clause {X}):
#         delete clauses containing {X}
#         delete {!X} from all clauses
#     if null clause exists:
#         return False
#     if CNF is null:
#         return True
#     select a literal {X}
#     cnf1 = cnf + {X}
#     cnf2 = cnf + {!X}
#     return solve_dpll(cnf1)+solve_dpll(cnf2)


"""
dpll(F, literal) {
    remove clauses containing literal
    shorten clauses containing ~literal
    if (F contains no clauses) :
        return "sat" (True)
    if (F contains empty clause) :
        return "unsat" (False)
    if (F contains a unit or pure L) :
        return DPLL(F, L = True)

    choose P in F (or another heuristic)
    
    if (dpll(F, ~P)) :
        return True;
    else :
        return DPLL(F, L = True)
}
"""
