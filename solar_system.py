# solarsystem.py

import itertools
import math
import numpy as np
import matplotlib.pyplot as plt

# Solar System Bodies
class SolarSystemBody():
    min_display_size = 200
    display_log_base = 1.1
    def __init__(
            self,
            solar_system,
            mass,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__()
        self.history = []
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.display_size = max(
            math.log(self.mass, self.display_log_base),
            self.min_display_size,
        )
        solar_system.add_body(self)

    def move(self):
        self.history.append([self.position[0], self.position[1]])
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def distance(self, planet):
        value = math.sqrt((self.position[0] - planet.position[0])**2 + (self.position[1] - planet.position[1])**2)
        #print(value)
        return value

    def towards(self, planet):
        x = planet.position[0]
        y = planet.position[1]
        x = x - self.position[0]
        y = y - self.position[1]
        return round(math.atan2(y,x)*180.0/math.pi, 10) % 360.0


class Sun(SolarSystemBody):
    def __init__(
            self,
            solar_system,
            mass,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__(solar_system, mass, position, velocity)
        self.color = "y"



class Planet(SolarSystemBody):
    colours = itertools.cycle(["red", "green", "blue"])

    def __init__(
            self,
            solar_system,
            mass,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__(solar_system, mass, position, velocity)
        self.color= next(Planet.colours)


# Solar System
class SolarSystem:
    def __init__(self, width, height):
        self.biggest_distance_loss = 0
        self.second_planet_radius = None
        #self.solar_system
        self.bodies = []

    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        #body.clear()
        self.bodies.remove(body)

    def update_all(self):
        for body in self.bodies:
            body.move()

        self.biggest_distance_loss_three_body()
        #self.solar_system.update()

    @staticmethod
    def accelerate_due_to_gravity(
            first: SolarSystemBody,
            second: SolarSystemBody,
    ):
        if first.distance(second) != 0:
            force = first.mass * second.mass / first.distance(second) ** 2
        else:
            force = first.mass * second.mass / 0.000000001
        angle = first.towards(second)
        reverse = 1
        for body in first, second:
            acceleration = force / body.mass
            acc_x = acceleration * math.cos(math.radians(angle))
            acc_y = acceleration * math.sin(math.radians(angle))
            body.velocity = (
                body.velocity[0] + (reverse * acc_x),
                body.velocity[1] + (reverse * acc_y),
            )
            reverse = -1

    def check_collision(self, first, second):
        if isinstance(first, Planet) and isinstance(second, Planet):
            return
        if first.distance(second) == 0 or second.distance(first) == 0:
            for body in first, second:
                if isinstance(body, Planet):
                    print('colision')
                    self.remove_body(body)
                    self.biggest_distance_loss = 1000
        if first.distance(second) < first.display_size/2 + second.display_size/2:
            for body in first, second:
                if isinstance(body, Planet):
                    print('colision')
                    self.remove_body(body)
                    self.biggest_distance_loss = 1000

    def calculate_all_body_interactions(self):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                self.accelerate_due_to_gravity(first, second)
                self.check_collision(first, second)

    def biggest_distance_loss_three_body(self):
        for body in self.bodies:
            body_initial_radius = math.sqrt(body.history[0][0] ** 2 + body.history[0][1] ** 2)
            body_present_radius = math.sqrt(body.position[0]**2 + body.position[1]**2)
            loss_radius = math.log(abs(body_initial_radius - body_present_radius))

            if loss_radius > self.biggest_distance_loss:
                self.biggest_distance_loss = loss_radius

    def plot_trajectories(self):
        for body in self.bodies:
            hist = np.array(body.history).T
            plt.plot(hist[0], hist[1])
            plt.scatter(hist[0][0], hist[1][0], s=100)
        plt.show()

    def plot_trajectories_time(self, until_time):
        for body in self.bodies:
            hist = np.array(body.history[:until_time]).T
            plt.plot(hist[0], hist[1], body.color)
            plt.scatter(hist[0][0], hist[1][0], c=body.color, s=100)
        plt.show()

