import numpy as np
from itertools import permutations
import time
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
    shortest_dist = float("inf")
    best = None
    for comb in permutations(range(1, len(cities))):
        permutation = (0,) + comb
        dist = measure_distance(permutation, distances)
        if dist < shortest_dist:
            shortest_dist = dist
            best = permutation
    return [cities[i] for i in best], shortest_dist


def main():
    cities, distances = read_file("european_cities.csv")
    sub_cities = cities[0:10]
    sub_distances = distances[0:10, 0:10]

    start = time.time()
    tour, distance = exhaustive_search(sub_cities, sub_distances)
    search_time = time.time() - start
    print(f"Shortest tour:                                 {' -> '.join(tour)} ->")
    print(f"Distance :                                     {distance}")
    print(f"Time to calculate:                             {search_time} s")

    # Calculate time for all cities:
    fac_10 = np.math.factorial(10)
    fac_24 = np.math.factorial(24)
    
    time_to_calculate_24 = search_time * fac_24 / fac_10
    print(f"Estimated time for all based on time for 10:   {time_to_calculate_24} s")


if __name__ == '__main__':
    main()
