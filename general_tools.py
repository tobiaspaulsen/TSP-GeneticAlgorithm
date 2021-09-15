import numpy as np


def read_file(csv_file):
    """
    Reads in cities and distances from csv file
    Args:
        csv_file (str): filename

    Returns:
        Tuple containing names of cities and np.array of distances
    """
    cities = np.genfromtxt(csv_file, max_rows=1, dtype=str, delimiter=";")
    distances = np.genfromtxt(csv_file, skip_header=True, dtype=float, delimiter=";")
    return cities, distances


def measure_distance(permutation, distances):
    """
    Measures the distance of the given permutation
    Args:
        permutation (np_array): each number represent a cities index
        distances (2d-list): table over distances between cities

    Returns:
        (int): distance
    """
    distance = 0
    prev = permutation[-1]
    for i in permutation:
        distance += distances[prev][i]
        prev = i
    return distance


def get_best(population):
    """
    Function that finds the tour with the shortest distance
    Args:
        population (List): containing permutations and their distances

    Returns:
        Tuple containing shortest tour, and its distance
    """
    best = None
    best_dist = float("inf")
    for tour, dist in population:
        if dist < best_dist:
            best = tour
            best_dist = dist
    return best, best_dist


def average_dist(population):
    """
    Function that calculates the average distance in a population
    Args:
        population: List

    Returns:
        Average distance of the individuals in the population
    """
    return np.average([i[1] for i in population])


def print_info(results, total_dist, number_of_runs):
    """
    Prints out info based on results
    Args:
        results (List): Containing results of runs, (tour, distance)
        total_dist (float): Sum of all distances
        number_of_runs (int): How many times the algorithm ran
    """
    average = total_dist / number_of_runs
    std = np.std([tup[1] for tup in results])

    best_dist = float("inf")
    worst_dist = 0
    best_tour = worst_tour = None

    for tour, dist in results:
        if dist < best_dist:
            best_tour = tour
            best_dist = dist
        elif dist > worst_dist:
            worst_tour = tour
            worst_dist = dist

    print(f"\nBest:                {'->'.join(best_tour)}")
    print(f"Best distance:       {best_dist}")
    print(f"\nWorst:               {'->'.join(worst_tour)}")
    print(f"Worst distance:      {worst_dist}")
    print(f"\nAverage distance:    {average}")
    print(f"Standard deviation:  {std}")
