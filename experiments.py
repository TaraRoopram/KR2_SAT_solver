# experiments 
# Hypothese:
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

runtime()

class Experiments:
    def __init__(self) -> None:
        self.stats = {}


    def get_number_of_givens(self, clauses):
        givens = list(filter(lambda c: len(c) == 1, clauses))
        self.stats["Number of givens"] = len(givens)

    
    def inc_num_backtracks(self):
        if not self.stats["Number of backtracks"]:
            self.stats["Number of backtracks"] = 0
        else:
            self.stats["Number of backtracks"] += 1


    def inc_num_splits(self):
        pass




    
    # https://www.scitepress.org/Papers/2022/109102/109102.pdf