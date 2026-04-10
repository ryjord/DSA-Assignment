# Libs
import random

    # Generates a random permutation for benchmark solution
def random_permutation(customer_identity_list):
    # Clone
    sequence = customer_identity_list[:]
    random.shuffle(sequence)
    return sequence


# Flat list of customers into capacity-aware routes.
def split(customer_sequence, customer_demands, vehicle_capacity):
    # We start with the bakery (0) as the initial departure point
    routes_list = []
    current_route_list = [0]
    current_vehicle_load = 0

    for customer_id in customer_sequence:
        # If Not Full
        if current_vehicle_load + customer_demands[customer_id] <= vehicle_capacity:
            current_route_list.append(customer_id)
            current_vehicle_load += customer_demands[customer_id]
        else:
        # If the van is full
            current_route_list.append(0)
            routes_list.append(current_route_list)
            current_route_list = [0, customer_id]
            current_vehicle_load = customer_demands[customer_id]

    # Ensure the final van returns to the bakery to complete the tour
    current_route_list.append(0)
    routes_list.append(current_route_list)
    return routes_list


# Calculates the total distance travelled by all vehicles combined
def total_distance(routes_list, distance_matrix):
    total_distance_sum = 0.0
    for individual_route in routes_list:
        # Sum the distance
        for index in range(len(individual_route) - 1):
            total_distance_sum += distance_matrix[individual_route[index]][individual_route[index + 1]]
    return total_distance_sum


# Best performing individual
def best(population_list, total, tournament_size = 3):
    # Randomly sample candidates for the tournament
    contestants = random.sample(population_list, min(tournament_size, len(population_list)))

    return min(contestants, key = total)


# Order Crossover method
def crossover(parent_alpha, parent_beta):
    sequence_size = len(parent_alpha)
    if sequence_size < 2:
        return parent_alpha[:], parent_beta[:]

    # Select a random segment to preserve in the child
    start_index, end_index = sorted(random.sample(range(sequence_size), 2))

    def generate_child(primary_parent, secondary_parent):
        # Initialise child
        child_sequence = [None] * sequence_size
        # Copy the selected segment from the first parent
        child_sequence[start_index:end_index + 1] = primary_parent[start_index:end_index + 1]

        # Track which customers are already in the child
        used_customers = set(primary_parent[start_index:end_index + 1])
        fill_position = (end_index + 1) % sequence_size

        # Fill remaining slots
        for customer_id in secondary_parent:
            if customer_id not in used_customers:
                child_sequence[fill_position] = customer_id
                fill_position = (fill_position + 1) % sequence_size
        return child_sequence

    return generate_child(parent_alpha, parent_beta), generate_child(parent_beta, parent_alpha)


# introduce genetic variation
def swap(customer_sequence):
    mutated_sequence = customer_sequence[:]
    if len(mutated_sequence) >= 2:
        index_1, index_2 = random.sample(range(len(mutated_sequence)), 2)
        mutated_sequence[index_1], mutated_sequence[index_2] = mutated_sequence[index_2], mutated_sequence[index_1]
    return mutated_sequence


# A local search heuristic
def search(individual_route, distance_matrix):
    # ignore Routes with 3 nodes
    if len(individual_route) <= 3:
        return individual_route

    current_best_route = individual_route[:]
    was_improved = True

    while was_improved:
        was_improved = False
        for i in range(1, len(current_best_route) - 2):
            for j in range(i + 1, len(current_best_route) - 1):
                # Calculate if reversing the segment reduces the distance
                current_cost = distance_matrix[current_best_route[i - 1]][current_best_route[i]] + \
                            distance_matrix[current_best_route[j]][current_best_route[j + 1]]

                potential_cost = distance_matrix[current_best_route[i - 1]][current_best_route[j]] + \
                                distance_matrix[current_best_route[i]][current_best_route[j + 1]]

                if potential_cost < current_cost - 1e-9:
                    # reverse the segment
                    current_best_route[i:j + 1] = current_best_route[i:j + 1][::-1]
                    was_improved = True

    return current_best_route


# Moves a customer from one van's path to another.
def relocation(routes_list, distance_matrix, customer_demands, vehicle_capacity):
    was_improved = True
    while was_improved:
        was_improved = False
        for route_1_index, route_1 in enumerate(routes_list):
            for route_2_index, route_2 in enumerate(routes_list):
                if route_1_index == route_2_index:
                    continue

                # Calculate current capacity
                route_2_total_load = sum(customer_demands[customer] for customer in route_2)

                for i in range(1, len(route_1) - 1):
                    customer_to_move = route_1[i]

                    # Ensure destination van has enough tray space
                    if route_2_total_load + customer_demands[customer_to_move] > vehicle_capacity:
                        continue

                    for j in range(1, len(route_2)):
                        # Cost reduction if removed from route 1
                        removal_benefit = (distance_matrix[route_1[i - 1]][route_1[i]] +
                                        distance_matrix[route_1[i]][route_1[i + 1]] -
                                        distance_matrix[route_1[i - 1]][route_1[i + 1]])

                        # Additional cost if inserted into route 2
                        insertion_cost = (distance_matrix[route_2[j - 1]][customer_to_move] +
                                        distance_matrix[customer_to_move][route_2[j]] -
                                        distance_matrix[route_2[j - 1]][route_2[j]])

                        if insertion_cost < removal_benefit - 1e-9:
                        # Execute the relocation
                            route_1.pop(i)
                            route_2.insert(j, customer_to_move)
                            was_improved = True
                            break
                    if was_improved: break
                if was_improved: break

    # Remove any routes that became empty
    return [individual_route for individual_route in routes_list if len(individual_route) > 2]
