import math

import GPyOpt
import numpy as np

from solar_system import SolarSystem, Sun, Planet

mass = 1
nr_bodies = 3
def simulate_n_gon_system_small_search(var):
    solar_system = SolarSystem(width=1000, height=1000)
    radius, v_x, v_y = var[0][0], var[0][1], var[0][2]

    coordinates = coordinates_n_gon(radius, nr_bodies)
    velocities = velocities_n_gon(v_x, v_y, nr_bodies)

    for i in range(nr_bodies):
        Planet(solar_system, mass=mass, position=(coordinates[i][0], coordinates[i][1]),
               velocity=(velocities[i][0], velocities[i][1]))

    for i in range(1000):
        solar_system.calculate_all_body_interactions()
        solar_system.update_all()

    return np.float(solar_system.biggest_distance_loss)


def velocities_n_gon(v_x, v_y, n):
    velocities = []
    for i in range(n):
        cos = math.cos(2 * math.pi * i / n)
        sin = math.sin(2 * math.pi * i / n)
        velocities.append([v_x * cos - v_y * sin, v_x * sin + v_y * cos])

    return velocities


def coordinates_n_gon(radius, n):
    coordinates = []
    for i in range(n):
        x = radius * math.cos(2 * math.pi * i / n)
        y = radius * math.sin(2 * math.pi * i / n)
        coordinates.append([x,y])

    return coordinates

# var[0] = radius
def simulate_n_gon_system_big_search(var):
    solar_system = SolarSystem(width=1000, height=1000)

    coordinates = coordinates_n_gon(var[0][0], 2)
    for i in range(2):
        Planet(solar_system, mass=2, position=(coordinates[i][0], coordinates[i][1]), velocity=(var[0][2*i + 1], var[0][2*i + 1]))

    for i in range(1000):
        solar_system.calculate_all_body_interactions()
        solar_system.update_all()

    return np.float(solar_system.biggest_distance_loss)

def evaluate_solution_for_n_gon(n_gon):

    var = n_gon.x_opt
    solar_system = SolarSystem(width=1000, height=1000)

    radius, v_x, v_y = var[0], var[1], var[2]
    coordinates = coordinates_n_gon(radius, nr_bodies)
    velocities = velocities_n_gon(v_x, v_y, nr_bodies)

    for i in range(nr_bodies):
        Planet(solar_system, mass=mass, position=(coordinates[i][0], coordinates[i][1]),
               velocity=(velocities[i][0], velocities[i][1]))

    for i in range(10000):
        solar_system.calculate_all_body_interactions()
        solar_system.update_all()

    print(solar_system.biggest_distance_loss)
    print(n_gon.x_opt)
    solar_system.plot_trajectories()

def run_big_experiment():
    space = [{'name': 'radius', 'type': 'continuous', 'domain': (50, 100)},
             {'name': 'vel_obj_1_x', 'type': 'continuous', 'domain': (-14, 14)},
             {'name': 'vel_obj_1_y', 'type': 'continuous', 'domain': (-14, 14)},
             {'name': 'vel_obj_2_x', 'type': 'continuous', 'domain': (-14, 14)},
             {'name': 'vel_obj_2_y', 'type': 'continuous', 'domain': (-14, 14)},]

    n_gon = GPyOpt.methods.BayesianOptimization(f=simulate_n_gon_system_big_search,
                                                    domain=space)

    n_gon.run_optimization(100)
    n_gon.plot_acquisition()

    print(n_gon.get_evaluations())
    evaluate_solution_for_n_gon(n_gon)

def run_small_experiment():
    space = [{'name': 'radius', 'type': 'continuous', 'domain': (0, 10)},
             {'name': 'vel_obj_1_x', 'type': 'continuous', 'domain': (-10, 10)},
             {'name': 'vel_obj_1_y', 'type': 'continuous', 'domain': (-10, 10)},]

    n_gon = GPyOpt.methods.BayesianOptimization(f=simulate_n_gon_system_small_search,
                                                    domain=space)

    print(n_gon.get_evaluations())
    for i in range(4):
        n_gon.run_optimization(100)
        evaluate_solution_for_n_gon(n_gon)



run_small_experiment()