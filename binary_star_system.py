# binary_star_system.py
from solar_system import SolarSystem, Sun, Planet

solar_system = SolarSystem(width=1400, height=900)

suns = (
    Sun(solar_system, mass=10000, position=(-200, 0), velocity=(0, 3)),
    Sun(solar_system, mass=10000, position=(200, 0), velocity=(0, -3)),
)

planets = (
)

for i in range(200):
    solar_system.calculate_all_body_interactions()
    solar_system.update_all()

solar_system.plot_trajectories(50)