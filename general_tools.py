import numpy as np


def read_file(csv_file):
    # Should use np.genfromtxt

    """
    Reads in cities and distances from csv file
    Args:
        csv_file (str): filename

    Returns:
        Tuple containing cities on index 0 and distances on index 1
    """
    distances = []
    with open(csv_file) as f:
        cities = f.readline().split(";")
        cities[-1] = cities[-1].strip()
        for line in f:
            distances.append([float(n) for n in line.split(";")])
    return cities, distances
    """distances = np.genfromtxt("european_cities.csv", dtype=None, names=True, delimiter=";")
    cities = distances.dtype.names"""
    return cities, distances


def make_subset(cities, distances, start, stop):
    """
    Makes a subset of input
    Args:
        cities: list of cities to make subset
        distances (2d-list): input table over distances between cities
        start (int): start index
        stop (int): stop index

    Returns:
        Tuple containing subset
    """
    sub_cities = cities[start: stop]
    sub_distances = distances[start: stop]
    for i in range(len(sub_distances)):
        sub_distances[i] = sub_distances[i][start: stop]

    return sub_cities, sub_distances


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
    tot = 0
    for i in population:
        tot += i[1]
    return tot/len(population)


def standard_deviation(values, avg):
    """
    Calculates the standard deviation of given values.
    Args:
        values (List): containing numbers
        avg (float): the average

    Returns:
        standard deviation (float)
    """
    tot_squared_dev = 0
    for val in values:
        tot_squared_dev += (val - avg)**2
    return (tot_squared_dev / len(values))**0.5


def print_info(results, total_dist, number_of_runs):
    """
    Prints out info based on results
    Args:
        results (List): Containing results of runs, (tour, distance)
        total_dist (float): Sum of all distances
        number_of_runs (int): How many times the algorithm ran
    """
    average = total_dist / number_of_runs
    sd = standard_deviation([tup[1] for tup in results], average)

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

    print(f"\nBest: {'->'.join(best_tour)}")
    print(f"Best distance: {best_dist}")
    print(f"\nWorst: {'->'.join(worst_tour)}")
    print(f"Worst distance: {worst_dist}")
    print(f"\nAverage distance: {average}")
    print(f"Standard deviation: {sd}")
