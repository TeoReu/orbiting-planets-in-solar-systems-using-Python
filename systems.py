import GPyOpt
import numpy as np

from solarsystem import SolarSystem, Sun, Planet, Earth
import math

angle = (math.pi/3)
velocity = 7.07

def simulate_system_third_body_position_lagrange(var):
    solar_system = SolarSystem(width=1000, height=1000)
    print((math.cos(var[0][0].item())*200,math.sin(var[0][0].item())*200))
    sun = Sun(solar_system, mass=10_000, position=(0, 0), velocity=(0, 0))

    suns = (
        sun
    )

    # Always add earth before 1 planet for lagrange calculations
    planets = (
        Earth(solar_system, mass=0.3, position=(200, 0), sun=sun),

        # L1, L2, and L3
        #Planet(solar_system, mass=0.00000001, position=(var[0][0].item(), 0), velocity=(0, var[0][1].item())),

        # L4
        #Planet(solar_system, mass=0.00000001, position=(var[0][0].item(), var[0][1].item()), velocity=(-math.sin(angle) * velocity , math.cos(angle) * velocity)),
        #Planet(solar_system, mass=0.00000001, position=(var[0][0].item(), var[0][1].item()), velocity=7.07),

        Planet(solar_system, mass=0.00000001, position=(math.cos(var[0][0].item())*200+0.00001,math.sin(var[0][0].item())*200+0.00001), velocity=var[0][1].item()),

        #Planet(solar_system, mass=0.00000001, position=(100, 0.866*200), velocity=7.07)
    )

    #Uncomment for visualisation
    # for i in range(1000):
    #     solar_system.calculate_all_body_interactions()
    #     solar_system.update_all()
    #     for i in solar_system.bodies:
    #         print(i.pos())
    #
    #     print("")


    solar_system.accumulated_distance_and_angle_loss_three_body(10000)
    return solar_system.biggest_angle_loss

#print(simulate_system_third_body_position_lagrange(0))


# space = [{'name': 'x', 'type': 'continuous', 'domain': (50, 150)},  # [(-7, -3), (3, 7)]},
#          {'name': 'y', 'type': 'continuous', 'domain': (-250, 250)},]
#          #{'name': 'v', 'type': 'continuous', 'domain': (6, 9)},]  # [(-7, -3), (3, 7)]}]
#
space = [{'name': 'angle', 'type': 'continuous', 'domain': (0, math.pi*2)},  # [(-7, -3), (3, 7)]},
         {'name': 'v', 'type': 'continuous', 'domain': (6, 8)},]


stability = GPyOpt.methods.BayesianOptimization(f=simulate_system_third_body_position_lagrange,
                                                domain=space)

stability.run_optimization(100)
stability.plot_acquisition()
print(stability.get_evaluations())
print(stability.x_opt)
print(stability.fx_opt)