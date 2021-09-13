from genetic_algorithm import *
from hill_climbing import *
from general_tools import *

def hill_climbing(cities, distances, start):
    best, best_dist = start
    neighbor, n_dist = get_best(get_neighbors(best, distances))
    while n_dist < best_dist:
        best = neighbor
        best_dist = n_dist
        neighbor, n_dist = get_best(get_neighbors(best, distances))
    return best, best_dist


def hybrid_algorithm(cities, distances, pop_size, p_mutation, num_gens):
    population = initiate_population(pop_size, cities, distances)

    for gen_n in range(num_gens):
        # Local search:
        for i in range(pop_size):
            population[i] = hill_climbing(cities, distances, population[i])
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
    subset = make_subset(cities, distances, 0, 24)
    print(hybrid_algorithm(*subset, 50, 0.5, 3))
    # tot_distance = 0
    # for _ in range(100):
    #     _, dist = genetic_algorithm(*subset, 50, 0.8, 80)
    #     tot_distance += dist
    # print(tot_distance/100)


main()