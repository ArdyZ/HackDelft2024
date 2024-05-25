# Python3 implementation of the above approach
from random import randint
import numpy as np


INT_MAX = 2147483647
# Number of cities in TSP
V = 5

# Names of the cities
GENES = "ABCDE"

# Starting Node Value
START = 0

# Initial population size for the algorithm
POP_SIZE = 10

# Vehicles
NUM_BIKES = 1
NUM_CARS = 1

NUM_VEHICLES = NUM_BIKES + NUM_CARS

# Structure of a GNOME
# defines the path traversed
# by the salesman while the fitness value
# of the path is stored in an integer


class individual:
    def __init__(self) -> None:
        self.gnome = [""] * NUM_VEHICLES
        self.fitness = 0

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness


# Function to return a random number
# from start and end
def rand_num(start, end):
    return randint(start, end-1)


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
def mutatedGene(gnome):
    gnome = list(gnome)
    while True:
        r = rand_num(1, V)
        r1 = rand_num(1, V)
        if r1 != r:
            temp = gnome[r]
            gnome[r] = gnome[r1]
            gnome[r1] = temp
            break
    return ''.join(gnome)


# Function to return a valid GNOME string
# required to create the population
def create_gnome():
    gnome = np.zeros((NUM_VEHICLES, V), dtype=int)
    gnome -= 1

    for city in range(V):
        picked_vehicle =  rand_num(0, NUM_VEHICLES)
        gnome[picked_vehicle, city] = 0

    # print("start\n", gnome)
        
    for vehicle in range(NUM_VEHICLES):
        zeroes = np.where(gnome[vehicle,:] == 0)[0]
        order = np.arange(len(zeroes))
        np.random.shuffle(order)
        # print("zeroes\n", order)
        for value, putindex in enumerate(zeroes):
            gnome[vehicle, putindex] = order[value]
        
    print("final\n", gnome)
    return gnome

def get_addresses_cost(start, end):
    time_bike = [
        [0, 4, INT_MAX, 10, 10],
        [4, 0, 9, 8, INT_MAX],
        [INT_MAX, 9, 0, 3, 3],
        [10, 8, 3, 0, 13],
        [10, INT_MAX, 3, 13, 0],
    ]
    time_car = [
        [0, 2, INT_MAX, 12, 5],
        [2, 0, 4, 8, INT_MAX],
        [INT_MAX, 4, 0, 3, 3],
        [12, 8, 3, 0, 10],
        [5, INT_MAX, 3, 10, 0],
    ]
    return (time_bike[start, end], time_car[start, end])

# Function to return the fitness value of a gnome.
# The fitness value is the path length
# of the path represented by the GNOME.
def cal_fitness(gnome):

    f = 0
    for veh in range(NUM_VEHICLES):
        pass

    return f


# Function to return the updated value
# of the cooling element.
def cooldown(temp):
    return (90 * temp) / 100


# Comparator for GNOME struct.
# def lessthan(individual t1,
#               individual t2)
# :
#     return t1.fitness < t2.fitness


# Utility function for TSP problem.
def TSPUtil(mp):
    # Generation Number
    gen = 1
    # Number of Gene Iterations
    gen_thres = 5

    population = []
    temp = individual()

    # Populating the GNOME pool.
    for i in range(POP_SIZE):
        temp.gnome = create_gnome()
        temp.fitness = cal_fitness(temp.gnome)
        population.append(temp)

    print("\nInitial population: \nGNOME     FITNESS VALUE\n")
    for i in range(POP_SIZE):
        print(population[i].gnome, population[i].fitness)
    print()

    found = False
    temperature = 10000

    # Iteration to perform
    # population crossing and gene mutation.
    while temperature > 1000 and gen <= gen_thres:
        population.sort()
        print("\nCurrent temp: ", temperature)
        new_population = []

        for i in range(POP_SIZE):
            p1 = population[i]

            while True:
                new_g = mutatedGene(p1.gnome)
                new_gnome = individual()
                new_gnome.gnome = new_g
                new_gnome.fitness = cal_fitness(new_gnome.gnome)

                if new_gnome.fitness <= population[i].fitness:
                    new_population.append(new_gnome)
                    break

                else:

                    # Accepting the rejected children at
                    # a possible probability above threshold.
                    prob = pow(
                        2.7,
                        -1
                        * (
                            (float)(new_gnome.fitness - population[i].fitness)
                            / temperature
                        ),
                    )
                    if prob > 0.5:
                        new_population.append(new_gnome)
                        break

        temperature = cooldown(temperature)
        population = new_population
        print("Generation", gen)
        print("GNOME     FITNESS VALUE")

        for i in range(POP_SIZE):
            print(population[i].gnome, population[i].fitness)
        gen += 1


if __name__ == "__main__":

    mp = [
        [0, 2, INT_MAX, 12, 5],
        [2, 0, 4, 8, INT_MAX],
        [INT_MAX, 4, 0, 3, 3],
        [12, 8, 3, 0, 10],
        [5, INT_MAX, 3, 10, 0],
    ]
    TSPUtil(mp)

