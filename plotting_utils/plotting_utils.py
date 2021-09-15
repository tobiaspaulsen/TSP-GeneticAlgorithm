#Breddegrad, lengdegrad
import numpy as np
import matplotlib.pyplot as plt

city_coordinates_numbered = {   0: (41.3828939, 2.1774322),
                                1: (44.8178131, 20.4568974),
                                2: (52.5170365, 13.3888599),
                                3: (50.8465573, 4.351697),
                                4: (44.4361414, 26.1027202),
                                5: (47.4813896, 19.1460728),
                                6: (55.6867243, 12.5700724),
                                7: (53.3497645, -6.2602732),
                                8: (53.550341, 10.000654),
                                9: (41.0096334, 28.9651646),
                                10: (50.4500336, 30.5241361),
                                11: (51.5073219, -0.1276474),
                                12: (40.4167047, -3.7035825),
                                13: (45.4668, 9.1905),
                                14: (55.7504461, 37.6174943),
                                15: (48.1371079, 11.5753822),
                                16: (48.8566969, 2.3514616),
                                17: (50.0874654, 14.4212535),
                                18: (41.8933203, 12.4829321),
                                19: (59.938732, 30.316229),
                                20: (42.6978634, 23.3221789),
                                21: (59.3251172, 18.0710935),
                                22: (48.2083537, 16.3725042),
                                23: (52.2319581, 21.0067249)}

city_coordinates_names = {  'Barcelona': (41.3828939, 2.1774322),
                            'Belgrade': (44.8178131, 20.4568974),
                            'Berlin': (52.5170365, 13.3888599),
                            'Brussels': (50.8465573, 4.351697),
                            'Bucharest': (44.4361414, 26.1027202),
                            'Budapest': (47.4813896, 19.1460728),
                            'Copenhagen': (55.6867243, 12.5700724),
                            'Dublin': (53.3497645, -6.2602732),
                            'Hamburg': (53.550341, 10.000654),
                            'Istanbul': (41.0096334, 28.9651646),
                            'Kiev': (50.4500336, 30.5241361),
                            'London': (51.5073219, -0.1276474),
                            'Madrid': (40.4167047, -3.7035825),
                            'Milan': (45.4668, 9.1905),
                            'Moscow': (55.7504461, 37.6174943),
                            'Munich': (48.1371079, 11.5753822),
                            'Paris': (48.8566969, 2.3514616),
                            'Prague': (50.0874654, 14.4212535),
                            'Rome': (41.8933203, 12.4829321),
                            'Saint Petersburg': (59.938732, 30.316229),
                            'Sofia': (42.6978634, 23.3221789),
                            'Stockholm': (59.3251172, 18.0710935),
                            'Vienna': (48.2083537, 16.3725042),
                            'Warsaw': (52.2319581, 21.0067249)}


city_names = ['barcelona', 'belgrade', 'berlin', 'brussels', 'bucharest', 'budapest', 'copenhagen', 'dublin', 'hamburg', 'istanbul', 'kiev', 'london', 'madrid', 'milan', 'moscow', 'munich', 'paris', 'prague', 'rome', 'saint petersburg', 'sofia', 'stockholm', 'vienna', 'warsaw']

def plot_tour(tour, show_map = False, figsize = (8, 8), annotate = False):
    """ 
        Creates a plot from the TSP route based om the GPS coordinates of the cities in the tour.
        
        Args: 
            tour: list or array of the order of the cities in the tour, either by their number or name. 
            
        Examples: 
           plot_tour(['Barcelona', 'Belgrade', 'Dublin', 'Barcelona'])
           plot_tour([1, 2, 4, 6, 3, 1])
    """
    if not tour[-1] == tour[0]:
        tour = list(tour)
        tour.append(tour[0])  
        
    if not (type(tour[0]) in (str, int) or isinstance(tour[0], (str, int))):
        try: 
            int(tour[0])
        except:
            print("tour should either contain integers or strings.")
            return

    #Store the coordinates in separate lists 
    if isinstance(tour[0], str):
        try:
            lat = [city_coordinates_names[city.lower().title()][0] for city in tour]
            lng = [city_coordinates_names[city.lower().title()][1] for city in tour]
        except Exception as e: 
            print("Something went wrong:", e)
            return 
    else:
        try:
            lat = [city_coordinates_numbered[int(city)][0] for city in tour]
            lng = [city_coordinates_numbered[int(city)][1] for city in tour]
        except Exception as e:
            print("Something went wrong:", e)
            return 
    
    fig, ax = plt.subplots(figsize = figsize)
    ax.plot(lng, lat)
    ax.scatter(lng[1:-1],lat[1:-1], marker ="o", s = 100, color = "red")
    ax.scatter(lng[0],lat[0], marker ="*", s = 300, color = "darkmagenta")


    if not show_map or annotate:
        color = "red"
        size = 18
        if not show_map:
            color = "black"
            size = 15
        if isinstance(tour[0], str):
            try:
                for i, city_name in enumerate(tour[:-1]):
                    ax.annotate(city_name.capitalize(), np.array((lng[i] +.2, lat[i]+.2)), fontsize = size, color = color)
            except Exception as e:
                print("Something went wrong:", e)
        else:
            try:
                for i, city_number in enumerate(tour[:-1]):
                    ax.annotate(f"{city_names[city_number].capitalize()}", np.array((lng[i] +.2, lat[i]+.2)), fontsize = size, color = color)
            except Exception as e:
                print("Something went wrong:", e)
                return 
    if show_map:
        r = plt.imread("plotting_utils/maps/map.png")
        ax.imshow(r, extent=[-14.56,38.43, 37.697 +0.3 , 64.344 +2.5], aspect = "auto")

    plt.show()
