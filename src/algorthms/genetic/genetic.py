# Libs
import random
import logging

# Operators
from .genetic_operators import ( random_permutation, best, crossover, swap, search, relocation, split, total_distance, )

# Logging Setup
logging.basicConfig(level = logging.INFO, format = "%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Meta Heuritstic approach
def run_optimised_solution(
    distance_matrix,
    demands,
    vehicle_capacity,
    population_size=80,
    total_generations=300,
    crossover_probability=0.85,
    mutation_probability=0.15,
    random_seed_value=None,
):
    # Input Validation
    if len(distance_matrix) == 0 or vehicle_capacity <= 0:
        logger.error("Invalid input: Distance matrix empty or capacity <= 0.")
        return { "routes": [], "total_distance": 0.0 }

    number_of_customers = len(distance_matrix) - 1
    if number_of_customers <= 0:
        return { "routes": [[0, 0]], "total_distance": 0.0 }

    if random_seed_value is not None:
        random.seed(random_seed_value)

    customer_id_list = list(range(1, number_of_customers + 1))

    # Evaluate the fitness
    fitness_cache = {}
    def evaluate_fitness(sequence):
        cache_key = tuple(sequence)
        if cache_key not in fitness_cache:
            routes = split(sequence, demands, vehicle_capacity)
            fitness_cache[cache_key] = total_distance(routes, distance_matrix)
        return fitness_cache[cache_key]

    # Initialise the Population with random customer permutations
    population_list = [random_permutation(customer_id_list) for _ in range(population_size)]

    # Identify the initial best performer
    best_overall_sequence = min(population_list, key = evaluate_fitness)
    best_fitness_value = evaluate_fitness(best_overall_sequence)

    # Main Evolution Loop
    for generation_index in range(total_generations):
        # Carry the best solution forward to the next generation
        new_population_list = [best_overall_sequence[:]]

        while len(new_population_list) < population_size:
        #  Pick two parents using tournament competition
            parent_alpha = best(population_list, evaluate_fitness)
            parent_beta = best(population_list, evaluate_fitness)

            # Produce offspring based on probability
            if random.random() < crossover_probability:
                child_alpha, child_beta = crossover(parent_alpha, parent_beta)
            else:
                child_alpha, child_beta = parent_alpha[:], parent_beta[:]

            # Introduce random changes to explore the solution space
            if random.random() < mutation_probability:
                child_alpha = swap(child_alpha)
            if random.random() < mutation_probability:
                child_beta = swap(child_beta)

            new_population_list.extend([child_alpha, child_beta])

        # Update population
        population_list = new_population_list[:population_size]

        # Track the global best
        current_generation_best = min(population_list, key = evaluate_fitness)
        current_generation_fitness = evaluate_fitness(current_generation_best)

        if current_generation_fitness < best_fitness_value:
            best_fitness_value = current_generation_fitness
            best_overall_sequence = current_generation_best[:]

    # Convert the best permutation into actual vehicle routes
    final_decoded_routes = split(best_overall_sequence, demands, vehicle_capacity)

    # Apply local search
    refined_routes = [search(route, distance_matrix) for route in final_decoded_routes]

    # Apply inter-route relocate to further reduce the total distance
    final_optimised_routes = relocation( refined_routes, distance_matrix, demands, vehicle_capacity)

    final_distance_result = total_distance(final_optimised_routes, distance_matrix)

    logger.debug(f"Genetic Algorithm Completed. Best distance: {final_distance_result:.4f}")

    return { "routes": final_optimised_routes, "total_distance": final_distance_result}
