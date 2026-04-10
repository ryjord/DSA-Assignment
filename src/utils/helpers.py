# Libs
import json
import time
import math

# Classes
from classes.models import Customer, VRPInstance


# --- Core Utils ---

# Loads a JSON test file and converts it into a VRPInstance
def load_test_case(filepath: str):
    try:
        with open(filepath, "r") as fh:
            data = json.load(fh)

        demands = data["demands"]
        customers = [
            Customer(customer_id=i, demand=demands[i])
            for i in range(len(demands))
        ]

        return VRPInstance(
            customers=customers,
            distance_matrix=data["distance_matrix"],
            vehicle_capacity=data["vehicle_capacity"],
            num_vehicles=data["num_vehicles"],
        )
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as error:
        print(f"[load_test_case] Failed to load '{filepath}': {error}")
        return None

# Validates if the given routing solution is logically valid
def validate_solution(solution: dict, demands: list, vehicle_capacity: int, num_customers: int) -> dict:
    errors = []
    routes = solution.get("routes", [])
    visited = set()

    for idx, route in enumerate(routes):
        if not route or route[0] != 0 or route[-1] != 0:
            errors.append(f"Route {idx}: must start and end at depot (0).")
            continue

        route_demand = 0
        for node in route[1:-1]:
            if node == 0:
                errors.append(f"Route {idx}: depot appears mid-route.")
                continue
            if node in visited:
                errors.append(f"Route {idx}: customer {node} visited more than once.")
            visited.add(node)
            route_demand += demands[node]

        if route_demand > vehicle_capacity:
            errors.append(f"Route {idx}: demand {route_demand} exceeds capacity.")

    missing = set(range(1, num_customers + 1)) - visited
    if missing:
        errors.append(f"Unvisited customers: {sorted(missing)}.")

    return {"valid": len(errors) == 0, "errors": errors}

# Formats and prints the routing solution visually to the terminal
def print_solution(solution: dict, label: str = "Solution") -> None:
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}")
    routes = solution.get("routes", [])
    for i, route in enumerate(routes):
        print(f"  Route {i + 1:>2}: {' -> '.join(str(n) for n in route)}")
    print(f"  {'─' * 40}")
    print(f"  Total distance : {solution.get('total_distance', 0):.4f}")
    print(f"  Number of routes: {len(routes)}")
    print(f"{'=' * 60}\n")


# --- Benchmarking ---

# Executes performance benchmarks for multiple solvers
def run_benchmark(solvers: dict, instance, runs: int = 1) -> list:
    results = []
    dm = instance.distance_matrix
    demands = instance.demands
    cap = instance.vehicle_capacity

    for label, solver_fn in solvers.items():
        best_distance = math.inf
        best_solution = None
        total_time = 0.0

        for _ in range(runs):
            t0 = time.perf_counter()
            sol = solver_fn(dm, demands, cap)
            t1 = time.perf_counter()
            total_time += (t1 - t0) * 1000

            if sol["total_distance"] < best_distance:
                best_distance = sol["total_distance"]
                best_solution = sol

        validity = validate_solution(best_solution, demands, cap, instance.num_customers)

        results.append({
            "solver": label,
            "distance": round(best_distance, 4),
            "time_ms": round(total_time / runs, 3),
            "routes": len(best_solution["routes"]),
            "valid": validity["valid"],
        })

    best_overall = min(r["distance"] for r in results)
    for r in results:
        r["gap"] = (r["distance"] - best_overall) / best_overall * 100 if best_overall > 0 else 0.0

    return results

# Formats and prints the benchmark results in an organized table
def print_benchmark_table(results: list) -> None:
    header = (
        f"{'Solver':<30} {'Distance':>12} {'Gap (%)':>10} "
        f"{'Time (ms)':>12} {'Routes':>8} {'Valid':>7}"
    )
    print("\n" + "=" * 85)
    print("  Benchmark Results")
    print("=" * 85)
    print(f"  {header}")
    print(f"  {'─' * 81}")

    for r in results:
        valid_str = "✓" if r["valid"] else "✗"
        print(
            f"  {r['solver']:<30} {r['distance']:>12.4f} {r['gap']:>10.2f} "
            f"{r['time_ms']:>12.3f} {r['routes']:>8} {valid_str:>7}"
        )
    print("=" * 85 + "\n")


# --- Visualisation ---

# Conditional rendering setup to prevent crash on missing libraries
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# Generates and saves a graph plot detailing the routing solution
def plot_solution(solution: dict, instance, title: str = "VRP Solution", output_path: str = "solution.png") -> None:
    if not MATPLOTLIB_AVAILABLE:
        print(f"Skipping visualization for '{title}' - matplotlib is not installed.")
        return

    customers = instance.customers
    routes = solution["routes"]
    colours = [
        "#e41a1c", "#377eb8", "#4daf4a", "#984ea3",
        "#ff7f00", "#a65628", "#f781bf", "#999999",
    ]

    fig, ax = plt.subplots(figsize=(9, 7))

    for r_idx, route in enumerate(routes):
        colour = colours[r_idx % len(colours)]
        xs = [customers[n].x_coordinate for n in route]
        ys = [customers[n].y_coordinate for n in route]
        ax.plot(xs, ys, "-o", color=colour, linewidth=1.5, markersize=5, zorder=2)

    depot = customers[0]
    ax.plot(
        depot.x_coordinate, depot.y_coordinate,
        "*", color="black", markersize=14, zorder=4, label="Depot",
    )

    for c in customers[1:]:
        ax.plot(c.x_coordinate, c.y_coordinate, "o", color="steelblue", markersize=8, zorder=3)
        ax.annotate(
            str(c.customer_id),
            (c.x_coordinate, c.y_coordinate),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=8,
            zorder=5,
        )

    patches = [
        mpatches.Patch(color=colours[i % len(colours)], label=f"Route {i + 1}")
        for i in range(len(routes))
    ]
    patches.insert(0, mpatches.Patch(color="black", label="Depot"))

    ax.legend(handles=patches, loc="upper right", fontsize=8)
    ax.set_title(f"{title}\nTotal distance: {solution['total_distance']:.4f}", fontsize=12)
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    ax.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close(fig)
