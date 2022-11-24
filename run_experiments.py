import json

import numpy as np

import util
import os

from statistics import Statistics, MetaStatistics
from SAT import dpll, preprocessing
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
                                   "Mean number of simplifications",
                                   "Number of simplifications", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of BCP applications",
                                   "Number of BCP applications", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of pure literal eliminations",
                                   "Number of pure literal eliminations", result, i + 1)

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
                                   "Std. number of clauses added or removed",
                                   "Std. rate of change clause frequency", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of clauses added",
                                   "Mean pos. rate of change clause frequency", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of clauses removed",
                                   "Mean neg. rate of change clause frequency", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Std. number of unit clauses added or removed",
                                   "Std. rate of change unit clause frequency", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of unit clauses added",
                                   "Mean pos. rate of change unit clause frequency", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of unit clauses removed",
                                   "Mean neg. rate of change unit clause frequency", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean number of splits",
                                   "Number of splits", result, i + 1)

            meta_stats.update_mean(heuristic.value,
                                   "Mean total runtime",
                                   "Total runtime", result, i + 1)

            meta_stats.add_value_to_list(heuristic.value,
                                         "List total runtime",
                                         result["Total runtime"])

            meta_stats.add_value_to_list(heuristic.value,
                                         "List number of backtracks",
                                         result["Number of backtracks"])

            meta_stats.add_value_to_list(heuristic.value,
                                         "List number of simplifications",
                                         result["Number of simplifications"])

            meta_stats.add_value_to_list(heuristic.value,
                                         "List number of BCP applications",
                                         result["Number of BCP applications"])

            meta_stats.add_value_to_list(heuristic.value,
                                         "List mean number of clauses removed",
                                         result["Mean neg. rate of change clause frequency"])

    return meta_stats


def filter_sudokus_num_givens(num_givens_threshold):
    filtered = []
    for filename in os.scandir("data/dimacs/sudoku/9x9"):
        if filename.is_file():
            clauses = util.read_dimacs_file(
                f"data/dimacs/sudoku/9x9/{filename.name}")
            temp_stats = Statistics()
            temp_stats.set_number_of_givens(clauses)
            num_givens = temp_stats.stats["Number of givens"]

            if num_givens >= num_givens_threshold:
                filtered.append(filename.name)

    return filtered


def run_experiments_on_filtered_sudoku(num_givens_threshold, heuristics):
    results_list = []
    for filename in os.scandir("data/dimacs/sudoku/9x9"):
        if filename.is_file():
            clauses = util.read_dimacs_file(
                f"data/dimacs/sudoku/9x9/{filename.name}")
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
    is_satisfiable = dpll(clauses, assignments, statistics,
                          heuristic, enable_elim_pure_literals=True)
    statistics.stop_timer()

    statistics.post_process_stats()
    return statistics.stats


def run_experiment_on_list_statistics(heuristics, results):
    keys = ["total runtime", "number of backtracks", "number of simplifications", "number of BCP applications",
            "mean number of clauses removed"]
    results_dict = {}
    for heuristic in heuristics:
        results_dict[heuristic.value] = {}

        for key in keys:
            results_dict[heuristic.value][key] = {}
            result = results[heuristic.value][f"List {key}"]

            results_dict[heuristic.value][key][f"Mean {key}"] = float(
                np.mean(result))
            results_dict[heuristic.value][key][f"Std. {key}"] = float(
                np.std(result))
            results_dict[heuristic.value][key][f"Max {key}"] = float(
                np.max(result))
            results_dict[heuristic.value][key][f"Min {key}"] = float(
                np.min(result))
            results_dict[heuristic.value][key][f"Range {key}"] = float(
                np.max(result) - np.min(result))

    util.write_json_file(
        "data/experiments/final/final_results_26_givens.json", results_dict)


def read_experiment_results(num_givens_threshold):
    with open(f"data/experiments/unprocessed/unprocessed_results_{num_givens_threshold}_givens.json", "r") as file:
        return json.load(file)


def save_experiment_results(results, num_givens_threshold):
    with open(f"data/experiments/unprocessed/unprocessed_results_{num_givens_threshold}_givens.json", "w+") as file:
        json.dump(results, file, indent=3)


# num_givens_threshold = 27
# results = read_experiment_results(num_givens_threshold)
# meta_stats = run_total_experiment(results, heuristics)
#
# with open(f"data/experiments/processed/processed_results_{num_givens_threshold}_givens_v2.json", "w+") as file:
#     json.dump(meta_stats.stats, file, indent=3)
num_givens_threshold = 27
heuristics = [Heuristic.BASE, Heuristic.DLCS,
              Heuristic.DLIS, Heuristic.MOMS, Heuristic.BOHMS]
results = run_experiments_on_filtered_sudoku(num_givens_threshold, heuristics)
save_experiment_results(results, num_givens_threshold)

# heuristics = [Heuristic.BASE, Heuristic.DLCS, Heuristic.DLIS, Heuristic.MOMS, Heuristic.BOHMS]
# results = util.read_json_file("data/experiments/processed/processed_results_27_givens_v2.json")
# run_experiment_on_list_statistics(heuristics, results)
