import util as util


# https://mathweb.ucsd.edu/~sbuss/CourseWeb/Math268_2007WS/MarquesSilva_Branching_1999.pdf

def bohms(clauses, alpha=1, beta=2):
    max_clause_size = max([len(clause) for clause in clauses])
    literal_count = {}

    for size in range(1, max_clause_size + 1):
        for clause in clauses:
            for literal in clause:
                if len(clause) == size and literal in clause:
                    if literal not in literal_count:
                        literal_count[literal] = [0] * max_clause_size
                        literal_count[util.negate(literal)] = [0] * max_clause_size
                        literal_count[literal][size - 1] = 1
                    else:
                        literal_count[literal][size - 1] += 1

    for size in range(0, max_clause_size):
        for literal in literal_count:
            h_pos = literal_count[literal][size]
            h_neg = literal_count[util.negate(literal)][size]
            literal_count[literal][size] = alpha * max(h_pos, h_neg) + beta * min(h_pos, h_neg)

    selected_literal = 0
    max_H = 0
    for literal, H in literal_count.items():
        if max(H) > max_H:
            max_H = max(H)
            selected_literal = literal

    return selected_literal

