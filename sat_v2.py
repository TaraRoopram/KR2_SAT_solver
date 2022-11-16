import timeit
import util

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

                propagated = list(
                    filter(lambda c: c != util.negate(unit_clause), clause))
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

                eliminated = list(
                    filter(lambda c: c != util.negate(pure_literal), clause))
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

    p = bohms(clauses)
    if dpll(clauses + [[util.positive(p)]], assignments, enable_elim_pure_literals=enable_elim_pure_literals):
        return True
    else:
        return dpll(clauses + [[util.negative(p)]], assignments, enable_elim_pure_literals=enable_elim_pure_literals)


def jeroslow_wang_onesided(clauses, weight=2):
    weights = {}
    for clause in clauses:
        for literal in clause:
            if literal in weights:
                weights[literal] += weight ** -len(clause)
            else:
                weights[literal] = weight ** -len(clause)
    # selects literal with the highest value of j
    return max(weights, key=weights.get)


def jeroslow_wang_twosided(clauses, weight=2):
    '''
        input: clauses, weights
        output: literal to split on
        - consider all clauses, shorter clauses are more important
        - choose literal with maximum  J(x) + J(~x)
        - if: J(x) >= J(~x), pick x, else pick ~x
    '''
    weights = {}
    max_value = -1
    max_literal = -1
    for clause in clauses:
        for literal in clause:
            if literal in weights:
                weights[literal] += weight ** -len(clause)
            else:
                weights[literal] = weight ** -len(clause)
    for literal in weights.keys():
        if util.negate(literal) not in weights:
            weights[util.negate(literal)] = 0
        jw2_value = weights[literal] + weights[util.negate(literal)]
        if jw2_value > max_value:
            max_value = jw2_value
            if weights[literal] >= weights[util.negate(literal)]:
                max_literal = literal
            else:
                max_literal = util.negate(literal)
    return max_literal, max_value


def main():
    clauses = util.read_dimacs_file("data/dimacs/sudoku/sudoku1.cnf")
    jeroslow_wang_onesided(clauses)
    assignments = {}

    start = timeit.default_timer()

    is_satisfiable = dpll(clauses, assignments,
                          enable_elim_pure_literals=False)
    # jw_one = jeroslow_wang_onesided(clauses) --> create rule to determine when this heuristic is chosen https://github.com/marcmelis/dpll-sat/blob/master/solvers/base_sat.py
    stop = timeit.default_timer()

    print("sat" if is_satisfiable else "unsat")
    print(f"assignments: {sorted(assignments.items())}")
    print(f"number of assignments: {len(assignments)}")
    print(f"runtime duration (s): {stop - start}")
    #print(f"literal with highest value: {jw_one}")


main()
