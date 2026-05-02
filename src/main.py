# Libs
import sys
import os

# Classes
from classes.models import Customer, VRPInstance

# Utils
from utils.helpers import print_solution, run_benchmark, print_benchmark_table, plot_solution, plot_comparative_analysis
from test import interactive_cli

# Algorithms
from algorthms.clarke.clarke import run_naive_solution
from algorthms.nearest.nearest import run_ai_solution
from algorthms.genetic.genetic import run_optimised_solution

# Builds Instance
def _build_bakery_instance() -> VRPInstance:
    # node demands
    demands = [0, 2, 3, 1, 4, 2, 3]
    customers = []

    # Populate node with demands
    for i in range(7):
        customers.append(Customer(customer_id=i, demand=demands[i]))

    coords = [(5, 5), (2, 7), (1, 4), (3, 2), (6, 1), (8, 3), (9, 6)]

    # Assign coordinates to customers
    for i, (x, y) in enumerate(coords):
        customers[i].x_coordinate = float(x)
        customers[i].y_coordinate = float(y)

    # Distance Matrix
    distance_matrix = [
        [0, 3, 5, 4, 6, 7, 8],
        [3, 0, 2, 6, 4, 5, 7],
        [5, 2, 0, 3, 5, 6, 4],
        [4, 6, 3, 0, 2, 5, 6],
        [6, 4, 5, 2, 0, 3, 4],
        [7, 5, 6, 5, 3, 0, 2],
        [8, 7, 4, 6, 4, 2, 0],
    ]

    return VRPInstance(
        customers=customers,
        distance_matrix=distance_matrix,
        vehicle_capacity=5,
        num_vehicles=3,
    )

# Executes all algorithms
def _solve_instance(instance: VRPInstance, label: str = "", output_dir: str = "outputs", hide_details: bool = False) -> None:
    # Path to save results
    routes_dir = os.path.join(output_dir, "routes")
    comp_dir = os.path.join(output_dir, "comparative")

    # Create dirs
    os.makedirs(routes_dir, exist_ok=True)
    os.makedirs(comp_dir, exist_ok=True)

    # Algorithms
    Algorithms = {
        "Clarke-Wright (Naive)": run_naive_solution,
        "Nearest Neighbour + 2-opt (AI)": run_ai_solution,
        "Genetic Algorithm": run_optimised_solution,
    }

    # Render the block header
    if not hide_details:
        print(f"\n{'=' * 65}")
        print(f"  Instance: {label or 'Unknown'}")
        print(f"  Customers: {instance.num_customers}  |  Capacity: {instance.vehicle_capacity}")
        print(f"{'=' * 65}")
    solutions = {}

    # Execute Algorithms
    for Algorithm_label, Algorithm_name in Algorithms.items():
        solution = Algorithm_name(instance.distance_matrix, instance.demands, instance.vehicle_capacity)
        solutions[Algorithm_label] = solution

        # Store solution
        if not hide_details:
            print_solution(solution, label=Algorithm_label)

    # Run benchmarking
    results = run_benchmark(Algorithms, instance, runs=5)

    # Comparative Chart
    if results is not None and not hide_details:
        print_benchmark_table(results)

        plot_comparative_analysis(results, label, comp_dir)
    # Visualise plot
    for Algorithm_label, solution in solutions.items():
        safe_name = (
            f"{(label or 'instance').replace(' ', '_')}__"
            f"{Algorithm_label.replace(' ', '_').replace('/', '-')}.png"
        )

        # Store plot
        plot_solution(
            solution,
            instance,
            title=f"{label} — {Algorithm_label}",
            output_path=os.path.join(routes_dir, safe_name)
        )

# Executes the CLI
def main() -> None:
    try:
        interactive_cli(_build_bakery_instance, _solve_instance)
    except KeyboardInterrupt:
        print("\nExecution interrupted by user...Exiting")

# Main
if __name__ == "__main__":
    main()