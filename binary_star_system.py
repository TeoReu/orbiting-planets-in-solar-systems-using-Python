# binary_star_system.py
from solarsystemturtle import SolarSystem, Sun, Planet

solar_system = SolarSystem(width=1400, height=900)

suns = (
    Sun(solar_system, mass=10000, position=(-200, 0), velocity=(0, 3)),
    Sun(solar_system, mass=10000, position=(200, 0), velocity=(0, -3)),
)

planets = (
)

while True:
    solar_system.calculate_all_body_interactions()
    solar_system.update_all()
