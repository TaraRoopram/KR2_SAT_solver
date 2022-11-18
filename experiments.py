import json
import timeit
# import numpy as np
import util


class Experiments:
    def __init__(self) -> None:
        self.stats = {
            "Number of givens": 0,
            "Number of initial clauses": 0,
            "Number of initial unit clauses": 0,
            "Number of initial pure literals": 0,
            "Number of backtracks": 0,
            "Number of splits": 0,
            "Number of clauses history": [],
            "Number of unit clauses history": [],
            "Number of pure literals history": [],
            "Average number of clauses": 0.,
            "Standard deviation number of clauses": 0.,
            "Average number of unit clauses": 0.,
            "Average number of pure literals": 0.,
            "Total runtime": 0.
        }

        self.start_time = 0
        self.end_time = 0
        self.split_time = 0
        self.unit_propagation_time = 0
        self.backtracking_time = 0


    def set_initial_conditions(self, clauses):
        initial_number_of_clauses = len(clauses)
        initial_number_of_unit_clauses = len(util.find_unit_clauses(clauses))
        initial_number_of_pure_literals = len(util.find_pure_literals(clauses))

        self.set_number_of_givens(clauses)
        self.set_number_of_initial_clauses(initial_number_of_clauses)
        self.set_number_of_unit_clauses(initial_number_of_unit_clauses)
        self.set_number_of_pure_literals(initial_number_of_pure_literals)
        self.update_number_of_clauses_history(initial_number_of_clauses)
        self.update_number_of_unit_clauses_history(initial_number_of_unit_clauses)
        self.update_number_of_pure_literals_history(initial_number_of_pure_literals)


    def set_number_of_givens(self, clauses):
        givens = list(filter(lambda c: len(c) == 1, clauses))
        self.stats["Number of givens"] = len(givens)

    def set_number_of_initial_clauses(self, num_initial_clauses):
        self.stats["Number of initial clauses"] = num_initial_clauses

    def set_number_of_unit_clauses(self, num_unit_clauses):
        self.stats["Number of initial unit clauses"] = num_unit_clauses

    def set_number_of_pure_literals(self, num_pure_literals):
        self.stats["Number of initial pure literals"] = num_pure_literals

    def inc_num_backtracks(self):
        self.stats["Number of backtracks"] += 1

    def inc_num_splits(self):
        self.stats["Number of splits"] += 1

    def update_number_of_clauses_history(self, num_clauses):
        self.stats["Number of clauses history"].append(num_clauses)

    def update_number_of_unit_clauses_history(self, num_unit_clauses):
        self.stats["Number of unit clauses history"].append(num_unit_clauses)

    def update_number_of_pure_literals_history(self, num_pure_literals):
        self.stats["Number of pure literals history"].append(num_pure_literals)

    def process_statistics(self):
        pass

    def mean_std_number_of_clauses_history(self, stat_name):
        # mean = np.mean(self.stats[stat_name])
        # std = np.std(self.stats[stat_name])

        # self.stats["Average number of clauses"] = mean
        # self.stats["Standard deviation number of clauses"] = std
        pass


    def start_timer(self):
        self.start_time = timeit.default_timer()

    def stop_timer(self):
        end_time = timeit.default_timer()
        self.end_time = end_time
        self.stats["Total runtime"] = end_time - self.start_time

    def to_string(self):
        stats_string = "\nSTATISTICS\n"
        for stat, value in self.stats.items():
            stats_string += f"{stat}: {value}\n"

        return stats_string


# 1 dpll (no heuristic)
# 2 dpll (with DLCS)
# 3 dpll (with DLIS)
# 4 dpll (with MOMS)
# 5 dpll (with BOHMS)

# runtime, number of backtracks, number of splits, number of intial clauses, 
# number of clauses over time, number of unit clauses over time, number of pure literals over time


# https://github.com/sgomber/CDCL-SAT/blob/master/SAT.py
# https://www.scitepress.org/Papers/2022/109102/109102.pdf
