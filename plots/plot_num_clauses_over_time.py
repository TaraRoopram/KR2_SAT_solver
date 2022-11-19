import matplotlib.pyplot as plt

import util


def plot_num_clauses_over_time(unprocessed_results, file_name):
    results = [data for data in unprocessed_results if data["filename"] == file_name][0]
    base_results = results["base"]["Number of clauses history"]
    dlcs_results = results["dlcs"]["Number of clauses history"]
    dlis_results = results["dlis"]["Number of clauses history"]
    moms_results = results["moms"]["Number of clauses history"]
    bohms_results = results["bohms"]["Number of clauses history"]

    plt.plot(range(1, len(base_results) + 1), base_results, label="Base DPLL")
    plt.plot(range(1, len(dlcs_results) + 1), dlcs_results, label="DLCS")
    plt.plot(range(1, len(dlis_results) + 1), dlis_results, label="DLIS")
    plt.plot(range(1, len(moms_results) + 1), moms_results, label="MOMS")
    plt.plot(range(1, len(bohms_results) + 1), bohms_results, label="Bohms")

    plt.legend(loc="upper right")
    plt.ylabel("Number of clauses after simplification")
    plt.xlabel("Number of simplifications")
    plt.title("Plot showing the number of remaining clauses \n after simplifying per heuristic")
    plt.grid()

    plt.show()


def plot_num_unit_clauses_over_time(unprocessed_results, file_name):
    results = [data for data in unprocessed_results if data["filename"] == file_name][0]
    base_results = results["base"]["Number of unit clauses history"]
    dlcs_results = results["dlcs"]["Number of unit clauses history"]
    dlis_results = results["dlis"]["Number of unit clauses history"]
    moms_results = results["moms"]["Number of unit clauses history"]
    bohms_results = results["bohms"]["Number of unit clauses history"]

    plt.plot(range(1, len(base_results) + 1), base_results, label="Base DPLL")
    plt.plot(range(1, len(dlcs_results) + 1), dlcs_results, label="DLCS")
    plt.plot(range(1, len(dlis_results) + 1), dlis_results, label="DLIS")
    plt.plot(range(1, len(moms_results) + 1), moms_results, label="MOMS")
    plt.plot(range(1, len(bohms_results) + 1), bohms_results, label="Bohms")

    plt.legend(loc="upper right")
    plt.ylabel("Number of unit clauses")
    plt.xlabel("Number of applications of BCP")
    plt.title("Plot showing the number of remaining \n unit clauses after BCP per heuristic")
    plt.grid()

    plt.show()


unprocessed_results = util.read_json_file("../data/experiments/results_26_givens.json")
plot_num_clauses_over_time(unprocessed_results, "dimacs_9x9_1004.cnf")
plot_num_unit_clauses_over_time(unprocessed_results, "dimacs_9x9_1004.cnf")
