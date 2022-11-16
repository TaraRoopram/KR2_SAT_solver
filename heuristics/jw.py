import util as util

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
