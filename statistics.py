import timeit
import numpy as np
import util


class MetaStatistics:
    def __init__(self):
        self.stats = {
            "base": self.generate_stats_template(),
            "dlcs": self.generate_stats_template(),
            "dlis": self.generate_stats_template(),
            "moms": self.generate_stats_template(),
            "bohms": self.generate_stats_template()
        }

    def update_mean(self, heuristic, meta_stat_name, stat_name, result, new_size):
        mean = self.stats[heuristic][meta_stat_name]
        new_value = result[stat_name]

        if not np.isnan(mean) and not np.isnan(new_value):
            mean += (new_value - mean) / new_size
            self.stats[heuristic][meta_stat_name] = mean

    def add_value_to_list(self, heuristic, meta_stat_name, value):
        self.stats[heuristic][meta_stat_name].append(value)

    def generate_stats_template(self):
        return {
            "Mean number of givens": 0.,
            "Mean number of backtracks": 0.,
            "Mean number of initial clauses": 0.,
            "Mean number of initial unit clauses": 0.,
            "Mean number of initial pure literals": 0.,
            "Mean number of simplifications": 0.,
            "Mean number of BCP applications": 0.,
            "Mean number of pure literal eliminations": 0.,
            "Mean number of clauses after simplification": 0.,
            "Mean number of remaining unit clauses per BCP application": 0.,
            "Std. number of clauses added or removed": 0.,
            "Mean number of clauses added": 0.,
            "Mean number of clauses removed": 0.,
            "Std. number of unit clauses added or removed": 0.,
            "Mean number of unit clauses added": 0.,
            "Mean number of unit clauses removed": 0.,
            "Mean number of splits": 0.,
            "Mean total runtime": 0.,
            "List total runtime": [],
            "List number of backtracks": [],
            "List number of simplifications": [],
            "List number of BCP applications": [],
            "List mean number of clauses removed": [],
            "List mean clause length": []
        }


class Statistics:
    def __init__(self) -> None:
        self.stats = {
            "Number of givens": 0.,
            "Number of initial clauses": 0.,
            "Number of initial unit clauses": 0.,
            "Number of initial pure literals": 0.,
            "Mean initial clause length": 0.,
            "Number of backtracks": 0.,
            "Number of splits": 0.,
            "Number of clauses history": [],
            "Number of simplifications": 0.,
            "Mean clause length": 0.,
            "Number of unit clauses history": [],
            "Number of BCP applications": 0.,
            "Number of pure literals history": [],
            "Number of pure literal eliminations": 0.,
            "Mean number of clauses": 0.,
            "Std. number of clauses": 0.,
            "Mean number of unit clauses": 0.,
            "Std. number of unit clauses": 0.,
            "Mean number of pure literals": 0.,
            "Std. number of pure literals": 0.,
            "Mean rate of change clause frequency": 0.,
            "Mean pos. rate of change clause frequency": 0.,
            "Mean neg. rate of change clause frequency": 0.,
            "Mean rate of change unit clause frequency": 0.,
            "Mean pos. rate of change unit clause frequency": 0.,
            "Mean neg. rate of change unit clause frequency": 0.,
            "Std. rate of change clause frequency": 0.,
            "Std. pos. rate of change clause frequency": 0.,
            "Std. neg. rate of change clause frequency": 0.,
            "Std. rate of change unit clause frequency": 0.,
            "Std. pos. rate of change unit clause frequency": 0.,
            "Std. neg. rate of change unit clause frequency": 0.,
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
        self.set_mean_clause_length(clauses)
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

    def set_mean_clause_length(self, clauses):
        mean = np.mean([len(clause) for clause in clauses])
        self.stats["Mean initial clause length"] = mean

    def inc_num_backtracks(self):
        if self.stats["Number of backtracks"] is None:
            self.stats["Number of backtracks"] = 1
        else:
            self.stats["Number of backtracks"] += 1

    def inc_num_splits(self):
        if self.stats["Number of splits"] is None:
            self.stats["Number of splits"] = 1
        else:
            self.stats["Number of splits"] += 1

    def update_number_of_clauses_history(self, num_clauses):
        self.stats["Number of clauses history"].append(num_clauses)

    def update_mean_clause_length(self, clauses):
        self.stats["Mean clause length"] = np.mean([len(clause) for clause in clauses])

    def update_number_of_unit_clauses_history(self, num_unit_clauses):
        self.stats["Number of unit clauses history"].append(num_unit_clauses)

    def update_number_of_pure_literals_history(self, num_pure_literals):
        self.stats["Number of pure literals history"].append(num_pure_literals)

    def post_process_stats(self):
        self.set_mean_std_number_of_clauses_history()
        self.set_mean_std_number_of_unit_clauses_history()
        self.set_mean_std_number_of_pure_literals_history()
        self.stats["Number of simplifications"] = len(self.stats["Number of clauses history"])-1
        self.stats["Number of BCP applications"] = len(self.stats["Number of unit clauses history"])-1
        self.stats["Number of pure literal eliminations"] = len(self.stats["Number of pure literals history"])-1

        clause_history = self.stats["Number of clauses history"]
        diff_clause_freq = np.diff(clause_history)
        pos_diff_clause_freq = [diff for diff in diff_clause_freq if diff > 0]
        # print([diff for diff in diff_clause_freq if diff > 0])
        neg_diff_clause_freq = [abs(diff) for diff in diff_clause_freq if diff < 0]
        # print([abs(diff) for diff in diff_clause_freq if diff < 0])
        self.stats["Mean rate of change clause frequency"] = np.mean(diff_clause_freq)
        self.stats["Mean pos. rate of change clause frequency"] = np.mean(pos_diff_clause_freq)
        self.stats["Mean neg. rate of change clause frequency"] = np.mean(neg_diff_clause_freq)
        self.stats["Std. rate of change clause frequency"] = np.std(diff_clause_freq)
        self.stats["Std. pos. rate of change clause frequency"] = np.std(pos_diff_clause_freq)
        self.stats["Std. neg. rate of change clause frequency"] = np.std(neg_diff_clause_freq)

        unit_clause_history = self.stats["Number of unit clauses history"]
        diff_unit_clause_freq = np.diff(unit_clause_history)
        pos_diff_unit_clause_freq = [diff for diff in diff_unit_clause_freq if diff > 0]
        neg_diff_unit_clause_freq = [abs(diff) for diff in diff_unit_clause_freq if diff < 0]
        self.stats["Mean rate of change unit clause frequency"] = np.mean(diff_unit_clause_freq)
        self.stats["Mean pos. rate of change unit clause frequency"] = np.mean(pos_diff_unit_clause_freq)
        self.stats["Mean neg. rate of change unit clause frequency"] = np.mean(neg_diff_unit_clause_freq)
        self.stats["Std. rate of change unit clause frequency"] = np.std(diff_unit_clause_freq)
        self.stats["Std. pos. rate of change unit clause frequency"] = np.std(pos_diff_unit_clause_freq)
        self.stats["Std. neg. rate of change unit clause frequency"] = np.std(neg_diff_unit_clause_freq)

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
