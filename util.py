import json

import numpy as np
from heuristics.heuristics import Heuristic


def find_unit_clauses(clauses):
    unit_clauses = filter(lambda c: len(c) == 1, clauses)
    return list(unit_clauses)


def find_pure_literals(clauses):
    pure_literals = []
    literal_count = count_literals(clauses)
    for l, c in literal_count.items():
        if c > 0 and negate(l) not in literal_count:
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
    return -literal


def positive(literal):
    return abs(literal)


def negative(literal):
    return -abs(literal)


def count_literals(clauses):
    literal_count = {}
    for clause in clauses:
        for literal in clause:
            if literal in literal_count:
                literal_count[literal] += 1
            else:
                literal_count[literal] = 1
    return literal_count


def get_random_literal(clauses):
    random_clause = np.random.choice(clauses)
    random_literal_i = np.random.choice(len(random_clause))
    return random_clause[random_literal_i]


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

        return clauses, num_variables


def read_json_file(file):
    with open(file, "r") as file:
        return json.load(file)


def write_json_file(file_name, contents):
    with open(file_name, "w+") as file:
        json.dump(contents, file, indent=3)


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
    return clauses  # , num_vars


def calculate_mean_std(data):
    mean = np.mean(data)
    std = np.std(data)
    return mean, std


def parse_heuristic(input_str):
    match input_str:
        case "-S1":
            return Heuristic.BASE

        case "-S2":
            return Heuristic.DLCS

        case "-S3":
            return Heuristic.DLIS

        case "-S4":
            return Heuristic.MOMS

        case "-S5":
            return Heuristic.BOHMS

def write_file_out(filename, sat, assignment, number_variables):
    '''
        input: -filename - 
        output: dimacs file with truth assignments to all variables (729). -> filename.out
    '''
    output_file = open(f'{filename}.out', 'w')
    if sat:
        print('SAT')
        print(f"File with assignments can be found in the same directory as input file: <{filename}.out>")
        output_file.write(f"p cnf {number_variables} {number_variables}\n")
        for list in assignment:
            dimacs_assignment = f"{list[1]} 0\n"
            output_file.write(dimacs_assignment)
    else:
        output_file.write('')

    output_file.close()