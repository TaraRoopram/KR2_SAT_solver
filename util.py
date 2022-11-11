
def find_unit_clauses(clauses):
    unit_clauses = filter(lambda c: len(c) == 1, clauses)
    flattened = map(lambda c: c[0], unit_clauses)
    return list(flattened)


def find_pure_literals(clauses):
    pure_literals = []
    for c in clauses:
        for l in c:
            if is_pure_literal(l, clauses):
                pure_literals.append(l)

    return pure_literals


def is_unit_clause(clause):
    return len(clause) == 1


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


def remove_literal_all_clauses(target_literal, clauses):
    for clause in clauses:
        for literal in clause:
            if literal == target_literal:
                clause.remove(literal)
                # if len(clause) == 0:
                #     clauses.remove(clause)

    return clauses


def remove_clauses_containing_literal(target_literal, clauses):
    for clause in clauses:
        for literal in clause:
            if literal == target_literal:
                clauses.remove(clause)

    return clauses


def count_literals(clauses):
    literal_count = {}
    for clause in clauses:
        for literal in clause:
            if literal in literal_count:
                literal_count[literal] += 1
            else:
                literal_count[literal] = 1
    return literal_count


def get_pures(literal_count):
    pure_clauses = []
    for literal, count in literal_count.items():
        if negate(literal) not in literal_count:
            pure_clauses.append(literal)
    return pure_clauses
