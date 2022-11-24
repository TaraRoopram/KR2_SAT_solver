<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://upload.wikimedia.org/wikipedia/commons/d/dc/Dpll11.png" alt="Project logo"></a>
</p>

<h3 align="center">DPLL SAT solver --Sudoku</h3>

---

<p align="center"> Few lines describing your project.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)

## 🧐 About <a name = "about"></a>

Basic SAT solver, with optionally DLCS, DLIS, BOHMS, MOMS heuristics. If the problem is satisfiable one solution is returned.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- python version 3.10 or higher.

### Installing

Clone the repository

```
git clone git@github.com:TaraRoopram/KR2_SAT_solver.git
```

Go into directory

```
cd KR2_SAT_solver/
```

## 🎈 Usage <a name="usage"></a>

Run the SAT solver

```
python sat.py <heuristic_tag> <filename>
```

heuristic_tag:

- -S1 : DPLL basic / no heuristic
- -S2 : DPLL with DLCS heuristic
- -S3 : DPLL with DLIS heuristic
- -S4 : DPLL with MOMS heurstic
- -S5 : DPLL with BOHMS heuristic

filename:

- Enter the filename of the problem in cnf format
- The program automatically adds the .cnf extension
- By default it looks for the file in the root directory

### Example

Example code for running the SAT solver with DLCS heuristic for file 'dimacs_4x4_1.cnf'

```
python sat.py -S4 dimacs_4x4_1
```
