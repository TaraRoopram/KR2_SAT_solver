# experiments 
# Hypothesis:
# how does the number of givens influence performance and runtime of an algorithm?
# performance = number of backtracks, number of splits, run/solving time
import time

# How do various SAT solving heuristics perform when applied to 9x9 sudokos?

# What are the strengths and weaknesses of various SAT solving heuristics when applied to 9x9 sudoku's?
#    - number of clauses over time
#    - average clause length over time
#    - number of literals over time
#    - ratio of positive to negative literals

def runtime():
    #start time of function
    start = time.time()

    # below, add functions for which we need to find out the runtime


    #end time of function
    end = time.time()

    # runtime --> depends on CPU but we can make relative comparisons
    print("Execution time of the program is: ", end - start, 'seconds')

#runtime()

class Experiments:
    def __init__(self) -> None:
        self.stats = {
            "Number of backtracks": 0,
            "Number of splits": 0,
            "Number of clauses history": 0, 
            "Number of unit clauses history": 0,
            "Number of pure literals history": 0
        }


    def set_number_of_givens(self, clauses):
        givens = list(filter(lambda c: len(c) == 1, clauses))
        self.stats["Number of givens"] = len(givens)


    def set_number_of_initial_clauses(self, num_initial_clauses):
        self.stats["Number of initial clauses"] = num_initial_clauses
    

    def set_number_of_unit_clauses(self, num_unit_clauses):
        self.stats["Number of unit clauses"] = num_unit_clauses
    

    def set_number_of_pure_literals(self, num_pure_literals):
        self.stats["Number of pure literals"] = num_pure_literals


    def inc_num_backtracks(self):
        self.stats["Number of backtracks"] += 1


    def inc_num_splits(self):
        self.stats["Number of splits"] += 1


    def update_number_of_clauses_history(self, num_clauses):
        self.stats["Number of clauses history"].append(num_clauses)


    def update_number_of_unit_clauses_history(self, num_unit_clauses):
        self.stats["Number of unit clauses history"].append(num_unit_clauses)


    def update_number_of_unit_clauses_history(self, num_pure_literals):
        self.stats["Number of pure literals history"].append(num_pure_literals)

#1 dpll (no heuristic) 
#2 dpll (with DLCS)
#3 dpll (with DLIS)
#4 dpll (with MOMS)
#5 dpll (with BOHMS)

# runtime, number of backtracks, number of splits, number of intial clauses, 
# number of clauses over time, number of unit clauses over time, number of pure literals over time


    # https://github.com/sgomber/CDCL-SAT/blob/master/SAT.py
    # https://www.scitepress.org/Papers/2022/109102/109102.pdf