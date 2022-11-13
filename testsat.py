## inspo from https://github.com/ldelille/dpll/blob/master/dpll.py
#globals
clauses = []

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

def unit_propagation_check(clause, literal):
    assignment = clause[:]
    if not clause:
        return None
    if literal not in clause and -literal not in clause:
        return assignment
    if literal in clause:
        return None
    assignment.remove(-literal)
    return assignment

def unit_propagation(clauses, literal):
    assignment = []
    if not clauses:
        return None
    for clause in clauses:
        propagated_clause = unit_propagation_check(clause, literal)
        if propagated_clause == []:
            return []
        if propagated_clause:
            assignment.append(propagated_clause)
    if len(assignment) == 0:
        return None
    else:
        return assignment

def find_pure_literals(clauses):
    pure_list = {}
    for clause in clauses:
        for literal in clause:
            if -literal in pure_list:
                pure_list[literal] = 0
                pure_list[-literal] = 0
            elif literal in pure_list:
                if pure_list[literal] == 0:
                    continue
            else:
                pure_list[literal] = 1
    return [pure for pure in pure_list if pure_list[pure] == 1]

def dpll(clauses):
    # if Σ contains p v -p then DP(\Σ{p v -p}) (Taut)

    # If Σ = Ø, the sentence is satisfiable (Sat)
    if not clauses:
        return True
    # # if Σ has unit clause {l} then DP(Σ{l = True}) (Empty)
    for clause in clauses:
        if len(clause) == 0:
            return False
    # if Σ has unit clause {l} then DP(Σ{l = True}) (Unit Pr)
    for clause in clauses:
        if len(clause) == 1:
            return unit_propagation(clauses, clause[0])
    # if Σ has pure literal l then DP(Σ{l = True}) (Pure) --> SKIP
    # for pure_literal in find_pure_literals(clauses):
    #     return unit_propagation(clauses, pure_literal)


c = parse_cnf("sudoku1.cnf")
print(dpll(c))





