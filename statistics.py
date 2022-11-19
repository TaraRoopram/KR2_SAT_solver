import timeit
import numpy as np
import util


class Statistics:
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
            "Number of BCP applications": 0,
            "Number of pure literals history": [],
            "Pure literal elimination step": 0,
            "Mean number of clauses": 0.,
            "Std. number of clauses": 0.,
            "Mean number of unit clauses": 0.,
            "Std. number of unit clauses": 0.,
            "Mean number of pure literals": 0.,
            "Std. number of pure literals": 0.,
            "Std. rate of change clause frequency": [],
            "Std. rate of change unit clause frequency": [],
            "Total runtime": 0.
        }

        self.start_time = 0
        self.end_time = 0
        self.split_time = 0
        self.unit_propagation_time = 0
        self.backtracking_time = 0

    def set_initial_stats(self, clauses):
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

    def post_process_stats(self):
        self.set_mean_std_number_of_clauses_history()
        self.set_mean_std_number_of_unit_clauses_history()
        self.set_mean_std_number_of_pure_literals_history()
        self.stats["Number of unit clause BCP applications"] = len(self.stats["Number of unit clauses history"])
        self.stats["Pure literal elimination step"] = len(self.stats["Number of pure literals history"])

        self.stats["Std. rate of change clause frequency"] = np.std(
            np.diff(self.stats["Number of clauses history"])
        )

        self.stats["Std. rate of change unit clause frequency"] = np.std(
            np.diff(self.stats["Number of unit clauses history"])
        )

    def set_mean_std_number_of_clauses_history(self):
        mean, std = util.calculate_mean_std(self.stats["Number of clauses history"])
        self.stats["Mean number of clauses"] = mean
        self.stats["Std. number of clauses"] = std

    def set_mean_std_number_of_unit_clauses_history(self):
        mean, std = util.calculate_mean_std(self.stats["Number of unit clauses history"])
        self.stats["Mean number of unit clauses"] = mean
        self.stats["Std. number of unit clauses"] = std

    def set_mean_std_number_of_pure_literals_history(self):
        mean, std = util.calculate_mean_std(self.stats["Number of pure literals history"])
        self.stats["Mean number of pure literals"] = mean
        self.stats["Std. number of pure literals"] = std

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
