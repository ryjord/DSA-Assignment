# Libs
from classes.models import Vehicle


# Calculates the potential savings for merging any two customers.
def savings(distance_matrix):
    # Total number of nodes
    number_of_nodes = len(distance_matrix)
    savings_list = []

    # Iterate through each pair of customers to find the best merge options
    for customer_1 in range(1, number_of_nodes):
        for customer_2 in range(customer_1 + 1, number_of_nodes):
            savings_value = (
                distance_matrix[0][customer_1] +
                distance_matrix[0][customer_2] -
                distance_matrix[customer_1][customer_2]
            )
            savings_list.append((savings_value, customer_1, customer_2))
    # Sort the savings in descending order so we pick the best ones first
    savings_list.sort(key=lambda entry: entry[0], reverse=True)

    return savings_list


# Sets up the starting state where every customer has their own dedicated route.
def setup_routes(number_of_nodes, demands, vehicle_capacity):
    # Each customer begins on an individual route (star configuration)
    routes_list = [[index] for index in range(1, number_of_nodes)]

    # Map each customer to their current route list for fast lookup

    # Map each customer to their current route index for safe, stable lookup
    customer_to_route_index = {customer_id: customer_id - 1 for customer_id in range(1, number_of_nodes)}

    # Build a Vehicle per route to track capacity explicitly
    route_vehicles = []
    for route in routes_list:
        vehicle = Vehicle(vehicle_id=len(route_vehicles), max_capacity=vehicle_capacity)
        vehicle.load(demands[route[0]])
        route_vehicles.append(vehicle)

    return routes_list, customer_to_route_index, route_vehicles


# Only merge two routes if endpoints align and vehicle capacity is not exceeded.
def merge_routes(
    customer_i,
    customer_j,
    routes_list,
    customer_to_route_index,
    route_vehicles,
    vehicle_capacity,
    demands,
):
    index_i = customer_to_route_index.get(customer_i)
    index_j = customer_to_route_index.get(customer_j)

    # Both routes must exist and must not already be the same route
    if index_i is None or index_j is None:
        return
    if index_i == index_j:
        return

    route_i = routes_list[index_i]
    route_j = routes_list[index_j]
    vehicle_i = route_vehicles[index_i]
    vehicle_j = route_vehicles[index_j]

    # A merge is only valid if the customers are at the connection endpoints
    is_customer_i_at_end = route_i[-1] == customer_i
    is_customer_j_at_start = route_j[0] == customer_j

    if not (is_customer_i_at_end and is_customer_j_at_start):
        # Check the reverse orientation
        is_customer_j_at_end = route_j[-1] == customer_j
        is_customer_i_at_start = route_i[0] == customer_i

        if is_customer_j_at_end and is_customer_i_at_start:
            # Swap to use the primary merge direction
            route_i, route_j = route_j, route_i
            vehicle_i, vehicle_j = vehicle_j, vehicle_i
            index_i, index_j = index_j, index_i
        else:
            return

    # Check if the combined demand exceeds the fixed vehicle capacity
    if not vehicle_i.can_carry(vehicle_j.current_load):
        return

    # Execute the merge
    route_i.extend(route_j)
    vehicle_i.load(vehicle_j.current_load)

    # Update mapping for all customers
    for customer_node in route_j:
        customer_to_route_index[customer_node] = index_i

    # remove the old route and update the demand tracker
    route_j.clear()
    route_vehicles[index_j] = None


# Simple utility to sum up the costs of the final route paths.
def total_distance(routes_list, distance_matrix):
    total_travel_distance = 0.0
    for route in routes_list:
        # Distance from depot to first customer
        total_travel_distance += distance_matrix[0][route[0]]

        # Distances between consecutive customers in the route
        for edge_index in range(len(route) - 1):
            total_travel_distance += distance_matrix[route[edge_index]][route[edge_index + 1]]

        # Distance from last customer back to depot
        total_travel_distance += distance_matrix[route[-1]][0]

    return total_travel_distance
