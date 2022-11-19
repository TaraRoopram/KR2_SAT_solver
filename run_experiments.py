import json

import util
import os

from statistics import Statistics, MetaStatistics
from sat import dpll, preprocessing
from heuristics.heuristics import Heuristic


def run_total_experiment(results, heuristics):
    meta_stats = MetaStatistics()
    for heuristic in heuristics:
        results_per_heuristic = [result[heuristic.value] for result in results]
        for i in range(0, len(results_per_heuristic)):
            result = results_per_heuristic[i]
            meta_stats.update_mean(heuristic.value,
                                   "Mean number of givens",
                                   "Number of givens", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of backtracks",
                                   "Number of backtracks", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of initial clauses",
                                   "Number of initial clauses", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of initial unit clauses",
                                   "Number of initial unit clauses", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of initial pure literals",
                                   "Number of initial pure literals", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of clauses after simplification",
                                   "Mean number of clauses", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of remaining unit clauses per BCP application",
                                   "Mean number of unit clauses", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of initial pure literals",
                                   "Number of initial pure literals", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean of the std. rate of change of clause frequency",
                                   "Std. rate of change clause frequency", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean of the std. rate of change of unit clause frequency",
                                   "Std. rate of change unit clause frequency", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of splits",
                                   "Number of splits", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean total runtime",
                                   "Total runtime", result, i + 1)

    return meta_stats


def run_experiments_on_filtered_sudoku(num_givens_threshold, heuristics):
    results_list = []
    for filename in os.scandir("data/dimacs/sudoku/9x9"):
        if filename.is_file():
            clauses = util.read_dimacs_file(f"data/dimacs/sudoku/9x9/{filename.name}")
            temp_stats = Statistics()
            temp_stats.set_number_of_givens(clauses)
            num_givens = temp_stats.stats["Number of givens"]

            if num_givens >= num_givens_threshold:
                print(filename.name)
                results = {"filename": filename.name}
                for heuristic in heuristics:
                    statistics = run_experiment_on_sudoku(clauses, heuristic)
                    results[heuristic.value] = statistics
                results_list.append(results)

    return results_list


def run_experiment_on_sudoku(clauses, heuristic):
    statistics = Statistics()
    statistics.set_initial_stats(clauses)
    assignments = {}

    clauses = preprocessing(clauses)

    statistics.start_timer()
    is_satisfiable = dpll(clauses, assignments, statistics, heuristic, enable_elim_pure_literals=True)
    statistics.stop_timer()

    statistics.post_process_stats()
    return statistics.stats


def read_experiment_results(num_givens_threshold):
    with open(f"data/experiments/results_{num_givens_threshold}_givens.json", "r") as file:
        return json.load(file)


def save_experiment_results(results, num_givens_threshold):
    with open(f"data/experiments/unprocessed/unprocessed_results_{num_givens_threshold}_givens.json", "w+") as file:
        json.dump(results, file, indent=3)


heuristics = [Heuristic.BASE, Heuristic.DLCS, Heuristic.DLIS, Heuristic.MOMS, Heuristic.BOHMS]
num_givens_threshold = 26
results = read_experiment_results(num_givens_threshold)
meta_stats = run_total_experiment(results, heuristics)

with open(f"data/experiments/processed/processed_results_{num_givens_threshold}_givens.json", "w+") as file:
    json.dump(meta_stats.stats, file, indent=3)

# num_givens_threshold = 26
# heuristics = [Heuristic.BASE, Heuristic.DLCS, Heuristic.DLIS, Heuristic.MOMS, Heuristic.BOHMS]
# results = run_experiments_on_filtered_sudoku(num_givens_threshold, heuristics)
# save_experiment_results(results, num_givens_threshold)
