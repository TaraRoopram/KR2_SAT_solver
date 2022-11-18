def find_unit_clauses(clauses):
    unit_clauses = filter(lambda c: len(c) == 1, clauses)
    return list(unit_clauses)


def find_pure_literals(clauses):
    pure_literals = []
    for c in clauses:
        for l in c:
            if is_pure_literal(l, clauses):
                pure_literals.append([l])

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
    return -literal


def positive(literal):
    return abs(literal)


def negative(literal):
    return -abs(literal)


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


def read_dimacs_file(path):
    with open(f"{path}") as file:
        header = file.readline().split(" ")
        num_variables = header[2]

        clauses = []
        for clause in file:
            if not clause.startswith("c"):
                parsed = list(filter(None, clause[:-1].split(" ")[:-1]))
                parsed = [int(var) for var in parsed]
                clauses.append(parsed)

        return clauses


def parse_cnf(filename):
    '''
    Input: file with all clauses in DIMACS format
    Output: array with clauses, number of variables
    '''
    clauses = []
    for line in open(filename):
        if line.startswith("c"):
            continue
        if line.startswith("p"):
            num_vars = line.split()[2]
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauses.append(clause)
    return clauses #, num_vars
