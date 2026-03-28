
# Calculates the potential savings for merging any two customers.
def compute_savings(distance_matrix):
    # Total number of nodes
    number_of_nodes = len(distance_matrix)
    savings_list = []

    # Iterate through each pair of customers to find the best merge options
    for customer_1 in range(1, number_of_nodes):
        for customer_2 in range(customer_1 + 1, number_of_nodes):
            savings_value = distance_matrix[0][customer_1] + distance_matrix[0][customer_2] - distance_matrix[customer_1][customer_2]
            savings_list.append((savings_value, customer_1, customer_2))
    # Sort the savings in descending order so we pick the best ones first
    savings_list.sort(key=lambda entry: entry[0], reverse=True)

    return savings_list


# Sets up the starting state where every customer has their own van.
def initialize_routes(number_of_nodes, demands):
    # Start with individual routes for each customer
    routes_list = [[index] for index in range(1, number_of_nodes)]

    # Map each customer to their current route list for fast lookup
    customer_to_route_mapping = { customer_id: routes_list[customer_id - 1] for customer_id in range(1, number_of_nodes) }

    # Track the current demand load of each route object
    route_demand_tracker = { id(individual_route): demands[individual_route[0]] for individual_route in routes_list }

    return routes_list, customer_to_route_mapping, route_demand_tracker


    # Only merge if they are at the end of routes and vehicle capacity is not exceeded.
def merge_routes(customer_i, customer_j, routes_list, customer_to_route_mapping, route_demand_tracker, vehicle_capacity):
    route_i = customer_to_route_mapping.get(customer_i)
    route_j = customer_to_route_mapping.get(customer_j)

    # Exist and already in the same route?
    if route_i is None or route_j is None or route_i is route_j:
        return

    # A merge is only possible if the customers are at the connection points
    is_customer_i_at_end = route_i[-1] == customer_i
    is_customer_j_at_start = route_j[0] == customer_j

    if not (is_customer_i_at_end and is_customer_j_at_start):
        # Check the reverse orientation
        is_customer_j_at_end = route_j[-1] == customer_j
        is_customer_i_at_start = route_i[0] == customer_i

        if is_customer_j_at_end and is_customer_i_at_start:
        # Swap variables to use the primary merge logic
            route_i, route_j = route_j, route_i
            customer_i, customer_j = customer_j, customer_i
        else:
            return

    # Check if the combined demand exceeds the fixed vehicle capacity
    combined_route_demand = route_demand_tracker[id(route_i)] + route_demand_tracker[id(route_j)]
    if combined_route_demand > vehicle_capacity:
        return

    # Execute the merge
    route_i.extend(route_j)

    # Update mapping for all customers
    for customer_node in route_j:
        customer_to_route_mapping[customer_node] = route_i

    # remove the old route and update the demand tracker
    routes_list.remove(route_j)
    route_demand_tracker[id(route_i)] = combined_route_demand


    # Simple utility to sum up the costs of the final route paths.
def calculate_total_distance(routes_list, distance_matrix):
    total_travel_distance = 0.0
    for route in routes_list:
        # Distance from depot to first customer [cite: 9]
        total_travel_distance += distance_matrix[0][route[0]]

        # Distances between each customer in the route
        for edge_index in range(len(route) - 1):
            total_travel_distance += distance_matrix[route[edge_index]][route[edge_index + 1]]

        # Distance from last customer back to depot [cite: 9]
        total_travel_distance += distance_matrix[route[-1]][0]

    return total_travel_distance
