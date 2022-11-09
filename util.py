from SAT_solver import read_dimacs_input


def find_unit_clauses(clauses):
    unit_clauses = filter(lambda c: len(c) == 1, clauses)
    return list(unit_clauses)


def find_pure_literals(clauses):
    pure_literals = list(filter(
        lambda clause: list(filter(
            lambda literal: is_pure_literal(literal, clauses),
            clause)),
        clauses))

    return pure_literals


def is_pure_literal(literal, clauses):
    for c in clauses:
        for v in c:
            if v == negate(literal):
                return False

    return True


def is_negated(literal):
    return literal < 0


def negate(literal):
    return literal * -1


clauses = read_dimacs_input("sudoku1.cnf")

unit_clauses = find_unit_clauses(clauses)
print(unit_clauses)

pure_literals = find_pure_literals(clauses)
print(pure_literals)
