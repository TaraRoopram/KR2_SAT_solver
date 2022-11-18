import timeit

import util
from heuristics.moms import moms
from heuristics.dlcs import dlcs
from heuristics.dlis import dlis
from heuristics.bohms import bohms


def propagate_unit_clauses(clauses, assignments):
    unit_clauses = util.find_unit_clauses(clauses)
    while len(unit_clauses) > 0:
        unit_clause = unit_clauses[0][0]

        propagated_clauses = []
        for clause in clauses:
            if util.negate(unit_clause) in clause:
                if util.is_unit_clause(clause):
                    return False

                propagated = list(filter(lambda c: c != util.negate(unit_clause), clause))
                propagated_clauses.append(propagated)
            elif unit_clause not in clause:
                propagated_clauses.append(clause)

        assignments[util.positive(unit_clause)] = unit_clause
        clauses = propagated_clauses
        unit_clauses = util.find_unit_clauses(clauses)

    return clauses


def eliminate_pure_literals(clauses, assignments):
    pure_literals = util.find_pure_literals(clauses)
    for pure_literal in pure_literals:
        eliminated_pure_literals = []
        pure_literal = pure_literal[0]

        for clause in clauses:
            if util.negate(pure_literal) in clause:
                if len(clause) == 1:
                    return False

                eliminated = list(filter(lambda c: c != util.negate(pure_literal), clause))
                eliminated_pure_literals.append(eliminated)
            elif pure_literal not in clause:
                eliminated_pure_literals.append(clause)

        assignments[util.positive(pure_literal)] = pure_literal
        clauses = eliminated_pure_literals

    return clauses


def dpll(clauses, assignments, enable_elim_pure_literals=False):
    clauses = propagate_unit_clauses(clauses, assignments)
    if clauses is False:
        return False

    if enable_elim_pure_literals:
        clauses = eliminate_pure_literals(clauses, assignments)
        if clauses is False:
            return False

    if len(clauses) == 0:
        return True

    for clause in clauses:
        if len(clause) == 0:
            return False

    p = bohms(clauses)
    if dpll(clauses + [[util.negate(p)]], assignments, enable_elim_pure_literals=enable_elim_pure_literals):
        return True
    else:
        return dpll(clauses + [[p]], assignments, enable_elim_pure_literals=enable_elim_pure_literals)


def main():
    clauses = util.read_dimacs_file("data/dimacs/sudoku/sudoku4.cnf")
    assignments = {}

    start = timeit.default_timer()

    is_satisfiable = dpll(clauses, assignments, enable_elim_pure_literals=False)

    stop = timeit.default_timer()

    print("sat" if is_satisfiable else "unsat")
    print(f"assignments: {sorted(assignments.items())}")
    print(f"number of assignments: {len(assignments)}")
    print(f"runtime duration (s): {stop - start}")


main()

# Helpful links
# https://github.com/muneeb706/sudoku-solver/blob/master/basic_sudoku_solver/sudoku-solver.py
# https://users.aalto.fi/~tjunttil/2020-DP-AUT/notes-sat/solving.html
# https://github.com/DRTooley/PythonSatSolver --> implements three different algorithms incl. dpll
# https://github.com/marcmelis/dpll-sat/blob/master/solvers/base_sat.py
