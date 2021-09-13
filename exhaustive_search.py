import numpy as np
from itertools import permutations
import time
import random
from plotting_utils.plotting_utils import plot_tour
from general_tools import *


def exhaustive_search(cities, distances):
    """
    Runs an exhaustive search to find the best solution of TSP on the given 
    cities. Finds permutation from 1 to the number of cities and adds 0 in front
    afterwords because the same tour can have different start cities.

    Args:
        cities: list of cities to solve
        distances (2d-list): table over distances

    Returns:
        Tuple containing the cities in the shortest order and the
        tours distance.
    """
    #Should use itertools.combinations to save memory
    combinations = permutations(range(1, len(cities)))
    shortest_dist = float("inf")
    best = None
    for comb in combinations:
        permutation = (0,) + comb
        dist = measure_distance(permutation, distances)
        if dist < shortest_dist:
            shortest_dist = dist
            best = permutation
    return [cities[i] for i in best], shortest_dist


def main():
    cities, distances = read_file("european_cities.csv")
    subset = make_subset(cities, distances, 0, 10)

    start = time.time()
    tour, distance = exhaustive_search(*subset)
    search_time = time.time() - start
    print("Shortest tour:          ", " -> ".join(tour), "->")
    print("Distance :              ", distance)
    print("Time to calculate:      ", search_time)

    # Calculate time for all cities:
    fac_10 = np.math.factorial(10)
    fac_24 = np.math.factorial(24)
    
    time_to_calculate_24 = search_time * fac_24 / fac_10
    print("Estimated time for all: ", time_to_calculate_24)


main()
