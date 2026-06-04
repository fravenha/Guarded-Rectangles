# Guarded-Rectangles
A decision-support system that solves the rectangular partition guarding problem using greedy algorithms, Integer Programming, Constraint Programming, and Dynamic Programming techniques.

Project developed for the Decision Support Methods discipline: A Case Study of the Rectangular Partition Guarding Problem.

## About

This project investigates the problem of determining the minimum number of guards (positioned at vertices) required to monitor a partition of adjacent rectangles. A guard can observe all rectangles incident to its corresponding vertex.

The project addresses two variants of the problem: complete coverage of the partition and coverage restricted to a subset of rectangles. To solve these problems, several approaches were implemented, including *greedy algorithms*, Integer Programming (IP), Constraint Programming (CP), Dynamic Programming (DP), and extensions involving coloring and variable-distance reachability.

## Requirements

The project requires Python, the OR-Tools library, and LaTeX packages for generating PDF visualizations of the results.

```bash
# Python solver dependency
python -m pip install ortools

# System dependencies (Debian/Ubuntu) for PDF rendering
sudo apt install texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
```

## Running the Project

To execute the program and test new instances, run the main script:

```bash
python src/main.py
```

### Interactive Inputs

When the script starts, the terminal will request the following parameters:

* **Number of rectangles (space-separated):** Defines the problem sizes to be generated. Example: `5 10 15 20`
* **Number of instances:** Defines how many different partitions will be generated for each rectangle set. Example: `5`
* **Compute subsets?:** Enter `0` (No) or `1` (Yes).

### Outputs and Results

The program displays a comparison of the solutions found by each method. Example output:

```text
20 RECTANGLES --------
Greedy Verts Solution =  9
Greedy Rects Solution =  9
Greedy Rects and Verts Solution =  9
Greedy Neighbors Solution =  9
IP Solution =  8
Dynamic Programming Solution =  8
* Number of colors by LP =  3
```

At the end of execution, three files are exported to the local directory:

* `output.pdf`: Visual representations of the geometric solutions produced by each algorithm (generated for instances with up to 60 rectangles).
* `resultados_algoritmos.csv`: Spreadsheet containing the number of guards found by each method for every instance.
* `tempos_algoritmos.csv`: Spreadsheet containing the execution time of each evaluated method.
