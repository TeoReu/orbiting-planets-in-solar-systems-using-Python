import math

import GPyOpt
import numpy as np
from matplotlib import pyplot as plt

from solar_system import SolarSystem, Planet, Sun

mass = 10000
loss = "area"
nr_bodies = 3
var = [316.27167284, 0,  -5.3581742]

def simulate_ngon_space_1p(var_1p, dim=2):
    solar_system = SolarSystem(width=1000, height=1000, loss=loss)
    if dim == 3:
        radius, v_x, v_y = var[0], var[1], var[2]
    elif dim == 2:
        radius, v_x, v_y = var[0], var[1], var[2]


    coordinates = coordinates_n_gon(radius)
    velocities = velocities_n_gon(v_x, v_y)

    for i in range(nr_bodies):
        Sun(solar_system, mass=mass, position=(coordinates[i][0], coordinates[i][1]),
               velocity=(velocities[i][0], velocities[i][1]))

    solar_system.configuration = var_1p

    Planet(solar_system, mass=3, position= (0, var_1p[0][0]), velocity = (0, var_1p[0][1]))
    for i in range(2000):
        solar_system.calculate_all_body_interactions()
        solar_system.update_all()

    return np.float(solar_system.loss)


def velocities_n_gon(v_x, v_y):
    n=3
    velocities = []
    for i in range(n):
        cos = math.cos(2 * math.pi * i / n)
        sin = math.sin(2 * math.pi * i / n)
        velocities.append([v_x * cos - v_y * sin, v_x * sin + v_y * cos])

    return velocities


def coordinates_n_gon(radius):
    n=3
    coordinates = []
    for i in range(n):
        x = radius * math.cos(2 * math.pi * i / n)
        y = radius * math.sin(2 * math.pi * i / n)
        coordinates.append([x,y])

    return coordinates


def evaluate_solution_for_n_gon(n_gon, dim=2):

    var_1p = n_gon.x_opt
    solar_system = SolarSystem(width=1000, height=1000, loss=loss)
    if dim == 3:
        radius, v_x, v_y = var[0], var[1], var[2]
    elif dim == 2:
        radius, v_x, v_y = var[0], var[1], var[2]


    coordinates = coordinates_n_gon(radius)
    velocities = velocities_n_gon(v_x, v_y)

    for i in range(nr_bodies):
        Sun(solar_system, mass=mass, position=(coordinates[i][0], coordinates[i][1]),
               velocity=(velocities[i][0], velocities[i][1]))

    Planet(solar_system, mass=3, position= (0, var_1p[0]), velocity = (0, var_1p[1]))
    solar_system.configuration = var
    for i in range(2000):
        solar_system.calculate_all_body_interactions()
        solar_system.update_all()

    print(solar_system.loss)
    print(n_gon.x_opt)
    print(n_gon.fx_opt)
    solar_system.plot_trajectories_at_times("3s_1p_")
    n_gon.plot_acquisition('aquisition_plots/' + solar_system.name + str(n_gon.domain[0]['domain']) + ".jpg")
    n_gon.save_report('reports/'+ solar_system.name + str(n_gon.domain[0]['domain']) +'.txt')

def plot_it_experiments(vec):
    solar_system = SolarSystem(width=1000, height=1000, loss=loss)

    radius, v_x, v_y = var[0], var[1], var[2]


    coordinates = coordinates_n_gon(radius)
    velocities = velocities_n_gon(v_x, v_y)

    for i in range(nr_bodies):
        Sun(solar_system, mass=mass, position=(coordinates[i][0], coordinates[i][1]),
               velocity=(velocities[i][0], velocities[i][1]))

    Planet(solar_system, mass=3, position= (520, 0), velocity = (0, -12))
    solar_system.configuration = var
    for i in range(70):
        solar_system.calculate_all_body_interactions()
        solar_system.update_all()

    solar_system.plot_trajectories_time(1000)

def increasing_radius_solutions():
    for radius_domain in [(400, 750), (750,1000)]:
        space = [{'name': 'radius', 'type': 'continuous', 'domain': radius_domain},
                 {'name': 'vel_obj_1_y', 'type': 'continuous', 'domain': (0, 20)}]

        n_gon = GPyOpt.methods.BayesianOptimization(f=simulate_ngon_space_1p,
                                                    domain=space, maximize=False, model_type="GP")

        n_gon.run_optimization(100)
        evaluate_solution_for_n_gon(n_gon)



#increasing_radius_solutions()




#[316.27167284, 0,  -5.3581742 ]

#fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(1, 6)
#plot_it_experiments([209.37481282,  -0.30809499,   6.86746548])
#fig.savefig("experiments.png")
plot_it_experiments([0,0 ,0])
#plot_trajectories_time(self, until_time):
#plot_it_experiments([209.37481282,-0.30809499,6.86746548])
#plot_it_experiments([235.02291814,  -1.67994131,  -6.05281996])