import timeit

import util
from heuristics.moms import moms
from heuristics.dlcs import dlcs
from heuristics.dlis import dlis
from heuristics.bohms import bohms
from experiments import Experiments


def propagate_unit_clauses(clauses, assignments, experiments):
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

        experiments.update_number_of_unit_clauses_history(len(unit_clauses))
        assignments[util.positive(unit_clause)] = unit_clause
        clauses = propagated_clauses
        unit_clauses = util.find_unit_clauses(clauses)

    return clauses


def eliminate_pure_literals(clauses, assignments, experiments):
    pure_literals = util.find_pure_literals(clauses)
    experiments.update_number_of_pure_literals_history(len(pure_literals))
    for pure_literal in pure_literals:
        eliminated_pure_literals = []

        for clause in clauses:
            if util.negate(pure_literal) in clause:
                if util.is_unit_clause(clause):
                    return False

                eliminated = list(filter(lambda c: c != util.negate(pure_literal), clause))
                eliminated_pure_literals.append(eliminated)
            elif pure_literal not in clause:
                eliminated_pure_literals.append(clause)

        assignments[util.positive(pure_literal)] = pure_literal
        clauses = eliminated_pure_literals

    return clauses


def perform_tautology_rule(clauses):
    simplified = []
    for clause in clauses:
        for literal in clause:
            if util.negate(literal) not in clause:
                simplified.append(clause)

    return simplified


def preprocessing(clauses):
    clauses = perform_tautology_rule(clauses)
    return clauses


def dpll(clauses, assignments, experiments, enable_elim_pure_literals=False):
    clauses = propagate_unit_clauses(clauses, assignments, experiments)
    if clauses is False:
        return False

    if enable_elim_pure_literals:
        clauses = eliminate_pure_literals(clauses, assignments, experiments)
        if clauses is False:
            return False

    experiments.update_number_of_clauses_history(len(clauses))

    if len(clauses) == 0:
        return True

    for clause in clauses:
        if len(clause) == 0:
            return False

    p = bohms(clauses)
    experiments.inc_num_splits()

    if dpll(clauses + [[util.negate(p)]], assignments, experiments,
            enable_elim_pure_literals=enable_elim_pure_literals):
        return True
    else:
        experiments.inc_num_backtracks()
        return dpll(clauses + [[p]], assignments, experiments, enable_elim_pure_literals=enable_elim_pure_literals)


def main():
    clauses = util.read_dimacs_file("data/dimacs/sudoku/sudoku5.cnf")
    assignments = {}

    experiments = Experiments()
    experiments.set_number_of_givens(clauses)
    experiments.set_number_of_initial_clauses(len(clauses))
    experiments.set_number_of_unit_clauses(len(util.find_unit_clauses(clauses)))
    experiments.set_number_of_pure_literals(len(util.find_pure_literals(clauses)))

    start = timeit.default_timer()
    clauses = preprocessing(clauses)
    is_satisfiable = dpll(clauses, assignments, experiments, enable_elim_pure_literals=True)
    stop = timeit.default_timer()

    print("sat" if is_satisfiable else "unsat")
    print(f"assignments: {sorted(assignments.items())}")
    print(f"number of assignments: {len(assignments)}")
    print(f"runtime duration (s): {stop - start}")

    print(experiments.to_string())


main()

# Helpful links
# https://github.com/muneeb706/sudoku-solver/blob/master/basic_sudoku_solver/sudoku-solver.py
# https://users.aalto.fi/~tjunttil/2020-DP-AUT/notes-sat/solving.html
# https://github.com/DRTooley/PythonSatSolver --> implements three different algorithms incl. dpll
# https://github.com/marcmelis/dpll-sat/blob/master/solvers/base_sat.py
