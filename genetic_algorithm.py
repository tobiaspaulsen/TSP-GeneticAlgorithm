import numpy as np
import matplotlib.pyplot as plt
import random
import time
from general_tools import *


def initiate_population(size, cities, distances):
    """
    Function that generates a random population
    Args:
        size (int): Population size
        cities: List of all cities to visit
        distances (2d-list): table over distances

    Returns:
        List of tuples containing the random individuals and their distance
    """
    permutations = [list(np.random.permutation(len(cities))) for _ in range(size)]
    return [(tour, measure_distance(tour, distances)) for tour in permutations]


def tournament_selection(population, pop_size, tournament_size=0):
    """
    Function that performs a tournament_selection on the population. Creates
    tournaments of given size and adds the winner of the tournaments in a list.
    Args:
        population (list)
        pop_size (int): Population size
        tournament_size (int): Size of each tournament

    Returns:
        A list with length pop_size containing all the chosen parents
    """
    selected = []
    if tournament_size == 0:
        tournament_size = pop_size // 5  # If size of tournament isn't given it's set to 20% of population size
    for i in range(pop_size):
        tournament = [population[np.random.randint(pop_size)] for _ in range(tournament_size)]
        selected.append(get_best(tournament))
    return selected


def ranked_selection(population, pop_size):
    """
    Function that performs a ranked selection on a population. Gives each
    individual a rank based on fitness and normalizes that rank to choose
    parents for the next generation.
    Args:
        population (list)
        pop_size (int): Population size

    Returns:
        A list with length pop_size containing all the chosen parents
    """
    sorted_pop = sorted(population, key=lambda tup: tup[1], reverse=True)
    ranks = [i for i in range(pop_size)]
    sum_ranks = sum(ranks)
    chances = [i/sum_ranks for i in ranks]
    return [sorted_pop[i] for i in np.random.choice(ranks, pop_size, p=chances)]


def survivor_selection(population, pop_size):
    """
    Function that chooses the survivors of this generation, based on
    (µ+λ)-selection.
    
    Args:
        population (list)
        pop_size (int): Population size

    Returns:
        List of survivors
    """
    population.sort(key=lambda tup: tup[1])
    return population[:pop_size]


def pmx(a, b, start, stop):
    """
    Partial-mapped crossover
    Args:
        a (List):    First parent
        b (List):    Second parent
        start (int): Start index
        stop (int:   End index

    Returns:
        Permutation based on parents
    """
    child = [None] * len(a)
    child[start:stop] = a[start:stop]

    for i, x in enumerate(b[start:stop], start):
        if x not in child:
            while child[i] is not None:
                i = b.index(a[i])
            child[i] = x

    for i in range(len(child)):
        if child[i] is None:
            child[i] = b[i]
    return child


def pmx_pair(a, b):
    """
    Function that creates two children based on parents.
    Args:
        a (List):    First parent
        b (List):    Second parent

    Returns:
        Tuple containing two children as a result of partially-mapped crossover
    """
    start = np.random.randint(0, len(a) // 2)
    stop = start + len(a) // 2
    return pmx(a, b, start, stop), pmx(b, a, start, stop)


def insert_mutation(permutation):
    """
    Function that mutates a given permutation using insertion
    Args:
        permutation (list):

    Returns:
        Mutated permutation where one value is moved to a different index
    """
    i, j = np.random.choice(len(permutation), 2, replace=False)
    permutation.insert(i + 1, permutation.pop(j))
    return permutation


def genetic_algorithm(cities, distances, pop_size, p_mutation, num_gens):
    """
    Implementation of a genetic algorithm to solve TSP.
    Uses ranked- or tournament-selection for parent-selection. Partially-mapped
    crossover for crossover. Insert-mutation for mutation and (µ+λ)-selection
    for survival selection.
    Args:
    cities:                  List of all cities to visit
        distances (2d-list): Table over distances
        pop_size (int):      Population size, should be an even number
        p_mutation (float):  Chance of mutation
        num_gens (int):      Number of generations before termination

    Returns:
        A tuple containing the best individual of the last generation and the
        shortest distance of each generation
    """
    if pop_size % 2 == 1:
        print("Population size must be even numbered")
        return

    best_of_each_gen = []
    population = initiate_population(pop_size, cities, distances)

    for gen_n in range(num_gens-1):
        best_of_each_gen.append(get_best(population)[1])
        # print(f"Gen {gen_n} average: {average_dist(population)}")
        # print(get_best(population)[1])

        # parents = tournament_selection(population, pop_size)
        parents = ranked_selection(population, pop_size)
        offspring = []
        for i in range(0, pop_size, 2):
            offspring.extend(pmx_pair(parents[i][0], parents[i+1][0]))
        for child in offspring:
            if random.random() < p_mutation:
                insert_mutation(child)
            population.append((child, measure_distance(child, distances)))
        population = survivor_selection(population, pop_size)
    best = get_best(population)
    best_of_each_gen.append(best[1])
    return [cities[i] for i in best[0]], best[1], best_of_each_gen


def measure_genetic(number_of_runs, pop_size, num_gens, cities, distances):
    """
    Method that runs the genetic algorithm several times and measures how well it
    does. It calculates the average and standard deviation of all the runs as well
    as it plots the average of each generation
    Args:
        number_of_runs (int)
        pop_size (int): Population size
        num_gens (int): Number of generations
        cities: List of all cities to visit
        distances (2d-list): table over distances
    """
    results = []
    total_dist = 0
    total_time = 0
    generations = []  # Each index is the best of each generation for one of the runs

    for _ in range(number_of_runs):
        start = time.time()
        result = genetic_algorithm(cities, distances, pop_size, 0.5, num_gens)
        stop = time.time()
        total_dist += result[1]
        results.append(result[:2])
        generations.append(result[2])
        total_time += (stop - start)

    print(f"\nResults of genetic algorithm over {number_of_runs} runs")
    print(f"Population: {pop_size}")
    print(f"Number of generations: {num_gens}")
    print(f"Chance of mutations: {50}%")
    print(f"Average time: {total_time/number_of_runs}")
    print_info(results, total_dist, number_of_runs)

    average_of_generations = [0]*num_gens
    for i in range(number_of_runs):
        for j in range(num_gens):
            average_of_generations[j] += generations[i][j]/number_of_runs
    plt.plot(average_of_generations, label=f"Population size: {pop_size}")


def genetic_main():
    """
    Main-method for genetic algorithm and calculations
    """
    cities, distances = read_file("european_cities.csv")
    # genetic_algorithm(cities, distances, 200, 0.5, 100)
    measure_genetic(20, 50, 150, cities, distances)
    print("\n\n\n\n")
    measure_genetic(20, 100, 150, cities, distances)
    print("\n\n\n\n")
    measure_genetic(20, 300, 150, cities, distances)
    plt.title("Genetic algorithm over 150 generations:")
    plt.ylabel("Distance")
    plt.xlabel("Generations")
    plt.legend()
    plt.show()


genetic_main()
