import numpy as np
from plotting_utils.plotting_utils import plot_tour
from general_tools import *

from general_tools import *


def get_neighbors(permutation, distances):
    """
    Function that finds all of a permutations neighbors,
    here the neighbor is defined as a different permutation
    where two of the values are swapped
    Args:
        distances (2d-list): table over distances
        permutation (np.array)

    Returns:
        list of all neighbors
    """
    neighbors = []
    for i in range(len(permutation)):
        for j in range(i+1, len(permutation)):
            neigh = permutation.copy()
            neigh[i], neigh[j] = neigh[j], neigh[i]
            neighbors.append((neigh, measure_distance(neigh, distances)))
    return neighbors


def hill_climbing(cities, distances):
    """
    An implementation of the steepest ascend hill climbing algorithm to find a
    solution to TSP-problem.
    Args:
        cities: List of all cities to visit
        distances (2d-list): table over distances

    Returns:
        A tuple containing the shortest tour found and its distance
    """
    best = np.random.permutation(len(cities))
    best_dist = measure_distance(best, distances)
    neighbor, n_dist = get_best(get_neighbors(best, distances))
    while n_dist < best_dist:
        best = neighbor
        best_dist = n_dist
        neighbor, n_dist = get_best(get_neighbors(best, distances))
    return [cities[i] for i in best], best_dist


def measure_hill_climbing(number_of_runs, cities, distances):
    """
    Runs the hill climbing algorithm n times to measure how well it does
    Args:
        number_of_runs (int)
        cities: List of all cities to visit
        distances (2d-list): table over distances
    """
    results = []
    total_dist = 0

    for _ in range(number_of_runs):
        result = hill_climbing(cities, distances)
        total_dist += result[1]
        results.append(result)

    print(f"\nResults of hill climbing on {len(cities)} cities {number_of_runs} times")
    print_info(results, total_dist, number_of_runs)


def main():
    cities, distances = read_file("european_cities.csv")
    best = hill_climbing(cities, distances)
    plot_tour(best[0], show_map=True)
    print(f"Best:                {'->'.join(best[0])}")
    print(f"Best distance:       {best[1]}")

    #subset_10 = make_subset(cities, distances, 0, 10)
    #measure_hill_climbing(20, *subset_10)
    #print("\n\n\n\n")
    #measure_hill_climbing(20, cities, distances)


if __name__ == '__main__':
    main()

