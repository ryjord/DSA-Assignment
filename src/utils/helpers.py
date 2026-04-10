# Libs
import json
import time
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
matplotlib.use("Agg")

# Classes
from classes.models import Customer, VRPInstance

# Load Test Case
def load_test_case(filepath: str):
    try:
        with open(filepath, "r") as test_cases:
            data = json.load(test_cases)

        # Initialise
        demands = data["demands"]
        customers = []

        # Load Customers & Assign Coordinates for visualisation (Note : ask lecturer if i need it to be visual, personally i think it helps my point)
        for i, demand in enumerate(demands):
            cust = Customer(customer_id=i, demand=demand)

            # Use Coordinates
            if "coordinates" in data:
                cust.x_coordinate = data["coordinates"][i][0]
                cust.y_coordinate = data["coordinates"][i][1]
            else:
                # Origin
                if i == 0:
                    cust.x_coordinate = 50.0
                    cust.y_coordinate = 50.0
                else:
                    # Geometric Falback
                    angle = (2 * math.pi * i) / (len(demands) - 1)
                    cust.x_coordinate = 50.0 + 40.0 * math.cos(angle)
                    cust.y_coordinate = 50.0 + 40.0 * math.sin(angle)

            customers.append(cust)

        return VRPInstance(
            customers=customers,
            distance_matrix=data["distance_matrix"],
            vehicle_capacity=data["vehicle_capacity"],
            num_vehicles=data["num_vehicles"],
        )

    # Error Handling
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as error:
        print(f"[load_test_case] Failed to load '{filepath}': {error}")
        return None

# Obeys VPR Constraint check
def validate_solution(solution: dict, demands: list, vehicle_capacity: int, num_customers: int) -> dict:
    errors = []
    routes = solution.get("routes", [])
    visited = set()

    # Route Check
    for index, route in enumerate(routes):
        # Every route must start and end at the depot
        if not route or route[0] != 0 or route[-1] != 0:
            errors.append(f"Route {index}: must start and end at depot (0).")
            continue
        route_demand = 0

        # Node Check
        for node in route[1:-1]:
            # Depot should not appear in the middle of a route
            if node == 0:
                errors.append(f"Route {index}: depot appears mid-route.")
                continue

            # A customer can only be visited once across all routes
            if node in visited:
                errors.append(f"Route {index}: customer {node} visited more than once.")

            visited.add(node)
            route_demand += demands[node]

        # Total Demand has to be less than capacity
        if route_demand > vehicle_capacity:
            errors.append(f"Route {index}: demand {route_demand} exceeds capacity.")

    # Customers have to be serviced
    missing = set(range(1, num_customers + 1)) - visited
    if missing:
        errors.append(f"Unvisited customers: {sorted(missing)}.")

    return {"valid": len(errors) == 0, "errors": errors}

# terminal solution
def print_solution(solution: dict, label: str = "Solution") -> None:
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}")

    routes = solution.get("routes", [])
    # Prints route path
    for i, route in enumerate(routes):
        print(f"  Route {i + 1:>2}: {' -> '.join(str(n) for n in route)}")

    print(f"  {'─' * 40}")
    print(f"  Total distance: {solution.get('total_distance', 0):.4f}")
    print(f"  Number of routes: {len(routes)}")
    print(f"{'=' * 60}\n")

# Benchmarks multiple algorithms
def run_benchmark(solvers: dict, instance, runs: int = 1) -> list:
    # Initialise
    results = []
    dm = instance.distance_matrix
    demands = instance.demands
    cap = instance.vehicle_capacity

    # Solvers Iterated
    for label, solver_names in solvers.items():
        best_distance = math.inf
        best_solution = None
        total_time = 0.0

        # Indexed Solver Runs
        for _ in range(runs):
            # counter
            start_time = time.perf_counter()
            solution = solver_names(dm, demands, cap)
            end_time = time.perf_counter()

            # Total
            total_time += (end_time - start_time) * 1000

            # Best Solution
            if solution["total_distance"] < best_distance:
                best_distance = solution["total_distance"]
                best_solution = solution

        # Validate
        validity = validate_solution(best_solution, demands, cap, instance.num_customers)

        results.append({
            "solver": label,
            "distance": round(best_distance, 4),
            "time_ms": round(total_time / runs, 3),
            "routes": len(best_solution["routes"]),
            "valid": validity["valid"],
        })

    # Calculate the gap compared to the best algorithm
    best_overall = min(run.get("distance") for run in results)

    for run in results:
        distance = run.get("distance")
        if best_overall and best_overall > 0:
            run["gap"] = (distance - best_overall) / best_overall * 100
        else:
            run["gap"] = 0.0

# benchmark results
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

    # Loops through results and checks validity
    for result in results:
        valid_str = "✓" if results["valid"] else "✗"
        print(
            f" {result['solver']:<30} {result['distance']:>12.4f} {result['gap']:>10.2f} "
            f" {result['time_ms']:>12.3f} {result['routes']:>8} {valid_str:>7}"
        )

    print("=" * 85 + "\n")

# Visualise
def plot_solution(solution: dict, instance, title: str = "VRP Solution", output_path: str = "solution.png") -> None:
    customers = instance.customers
    routes = solution["routes"]

    # Colour palette
    colours = [
        "#e41a1c", "#377eb8", "#4daf4a", "#984ea3",
        "#ff7f00", "#a65628", "#f781bf", "#999999",
    ]
    fig, ax = plt.subplots(figsize=(9, 7))

    # Plot the routing paths
    for route_index, route in enumerate(routes):
        colour = colours[route_index % len(colours)]
        xs = [customers[n].x_coordinate for n in route]
        ys = [customers[n].y_coordinate for n in route]
        ax.plot(xs, ys, "-o", color=colour, linewidth=1.5, markersize=5, zorder=2)

    # Depot location
    depot = customers[0]
    ax.plot(
        depot.x_coordinate, depot.y_coordinate,
        "*", color="black", markersize=14, zorder=4, label="Depot",
    )

    # Customer nodes and ID labels
    for customer in customers[1:]:
        ax.plot(customer.x_coordinate, customer.y_coordinate, "o", color="steelblue", markersize=8, zorder=3)
        # Annotates ID
        ax.annotate(
            str(customer.customer_id),
            (customer.x_coordinate, customer.y_coordinate),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=8,
            zorder=5,
        )

    # Map Colours to Route
    patches = [
        mpatches.Patch(color=colours[i % len(colours)], label=f"Route {i + 1}")
        for i in range(len(routes))
    ]
    patches.insert(0, mpatches.Patch(color="black", label="Depot"))

    # Finalise graph styling
    ax.legend(handles=patches, loc="upper right", fontsize=8)
    ax.set_title(f"{title}\nTotal distance: {solution['total_distance']:.4f}", fontsize=12)
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    ax.grid(True, linestyle="--", alpha=0.4)

    # Save and cleanup
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close(fig)
