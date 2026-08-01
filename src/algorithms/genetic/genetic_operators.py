# Libs
import random

# Classes
from classes.models import Vehicle

# Generates a random permutation
def random_permutation(customer_identity_list):
    # Clone
    sequence = customer_identity_list[:]
    random.shuffle(sequence)
    return sequence


# Flat list of customers into capacity-aware routes
def split(customer_sequence, customer_demands, vehicle_capacity):
    # Start with the depot
    routes_list = []
    current_route_list = [0]
    current_vehicle = Vehicle(vehicle_id=0, max_capacity=vehicle_capacity)

    for customer_id in customer_sequence:
        # If Not Full
        if current_vehicle.can_carry(customer_demands[customer_id]):
            # Add customer to route & update vehicle load
            current_route_list.append(customer_id)
            current_vehicle.load(customer_demands[customer_id])
        else:
        # If the van is full
            current_route_list.append(0)
            routes_list.append(current_route_list)
            # Reset vehicle
            current_route_list = [0, customer_id]
            current_vehicle = Vehicle(vehicle_id=len(routes_list), max_capacity=vehicle_capacity)
            current_vehicle.load(customer_demands[customer_id])

    # Ensure the final van returns to the depot to complete the tour
    current_route_list.append(0)
    routes_list.append(current_route_list)
    return routes_list


# Calculates the total distance travelled by all vehicles
def total_distance(routes_list, distance_matrix):
    total_distance_sum = 0.0
    for individual_route in routes_list:
        # Sum the distance of the route
        for index in range(len(individual_route) - 1):
            total_distance_sum += distance_matrix[individual_route[index]][individual_route[index + 1]]
    return total_distance_sum


# Best performing individual
def best(population_list, total, tournament_size = 3):
    # Randomly sample candidates for the tournament
    contestants = random.sample(population_list, min(tournament_size, len(population_list)))

    return min(contestants, key = total)


# Order Crossover
def crossover(parent_alpha, parent_beta):
    sequence_size = len(parent_alpha)

    # Handle edge case of very short sequences
    if sequence_size < 2:
        return parent_alpha[:], parent_beta[:]

    # Select a random segment to preserve in the child
    start_index, end_index = sorted(random.sample(range(sequence_size), 2))

    def generate_child(primary_parent, secondary_parent):
        # Initialise child with None placeholders
        child_sequence = [None] * sequence_size
        # Copy the selected segment from the first parent
        child_sequence[start_index:end_index + 1] = primary_parent[start_index:end_index + 1]

        # Identify which customers are already in the child
        used_customers = set(primary_parent[start_index:end_index + 1])
        # Determine the starting position for filling the remaining slots
        fill_position = (end_index + 1) % sequence_size

        # Iterate through the second parent to fill the remaining slots
        for customer_id in secondary_parent:
            if customer_id not in used_customers:
                # Insert unused customer into child
                child_sequence[fill_position] = customer_id
                fill_position = (fill_position + 1) % sequence_size
        return child_sequence

    return generate_child(parent_alpha, parent_beta), generate_child(parent_beta, parent_alpha)


# introduce genetic variations
def swap(customer_sequence):
    mutated_sequence = customer_sequence[:]

    # Handle edge case of very short sequences
    if len(mutated_sequence) >= 2:
        # Randomly select for sawp
        index_1, index_2 = random.sample(range(len(mutated_sequence)), 2)
        mutated_sequence[index_1], mutated_sequence[index_2] = mutated_sequence[index_2], mutated_sequence[index_1]
    return mutated_sequence


# Performs a 2-opt local search to improve a single route
def search(individual_route, distance_matrix):
    # ignore Routes with 3 nodes
    if len(individual_route) <= 3:
        return individual_route

    # Initialise the best route
    current_best_route = individual_route[:]
    # Flag to track improvements
    was_improved = True

    # Continues until no improvements
    while was_improved:
        was_improved = False
        # Define the range of indices to check for potential swaps
        for i in range(1, len(current_best_route) - 2):
            for j in range(i + 1, len(current_best_route) - 1):

                # Cost of removing edges
                current_cost = (distance_matrix[current_best_route[i - 1]][current_best_route[i]] +
                                distance_matrix[current_best_route[j]][current_best_route[j + 1]])

                # New cost if edges are added
                potential_cost = (distance_matrix[current_best_route[i - 1]][current_best_route[j]] +
                                distance_matrix[current_best_route[i]][current_best_route[j + 1]])

                # If cost is lower, perform the swap
                if potential_cost < current_cost - 1e-9:
                    # reverse the segment
                    current_best_route[i:j + 1] = current_best_route[i:j + 1][::-1]
                    was_improved = True

    return current_best_route


# Moves a customer from one route to another
def relocation(routes_list, distance_matrix, customer_demands, vehicle_capacity):
    was_improved = True

    while was_improved:
        was_improved = False
        # Loops through routes
        for route_1_index, route_1 in enumerate(routes_list):
            for route_2_index, route_2 in enumerate(routes_list):
                if route_1_index == route_2_index:
                    continue

                # Build a Vehicle representing the destination route for capacity checks
                route_2_vehicle = Vehicle(vehicle_id=route_2_index, max_capacity=vehicle_capacity)
                # Update the van capacity with customers
                for customer in route_2[1:-1]:
                    route_2_vehicle.load(customer_demands[customer])

                # Loops through customers
                for i in range(1, len(route_1) - 1):
                    customer_to_move = route_1[i]

                    # Check if destination van has enough tray space
                    if not route_2_vehicle.can_carry(customer_demands[customer_to_move]):
                        continue

                    for j in range(1, len(route_2)):
                        # Cost reduction if customer is removed from route 1
                        removal_benefit = (distance_matrix[route_1[i - 1]][route_1[i]] + distance_matrix[route_1[i]][route_1[i + 1]] - distance_matrix[route_1[i - 1]][route_1[i + 1]])

                        # Additional cost if customer is inserted into route 2
                        insertion_cost = (distance_matrix[route_2[j - 1]][customer_to_move] + distance_matrix[customer_to_move][route_2[j]] - distance_matrix[route_2[j - 1]][route_2[j]])

                        if insertion_cost < removal_benefit - 1e-9:
                            # Move customer from route 1 to route 2
                            route_1.pop(i)
                            route_2.insert(j, customer_to_move)
                            was_improved = True
                            break
                    if was_improved:
                        break
                if was_improved:
                    break

    # Remove any routes that became empty
    return [individual_route for individual_route in routes_list if len(individual_route) > 2]
