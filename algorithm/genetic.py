import random
import numpy as np
import math
import matplotlib.pyplot as plt
import copy

INT_MAX = 100000000000 
# Number of cities in TSP
NUM_LOCATIONS = 30

# Initial population size for the algorithm
POP_SIZE = 20

# Vehicles
NUM_BIKES = 3
NUM_CARS = 1

BIKE_CAPACITY = 20
CAR_PENALTY = 1.20 # Percentage penalty for using a car

NUM_GENERATIONS = 200000

NUM_VEHICLES = NUM_BIKES + NUM_CARS


# Structure of a GNOME
# defines the path traversed
# by the salesman while the fitness value
# of the path is stored in an integer

# Temporary fake matrix generator
def generate_points(max_range=100):
    points = [(round(random.uniform(0, max_range),3), round(random.uniform(0, max_range), 3)) for _ in range(NUM_LOCATIONS)]
    return points

def create_distance_matrix():
    points = generate_points()
    matrix = [[0 for _ in range(len(points))] for _ in range(len(points))]
    for i, p in enumerate(points):
        for j, q in enumerate(points): 
            matrix[i][j] = get_distance(p, q)
    return matrix

def create_ewi_distances(max_range=100):
    return [round(random.uniform(0, max_range),3) for _ in range(NUM_LOCATIONS)]


def get_distance(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

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
    vehicle = rand_num(0, NUM_VEHICLES)
    gnome_v = gnome[vehicle][:]
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
    gnome[vehicle] = gnome_v
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

    moved_location = gnome[source_v][rand_num(0, len(gnome[source_v]))]
    gnome[source_v].remove(moved_location)

    if len(gnome[dest_v]) == 0:
        gnome[dest_v] = [moved_location]
    else:
        insert_in = rand_num(0, len(gnome[dest_v]))
        gnome[dest_v].insert(insert_in, moved_location)
        # gnome[dest_v] = gnome[dest_v][:random_split] + moved_letter + gnome[dest_v][random_split:]
        # gnome[dest_v] = gnome[dest_v] + moved_letter
    
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

def ewi_distance(place):
    return (BIKE_TIME_EWI[place], CAR_TIME_EWI[place]) 


def get_addresses_cost(start, end):
    return (BIKE_TIME_MATRIX[start][end], CAR_TIME_MATRIX[start][end]) 

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
    if len(partial_gnome) == 0:
        return 0
    if vehicle_type == 0 and len(partial_gnome) > BIKE_CAPACITY:
        return INT_MAX
    f = ewi_distance(partial_gnome[0])[vehicle_type] + ewi_distance(partial_gnome[-1])[vehicle_type]
    # print(partial_gnome)
    for i in range(len(partial_gnome) - 1):
        # if get_addresses_cost(partial_gnome[i], partial_gnome[i + 1])[vehicle_type] == INT_MAX:
            # return INT_MAX
        f += get_addresses_cost(partial_gnome[i], partial_gnome[i + 1])[vehicle_type]
    
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

    print("\nInitial population: \nGNOME     FITNESS VALUE\n")
    for i in range(POP_SIZE):
        print(population[i].gnome, population[i].fitness)
    print()

    while gen <= NUM_GENERATIONS:
        new_population = population[0:int(POP_SIZE/5)] # elitism on best 20% of gnomes

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
            print("\nGeneration", gen, "Best Fitness", best_fitness)
            print("GNOME     FITNESS VALUE")
            for pop in population:
                print(pop.gnome, pop.fitness)
        gen += 1

    print("\nFinal Generation", "Best Fitness", best_fitness)
    print("GNOME     FITNESS VALUE")
    for pop in population:
        print(pop.gnome, pop.fitness)
    
    x = np.arange(len(best_fitness_over_time))  # X-axis points
    y = best_fitness_over_time # Y-axis points
 
    plt.plot(x, y)  # Plot the chart
    plt.show()  # display


if __name__ == "__main__":
   RunMaCHazineTSP()


