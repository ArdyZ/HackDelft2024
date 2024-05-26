import random
import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import functools
import requests
import operator

INT_MAX = 100000000000
# Number of cities in TSP
NUM_LOCATIONS = 25

# Initial population size for the algorithm
POP_SIZE = 30

# Vehicles
NUM_BIKES = 2
NUM_CARS = 1

BIKE_CAPACITY = 20
CAR_PENALTY = 1.20 # Percentage penalty for using a car

NUM_GENERATIONS = 100000

NUM_VEHICLES = NUM_BIKES + NUM_CARS

# Structure of a GNOME
# defines the path traversed
# by the salesman while the fitness value
# of the path is stored in an integer

def create_distance_matrix():
    return [[-1 for _ in range(NUM_LOCATIONS)] for _ in range(NUM_LOCATIONS)]

def create_ewi_distances(max_range=100):
    return [-1 for _ in range(NUM_LOCATIONS)]

BIKE_TIME_MATRIX = create_distance_matrix()
CAR_TIME_MATRIX = create_distance_matrix()

BIKE_TIME_EWI = create_ewi_distances()
CAR_TIME_EWI = create_ewi_distances()

class individual:
    def __init__(self) -> None:
        self.gnome = [""] * NUM_VEHICLES
        self.fitness = 0

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __eq__(self, other):
        return self.gnome == other.gnome

    def __hash__(self):
        return hash(str(self.gnome))

# Function to return a random number
# from start and end
def rand_num(start, end):
    return random.randint(start, end-1)


# Function to check if the character
# has already occurred in the string
def repeat(s, ch):
    for i in range(len(s)):
        if s[i] == ch:
            return True

    return False


# Function to return a mutated GNOME
# Mutated GNOME is a string
# with a random interchange
# of two genes to create variation in species
def mutate_gnome(gnome):
    gnome = copy.deepcopy(gnome)
    mutation_type = rand_num(0, 2) # 0 is change route, 1 is change vehicle
    if mutation_type == 0:
        return mutate_gnome_route(gnome)
    else:
        return mutate_gnome_vehicle(gnome)

# Change the order of two destinations within one vehicle
def mutate_gnome_route(gnome):
    all_vehs = np.arange(0, NUM_VEHICLES)
    legal_vehs = []
    for veh in all_vehs:
        if len(gnome[veh]) >= 2:
            legal_vehs.append(veh)
    random.shuffle(legal_vehs)
    if len(legal_vehs) == 0:
        return mutate_gnome_vehicle(gnome) # If for some reason there's no legal vehicles for a swap, move an addresss between vehicles instead
    vehicle = legal_vehs[0]
    gnome_v = gnome[vehicle][:]

    while True:
        r = rand_num(0, len(gnome_v))
        r1 = rand_num(0, len(gnome_v))
        if r1 != r:
            temp = gnome_v[r]
            gnome_v[r] = gnome_v[r1]
            gnome_v[r1] = temp
            break
    gnome[vehicle] = gnome_v
    return gnome

# Take a random address from one vehicle to a random other one
def mutate_gnome_vehicle(gnome):
    all_vehs = np.arange(0, NUM_VEHICLES)
    legal_source_vehs = []
    for veh in all_vehs:
        if len(gnome[veh]) != 0:
            legal_source_vehs.append(veh)
    random.shuffle(legal_source_vehs)
    source_v = legal_source_vehs[0]

    np.delete(all_vehs, source_v)
    np.random.shuffle(all_vehs)
    dest_v = all_vehs[1]

    moved_location = gnome[source_v][rand_num(0, len(gnome[source_v]))]
    gnome[source_v].remove(moved_location)

    if len(gnome[dest_v]) == 0:
        gnome[dest_v] = [moved_location]
    else:
        insert_in = rand_num(0, len(gnome[dest_v]))
        gnome[dest_v].insert(insert_in, moved_location)

    return gnome


# Function to return a valid GNOME string
# required to create the population
def create_gnome():
    gnome = []

    for _ in range(NUM_VEHICLES):
        gnome.append([])

    for i in range(NUM_LOCATIONS):
        chosen_vehicle = rand_num(0, NUM_VEHICLES)
        gnome[chosen_vehicle].append(i)

    for i in range(len(gnome)):
        random.shuffle(gnome[i])

    return gnome

def ewi_distance(place, vehicle):
    # Integrate real data
    # return (BIKE_TIME_EWI[place], CAR_TIME_EWI[place])
    if vehicle == 0:
        if BIKE_TIME_EWI[place] != -1:
            return BIKE_TIME_EWI[place]
    else:
        if CAR_TIME_EWI[place] != -1:
            return CAR_TIME_EWI[place]

    requrl = "http://localhost:3000/api/distanceEwi?b={}&type={}".format(place + 1, "cycling" if vehicle == 0 else "driving")
    distance = requests.get(requrl).json()["distance"]

    if vehicle == 0:
        BIKE_TIME_EWI[place] = distance
    else:
        CAR_TIME_EWI[place] = distance

    return distance


def get_addresses_cost(start, end, vehicle):
    if vehicle == 0:
        if BIKE_TIME_MATRIX[start][end] != -1:
            return BIKE_TIME_MATRIX[start][end]
    else:
        if CAR_TIME_MATRIX[start][end] != -1:
            return CAR_TIME_MATRIX[start][end]

    requrl = "http://localhost:3000/api/distance?a={}&b={}&type={}".format(start + 1, end + 1, "cycling" if vehicle == 0 else "driving")
    distance = requests.get(requrl).json()["distance"]

    if vehicle == 0:
        BIKE_TIME_MATRIX[start][end] = distance
    else:
        CAR_TIME_MATRIX[start][end] = distance

    return distance

    # return (BIKE_TIME_MATRIX[start][end], CAR_TIME_MATRIX[start][end])

