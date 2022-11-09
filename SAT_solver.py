# Helpful links
# https://github.com/muneeb706/sudoku-solver/blob/master/basic_sudoku_solver/sudoku-solver.py
# https://users.aalto.fi/~tjunttil/2020-DP-AUT/notes-sat/solving.html
# https://github.com/mxklabs/mxklabs-python/tree/master/mxklabs/dimacs
# https://github.com/DRTooley/PythonSatSolver --> implements three different algorithms incl. dpll
# https://github.com/marcmelis/dpll-sat/blob/master/solvers/base_sat.py

## three different strategies: the DPLL algorithm without any further heuristics and two different heuristics

#1: Read DIMACS input
clauses = []
with open("sudoku1.cnf",'r') as file:
    next(file) #skips first row in file
    for line in file:
        data = line.split()
        clause = [int(x) for x in line[:-2].split()]
        clauses.append(clause)
    print(clauses) # prints clauses as list of lists

#2: Encode Sudoku rules as clauses in DIMACS


#3: Encode a given puzzle in DIMACS


#4: Give (2)+(3) as input to (1) and return the solution to the given puzzle

