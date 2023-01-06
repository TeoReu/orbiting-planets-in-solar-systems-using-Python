# binary_star_system.py
from solarsystemturtle import SolarSystem, Sun, Planet

solar_system = SolarSystem(width=1400, height=900)


suns = (
    Sun(solar_system, mass=100, position=(5, 5), velocity=(5, 5)),
    Sun(solar_system, mass=100, position=(-5, 5), velocity=(-5, 5)),
    Sun(solar_system, mass=100, position=(5, -5), velocity=(5, -5)),
    Sun(solar_system, mass=100, position=(-5, -5), velocity=(-5, -5))
)


while True:
    solar_system.calculate_all_body_interactions()
    solar_system.update_all()