def gnome_offspring(partner1, partner2):
    structure_of_child = [len(x) for x in partner1]

    partner1 = functools.reduce(operator.iconcat, partner1, [])
    partner2 = functools.reduce(operator.iconcat, partner2, [])

    cutoff_point = rand_num(1, len(partner1) - 1)

    unstructured_child = []

    for i, current_address in enumerate(partner1):
        if i <= cutoff_point:
            unstructured_child.append(current_address)

            # in partner2, swap index of current_address with i
            location_of_current_address_in_p2 = partner2.index(current_address)
            partner2[i], partner2[location_of_current_address_in_p2] = partner2[location_of_current_address_in_p2], partner2[i]
        else:
            unstructured_child.append(partner2[i])

    structured_child = []
    for veh in structure_of_child:
        structured_child.append([])
        for _ in range(veh):
            structured_child[-1].append(unstructured_child[0])
            unstructured_child = unstructured_child[1:]

    return structured_child

# Function to return the fitness value of a gnome.
# The fitness value is the path length
# of the path represented by the GNOME.
def cal_fitness(gnome):
    f = 0
    for veh in range(NUM_VEHICLES):
        # print(veh, 0 if veh < NUM_BIKES else 1)
        cur_fitness = fitness_one_vehicle(gnome[veh], 0 if veh < NUM_BIKES else 1)
        if cur_fitness == INT_MAX:
            return INT_MAX
        f += cur_fitness
    return f

def fitness_one_vehicle(partial_gnome, vehicle_type):
    if len(partial_gnome) == 0:
        return 0
    if vehicle_type == 0 and len(partial_gnome) > BIKE_CAPACITY:
        return INT_MAX
    f = ewi_distance(partial_gnome[0], vehicle_type) + ewi_distance(partial_gnome[-1], vehicle_type)
    # print(partial_gnome)
    for i in range(len(partial_gnome) - 1):
        f += get_addresses_cost(partial_gnome[i], partial_gnome[i + 1], vehicle_type)

    if vehicle_type == 1:
        f *= CAR_PENALTY
    return f

def RunMaCHazineTSP():
    # Generation Number
    gen = 1
    population = []

    best_fitness_over_time = []

    # Populating the gnome pool.
    for i in range(POP_SIZE):
        temp = individual()
        temp.gnome = create_gnome()
        temp.fitness = cal_fitness(temp.gnome)
        population.append(temp)

    population.sort()
    #
    # print("\nInitial population: \nGNOME     FITNESS VALUE\n")
    # for i in range(POP_SIZE):
    #     print(population[i].gnome, population[i].fitness)
    # print()

    while gen <= NUM_GENERATIONS:
        new_population = population[0:int(POP_SIZE/5)] # elitism on best 20% of gnomes
        suitible_population = population[0:int(POP_SIZE/5)*2] # select best 40% for cross-over
        # suitible_population = population[:]
        # gnome_offspring(population[0].gnome, population[1].gnome)
        random.shuffle(suitible_population)
        suitible_population.insert(0, population[0])
        suitible_population.insert(1, population[1])

        for i in range(len(suitible_population) - 1):
            child1 = individual()
            child1.gnome = gnome_offspring(suitible_population[i].gnome, suitible_population[i+1].gnome)
            child1.fitness = cal_fitness(child1.gnome)
            new_population.append(child1)
            child2 = individual()
            child2.gnome = gnome_offspring(suitible_population[i+1].gnome, suitible_population[i].gnome)
            child2.fitness = cal_fitness(child2.gnome)
            new_population.append(child2)


        mutation_population = new_population.copy()
        for position, breeding_gnome in enumerate(population):
            nr_of_mutations = max(1, len(population) - position - POP_SIZE + int(POP_SIZE/5))
            for mut in range(nr_of_mutations):
                mutated = mutate_gnome(breeding_gnome.gnome)
                new_gnome = individual()
                new_gnome.gnome = mutated
                new_gnome.fitness = cal_fitness(mutated)
                new_population.append(new_gnome)


        population = new_population
        population = list(set(population))
        while len(population) < POP_SIZE:
            temp = individual()
            temp.gnome = create_gnome()
            temp.fitness = cal_fitness(temp.gnome)
            population.append(temp)
        population.sort()
        population = population[:POP_SIZE]

        best_fitness = population[0].fitness
        best_fitness_over_time.append(best_fitness)

        if gen % 100 == 0:
            printobj = {}
            printobj["distance"] = best_fitness
            printobj["route"] = population[0].gnome
            print(printobj)

            if gen > 500:
                if abs(best_fitness - best_fitness_over_time[gen-500]) < 1:
                    print("convergence!")
                    return
            # print("\nGeneration", gen, "Best Fitness", best_fitness)
            # print("GNOME     FITNESS VALUE")
            # for pop in population:
            #     print(pop.gnome, pop.fitness)
        gen += 1
    #
    # print("\nFinal Generation", "Best Fitness", best_fitness)
    # print("GNOME     FITNESS VALUE")
    # for pop in population:
    #     print(pop.gnome, pop.fitness)

    # x = np.arange(len(best_fitness_over_time))  # X-axis points
    # y = best_fitness_over_time # Y-axis points
    #
    # plt.plot(x, y)  # Plot the chart
    # plt.show()  # display
    #

if __name__ == "__main__":
   RunMaCHazineTSP()


