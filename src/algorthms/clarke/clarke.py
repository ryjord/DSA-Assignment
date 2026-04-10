# Libs
import logging

# Methods
from .clarke_operators import ( savings, setup_routes, merge_routes, total_distance )

# Logging setup for visibility during execution
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Runs Naive Solution
def run_naive_solution(distance_matrix, demands, vehicle_capacity):
    # Prevent errors with empty data
    if not distance_matrix or vehicle_capacity <= 0:
        logger.error("Invalid input: Distance matrix empty or capacity <= 0.")
        return { "routes": [], "total_distance": 0.0 }

    number_of_nodes = len(distance_matrix)

    # Handle the case where there is only the depot or one customer
    if number_of_nodes <= 1:
        return { "routes": [[0, 0]], "total_distance": 0.0 }

    # Calculate the savings for every possible pair of customers
    savings_list = savings(distance_matrix)

    # Start with the star configurations
    routes_list, customer_to_route_mapping, route_demand_tracker = setup_routes( number_of_nodes, demands )

    # Iterate through the savings list and greedily merge routes
    for savings_value, customer_i, customer_j in savings_list:
        merge_routes( customer_i, customer_j, routes_list, customer_to_route_mapping, route_demand_tracker, vehicle_capacity)

    # Finalise the routes
    final_routes_list = [[0] + individual_route + [0] for individual_route in routes_list]

    # Calculate the final objective value
    total_travel_distance = total_distance(final_routes_list, distance_matrix)
    logger.debug(f"Clarke-Wright Completed. Best distance: {total_travel_distance:.4f}")

    # Return the results in a structured dictionary
    return { "routes": final_routes_list,"total_distance": total_travel_distance }
