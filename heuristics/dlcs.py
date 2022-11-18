import util as util


def dlcs(clauses):
    literal_count = util.count_literals(clauses)
    max_c_pn = -1
    max_v = -1
    for l in literal_count:
        c_p = literal_count[l]
        c_n = literal_count[util.negate(l)] if util.negate(l) in literal_count else 0
        c_pn = c_p + c_n
        if c_pn > max_c_pn:
            max_c_pn = c_pn
            max_v = l

    if literal_count[max_v] > literal_count[util.negate(max_v)]:
        return util.positive(max_v)

    return util.negative(max_v)