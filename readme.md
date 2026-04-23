## Vehicle Routing Problem: DSA Assignment
**Data Structures Assignment Deadline:** Tuesday 5 May 2026

## Overview
This Project compares the implementation of 3 algorithms against the **Vehicle Routing Problem (VRP)** with varying stressed benchmarks:

| # | Algorithm | Type |
| --- | -------------------------------------- | ---------------------------------- |
| 1 | Clarke-Wright Savings | Heuristic (Naive) |
| 2 | Nearest Neighbour + 2-opt | AI Generated Greedy + Local Search |
| 3 | Genetic Algorithm + 2-opt + Relocation | Metaheuristic (Optimised) |

**Contraints**
- Bakery depot delivering to multiple cafés using a fleet of identical vans.
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
## Algorithms
**1. Clarke-Wright** - Naive Approach
**File:** `algorthms/clarke/`
This approach starts with every customer on a dedicated route calculates the saving from merging any two routes. Savings are sorted descending and then greedily applied, The validity is tested when:

- Customer `i` is at the **end** of its route and customer `j` is at the **start**
- The combined demand doesnt exceed the vehicle capacity, `Vehicle.can_carry()`
Implements enhanced endpoint merging as described by Stanojević, Stanojević & Vujošević (2013).

---
**2. Nearest Neighbour + 2-opt** - AI-Generated Solution
**File:** `algorthms/nearest/nearest.py`

>  **This solution was generated with the assistance of AI, Anthropic & Gemini.**
> The exact prompt used is included in the file header of `nearest.py`.

**Phase 1 — Generation:** Attached content of existing code to Gemini and provided context on what the code does and what the assignment requires from the AI generated solution.
**Phase 2 — Improvement:** After the AI model was implemented, the use of Anthropic is utilised to help debug and apply the code of Nearest to correctly utilise the classes and methods of VRPInstance.
**Phase 3 — Cleanup:** Utilised AI once more to modify minor changes when updated external code

---

**3. Genetic Algorithm + 2-opt + Relocation** - Optimised Approach
**File:** `algorthms/genetic/`
A population control implementation, which requires changing the customers permutations by using the fitness functions to determine the best possible routes.

**Key components:**
| Component | Implementation | Notes |
| -------------- | --------------------------------------- | ------------------------------------------------- |
| Initialisation | `random_permutation()` | Random shuffles of all customer IDs |
| Fitness | `total_distance()` on `split()` routes | Cached via dict for performance |
| Selection | Tournament selection (`best()`, size=3) | Avoids fitness-proportionate bias |
| Crossover | Order Crossover / OX (`crossover()`) | Preserves relative order; 85% probability |
| Mutation | Swap mutation (`swap()`) | Randomly exchanges two positions; 15% probability |
| Elitism | Best individual carried forward | Prevents regression between generations |
| Local search | `search()` — intra-route 2-opt | Applied post-evolution to each route |
| Inter-route | `relocation()` — customer relocation | Moves customers between routes if beneficial |

**Default parameters:**
- population = 80
- generations = 300

---
## How to Run

**Requirements**
```bash
pip  install  matplotlib
```
Python 3.10+ is required

**Run through CLI**
```bash
python  main.py
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
All test inputs are JSON files in `tests/`. Each file follows this schema:

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

## Solution Validation
Every solution is automatically validated against all VRP constraints via `validate_solution()` in `helpers.py`:

- Every route starts and ends at depot (`0`)
- Depot does not appear mid-route
- Every customer visited exactly once
- Route demand does not exceed vehicle capacity
Results are shown in the benchmark table as `Valid ✓` or `✗` with error details.


## References

Clarke, G., & Wright, J. W. (1964). Scheduling of vehicles from a central depot to a number of delivery points. _Operations Research, 12_(4), 568–581.

Nazif, H., & Lee, L. S. (2012). Optimised crossover genetic algorithm for capacitated vehicle routing problem. _Applied Mathematical Modelling, 36_(5), 2110–2117.

Ozsoydan, F. B., & Sipahioglu, A. (2013). Heuristic solution approaches for the cumulative capacitated vehicle routing problem. _Optimization, 62_(10), 1321–1340.

Simensen, M., Hasle, G., & Stålhane, M. (2022). Combining hybrid genetic search with ruin-and-recreate for solving the capacitated vehicle routing problem. _Journal of Heuristics, 28_(5-6), 653–697.

Stanojević, M., Stanojević, B., & Vujošević, M. (2013). Enhanced savings calculation and its applications for solving capacitated vehicle routing problem. _Applied Mathematics and Computation, 219_(20), 10302–10312.