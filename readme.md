# VRP Solver — Vehicle Routing Problem Benchmark

Compares three algorithmic approaches to the **Vehicle Routing Problem (VRP)** across benchmark instances ranging from a small worked example to a stressed 120-customer case.

> Originally built for a Data Structures & Algorithms module assignment at Bournemouth University; published here as a standalone benchmarking tool.

## Overview
This project compares the implementation of 3 algorithms against the **Vehicle Routing Problem (VRP)** with varying stressed benchmarks:

| | Algorithm | Type |
| --- | -------------------------------------- | ---------------------------------- |
| 1 | Clarke-Wright Savings | Heuristic (Naive) |
| 2 | Nearest Neighbour + 2-opt | AI Generated Greedy + Local Search |
| 3 | Genetic Algorithm + 2-opt + Relocation | Metaheuristic (Optimised) |

**Constraints**
- Bakery depot delivering to multiple customers using a fleet of identical vans.
- Each route must start and end at the depot.
- Every customer must be visited exactly once.
- No vehicle may exceed its capacity.

## Data Structures
| Structure | Class / Type | Purpose |
| ---------------- | ------------------- | ---------------------------------------------------------------------------- |
| Customer node | `Customer` | Stores `customer_id`, `demand`, `x_coordinate`, `y_coordinate` |
| Vehicle | `Vehicle` | Tracks `current_load` vs `max_capacity`; enforces capacity via `can_carry()` |
| Problem instance | `VRPInstance` | Wraps customers, distance matrix, vehicle capacity, num_vehicles |
| Distance matrix | `list[list[float]]` | n×n adjacency matrix; index `0` = depot |
| Routes | `list[list[int]]` | Each route is a list of node IDs starting and ending at `0` |
| Savings list | `list[tuple]` | Sorted `(savings_value, i, j)` triples used by Clarke-Wright |
| Population | `list[list[int]]` | Flat customer permutations evolved by the Genetic Algorithm |

---

## How to Run

**Requirements**
```bash
pip install -r requirements.txt
```
Python 3.10+ is required

**Run through CLI**
```bash
python3  src/main.py
```
**Prompting**
Upon running the program will ask you this
```
========================================
VRP Algorithm Tester
========================================
[1] Bakery Example (Assignment Brief)
[2] Small — 10 Customers
[3] Medium — 20 Customers
**(and so on)**
...
----------------------------------------
[A] Run All Tests (Comparison Mode)
[V] Visualise All Tests
[Q] Quit
========================================
```
using keyboard enter characters seen in '[x]'.
-  **Numbers** to run all three algorithms on that test case and see routes + benchmark table.
-  **[A]** runs every test case in bulk and prints a comparison table for each.
-  **[V]** runs every test case and saves route visualisation PNGs to `outputs/`. As coordinates are estimated all points will surround the origin with no distance, but show a clear route.

**Output**
Each run prints:
- Route breakdown (e.g. `0 -> 3 -> 4 -> 0`)
- Benchmark table: Distance | Gap (%) | Time (ms) | Routes | Valid ✓/✗
Visualisation PNGs are saved to `outputs/` automatically when using `[V]`.
---

**Test Cases**
All test inputs are JSON files in `src/tests/`. Each file follows this schema:

```json
{
    "label": "Human-readable name",
    "demands": [0, 2, 3, 1, 4, 2, 3],
    "distance_matrix": [[0, 3, 5, ...], ...],
    "vehicle_capacity": 5,
    "num_vehicles": 3,
    "coordinates": [[5,5], [2,7], ...]
}
```
-  `demands[0]` is always the depot (demand = 0)
-  `coordinates` is only used for graph visualisation `v` to convey routing on a graph.

---

## License
All rights reserved — see [LICENSE](LICENSE). Published for portfolio and demonstration purposes only.
