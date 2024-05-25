import math 
import random
import matplotlib.pyplot as plt

def generate_points(n, max_range=100):
    points = [(round(random.uniform(0, max_range),3), round(random.uniform(0, max_range), 3)) for _ in range(n)]
    return points

def create_distance_matrix(points):
    matrix = [[0 for _ in range(len(points))] for _ in range(len(points))]
    for i, p in enumerate(points):
        for j, q in enumerate(points): 
            matrix[i][j] = get_distance(p, q)

    return matrix

def get_distance(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def print_distance_matrix(matrix):
    for row in matrix:
        print(" ".join(str(round(elem, 3)) for elem in row))

if __name__ == '__main__':
    points = generate_points(10)
    dist_matrix = create_distance_matrix(points)
    print(dist_matrix)
    # print_distance_matrix(dist_matrix)
    # plot_points(points)
