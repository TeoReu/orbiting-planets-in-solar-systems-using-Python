# binary_star_system.py
from solarsystemturtle import SolarSystem, Sun, Planet

solar_system = SolarSystem(width=1400, height=900)

suns = (
    Sun(solar_system, mass=10000, position=(-156.70230254, 0), velocity=(0.20096113, 2.0067794)),
    Sun(solar_system, mass=10000, position=(156.70230254, 0), velocity=(-0.20096113, -2.0067794)),
)

planets = (
)

for i in range(1000):
    solar_system.calculate_all_body_interactions()
    solar_system.update_all()

#solar_system.plot_trajectories(50)