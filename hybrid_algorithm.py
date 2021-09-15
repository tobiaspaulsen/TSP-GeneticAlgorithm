from genetic_algorithm import *
from hill_climbing import *
from general_tools import *


def hill_climbing(distances, start):
    """
    Function to perform hill climbing from a start permutation
    Args:
        distances: 2D array containing the distances
        start: Start permutation to start hill climbing from

    Returns:
        Tuple containing the local best starting from start
    """
    best, best_dist = start
    neighbor, n_dist = get_best(get_neighbors(best, distances))

    while n_dist < best_dist:
        best = neighbor
        best_dist = n_dist
        neighbor, n_dist = get_best(get_neighbors(best, distances))

    return best, best_dist


def hybrid_algorithm(cities, distances, pop_size, p_mutation, num_gens):
    """
    Algorithm that combines a genetic algorithm with a hill climbing to
    perform a local search for each generation.
    Args:
        cities:              List of all cities to visit
        distances (2d-list): Table over distances
        pop_size (int):      Population size, should be an even number
        p_mutation (float):  Chance of mutation
        num_gens (int):      Number of generations before termination

    Returns:
        A tuple containing the best individual of the last generation and the
        shortest distance of each generation
    """
    population = initiate_population(pop_size, cities, distances)

    for gen_n in range(num_gens):
        # Local search:
        for i in range(pop_size):
            population[i] = hill_climbing(distances, population[i])
        # print(f"Gen {gen_n} average: {average_dist(population)}")
        # print(get_best(population))

        # parents = tournament_selection(population, pop_size)
        parents = ranked_selection(population, pop_size)
        offspring = []
        for i in range(0, pop_size, 2):
            offspring.extend(pmx_pair(parents[i][0], parents[i + 1][0]))

        for child in offspring:
            if random.random() < p_mutation:
                insert_mutation(child)
            population.append((child, measure_distance(child, distances)))

        population = survivor_selection(population, pop_size)

    return get_best(population)


def main():
    cities, distances = read_file("european_cities.csv")
    print(hybrid_algorithm(cities, distances, 50, 0.5, 3))
    # tot_distance = 0
    # for _ in range(100):
    #     _, dist = genetic_algorithm(*subset, 50, 0.8, 80)
    #     tot_distance += dist
    # print(tot_distance/100)


if __name__ == '__main__':
    main()
