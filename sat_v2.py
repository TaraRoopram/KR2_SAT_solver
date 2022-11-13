import timeit

import util


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

def tautology(clauses, assignments):
    new_clauses = []
    for clause in clauses:
        for literal in clause:
            if util.negate(literal) not in clause:
                new_clauses.append(clause)
    
    clauses = new_clauses
    return clauses


def dpll(clauses, assignments, enable_elim_pure_literals=False):
    clauses = tautology(clauses, assignments)

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

    p = clauses[0][0]
    if dpll(clauses + [[util.positive(p)]], assignments, enable_elim_pure_literals=enable_elim_pure_literals):
        return True
    else:
        return dpll(clauses + [[util.negative(p)]], assignments, enable_elim_pure_literals=enable_elim_pure_literals)


def main():
    clauses = util.read_dimacs_file("sudoku1.cnf")
    assignments = {}

    start = timeit.default_timer()

    is_satisfiable = dpll(clauses, assignments, enable_elim_pure_literals=False)

    stop = timeit.default_timer()

    print("sat" if is_satisfiable else "unsat")
    print(f"assignments: {sorted(assignments.items())}")
    print(f"number of assignments: {len(assignments)}")
    print(f"runtime duration (s): {stop - start}")


main()