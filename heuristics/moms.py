import util


def moms(clauses, k):
    smallest_clauses = find_smallest_clauses(clauses)
    literal_moms_values = {}
    max_moms_value = -1
    max_moms_literal = clauses[0][0]
    literal_count = util.count_literals(smallest_clauses)

    for clause in smallest_clauses:
        for literal in clause:
            if literal not in literal_moms_values:
                f = literal_count[literal]
                f_neg = literal_count[util.negate(literal)] if util.negate(literal) in literal_count else 0
                s = ((f + f_neg) * (2 ** k)) + (f * f_neg)
                if s > max_moms_value:
                    max_moms_value = s
                    max_moms_literal = literal
                literal_moms_values[literal] = s

    return max_moms_literal


def count_occurrences(clauses, literal):
    count = 0
    for clause in clauses:
        if literal in clause:
            count += 1

    return count


def find_smallest_clauses(clauses):
    smallest_clauses = []
    min_clause_size = len(clauses[0])
    for clause in clauses:
        if len(clause) < min_clause_size:
            min_clause_size = len(clause)

    for clause in clauses:
        if len(clause) == min_clause_size:
            smallest_clauses.append(clause)

    return smallest_clauses
