import GPyOpt
import numpy as np

from solarsystem import SolarSystem, Sun, Planet


def simulate_system_third_body_position_lagrange(var):
    solar_system = SolarSystem(width=1000, height=1000)

    suns = (
        Sun(solar_system, mass=10_000, position=(0, 0), velocity=(0, 0))
    )

    planets = (
        Planet(solar_system, mass=0.3, position=(200, 0), velocity=(0, 7)),
        Planet(solar_system, mass=0.00001, position=(var[0][0].item(), 0), velocity=(0, var[0][1].item())),
    )


    for i in range(1000):
        solar_system.calculate_all_body_interactions()
        solar_system.update_all()

    return np.float(solar_system.biggest_distance_loss)


space = [{'name': 'x', 'type': 'continuous', 'domain': (-205, -195)},  # [(-7, -3), (3, 7)]},
         {'name': 'y', 'type': 'continuous', 'domain': (-14, 14)}]  # [(-7, -3), (3, 7)]}]
# {'name': 'vx', 'type': 'continuous', 'domain': (-5, 5)}]
# {'name': 'vy', 'type': 'continuous', 'domain': (-5, 5)}]

stability = GPyOpt.methods.BayesianOptimization(f=simulate_system_third_body_position_lagrange,
                                                domain=space)

stability.run_optimization(50)
stability.plot_acquisition()
print(stability.get_evaluations())