import json

import util
import os

from statistics import Statistics
from sat import dpll, preprocessing
from heuristics.heuristics import Heuristic


def run_experiments_on_filtered_sudoku(num_givens_threshold):
    heuristics = [Heuristic.BASE, Heuristic.DLCS, Heuristic.DLIS, Heuristic.MOMS, Heuristic.BOHMS]
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


def save_experiment_results(results, num_givens_threshold):
    with open(f"data/experiments/results_{num_givens_threshold}_givens.json", "w+") as file:
        json.dump(results, file, indent=3)


num_givens_threshold = 26
results = run_experiments_on_filtered_sudoku(num_givens_threshold=num_givens_threshold)
save_experiment_results(results, num_givens_threshold)
