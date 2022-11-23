import util as util


def dlis(clauses):
    literal_count = util.count_literals(clauses)
    max_c_pn = -1
    max_v = -1
    for l in literal_count:
        c_p = literal_count[l]
        c_n = literal_count[util.negate(l)] if util.negate(l) in literal_count else 0
        if c_p > max_c_pn:
            max_c_pn = c_p
            max_v = l

        if c_n > max_c_pn:
            max_c_pn = c_n
            max_v = l

    if literal_count[max_v] > literal_count[util.negate(max_v)]:
        return util.positive(max_v)

    return util.negative(max_v)
