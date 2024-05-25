# Python3 implementation of the above approach
import random
import numpy as np


INT_MAX = 100000000000 # Path not possible 
# Number of cities in TSP
NUM_LOCATIONS = 5

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
    mutation_type = rand_num(0, 2) # 0 is change route, 1 is change vehicle
    if mutation_type == 0:
        return mutate_gnome_route(gnome)
    else:
        return mutate_gnome_vehicle(gnome)

# Change the order of two destinations within one vehicle
def mutate_gnome_route(gnome):
    vehicle = rand_num(0, NUM_VEHICLES)
    gnome_v = list(gnome[vehicle])
    if len(gnome_v) == 0 or len(gnome_v) == 1:
        return mutate_gnome_route(gnome)
        # return gnome
    while True:
        r = rand_num(0, len(gnome_v))
        r1 = rand_num(0, len(gnome_v))
        if r1 != r:
            temp = gnome_v[r]
            gnome_v[r] = gnome_v[r1]
            gnome_v[r1] = temp
            break
    gnome[vehicle] = ''.join(gnome_v)
    return gnome

# Take a random address from one vehicle to a random other one
def mutate_gnome_vehicle(gnome):
    source_v = rand_num(0, NUM_VEHICLES)
    dest_v = rand_num(0, NUM_VEHICLES)
    if source_v == dest_v:
        # return gnome
        return mutate_gnome_vehicle(gnome)

    # gnome_v_source = gnome[source_v]
    # gnome_v_dest = gnome[dest_v]

    if len(gnome[source_v]) == 0:
        return mutate_gnome_vehicle(gnome)

    moved_letter = gnome[source_v][rand_num(0, len(gnome[source_v]))]
    gnome[source_v] = gnome[source_v].replace(moved_letter, "")
    if len(gnome[dest_v]) == 0:
        gnome[dest_v] = moved_letter
    else:
        random_split = rand_num(0, len(gnome[dest_v]))
        gnome[dest_v] = gnome[dest_v][:random_split] + moved_letter + gnome[dest_v][random_split:]
        # gnome[dest_v] = gnome[dest_v] + moved_letter
    
    return gnome


# Function to return a valid GNOME string
# required to create the population
def create_gnome():
    gnome = [""] * NUM_VEHICLES
    
    for i in range(NUM_LOCATIONS):
        chosen_vehicle = rand_num(0, NUM_VEHICLES)
        gnome[chosen_vehicle] += str(i)
    
    for i in range(len(gnome)):
        temp = list(gnome[i])
        random.shuffle(temp)
        gnome[i] = "".join(temp)
        
    print("final gnome", gnome, cal_fitness(gnome))
    return gnome

def get_addresses_cost(start, end):
    time_bike = [
        [0, 4, 2, 10, 10],
        [4, 0, 9, 8, 100],
        [2, 9, 0, 3, 3],
        [10, 8, 3, 0, 13],
        [10, 100, 3, 13, 0],
    ]
    time_car = [
        [0, 2, INT_MAX, 12, 5],
        [2, 0, 4, 8, 40],
        [INT_MAX, 4, 0, 3, 3],
        [12, 8, 3, 0, 10],
        [5, 40, 3, 10, 0],
    ]
    return (time_bike[start][end], time_car[start][end])

# Function to return the fitness value of a gnome.
# The fitness value is the path length
# of the path represented by the GNOME.
def cal_fitness(gnome):
    f = 0
    for veh in range(NUM_VEHICLES):
        cur_fitness = fitness_one_vehicle(gnome[veh], 0 if veh < NUM_BIKES else 1)
        if cur_fitness == INT_MAX:
            return INT_MAX
        f += cur_fitness
    return f

def fitness_one_vehicle(partial_gnome, vehicle_type):
    f = 0
    for i in range(len(partial_gnome) - 1):
        if get_addresses_cost(ord(partial_gnome[i]) - 48, ord(partial_gnome[i + 1]) - 48)[vehicle_type] == INT_MAX:
            return INT_MAX
        f += get_addresses_cost(ord(partial_gnome[i]) - 48, ord(partial_gnome[i + 1]) - 48)[vehicle_type]

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
    gen_thres = 100

    population = []

    # Populating the GNOME pool.
    for i in range(POP_SIZE):
        temp = individual()
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
    while temperature > 100 and gen <= gen_thres:
        population.sort()
        print("\nCurrent temp: ", temperature)
        new_population = []

        for i in range(POP_SIZE):
            p1 = population[i]

            while True:
                new_g = mutate_gnome(p1.gnome)
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
        best_fitness = INT_MAX
        for i in range(POP_SIZE):
            best_fitness = min(population[i].fitness, best_fitness)
        print("Generation", gen, "Best Fitness", best_fitness)
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

